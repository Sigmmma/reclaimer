from supyr_struct.fields import *


def sub_objects_size(block=None, parent=None, attr_index=None,
                     rawdata=None, new_value=None, *args, **kwargs):
    if new_value is not None:
        if new_value <= 1:
            block.parent.parent.sub_objects_count = 0
        else:
            block.parent.parent.sub_objects_count = new_value - 1
    else:
        block_count = block.parent.parent.sub_objects_count - 1
        if block_count < 0:
            return 0
        return block_count


def qword_size(block=None, parent=None, attr_index=None,
               rawdata=None, new_value=None, *args, **kwargs):
    if block and parent is None:
        parent = block.parent
    if new_value is not None:
        parent.qword_count = (new_value-8)//16
    return parent.qword_count*16+8


def lump_array_reader(self, desc, parent=None, rawdata=None, attr_index=None,
                      root_offset=0, offset=0, **kwargs):
    if attr_index is None and parent is not None:
        new_block = parent
    else:
        new_block = desc.get('DEFAULT',self.py_type)(desc, parent=parent,
                                                    init_attrs=rawdata is None)
        parent[attr_index] = new_block
        
    b_desc  = desc['SUB_STRUCT']
    b_field = b_desc['TYPE']
    
    if attr_index is not None and desc.get('POINTER') is not None:
        offset = new_block.get_meta('POINTER', **kwargs)
        
    list.__delitem__(new_block, slice(None, None, None))
    for i in range(new_block.get_size()):
        #need to append a new entry to the block
        list.append(new_block, None)
        offset = b_field.reader(b_desc, new_block, rawdata, i,
                                root_offset, offset,**kwargs)

    return offset


Lump = Field(base=Array, name='Lump', reader=lump_array_reader)
