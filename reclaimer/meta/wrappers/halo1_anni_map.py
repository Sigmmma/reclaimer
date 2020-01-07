#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from math import pi, sqrt, log
from struct import Struct as PyStruct
from traceback import format_exc

from reclaimer.meta.wrappers.halo_map import HaloMap
from reclaimer.meta.wrappers.halo1_rsrc_map import Halo1RsrcMap
from reclaimer.meta.wrappers.halo1_map import Halo1Map
from reclaimer import data_extraction
from reclaimer.halo_script.hsc import h1_script_syntax_data_def
from reclaimer.hek.defs.coll import fast_coll_def
from reclaimer.hek.defs.sbsp import fast_sbsp_def
from reclaimer.hek.handler import HaloHandler
from reclaimer.util import int_to_fourcc

from supyr_struct.field_types import FieldType

__all__ = ("Halo1AnniMap",)


def end_swap_float(v, packer=PyStruct(">f").pack,
                   unpacker=PyStruct("<f").unpack):
    return unpacker(packer(v))[0]


def end_swap_int32(v):
    assert v >= -0x80000000 and v < 0x80000000
    if v < 0:
        v += 0x100000000
    v = ((((v << 24) + (v >> 24)) & 0xFF0000FF) +
         ((v << 8) & 0xFF0000) +
         ((v >> 8) & 0xFF00))
    if v & 0x80000000:
        return v - 0x100000000
    return v


def end_swap_int16(v):
    assert v >= -0x8000 and v < 0x8000
    if v < 0:
        v += 0x10000
    v = ((v << 8)  + (v >> 8)) & 0xFFFF
    if v & 0x8000:
        return v - 0x10000
    return v


def end_swap_uint32(v):
    assert v >= 0 and v <= 0xFFFFFFFF
    return ((((v << 24) + (v >> 24)) & 0xFF0000FF) +
            ((v << 8) & 0xFF0000) +
            ((v >> 8) & 0xFF00))


def end_swap_uint16(v):
    assert v >= 0 and v <= 0xFFFF
    return ((v << 8) + (v >> 8)) & 0xFFFF


