from ..field_type_methods import *
from .constants import *


def tbfd_parser(self, desc, node=None, parent=None, attr_index=None,
                rawdata=None, root_offset=0, offset=0, **kwargs):
    """
    """
    try:
        orig_offset = offset
        if node is None:
            parent[attr_index] = node = desc.get(BLOCK_CLS, self.node_cls)\
                (desc, parent=parent, init_attrs=rawdata is None)

        try:
            # if the parent reflexive structs size is 0 then this tbfd struct
            # doesnt actually exist, and shouldn't be parsed from the stream.
            if not parent.size:
                return offset
        except Exception:
            pass

        # If there is rawdata to build the structure from
        if rawdata is not None:
            # loop once for each field in the node
            for i in range(len(node)):
                offset = desc[i]['TYPE'].parser(desc[i], None, node, i, rawdata,
                                                root_offset, offset, **kwargs)

        # pass the incremented offset to the caller
        return offset
    except Exception as e:
        # if the error occurred while parsing something that doesnt have an
        # error report routine built into the function, do it for it.
        kwargs.update(buffer=rawdata, root_offset=root_offset)
        if 'i' in locals():
            e = format_parse_error(e, field_type=desc[i].get(TYPE),
                                   desc=desc.get(i), parent=node, attr_index=i,
                                   offset=offset, **kwargs)
        e = format_parse_error(e, field_type=self, desc=desc,
                               parent=parent, attr_index=attr_index,
                               offset=orig_offset, **kwargs)
        raise e


def tbfd_serializer(self, node, parent=None, attr_index=None,
                    writebuffer=None, root_offset=0, offset=0, **kwargs):
    """
    """
    try:
        try:
            # if the parent reflexive structs size is 0 then this tbfd struct
            # shouldn't even exist, and shouldn't be serialized to the stream.
            if not parent.size:
                return offset
        except Exception:
            pass

        orig_offset = offset
        desc = node.desc

        # loop once for each node in the node
        for i in range(len(node)):
            offset = desc[i]['TYPE'].serializer(
                node[i], node, i, writebuffer, root_offset, offset, **kwargs)

        # pass the incremented offset to the caller
        return offset
    except Exception as e:
        # if the error occurred while parsing something that doesnt have an
        # error report routine built into the function, do it for it.
        desc = locals().get('desc', None)
        kwargs.update(buffer=writebuffer, root_offset=root_offset)
        if 'i' in locals():
            kwargs.update(field_type=a_desc.get(TYPE), desc=desc.get(i),
                          parent=node, attr_index=i, offset=offset)
            e = format_serialize_error(e, **kwargs)

        kwargs.update(field_type=self, desc=desc, parent=parent,
                      attr_index=attr_index, offset=orig_offset)
        e = format_serialize_error(e, **kwargs)
        raise e

