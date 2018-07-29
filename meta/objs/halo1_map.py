from math import pi, sqrt, log
from os.path import exists, join
from struct import pack_into
from tkinter.filedialog import askopenfilename
from traceback import format_exc

from .halo_map import *
from reclaimer.hek.defs.sbsp import sbsp_meta_header_def
from reclaimer.os_hek.defs.gelc    import gelc_def
from reclaimer.os_v4_hek.defs.coll import fast_coll_def
from reclaimer.os_v4_hek.defs.sbsp import fast_sbsp_def
from reclaimer.os_v4_hek.handler   import OsV4HaloHandler
from .halo1_rsrc_map import Halo1RsrcMap, inject_sound_data
from .byteswapping import raw_block_def, byteswap_animation,\
     byteswap_uncomp_verts, byteswap_comp_verts, byteswap_tris,\
     byteswap_coll_bsp, byteswap_sbsp_meta, byteswap_scnr_script_syntax_data,\
     byteswap_pcm16_samples
from reclaimer import data_extraction


__all__ = ("Halo1Map", "Halo1RsrcMap")


class Halo1Map(HaloMap):
    ce_rsrc_sound_indexes_by_path = None
    ce_tag_indexs_by_paths = None
    tag_headers = None
    sound_rsrc_id = None
    defs = None

    force_checksum = False

    inject_rawdata = Halo1RsrcMap.inject_rawdata

    def __init__(self, maps=None):
        HaloMap.__init__(self, maps)
        self.ce_rsrc_sound_indexes_by_path = {}
        self.ce_tag_indexs_by_paths  = {}
        self.setup_tag_headers()

    def setup_tag_headers(self):
        if Halo1Map.tag_headers is not None:
            return

        tag_headers = Halo1Map.tag_headers = {}
        for def_id in sorted(self.defs):
            if def_id in tag_headers or len(def_id) != 4:
                continue
            h_desc, h_block = self.defs[def_id].descriptor[0], [None]
            h_desc['TYPE'].parser(h_desc, parent=h_block, attr_index=0)
            tag_headers[def_id] = bytes(
                h_block[0].serialize(buffer=BytearrayBuffer(),
                                     calc_pointers=False))

    def ensure_sound_maps_valid(self):
        sounds = self.maps.get("sounds")
        if not sounds or self.is_resource:
            return

        if id(sounds) != self.sound_rsrc_id:
            pass
        elif not(self.ce_rsrc_sound_indexes_by_path and
                 self.ce_tag_indexs_by_paths):
            pass
        else:
            return

        self.sound_rsrc_id = id(sounds)
        if self.engine in ("halo1ce", "halo1yelo"):
            # ce resource sounds are recognized by tag_path
            # so we must cache their offsets by their paths
            rsrc_snd_map = self.ce_rsrc_sound_indexes_by_path = {}
            inv_snd_map  = self.ce_tag_indexs_by_paths = {}

            if sounds is not None:
                i = 0
                for tag_header in sounds.rsrc_header.tag_paths:
                    rsrc_snd_map[tag_header.tag_path] = i
                    i += 1

            i = 0
            for tag_header in self.tag_index.tag_index:
                inv_snd_map[tag_header.tag.tag_path] = i
                i += 1

    def get_dependencies(self, meta, tag_id, tag_cls):
        if self.is_indexed(tag_id):
            if tag_cls != "snd!":
                return ()

            rsrc_id = meta.promotion_sound.id[0]
            if rsrc_id == 0xFFFF: return ()

            sounds = self.maps.get("sounds")
            rsrc_id = rsrc_id // 2
            if   sounds is None: return ()
            elif rsrc_id >= len(sounds.tag_index.tag_index): return ()

            tag_path = sounds.tag_index.tag_index[rsrc_id].tag.tag_path
            inv_snd_map = getattr(self, 'ce_tag_indexs_by_paths', {})
            tag_id = inv_snd_map.get(tag_path, 0xFFFF)
            if tag_id >= len(self.tag_index.tag_index): return ()

            return [self.tag_index.tag_index[tag_id]]

        if self.handler is None: return ()

        dependency_cache = self.handler.tag_ref_cache.get(tag_cls)
        if not dependency_cache: return ()

        nodes = self.handler.get_nodes_by_paths(dependency_cache, (None, meta))
        dependencies = []

        for node in nodes:
            if node.id[0] == 0xFFFF:
                continue
            dependencies.append(node)
        return dependencies

    def setup_defs(self):
        if Halo1Map.defs is None:
            print("    Loading Halo 1 OSv4 tag definitions...")
            Halo1Map.handler = OsV4HaloHandler(build_reflexive_cache=False,
                                               build_raw_data_cache=False)

            Halo1Map.defs = dict(Halo1Map.handler.defs)
            Halo1Map.defs["sbsp"] = fast_sbsp_def
            Halo1Map.defs["coll"] = fast_coll_def
            Halo1Map.defs["gelc"] = gelc_def
            Halo1Map.defs = FrozenDict(Halo1Map.defs)
            print("        Finished")

        # make a shallow copy for this instance to manipulate
        self.defs = dict(self.defs)

    def load_map(self, map_path, **kwargs):
        autoload_resources = kwargs.get("autoload_resources", True)
        HaloMap.load_map(self, map_path, **kwargs)

        tag_index = self.tag_index
        tag_index_array = tag_index.tag_index

        # record the original halo 1 tag_paths so we know if they change
        self.orig_tag_paths = tuple(b.tag.tag_path for b in tag_index_array)

        # make all contents of the map parasble
        self.basic_deprotection()

        # get the scenario meta
        try:
            self.scnr_meta = self.get_meta(tag_index.scenario_tag_id[0])

            if self.scnr_meta is not None:
                bsp_sizes   = self.bsp_sizes
                bsp_magics  = self.bsp_magics
                bsp_offsets = self.bsp_header_offsets
                for b in self.scnr_meta.structure_bsps.STEPTREE:
                    bsp = b.structure_bsp
                    bsp_offsets[bsp.id.tag_table_index] = b.bsp_pointer
                    bsp_magics[bsp.id.tag_table_index]  = b.bsp_magic
                    bsp_sizes[bsp.id.tag_table_index]   = b.bsp_size

                # read the sbsp headers
                for tag_id, offset in bsp_offsets.items():
                    header = sbsp_meta_header_def.build(rawdata=self.map_data,
                                                        offset=offset)
                    self.bsp_headers[tag_id] = header
                    if header.sig != header.get_desc("DEFAULT", "sig"):
                        print("Sbsp header is invalid for '%s'" %
                              tag_index_array[tag_id].tag.tag_path)
            else:
                print("Could not read scenario tag")

        except Exception:
            print(format_exc())
            print("Could not read scenario tag")

        # get the globals meta
        try:
            matg_id = None
            for b in tag_index_array:
                if fourcc(b.class_1.data) == "matg":
                    matg_id = b.id.tag_table_index
                    break

            self.matg_meta = self.get_meta(matg_id)
            if self.matg_meta is None:
                print("Could not read globals tag")
        except Exception:
            print(format_exc())
            print("Could not read globals tag")

        if autoload_resources:
            self.load_all_resource_maps(dirname(map_path))
        self.map_data.clear_cache()

    def extract_tag_data(self, meta, tag_index_ref, **kw):
        extractor = data_extraction.h1_data_extractors.get(
            fourcc(tag_index_ref.class_1.data))
        if extractor is None:
            return "No extractor for this type of tag."
        kw['halo_map'] = self
        return extractor(meta, tag_index_ref.tag.tag_path, **kw)

    def get_meta(self, tag_id, reextract=False):
        '''
        Takes a tag reference id as the sole argument.
        Returns that tags meta data as a parsed block.
        '''
        if tag_id is None: return
        magic     = self.map_magic
        engine    = self.engine
        map_data  = self.map_data
        tag_index = self.tag_index
        tag_index_array = tag_index.tag_index

        # if we are given a 32bit tag id, mask it off
        tag_id &= 0xFFFF

        tag_index_ref = tag_index_array[tag_id]

        if tag_id != tag_index.scenario_tag_id[0] or self.is_resource:
            tag_cls = None
            if tag_index_ref.class_1.enum_name not in ("<INVALID>", "NONE"):
                tag_cls = fourcc(tag_index_ref.class_1.data)
        else:
            tag_cls = "scnr"

        # if we dont have a defintion for this tag_cls, then return nothing
        if self.get_meta_descriptor(tag_cls) is None:
            return

        self.ensure_sound_maps_valid()

        if tag_cls is None:
            # couldn't determine the tag class
            return
        elif self.is_indexed(tag_id):
            # tag exists in a resource cache
            tag_id = tag_index_ref.meta_offset

            rsrc_map = None
            if tag_cls == "snd!" and "sounds" in self.maps:
                rsrc_map = self.maps["sounds"]
                sound_mapping = self.ce_rsrc_sound_indexes_by_path
                tag_path = tag_index_ref.tag.tag_path
                if sound_mapping is None or tag_path not in sound_mapping:
                    return

                tag_id = sound_mapping[tag_path]//2
            elif tag_cls == "bitm" and "bitmaps" in self.maps:
                rsrc_map = self.maps["bitmaps"]
                tag_id = tag_id//2

            elif "loc" in self.maps:
                rsrc_map = self.maps["loc"]
                # this resource tag is in a yelo loc.map, which means
                # we will need to set its tag class to what this map
                # specifies it as or else the resource map wont know
                # what type of tag to extract it as.
                rsrc_map.tag_index.tag_index[tag_id].class_1.set_to(
                    tag_index_ref.class_1.enum_name)

            if rsrc_map is None:
                return

            return rsrc_map.get_meta(tag_id)
        elif not reextract:
            if tag_id == tag_index.scenario_tag_id[0] and self.scnr_meta:
                return self.scnr_meta
            elif tag_cls == "matg" and self.matg_meta:
                return self.matg_meta

        desc = self.get_meta_descriptor(tag_cls)
        block = [None]
        offset = tag_index_ref.meta_offset - magic
        if tag_cls == "sbsp":
            # bsps use their own magic because they are stored in
            # their own section of the map, directly after the header
            magic  = (self.bsp_magics[tag_id] -
                      self.bsp_header_offsets[tag_id])
            offset = self.bsp_headers[tag_id].meta_pointer - magic

        try:
            # read the meta data from the map
            FieldType.force_little()
            desc['TYPE'].parser(
                desc, parent=block, attr_index=0, magic=magic,
                tag_index=tag_index_array, rawdata=map_data, offset=offset)
            FieldType.force_normal()
        except Exception:
            print(format_exc())
            FieldType.force_normal()
            return

        self.record_map_cache_read(tag_id, 0)  # cant get size quickly enough
        if self.map_cache_over_limit():
            self.clear_map_cache()

        self.inject_rawdata(block[0], tag_cls, tag_index_ref)

        return block[0]

    def meta_to_tag_data(self, meta, tag_cls, tag_index_ref, **kwargs):
        magic      = self.map_magic
        engine     = self.engine
        map_data   = self.map_data
        tag_index  = self.tag_index

        predicted_resources = []

        if hasattr(meta, "obje_attrs"):
            predicted_resources.append(meta.obje_attrs.predicted_resources)


        if tag_cls == "actv":
            # multiply grenade velocity by 30
            meta.grenades.grenade_velocity *= 30
            
        elif tag_cls in ("antr", "magy"):
            # byteswap animation data
            for anim in meta.animations.STEPTREE:
                byteswap_animation(anim)

        elif tag_cls == "bitm":
            # set the size of the compressed plate data to nothing
            meta.compressed_color_plate_data.STEPTREE = BytearrayBuffer()

            # to enable compatibility with my bitmap converter we'll set the
            # base address to a certain constant based on the console platform
            is_xbox = "xbox" in engine or engine in ("stubbs", "shadowrun_beta")

            new_pixels_offset = 0

            # uncheck the prefer_low_detail flag and
            # set up the pixels_offset correctly.
            for bitmap in meta.bitmaps.STEPTREE:
                bitmap.flags.prefer_low_detail = is_xbox
                bitmap.pixels_offset = new_pixels_offset
                new_pixels_offset += bitmap.pixels_meta_size

                # clear some meta-only fields
                bitmap.pixels_meta_size = 0
                bitmap.bitmap_id_unknown1 = bitmap.bitmap_id_unknown2 = 0
                bitmap.bitmap_data_pointer = 0

                if is_xbox:
                    bitmap.base_address = 1073751810
                    if "dxt" in bitmap.format.enum_name:
                        # need to correct mipmap count on xbox dxt bitmaps.
                        # the game seems to prune the mipmap texels for any
                        # mipmaps whose dimensions are 2x2 or smaller

                        max_dim = max(bitmap.width, bitmap.height)
                        if 2 ** bitmap.mipmaps > max_dim:
                            # make sure the mipmap level isnt higher than the
                            # number of mipmaps that should be able to exist.
                            bitmap.mipmaps = int(log(max_dim, 2))

                        last_mip_dim = max_dim // (2 ** bitmap.mipmaps)
                        if last_mip_dim == 1:
                            bitmap.mipmaps -= 2
                        elif last_mip_dim == 2:
                            bitmap.mipmaps -= 1

                        if bitmap.mipmaps < 0:
                            bitmap.mipmaps = 0
                else:
                    bitmap.base_address = 0

        elif tag_cls == "cdmg":
            # divide camera shaking wobble period by 30
            meta.camera_shaking.wobble_function_period /= 30

        elif tag_cls == "coll":
            # byteswap the raw bsp collision data
            for node in meta.nodes.STEPTREE:
                for perm_bsp in node.bsps.STEPTREE:
                    byteswap_coll_bsp(perm_bsp)

        elif tag_cls == "effe":
            # mask away the meta-only flags
            meta.flags.data &= 3

        elif tag_cls == "jpt!":
            # camera shaking wobble period by 30
            meta.camera_shaking.wobble_function_period /= 30

        elif tag_cls == "glw!":
            # increment enumerators properly
            for b in (meta.particle_rotational_velocity,
                      meta.effect_rotational_velocity,
                      meta.effect_translational_velocity,
                      meta.particle_distance_to_object,
                      meta.particle_size,
                      meta.particle_color):
                b.attachment.data += 1

        elif tag_cls == "lens":
            # multiply corona rotation by pi/180
            meta.corona_rotation.function_scale *= pi/180

        elif tag_cls == "ligh":
            # divide light time by 30
            meta.effect_parameters.duration /= 30

        elif tag_cls == "matg":
            # tool will fail to compile any maps if the
            # multiplayer_info or falling_damage is blank

            # make sure there is multiplayer info.
            multiplayer_info = meta.multiplayer_informations.STEPTREE
            if not len(multiplayer_info):
                multiplayer_info.append()

            # make sure there is falling damage info.
            falling_damages = meta.falling_damages.STEPTREE
            if not len(falling_damages):
                falling_damages.append()

        elif tag_cls == "metr":
            # The meter bitmaps can literally point to not
            # only the wrong tag, but the wrong TYPE of tag.
            # Since dependencies in meter tags are useless, we null them out.
            meta.stencil_bitmap.filepath = meta.source_bitmap.filepath = ''

        elif tag_cls in ("mode", "mod2"):
            if engine in ("halo1yelo", "halo1ce", "halo1pc", "halo1pcdemo",
                          "stubbspc"):
                # model_magic seems to be the same for all pc maps
                verts_start = tag_index.model_data_offset
                tris_start  = verts_start + tag_index.vertex_data_size
                model_magic = None
            else:
                model_magic = magic

            if model_magic is None:
                verts_attr_name = "uncompressed_vertices"
                byteswap_verts = byteswap_uncomp_verts
                vert_size = 68

                if engine != "stubbspc":
                    # need to swap the lod cutoff and nodes values around
                    cutoffs = (meta.superlow_lod_cutoff, meta.low_lod_cutoff,
                               meta.high_lod_cutoff, meta.superhigh_lod_cutoff)
                    nodes = (meta.superlow_lod_nodes, meta.low_lod_nodes,
                             meta.high_lod_nodes, meta.superhigh_lod_nodes)
                    meta.superlow_lod_cutoff  = cutoffs[3]
                    meta.low_lod_cutoff       = cutoffs[2]
                    meta.high_lod_cutoff      = cutoffs[1]
                    meta.superhigh_lod_cutoff = cutoffs[0]
                    meta.superlow_lod_nodes  = nodes[3]
                    meta.low_lod_nodes       = nodes[2]
                    meta.high_lod_nodes      = nodes[1]
                    meta.superhigh_lod_nodes = nodes[0]
            else:
                verts_attr_name = "compressed_vertices"
                byteswap_verts = byteswap_comp_verts
                vert_size = 32

            # grab vertices and indices from the map
            for geom in meta.geometries.STEPTREE:
                for part in geom.parts.STEPTREE:
                    verts_block = part[verts_attr_name]
                    tris_block  = part.triangles
                    info  = part.model_meta_info

                    # null out certain things in the part
                    part.previous_part_index = part.next_part_index = 0
                    part.centroid_primary_node = 0
                    part.centroid_secondary_node = 0
                    part.centroid_primary_weight = 0.0
                    part.centroid_secondary_weight = 0.0

                    # make the new blocks to hold the raw data
                    verts_block.STEPTREE = raw_block_def.build()
                    tris_block.STEPTREE  = raw_block_def.build()

                    # read the offsets of the vertices and indices from the map
                    if model_magic is None:
                        verts_off = verts_start + info.vertices_offset
                        tris_off  = tris_start  + info.indices_offset
                    else:
                        map_data.seek(
                            info.vertices_reflexive_offset + 4 - model_magic)
                        verts_off = unpack(
                            "<I", map_data.read(4))[0] - model_magic
                        map_data.seek(
                            info.indices_reflexive_offset  + 4 - model_magic)
                        tris_off  = unpack(
                            "<I", map_data.read(4))[0] - model_magic

                    # read the raw data from the map
                    map_data.seek(verts_off)
                    raw_verts = map_data.read(vert_size*info.vertex_count)
                    map_data.seek(tris_off)
                    raw_tris  = map_data.read(2*(info.index_count + 2))

                    # put the raw data in the verts and tris blocks
                    verts_block.STEPTREE.data = raw_verts
                    tris_block.STEPTREE.data  = raw_tris

                    # call the byteswappers
                    byteswap_verts(verts_block)
                    byteswap_tris(tris_block)

                    # null out the model_meta_info
                    info.index_type.data  = info.index_count  = 0
                    info.vertex_type.data = info.vertex_count = 0
                    info.indices_offset = info.vertices_offset  = 0
                    if model_magic is None:
                        info.indices_magic_offset  = 0
                        info.vertices_magic_offset = 0
                    else:
                        info.indices_reflexive_offset  = 0
                        info.vertices_reflexive_offset = 0

        elif tag_cls == "pphy":
            # set the meta-only values to 0
            meta.wind_coefficient = 0
            meta.wind_sine_modifier = 0
            meta.z_translation_rate = 0

            # scale friction values
            meta.air_friction /= 10000
            meta.water_friction /= 10000

        elif tag_cls == "proj":
            # need to scale velocities by 30
            meta.proj_attrs.physics.initial_velocity *= 30
            meta.proj_attrs.physics.final_velocity *= 30

        elif tag_cls == "sbsp":
            byteswap_sbsp_meta(meta)

            # null out the runtime decals
            del meta.runtime_decals.STEPTREE[:]

            for cluster in meta.clusters.STEPTREE:
                predicted_resources.append(cluster.predicted_resources)

            compressed = "xbox" in engine or engine in ("stubbs", "shadowrun_beta")

            if compressed:
                generate_verts = kwargs.get("generate_uncomp_verts", False)
            else:
                generate_verts = kwargs.get("generate_comp_verts", False)

            # local variables for faster access
            s_unpack = unpack
            s_pack_into = pack_into

            for lightmap in meta.lightmaps.STEPTREE:
                for b in lightmap.materials.STEPTREE:
                    # need to null these or switching bsps will crash sapien
                    b.unknown_meta_offset0 = b.unknown_meta_offset1 = 0
                    b.vertices_meta_offset = 0
                    b.lightmap_vertices_meta_offset = 0
                    b.vertex_type.data = 0

                    if not generate_verts:
                        continue

                    vert_count = b.vertices_count
                    lightmap_vert_count = b.lightmap_vertices_count

                    u_verts = b.uncompressed_vertices
                    c_verts = b.compressed_vertices

                    if compressed:
                        # generate uncompressed vertices from the compressed
                        comp_buffer   = c_verts.STEPTREE
                        uncomp_buffer = bytearray(56*vert_count +
                                                  20*lightmap_vert_count)
                        in_off  = 0
                        out_off = 0
                        for i in range(vert_count):
                            n, b, t = s_unpack("<3I",
                                comp_buffer[in_off + 12: in_off + 24])
                            ni = (n&1023) / 1023
                            nj = ((n>>11)&1023) / 1023
                            nk = ((n>>22)&511) / 511
                            if (n>>10)&1: ni = ni - 1.0
                            if (n>>21)&1: nj = nj - 1.0
                            if (n>>31)&1: nk = nk - 1.0

                            bi = (b&1023) / 1023
                            bj = ((b>>11)&1023) / 1023
                            bk = ((b>>22)&511) / 511
                            if (b>>10)&1: bi = bi - 1.0
                            if (b>>21)&1: bj = bj - 1.0
                            if (b>>31)&1: bk = bk - 1.0

                            ti = (t&1023) / 1023
                            tj = ((t>>11)&1023) / 1023
                            tk = ((t>>22)&511) / 511
                            if (t>>10)&1: ti = ti - 1.0
                            if (t>>21)&1: tj = tj - 1.0
                            if (t>>31)&1: tk = tk - 1.0

                            nmag = max(sqrt(ni**2 + nj**2 + nk**2), 0.00000000001)
                            bmag = max(sqrt(bi**2 + bj**2 + bk**2), 0.00000000001)
                            tmag = max(sqrt(ti**2 + tj**2 + tk**2), 0.00000000001)
                            
                            # write the uncompressed data
                            s_pack_into('<12s9f8s', uncomp_buffer, out_off,
                                        comp_buffer[in_off: in_off + 12],
                                        ni/nmag, nj/nmag, nk/nmag,
                                        bi/bmag, bj/bmag, bk/bmag,
                                        ti/tmag, tj/tmag, tk/tmag,
                                        comp_buffer[in_off + 24: in_off + 32])

                            in_off  += 32
                            out_off += 56

                        for i in range(lightmap_vert_count):
                            n, u, v = s_unpack(
                                "<I2h", comp_buffer[in_off: in_off + 8])
                            ni = (n&1023) / 1023
                            nj = ((n>>11)&1023) / 1023
                            nk = ((n>>22)&511) / 511
                            if (n>>10)&1: ni -= 1.0
                            if (n>>21)&1: nj -= 1.0
                            if (n>>31)&1: nk -= 1.0
                            mag = max(sqrt(ni**2 + nj**2 + nk**2), 0.00000000001)

                            # write the uncompressed data
                            s_pack_into('<5f', uncomp_buffer, out_off,
                                        ni/mag, nj/mag, nk/mag,
                                        u/32767, v/32767)

                            in_off  += 8
                            out_off += 20
                    else:
                        # generate compressed vertices from uncompressed
                        uncomp_buffer = u_verts.STEPTREE
                        comp_buffer   = bytearray(32*vert_count +
                                                  8*lightmap_vert_count)

                        in_off  = 0
                        out_off = 0
                        # for speed purposes, we'll assume all vectors
                        # are already normalized to a length of ~1.0
                        for i in range(vert_count):
                            ni, nj, nk, bi, bj, bk, ti, tj, tk = s_unpack(
                                "<9f", uncomp_buffer[in_off + 12:
                                                     in_off + 48])
                            ni = int(min(ni, 1.0)*1023)
                            nj = int(min(nj, 1.0)*1023)
                            nk = int(min(nk, 1.0)*511)
                            bi = int(min(bi, 1.0)*1023)
                            bj = int(min(bj, 1.0)*1023)
                            bk = int(min(bk, 1.0)*511)
                            ti = int(min(ti, 1.0)*1023)
                            tj = int(min(tj, 1.0)*1023)
                            tk = int(min(tk, 1.0)*511)
                            if ni < 0: ni = max(ni, -1023) + 2047
                            if nj < 0: nj = max(nj, -1023) + 2047
                            if nk < 0: nk = max(nk, -511)  + 1023
                            if bi < 0: bi = max(bi, -1023) + 2047
                            if bj < 0: bj = max(bj, -1023) + 2047
                            if bk < 0: bk = max(bk, -511)  + 1023
                            if ti < 0: ti = max(ti, -1023) + 2047
                            if tj < 0: tj = max(tj, -1023) + 2047
                            if tk < 0: tk = max(tk, -511)  + 1023

                            # write the compressed data
                            s_pack_into('<12s3I8s', comp_buffer, out_off,
                                        uncomp_buffer[in_off: in_off + 12],
                                        ni + (nj<<11) + (nk<<22),
                                        bi + (bj<<11) + (bk<<22),
                                        ti + (tj<<11) + (tk<<22),
                                        uncomp_buffer[in_off + 48:
                                                      in_off + 56])

                            in_off  += 56
                            out_off += 32

                        for i in range(lightmap_vert_count):
                            ni, nj, nk, u, v = s_unpack(
                                "<5f", uncomp_buffer[in_off: in_off + 20])
                            ni = int(min(ni, 1.0)*1023)
                            nj = int(min(nj, 1.0)*1023)
                            nk = int(min(nk, 1.0)*511)
                            if ni < 0: ni = max(ni, -1023) + 2047
                            if nj < 0: nj = max(nj, -1023) + 2047
                            if nk < 0: nk = max(nk, -511)  + 1023

                            # write the compressed data
                            s_pack_into('<I2h', comp_buffer, out_off,
                                        ni + (nj<<11) + (nk<<22),
                                        int(min(max(u, -1.0), 1.0)*32767),
                                        int(min(max(v, -1.0), 1.0)*32767))

                            in_off  += 20
                            out_off += 8

                    # replace the buffers
                    u_verts.STEPTREE = uncomp_buffer
                    c_verts.STEPTREE = comp_buffer

        elif tag_cls == "scnr":
            # need to remove the references to the child scenarios
            del meta.child_scenarios.STEPTREE[:]

            # set the bsp pointers and stuff to 0
            for b in meta.structure_bsps.STEPTREE:
                b.bsp_pointer = b.bsp_size = b.bsp_magic = 0

            predicted_resources.append(meta.predicted_resources)

            # byteswap the script syntax data
            byteswap_scnr_script_syntax_data(meta)

            # rename duplicate stuff that causes errors when compiling scripts
            if kwargs.get("rename_scnr_dups", False):
                for refl in (meta.cutscene_flags, meta.cutscene_camera_points,
                             meta.recorded_animations):
                    names = set()
                    blocks = refl.STEPTREE
                    # go through the array in reverse so the last name is
                    # considered the actual name and all others are renamed
                    for i in range(len(blocks) -1, -1, -1):
                        j = 0
                        b = blocks[i]
                        name = orig_name = b.name
                        while name in names:
                            name = ("DUP_%s_%s" % (j, orig_name))[:31]
                            j += 1
                        b.name = name
                        names.add(name)

            # divide the cutscene times by 30(they're in ticks)
            for b in meta.cutscene_titles.STEPTREE:
                b.fade_in_time /= 30
                b.up_time /= 30
                b.fade_out_time /= 30

        elif tag_cls == "snd!":
            for pitch_range in meta.pitch_ranges.STEPTREE:
                for permutation in pitch_range.permutations.STEPTREE:
                    if permutation.compression.enum_name == "none":
                        # byteswap pcm audio
                        byteswap_pcm16_samples(permutation.samples)

        elif tag_cls == "shpp":
            predicted_resources.append(meta.predicted_resources)

        elif tag_cls == "shpg":
            shpg_attrs = meta.shpg_attrs

            # copy all merged values into their respective reflexives
            for b in shpg_attrs.merged_values.STEPTREE:
                typ = b.value_type.enum_name
                cnt = b.value_count
                if   typ == "boolean": array = shpg_attrs.booleans.STEPTREE
                elif typ == "integer": array = shpg_attrs.integers.STEPTREE
                elif typ == "color":   array = shpg_attrs.colors.STEPTREE
                elif typ == "bitmap":  array = shpg_attrs.bitmaps.STEPTREE
                elif typ != "float":   continue  # unknown type
                elif cnt == 1: array = shpg_attrs.floats_1d.STEPTREE
                elif cnt == 2: array = shpg_attrs.floats_2d.STEPTREE
                elif cnt == 3: array = shpg_attrs.floats_3d.STEPTREE
                elif cnt == 4: array = shpg_attrs.floats_4d.STEPTREE
                else:          continue  # unknown float type

                array.append()
                new_b = array[-1]
                new_b.value_name = b.value_name
                values = b.values.u_node

                if typ == "bitmap":
                    new_b.bitmap = b.bitmap
                    new_b.bitmap_index = values.bitmap_index
                    continue

                new_b.runtime_value      = b.runtime_value
                new_b.animation_function = b.animation_function
                new_b.animation_flags    = b.animation_flags
                new_b.animation_duration = b.animation_duration
                new_b.animation_rate     = b.animation_rate

                if typ == "boolean":
                    new_b.flags = b.flags
                    new_b.value = values.value
                else:
                    new_b.value_lower_bound = values.value_lower_bound
                    new_b.value_upper_bound = values.value_upper_bound

            # clear the merged values reflexive
            del shpg_attrs.merged_values.STEPTREE[:]

        elif tag_cls == "weap":
            predicted_resources.append(meta.weap_attrs.predicted_resources)

        # remove any predicted resources
        for pr in predicted_resources:
            del pr.STEPTREE[:]

        return meta

    def load_all_resource_maps(self, maps_dir=""):
        if self.is_resource:
            return
        elif self.engine not in ("halo1pc", "halo1pcdemo", "halo1ce", "halo1yelo"):
            return

        if not maps_dir:
            maps_dir = dirname(self.filepath)

        map_paths = {name: None for name in ("bitmaps", "sounds")}
        if self.engine in ("halo1ce", "halo1yelo"):
            map_paths['loc'] = None

        data_files = False
        if hasattr(self.map_header, "yelo_header"):
            data_files = self.map_header.yelo_header.flags.uses_mod_data_files

        # detect/ask for the map paths for the resource maps
        for map_name in sorted(map_paths.keys()):
            if self.maps.get(map_name) is not None:
                # map already loaded
                continue

            if data_files:
                map_name = "-" + map_name
                map_path = join(maps_dir, "data_files", "%s.map" % map_name)
            else:
                map_path = join(maps_dir, "%s.map" % map_name)

            while map_path and not exists(map_path):
                map_path = askopenfilename(
                    initialdir=maps_dir,
                    title="Select the %s.map" % map_name,
                    filetypes=(("%s.map" % map_name, "*.map"), ("All", "*.*")))

                if map_path:
                    maps_dir = dirname(map_path)
                else:
                    print("    You wont be able to extract from %s.map" % map_name)

            map_paths[map_name] = map_path

        for map_name in sorted(map_paths.keys()):
            map_path = map_paths[map_name]
            try:
                if self.maps.get(map_name) is None and map_path:
                    print("    Loading %s.map..." % map_name)
                    Halo1RsrcMap(self.maps).load_map(
                        map_path, will_be_active=False)
                    print("        Finished")

                if map_name == "sounds":
                    self.ensure_sound_maps_valid()

            except Exception:
                self.maps.pop(map_name, None)
                print(format_exc())
