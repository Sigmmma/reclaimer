import os

from time import time
from hashlib import md5
from datetime import datetime
from os.path import abspath, basename, exists, isfile, join, normpath, splitext

from binilla.handler import Handler
from supyr_struct.buffer import BytearrayBuffer
from ..field_types import *
from .defs.objs.tag import HekTag
from traceback import format_exc


BAD_DEPENDENCY_HASH = (b"<BAD_DEPENDENCY>", "0cf3d02152f2f7109908a3cdf3ae29d2")
CIR_DEPENDENCY_HASH = (b"<CIR_DEPENDENCY>", "76b8f46d8d8daac892ea2d5143eed246")
CANT_PARSE_TAG_HASH = (b"<CANT_PARSE_TAG>", "212d0231ac4d6b7600118c853c081d35")


class HaloHandler(Handler):
    default_defs_path = "reclaimer.hek.defs"
    tag_fcc_match_set = frozenset()
    tag_filepath_match_set = frozenset()

    tagsdir = "%s%stags%s" % (abspath(os.curdir), PATHDIV, PATHDIV)

    case_sensitive = False
    tagsdir_relative = True

    treat_mode_as_mod2 = True
    tag_ref_cache   = None
    reflexive_cache = None
    raw_data_cache  = None

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

        if kwargs.get("field_caches"):
            caches = kwargs["field_caches"]
            self.tag_ref_cache = caches[0]
            self.reflexive_cache = caches[1]
            self.raw_data_cache = caches[2]
        else:
            self.build_loc_caches()

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
            return coll

        # for the sake of speed, I am omitting the checks
        # that are found in the commented out code below.
        if 'SUB_STRUCT' in paths:
            paths = paths['SUB_STRUCT']
            for subnode in node:
                self._get_nodes_by_paths(paths, subnode, coll, cond)
            return coll
        
        for key in paths:
            self._get_nodes_by_paths(paths[key], node[key], coll, cond)
        '''
        elif isinstance(paths, dict):
            if 'SUB_STRUCT' in paths:
                paths = paths['SUB_STRUCT']
                for subnode in node:
                    self._get_nodes_by_paths(paths, subnode, coll, cond)
                return coll
            
            for key in paths:
                self._get_nodes_by_paths(paths[key], node[key], coll, cond)
        else:
            raise TypeError("Expected 'paths' to be of type %s or %s, not %s."%
                            (type(None), type(dict), type(paths)) )
        '''
        return coll

    def build_loc_caches(self):
        '''this builds a cache of paths that will be used
        to quickly locate specific FieldTypes in structures
        by caching all possible locations of the FieldType'''
        caches = []
        for f_type in (TagIndexRef, Reflexive, RawdataRef): 
            cache = {}
            caches.append(cache)
            
            for def_id in self.defs:
                definition = self.defs[def_id].descriptor

                hasrefs, refs = self._build_loc_cache(f_type, definition)
                
                if hasrefs:
                    cache[def_id] = refs

        self.tag_ref_cache   = caches[0]
        self.reflexive_cache = caches[1]
        self.raw_data_cache  = caches[2]

        return caches

    def get_nodes_by_paths(self, paths, node, cond=lambda x: True):
        if paths:
            return self._get_nodes_by_paths(paths, node, [], cond)

        return ()

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
            with open(filepath, 'rb') as f:
                f.seek(36)
                def_id = str(f.read(4), 'latin-1')
                f.seek(60)
                engine_id = f.read(4)
            if def_id in self.defs and engine_id == b'blam':
                return def_id
        except Exception:
            return None

    def get_tag_hash(self, data, def_id, data_key, hashes, is_meta=False):
        if data_key in hashes:
            if hashes[data_key] is None:
                # Oh shit, the data_key is already in the hash set
                # and hasn't been computed! CIRCULAR REFERENCES!
                # We can't resolve this, so the tag can't be hashed.
                hashes[data_key] = CIR_DEPENDENCY_HASH
            return hashes

        empty = ((), ())

        tag_ref_paths   = self.tag_ref_cache.get(def_id, empty)[1]
        reflexive_paths = self.reflexive_cache.get(def_id, empty)[1]
        raw_data_paths  = self.raw_data_cache.get(def_id, empty)[1]

        # temporarily put a None in for this hash so we know we're
        # trying to compute it, but that it's not been determined yet
        hashes[data_key] = None

        __lsi__ = list.__setitem__
        __osa__ = object.__setattr__
        ext_id_map = self.ext_id_map

        #null out the parts of a tag that can screw
        #with the hash when compared to a tag meta
        if tag_ref_paths is not empty:
            for b in self.get_nodes_by_paths(tag_ref_paths, data):
                ext = "." + b[0].enum_name
                if ext == '.model':
                    ext = '.gbxmodel'

                if is_meta:
                    ref_key = b.id
                    if ref_key not in hashes:
                        # we DONT already have this tag's hash, so
                        # we need to try to get the meta and hash it
                        refd_tagdata = self.get_meta(ref_key)
                        if refd_tagdata:
                            self.get_tag_hash(refd_tagdata, ext_id_map[ext],
                                              ref_key, hashes, is_meta)
                    if hashes.get(ref_key, '') is None:
                        # Circular reference. See above for explaination
                        hashes[ref_key] = hashes[data_key] = CIR_DEPENDENCY_HASH
                        return hashes

                elif b.filepath:
                    tagpath = b.filepath + ext
                    ref_key = tagpath
                    if ext == ".NONE":
                        # bad dependency
                        hashes[data_key] = BAD_DEPENDENCY_HASH
                        print("        Bad dependency in '%s': '%s%s'" %
                              (data_key, b.filepath, ext))
                        return hashes
                    else:
                        refd_tag = self.get_tag(tagpath, ext_id_map[ext], True)
                        if refd_tag is None:
                            # Something happened to prevent loading the tag...
                            hashes[data_key] = BAD_DEPENDENCY_HASH
                            hashes[ref_key] = CANT_PARSE_TAG_HASH
                            return hashes
                        else:
                            # conserve ram
                            self.delete_tag(tag=refd_tag)
                            self.get_tag_hash(refd_tag.data.tagdata,
                                              ext_id_map[ext], tagpath,
                                              hashes, is_meta)
                else:
                    ref_key = None

                if hashes.get(ref_key):
                    # a hash exists for this reference, so set the path to it
                    __osa__(b, 'STEPTREE', hashes[ref_key][1])

                __lsi__(b, 1, 0)  # set path_pointer to 0
                __lsi__(b, 2, 0)  # set path_length to 0
                __lsi__(b, 3, 0)  # set id to 0

        if reflexive_paths is not empty:
            for b in self.get_nodes_by_paths(reflexive_paths, data):
                __lsi__(b, 1, 0)  # set pointer to 0
                __lsi__(b, 2, 0)  # set id to 0

        if raw_data_paths is not empty:
            for b in self.get_nodes_by_paths(raw_data_paths, data):
                __lsi__(b, 1, 0)  # set unknown to 0
                __lsi__(b, 2, 0)  # set raw_pointer to 0
                __lsi__(b, 3, 0)  # set pointer to 0
                __lsi__(b, 4, 0)  # set id to 0

        #serialize the tag data to a hashbuffer
        hashbuffer = BytearrayBuffer()
        data.TYPE.serializer(data, writebuffer=hashbuffer)
        # we'll include the def_id on the end of the data
        # to make sure tags of different types, but identical
        # contents, aren't detected as the same tag.
        hsh = md5(hashbuffer + def_id.encode("latin-1"))
        hashes[data_key] = (hsh.digest(), hsh.hexdigest())

        # return the collection of id's/tagpaths to hashes
        return hashes

    def get_tagref_invalid(self, node):
        '''
        Returns whether or not the filepath of the tag reference isnt valid.
        Returns False if the filepath is empty or the file exists.
        Returns True otherwise.
        '''
        #if the string is empty, then it doesnt NOT exist, so return False
        if not node.filepath:
            return False
        filepath = join(self.tagsdir, node.filepath)
        
        try:
            ext = '.' + node.tag_class.enum_name
            if (self.treat_mode_as_mod2 and (
                ext == '.model' and not exists(filepath + ext))):
                return not exists(filepath + '.gbxmodel')
            filepath += ext
        except Exception:
            pass
        
        return not exists(filepath)

    def get_tagref_exists(self, node):
        if not node.filepath:
            return False
        filepath = join(self.tagsdir, node.filepath)
        
        try:
            ext = '.' + node.tag_class.enum_name
            if (self.treat_mode_as_mod2 and (
                ext == '.model' and not exists(filepath + ext))):
                return exists(filepath + '.gbxmodel')
            filepath += ext
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

        if logpath:
            pass
        elif isinstance(self.log_filename, str) and self.log_filename:
            logpath = self.tagsdir + self.log_filename
            logstr = '\n' + '-'*80 + '\n' + timestamp + '\n' + logstr
        else:
            logpath = self.tagsdir + timestamp.replace(':', '.') + ".log"

        mode = 'w'
        if isfile(logpath):
            mode = 'a'

        # open a debug file and write the debug string to it
        with open(logpath, mode) as logfile:
            logfile.write(logstr)

    def make_write_log(self, all_successes, rename=True, backup=None):
        '''
        Creates a log string of all tags that were saved and renames
        the tags from their temp filepaths to their original filepaths.
        Returns the created log string
        Raises TypeError if the Tag's status is not in (True,False,None)

        Renaming is done by removing '.temp' from the end of all files
        mentioned in 'all_successes' having a value of True.
        The log consists of a section showing which tags were properly
        loaded and processed, a section showing tags were either not
        properly loaded or not properly processed, and a section showing
        which tags were either not loaded or ignored during processing.

        Required arguments:
            all_successes(dict)
        Optional arguments:
            rename(bool)
            backup(bool)

        'all_successes' must be a dict with the same structure
        as self.tags, but with bools instead of tags.
        all_successes[def_id][filepath] = True/False/None

        True  = Tag was properly loaded and processed
        False = Tag was not properly loaded or not properly processed
        None  = Tag was not loaded or ignored during processing

        If 'backup' is True and a file already exists with the name
        that a temp file is going to be renamed to, the currently
        existing filename will be appended with '.backup'

        If 'rename' is True then the tags are expected to be in a
        temp file form where their filename ends with '.temp'
        Attempts to os.remove '.temp' from all tags if 'rename' == True

        The 'filepath' key of each entry in all_successes[def_id]
        are expected to be the original, non-temp filepaths. The
        temp filepaths are assumed to be (filepath + '.temp').
        '''
        if backup is None:
            backup = self.backup

        error_str = success_str = ignored_str = "\n\nThese tags were "

        error_str += "improperly loaded or processed:\n"
        success_str += "properly loaded and processed:\n"
        ignored_str += "not loaded or ignored during processing:\n"

        # loop through each tag
        for def_id in sorted(all_successes):
            write_successes = all_successes[def_id]

            error_str += "\n" + def_id
            success_str += "\n" + def_id
            ignored_str += "\n" + def_id

            for filepath in sorted(write_successes):
                status = write_successes[filepath]

                # if we had no errors trying to convert the tag
                if status is False:
                    error_str += "\n    " + filepath
                    continue
                elif status is None:
                    ignored_str += "\n    " + filepath
                    continue

                success_str += "\n    " + filepath
                filepath = self.tagsdir + filepath

                if not rename:
                    continue

                if not backup or isfile(filepath + ".backup"):
                    # try to delete the tag if told to not backup tags
                    # OR if there's already a backup with its name
                    try:
                        os.remove(filepath)
                    except Exception:
                        success_str += ('\n        Could not ' +
                                        'delete original file.')
                else:
                    # Otherwise try to os.rename the old
                    # files to the backup file names
                    try:
                        os.rename(filepath, filepath + ".backup")
                    except Exception:
                        success_str += ('\n        Could not ' +
                                        'backup original file.')

                # Try to os.rename the temp file
                try:
                    os.rename(filepath + ".temp", filepath)
                except Exception:
                    success_str += ("\n        Could not os.remove " +
                                    "'temp' from filename.")
                    # restore the backup
                    try:
                        if backup:
                            os.rename(filepath + ".backup", filepath)
                    except Exception:
                        pass

        return success_str + error_str + ignored_str + '\n'
