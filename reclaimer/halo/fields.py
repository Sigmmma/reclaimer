from struct import unpack

from supyr_struct.fields import *
from supyr_struct.blocks import *
from .field_methods import *


'''These are varients of the standard Fields that have been
slightly modified based on how Halo needs to utilize them.'''
StringVarLen   = Field(base=StrLatin1, name="HaloRefStr",
                       encoder=encode_tag_ref_str, sizecalc=tag_ref_sizecalc)
FlUTF16StrData = Field(base=StrUtf16.little, name="UTF16StrData", endian='=',
                       decoder=decode_raw_string,  sizecalc=utf_sizecalc )
FlStrUTF16     = Field(base=StrUtf16.little, name="StrUTF16", endian='=',
                       decoder=decode_string,      sizecalc=delim_utf_sizecalc )

#forces little endian integers and float
FlUInt16 = Field(base=UInt16.little, name="FlUInt16", endian='=')
FlUInt32 = Field(base=UInt32.little, name="FlUInt32", endian='=')

FlEnum16 = Field(base=Enum16.little, name="FlEnum16", endian='=')
FlEnum32 = Field(base=Enum32.little, name="FlEnum32", endian='=')

FlBool16 = Field(base=Bool16.little, name="FlBool16", endian='=')
FlBool32 = Field(base=Bool32.little, name="FlBool32", endian='=')

FlSInt16 = Field(base=SInt16.little, name="FlSInt16", endian='=')
FlSInt32 = Field(base=SInt32.little, name="FlSInt32", endian='=')

FlFloat = Field(base=Float.little, name="FlFloat", endian='=')

'''These Fields exist to easily identify where in a tag
that raw data refs, reflexives, and tag references exist.'''
RawDataRef  = Field(base=Struct, name="RawDataRef")
Reflexive   = Field(base=Struct, name="Reflexive")
TagIndexRef = Field(base=Struct, name="TagIndexRef")

#the Tag_Index is the array that stores all the tag string paths and
#meta datas in a map file. This Field exists so the Map_Magic
#can be easily supplied through the keyword argument "Map_Magic"
TagIndex = Field(base=Array, name="TagIndex",
                 reader=tag_index_reader, writer=tag_index_writer)
