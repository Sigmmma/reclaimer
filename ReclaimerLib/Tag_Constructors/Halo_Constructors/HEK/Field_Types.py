from supyr_struct.Field_Types import *
from supyr_struct.Defs.Constants import *
from supyr_struct.Re_Wr_De_En import *


def Enc_Tag_Ref_Str(self, Block_Data, Parent, Attr_Index):
    """This function is the same as Encode_String, except that
    when a halo reference string has zero length, the string doesnt
    actually exist. It's not just a delimiter character, the string
    isn't stored at all. To make it work, we instead return an
    empty bytes object if the string length is zero"""
    if len(Block_Data):
        return Encode_String(self, Block_Data, Parent, Attr_Index)
    return bytes()


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
                

def Decode_Raw_String(self, Bytes, Parent=None, Attr_Index=None):
    return Bytes.decode(encoding=self.Enc)


tmp = {'Str':True, 'Default':'', 'Delimited':True,
       'Reader':Data_Reader, 'Writer':Data_Writer,
       'Decoder':Decode_Raw_String, 'Encoder':Encode_String}
Com = Combine

String_Var_Len = Field_Type(**Com({'Name':"Halo Ref Str", 'Size':1, 
                                   'Decoder':Decode_String, 'Enc':'latin-1',
                                   'Encoder':Enc_Tag_Ref_Str,
                                   'Size_Calc':Calc_Tag_Ref_Size}, tmp))

UTF16_Str_Data = Field_Type(**Com({'Name':"UTF16 Str Data", 'Size':2,
                                   'Size_Calc':Str_Size_Calc_UTF,
                                   'Enc':{"<":"utf_16_le",">":"utf_16_be"}},tmp))
