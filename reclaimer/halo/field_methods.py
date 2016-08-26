from supyr_struct.field_methods import *
from .constants import *


def tag_ref_sizecalc(self, block, **kwargs):
    '''
    Used to calculate the size of a tag reference string from a given string
    '''
    block = block.split(self.str_delimiter)[0]
    if block:
        return len(block) + 1
    return 0

def tag_ref_size(block=None, parent=None, attr_index=None,
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
        strlen += 1*bool(strlen)
        return strlen
    if new_value <= 1:
        parent.path_length = 0
    else:
        parent.path_length = new_value - 1


def encode_tag_ref_str(self, block, parent=None, attr_index=None):
    """This function is the same as encode_string, except that
    when a halo reference string has zero length, the string doesnt
    actually exist. It's not just a delimiter character, the string
    isn't stored at all. To make it work, we instead return an
    empty bytes object if the string length is zero"""
    if block:
        return encode_string(self, block, parent=parent, attr_index=attr_index)
    return b''


def tag_index_reader(self, desc, parent=None, rawdata=None, attr_index=None,
                     root_offset=0, offset=0, **kwargs):
    if parent is not None:
        m_head = parent.map_header
        kwargs['magic'] = PC_INDEX_MAGIC - m_head.tag_index_offset

    array_reader(self, desc, parent, rawdata, attr_index,
                 root_offset, offset, **kwargs)


def tag_index_writer(self, parent, writebuffer, attr_index=None,
                     root_offset=0, offset=0, **kwargs):
    if parent is not None:
        m_head = parent.map_header
        kwargs['magic'] = PC_INDEX_MAGIC - m_head.tag_index_offset
        
    array_writer(self, parent, writebuffer, attr_index,
                 root_offset, offset, **kwargs)


def rawdata_reader(self, desc, parent, rawdata=None, attr_index=None,
                   root_offset=0, offset=0, **kwargs):
    if rawdata is not None:
        bytecount = parent.size

        if 'magic' in kwargs:
            offset = PC_TAG_INDEX_HEADER_SIZE + parent.pointer - kwargs['magic']
        rawdata.seek(root_offset + offset)
        parent[attr_index] = self.py_type(rawdata.read(bytecount))
        return offset + bytecount

    parent[attr_index] = self.py_type(b'\x00'*parent.size)
    return offset
