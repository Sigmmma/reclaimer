from ..field_type_methods import *
from .constants import *


def h2_rawdata_ref_parser(self, desc, node=None, parent=None, attr_index=None,
                          rawdata=None, root_offset=0, offset=0, **kwargs):
    try:
        orig_offset = offset
        if node is None:
            parent[attr_index] = node = desc.get(BLOCK_CLS, self.node_cls)\
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
            if 'magic' in kwargs:
                magic_offset = node[1] - kwargs["magic"]

                if not node[0] or (magic_offset + node[0] > len(rawdata) or
                                   magic_offset <= 0):
                    # data is stored in a resource map, or the size is invalid
                    s_desc['TYPE'].parser(s_desc, None, node, 'STEPTREE', None)
                else:
                    s_desc['TYPE'].parser(
                        s_desc, None, node, 'STEPTREE', rawdata,
                        root_offset, magic_offset, **kwargs)
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

