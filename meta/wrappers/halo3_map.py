import zlib

from os.path import exists, join
from tkinter.filedialog import askopenfilename

from reclaimer.h3.constants import h3_tag_class_fcc_to_ext
from reclaimer.h3.util import HALO3_SHARED_MAP_TYPES
from reclaimer.h3.handler import Halo3Handler
from .halo_map import *


class Halo3Map(HaloMap):
    rawdata_manager = None

    shared_map_names = ()

    root_tags = {}

    string_id_set_offsets = (
        (0x4B7, 0xC11), (0x0, 0x4B7), (0x0, 0xA7D),
        (0x0, 0xB0F),   (0x0, 0xBAF), (0x0, 0xB63),
        (0x0, 0xBBF),   (0x0, 0xBF0), (0x0, 0xC04))

    def __init__(self, maps=None):
        HaloMap.__init__(self, maps)
        self.setup_tag_headers()

    def setup_tag_headers(self):
        if Halo3Map.tag_headers is not None:
            return

        tag_headers = Halo3Map.tag_headers = {}
        for def_id in sorted(self.defs):
            if def_id in tag_headers or len(def_id) != 4:
                continue
            h_desc, h_block = self.defs[def_id].descriptor[0], [None]
            h_desc['TYPE'].parser(h_desc, parent=h_block, attr_index=0)
            tag_headers[def_id] = bytes(
                h_block[0].serialize(buffer=BytearrayBuffer(),
                                     calc_pointers=False))

    def setup_defs(self):
        if Halo3Map.defs is None:
            print("    Loading Halo 3 tag definitions...")
            Halo3Map.handler = Halo3Handler(build_reflexive_cache=False,
                                            build_raw_data_cache=False)

            Halo3Map.defs = FrozenDict(Halo3Map.handler.defs)
            print("        Finished")

        # make a shallow copy for this instance to manipulate
        self.defs = dict(self.defs)

    def load_all_resource_maps(self, maps_dir=""):
        play_meta = self.root_tags.get("cache_file_resource_layout_table")
        if not play_meta:
            print("Could not get cache_file_resource_layout_table meta. "
                  "Cannot determine resource maps.")
            return

        map_paths = {name: None for name in self.shared_map_names}
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
                    print("    Loading %s..." % map_name)
                    type(self)(self.maps).load_map(map_path, will_be_active=False)
                    print("        Finished")
            except Exception:
                print(format_exc())

    def get_meta_descriptor(self, tag_cls):
        tagdef = self.defs.get(tag_cls)
        if tagdef is not None:
            return tagdef.descriptor[1]

    def load_root_tags(self):
        new_root_tags = {}
        for b in self.orig_tag_index.root_tags:
            meta = self.get_meta(b.id)
            if meta:
                new_root_tags[b.id & 0xFFff] = meta
                new_root_tags[b.tag_class.enum_name] = meta

        self.root_tags = new_root_tags

    def load_map(self, map_path, **kwargs):
        autoload_resources = kwargs.get("autoload_resources", True)
        will_be_active = kwargs.get("will_be_active", True)
        HaloMap.load_map(self, map_path, **kwargs)
        self.tag_index = h3_to_h1_tag_index(self.map_header, self.tag_index)

        tag_index_array = self.tag_index.tag_index
        self.tag_index_manager = TagIndexManager(tag_index_array)
        self.string_id_manager = StringIdManager(
            self.map_header.strings.string_id_table,
            self.string_id_set_offsets,
            )
        for sect in self.map_header.sections:
            self.map_pointer_converter.add_page_info(
                sect.virtual_address, sect.file_offset, sect.size)

        for part in self.map_header.partitions:
            self.map_pointer_converter.add_page_info(
                part.load_address, part.file_offset, part.size)

        self.load_root_tags()

        map_type = self.map_header.map_type.data
        # ensure the sharable maps are also indexed under their internal names
        if map_type >= 2 and map_type < 5:
            self.is_resource = True
            self.maps[HALO3_SHARED_MAP_TYPES[map_type - 2]] = self

        play_meta = self.root_tags.get("cache_file_resource_layout_table")
        if play_meta:
            self.shared_map_names = list(
                b.map_path.replace('\\', '/').split("/")[-1].lower()
                for b in play_meta.external_cache_references.STEPTREE)

        self.rawdata_manager = RawdataManager(self)
        if autoload_resources and (will_be_active or not self.is_resource):
            self.load_all_resource_maps(dirname(map_path))

        self.map_data.clear_cache()

    def get_meta(self, tag_id, reextract=False):
        if tag_id is None or self.map_header.map_type.data > 2:
            # shared maps don't have a tag index
            return

        # if we are given a 32bit tag id, mask it off
        tag_id &= 0xFFff
        tag_index_ref = self.tag_index_manager.get_tag_index_ref(tag_id)
        if tag_index_ref is None:
            return

        tag_cls = None
        full_tag_cls_name = tag_index_ref.class_1.enum_name
        if full_tag_cls_name not in ("<INVALID>", "NONE"):
            tag_cls = fourcc(tag_index_ref.class_1.data)

        desc = self.get_meta_descriptor(tag_cls)
        if desc is None or tag_cls is None:
            return
        elif not reextract and self.root_tags.get(full_tag_cls_name):
            return self.root_tags[full_tag_cls_name]

        block = [None]

        try:
            # read the meta data from the map
            offset = self.map_pointer_converter.v_ptr_to_f_ptr(
                tag_index_ref.meta_offset)

            desc['TYPE'].parser(
                desc, parent=block, attr_index=0,
                rawdata=self.map_data, offset=offset,
                tag_index_manager=self.tag_index_manager,
                map_string_id_manager=self.string_id_manager,
                map_pointer_converter=self.map_pointer_converter,)
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

    def meta_to_tag_data(self, meta, tag_cls, tag_index_ref, **kwargs):
        return meta
