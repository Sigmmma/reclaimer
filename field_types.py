from struct import unpack

from supyr_struct.field_types import *
from supyr_struct.blocks import *
from .field_type_methods import *
from .constants import *


'''These are varients of the standard FieldTypes that have been
slightly modified based on how Halo needs to utilize them.'''
StrTagRef = FieldType(
    base=StrLatin1, name="StrTagRef",
    parser=tag_ref_str_parser, serializer=tag_ref_str_serializer,
    encoder=encode_tag_ref_str, sizecalc=tag_ref_str_sizecalc)
FlStrUTF16Data = FieldType(
    base=StrUtf16, name="StrUTF16Data",
    enc={">": StrUtf16.little.enc, "<": StrUtf16.little.enc},
    decoder=decode_raw_string, sizecalc=utf_sizecalc)
FlStrUTF16 = FieldType(
    base=StrUtf16, name="StrUTF16",
    enc={">": StrUtf16.little.enc, "<": StrUtf16.little.enc},
    decoder=decode_string, sizecalc=delim_utf_sizecalc)

#forces little endian integers and float
FlUInt16 = FieldType(
    base=UInt16.little, name="FlUInt16", enc=UInt16.little.enc)
FlUInt32 = FieldType(
    base=UInt32.little, name="FlUInt32", enc=UInt32.little.enc)

FlUEnum16 = FieldType(
    base=UEnum16.little, name="FlUEnum16", enc=UEnum16.little.enc)
FlUEnum32 = FieldType(
    base=UEnum32.little, name="FlUEnum32", enc=UEnum32.little.enc)

FlBool16 = FieldType(
    base=Bool16.little, name="FlBool16", enc=Bool16.little.enc)
FlBool32 = FieldType(
    base=Bool32.little, name="FlBool32", enc=Bool32.little.enc)

FlSInt16 = FieldType(
    base=SInt16.little, name="FlSInt16", enc=SInt16.little.enc)
FlSInt32 = FieldType(
    base=SInt32.little, name="FlSInt32", enc=SInt32.little.enc)

FlSEnum16 = FieldType(
    base=SEnum16.little, name="FlSEnum16", enc=SEnum16.little.enc)
FlSEnum32 = FieldType(
    base=SEnum32.little, name="FlSEnum32", enc=SEnum32.little.enc)

FlFloat = FieldType(base=Float.little, name="FlFloat", enc=Float.little.enc)

'''These FieldTypes exist to easily identify where in a tag
that raw data refs, reflexives, and tag references exist.'''
RawdataRef   = FieldType(base=Struct,  name="RawdataRef", parser=rawdata_ref_parser)
Reflexive    = FieldType(base=QStruct, name="Reflexive", parser=reflexive_parser)
RawReflexive = FieldType(base=Reflexive, name="RawReflexive")
TagRef       = FieldType(base=Struct, name="TagRef")

ZoneAsset = FieldType(base=QStruct, name="ZoneAsset")
StringID  = FieldType(base=QStruct, name="StringID")
TagIndex  = FieldType(base=Array, name="TagIndex")

StrLatin1Enum = FieldType(base=StrRawLatin1, name="StrLatin1Enum",
                          is_block=True, is_data=True, data_cls=str,
                          sizecalc=sizecalc_wrapper(len_sizecalc),
                          decoder=decoder_wrapper(decode_string),
                          encoder=encoder_wrapper(encode_string),
                          node_cls=EnumBlock, sanitizer=enum_sanitizer)
