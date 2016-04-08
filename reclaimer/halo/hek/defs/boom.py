from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return boom_def

boom_def = TagDef(
    com( {1:{DEFAULT:"boom" }}, Tag_Header),
    Struct('Data',
        #this is just a guess. This could just as easily
        #be 4 bytes of padding. effing useless tag type
        BFloat('radius')
        ),
    
    NAME="spheroid",
    
    ext=".spheroid", def_id="boom", endian=">"
    )
