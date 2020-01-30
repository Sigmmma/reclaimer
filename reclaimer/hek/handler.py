#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

import os

from datetime import datetime
from time import time
from traceback import format_exc
from pathlib import Path, PureWindowsPath

from binilla.handler import Handler

from reclaimer.data_extraction import h1_data_extractors
from reclaimer.field_types import TagRef, Reflexive, RawdataRef
from reclaimer.hek.defs.objs.tag import HekTag
from reclaimer.hek.defs import __all__ as all_def_names

from supyr_struct.buffer import BytearrayBuffer
from supyr_struct.util import tagpath_to_fullpath, is_path_empty
from supyr_struct.field_types import FieldType


class NodepathRef(dict):
    __slots__ = ("is_ref",)
    def __init__(self, is_ref, *a, **kw):
        self.is_ref = is_ref
        dict.__init__(self, *a, **kw)


NO_LOC_REFS = NodepathRef(False)


class HaloHandler(Handler):
    frozen_imp_paths = all_def_names
    tag_header_engine_id = "blam"
    default_defs_path = "reclaimer.hek.defs"
    tag_fcc_match_set = frozenset()
    tag_filepath_match_set = frozenset()

    _tagsdir = Path.cwd().joinpath("tags")
    _datadir = Path.cwd().joinpath("data")

    case_sensitive = False
    tagsdir_relative = True

    treat_mode_as_mod2 = True
    tag_ref_cache   = None
    reflexive_cache = None
    raw_data_cache  = None

    tag_data_extractors = h1_data_extractors

    def __init__(self, *args, **kwargs):
        if not kwargs.pop("build_tag_ref_cache", True):
            self.tag_ref_cache = NO_LOC_REFS
        if not kwargs.pop("build_reflexive_cache", True):
            self.reflexive_cache = NO_LOC_REFS
        if not kwargs.pop("build_raw_data_cache", True):
            self.raw_data_cache = NO_LOC_REFS

        Handler.__init__(self, *args, **kwargs)

        self.tag_fcc_match_set = set()
        self.tag_filepath_match_set = set()

        self.ext_id_map = {}
        for key in self.id_ext_map.keys():
            self.ext_id_map[self.id_ext_map[key]] = key

        if "default_conversion_flags" in kwargs:
            self.default_conversion_flags = kwargs["default_conversion_flags"]
        else:
            self.default_conversion_flags = {}
            for def_id in self.tags:
                self.default_conversion_flags[def_id] = {}

        self.datadir = Path(
            kwargs.get("datadir", self.tagsdir.parent.joinpath("data")))

        if self.tag_ref_cache is None:
            self.tag_ref_cache  = self.build_loc_caches(TagRef)

        if self.reflexive_cache is None:
            self.reflexive_cache = self.build_loc_caches(Reflexive)

        if self.raw_data_cache is None:
            self.raw_data_cache  = self.build_loc_caches(RawdataRef)

    @property
    def datadir(self):
        return self._datadir
    @datadir.setter
    def datadir(self, new_val):
        if not isinstance(new_val, Path):
            new_val = Path(new_val)
        self._datadir = new_val

    def _build_loc_cache(self, cond, desc={}):
        try:
            f_type = desc['TYPE']
        except Exception:
            f_type = None

        if f_type is None:
            return NO_LOC_REFS

        nodepath_ref = NodepathRef(cond(desc))

        for key in desc:
            sub_nodepath_ref = self._build_loc_cache(cond, desc[key])
            if sub_nodepath_ref.is_ref or sub_nodepath_ref:
                nodepath_ref[key] = sub_nodepath_ref

        return nodepath_ref

    def build_loc_caches(self, cond):
        # if we are looking for only one specific FieldType, make it a tuple
        if isinstance(cond, FieldType):
            cond = (cond,)

        # if we are looking for FieldTypes, make it into a function
        if isinstance(cond, (tuple, list)):
            cond = lambda desc, f_types=cond: desc.get('TYPE') in f_types

        cache = {}

        for def_id in sorted(self.defs):
            definition = self.defs[def_id].descriptor

            nodepath_ref = self._build_loc_cache(cond, definition)
            if nodepath_ref.is_ref or nodepath_ref:
                cache[def_id] = nodepath_ref

        return cache

    def _get_nodes_by_paths(self, paths, coll, cond, parent, key):
        node = parent[key]
        if paths.is_ref and cond(parent, key):
            # this node is a node we are looking for; add it to the collection
            if hasattr(node, "desc"):
                coll.append(node)
            else:
                coll.append((parent, key))

        if 'SUB_STRUCT' in paths:
            paths = paths['SUB_STRUCT']
            for i in range(len(node)):
                self._get_nodes_by_paths(paths, coll, cond, node, i)
            return coll

        for i in paths:
            self._get_nodes_by_paths(paths[i], coll, cond, node, i)

        return coll

    def get_nodes_by_paths(self, paths, node, cond=lambda x, y: True):
        if paths:
            return self._get_nodes_by_paths(paths, [], cond, (node,), 0)

        return ()

    def get_def_id(self, filepath):
        filepath = Path(filepath)
        if self.tagsdir_relative and not filepath.is_absolute():
            filepath = self.tagsdir.joinpath(filepath)

        # It is more reliable to determine a Halo tag
        # based on its 4CC def_id than by file extension
        try:
            with filepath.open('rb') as f:
                f.seek(36)
                def_id = str(f.read(4), 'latin-1')
                f.seek(60)
                engine_id = f.read(4).decode(encoding='latin-1')
            if def_id in self.defs and engine_id == self.tag_header_engine_id:
                return def_id
        except Exception:
            pass

        return self.ext_id_map.get(filepath.suffix.lower())

    def get_tagref_invalid(self, parent, attr_index):
        '''
        Checks if filepath of a tag reference is invalid.
        Returns False if file exists.
        Returns True if does not or if the reference is empty.
        '''
        node = parent[attr_index]
        #if the string is empty, there is no reference, can't be invalid.
        if not node.filepath:
            return False

        return not self.get_tagref_exists(parent, attr_index)

    def get_tagref_exists(self, parent, attr_index):
        '''Returns whether or not a tag reference is valid.'''
        node = parent[attr_index]
        if not node.filepath:
            return False

        ext = '.' + node.tag_class.enum_name

        # Get full path with proper capitalization if it points to a file.
        filepath = tagpath_to_fullpath(
            self.tagsdir, PureWindowsPath(node.filepath), extension=ext)

        if filepath is None and (self.treat_mode_as_mod2 and
                                 ext == '.model'):
            filepath = tagpath_to_fullpath(
                self.tagsdir, PureWindowsPath(node.filepath), extension='.gbxmodel')

        return filepath is not None

    def get_tagref_matches(self, parent, attr_index):
        '''
        Returns whether or not the int fcc of the nodes tag_class
        matches any of the int fccs in self.tag_fcc_match_set and
        if the nodes filepath is in self.tag_filepath_match_set.

        Returns True if both matchs are found AND the filepath is valid.
        Returns False otherwise.
        '''
        node = parent[attr_index]
        return (bool(node.filepath) and (
            node.filepath in self.tag_filepath_match_set and
            node.tag_class.data in self.tag_fcc_match_set))

    def make_log_file(self, logstr, logpath=None):
        '''
        Writes the supplied string to a log file.

        Required arguments:
            logstr(str)

        If self.log_filename is a non-blank string it will be used as the
        log filename. Otherwise the current timestamp will be used as the
        filename in the format "YY-MM-DD  HH:MM SS".
        If the file already exists it will be appended to with the current
        timestamp separating each write. Otherwise the file will be created.
        '''
        # get the timestamp for the debug log's name
        timestamp = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")

        if not is_path_empty(logpath):
            pass
        elif isinstance(self.log_filename, str) and self.log_filename:
            logpath = self.tagsdir.joinpath(self.log_filename)
            logstr = '\n' + '-'*80 + '\n' + timestamp + '\n' + logstr
        else:
            logpath = self.tagsdir.joinpath(timestamp.replace(':', '.') + ".log")

        logpath = Path(logpath)

        mode = 'w'
        if logpath.is_file():
            mode = 'a'

        # open a debug file and write the debug string to it
        with logpath.open(mode) as logfile:
            logfile.write(logstr)
