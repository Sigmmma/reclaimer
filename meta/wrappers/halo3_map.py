from os.path import exists, join
from tkinter.filedialog import askopenfilename

from arbytmap.bitmap_io import get_pixel_bytes_size

from reclaimer.h3.constants import h3_tag_class_fcc_to_ext, FORMAT_NAME_MAP
from reclaimer.h3.util import HALO3_SHARED_MAP_TYPES, get_virtual_dimension
from reclaimer.h3.handler import Halo3Handler
from reclaimer.h3.constants import h3_tag_class_fcc_to_ext
from reclaimer.meta.wrappers.halo_map import *


__all__ = ("Halo3Map", )


def get_bitmap_pixel_data(halo_map, bitm_meta, bitmap_index):
    n_assets = bitm_meta.zone_assets_normal.STEPTREE
    i_assets = bitm_meta.zone_assets_interleaved.STEPTREE
    bitmap = bitm_meta.bitmaps.STEPTREE[bitmap_index]

    bitm_fmt = FORMAT_NAME_MAP[bitmap.format.data]
    v_height = get_virtual_dimension(bitm_fmt, bitmap.height)
    v_width = get_virtual_dimension(bitm_fmt, bitmap.width)

    pixel_data_size = get_pixel_bytes_size(bitm_fmt, v_width, v_height,
                                           bitmap.depth)
    if bitmap.type.enum_name == "cubemap":
        pixel_data_size *= 6

    if bitmap_index in range(len(n_assets)):
        is_interleaved = False
        pixel_data = halo_map.rawdata_manager.get_tag_resource_data(
            n_assets[bitmap_index].idx, pixel_data_size, pixel_data_size)
    elif bitmap_index in range(len(i_assets)):
        is_interleaved = True
        pixel_data = halo_map.rawdata_manager.get_tag_resource_data(
            i_assets[bitmap_index].idx, pixel_data_size, pixel_data_size)
    else:
        return False, b''

    return is_interleaved, pixel_data


def inject_bitmap_data(halo_map, bitm_meta):
    bitmaps = bitm_meta.bitmaps.STEPTREE
    for i in range(len(bitmaps)):
        bitmap = bitmaps[i]
        bitm_fmt = FORMAT_NAME_MAP[bitmap.format.data]
        
        v_height = get_virtual_dimension(bitm_fmt, bitmap.height)
        v_width = get_virtual_dimension(bitm_fmt, bitmap.width)

        try:
            pixel_data_size = get_pixel_bytes_size(bitm_fmt, v_width, v_height,
                                                   bitmap.depth)
        except KeyError:
            # unknown bitmap format
            continue

        # TEMPORARY: Don't want to worry about mips for now
        #bitmap.mipmaps = 0

        is_interleaved, pixel_data_chunks = get_bitmap_pixel_data(
            halo_map, bitm_meta, i)

        all_pixel_data = bytearray()
        for pixel_data in reversed(pixel_data_chunks):
            all_pixel_data.extend(pixel_data)

        if not all_pixel_data:
            pass
        elif not is_interleaved:
            bitm_meta.zone_assets_normal.STEPTREE[i].data = all_pixel_data
        else:
            bitm_meta.zone_assets_interleaved.STEPTREE[i].data = all_pixel_data


class Halo3Map(HaloMap):
    '''Generation 3 map'''
    rawdata_manager = None

    shared_map_names = ()

    root_tags = {}

    tag_defs_module = "reclaimer.h3.defs"
    tag_classes_to_load = tuple(sorted(h3_tag_class_fcc_to_ext.keys()))

    handler_class = Halo3Handler

    string_id_set_offsets = (
        (0x4B7, 0xC11), (0x0, 0x4B7), (0x0, 0xA7D),
        (0x0, 0xB0F),   (0x0, 0xBAF), (0x0, 0xB63),
        (0x0, 0xBBF),   (0x0, 0xBF0), (0x0, 0xC04))

    def __init__(self, maps=None):
        HaloMap.__init__(self, maps)
        self.setup_tag_headers()

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

        play_meta = self.root_tags.get("cache_file_resource_layout_table")
        if play_meta:
            self.shared_map_names = list(
                b.map_path.lower().replace('\\', '/').split("/")[-1].split(".")[0]
                for b in play_meta.external_cache_references.STEPTREE)

        self.rawdata_manager = RawdataManager(self)

        map_type = self.map_header.map_type.data
        if map_type >= 2 and map_type < 5:
            self.is_resource = True
            ext_cache_name = HALO3_SHARED_MAP_TYPES[map_type - 2]

            for map_name, halo_map in self.maps.items():
                # update each map's rawdata_manager so each one
                # knows what name the shared caches are named.
                if map_name != "<active>":
                    halo_map.rawdata_manager.add_shared_map_name(
                        ext_cache_name, self.map_header.map_name)

        if autoload_resources and map_type <= 2:
            self.load_all_resource_maps(dirname(map_path))

        self.map_data.clear_cache()

    def load_all_resource_maps(self, maps_dir=""):
        play_meta = self.root_tags.get("cache_file_resource_layout_table")
        if not play_meta:
            print("Could not get cache_file_resource_layout_table meta.\n"
                  "Cannot determine resource maps.")
            return

        map_paths = {name: None for name in self.shared_map_names}
        if not maps_dir:
            maps_dir = dirname(self.filepath)

        # detect/ask for the map paths for the resource maps
        for map_name in sorted(map_paths.keys()):
            map_name = map_name.split(".")[0]
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
        if tag_cls == "bitm":
            inject_bitmap_data(self, meta)

        return meta

    def meta_to_tag_data(self, meta, tag_cls, tag_index_ref, **kwargs):
        return meta
