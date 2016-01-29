from struct import unpack

from supyr_struct.fields import *
from supyr_struct.blocks import *
from .field_methods import *


tmp = {'str':True, 'default':'', 'delimited':True,
       'reader':data_reader, 'writer':data_writer,
       'decoder':decode_raw_string, 'encoder':encode_string}
com = combine

'''These are varients of the standard Fields that have been
slightly modified based on how Halo needs to utilize them.'''
StringVarLen = Field(**com({'name':"HaloRefStr", 'size':1, 
                            'decoder':decode_string, 'enc':'latin-1',
                            'encoder':encode_tag_ref_str,
                            'sizecalc':tag_ref_sizecalc}, tmp))

FlUTF16StrData = Field(**com({'name':"UTF16StrData", 'size':2,
                              'sizecalc':utf_sizecalc, 'enc':"utf_16_le"},tmp))
FlStrUTF16 = Field(**com({'name':"StrUTF16", 'size':2, 'decoder':decode_string,
                          'sizecalc':delim_utf_sizecalc,'enc':"utf_16_le"},tmp))

tmp = {'data':True, 'sizecalc':def_sizecalc,
       'size':2, 'min':0, 'max':2**16-1, 'enc':"<H", "endian":'<',
       'reader':f_s_data_reader, 'writer':data_writer,
       'decoder':decode_numeric, 'encoder':encode_numeric}

FlUInt16 = Field(**com({"name":"FlUInt16", 'default':0 }, tmp))
FlEnum16 = Field(**com({"name":"FlEnum16", 'enum':True,
                        'py_type':EnumBlock, 'data_type':int}, tmp))
FlBool16 = Field(**com({"name":"FlBool16", 'bool':True,
                        'py_type':BoolBlock, 'data_type':int}, tmp))

tmp['size'], tmp['max'], tmp['enc'] = 4, 2**32-1, "<I"
FlUInt32 = Field(**com({"name":"FlUInt32", 'default':0 }, tmp))
FlEnum32 = Field(**com({"name":"FlEnum32", 'enum':True,
                        'py_type':EnumBlock, 'data_type':int}, tmp))
FlBool32 = Field(**com({"name":"FlBool32", 'bool':True,
                        'py_type':BoolBlock, 'data_type':int}, tmp))

tmp["default"] = 0
FlSInt16 = Field(**com({"name":"FlSInt16", "size":2, "enc":"<h",
                        'min':-32768, 'max':32767 }, tmp))
FlSInt32 = Field(**com({"name":"FlSInt32", "size":4, "enc":"<i",
                        'min':-2147483648, 'max':2147483647 }, tmp))

tmp["default"] = 0.0
FlFloat = Field(**com({"name":"FlFloat", "size":4, "enc":"<f",
                       "max":unpack('>f',b'\x7f\x7f\xff\xff'),
                       "min":unpack('>f',b'\xff\x7f\xff\xff') }, tmp))

'''These Fields exist to easily identify where in a tag
that raw data refs, reflexives, and tag references exist.'''
RawDataRef = Field(name="RawDataRef", struct=True,
                   endian='=', py_type=ListBlock,
                   reader=struct_reader, writer=struct_writer)

Reflexive = Field(name="Reflexive", struct=True, endian='=',
                  py_type=ListBlock,
                  reader=struct_reader, writer=struct_writer)

TagIndexRef = Field(name="TagIndexRef", struct=True, endian='=',
                    py_type=ListBlock,
                    reader=struct_reader, writer=struct_writer)

#the Tag_Index is the array that stores all the tag string paths and
#meta datas in a map file. This Field exists so the Map_Magic
#can be easily supplied through the keyword argument "Map_Magic"
TagIndex = Field(name="TagIndex", array=True, endian='=',
                 py_type=ListBlock,
                 reader=tag_index_reader, writer=tag_index_writer)
