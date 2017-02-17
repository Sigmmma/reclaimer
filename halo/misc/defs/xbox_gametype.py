'''
    This varient of the gametype tag is intended to allow easily creating a
    gametype from within Mozzarilla by just selecting the xbox_gametype def
'''

from .pc_gametype import *
from .objs.xbox_gametype import *

def get():
    return xbox_gametype_def

xbox_gametype_def = TagDef('xbox_gametype',
    xbox_gametype_header,
    settings,
    xbox_gametype_footer,

    ext='.lst', endian='<', tag_cls=XboxGametypeTag,
    )
