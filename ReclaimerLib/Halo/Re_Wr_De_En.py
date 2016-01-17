from supyr_struct.Re_Wr_De_En import *
from supyr_struct.Defs.Constants import *


def Calc_Tag_Ref_Size(self, Block, **kwargs):
    '''Used to calculate the size of a tag
    reference string from a given string'''
    Block = Block.strip(self.Str_Delimiter)
    if len(Block):
        return len(Block) + 1
    return 0

def Tag_Ref_Size(New_Value=None, *args, **kwargs):
    '''Used to retrieve or set the byte size of a Halo tag
    reference string. If the string is empty, the actual amount
    of bytes it takes up is zero, otherwise it is (1+length) bytes.
    This is to account for the delimiter.
    
    When setting the size, the provided New_Value is expected to
    be including the delimiter, so the reverse operation is applied.
    If the string's length is 1(only a delimiter), the bytes size
    is zero, but otherwise it is (length-1).

    Lengths of 1 cant exist.'''
    
    if New_Value is not None:
        if New_Value <= 1:
            kwargs["Parent"].Tag_Path_Length = 0
        else:
            kwargs["Parent"].Tag_Path_Length = New_Value - 1
    else:
        Str_Len = kwargs["Parent"].Tag_Path_Length
        if Str_Len:
            return Str_Len + 1
        return Str_Len


def Enc_Tag_Ref_Str(self, Block_Data, Parent, Attr_Index):
    """This function is the same as Encode_String, except that
    when a halo reference string has zero length, the string doesnt
    actually exist. It's not just a delimiter character, the string
    isn't stored at all. To make it work, we instead return an
    empty bytes object if the string length is zero"""
    if len(Block_Data):
        return Encode_String(self, Block_Data, Parent, Attr_Index)
    return bytes()

def Decode_Raw_String(self, Bytes, Parent=None, Attr_Index=None):
    return Bytes.decode(encoding=self.Enc)




def Tag_Index_Reader(self, Desc, Parent=None, Raw_Data=None, Attr_Index=None,
                     Root_Offset=0, Offset=0, **kwargs):
    if Parent is not None:
        M_Head = Parent.PARENT.Mapfile_Header
        kwargs['Map_Magic'] = Parent.Index_Magic - M_Head.Tag_Index_Offset

    Array_Reader(self, Desc, Parent, Raw_Data, Attr_Index,
                 Root_Offset, Offset, **kwargs)


def Tag_Index_Writer(self, Parent, Write_Buffer, Attr_Index=None,
                     Root_Offset=0, Offset=0, **kwargs):
    if Parent is not None:
        M_Head = Parent.PARENT.Mapfile_Header
        kwargs['Map_Magic'] = Parent.Index_Magic - M_Head.Tag_Index_Offset
        
    Array_Writer(self, Parent, Write_Buffer, Attr_Index,
                 Root_Offset, Offset, **kwargs)
