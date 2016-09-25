from supyr_struct.field_types import *
from supyr_struct.editor.constants import *


def sub_objects_size(node=None, parent=None, attr_index=None,
                     rawdata=None, new_value=None, *args, **kwargs):
    if new_value is not None:
        if new_value <= 1:
            node.parent.parent.sub_objects_count = 0
        else:
            node.parent.parent.sub_objects_count = new_value - 1
    else:
        node_count = node.parent.parent.sub_objects_count - 1
        if node_count < 0:
            return 0
        return node_count


def qword_size(node=None, parent=None, attr_index=None,
               rawdata=None, new_value=None, *args, **kwargs):
    if node and parent is None:
        parent = node.parent
    if new_value is not None:
        parent.qword_count = (new_value-8)//16
    return parent.qword_count*16+8


def lump_array_reader(self, desc, node=None, parent=None, attr_index=None,
                      rawdata=None, root_offset=0, offset=0, **kwargs):
    if node is None:
        node = (desc.get(BLOCK_CLS, self.py_type)
                     (desc, parent=parent, init_attrs=rawdata is None))
        parent[attr_index] = node
        
    b_desc  = desc['SUB_STRUCT']
    b_f_type = b_desc['TYPE']

    if attr_index is not None and desc.get('POINTER') is not None:
        offset = node.get_meta('POINTER', **kwargs)

    list.__delitem__(node, slice(None, None, None))
    kwargs.update(root_offset=root_offset, parent=node, rawdata=rawdata)

    for i in range(node.get_size()):
        #need to append a new entry to the block
        list.append(node, None)
        offset = b_f_type.reader(b_desc, attr_index=i, offset=offset, **kwargs)

    return offset


Lump = FieldType(base=Array, name='Lump', reader=lump_array_reader)
