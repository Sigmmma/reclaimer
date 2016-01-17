from supyr_struct.Field_Types import *
from supyr_struct.Tag_Blocks import *
from .Re_Wr_De_En import *


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


'''These Field_Types exist to easily identify where in a tag
that raw data refs, reflexives, and tag references exist.'''
Raw_Data_Ref = Field_Type(Name="Raw_Data_Ref", Struct=True,
                          Endian='=', Py_Type=List_Block,
                          Reader=Struct_Reader, Writer=Struct_Writer)

Reflexive = Field_Type(Name="Reflexive", Struct=True, Endian='=',
                       Py_Type=List_Block,
                       Reader=Struct_Reader, Writer=Struct_Writer)

Tag_Index_Ref = Field_Type(Name="Tag_Index_Ref", Struct=True, Endian='=',
                           Py_Type=List_Block,
                           Reader=Struct_Reader, Writer=Struct_Writer)

#the Tag_Index is the array that stores all the tag string paths and
#meta datas in a map file. This Field_Type exists so the Map_Magic
#can be easily supplied through the keyword argument "Map_Magic"
Tag_Index = Field_Type(Name="Tag_Index", Array=True, Endian='=',
                       Py_Type=List_Block,
                       Reader=Tag_Index_Reader, Writer=Tag_Index_Writer)
