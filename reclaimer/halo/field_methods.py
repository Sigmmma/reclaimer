from supyr_struct.field_methods import *
from .constants import *


def tag_ref_sizecalc(self, block, **kwargs):
    '''Used to calculate the size of a tag
    reference string from a given string'''
    block = block.strip(self.str_delimiter)
    if len(block):
        return len(block) + 1
    return 0

def tag_ref_size(new_value=None, *args, **kwargs):
    '''Used to retrieve or set the byte size of a Halo tag
    reference string. If the string is empty, the actual amount
    of bytes it takes up is zero, otherwise it is (1+length) bytes.
    This is to account for the delimiter.
    
    When setting the size, the provided new_value is expected to
    be including the delimiter, so the reverse operation is applied.
    If the string's length is 1(only a delimiter), the bytes size
    is zero, but otherwise it is (length-1).

    Lengths of 1 cant exist.'''
    
    if new_value is not None:
        if new_value <= 1:
            kwargs["parent"].Tag_Path_Length = 0
        else:
            kwargs["parent"].Tag_Path_Length = new_value - 1
    else:
        strlen = kwargs["parent"].Tag_Path_Length
        if strlen:
            return strlen + 1
        return strlen


def encode_tag_ref_str(self, block, parent, attr_index):
    """This function is the same as encode_string, except that
    when a halo reference string has zero length, the string doesnt
    actually exist. It's not just a delimiter character, the string
    isn't stored at all. To make it work, we instead return an
    empty bytes object if the string length is zero"""
    if len(block):
        return encode_string(self, block, parent, attr_index)
    return bytes()

def decode_raw_string(self, rawbytes, parent=None, attr_index=None):
    return rawbytes.decode(encoding=self.enc)




def tag_index_reader(self, desc, parent=None, raw_data=None, attr_index=None,
                     root_offset=0, offset=0, **kwargs):
    if parent is not None:
        m_head = parent.PARENT.Mapfile_Header
        kwargs['magic'] = PC_INDEX_MAGIC - m_head.Tag_Index_Offset

    array_reader(self, desc, parent, raw_data, attr_index,
                 root_offset, offset, **kwargs)


def tag_index_writer(self, parent, write_buffer, attr_index=None,
                     root_offset=0, offset=0, **kwargs):
    if parent is not None:
        m_head = parent.PARENT.Mapfile_Header
        kwargs['magic'] = PC_INDEX_MAGIC - m_head.Tag_Index_Offset
        
    array_writer(self, parent, write_buffer, attr_index,
                 root_offset, offset, **kwargs)
