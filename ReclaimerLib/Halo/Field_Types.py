from struct import unpack

from supyr_struct.Field_Types import *
from supyr_struct.Tag_Blocks import *
from .Re_Wr_De_En import *


tmp = {'Str':True, 'Default':'', 'Delimited':True,
       'Reader':Data_Reader, 'Writer':Data_Writer,
       'Decoder':Decode_Raw_String, 'Encoder':Encode_String}
Com = Combine

'''These are varients of the standard Field_Types that have been
slightly modified based on how Halo needs to utilize them.'''
String_Var_Len = Field_Type(**Com({'Name':"Halo Ref Str", 'Size':1, 
                                   'Decoder':Decode_String, 'Enc':'latin-1',
                                   'Encoder':Enc_Tag_Ref_Str,
                                   'Size_Calc':Calc_Tag_Ref_Size}, tmp))

FL_UTF16_Str_Data = Field_Type(**Com({'Name':"UTF16 Str Data", 'Size':2,
                                      'Size_Calc':Str_Size_Calc_UTF,
                                      'Enc':"utf_16_le"},tmp))
FL_Str_UTF16 = Field_Type(**Com({'Name':"Str_UTF16", 'Size':2,
                               'Size_Calc':Delim_Str_Size_Calc_UTF,
                               'Enc':"utf_16_le", 'Decoder':Decode_String},tmp))

tmp = {'Data':True, 'Size_Calc':Default_Size_Calc,
       'Size':2, 'Max':2**16-1, 'Enc':"<H", "Endian":'<',
       'Reader':F_S_Data_Reader, 'Writer':Data_Writer,
       'Decoder':Decode_Numeric, 'Encoder':Encode_Numeric}

FL_UInt16 = Field_Type(**Com({"Name":"FL_UInt16", 'Default':0 }, tmp))
FL_Enum16 = Field_Type(**Com({"Name":"FL_Enum16", 'Enum':True,
                              'Py_Type':Enum_Block, 'Data_Type':int}, tmp))
FL_Bool16 = Field_Type(**Com({"Name":"FL_Bool16", 'Bool':True,
                              'Py_Type':Bool_Block, 'Data_Type':int}, tmp))

tmp['Size'], tmp['Max'], tmp['Enc'] = 4, 2**32-1, "<I"
FL_UInt32 = Field_Type(**Com({"Name":"FL_UInt32", 'Default':0 }, tmp))
FL_Enum32 = Field_Type(**Com({"Name":"FL_Enum32", 'Enum':True,
                              'Py_Type':Enum_Block, 'Data_Type':int}, tmp))
FL_Bool32 = Field_Type(**Com({"Name":"FL_Bool32", 'Bool':True,
                              'Py_Type':Bool_Block, 'Data_Type':int}, tmp))

tmp["Default"] = 0
FL_SInt16 = Field_Type(**Com({"Name":"FL_SInt16", "Size":2, "Enc":"<h",
                              'Min':-32768, 'Max':32767 }, tmp))
FL_SInt32 = Field_Type(**Com({"Name":"FL_SInt32", "Size":4, "Enc":"<i",
                              'Min':-2147483648, 'Max':2147483647 }, tmp))

tmp["Default"] = 0.0
FL_Float = Field_Type(**Com({"Name":"FL_Float", "Size":4, "Enc":"<f",
                             "Max":unpack('>f',b'\x7f\x7f\xff\xff'),
                             "Min":unpack('>f',b'\xff\x7f\xff\xff') }, tmp))

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
