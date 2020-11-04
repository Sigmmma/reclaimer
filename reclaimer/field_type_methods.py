#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from struct import unpack

from supyr_struct.field_type_methods import *
from reclaimer.constants import *


def tag_cstring_parser(self, desc, node=None, parent=None, attr_index=None,
                       rawdata=None, root_offset=0, offset=0, **kwargs):
    """
    """
    assert parent is not None and attr_index is not None, (
        "parent and attr_index must be provided " +
        "and not None when reading a data field.")

    if rawdata is not None:
        max_len = desc.get(MAX, 0xFFffFFff)
        offset = parent.get_meta(POINTER, attr_index, **kwargs)

        start = root_offset + offset
        charsize = self.size
        delimiter = self.delimiter

        # if the character size is greater than 1 we need to do special
        # checks to ensure the position the null terminator was found at
        # is not overlapping the boundary between individual characters.
        size = rawdata.find(delimiter, start) - start
        if size > max_len:
            size = max_len

        if size >= 0:
            rawdata.seek(start)
            # read and store the string
            parent[attr_index] = self.decoder(
                rawdata.read(size), desc=desc,
                parent=parent, attr_index=attr_index)

            return offset + size + charsize

    parent[attr_index] = desc.get(DEFAULT, self.default())

    return offset


def tag_ref_str_sizecalc(self, node, **kwargs):
    '''
    Used to calculate the size of a tag reference string from a given string
    '''
    node = node.split(self.str_delimiter)[0]
    if node:
        return len(node) + 1
    return 0


def get_set_zone_asset_size(node=None, parent=None, attr_index=None,
                            rawdata=None, new_value=None, **kwargs):
    if new_value is not None:
        parent.size = new_value
    elif "map_pointer_converter" in kwargs:
        return 0
    return parent.size


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
    tag_index_manager = kwargs.get("tag_index_manager")
    if tag_index_manager:
        tag_index_ref = tag_index_manager.get_tag_index_ref(parent.id)
        if tag_index_ref is None or (not kwargs.get("indexed") and
                                     tag_index_ref.id != parent.id):
            parent[attr_index] = ""
        else:
            parent[attr_index] = tag_index_ref.path

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


def read_string_id_string(parent=None, attr_index=None, rawdata=None, offset=0,
                          map_string_id_manager=None, **kwargs):
    assert parent is not None
    if map_string_id_manager:
        parent[attr_index] = map_string_id_manager.get_string(parent)
    elif "map_pointer_converter" not in kwargs:
        desc = parent.desc
        str_len = (parent[0] & 0xFFffFFff) >> (desc[STRINGID_IDX_BITS] +
                                               desc[STRINGID_SET_BITS])
        if str_len:
            rawdata.seek(offset)
            parent[attr_index] = rawdata.read(str_len).strip(b'\x00').decode(
                encoding="latin-1")
        else:
            parent[attr_index] = ""

        offset += str_len + 1  # add 1 for the null terminator
    else:
        parent[attr_index] = ""

    return offset


def write_string_id_string(parent=None, attr_index=None,
                           writebuffer=None, offset=0, **kwargs):
    assert parent is not None
    if "map_pointer_converter" in kwargs:
        return offset

    raw_string = parent.string.encode(encoding="latin-1") + b'\x00'
    writebuffer.seek(offset)
    writebuffer.write(raw_string)
    return offset + len(raw_string)


def get_set_string_id_size(parent=None, attr_index=None,
                           new_value=None, **kwargs):
    desc = parent.desc
    string_id = parent[0]
    idx_set_bit_ct = desc[STRINGID_IDX_BITS] + desc[STRINGID_SET_BITS]
    len_bit_ct = desc[STRINGID_LEN_BITS]
    if new_value is None:
        return (string_id & 0xFFffFFff) >> idx_set_bit_ct
    elif new_value > (1 << len_bit_ct):
        raise ValueError("String ID's cannot be longer than %s characters." %
                         ((1 << len_bit_ct) - 1))
    elif new_value > 0:
        new_value -= 1  # subtract the null delimiter
    else:
        assert new_value == 0
    parent[0] = (string_id & ((1 << idx_set_bit_ct) - 1)) + (
        new_value << idx_set_bit_ct)


