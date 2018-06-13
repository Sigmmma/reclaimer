import re

from mmap import mmap
from os.path import dirname, splitext, isfile
from struct import unpack
from tkinter.filedialog import asksaveasfilename
from traceback import format_exc

from supyr_struct.defs.constants import *
from supyr_struct.defs.util import *
from supyr_struct.buffer import BytearrayBuffer, BytesBuffer, PeekableMmap
from supyr_struct.field_types import FieldType
from supyr_struct.defs.frozen_dict import FrozenDict

from ..resource import resource_def
from ..halo_map import get_map_version, get_map_header,\
     get_tag_index, get_index_magic, get_map_magic, get_is_compressed_map,\
     decompress_map, map_header_demo_def, tag_index_pc_def

from reclaimer.util import is_protected_tag, fourcc


backslash_fix = re.compile(r"\\{2,}")


def h2_alpha_to_h1_tag_index(map_header, tag_index):
    new_index = tag_index_pc_def.build()
    old_index_array = tag_index.tag_index
    new_index_array = new_index.tag_index

    # copy information from the h2 index into the h1 index
    new_index.scenario_tag_id[:] = tag_index.scenario_tag_id[:]
    new_index.tag_index_offset = tag_index.tag_index_offset
    new_index.tag_count = tag_index.tag_count

    for i in range(len(old_index_array)):
        old_index_entry = old_index_array[i]
        new_index_array.append()
        new_index_entry = new_index_array[-1]

        new_index_entry.class_1 = old_index_entry.class_1
        new_index_entry.class_2 = old_index_entry.class_2
        new_index_entry.class_3 = old_index_entry.class_3

        new_index_entry.id  = old_index_entry.id
        new_index_entry.pad = old_index_entry.flags
        new_index_entry.path_offset = old_index_entry.path_offset
        new_index_entry.meta_offset = old_index_entry.meta_offset
        new_index_entry.tag.tag_path = old_index_entry.tag.tag_path

    return new_index


def h2_to_h1_tag_index(map_header, tag_index):
    new_index = tag_index_pc_def.build()
    old_index_array = tag_index.tag_index
    new_index_array = new_index.tag_index

    # copy information from the h2 index into the h1 index
    new_index.scenario_tag_id[:] = tag_index.scenario_tag_id[:]
    new_index.tag_index_offset = tag_index.tag_index_offset
    new_index.tag_count = tag_index.tag_count

    tag_types = {}
    for typ in tag_index.tag_types:
        tag_types[typ.class_1.data] = [typ.class_1, typ.class_2, typ.class_3]

    for i in range(len(old_index_array)):
        old_index_entry = old_index_array[i]
        new_index_array.append()
        new_index_entry = new_index_array[-1]
        if old_index_entry.tag_class.data not in tag_types:
            new_index_entry.tag.tag_path = "reserved"
            new_index_entry.class_1.data = new_index_entry.class_2.data =\
                                           new_index_entry.class_3.data =\
                                           0xFFFFFFFF
            continue
        else:
            types = tag_types[old_index_entry.tag_class.data]
            new_index_entry.class_1 = types[0]
            new_index_entry.class_2 = types[1]
            new_index_entry.class_3 = types[2]

            #new_index_entry.path_offset = ????
            new_index_entry.tag.tag_path = map_header.strings.\
                                           tag_name_table[i].tag_name

        new_index_entry.id = old_index_entry.id
        new_index_entry.meta_offset = old_index_entry.offset
        if new_index_entry.meta_offset == 0:
            # might flag sbsp and ltmp tags as indexed
            new_index_entry.indexed = 1

    return new_index


