from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return boom_def

boom_def = TagDef(
    blam_header('boom'),
    Struct('tagdata',
        #this is just a guess. This could just as easily
        #be 4 bytes of padding. effing useless tag type
        BFloat('radius')
        ),
    
    NAME="spheroid",
    
    ext=".spheroid", def_id="boom", endian=">"
    )
