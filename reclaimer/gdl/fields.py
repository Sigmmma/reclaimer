from supyr_struct.fields import *


def sub_objects_size(block=None, parent=None, attr_index=None,
                     rawdata=None, new_value=None, *args, **kwargs):
    if new_value is not None:
        if new_value <= 1:
            block.PARENT.PARENT.Sub_Objects_Count = 0
        else:
            block.PARENT.PARENT.Sub_Objects_Count = new_value - 1
    else:
        block_count = block.PARENT.PARENT.Sub_Objects_Count - 1
        if block_count < 0:
            return 0
        return block_count


#NEED A PARSER SPECIFICALLY FOR THE GDL OBJECTS BLOCK.
#IF THE POINTER FOR THE SUB-OBJECTS DATA IS 0 THEN THE
#PRIMITIVES BLOCK DOESNT EXIST.

#ALSO NEED READER FOR PRIMITIVES BLOCK SINCE THE TYPE
#OF PRIMITIVE DETERMINES THE STRUCTURE.
