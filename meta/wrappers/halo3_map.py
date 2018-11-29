import zlib

from os.path import exists, join
from tkinter.filedialog import askopenfilename

from reclaimer.h3.constants import h3_tag_class_fcc_to_ext
from reclaimer.h3.defs import __all__ as all_h3_def_ids
from reclaimer.h3.util import HALO3_MAP_TYPES
from .halo_map import *

class Halo3Map(HaloMap):
    tag_index_map = ()

    string_id_set_offsets = (
        (0x4B7, 0xC11), (0x0, 0x4B7), (0x0, 0xA7D),
        (0x0, 0xB0F),   (0x0, 0xBAF), (0x0, 0xB63),
        (0x0, 0xBBF),   (0x0, 0xBF0), (0x0, 0xC04))

    def __init__(self, maps=None):
        HaloMap.__init__(self, maps)

    def load_all_resource_maps(self, maps_dir=""):
        map_paths = {name: None for name in HALO3_MAP_TYPES[1:]}
        if not maps_dir:
            maps_dir = dirname(self.filepath)

        # detect/ask for the map paths for the resource maps
        for map_name in sorted(map_paths.keys()):
            if self.maps.get(map_name) is not None:
                # map already loaded
                continue

            map_path = join(maps_dir, map_name)
            if exists(map_path + ".map"):
                map_path += ".map"

            while map_path and not exists(map_path):
                map_path = askopenfilename(
                    initialdir=maps_dir,
                    title="Select the %s.map" % map_name,
                    filetypes=((map_name, "*.map"),
                               (map_name, "*.*")))

                if map_path:
                    maps_dir = dirname(map_path)
                else:
                    print("    You wont be able to extract from %s.map" % map_name)
                    break

            map_paths[map_name] = map_path

        for map_name in sorted(map_paths.keys()):
            map_path = map_paths[map_name]
            try:
                if self.maps.get(map_name) is None and map_path:
                    print("    Loading %s.map..." % map_name)
                    type(self)(self.maps).load_map(map_path, will_be_active=False)
                    print("        Finished")
            except Exception:
                print(format_exc())

    def setup_defs(self):
        if Halo3Map.defs:
            return

        Halo3Map.defs = defs = {}
        for fcc in h3_tag_class_fcc_to_ext:
            try:
                fcc2 = "".join(c if c in VALID_MODULE_NAME_CHARS
                               else "_" for c in fcc)
                fcc2 += "_" * ((4 - (len(fcc2) % 4)) % 4)
                if fcc2 not in all_h3_def_ids:
                    continue

                exec("from reclaimer.h3.defs.%s import %s_meta_def" %
                     (fcc2, fcc2))
                exec("defs['%s'] = %s_meta_def" % (fcc, fcc2))
            except Exception:
                print(format_exc())

    def get_meta_descriptor(self, tag_cls):
        tagdef = self.defs.get(tag_cls)
        if tagdef is not None:
            return tagdef.descriptor

    def load_map(self, map_path, **kwargs):
        autoload_resources = kwargs.get("autoload_resources", True)
        will_be_active = kwargs.get("will_be_active", True)
        HaloMap.load_map(self, map_path, **kwargs)
        tag_index = self.tag_index
        self.tag_index = h3_to_h1_tag_index(self.map_header, tag_index)

        self.string_id_manager = StringIdManager(
            self.map_header.strings.string_id_table,
            self.string_id_set_offsets,
            )

        map_type = self.map_header.map_type.data - 1
        if map_type > 0 and map_type < 4:
            self.is_resource = True
            self.maps[HALO3_MAP_TYPES[map_type]] = self

        self.tag_index_map = {}
        tag_index_array = self.tag_index.tag_index
        for i in range(len(tag_index_array)):
            self.tag_index_map[tag_index_array[i].id & 0xFFff] = i

        if autoload_resources and (will_be_active or not self.is_resource):
            self.load_all_resource_maps(dirname(map_path))

        self.map_data.clear_cache()

    def get_meta(self, tag_id, reextract=False):
        if tag_id is None:
            return
        elif self.map_header.map_type.enum_name not in ("sp", "mp", "ui"):
            # shared maps don't have a tag index
            return

        tag_index_array = self.tag_index.tag_index

        # if we are given a 32bit tag id, mask it off
        tag_id = self.tag_index_map.get(tag_id & 0xFFff, 0xFFff)
        if tag_id >= len(tag_index_array):
            return

        tag_index_ref = tag_index_array[tag_id]

        tag_cls = None
        if tag_index_ref.class_1.enum_name not in ("<INVALID>", "NONE"):
            tag_cls = fourcc(tag_index_ref.class_1.data)

        desc = self.get_meta_descriptor(tag_cls)
        if desc is None or tag_cls is None:        return
        elif reextract:                            pass
        elif tag_id == scnr_id and self.scnr_meta: return self.scnr_meta
        elif tag_id == matg_id and self.matg_meta: return self.matg_meta
        elif tag_cls == "ugh!" and self.ugh__meta: return self.ugh__meta

        block = [None]

        try:
            # read the meta data from the map
            meta_magic = 0
            offset = tag_index_ref.meta_offset
            for partition in self.map_header.partitions:
                if offset in range(partition.load_address,
                                   partition.load_address + partition.size):
                    meta_magic = partition.load_address - partition.file_offset
                    offset -= meta_magic
                    break

            desc['TYPE'].parser(
                desc, parent=block, attr_index=0, magic=meta_magic,
                tag_index=tag_index_array, rawdata=self.map_data,
                offset=offset, parsing_resource=True,
                map_sections=self.map_header.sections,
                map_string_id_manager=self.string_id_manager,
                map_partitions=self.map_header.partitions)
        except Exception:
            print(format_exc())
            return

        self.record_map_cache_read(tag_id, 0)
        if self.map_cache_over_limit():
            self.clear_map_cache()

        self.inject_rawdata(block[0], tag_cls, tag_index_ref)

        return block[0]

    def inject_rawdata(self, meta, tag_cls, tag_index_ref):
        # get some rawdata that would be pretty annoying to do in the parser
        return meta
