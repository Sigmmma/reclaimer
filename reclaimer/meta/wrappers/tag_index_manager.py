#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

import os
from math import log, ceil

__all__ = ("TagIndexManager", "TagDirectoryNode")

TAG_ID_HEADER_STR = "  id  "
INDEXED_HEADER_STR = "| indexed "
FILEPATH_HEADER_STR = "| filepath"


class TagIndexManager:
    _tag_index = ()
    _tag_index_map = ()

    _get_dir_nodes_root = None

    def __init__(self, tag_index, tag_index_map=None):
        self._tag_index = tag_index
        if tag_index_map:
            self._tag_index_map = dict(tag_index_map)
        else:
            self._tag_index_map = {}
            for i in range(len(tag_index)):
                self._tag_index_map[tag_index[i].id & 0xFFff] = i

        # 0xFFff is reserved to mean NULL, so don't map it
        self._tag_index_map.pop(0xFFff, None)

        self._get_dir_nodes_root = TagDirectoryNode(self.tag_index).root_getter

    @property
    def tag_index(self): return self._tag_index
    @property
    def directory_nodes(self): return self._get_dir_nodes_root()

    def get_total_dir_count(self, dir=""):
        return self.directory_nodes.get_dir_node(dir).total_dir_count
    def get_total_file_count(self, dir=""):
        return self.directory_nodes.get_dir_node(dir).total_file_count
    def get_dir_count(self, dir=""):
        return self.directory_nodes.get_dir_node(dir).dir_count
    def get_file_count(self, dir=""):
        return self.directory_nodes.get_dir_node(dir).file_count
    def get_dir_names(self, dir=""):
        return self.directory_nodes.get_dir_node(dir).dir_names
    def get_file_names(self, dir=""):
        return self.directory_nodes.get_dir_node(dir).file_names

    # wrappers around the directory nodes
    def rename_tag(self, tag_path, new_path):
        return self.directory_nodes.rename_tag(tag_path, new_path)

    def rename_tag_by_id(self, tag_id, new_path):
        return self.directory_nodes.rename_tag_by_id(tag_id, new_path)

    def rename_dir(self, curr_dir, new_dir):
        return self.directory_nodes.rename_dir(curr_dir, new_dir)

    def pprint(self, dir="", **kw):
        return self.directory_nodes.pprint(dir, **kw)

    def pprint_files(self, dir="", **kw):
        return self.directory_nodes.pprint_files(dir, **kw)

    def walk(self, top_down=True):
        yield from self.directory_nodes.walk(top_down)

    def translate_tag_id(self, tag_id):
        tag_id &= 0xFFff
        if tag_id in self._tag_index_map:
            return self._tag_index_map[tag_id]
        return tag_id

    def get_tag_index_ref(self, tag_id):
        tag_id = self.translate_tag_id(tag_id)
        if tag_id in range(len(self._tag_index)):
            return self._tag_index[tag_id]


