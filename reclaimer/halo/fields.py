from struct import unpack

from supyr_struct.editor.constants import *
from supyr_struct.fields import *
from supyr_struct.blocks import *
from .field_methods import *


'''These are varients of the standard Fields that have been
slightly modified based on how Halo needs to utilize them.'''
StringVarLen = Field(base=StrLatin1, name="HaloRefStr",
                     encoder=encode_tag_ref_str, sizecalc=tag_ref_sizecalc)
FlUTF16StrData = Field(base=StrUtf16, name="UTF16StrData",
                       enc=StrUtf16.little.enc, decoder=decode_raw_string,
                       sizecalc=utf_sizecalc )
FlStrUTF16 = Field(base=StrUtf16, name="StrUTF16",
                   enc=StrUtf16.little.enc, decoder=decode_string,
                   sizecalc=delim_utf_sizecalc )

#forces little endian integers and float
FlUInt16 = Field(base=UInt16.little, name="FlUInt16", enc=UInt16.little.enc)
FlUInt32 = Field(base=UInt32.little, name="FlUInt32", enc=UInt32.little.enc)

FlUEnum16 = Field(base=UEnum16.little, name="FlUEnum16", enc=UEnum16.little.enc)
FlUEnum32 = Field(base=UEnum32.little, name="FlUEnum32", enc=UEnum32.little.enc)

FlBool16 = Field(base=Bool16.little, name="FlBool16", enc=Bool16.little.enc)
FlBool32 = Field(base=Bool32.little, name="FlBool32", enc=Bool32.little.enc)

FlSInt16 = Field(base=SInt16.little, name="FlSInt16", enc=SInt16.little.enc)
FlSInt32 = Field(base=SInt32.little, name="FlSInt32", enc=SInt32.little.enc)

FlSEnum16 = Field(base=SEnum16.little, name="FlSEnum16", enc=SEnum16.little.enc)
FlSEnum32 = Field(base=SEnum32.little, name="FlSEnum32", enc=SEnum32.little.enc)

FlFloat = Field(base=Float.little, name="FlFloat", enc=Float.little.enc)

'''These Fields exist to easily identify where in a tag
that raw data refs, reflexives, and tag references exist.'''
RawdataRef  = Field(base=QuickStruct, name="RawdataRef")
Reflexive   = Field(base=QuickStruct, name="Reflexive")
TagIndexRef = Field(base=Struct, name="TagIndexRef")

#the Tag_Index is the array that stores all the tag string paths and
#meta datas in a map file. This Field exists so the Map_Magic
#can be easily supplied through the keyword argument "Map_Magic"
TagIndex = Field(base=Array, name="TagIndex",
                 reader=tag_index_reader, writer=tag_index_writer)

Rawdata = Field(base=BytearrayRaw, name="Rawdata", reader=rawdata_reader)

StrLatin1Enum = Field(base=StrRawLatin1, name="StrLatin1Enum",
                      is_enum=True, is_block=True, is_data=True, data_type=str,
                      py_type=EnumBlock, sanitizer=bool_enum_sanitizer)
