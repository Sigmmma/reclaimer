from supyr_struct.defs.tag_def import TagDef
from supyr_struct.defs.common_descriptors import *
from ..fields import *
from .objs.anim import AnimPs2Tag

def get():
    return AnimPs2Def

class AnimPs2Def(TagDef):
    
    ext = ".ps2"

    tag_id = "anim.ps2"

    #The constructor used to build this definitions tag_obj
    tag_cls = AnimPs2Tag

    endian = "<"

    incomplete = True

    descriptor = { TYPE:Container, NAME:'GDL_Anim_Resource' }