class Halo1AnniMap(Halo1Map):
    tag_headers = None
    defs = None

    handler_class = HaloHandler

    inject_rawdata = Halo1RsrcMap.inject_rawdata

    def __init__(self, maps=None):
        HaloMap.__init__(self, maps)
        self.setup_tag_headers()

    def get_dependencies(self, meta, tag_id, tag_cls):
        if self.is_indexed(tag_id):
            if tag_cls != "snd!":
                return ()

            rsrc_id = meta.promotion_sound.id & 0xFFff
            if rsrc_id == 0xFFFF: return ()

            sounds = self.maps.get("sounds")
            rsrc_id = rsrc_id // 2
            if   sounds is None: return ()
            elif rsrc_id >= len(sounds.tag_index.tag_index): return ()

            tag_path = sounds.tag_index.tag_index[rsrc_id].path
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
            if node.id & 0xFFff == 0xFFFF:
                continue
            dependencies.append(node)
        return dependencies

    def get_meta(self, tag_id, reextract=False, ignore_rsrc_sounds=False, **kw):
        '''
        Takes a tag reference id as the sole argument.
        Returns that tags meta data as a parsed block.
        '''
        if tag_id is None:
            return
        magic     = self.map_magic
        map_data  = self.map_data
        tag_index = self.tag_index
        tag_index_array = tag_index.tag_index

        tag_id &= 0xFFFF
        tag_index_ref = self.tag_index_manager.get_tag_index_ref(tag_id)
        if tag_index_ref is None:
            return

        tag_cls = None
        if tag_id == tag_index.scenario_tag_id & 0xFFff:
            tag_cls = "scnr"
        elif tag_index_ref.class_1.enum_name not in ("<INVALID>", "NONE"):
            tag_cls = int_to_fourcc(tag_index_ref.class_1.data)

        # if we dont have a defintion for this tag_cls, then return nothing
        if self.get_meta_descriptor(tag_cls) is None:
            return


        if tag_cls is None:
            # couldn't determine the tag class
            return
        elif reextract:
            pass
        elif tag_id == tag_index.scenario_tag_id & 0xFFff and self.scnr_meta:
            return self.scnr_meta
        elif tag_cls == "matg" and self.matg_meta:
            return self.matg_meta

        desc = self.get_meta_descriptor(tag_cls)
        block = [None]
        pointer_converter = self.bsp_pointer_converters.get(
            tag_id, self.map_pointer_converter)

        offset = pointer_converter.v_ptr_to_f_ptr(tag_index_ref.meta_offset)

        try:
            # read the meta data from the map
            with FieldType.force_big:
                desc['TYPE'].parser(
                    desc, parent=block, attr_index=0, rawdata=map_data,
                    map_pointer_converter=pointer_converter,
                    tag_index_manager=self.tag_index_manager, offset=offset)
        except Exception:
            print(format_exc())
            if kw.get("allow_corrupt"):
                return block[0]
            return

        meta = block[0]
        try:

            self.record_map_cache_read(tag_id, 0)  # cant get size quickly enough
            if self.map_cache_over_limit():
                self.clear_map_cache()

            self.inject_rawdata(meta, tag_cls, tag_index_ref)
            self.byteswap_anniversary_fields(meta, tag_cls)
        except Exception:
            print(format_exc())
            if not kw.get("allow_corrupt"):
                meta = None

        return meta

    def byteswap_anniversary_fields(self, meta, tag_cls):

        if tag_cls == "antr":
            unpack_header = PyStruct("<11i").unpack
            for b in meta.animations.STEPTREE:
                b.unknown_sint16 = end_swap_int16(b.unknown_sint16)
                b.unknown_float = end_swap_float(b.unknown_float)
                if not b.flags.compressed_data:
                    continue

                comp_data = b.frame_data.data[b.offset_to_compressed_data: ]
                # byteswap compressed frame data header
                for i in range(0, 44, 4):
                    data = comp_data[i: i + 4]
                    for j in range(4):
                        comp_data[i + 3 - j] = data[j]

                header = list(unpack_header(comp_data[: 44]))
                header.insert(0, 44)
                header.append(len(comp_data))

                item_sizes = (4, 2, 2, 2,  4, 2, 4, 4,  4, 2, 4, 4)
                comp_data_off_len_size = []
                for i in range(len(header) - 1):
                    comp_data_off_len_size.append([
                        header[i], header[i + 1] - header[i], item_sizes[i]])

                for off, length, size in comp_data_off_len_size:
                    for i in range(off, off + length, size):
                        data = comp_data[i: i + size]
                        for j in range(size):
                            comp_data[i + size - 1 - j] = data[j]

                # replace the frame_data with the compressed data and some
                # blank default / frame data so tool doesnt shit the bed.
                default_data_size = b.node_count * (12 + 8 + 4) - b.frame_size
                b.default_data.data += bytearray(
                    max(0, len(b.default_data.data) - default_data_size))

                b.offset_to_compressed_data = b.frame_count * b.frame_size
                b.frame_data.data = bytearray(
                    b.frame_count * b.frame_size) + comp_data

        elif tag_cls == "bitm":
            for b in meta.bitmaps.STEPTREE:
                b.pixels = end_swap_uint16(b.pixels)

        elif tag_cls == "coll":
            for b in meta.nodes.STEPTREE:
                b.unknown0 = end_swap_int16(b.unknown0)
                b.unknown1 = end_swap_int16(b.unknown1)

        elif tag_cls == "effe":
            for event in meta.events.STEPTREE:
                for b in event.particles.STEPTREE:
                    b.unknown0 = end_swap_int16(b.unknown0)
                    b.unknown1 = end_swap_int16(b.unknown1)

        elif tag_cls == "hmt ":
            block_bytes = bytearray(meta.string.serialize())
            for i in range(20, len(block_bytes), 2):
                byte = block_bytes[i + 1]
                block_bytes[i + 1] = block_bytes[i]
                block_bytes[i] = byte

            meta.string.parse(rawdata=block_bytes)

        elif tag_cls == "lens":
            meta.unknown0 = end_swap_float(meta.unknown0)
            meta.unknown1 = end_swap_float(meta.unknown1)

        elif tag_cls == "lsnd":
            meta.unknown0 = end_swap_float(meta.unknown0)
            meta.unknown1 = end_swap_float(meta.unknown1)
            meta.unknown2 = end_swap_float(meta.unknown2)
            meta.unknown3 = end_swap_float(meta.unknown3)
            meta.unknown4 = end_swap_int16(meta.unknown4)
            meta.unknown5 = end_swap_int16(meta.unknown5)
            meta.unknown6 = end_swap_float(meta.unknown6)

        elif tag_cls == "metr":
            meta.screen_x_pos = end_swap_uint16(meta.screen_x_pos)
            meta.screen_y_pos = end_swap_uint16(meta.screen_y_pos)
            meta.width  = end_swap_uint16(meta.width)
            meta.height = end_swap_uint16(meta.height)

        elif tag_cls in ("mod2", "mode"):
            for node in meta.nodes.STEPTREE:
                node.unknown = end_swap_float(node.unknown)
                for b in (node.rot_jj_kk, node.rot_kk_ii, node.rot_ii_jj,
                          node.translation_to_root):
                    for i in range(len(b)):
                        b[i] = end_swap_float(b[i])

        elif tag_cls == "part":
            meta.rendering.unknown0 = end_swap_int32(meta.rendering.unknown0)
            meta.rendering.unknown1 = end_swap_float(meta.rendering.unknown1)
            meta.rendering.unknown2 = end_swap_uint32(meta.rendering.unknown2)

        elif tag_cls == "pphy":
            meta.scaled_density = end_swap_float(meta.scaled_density)
            meta.water_gravity_scale = end_swap_float(meta.water_gravity_scale)
            meta.air_gravity_scale = end_swap_float(meta.air_gravity_scale)

        elif tag_cls == "sbsp":
            # TODO: Might need to byteswap cluster data and sound_pas data

            for coll_mat in meta.collision_materials.STEPTREE:
                coll_mat.unknown = end_swap_uint32(coll_mat.unknown)

            node_data = meta.nodes.STEPTREE
            for i in range(0, len(node_data), 2):
                b0 = node_data[i]
                node_data[i] = node_data[i + 1]
                node_data[i + 1] = b0

            leaf_data = meta.leaves.STEPTREE
            for i in range(0, len(leaf_data), 16):
                b0 = leaf_data[i]
                leaf_data[i] = leaf_data[i + 1]
                leaf_data[i + 1] = b0

                b0 = leaf_data[i + 2]
                leaf_data[i + 2] = leaf_data[i + 3]
                leaf_data[i + 3] = b0

                b0 = leaf_data[i + 4]
                leaf_data[i + 4] = leaf_data[i + 5]
                leaf_data[i + 5] = b0

                b0 = leaf_data[i + 6]
                leaf_data[i + 6] = leaf_data[i + 7]
                leaf_data[i + 7] = b0

            for lightmap in meta.lightmaps.STEPTREE:
                for b in lightmap.materials.STEPTREE:
                    vt_ct = b.vertices_count
                    l_vt_ct = b.lightmap_vertices_count

                    u_verts = b.uncompressed_vertices.STEPTREE
                    c_verts = b.compressed_vertices.STEPTREE

                    b.unknown_meta_offset0 = end_swap_uint32(
                        b.unknown_meta_offset0)
                    b.vertices_meta_offset = end_swap_uint32(
                        b.vertices_meta_offset)

                    b.vertex_type.data = end_swap_uint16(b.vertex_type.data)

                    b.unknown_meta_offset1 = end_swap_uint32(
                        b.unknown_meta_offset1)
                    b.lightmap_vertices_meta_offset = end_swap_uint32(
                        b.lightmap_vertices_meta_offset)

                    # byteswap (un)compressed verts and lightmap verts
                    for data in (u_verts, c_verts):
                        for i in range(0, len(data), 4):
                            b0 = data[i]
                            b1 = data[i+1]
                            data[i]   = data[i+3]
                            data[i+1] = data[i+2]
                            data[i+2] = b1
                            data[i+3] = b0

                    # since the compressed lightmap u and v coordinates are
                    # 2 byte fields rather than 4, the above byteswapping
                    # will have swapped u and v. we need to swap them back.
                    # multiply vt_ct by 32 to skip non-lightmap verts, and
                    # add 4 to skip the 4 byte compressed lightmap normal.
                    for i in range(vt_ct * 32 + 4, len(c_verts), 8):
                        c_verts[i: i + 1] = c_verts[i+1], c_verts[i]

            for fog_plane in meta.fog_planes.STEPTREE:
                fog_plane.material_type.data = end_swap_int16(
                    fog_plane.material_type.data)

        elif tag_cls == "scnr":
            for b in meta.object_names.STEPTREE:
                b.object_type.data = end_swap_uint16(b.object_type.data)
                b.reflexive_index = end_swap_int16(b.reflexive_index)

            for b in meta.trigger_volumes.STEPTREE:
                b.unknown = end_swap_uint16(b.unknown)

            for b in meta.encounters.STEPTREE:
                b.unknown = end_swap_int16(b.unknown)

            # PROLLY GONNA HAVE TO BYTESWAP RECORDED ANIMS AND MORE SHIT
            syntax_data = meta.script_syntax_data.data
            with FieldType.force_big:
                syntax_header = h1_script_syntax_data_def.build(rawdata=syntax_data)

            i = 56
            for node_i in range(syntax_header.last_node):
                n_typ = syntax_data[i + 5] + (syntax_data[i + 4] << 8)
                flags = syntax_data[i + 7] + (syntax_data[i + 6] << 8)
                if flags & 7 == 1:
                    # node is a primitive
                    if n_typ == 5:
                        # node is a boolean
                        syntax_data[i + 19] = syntax_data[i + 16]
                        syntax_data[i + 16: i + 19] = (0, 0, 0) # null these 3
                    elif n_typ == 7:
                        # node is a sint16
                        syntax_data[i + 18] = syntax_data[i + 16]
                        syntax_data[i + 19] = syntax_data[i + 17]
                        syntax_data[i + 16: i + 18] = (0, 0) # null these 2

                i += 20

        elif tag_cls == "senv":
            meta.senv_attrs.bump_properties.map_scale_x = end_swap_float(
                meta.senv_attrs.bump_properties.map_scale_x)
            meta.senv_attrs.bump_properties.map_scale_y = end_swap_float(
                meta.senv_attrs.bump_properties.map_scale_y)

        elif tag_cls == "snd!":
            for pr in meta.pitch_ranges.STEPTREE:
                for b in pr.permutations.STEPTREE:
                    b.ogg_sample_count = end_swap_uint32(b.ogg_sample_count)

        elif tag_cls == "spla":
            meta.spla_attrs.primary_noise_map.unknown0 = end_swap_uint16(
                meta.spla_attrs.primary_noise_map.unknown0)
            meta.spla_attrs.primary_noise_map.unknown1 = end_swap_uint16(
                meta.spla_attrs.primary_noise_map.unknown1)

            meta.spla_attrs.secondary_noise_map.unknown0 = end_swap_uint16(
                meta.spla_attrs.secondary_noise_map.unknown0)
            meta.spla_attrs.secondary_noise_map.unknown1 = end_swap_uint16(
                meta.spla_attrs.secondary_noise_map.unknown1)

        elif tag_cls == "ustr":
            for b in meta.strings.STEPTREE:
                block_bytes = bytearray(b.serialize())
                for i in range(12, len(block_bytes), 2):
                    byte = block_bytes[i + 1]
                    block_bytes[i + 1] = block_bytes[i]
                    block_bytes[i] = byte

                b.parse(rawdata=block_bytes)


        if tag_cls in ("bipd", "vehi", "weap", "eqip", "garb", "proj",
                       "scen", "mach", "ctrl", "lifi", "plac", "ssce", "obje"):
            meta.obje_attrs.object_type.data = end_swap_int16(
                meta.obje_attrs.object_type.data)
        elif tag_cls in ("senv", "soso", "sotr", "schi", "scex",
                         "swat", "sgla", "smet", "spla", "shdr"):
            meta.shdr_attrs.shader_type.data = end_swap_int16(
                meta.shdr_attrs.shader_type.data)

    def inject_rawdata(self, meta, tag_cls, tag_index_ref):
        pass

    def meta_to_tag_data(self, meta, tag_cls, tag_index_ref, **kwargs):
        kwargs["byteswap"] = False
        Halo1Map.meta_to_tag_data(self, meta, tag_cls, tag_index_ref, **kwargs)


        # TODO: Remove this if bitmap/sound extraction is ever implemented
        if tag_cls in ("snd!", "bitm"):
            # these tags don't properly extract due to missing
            # pixel data and sound permutation sample data
            return
        elif tag_cls in ("sbsp", "scnr"):
            # renderable geometry is absent from h1 anniversary bsps, and
            # we don't know how to properly byteswap recorded animations,
            # so scenarios can't be extracted properly either.
            return

        return meta
