from supyr_struct.fields import *


def sub_objects_size(newsize=None, *args, **kwargs):
    if newsize is not None:
        if newsize <= 1:
            kwargs["block"].PARENT.PARENT.Sub_Objects_Count = 0
        else:
            kwargs["block"].PARENT.PARENT.Sub_Objects_Count = newsize - 1
    else:
        block_count = kwargs["block"].PARENT.PARENT.Sub_Objects_Count - 1
        if block_count < 0:
            return 0
        return block_count


#NEED A PARSER SPECIFICALLY FOR THE GDL OBJECTS BLOCK.
#IF THE POINTER FOR THE SUB-OBJECTS DATA IS 0 THEN THE
#PRIMITIVES BLOCK DOESNT EXIST.

#ALSO NEED READER FOR PRIMITIVES BLOCK SINCE THE TYPE
#OF PRIMITIVE DETERMINES THE STRUCTURE.