def reflexive_parser(self, desc, node=None, parent=None, attr_index=None,
                     rawdata=None, root_offset=0, offset=0, **kwargs):
    """
    """
    try:
        __lsi__ = list.__setitem__
        orig_offset = offset
        if node is None:
            parent[attr_index] = node = desc.get(NODE_CLS, self.node_cls)\
                (desc, parent=parent)

        # If there is rawdata to build the structure from
        if rawdata is not None:
            struct_off = root_offset + offset

            if self.f_endian == '=':
                for i, off in enumerate(desc[ATTR_OFFS]):
                    off += struct_off
                    typ = desc[i][TYPE]
                    __lsi__(node, i, typ.struct_unpacker(
                        rawdata[off:off + typ.size])[0])
            elif self.f_endian == '<':
                for i, off in enumerate(desc[ATTR_OFFS]):
                    off += struct_off
                    typ = desc[i][TYPE].little
                    __lsi__(node, i, typ.struct_unpacker(
                        rawdata[off:off + typ.size])[0])
            else:
                for i, off in enumerate(desc[ATTR_OFFS]):
                    off += struct_off
                    typ = desc[i][TYPE].big
                    __lsi__(node, i, typ.struct_unpacker(
                        rawdata[off:off + typ.size])[0])

            # increment offset by the size of the struct
            offset += desc[SIZE]
        else:
            for i in range(len(node)):
                __lsi__(node, i, desc[i].get(
                    DEFAULT, desc[i][TYPE].default()))

        s_desc = desc.get(STEPTREE)
        if s_desc:
            pointer_converter = kwargs.get('map_pointer_converter')
            safe_mode = kwargs.get("safe_mode", True) and not desc.get(IGNORE_SAFE_MODE)

            if pointer_converter is not None:
                file_ptr = pointer_converter.v_ptr_to_f_ptr(node[1])
                if safe_mode:
                    # make sure the reflexive sizes are within sane bounds.
                    node[0] = min(node[0], max(SANE_MAX_REFLEXIVE_COUNT, s_desc.get(MAX, 0)))

                if (file_ptr < 0 or file_ptr +
                    node[0]*s_desc[SUB_STRUCT].get(SIZE, 0) > len(rawdata)):
                    # the reflexive is corrupt for some reason
                    #    (ex: bad hek+ extraction)
                    node[0] = node[1] = 0

            elif node[0] > max(SANE_MAX_REFLEXIVE_COUNT, s_desc.get(MAX, 0)):
                raise ValueError("Reflexive size is above highest allowed value.")

            if not node[0]:
                # reflexive is empty. no need to provide rawdata
                s_desc[TYPE].parser(s_desc, None, node, STEPTREE, None)
            elif pointer_converter is not None:
                # parsing tag from a map
                s_desc[TYPE].parser(s_desc, None, node, STEPTREE, rawdata,
                                      root_offset, file_ptr, **kwargs)
            elif 'steptree_parents' not in kwargs:
                offset = s_desc[TYPE].parser(s_desc, None, node, STEPTREE,
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


def reflexive_array_parser(self, desc, node=None, parent=None, attr_index=None,
                           rawdata=None, root_offset=0, offset=0, **kwargs):
    '''
    Variant of array_parser which ensures there is enough rawdata to parse the array.
    '''
    try:
        if parent is not None and rawdata is not None:
            if root_offset + offset + parent.size * desc['SUB_STRUCT'][SIZE] > len(rawdata):
                raise ValueError("Reflexive size is out of bounds of input stream.")

        return array_parser(
            self, desc, node, parent, attr_index, rawdata, root_offset, offset, **kwargs
            )
    except Exception as e:
        e = format_parse_error(e, field_type=self, desc=desc,
                               parent=parent, attr_index=attr_index,
                               offset=offset, root_offset=root_offset,
                               buffer=rawdata, **kwargs)
        raise e


def rawdata_ref_parser(self, desc, node=None, parent=None, attr_index=None,
                       rawdata=None, root_offset=0, offset=0, **kwargs):
    try:
        orig_offset = offset
        if node is None:
            parent[attr_index] = node = desc.get(NODE_CLS, self.node_cls)\
                (desc, parent=parent, init_attrs=rawdata is None)

        # If there is rawdata to build the structure from
        if rawdata is not None:
            # loop once for each field in the node
            for i, off in enumerate(desc['ATTR_OFFS']):
                desc[i][TYPE].parser(desc[i], None, node, i, rawdata,
                                     root_offset, offset + off, **kwargs)

            # increment offset by the size of the struct
            offset += desc[SIZE]

        s_desc = desc.get(STEPTREE)
        if s_desc:
            pointer_converter = kwargs.get("map_pointer_converter")
            safe_mode = kwargs.get("safe_mode", True) and not s_desc.get(IGNORE_SAFE_MODE)

            if pointer_converter is not None:
                node[0] = max(0, min(node[0], s_desc.get(MAX, node[0])))

            #if safe_mode:
            #    if pointer_converter is not None:
            #        node[0] = max(0, min(node[0], s_desc.get(MAX, node[0])))
            #    elif node[0] > s_desc.get(MAX, node[0]):
            #        raise ValueError("Rawdata size is above highest allowed value.")

            if kwargs.get("parsing_resource"):
                # parsing JUST metadata from a resource cache
                node_size = node[0]
                if 'steptree_parents' not in kwargs and pointer_converter is not None:
                    # need to skip over the rawdata
                    offset += node_size + node[2]

                node[0] = 0
                s_desc[TYPE].parser(s_desc, None, node, STEPTREE, None)
                node[0] = node_size
            elif pointer_converter is not None:
                file_ptr = pointer_converter.v_ptr_to_f_ptr(node[3])
                if not node[3] or file_ptr < 0:
                    file_ptr = node[2]

                if not node[0] or (file_ptr + node[0] > len(rawdata) or
                                   file_ptr <= 0):
                    # data is stored in a resource map, or the size is invalid
                    s_desc[TYPE].parser(s_desc, None, node, STEPTREE, None)
                else:
                    s_desc[TYPE].parser(
                        s_desc, None, node, STEPTREE, rawdata,
                        root_offset, file_ptr, **kwargs)
            elif 'steptree_parents' not in kwargs:
                offset = s_desc[TYPE].parser(s_desc, None, node, STEPTREE,
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


def tag_ref_str_serializer(self, node, parent=None, attr_index=None,
                           writebuffer=None, root_offset=0, offset=0, **kwargs):
    if "map_pointer_converter" in kwargs:
        # don't serialize the string
        return offset

    node_bytes = self.encoder(node, parent, attr_index)
    writebuffer.seek(root_offset + offset)
    writebuffer.write(node_bytes)
    size = parent.get_size(attr_index, root_offset=root_offset,
                           offset=offset, **kwargs)
    if size - len(node_bytes):
        writebuffer.write(b'\x00'*(size - len(node_bytes)))
    return offset + size