class HaloMap:
    map_data = None
    map_data_cache_limit = 50
    _map_cache_byte_count = 0
    _ids_of_tags_read = None

    # these are the different pieces of the map as parsed blocks
    map_header  = None
    rsrc_header = None
    tag_index   = None
    orig_tag_index = None  # the tag index specific to the
    #                        halo version that this map is from

    # the original tag_path of each tag in the map before any deprotection
    orig_tag_paths = None

    # the parsed meta of the root tags in the map
    scnr_meta = None
    matg_meta = None

    # determines how to work with this map
    filepath      = ""
    engine        = ""
    is_resource   = False
    is_compressed = False

    handler = None

    index_magic = 0  # the offset that halo would load the tag index
    #                  header at in virtual memory
    map_magic   = 0  # used to convert pointers in a map into file offsets.
    #                  subtract this from a pointer to convert it to an offset.
    #                      map_magic = index_magic - index_header_offset

    bsp_magics  = ()
    bsp_sizes   = ()
    bsp_headers = ()
    bsp_header_offsets = ()

    defs = None
    maps = None

    def __init__(self, maps=None, map_data_cache_limit=None):
        self.bsp_magics = {}
        self.bsp_sizes  = {}
        self.bsp_header_offsets = {}
        self.bsp_headers = {}
        self.orig_tag_paths = ()
        self.setup_defs()

        self._ids_of_tags_read = set()
        if map_data_cache_limit is not None:
            self.map_data_cache_limit = map_data_cache_limit

        self.maps = {} if maps is None else maps

    def __del__(self):
        self.unload_map(False)

    def is_indexed(self, tag_id):
        return bool(self.tag_index.tag_index[tag_id].indexed)

    def basic_deprotection(self):
        if self.tag_index is None or self.is_resource:
            return

        i = 0
        found_counts = {}
        for b in self.tag_index.tag_index:
            tag_path = backslash_fix.sub(r'\\', b.tag.tag_path)

            tag_cls  = b.class_1.data
            name_id  = (tag_path, tag_cls)
            if is_protected_tag(tag_path):
                tag_path = "protected_%s" % i
                i += 1
            elif name_id in found_counts:
                tag_path = "%s_%s" % (tag_path, found_counts[name_id])
                found_counts[name_id] += 1
            else:
                found_counts[name_id] = 0

            b.tag.tag_path = tag_path

    def get_meta_descriptor(self, tag_cls):
        tagdef = self.defs.get(tag_cls)
        if tagdef is not None:
            return tagdef.descriptor[1]

    def record_map_cache_read(self, tag_id, size):
        if tag_id in self._ids_of_tags_read: return
        self._ids_of_tags_read.add(tag_id)
        self._map_cache_byte_count += size

    def map_cache_over_limit(self):
        return (self._map_cache_byte_count  >= self.map_data_cache_limit or
                len(self._ids_of_tags_read) >= self.map_data_cache_limit)

    def clear_map_cache(self):
        if not isinstance(self.map_data, mmap) or self.map_data.closed:
            return

        try:
            self.map_data.clear_cache()
        except Exception:
            print(format_exc())

        self._ids_of_tags_read.clear()
        self._map_cache_byte_count = 0

    def meta_to_tag_data(self, meta, tag_cls, tag_index_ref, **kwargs):
        '''
        Changes anything in a meta data block that needs to be changed for
        it to be a working tag. This includes removing predicted_resource
        references, fetching rawdata for the bitmaps, sounds, and models,
        and byteswapping any rawdata that needs it(animations, bsp, etc).
        '''
        raise NotImplementedError()

    def inject_rawdata(self, meta, tag_cls, tag_index_ref):
        raise NotImplementedError()

    def setup_defs(self):
        raise NotImplementedError()

    def get_meta(self, tag_id, reextract=False):
        raise NotImplementedError()

    def load_all_resource_maps(self, maps_dir=""):
        pass

    def load_map(self, map_path, **kwargs):
        will_be_active = kwargs.get("will_be_active", True)

        with open(map_path, 'rb+') as f:
            comp_data = PeekableMmap(f.fileno(), 0)

        map_header = get_map_header(comp_data, True)
        if map_header is None:
            print("    Could not read map header.")
            comp_data.close()
            return

        engine = get_map_version(map_header)

        decomp_path = None
        map_name = map_header.map_name
        self.is_compressed = get_is_compressed_map(comp_data, map_header)
        if self.is_compressed:
            decomp_path = splitext(map_path)
            while decomp_path[1]:
                decomp_path = splitext(decomp_path[0])
            decomp_path = decomp_path[0] + "_DECOMP.map"

            if isfile(decomp_path):
                decomp_path = ''
                while not decomp_path:
                    decomp_path = asksaveasfilename(
                        initialdir=dirname(map_path),
                        title="Decompress '%s' to..." % map_name,
                        filetypes=(("mapfile", "*.map"),
                                   ("All", "*.*")))

            if not(decomp_path.lower().endswith(".map") or
                   isfile(decomp_path + ".map")):
                decomp_path += ".map"

            print("    Decompressing to: %s" % decomp_path)

        map_data = decompress_map(comp_data, map_header, decomp_path)
        if self.is_compressed:
            print("    Decompressed")
        self.map_data = map_data

        if comp_data is not map_data: comp_data.close()

        map_header = get_map_header(map_data)
        tag_index  = self.orig_tag_index = get_tag_index(map_data, map_header)

        if tag_index is None:
            print("    Could not read tag index.")
            return

        self.maps[map_header.map_name] = self
        if will_be_active:
            self.maps["active"] = self

        self.filepath    = map_path
        self.engine      = engine
        self.map_header  = map_header
        self.index_magic = get_index_magic(map_header)
        self.map_magic   = get_map_magic(map_header)
        self.tag_index   = tag_index

    def unload_map(self, keep_resources_loaded=True):
        keep_resources_loaded &= self.is_resource 
        try: map_name = self.map_header.map_name
        except Exception: map_name = None

        if self.maps.get('active') is self:
            self.maps.pop('active')
        if self.maps.get(map_name) is self:
            self.maps.pop(map_name, None)

        if keep_resources_loaded and map_name in self.maps:
            return

        try: self.map_data.close()
        except Exception: pass
