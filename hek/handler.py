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
from .defs import __all__ as all_def_names


def bytes_to_hex(taghash):
    hsh = hex(int.from_bytes(taghash, 'big'))[2:]
    return '0x' + '0'*(len(taghash)*2-len(hsh)) + hsh


def fps_60_related(desc):
    unit_scale = desc.get("UNIT_SCALE")
    if hasattr(unit_scale, "fps_60_scale") and unit_scale.fps_60_scale:
        return True


BAD_DEPENDENCY_HASH = (b"<BAD_DEPENDENCY>", bytes_to_hex(b"<BAD_DEPENDENCY>"))
CANT_PARSE_TAG_HASH = (b"<CANT_PARSE_TAG>", bytes_to_hex(b"<CANT_PARSE_TAG>"))


class NodepathRef(dict):
    __slots__ = ("is_ref",)
    def __init__(self, is_ref, *a, **kw):
        self.is_ref = is_ref
        dict.__init__(self, *a, **kw)


NO_LOC_REFS = NodepathRef(False)


class HaloHandler(Handler):
    frozen_imp_paths = all_def_names
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

        if "datadir" in kwargs:
            self.datadir = kwargs["datadir"]
        else:
            self.datadir = basename(normpath(self.tagsdir))
            self.datadir = join(self.tagsdir.split(self.datadir)[0], "data")

        self.datadir = join(self.datadir, '')

        if self.tag_ref_cache is None:
            self.tag_ref_cache   = self.build_loc_caches(TagRef)
        
        if self.reflexive_cache is None:
            self.reflexive_cache = self.build_loc_caches(Reflexive)

        if self.raw_data_cache is None:
            self.raw_data_cache  = self.build_loc_caches(RawdataRef)

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

    def get_tag_hash(self, data, def_id, data_key, hashes=None, is_meta=False):
        if hashes is None:
            hashes = {}
        self._get_tag_hash(data, def_id, data_key, hashes, is_meta, {}, {}, 0)
        return hashes

    def _get_tag_hash(self, data, def_id, data_key, hashes, is_meta,
                      partial_hashes, node_depths, curr_depth):
        # NOTE! a clone of node_depths must be provided when calling
        # this function as its contents MUST depend on the hierarchy

        if data_key in partial_hashes:
            ###########################################
            #              INCOMPLETE
            ###########################################
            return partial_hashes[data_key]
            __osa__(b, 'STEPTREE', partial_hashes[ref_key])
        elif data_key in hashes:
            #########################################################
            #  If detecting a tag as being circularly referenced,
            #  a set of data_keys will be returned containing any
            #  references which were re-encountered. If a higher up
            #  _get_tag_hash recursion sees the set that was returned
            #  isnt empty, it will update its own set with it.
            #  When choosing whether to save the hash as a partial or
            #  full, this recursion levels data_key will be removed
            #  from the set. If the set is not empty then it will be
            #  considerd as a partial hash.
            #
            #  When a circular tag is encountered, all tags in its
            #  chain need to be recognized as circular. This make it
            #  so any time a tag in that chain is about to be hashed,
            #  it will know that unless a hash has been calculated
            #  for the tag the chain was entered on, a complete hash
            #  will need to be calculated starting at that point.
            #########################################################
            partial_hashes[data_key] = None
            return

        # keep track of the depth of any circular reference
        node_depths[data_key] = curr_depth
        curr_depth += 1

        empty = ((), ())

        reflexive_paths = self.reflexive_cache.get(def_id, empty)[1]
        raw_data_paths  = self.raw_data_cache.get(def_id, empty)[1]
        tag_ref_paths   = self.tag_ref_cache.get(def_id, empty)[1]

        # temporarily put a None in for this hash so we know we're
        # trying to compute it, but that it's not been determined yet
        hashes[data_key] = None

        # local variables for faster access
        __lsi__ = list.__setitem__
        __osa__ = object.__setattr__
        ext_id_map = self.ext_id_map

        # null out the parts of a tag that can screw
        # with the hash when compared to a tag meta
        if tag_ref_paths is not empty:
            for b in self.get_nodes_by_paths(tag_ref_paths, data):
                tag_id = b.id
                ref_key = tag_id[0] + (tag_id[1] << 16)
                filepath = b.filepath
                __lsi__(b, 1, 0)  # set path_pointer to 0
                __lsi__(b, 2, 0)  # set path_length to 0
                # set id to 0
                __lsi__(tag_id, 0, 0)
                __lsi__(tag_id, 1, 0)

                if ((is_meta and ref_key == 0xFFFFFFFF) or
                    not(is_meta or filepath)):
                    # dependency is empty
                    __osa__(b, 'STEPTREE', '')
                    continue

                try:
                    ext = "." + b[0].enum_name
                except Exception:
                    ext = ".NONE"
                if filepath and not is_meta:
                    ref_key = filepath + ext


                if ext == ".NONE":
                    # the tag class is invalid
                    hashes[ref_key] = BAD_DEPENDENCY_HASH
                    __osa__(b, 'STEPTREE', BAD_DEPENDENCY_HASH[1])
                    continue
                elif ext == '.model' and self.treat_mode_as_mod2:
                    ext = '.gbxmodel'


                if ref_key in node_depths:
                    # this dependency points to something already being
                    # parsed in the chain above. use the depth as the hash
                    __osa__(b, 'STEPTREE', str(
                        curr_depth - node_depths[ref_key]))
                    continue

                if is_meta:
                    refd_tagdata = self.get_meta(ref_key)
                else:
                    refd_tag = self.get_tag(ref_key, ext_id_map[ext], True)
                    refd_tagdata = refd_tag.data.tagdata
                    # conserve ram
                    self.delete_tag(tag=refd_tag)

                # get the hash of this dependency
                self._get_tag_hash(refd_tagdata, ext_id_map[ext],
                                   ref_key, hashes, is_meta, partial_hashes,
                                   dict(node_depths), curr_depth)

                if ref_key in partial_hashes:
                    ###########################################
                    #              INCOMPLETE
                    ###########################################
                    __osa__(b, 'STEPTREE', partial_hashes[ref_key])
                elif hashes.get(ref_key):
                    # a hash exists for this reference, so set the path to it
                    __osa__(b, 'STEPTREE', hashes[ref_key][1])

        if reflexive_paths is not empty:
            for b in self.get_nodes_by_paths(reflexive_paths, data):
                __lsi__(b, 1, 0)  # set pointer to 0
                __lsi__(b, 2, 0)  # set id to 0

        if raw_data_paths is not empty:
            for b in self.get_nodes_by_paths(raw_data_paths, data):
                b[0].data = 0     # set flags to 0
                __lsi__(b, 2, 0)  # set raw_pointer to 0
                __lsi__(b, 3, 0)  # set pointer to 0
                __lsi__(b, 4, 0)  # set id to 0

        #serialize the tag data to a hashbuffer
        hashbuffer = BytearrayBuffer()

        if is_meta:
            data.TYPE.serializer(data, writebuffer=hashbuffer)
        else:
            # force the library to serialize tags in little endian
            try:
                FieldType.force_little()
                data.TYPE.serializer(data, writebuffer=hashbuffer)
            finally:
                FieldType.force_normal()
            
        # we'll include the def_id on the end of the data
        # to make sure tags of different types, but identical
        # contents, aren't detected as the same tag.
        hsh = md5(hashbuffer + def_id.encode("latin-1"))

        if partial:
            ###########################################
            #              INCOMPLETE
            ###########################################
            partial_hashes[data_key] = hsh.digest()
        else:
            hashes[data_key] = (hsh.digest(), hsh.hexdigest())

    def get_tagref_invalid(self, parent, attr_index):
        '''
        Returns whether or not the filepath of the tag reference isnt valid.
        Returns False if the filepath is empty or the file exists.
        Returns True otherwise.
        '''
        node = parent[attr_index]
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

    def get_tagref_exists(self, parent, attr_index):
        node = parent[attr_index]
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
                        success_str += (
                            '\n        Could not delete original file.')
                else:
                    # Otherwise try to os.rename the old
                    # files to the backup file names
                    try:
                        os.rename(filepath, filepath + ".backup")
                    except Exception:
                        success_str += (
                            '\n        Could not backup original file.')

                # Try to os.rename the temp file
                try:
                    os.rename(filepath + ".temp", filepath)
                except Exception:
                    success_str += (
                        "\n        Could not os.remove 'temp' from filename.")
                    # restore the backup
                    try:
                        if backup:
                            os.rename(filepath + ".backup", filepath)
                    except Exception:
                        pass

        return success_str + error_str + ignored_str + '\n'
