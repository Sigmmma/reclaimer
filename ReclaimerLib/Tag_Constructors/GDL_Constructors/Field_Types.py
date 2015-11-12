from supyr_struct.Field_Types import *


def Sub_Objects_Size(New_Size=None, *args, **kwargs):
    if New_Size is not None:
        if New_Size <= 1:
            kwargs["Block"].PARENT.PARENT.Sub_Objects_Count = 0
        else:
            kwargs["Block"].PARENT.PARENT.Sub_Objects_Count = New_Size - 1
    else:
        Block_Count = kwargs["Block"].PARENT.PARENT.Sub_Objects_Count - 1
        if Block_Count < 0:
            return 0
        return Block_Count


#NEED A PARSER SPECIFICALLY FOR THE GDL OBJECTS BLOCK.
#IF THE POINTER FOR THE SUB-OBJECTS DATA IS 0 THEN THE
#PRIMITIVES BLOCK DOESNT EXIST.

#ALSO NEED READER FOR PRIMITIVES BLOCK SINCE THE TYPE
#OF PRIMITIVE DETERMINES THE STRUCTURE.
