from ..field_type_methods import *
from .constants import *


def h2_rawdata_ref_parser(self, desc, node=None, parent=None, attr_index=None,
                          rawdata=None, root_offset=0, offset=0, **kwargs):
    try:
        orig_offset = offset
        if node is None:
            parent[attr_index] = node = desc.get(NODE_CLS, self.node_cls)\
                (desc, parent=parent, init_attrs=rawdata is None)

        # If there is rawdata to build the structure from
        if rawdata is not None:
            offsets = desc['ATTR_OFFS']
            # loop once for each field in the node
            for i in range(len(node)):
                desc[i]['TYPE'].parser(desc[i], None, node, i, rawdata,
                                       root_offset, offset + offsets[i],
                                       **kwargs)

            # increment offset by the size of the struct
            offset += desc['SIZE']

        s_desc = desc.get('STEPTREE')
        if s_desc:
            pointer_converter = kwargs.get("map_pointer_converter")
            if pointer_converter is not None:
                file_ptr = pointer_converter.v_ptr_to_f_ptr(node[1])
                if not node[0] or (file_ptr + node[0] > len(rawdata) or
                                   file_ptr <= 0):
                    # data is stored in a resource map, or the size is invalid
                    s_desc['TYPE'].parser(s_desc, None, node, 'STEPTREE', None)
                else:
                    s_desc['TYPE'].parser(
                        s_desc, None, node, 'STEPTREE', rawdata,
                        root_offset, file_ptr, **kwargs)
            elif 'steptree_parents' not in kwargs:
                offset = s_desc['TYPE'].parser(s_desc, None, node, 'STEPTREE',
                                               rawdata, root_offset, offset,
                                               **kwargs)
            else:
                kwargs['steptree_parents'].append(node)

        # pass the incremented offset to the caller
        return offset
    except Exception as e:
        # if the error occurred while parsing something that doesnt have an
        # error report routine built into the function, do it for it.
        kwargs.update(buffer=rawdata, root_offset=root_offset)
        if 's_desc' in locals():
            e = format_parse_error(e, field_type=s_desc.get(TYPE), desc=s_desc,
                                  parent=node, attr_index=STEPTREE,
                                  offset=offset, **kwargs)
        elif 'i' in locals():
            e = format_parse_error(e, field_type=desc[i].get(TYPE),
                                   desc=desc[i], parent=node, attr_index=i,
                                   offset=offset, **kwargs)
        e = format_parse_error(e, field_type=self, desc=desc,
                               parent=parent, attr_index=attr_index,
                               offset=orig_offset, **kwargs)
        raise e


def h2_tag_ref_parser(self, desc, node=None, parent=None, attr_index=None,
                      rawdata=None, root_offset=0, offset=0, **kwargs):
    # parse tag_class and id(if meta) or path length(if not meta)
    try:
        orig_offset = offset
        if node is None:
            parent[attr_index] = node = desc.get(NODE_CLS, self.node_cls)\
                (desc, parent=parent, init_attrs=rawdata is None)

        # If there is rawdata to build the structure from
        if rawdata is not None:
            offsets = desc['ATTR_OFFS']
            if "map_pointer_converter" in kwargs:
                attr_indices = (0, 1)
                node[2] = 0
            else:
                attr_indices = (0, 2)
                node[1] = 0xFFffFFff

            # loop once for each field in the node
            for i in attr_indices:
                desc[i]['TYPE'].parser(desc[i], None, node, i, rawdata,
                                       root_offset, offset + offsets[i],
                                       **kwargs)

            # increment offset by the size of the struct
            offset += desc['SIZE']

        if 'steptree_parents' in kwargs:
            kwargs['steptree_parents'].append(node)
        else:
            s_desc = desc.get('STEPTREE')
            offset = s_desc['TYPE'].parser(s_desc, None, node, 'STEPTREE',
                                           rawdata, root_offset, offset,
                                           **kwargs)

        # pass the incremented offset to the caller
        return offset
    except Exception as e:
        # if the error occurred while parsing something that doesnt have an
        # error report routine built into the function, do it for it.
        kwargs.update(buffer=rawdata, root_offset=root_offset)
        if 's_desc' in locals():
            e = format_parse_error(e, field_type=s_desc.get(TYPE), desc=s_desc,
                                  parent=node, attr_index=STEPTREE,
                                  offset=offset, **kwargs)
        elif 'i' in locals():
            e = format_parse_error(e, field_type=desc[i].get(TYPE),
                                   desc=desc[i], parent=node, attr_index=i,
                                   offset=offset, **kwargs)
        e = format_parse_error(e, field_type=self, desc=desc,
                               parent=parent, attr_index=attr_index,
                               offset=orig_offset, **kwargs)
        raise e

    
def h2_tag_ref_serializer(self, node, parent=None, attr_index=None,
                          writebuffer=None, root_offset=0, offset=0, **kwargs):
    # serialize tag_class and id(if meta) or path length(if not meta)
    try:
        orig_offset = offset
        desc = node.desc
        offsets = desc['ATTR_OFFS']
        is_tree_root = 'steptree_parents' not in kwargs

        if is_tree_root:
            kwargs['steptree_parents'] = parents = []
        if hasattr(node, 'STEPTREE'):
            kwargs['steptree_parents'].append(node)

        # loop once for each node in the node
        if "map_pointer_converter" in kwargs:
            attr_indices = (0, 1)
        else:
            attr_indices = (0, 2)

        # loop once for each field in the node
        for i in attr_indices:
            desc[i]['TYPE'].serializer(
                node[i], node, i, writebuffer, root_offset,
                offset + offsets[i], **kwargs)

        # increment offset by the size of the struct
        offset += desc['SIZE']
        if is_tree_root:
            del kwargs['steptree_parents']
            s_desc = node.desc['STEPTREE']
            offset = s_desc['TYPE'].serializer(
                p_node.STEPTREE, p_node, 'STEPTREE', writebuffer,
                root_offset, offset, **kwargs)

        # pass the incremented offset to the caller
        return offset
    except Exception as e:
        # if the error occurred while parsing something that doesnt have an
        # error report routine built into the function, do it for it.
        desc = locals().get('desc', None)
        kwargs.update(buffer=writebuffer, root_offset=root_offset)
        if 's_desc' in locals():
            kwargs.update(field_type=s_desc.get(TYPE), desc=s_desc,
                          parent=p_node, attr_index=STEPTREE, offset=offset)
            e = format_serialize_error(e, **kwargs)
        elif 'a_desc' in locals():
            kwargs.update(field_type=a_desc.get(TYPE), desc=a_desc,
                          parent=node, attr_index=i, offset=offset)
            e = format_serialize_error(e, **kwargs)

        kwargs.update(field_type=self, desc=desc, parent=parent,
                      attr_index=attr_index, offset=orig_offset)
        e = format_serialize_error(e, **kwargs)
        raise e