class TagDirectoryNode:
    class SharedRoot:
        __slots__ = ("_val", )
        def __init__(self, val): self._val = val
        def get(self): return self._val
        def set(self, new_val): self._val = new_val

    __slots__ = (
        "_names_to_ids",
        "_ids_to_names",
        "_sub_nodes",
        "_tag_index",
        "_shared_root",
        "remove_empty"
        )
    def __init__(self, tag_index, dir_items=(), shared_root=None):
        self._names_to_ids = {}
        self._ids_to_names = {}
        self._sub_nodes = {}
        self._tag_index = tag_index
        self.remove_empty = True

        if shared_root is None:
            self._shared_root = self.SharedRoot(self)
        else:
            self._shared_root = shared_root

        if self.root is self:
            # this is the root node. add entire tag index as children
            self.recalculate_nodes()
        else:
            for tag_id in dir_items:
                self._add_node(tag_id, dir_items[tag_id])

    def __getitem__(self, item_key):
        if isinstance(item_key, int):
            if item_key in range(len(self.tag_index)):
                return self.tag_index[item_key]
            raise IndexError(
                'Tag_id "%s" is outside the bounds of the tag index.' % item_key)
        elif item_key in self._sub_nodes:
            return self._sub_nodes[item_key]
        elif item_key in self._names_to_ids:
            return self._tag_index[self._names_to_ids[item_key]]
        else:
            item_key = item_key.replace('/', '\\').strip("\\ ")
            return self._get_node(
                [name for name in item_key.lower().split("\\") if name])

    def __str__(self): return self.pprint()

    @property
    def total_file_count(self):
        return self.file_count + sum(node.total_file_count for node in
                                     self._sub_nodes.values())
    @property
    def total_dir_count(self):
        return self.dir_count + sum(node.total_dir_count for node in
                                    self._sub_nodes.values())
    @property
    def file_count(self): return len(self._names_to_ids)
    @property
    def dir_count(self): return len(self._sub_nodes)
    @property
    def file_names(self): return sorted(self._names_to_ids)
    @property
    def dir_names(self): return sorted(self._sub_nodes)

    @property
    def names_to_ids(self): return dict(self._names_to_ids)
    @property
    def ids_to_names(self): return dict(self._ids_to_names)
    @property
    def sub_nodes(self): return dict(self._sub_nodes)
    @property
    def tag_index(self): return self._tag_index
    @property
    def root(self): return self.root_getter()
    @property
    def root_getter(self): return self._shared_root.get
    @property
    def shallow_empty(self): return not(self._names_to_ids or self._sub_nodes)
    @property
    def empty(self):
        if not self.shallow_empty:
            return False

        for node in self._sub_nodes.values():
            if not node.empty:
                return False
        return True

    def get_dir_node(self, dir=""):
        return self._get_node([n for n in dir.replace("/", "\\").
                               lower().strip("\\ ").split("\\") if n])

    def pprint(self, dir="", **kw):
        if dir:
            dir_pieces = [n for n in dir.replace("/", "\\").
                          lower().strip("\\ ").split("\\") if n]
            return self._get_node(dir_pieces).pprint(**kw)

        # these are user-supplied settings
        printout = kw.pop("do_printout", False)
        print_header = kw.get("header", True)
        print_guides = kw.get("guides", True)
        print_files = kw.get("files", True)
        print_tag_ids = kw.get("tag_ids", True) and print_files
        print_indexed = kw.get("indexed", False) and print_files
        dirs_first = kw.get("dirs_first", True)
        extra_dir_spacing = kw.get("extra_dir_spacing", 1)
        depth = kw.get("depth", 0)
        indent = kw.get("indent", 4)

        extra_returns = kw.pop("_extra_returns", False)
        indent_str = kw.get("indent_str", "")
        seen = kw.setdefault("seen", set())

        if depth is None:
            depth = float("inf")

        if id(self) in seen:
            return ""

        seen.add(id(self))
        string = indexed_pad_str = tag_id_pad = ""

        print_files = print_files and self._names_to_ids

        # subtract 1 char for the directory bar column and 1 for the space
        indent = max(indent - (2 if print_guides else 1), 0)

        # increase the indent str for next level
        kw["header"] = False
        kw["_extra_returns"] = int(extra_dir_spacing)
        last_item_indent_str = indent_str + (" " * (indent + 1)) + " "

        if print_tag_ids:
            tag_id_pad = " " * 6

        if print_header:
            if print_tag_ids:
                string += TAG_ID_HEADER_STR
            if print_indexed:
                string += INDEXED_HEADER_STR
            string += FILEPATH_HEADER_STR + "\n"

        if print_indexed:
            indexed_pad_str = " " * len(INDEXED_HEADER_STR)

        # put together tag path strings
        if print_files and not dirs_first:
            string += self.pprint_files(**kw)
        else:
            files_kw = dict(kw)

        dir_indent_str = indent_str
        if print_guides:
            indent_str += "|"
            if not self.file_count or depth > 0:
                dir_indent_str += "|"
            else:
                dir_indent_str += "+"

        kw["indent_str"] = indent_str + (" " * indent) + " "
        kw["depth"] = depth - 1

        dir_indent_str += (("-" if print_guides else " ") * indent) + " "
        # put together sub-directory strings
        item_count = self.dir_count
        for dir_name in sorted(self._sub_nodes):
            item_count -= 1
            if item_count == 0 and not(print_files and dirs_first):
                # helps with readability
                kw.update(_extra_returns=False, indent_str=last_item_indent_str)

            string += "%s%s%s%s\n" % (tag_id_pad, indexed_pad_str,
                                      dir_indent_str, dir_name)
            if depth > 0:
                string += self._sub_nodes[dir_name].pprint(**kw)

        if print_files and dirs_first:
            string += self.pprint_files(**files_kw)

        # add extra spacing after last directory
        for i in range(extra_returns):
            string += tag_id_pad + indexed_pad_str + last_item_indent_str + "\n"

        # either print the string, or return it
        if printout:
            lines = list(string.split("\n"))
            if not lines[-1]:
                lines.pop(-1)
            for line in lines:
                print(line)

            return ""
        else:
            return string

    def pprint_files(self, dir="", **kw):
        if dir:
            dir_pieces = [n for n in dir.replace("/", "\\").
                          lower().strip("\\ ").split("\\") if n]
            return self._get_node(dir_pieces).pprint_files(**kw)

        # these are user-supplied settings
        printout = kw.pop("do_printout", False)
        print_header = kw.get("header", True)
        print_guides = kw.get("guides", True)
        print_tag_ids = kw.get("tag_ids", True)
        print_indexed = kw.get("indexed", False)
        indent = kw.get("indent", 4)

        indent_str = kw.get("indent_str", "")
        string = ""

        # subtract 1 char for the directory bar column and 1 for the space
        indent = max(indent - (2 if print_guides else 1), 0)

        if print_tag_ids:
            tag_id_pad = " " * 6
        else:
            tag_id_pad = ""

        if print_header:
            if print_tag_ids:
                string += TAG_ID_HEADER_STR
            if print_indexed:
                string += INDEXED_HEADER_STR
            string += FILEPATH_HEADER_STR + "\n"

        if print_guides:
            indent_str += "|"

        indent_str += (("-" if print_guides else " ") * indent) + " "
        for name in sorted(self._names_to_ids):
            tag_id = self._names_to_ids[name]
            if print_tag_ids:
                tag_id_str = str(tag_id)
                string += tag_id_str + tag_id_pad[len(tag_id_str): ]

            if print_indexed:
                try:
                    indexed = self.tag_index[tag_id].indexed
                except Exception:
                    indexed = False

                if indexed:
                    string += "   YES" + (" " * (len(INDEXED_HEADER_STR) - 6))
                else:
                    string += " " * len(INDEXED_HEADER_STR)

            string += "%s%s\n" % (indent_str, name)

        # either print the string, or return it
        if printout:
            lines = list(string.split("\n"))
            if not lines[-1]:
                lines.pop(-1)
            for line in lines:
                print(line)

            return ""
        else:
            return string

    def rename_tag(self, curr_path, new_path):
        curr_path = curr_path.replace('/', '\\').strip("\\ ")
        self._rename_tag(
            [name for name in curr_path.lower().split("\\") if name], new_path)

    def rename_tag_by_id(self, tag_id, new_path):
        tag_ref = self.tag_index[tag_id]
        if tag_ref.id == 0xFFffFFff:
            return

        curr_path = tag_ref.path.replace('/', '\\').strip("\\ ")
        curr_path = "%s.%s" % (new_path, tag_ref.class_1.enum_name)
        self._rename_tag(curr_path.lower().split("\\"), new_path)

    def rename_dir(self, curr_dir, new_dir):
        curr_dir = curr_dir.replace('/', '\\').strip("\\ ")
        self._rename_dir(
            [name for name in curr_dir.lower().split("\\") if name], new_dir)

    def walk(self, top_down=True):
        yield from self._walk(top_down, "")

    def recalculate_nodes(self):
        if self.root is not self:
            return self.root.recalculate_nodes()

        self._names_to_ids = {}
        self._ids_to_names = {}
        self._sub_nodes = {}
        tag_id = 0
        for b in self.tag_index:
            if b.id != 0xFFffFFff:
                tag_path = b.path.replace('/', '\\').strip("\\ ").lower()
                self._add_node(tag_id, [
                    name for name in tag_path.lower().split("\\") if name])
            tag_id += 1

    def _apply_names_to_tag_index(self, parent_dir=""):
        # rename tags
        for name in self._names_to_ids:
            tag_path = "\\".join((parent_dir, os.path.splitext(name)[0]))
            self.tag_index[self._names_to_ids[name]].path = tag_path

        # rename directories
        for name, sub_node in self._sub_nodes.items():
            sub_node._apply_names_to_tag_index("\\".join((parent_dir, name)))

    def _get_node(self, node_path_pieces, dir_index=0):
        if dir_index == len(node_path_pieces):
            return self

        name = node_path_pieces[dir_index]
        dir_index += 1
        if dir_index < len(node_path_pieces):
            # continue navigating directories downward
            if name not in self._sub_nodes:
                raise KeyError('Directory "%s" does not exist in "%s"' % (
                    name, "\\".join(node_path_pieces[: dir_index - 1])))

            return self._sub_nodes[name]._get_node(node_path_pieces, dir_index)
        elif name in self._sub_nodes:
            return self._sub_nodes[name]
        elif name in self._names_to_ids:
            return self._tag_index[self._names_to_ids[name]]
        else:
            raise KeyError('Directory/tag name "%s" does not exist in "%s"' % (
                name, "\\".join(node_path_pieces[: dir_index - 1])))

    def _add_dir(self, dir_pieces, dir_node=None, dir_index=0):
        name = None
        if dir_pieces:
            name = dir_pieces[dir_index]
            dir_index += 1
            if name not in self._sub_nodes:
                # plop a new directory in if one doesnt already exist
                self._sub_nodes[name] = TagDirectoryNode(
                    self.tag_index, (), self._shared_root)
            node = self._sub_nodes[name]
        else:
            node = self

        if dir_index < len(dir_pieces):
            # continue navigating directories downward
            node._add_dir(dir_pieces, dir_node, dir_index)
        elif dir_node is not None:
            # update the currently existing directories contents
            node._update(dir_node)
        else:
            # just added an empty dir_node in the previous "if" statement.
            # nothing to do but return
            pass

    def _rename_dir(self, curr_dir_pieces, new_dir, dir_index=0):
        if not curr_dir_pieces:
            # oh boy, we're renaming the root. we'll need to make a
            # new root and add this node to it at the new directory
            new_root = TagDirectoryNode(self.tag_index, (), self._shared_root)
            new_dir = new_dir.replace('/', '\\').strip("\\ ")
            new_dir_pieces = [name for name in new_dir.lower().split("\\") if name]
            try:
                self._shared_root.set(new_root)
                new_root._add_dir(new_dir_pieces, self)
            except Exception:
                self._shared_root.set(self)
                raise
            return

        name = curr_dir_pieces[dir_index]
        dir_index += 1

        if dir_index == len(curr_dir_pieces):
            # rename this directory
            if name not in self._sub_nodes:
                raise KeyError('Directory "%s" does not exist in "%s"' % (
                    name, "\\".join(curr_dir_pieces[: dir_index - 1])))

            new_dir = new_dir.replace('/', '\\').strip("\\ ")
            new_dir_pieces = [name for name in new_dir.lower().split("\\") if name]

            # apply renames to the tags in this directory node
            dir_node = self._sub_nodes.pop(name)
            try:
                dir_node._apply_names_to_tag_index("\\".join(new_dir_pieces))
                self.root._add_dir(new_dir_pieces, dir_node)
            except Exception:
                self._sub_nodes[name] = dir_node
                raise

        elif name in self._sub_nodes:
            # continue navigating directories downward
            self._sub_nodes[name]._rename_dir(
                curr_dir_pieces, new_dir, dir_index)
            if self.root.remove_empty and self._sub_nodes[name].shallow_empty:
                # remove empty directories
                self._sub_nodes.pop(name)
        else:
            raise KeyError('Directory "%s" does not exist in "%s"' % (
                name, "\\".join(curr_dir_pieces[: dir_index - 1])))

    def _add_node(self, tag_id_or_dir_node, tag_path_pieces, dir_index=0):
        name = tag_path_pieces[dir_index]
        dir_index += 1
        if dir_index < len(tag_path_pieces):
            # continue navigating directories downward
            if name not in self._sub_nodes:
                self._sub_nodes[name] = TagDirectoryNode(
                    self.tag_index, (), self._shared_root)

            self._sub_nodes[name]._add_node(
                tag_id_or_dir_node, tag_path_pieces, dir_index)

        elif not isinstance(tag_id_or_dir_node, TagDirectoryNode):
            # add this tag id to this directory
            tag_id = int(tag_id_or_dir_node)
            if self.tag_index[tag_id].id == 0xFFffFFff:
                return

            name_key = "%s.%s" % (name, self.tag_index[tag_id].class_1.enum_name)

            if name_key in self._names_to_ids:
                raise KeyError(
                    'Tag name "%s" already tied to tag_id "%s" in "%s"' %
                    (name_key, self._names_to_ids[name_key],
                     "\\".join(tag_path_pieces[: -1])))

            self._names_to_ids[name_key] = tag_id
            self._ids_to_names[tag_id] = name_key
        elif name in self._sub_nodes:
            # update an existing directory node with this one
            self._sub_nodes[name]._update(tag_id_or_dir_node)
        else:
            # add this directory node to the list of nodes
            self._sub_nodes[name] = tag_id_or_dir_node

    def _rename_tag(self, tag_path_pieces, new_path, dir_index=0):
        name = tag_path_pieces[dir_index]
        dir_index += 1
        if dir_index == len(tag_path_pieces):
            # rename this tag
            if name not in self._names_to_ids:
                raise KeyError('Tag name "%s" does not exist in "%s"' % (
                    name, "\\".join(tag_path_pieces[: dir_index - 1])))

            # pop the name out of names_to_ids and the id out of ids_to_names
            new_path = new_path.replace('/', '\\').strip("\\ ")
            tag_id = self._names_to_ids[name]
            tag_ref = self.tag_index[tag_id]

            old_tag_path = tag_ref.path
            old_name = self._ids_to_names[tag_id]
            new_tag_path_pieces = [
                name for name in new_path.lower().split("\\") if name]
            new_tag_path_pieces[-1] = os.path.splitext(new_tag_path_pieces[-1])[0]

            new_tag_path = "\\".join(new_tag_path_pieces)
            try:
                self._names_to_ids.pop(old_name)
                self._ids_to_names.pop(tag_id)
                self.root._add_node(tag_id, new_tag_path_pieces)
                tag_ref.path = new_tag_path
            except Exception:
                # revert changes and re-raise the exception
                if old_name is not None:
                    self._names_to_ids[old_name] = tag_id
                    self._ids_to_names[tag_id] = old_name
                tag_ref.path = old_tag_path
                raise

        elif name in self._sub_nodes:
            # continue navigating directories downward
            self._sub_nodes[name]._rename_tag(
                tag_path_pieces, new_path, dir_index)
            if self.root.remove_empty and self._sub_nodes[name].shallow_empty:
                # remove empty directories
                self._sub_nodes.pop(name)
        else:
            raise KeyError('Directory "%s" does not exist in "%s"' % (
                name, "\\".join(tag_path_pieces[: dir_index - 1])))

    def _update(self, other_node):
        if other_node is self:
            return

        for tag_id, tag_name in other_node._ids_to_names.items():
            self._add_node(tag_id, (os.path.splitext(tag_name)[0], ))

        for dir_name, sub_node in other_node._sub_nodes.items():
            if dir_name in self._sub_nodes:
                self._sub_nodes[dir_name]._update(sub_node)
            else:
                self._sub_nodes[dir_name] = sub_node

    def _walk(self, top_down, root=""):
        dirs = list(sorted(self._sub_nodes))
        files = list(sorted(self._names_to_ids))

        if top_down:
            yield root, dirs, files
        else:
            for dir_name in dirs:
                dir_path = "\\".join((root, dir_name)).lstrip("\\")
                yield from self._sub_nodes[dir_name]._walk(top_down, dir_path)

        if top_down:
            for dir_name in dirs:
                dir_path = "\\".join((root, dir_name)).lstrip("\\")
                yield from self._sub_nodes[dir_name]._walk(top_down, dir_path)
        else:
            yield root, dirs, files


if __name__ == "__main__":
    '''
    from reclaimer.meta.halo_map import get_tag_index
    from supyr_struct.buffer import get_rawdata

    tag_index = get_tag_index(
        get_rawdata(
            filepath="C:\\Users\\Moses\\Desktop\\halo_test\\maps\\putput.map")
        )

    dir_nodes = TagDirectoryNode(tag_index.tag_index)
    dir_nodes.pprint(do_printout=True, depth=1, extra_dir_spacing=False)
    dir_nodes.pprint("weapons\\assault rifle", do_printout=True, depth=None,
                     files=False, indexed=True)
    dir_nodes.pprint("weapons\\assault rifle", do_printout=True, depth=None,
                     dirs_first=1, indexed=True)
    #dir_nodes.rename_dir("weapons\\assault rifle\\",
    #                     "weapons\\assault rifle\\asdf\\")
    #dir_nodes.rename_dir("weapons\\assault rifle\\asdf\\",
    #                     "weapons\\assault rifle\\", )
    #dir_nodes.rename_dir("", "test\\")
    #dir_nodes.pprint(do_printout=True, depth=1, indexed=0)#'''
