from supyr_struct.Defs.Tag_Def import Tag_Def
from supyr_struct.Defs.Common_Structures import *
from ...Tag_Constructors.GDL_Constructors.Field_Types import *
from .Objs.anim import Anim_PS2_Tag

def Construct():
    return ANIM_PS2_Definition

class ANIM_PS2_Definition(Tag_Def):
    
    Tag_Ext = ".ps2"

    Tag_ID = "anim.ps2"

    #The constructor used to build this definitions Tag_Obj
    Tag_Obj = Anim_PS2_Tag

    Endianness = "<"

    Incomplete = True

    Tag_Structure = { TYPE:Container, GUI_NAME:'GDL Animations Resource',
                      SIZE:0, ENTRIES:0, POINTER:0 }
