# This module is to deal with the enforced lower case paths in Halo tags on
# systems other than Windows.
#
# It replaces some manual tasks like using string splits on paths or path
# splits that are often required for for instance finding a data dir's
# tag dir equivalent.
#
# This module prefers to make paths lower case, because Halo can only stores
# lower case paths. And because I don't trust modders to not have two
# identically named but with different capitalization files/folders on linux.

import pathlib
from pathlib import Path, PurePath, PurePosixPath, PureWindowsPath
import os
from os import path

# If not windows then we're likely on a posix filesystem.
# This function will not break on windows. But it's just slower.
def tagpath_to_fullpath(tagdir, tagpath, extension="", force_windows=False, folder=False):
    '''Takes a tagpath and case-insenstively goes through the directory
    tree to find the true path if it exists. (True path being the path with
    proper capitalization.) If force_windows is True, it will always treat
    the path as a windows path, otherwise it will treat it as whatever
    operating system you are using.

    Tagpaths from saved tagfiles should always be treated as windows.
    Tagpaths from filepickers must be native, and thus not forced_windows.

    If folder is True this program will search for a folder and assume
    that the path does not contain a file at the end.

    Returns properly capitalized path if found. None if not found.'''

    if tagdir == "" or tagpath == "":
        return None
    # Get all elements of the tagpath
    if force_windows:
        tagpath = list(pathlib.PureWindowsPath(tagpath).parts)
    else:
        tagpath = list(pathlib.PurePath(tagpath).parts)
    # Get the final element: The tag!
    tagname = ""
    if not folder:
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
    if not folder:
        files = os.listdir(cur_path) # Get all files in the current dir
        for file in files:
            fullpath = os.path.join(cur_path, file)
            if file.lower() == tagname and os.path.isfile(fullpath):
                return fullpath
    # If the execution reaches this point, nothing is found.
    return None

def path_split(path, splitword, force_windows=False):
    '''Takes a path and case-insentively splits it to
    the point before the given splitword.'''
    # Convert path into a list of each seperate piece.
    parts = list(pathlib.PurePath(path).parts)
    # Go through the path and find the first occurence of the word before which
    # we want to end the path.
    split_idx = len(parts)
    for i in range(len(parts)-1, -1, -1):
        if parts[i].lower() == splitword.lower():
            split_idx = i
            break

    # Build new path from leftover parts.
    new_path = Path(parts[:split_idx])

    # Return path in the same format, or in a string if the format isn't listed.
    if isinstance(path, pathlib.PureWindowsPath) or force_windows:
        return pathlib.PureWindowsPath(new_path)
    elif isinstance(path, (pathlib.PurePath, pathlib.PurePosixPath)):
        return pathlib.PurePath(new_path)
    elif isinstance(path, pathlib.Path):
        return new_path

    return str(pathlib.PurePath(new_path))

def path_replace(path, replace, new, backwards=True, split=False):
    '''Case-insentively replaces a part of the given path.
    Checks what pieces exist in the replaced string and will math the new path
    up to the existing point and finishes it with whatever was put in if it
    doesn't completely exist.

    If backbards it set, which it will be by default, it will try to find the
    right most matching part. Otherwise it will try to find the left most.'''
    parts = list(pathlib.PurePath(path).parts)
    split_idx = len(parts)
    if backwards:
        for i in range(len(parts)-1, -1, -1):
            if parts[i].lower() == replace.lower():
                split_idx = i
                break
    else:
        for i in range(len(parts)):
            if parts[i].lower() == replace.lower():
                split_idx = i
                break

    # Keep the before parts as is.
    before_parts = []
    before_parts.extend(parts[:split_idx])
    # Start after parts at the replacement point.
    after_parts = [new]
    if not split:
        after_parts.extend(parts[split_idx+1:])

    # Go through each directory level and find the corresponding directory name
    # case insensitively. Give up if we can't find any.
    cur_path = before_parts
    for dir in after_parts:
        subdirs = os.listdir(Path(*cur_path)) # Get all files in the current dir
        found = False
        # Check if there is directories with the correct name
        for subdir in subdirs:
            if (subdir.lower() == dir.lower()):
                cur_path.append(subdir)
                # Add the current directory to the end of our full path.
                found = True
                break
        # If no matching directory was found, give up.
        if not found:
            break

    # Get the path pieces that don't exist in the new directory and extend it
    # with all lower case versions of the original.
    leftover = parts[len(cur_path):len(parts)]
    for part in leftover:
        cur_path.append(part.lower())

    # Return path in the same format, or in a string if the format isn't listed.
    if isinstance(path, (PurePath, PurePosixPath)):
        return pathlib.PurePath(*cur_path)
    elif isinstance(path, PureWindowsPath):
        return pathlib.PureWindowsPath(*cur_path)
    elif isinstance(path, Path):
        return Path(*cur_path)

    return str(PurePath(*cur_path))

def path_normalize(path):
    '''Normalizes a path: Removes redundant seperators, and lower cases it on Windows.'''
    # Handling an edge case here. If a path is empty it will turn into "."
    # Which will fuck up some 'not' operators.
    if path == "":
        return path
    return os.path.normpath(os.path.normcase(path))
