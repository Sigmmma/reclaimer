from supyr_struct.defs.tag_def import TagDef
from supyr_struct.defs.common_descriptors import *
from ..fields import *
from .objs.anim import AnimPs2Tag

def get(): return anim_ps2_def

anim_ps2_def = TagDef(
    TYPE=Container,
    NAME='gdl anim resource',

    ext=".ps2", def_id="anim",
    tag_cls=AnimPs2Tag, incomplete=True
    )
