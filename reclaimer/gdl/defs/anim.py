from supyr_struct.defs.tag_def import TagDef
from supyr_struct.defs.common_descriptors import *
from ..fields import *
from .objs.anim import AnimPs2Tag

def get():
    return AnimPs2Def

AnimPs2Def = TagDef( NAME='GDL_Anim_Resource',
                     
                     ext=".ps2", def_id="anim",
                     tag_cls=AnimPs2Tag, incomplete=True
                     )
