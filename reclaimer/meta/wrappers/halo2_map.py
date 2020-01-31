#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

import os
import zlib

from pathlib import Path
from traceback import format_exc

from reclaimer.meta.wrappers.halo_map import HaloMap
from reclaimer import data_extraction
from reclaimer.h2.util import HALO2_MAP_TYPES, split_raw_pointer
from reclaimer.util import is_reserved_tag, int_to_fourcc
from reclaimer.meta.wrappers.string_id_manager import StringIdManager
from reclaimer.meta.wrappers.tag_index_manager import TagIndexManager
from reclaimer.meta.wrappers.tag_index_converters import h2_alpha_to_h1_tag_index,\
     h2_to_h1_tag_index, h3_to_h1_tag_index

from supyr_struct.util import is_path_empty

from supyr_struct.buffer import BytearrayBuffer


class Halo2Map(HaloMap):
    '''Generation 2 map'''
    ugh__meta = None

    tag_defs_module = "reclaimer.h2.defs"
    tag_classes_to_load = (
        "ant!", "bitm", "hsc*", "pphy", "snd!", "shad", "trak", "ugh!"
        )
    data_extractors = data_extraction.h2_data_extractors

    def __init__(self, maps=None):
        HaloMap.__init__(self, maps)
        self.setup_tag_headers()

    def inject_rawdata(self, meta, tag_cls, tag_index_ref):
        # get some rawdata that would be pretty annoying to do in the parser
        if tag_cls == "bitm":
            # grab bitmap data correctly from map
            new_pixels = BytearrayBuffer()
            pix_off = 0

            for bitmap in meta.bitmaps.STEPTREE:
                # grab the bitmap data from the correct map
                bitmap.pixels_offset = pix_off

                ptr, map_name = split_raw_pointer(bitmap.lod1_offset)
                halo_map = self
                if map_name != "local":
                    halo_map = self.maps.get(map_name)

                if halo_map is None:
                    bitmap.lod1_size = 0
                    continue

                halo_map.map_data.seek(ptr)
                mip_pixels = halo_map.map_data.read(bitmap.lod1_size)
                mip_pixels = zlib.decompress(mip_pixels)

                new_pixels += mip_pixels
                bitmap.lod1_size = len(mip_pixels)
                pix_off += bitmap.lod1_size

            meta.processed_pixel_data.STEPTREE = new_pixels

    def meta_to_tag_data(self, meta, tag_cls, tag_index_ref, **kwargs):
        engine     = self.engine
        tag_index  = self.tag_index

        if tag_cls == "bitm":
            # set the size of the compressed plate data to nothing
            meta.compressed_color_plate_data.STEPTREE = BytearrayBuffer()
            new_pixels_offset = 0

            # uncheck the prefer_low_detail flag and
            # set up the lod1_offset correctly.
            for bitmap in meta.bitmaps.STEPTREE:
                bitmap.lod1_offset = new_pixels_offset
                new_pixels_offset += bitmap.lod1_size

                bitmap.lod2_offset = bitmap.lod3_offset = bitmap.lod4_offset =\
                                     bitmap.lod5_offset = bitmap.lod6_offset = 0
                bitmap.lod2_size = bitmap.lod3_size = bitmap.lod4_size =\
                                   bitmap.lod5_size = bitmap.lod6_size = 0

        return meta

    def get_resource_map_paths(self, maps_dir=""):
        map_paths = {name: None for name in HALO2_MAP_TYPES[1:]}
        if self.engine == "halo2alpha":
            map_paths.pop("single_player_shared", None)

        if not is_path_empty(maps_dir):
            maps_dir = Path(maps_dir)
        else:
            maps_dir = self.filepath.parent

        # detect the map paths for the resource maps
        for map_name in sorted(map_paths):
            map_path = str(maps_dir.joinpath(map_name))
            if self.maps.get(map_name) is not None:
                map_path = self.maps[map_name].filepath
            elif os.path.exists(map_path + ".map"):
                map_path = Path(map_path + ".map")
            elif os.path.exists(map_path + "_DECOMP.map"):
                map_path = Path(map_path + "_DECOMP.map")
            elif os.path.exists(map_path + ".map.dtz"):
                map_path = Path(map_path + ".map.dtz")
            else:
                map_path = None

            map_paths[map_name] = map_path

        return map_paths

    def load_map(self, map_path, **kwargs):
        HaloMap.load_map(self, map_path, **kwargs)
        tag_index = self.tag_index
        if self.engine == "halo2alpha":
            self.tag_index = h2_alpha_to_h1_tag_index(self.map_header, tag_index)
        else:
            self.tag_index = h2_to_h1_tag_index(self.map_header, tag_index)

        # add the tag data section
        self.map_pointer_converter.add_page_info(
            self.index_magic, self.map_header.tag_index_header_offset,
            self.map_header.tag_index_data_size + self.map_header.tag_data_size
            )

        self.string_id_manager = StringIdManager(
            self.map_header.strings.string_id_table, (),
            )
        self.tag_index_manager = TagIndexManager(self.tag_index.tag_index)
        map_type = self.map_header.map_type.data - 1
        if map_type > 0 and map_type < 4:
            self.is_resource = True
            self.maps[HALO2_MAP_TYPES[map_type]] = self

        # get the sound_cache_file_gestalt meta
        try:
            if self.engine == "halo2vista":
                ugh__id = None
                for b in self.tag_index.tag_index:
                    if int_to_fourcc(b.class_1.data) == "ugh!":
                        ugh__id = b.id & 0xFFff
                        break

                self.ugh__meta = self.get_meta(ugh__id)
                if self.ugh__meta is None:
                    print("Could not read sound_cache_file_gestalt tag")
        except Exception:
            print(format_exc())
            print("Could not read sound_cache_file_gestalt tag")

        self.clear_map_cache()

    def get_meta(self, tag_id, reextract=False, **kw):
        if tag_id is None:
            return
        elif self.engine == "halo2alpha":
            return

        scnr_id = self.orig_tag_index.scenario_tag_id & 0xFFff
        tag_index_array = self.tag_index.tag_index
        shared_map    = self.maps.get("shared")

        tag_id &= 0xFFFF
        tag_index_ref = self.tag_index_manager.get_tag_index_ref(tag_id)
        if tag_index_ref is None:
            return

        matg_id = self.orig_tag_index.globals_tag_id & 0xFFff
        sp_shared_map = self.maps.get("single_player_shared")

        if tag_id >= 10000 and shared_map is not self:
            if shared_map is None: return
            return shared_map.get_meta(tag_id, reextract)
        elif tag_id >= len(tag_index_array) and sp_shared_map is not self:
            if sp_shared_map is None: return
            return sp_shared_map.get_meta(tag_id, reextract)

        tag_index_ref = tag_index_array[tag_id]

        tag_cls = None
        if   tag_id == scnr_id: tag_cls = "scnr"
        elif tag_id == matg_id: tag_cls = "matg"
        elif tag_index_ref.class_1.enum_name not in ("<INVALID>", "NONE"):
            tag_cls = int_to_fourcc(tag_index_ref.class_1.data)

        desc = self.get_meta_descriptor(tag_cls)
        if desc is None or tag_cls is None:        return
        elif reextract:                            pass
        elif tag_id == scnr_id and self.scnr_meta: return self.scnr_meta
        elif tag_id == matg_id and self.matg_meta: return self.matg_meta
        elif tag_cls == "ugh!" and self.ugh__meta: return self.ugh__meta

        block = [None]
        offset = self.map_pointer_converter.v_ptr_to_f_ptr(
            tag_index_ref.meta_offset)

        try:
            # read the meta data from the map
            desc['TYPE'].parser(
                desc, parent=block, attr_index=0, rawdata=self.map_data,
                map_string_id_manager=self.string_id_manager,
                map_pointer_converter=self.map_pointer_converter,
                tag_index_manager=self.tag_index_manager, offset=offset,)
        except Exception:
            print(format_exc())
            if kw.get("allow_corrupt"):
                return block[0]
            return

        meta = block[0]
        try:
            self.record_map_cache_read(tag_id, 0)
            if self.map_cache_over_limit():
                self.clear_map_cache()

            self.inject_rawdata(meta, tag_cls, tag_index_ref)
            if tag_cls == "ugh!":
                self.ugh__meta = meta
        except Exception:
            print(format_exc())
            if not kw.get("allow_corrupt"):
                meta = None

        return meta

    def generate_map_info_string(self):
        string = HaloMap.generate_map_info_string(self)
        string += """

Calculated information:
    index magic == %s
    map magic   == %s
""" % (self.index_magic, self.map_magic)

        if self.engine == "halo2alpha":
            string += (("""
Tag index:
    tag count           == %s
    scenario tag id     == %s
    index array pointer == %s""") %
            (self.orig_tag_index.tag_count,
             self.orig_tag_index.scenario_tag_id & 0xFFff,
             self.tag_index.tag_index_offset))
        else:
            used_tag_count = 0
            local_tag_count = 0
            for index_ref in self.tag_index.tag_index:
                if is_reserved_tag(index_ref):
                    continue
                elif index_ref.meta_offset != 0:
                    local_tag_count += 1
                used_tag_count += 1

            string += (("""
Tag index:
    tag count           == %s
    used tag count      == %s
    local tag count     == %s
    tag types count     == %s
    scenario tag id     == %s
    globals  tag id     == %s
    index array pointer == %s""") %
            (self.orig_tag_index.tag_count, used_tag_count, local_tag_count,
             self.orig_tag_index.tag_types_count,
             self.orig_tag_index.scenario_tag_id & 0xFFff,
             self.orig_tag_index.globals_tag_id & 0xFFff,
             self.tag_index.tag_index_offset))

        return string
