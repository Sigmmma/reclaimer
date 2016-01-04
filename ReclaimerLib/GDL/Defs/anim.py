from supyr_struct.Defs.Tag_Def import Tag_Def
from supyr_struct.Defs.Common_Structures import *
from ..Field_Types import *
from .Objs.anim import Anim_PS2_Tag

def Construct():
    return ANIM_PS2_Definition

class ANIM_PS2_Definition(Tag_Def):
    
    Ext = ".ps2"

    Cls_ID = "anim.ps2"

    #The constructor used to build this definitions Tag_Obj
    Tag_Obj = Anim_PS2_Tag

    Endian = "<"

    Incomplete = True

    Tag_Structure = { TYPE:Container, NAME:'GDL_Anim_Resource' }
