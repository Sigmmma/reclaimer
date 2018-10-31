from math import pi, sqrt, log
from os.path import exists, join
from struct import pack_into
from tkinter.filedialog import askopenfilename

from .halo_map import *
from .halo1_rsrc_map import Halo1RsrcMap
from .halo1_map import Halo1Map
from reclaimer import data_extraction

from reclaimer.hsc import h1_script_syntax_data_def
from reclaimer.hek.defs.coll import fast_coll_def
from reclaimer.hek.defs.sbsp import fast_sbsp_def
from reclaimer.hek.handler import HaloHandler

__all__ = ("Halo1AnniMap",)


class Halo1AnniMap(Halo1Map):
    tag_headers = None
    defs = None

    inject_rawdata = Halo1RsrcMap.inject_rawdata

    def __init__(self, maps=None):
        HaloMap.__init__(self, maps)
        self.setup_tag_headers()

    def setup_tag_headers(self):
        if Halo1AnniMap.tag_headers is not None:
            return

        tag_headers = Halo1AnniMap.tag_headers = {}
        for def_id in sorted(self.defs):
            if def_id in tag_headers or len(def_id) != 4:
                continue
            h_desc, h_block = self.defs[def_id].descriptor[0], [None]
            h_desc['TYPE'].parser(h_desc, parent=h_block, attr_index=0)
            tag_headers[def_id] = bytes(
                h_block[0].serialize(buffer=BytearrayBuffer(),
                                     calc_pointers=False))

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
            if node.id & 0xFFff == 0xFFFF:
                continue
            dependencies.append(node)
        return dependencies

    def setup_defs(self):
        if Halo1AnniMap.defs is None:
            print("    Loading Halo 1 tag definitions...")
            Halo1AnniMap.handler = HaloHandler(build_reflexive_cache=False,
                                               build_raw_data_cache=False)

            Halo1AnniMap.defs = dict(Halo1AnniMap.handler.defs)
            Halo1AnniMap.defs["sbsp"] = fast_sbsp_def
            Halo1AnniMap.defs["coll"] = fast_coll_def
            Halo1AnniMap.defs = FrozenDict(Halo1AnniMap.defs)
            print("        Finished")

        # make a shallow copy for this instance to manipulate
        self.defs = dict(self.defs)

    def get_meta(self, tag_id, reextract=False, ignore_rsrc_sounds=False):
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

        # if we are given a 32bit tag id, mask it off
        tag_id &= 0xFFFF
        if tag_id >= len(tag_index_array):
            return
        tag_index_ref = tag_index_array[tag_id]

        tag_cls = None
        if tag_id == tag_index.scenario_tag_id & 0xFFff:
            tag_cls = "scnr"
        elif tag_index_ref.class_1.enum_name not in ("<INVALID>", "NONE"):
            tag_cls = fourcc(tag_index_ref.class_1.data)

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
        offset = tag_index_ref.meta_offset - magic
        if tag_cls == "sbsp":
            # bsps use their own magic because they are stored in
            # their own section of the map, directly after the header
            magic  = (self.bsp_magics[tag_id] -
                      self.bsp_header_offsets[tag_id])
            offset = self.bsp_headers[tag_id].meta_pointer - magic

        try:
            # read the meta data from the map
            with FieldType.force_big:
                desc['TYPE'].parser(
                    desc, parent=block, attr_index=0, magic=magic,
                    tag_index=tag_index_array, rawdata=map_data, offset=offset)
        except Exception:
            print(format_exc())
            return


        self.record_map_cache_read(tag_id, 0)  # cant get size quickly enough
        if self.map_cache_over_limit():
            self.clear_map_cache()

        meta = block[0]
        self.inject_rawdata(meta, tag_cls, tag_index_ref)


        # need to adjust data union values for int16 and bool types
        if tag_cls == "scnr":
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
                    elif n_typ == 7:
                        # node is a sint16
                        syntax_data[i + 18] = syntax_data[i + 16]
                        syntax_data[i + 19] = syntax_data[i + 17]

                i += 20

        return meta

    def inject_rawdata(self, meta, tag_cls, tag_index_ref):
        pass

    def meta_to_tag_data(self, meta, tag_cls, tag_index_ref, **kwargs):
        kwargs["byteswap"] = False
        Halo1Map.meta_to_tag_data(self, meta, tag_cls, tag_index_ref, **kwargs)

        # TODO: Fix any fields that should be little endian in tags, but
        # are currently big endian due to anniversary maps being big endian.
        # Examples:
        #   compressed animation frame data
        #   ogg sample counts

        if tag_cls == "sbsp":
            for lightmap in meta.lightmaps.STEPTREE:
                for b in lightmap.materials.STEPTREE:
                    vt_ct = b.vertices_count
                    l_vt_ct = b.lightmap_vertices_count

                    u_verts = b.uncompressed_vertices.STEPTREE
                    c_verts = b.compressed_vertices.STEPTREE

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

        return meta
