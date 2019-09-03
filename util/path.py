import pathlib
import os
from os import path

# This module is to deal with the enforced lower case paths in Halo tags on
# systems other than Windows.

# Inverted this comparison so the version with the most
# important code is at the top.
if os.name != 'nt':
    # If not windows then we're likely on a posix filesystem.
    # This function will not break on windows. But it's just slower.
    def tagpath_to_fullpath(tagdir, tagpath, extension="", force_windows=False):
        '''Takes a tagpath and case-insenstively goes through the directory
        tree to find the true path if it exists. (True path being the path with
        proper capitalization.) If force_windows is True, it will always treat
        the path as a windows path, otherwise it will treat it as whatever
        operating system you are using.

        Tagpaths from saved tagfiles should always be treated as windows.
        Tagpaths from filepickers must be native, and thus not forced_windows.

        Returns properly capitalized path if found. None if not found.'''

        if tagdir == "" or tagpath == "":
            return None
        # Get all elements of the tagpath
        if force_windows:
            tagpath = list(pathlib.PureWindowsPath(tagpath).parts)
        else:
            tagpath = list(pathlib.PurePath(tagpath).parts)
        # Get the final element: The tag!
        tagname = (tagpath.pop(-1) + extension).lower()
        # Store our current progression through the tree.
        cur_path = tagdir
        for dir in tagpath:
            subdirs = os.listdir(cur_path) # Get all files in the current dir
            found = False
            # Check if there is directories with the correct name
            for subdir in subdirs:
                if (subdir.lower() == dir.lower()):
                    fullpath = path.join(cur_path, subdir)
                    if not path.isdir(fullpath):
                        continue
                    # Add the current directory to the end of our full path.
                    cur_path = fullpath
                    found = True
                    break
            # If no matching directory was found, give up.
            if not found:
                return None
        # Check if we can find the right file at the end of the chain
        files = os.listdir(cur_path) # Get all files in the current dir
        for file in files:
            fullpath = os.path.join(cur_path, file)
            if file.lower() == tagname and os.path.isfile(fullpath):
                return fullpath
        # If the execution reaches this point, nothing is found.
        return None

else:
    # We use this if on windows.
    def tagpath_to_fullpath(tagdir, tagpath, extension="", force_windows=False):
        '''Takes a tagpath and checks if it is valid. This is the windows
        version, and on windows anything goes in terms of case sensitivity.
        So, that's why it's simpler than the posix version.

        Returns all lowercase path if found. None if not found.'''

        # Get a full path.
        tagdir = os.path.normpath(tagdir).lower()
        tagpath = os.path.normpath(tagpath).lower() + extension.lower()
        fullpath = os.path.join(tagdir, tagpath)
        # Check if there is a file at this path.
        if os.path.isfile(fullpath):
            return fullpath
        # If the execution reaches this point, nothing is found.
        return None
