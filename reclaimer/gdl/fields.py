from supyr_struct.fields import *
from supyr_struct.editor.constants import *


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


def lump_array_reader(self, desc, block=None, parent=None, attr_index=None,
                      rawdata=None, root_offset=0, offset=0, **kwargs):
    if block is None:
        block = (desc.get(BLOCK_CLS, self.py_type)
                     (desc, parent=parent, init_attrs=rawdata is None))
        parent[attr_index] = block
        
    b_desc  = desc['SUB_STRUCT']
    b_field = b_desc['TYPE']

    if attr_index is not None and desc.get('POINTER') is not None:
        offset = block.get_meta('POINTER', **kwargs)

    list.__delitem__(block, slice(None, None, None))
    kwargs.update(root_offset=root_offset, parent=block, rawdata=rawdata)

    for i in range(block.get_size()):
        #need to append a new entry to the block
        list.append(block, None)
        offset = b_field.reader(b_desc, attr_index=i, offset=offset, **kwargs)

    return offset


Lump = Field(base=Array, name='Lump', reader=lump_array_reader)
