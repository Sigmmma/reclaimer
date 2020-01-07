#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

import os
import re
import tempfile

from mmap import mmap
from pathlib import Path, PureWindowsPath
from traceback import format_exc
from string import ascii_letters

from reclaimer.meta.halo_map import get_map_version, get_map_header,\
     get_tag_index, get_index_magic, get_map_magic, get_is_compressed_map,\
     decompress_map
from reclaimer.meta.wrappers.map_pointer_converter import MapPointerConverter
from reclaimer.util import is_protected_tag, int_to_fourcc, path_normalize

from supyr_struct.buffer import BytearrayBuffer, get_rawdata
from supyr_struct.util import is_path_empty


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
    _filepath        = Path("")  # the filepath of the map being opened
    _decomp_filepath = Path("")  # the filepath of the map that map_data
    #                              is actually mapping. Typically only
    #                              different from filepath if the map had
    #                              to be decompressed to a different file.
    map_name        = ""
    engine          = ""
    is_resource     = False
    is_compressed   = False

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
    data_extractors = {}

    resource_map_class = None

    _decomp_file_ext = ".map"

    def __init__(self, maps=None, map_data_cache_limit=None):
        self.resource_map_class = type(self)
        self.setup_defs()

        self.cache_original_tag_paths()

        self._ids_of_tags_read = set()
        if map_data_cache_limit is not None:
            self.map_data_cache_limit = HaloMap.map_data_cache_limit

        self.maps = {} if maps is None else maps

    def __del__(self):
        self.unload_map()

    @property
    def filepath(self):
        return self._filepath
    @filepath.setter
    def filepath(self, new_val):
        if not isinstance(new_val, Path):
            new_val = Path(new_val)
        self._filepath = new_val

    @property
    def decomp_filepath(self):
        return self._decomp_filepath
    @decomp_filepath.setter
    def decomp_filepath(self, new_val):
        if not isinstance(new_val, Path):
            new_val = Path(new_val)
        self._decomp_filepath = new_val

    @property
    def decomp_file_ext(self):
        return self._decomp_file_ext

    def get_writable_map_data(self):
        if not self.map_data:
            return None
        elif getattr(self.map_data, "writable", False):
            return self.map_data

        try:
            writable_map_data = get_rawdata(
                filepath=self.decomp_filepath, writable=True)
        except Exception:
            writable_map_data = None

        if not getattr(writable_map_data, "writable"):
            raise OSError("Cannot open map in write mode: %s" %
                          self.decomp_filepath)

        self.map_data.close()
        self.map_data = writable_map_data

        # need to reopen the map as a writable stream
        # and replace self.map_data with it
        return self.map_data

    # wrappers around the tag index handler
    def get_total_dir_count(self, dir=""):  return self.tag_index_manager.get_total_dir_count(dir)
    def get_total_file_count(self, dir=""): return self.tag_index_manager.get_total_file_count(dir)
    def get_dir_count(self, dir=""):  return self.tag_index_manager.get_dir_count(dir)
    def get_file_count(self, dir=""): return self.tag_index_manager.get_file_count(dir)
    def get_dir_names(self, dir=""):  return self.tag_index_manager.get_dir_names(dir)
    def get_file_names(self, dir=""): return self.tag_index_manager.get_file_names(dir)

    def rename_tag(self, tag_path, new_path):
        return self.tag_index_manager.rename_tag(tag_path, new_path)

    def rename_tag_by_id(self, tag_id, new_path):
        return self.tag_index_manager.rename_tag_by_id(tag_id, new_path)

    def rename_dir(self, curr_dir, new_dir):
        return self.tag_index_manager.rename_dir(curr_dir, new_dir)

    def print_tag_index(self, dir="", **kw):
        return self.tag_index_manager.pprint(dir, **kw)

    def print_tag_index_files(self, dir="", **kw):
        return self.tag_index_manager.pprint_files(dir, **kw)

    def walk(self, top_down=True):
        yield from self.tag_index_manager.walk(top_down)

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

    def get_dependencies(self, meta, tag_id, tag_cls):
        return ()

    def is_indexed(self, tag_id):
        return bool(self.tag_index.tag_index[tag_id].indexed)

    def cache_original_tag_paths(self):
        tags = () if self.tag_index is None else self.tag_index.tag_index

        # record the original tag_paths so we know if they change
        self.orig_tag_paths = tuple(b.path for b in tags)

    def basic_deprotection(self):
        if self.tag_index is None:
            return

        i = 0
        found_counts = {}
        for b in self.tag_index.tag_index:
            tag_path = backslash_fix.sub(
                r'\\', b.path.replace("/", "\\")).strip().strip("\\").lower()

            name_id = (tag_path, b.class_1.enum_name)
            if is_protected_tag(tag_path):
                tag_path = "protected_%s" % i
            elif name_id in found_counts:
                tag_path = "%s_%s" % (tag_path, found_counts[name_id])
                found_counts[name_id] += 1
            else:
                found_counts[name_id] = 1

            b.path = tag_path
            i += 1

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
            pass

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

    def get_resource_map_paths(self, maps_dir=""):
        return {}

    def is_data_extractable(self, tag_index_ref):
        return int_to_fourcc(tag_index_ref.class_1.data) in self.data_extractors

    def extract_tag_data(self, meta, tag_index_ref, **kw):
        if not self.is_data_extractable(tag_index_ref):
            return "No extractor for this type of tag."

        extractor = self.data_extractors.get(
            int_to_fourcc(tag_index_ref.class_1.data))
        kw['halo_map'] = self
        return extractor(meta, Path(PureWindowsPath(tag_index_ref.path)), **kw)

    def load_resource_maps(self, maps_dir="", map_paths=(), **kw):
        do_printout = kw.get("do_printout", False)
        detected_map_paths = self.get_resource_map_paths(maps_dir)
        if isinstance(map_paths, dict):
            for name in detected_map_paths:
                if name in map_paths:
                    detected_map_paths[name] = map_paths[name]

        map_paths = detected_map_paths
        for map_name in sorted(map_paths.keys()):
            map_path = map_paths[map_name]
            if not(self.maps.get(map_name) is None and map_path):
                continue

            new_map = None
            try:
                new_map = self.resource_map_class(self.maps)
                if do_printout:
                    print("Loading %s..." % map_name)

                new_map.load_map(map_path, **kw)
                if new_map.engine != self.engine:
                    if do_printout:
                        print("Incorrect engine for this map.")
                    self.maps.pop(new_map.map_name, None)
            except Exception:
                if do_printout:
                    print(format_exc())

                # make sure to clear out any potentially bad maps
                for name in sorted(self.maps):
                    if self.maps[name] is new_map:
                        self.maps.pop(name, None)

        return set(name for name in map_paths if not self.maps.get(name))

    def load_map(self, map_path, **kwargs):
        decompress_overwrite = kwargs.get("decompress_overwrite")
        comp_data = get_rawdata(filepath=map_path, writable=False)

        map_header = get_map_header(comp_data, True)
        if map_header is None:
            print("    Could not read map header.")
            comp_data.close()
            return

        # set self.engine early so self.decomp_file_ext will be accurate
        self.engine = get_map_version(map_header)
        self.map_name = map_header.map_name

        self.is_compressed = get_is_compressed_map(comp_data, map_header)
        if self.is_compressed:
            decomp_path = os.path.splitext(map_path)
            while decomp_path[1]:
                decomp_path = os.path.splitext(decomp_path[0])

            decomp_path = decomp_path[0] + "_DECOMP" + self.decomp_file_ext
            if not decompress_overwrite and os.path.isfile(decomp_path):
                decomp_path = os.path.join(
                    tempfile.gettempdir(), os.path.basename(decomp_path))

            print("    Decompressing to: %s" % decomp_path)
            self.map_data = decompress_map(comp_data, map_header, decomp_path)
            if comp_data is not self.map_data:
                comp_data.close()
        else:
            self.map_data = comp_data
            decomp_path = map_path

        map_header = get_map_header(self.map_data)
        tag_index  = self.orig_tag_index = get_tag_index(
            self.map_data, map_header)

        if tag_index is None:
            print("    Could not read tag index.")
            return

        self.maps[self.map_name] = self
        self.filepath        = path_normalize(map_path)
        self.decomp_filepath = path_normalize(decomp_path)
        self.map_header  = map_header
        self.index_magic = get_index_magic(map_header)
        self.map_magic   = get_map_magic(map_header)
        self.tag_index   = tag_index
        self.map_pointer_converter = MapPointerConverter()

    def unload_map(self):
        if not isinstance(getattr(self, "maps", None), dict):
            return

        keys_to_pop = list(k for k, v in self.maps.items() if v is self)
        for k in keys_to_pop:
            self.maps.pop(k, None)

        try: self.map_data.close()
        except Exception: pass

    def generate_map_info_string(self):
        if hasattr(self.map_data, '__len__'):
            decomp_size = str(len(self.map_data))
        elif (hasattr(self.map_data, 'seek') and
              hasattr(self.map_data, 'tell')):
            curr_pos = self.map_data.tell()
            self.map_data.seek(0, 2)
            decomp_size = str(self.map_data.tell())
            self.map_data.seek(curr_pos)
        else:
            decomp_size = "unknown"

        if not self.is_compressed:
            decomp_size += "(is already uncompressed)"

        map_type = self.map_header.map_type.enum_name
        if   map_type == "sp": map_type = "singleplayer"
        elif map_type == "mp": map_type = "multiplayer"
        elif map_type == "ui": map_type = "mainmenu"
        elif map_type == "shared":   map_type = "shared"
        elif map_type == "sharedsp": map_type = "shared single player"
        elif self.is_resource: map_type = "resource cache"
        elif "INVALID" in map_type:  map_type = "unknown"

        return (("""%s
Header:
    engine              == %s
    name                == %s
    build date          == %s
    type                == %s
    checksum            == %s
    decompressed size   == %s
    index header offset == %s""") %
        (self.filepath, self.engine, self.map_header.map_name,
         self.map_header.build_date, map_type, self.map_header.crc32,
         decomp_size, self.map_header.tag_index_header_offset))
