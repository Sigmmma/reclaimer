import re

from mmap import mmap
from os.path import dirname, splitext, isfile
from struct import unpack
from tkinter.filedialog import asksaveasfilename
from traceback import format_exc
from string import ascii_letters

from reclaimer.util import is_protected_tag, fourcc
from supyr_struct.defs.constants import *
from supyr_struct.defs.util import *
from supyr_struct.buffer import BytearrayBuffer, BytesBuffer, PeekableMmap
from supyr_struct.field_types import FieldType
from supyr_struct.defs.frozen_dict import FrozenDict

from ..halo_map import get_map_version, get_map_header,\
     get_tag_index, get_index_magic, get_map_magic, get_is_compressed_map,\
     decompress_map, map_header_demo_def, tag_index_pc_def

from .map_pointer_converter import MapPointerConverter
from .string_id_manager import StringIdManager
from .tag_index_manager import TagIndexManager
from .tag_index_converters import h2_alpha_to_h1_tag_index,\
     h2_to_h1_tag_index, h3_to_h1_tag_index
from .rawdata_manager import RawdataManager


VALID_MODULE_NAME_CHARS = ascii_letters + '_' + '0123456789'


backslash_fix = re.compile(r"\\{2,}")


class HaloMap:
    map_data = None
    map_data_cache_limit = 50
    _map_cache_byte_count = 0
    _ids_of_tags_read = None

    # these are the different pieces of the map as parsed blocks
    map_header  = None
    rsrc_map    = None
    tag_index   = None
    orig_tag_index = ()  # the tag index specific to the
    #                      halo version that this map is from

    # the original tag_path of each tag in the map before any deprotection
    orig_tag_paths = None

    string_id_manager = None
    tag_index_manager = None
    map_pointer_converter = None

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

    defs = None
    maps = None
    tag_headers = None

    tag_defs_module = ""
    tag_classes_to_load = ()

    def __init__(self, maps=None, map_data_cache_limit=None):
        self.orig_tag_paths = ()
        self.setup_defs()

        self._ids_of_tags_read = set()
        if map_data_cache_limit is not None:
            self.map_data_cache_limit = HaloMap.map_data_cache_limit

        self.maps = {} if maps is None else maps

    def setup_tag_headers(self):
        if type(self).tag_headers is not None:
            return

        tag_headers = type(self).tag_headers = {}
        for def_id in sorted(self.defs):
            if def_id in tag_headers or len(def_id) != 4:
                continue
            h_desc, h_block = self.defs[def_id].descriptor[0], [None]
            h_desc['TYPE'].parser(h_desc, parent=h_block, attr_index=0)
            tag_headers[def_id] = bytes(
                h_block[0].serialize(buffer=BytearrayBuffer(),
                                     calc_pointers=False))

    def setup_defs(self):
        assert type(self) is not HaloMap
        if type(self).defs:
            return

        print("    Loading definitions in '%s'" % self.tag_defs_module)

        type(self).defs = defs = {}
        for fcc in type(self).tag_classes_to_load:
            fcc2 = "".join(c if c in VALID_MODULE_NAME_CHARS
                           else "_" for c in fcc)
            fcc2 += "_" * ((4 - (len(fcc2) % 4)) % 4)
            try:
                # try to import the module, but ignore it if it doesnt exist
                exec("from %s.%s import get" % (self.tag_defs_module, fcc2))
                exec("defs['%s'] = get()" % fcc)
            except ImportError:
                continue
            except Exception:
                print(format_exc())

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
            tag_path = backslash_fix.sub(r'\\', b.path)

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

            b.path = tag_path

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

    def get_meta(self, tag_id, *a, **kw):
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
                new_decomp_path = asksaveasfilename(
                    initialdir=dirname(map_path),
                    title="Decompress '%s' to..." % map_name,
                    filetypes=(("mapfile", "*.map"),
                               ("All", "*.*")))
                if new_decomp_path:
                    decomp_path = new_decomp_path

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
            self.maps["<active>"] = self

        self.filepath    = map_path
        self.engine      = engine
        self.map_header  = map_header
        self.index_magic = get_index_magic(map_header)
        self.map_magic   = get_map_magic(map_header)
        self.tag_index   = tag_index
        self.map_pointer_converter = MapPointerConverter()

    def unload_map(self, keep_resources_loaded=True):
        keep_resources_loaded &= self.is_resource
        try: map_name = self.map_header.map_name
        except Exception: map_name = None

        if self.maps.get('<active>') is self:
            self.maps.pop('<active>')
        if self.maps.get(map_name) is self:
            self.maps.pop(map_name, None)

        if keep_resources_loaded and map_name in self.maps:
            return

        try: self.map_data.close()
        except Exception: pass
