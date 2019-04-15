from os.path import splitext

class TagIndexManager:
    _tag_index = ()
    _tag_index_map = ()

    _directory_nodes = None

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

        self._directory_nodes = TagDirectoryNode(self.tag_index)

    @property
    def tag_index(self): return self._tag_index
    @property
    def directory_nodes(self): return self._directory_nodes

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
            self._shared_root = SharedRoot(self)
        else:
            self._shared_root = shared_root

        if self.root is self:
            # this is the root node. add entire tag index as children
            self.recalculate_nodes()
        else:
            for tag_id in dir_items:
                self._add_node(tag_id, dir_items[tag_id])

    @property
    def names_to_ids(self): return dict(self._names_to_ids)
    @property
    def ids_to_names(self): return dict(self._ids_to_names)
    @property
    def sub_nodes(self): return dict(self._sub_nodes)
    @property
    def tag_index(self): return self._tag_index
    @property
    def root(self): return self._shared_root.get()
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

    def rename_tag(self, curr_path, new_path):
        curr_path = curr_path.replace('/', '\\').strip("\\ ")
        return self._rename_tag(curr_path.lower().split("\\"), new_path)

    def rename_tag_by_id(self, tag_id, new_path):
        tag_ref = self.tag_index[tag_id]
        curr_path = tag_ref.path.replace('/', '\\').strip("\\ ")
        curr_path = "%s.%s" % (name, tag_ref.class_1.enum_name)
        return self._rename_tag(curr_path.lower().split("\\"), new_path)

    def rename_dir(self, curr_dir, new_dir):
        return self._rename_dir(
            curr_dir.replace('/', '\\').strip("\\ ").split("\\"), new_dir)

    def recalculate_nodes(self):
        if self.root is not self:
            return self.root.recalculate_nodes()

        self._names_to_ids = {}
        self._ids_to_names = {}
        self._sub_nodes = {}
        tag_id = 0
        for b in self.tag_index:
            tag_path = "%s.%s" % (b.path.replace('/', '\\').strip("\\ "), b.class_1.enum_name)
            self._add_node(tag_id, tag_path.lower().split("\\"))
            tag_id += 1

    def _apply_names_to_tag_index(self, parent_dir=""):
        # rename tags
        for name in self._names_to_ids:
            tag_path = "\\".join(parent_dir, splitext(name)[0])
            self.tag_index[self._ids_to_names[name]].path = tag_path

        # rename directories
        for name, sub_node in self._sub_nodes.items():
            sub_node._apply_names_to_tag_index("\\".join(parent_dir, name))

    def _add_node(self, tag_id_or_dir_node, tag_path_pieces, dir_index=0):
        name = tag_path_pieces[dir_index]
        dir_index += 1
        if dir_index < len(tag_path_pieces):
            # continue navigating directories downward
            if name not in self._sub_nodes:
                self._sub_nodes[name] = TagDirectoryNode(self.tag_index, (), self.root)

            self._sub_nodes[name]._add_node(
                tag_id_or_dir_node, tag_path_pieces, dir_index)

        elif not isinstance(tag_id_or_dir_node, TagDirectoryNode):
            # add this tag id to this directory
            tag_id = int(tag_id_or_dir_node)
            name_key = "%s.%s" % (name, self.tag_index[tag_id].class_1.enum_name)

            if name_key in self._names_to_ids:
                raise KeyError(
                    'Tag name "%s" already tied to tag_id "%s" in "%s"' %
                    (name_key, self._names_to_ids[name],
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
            # pop the name out of names_to_ids and the id out of ids_to_names
            new_path = new_path.replace('/', '\\').strip("\\ ")
            tag_id = self.names_to_ids.pop(name)
            tag_ref = self.tag_index[tag_id]

            old_tag_path = tag_ref.path
            old_name = self.ids_to_names[tag_id]
            new_tag_path_pieces = new_path.lower().split("\\")
            new_tag_path = splitext(new_tag_path_pieces[-1])
            if len(new_tag_path_pieces) > 1:
                new_tag_path = "\\".join(new_tag_path_pieces[: -1], new_tag_path)

            try:
                self.ids_to_names.pop(tag_id)
                self.root._add_node(tag_id, new_tag_path_pieces)
                tag_ref.path = new_tag_path
            except Exception:
                # revert changes and re-raise the exception
                if old_name is not None:
                    self.names_to_ids[old_name] = tag_id
                    self.ids_to_names[tag_id] = old_name
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
            raise KeyError('Directory "%s" does not exist in "%s".' % (
                name, "\\".join(tag_path_pieces[: dir_index - 1])))

    def _add_dir(self, dir_pieces, new_dir=None, dir_index=0):
        if new_dir is None:
            new_dir = TagDirectoryNode(self.tag_index, (), self.root)

        if dir_pieces:
            name = dir_pieces[dir_index]
            dir_index += 1

        if name not in self._sub_nodes:
            # plop the new directory in and be done with it
            self._sub_nodes[name] = new_dir
        elif dir_index == len(dir_pieces):
            # update the currently existing directories contents
            self._sub_nodes[name]._update(new_dir)
        else:
            # continue navigating directories downward
            self._sub_nodes[name]._add_dir(dir_pieces, new_dir, dir_index)

    def _rename_dir(self, curr_dir_pieces, new_dir, dir_index=0):
        if curr_dir_pieces:
            name = curr_dir_pieces[dir_index]
            dir_index += 1

        if dir_index == len(curr_dir_pieces):
            # rename this directory
            new_dir = new_dir.replace('/', '\\').strip("\\ ")
            new_dir_pieces = new_dir.lower().split("\\")

            # apply renames to the tags in this directory node
            self._apply_names_to_tag_index("\\".join(new_dir_pieces))
            self.root._add_dir(new_dir_pieces, new_dir)

        elif name in self._sub_nodes:
            # continue navigating directories downward
            self._sub_nodes[name]._rename_dir(
                curr_dir_pieces, new_path, dir_index)
            if self.root.remove_empty and self._sub_nodes[name].shallow_empty:
                # remove empty directories
                self._sub_nodes.pop(name)
        else:
            raise KeyError('Directory "%s" does not exist in "%s".' % (
                name, "\\".join(curr_dir_pieces[: dir_index - 1])))

    def _update(self, other_node):
        if other_node is self:
            return

        for tag_id, tag_name in other_node.ids_to_names.items():
            self._add_node(tag_id, (tag_name, ))

        for dir_name, sub_node in other_node.sub_nodes.items():
            if dir_name in self._sub_nodes:
                self._sub_nodes[dir_name]._update(sub_node)
            else:
                self._sub_nodes[dir_name] = sub_node
