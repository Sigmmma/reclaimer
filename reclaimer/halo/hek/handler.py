import os

from hashlib import md5
from os.path import abspath, basename, exists, normpath, splitext

from supyr_struct.apps.handler import Handler
from supyr_struct.buffer import BytearrayBuffer
from ..field_types import *
from .defs.objs.tag import HekTag


class HaloHandler(Handler):
    default_defs_path = "reclaimer.halo.hek.defs"
    tag_fcc_match_set = frozenset()
    tag_filepath_match_set = frozenset()

    tagsdir = "%s%stags%s" % (abspath(os.curdir), PATHDIV, PATHDIV)

    treat_mode_as_mod2 = True

    def __init__(self, *args, **kwargs):
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
        
        if "datadir" in kwargs:
            self.datadir = kwargs["datadir"]
        else:
            self.datadir = basename(normpath(self.tagsdir))
            self.datadir = self.tagsdir.split(self.datadir)[0] + "data\\"

        #call the functions to build the tag_ref_cache,
        #reflexive_cache, and raw_data_cache
        self.tag_ref_cache   = self.build_loc_cache(TagIndexRef)
        self.reflexive_cache = self.build_loc_cache(Reflexive)
        self.raw_data_cache  = self.build_loc_cache(RawdataRef)

    def _build_loc_cache(self, f_type, desc={}):
        hasrefs = False
        refs = {}

        try:
            this_f_type = desc['TYPE']
        except Exception:
            this_f_type = None
        
        if this_f_type is f_type:
            return True, None
        elif this_f_type is not None:
            for key in desc:
                hassubrefs, subrefs = self._build_loc_cache(f_type, desc[key])
                if hassubrefs:
                    hasrefs = True
                    refs[key] = subrefs
                    
        return hasrefs, refs

    def _get_nodes_by_paths(self, paths, node, coll, cond):
        if paths is None:
            # the paths have been exhausted, so this is a Block to check
            if cond(node):
                coll.append(node)
        elif isinstance(paths, dict):
            if 'SUB_STRUCT' in paths:
                paths = paths['SUB_STRUCT']
                for i in range(len(node)):
                    self._get_nodes_by_paths(paths, node[i], coll, cond)
                return
            
            for key in paths:
                self._get_nodes_by_paths(paths[key], node[key], coll, cond)
        else:
            raise TypeError("Expected 'paths' to be of type %s or %s, not %s."%
                            (type(None), type(dict), type(paths)) )

    def build_loc_cache(self, f_type):
        '''this builds a cache of paths that will be used
        to quickly locate specific FieldTypes in structures
        by caching all possible locations of the FieldType'''
        cache = {}
        
        for def_id in self.defs:
            definition = self.defs[def_id].descriptor

            hasrefs, refs = self._build_loc_cache(f_type, definition)
            
            if hasrefs:
                cache[def_id] = refs

        return cache

    def get_nodes_by_paths(self, paths, node, cond=None):
        coll = []
        if cond is None:
            cond = lambda x: True
            
        if len(paths):
            self._get_nodes_by_paths(paths, node, coll, cond)

        return coll

    def get_def_id(self, filepath):
        if not filepath.startswith('.') and '.' in filepath:
            ext = splitext(filepath)[-1].lower()
        else:
            ext = filepath.lower()

        if ext in self.ext_id_map:
            return self.ext_id_map[ext]

        '''It is more reliable to determine a Halo tag
        based on its 4CC def_id than by file extension'''
        try:
            with open(filepath, 'r+b') as tagfile:
                tagfile.seek(36)
                def_id = str(tagfile.read(4), 'latin-1')
            if def_id in self.defs:
                return def_id
        except:
            return None

    def get_tag_hash(self, data, tag_ref_paths=(),
                     reflexive_paths=(), raw_data_paths=()):
        hash_buffer = BytearrayBuffer()

        #null out the parts of a tag that can screw
        #with the hash when compared to a tag meta                        
        for b in self.get_nodes_by_paths(tag_ref_paths, data):
            b.path_pointer = b.id = 0
            
        for b in self.get_nodes_by_paths(reflexive_paths, data):
            b.id = b.pointer = 0
            
        for b in self.get_nodes_by_paths(raw_data_paths, data):
            b.unknown = b.raw_pointer = b.pointer = b.id = 0

        #serialize the tag data to the hash buffer
        data.TYPE.serializer(data, writebuffer=hash_buffer)
        
        return md5(hash_buffer)

    def get_tagref_invalid(self, node):
        '''
        Returns whether or not the filepath of the tag reference isnt valid.
        Returns False if the filepath is empty or the file exists.
        Returns True otherwise.
        '''
        #if the string is empty, then it doesnt NOT exist, so return False
        if not node.filepath:
            return False
        filepath = self.tagsdir + node.filepath
        
        try:
            ext = node.tag_class.enum_name
            if (self.treat_mode_as_mod2 and (ext == 'model' and
                not exists(filepath + '.model'))):
                return not exists(filepath + '.gbxmodel')
            filepath += '.' + ext
        except Exception:
            pass
        
        return not exists(filepath)

    def get_tagref_exists(self, node):
        if not node.filepath:
            return False
        filepath = self.tagsdir + node.filepath
        
        try:
            filepath += '.' + node.tag_class.enum_name
        except Exception:
            pass
        
        return exists(filepath)

    def get_tagref_matches(self, node):
        '''
        Returns whether or not the int fcc of the nodes tag_class
        matches any of the int fccs in self.tag_fcc_match_set and
        if the nodes filepath is in self.tag_filepath_match_set.

        Returns True if both matchs are found AND the filepath is valid.
        Returns False otherwise.
        '''
        return (bool(node.filepath) and (
            node.filepath in self.tag_filepath_match_set and
            node.tag_class.data in self.tag_fcc_match_set))
