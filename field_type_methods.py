from supyr_struct.field_type_methods import *
from .constants import *


# this is ultra hacky, but it seems to be the only
# way to fix the tagid for the sounds resource map
sound_rsrc_id_map = {
    92: 15,  # sound\sfx\impulse\impacts\smallrock
    93: 17,  # sound\sfx\impulse\impacts\medrocks
    94: 19,  # sound\sfx\impulse\impacts\lrgrocks

    125: 25,  # sound\sfx\impulse\impacts\metal_chips
    126: 27,  # sound\sfx\impulse\impacts\metal_chip_med

    372: 123,  # sound\sfx\impulse\shellcasings\double_shell_dirt
    373: 125,  # sound\sfx\impulse\shellcasings\multi_shell_dirt
    374: 127,  # sound\sfx\impulse\shellcasings\single_shell_metal
    375: 129,  # sound\sfx\impulse\shellcasings\double_shell_metal
    376: 131,  # sound\sfx\impulse\shellcasings\multi_shell_metal

    1545: 529,  # sound\sfx\impulse\glass\glass_medium
    1546: 531,  # sound\sfx\impulse\glass\glass_large
    }


def tag_ref_str_sizecalc(self, node, **kwargs):
    '''
    Used to calculate the size of a tag reference string from a given string
    '''
    node = node.split(self.str_delimiter)[0]
    if node:
        return len(node) + 1
    return 0

def tag_ref_str_size(node=None, parent=None, attr_index=None,
                 rawdata=None, new_value=None, **kwargs):
    '''Used to retrieve or set the byte size of a Halo tag
    reference string. If the string is empty, the actual amount
    of bytes it takes up is zero, otherwise it is (1+length) bytes.
    This is to account for the delimiter.
    
    When setting the size, the provided new_value is expected to
    be including the delimiter, so the reverse operation is applied.
    If the string's length is 1(only a delimiter), the bytes size
    is zero, but otherwise it is (length-1).

    Lengths of 1 cant exist.'''
    
    if new_value is None:
        strlen = parent.path_length
        return strlen + bool(strlen)

    parent.path_length = (new_value - 1)*(new_value > 1)


def encode_tag_ref_str(self, node, parent=None, attr_index=None):
    """This function is the same as encode_string, except that
    when a halo reference string has zero length, the string doesnt
    actually exist. It's not just a delimiter character, the string
    isn't stored at all. To make it work, we instead return an
    empty bytes object if the string length is zero"""
    if node:
        return encode_string(self, node, parent=parent, attr_index=attr_index)
    return b''


def tag_ref_str_parser(self, desc, node=None, parent=None, attr_index=None,
                   rawdata=None, root_offset=0, offset=0, **kwargs):
    """
    """
    assert parent is not None and attr_index is not None, (
        "parent and attr_index must be provided " +
        "and not None when reading a data field.")
    if "tag_index" in kwargs:
        tag_index = kwargs["tag_index"]
        tagid = parent.id.tag_table_index
        if tagid >= 0 and tagid != 0xFFFF:
            try:
                parent[attr_index] = tag_index[tagid].tag.tag_path
            except (AttributeError, IndexError):
                # tag_index is a resource map tag_paths collection
                if kwargs['tag_cls'] == 'snd!':
                    # fix the sound reference tagid
                    parent.id[0] = tagid = sound_rsrc_id_map[tagid]
                    parent[attr_index] = tag_index[tagid].tag_path
                else:
                    # unable to get the tag path
                    parent[attr_index] = ""
        else:
            parent[attr_index] = ""
    elif rawdata:
        # read and store the node
        rawdata.seek(root_offset + offset)
        size = parent.get_size(attr_index, root_offset=root_offset,
                               offset=offset, rawdata=rawdata, **kwargs)
        parent[attr_index] = self.decoder(rawdata.read(size), desc=desc,
                                          parent=parent, attr_index=attr_index)
        return offset + size
    else:
        parent[attr_index] = desc.get(DEFAULT, self.default())

    return offset


def reflexive_parser(self, desc, node=None, parent=None, attr_index=None,
                     rawdata=None, root_offset=0, offset=0, **kwargs):
    """
    """
    try:
        __lsi__ = list.__setitem__
        orig_offset = offset
        if node is None:
            parent[attr_index] = node = desc.get(BLOCK_CLS, self.node_cls)\
                (desc, parent=parent)

        # If there is rawdata to build the structure from
        if rawdata is not None:
            offsets = desc['ATTR_OFFS']
            struct_off = root_offset + offset

            if self.f_endian == '=':
                for i in range(len(node)):
                    off = struct_off + offsets[i]
                    typ = desc[i]['TYPE']
                    __lsi__(node, i,
                            unpack(typ.enc, rawdata[off:off + typ.size])[0])
            elif self.f_endian == '<':
                for i in range(len(node)):
                    off = struct_off + offsets[i]
                    typ = desc[i]['TYPE']
                    __lsi__(node, i, unpack(typ.little.enc,
                                            rawdata[off:off + typ.size])[0])
            else:
                for i in range(len(node)):
                    off = struct_off + offsets[i]
                    typ = desc[i]['TYPE']
                    __lsi__(node, i, unpack(typ.big.enc,
                                            rawdata[off:off + typ.size])[0])

            # increment offset by the size of the struct
            offset += desc['SIZE']
        else:
            for i in range(len(node)):
                __lsi__(node, i,
                        desc[i].get(DEFAULT, desc[i]['TYPE'].default()))

        s_desc = desc.get('STEPTREE')
        if s_desc:
            magic = kwargs.get('magic')
            if magic is None:
                pass
            elif (node[1] - magic < 0 or node[1] - magic +
                  node[0]*s_desc['SUB_STRUCT'].get('SIZE', 0) > len(rawdata)):
                # the reflexive is corrupt for some reason
                #    (ex: bad hek+ extraction)
                node.size = node.pointer = 0

            if not node[0]:
                # reflexive is empty. no need to provide rawdata
                s_desc['TYPE'].parser(s_desc, None, node, 'STEPTREE', None)
            elif magic is not None:
                # parsing tag from a map
                s_desc['TYPE'].parser(s_desc, None, node, 'STEPTREE', rawdata,
                                      root_offset, node[1] - magic, **kwargs)
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


def rawdata_ref_parser(self, desc, node=None, parent=None, attr_index=None,
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
            if kwargs.get("parsing_resource"):
                # parsing JUST metadata from a resource cache
                if 'steptree_parents' not in kwargs and 'magic' in kwargs:
                    # need to skip over the rawdata
                    offset += node[0] + node[2] - kwargs['magic']
            elif 'magic' in kwargs:
                # use magic offset if it is valid
                if node[3]:
                    nonmagic_offset = node[3] - kwargs["magic"]
                else:
                    nonmagic_offset = node[2]

                if not node[0] or (nonmagic_offset + node[0] > len(rawdata) or
                                   nonmagic_offset <= 0):
                    # data is stored in a resource map, or the size is invalid
                    s_desc['TYPE'].parser(s_desc, None, node, 'STEPTREE', None)
                else:
                    s_desc['TYPE'].parser(
                        s_desc, None, node, 'STEPTREE', rawdata,
                        root_offset, nonmagic_offset, **kwargs)
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
