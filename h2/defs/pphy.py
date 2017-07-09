from ..common_descs import *
from .objs.tag import H2Tag
from supyr_struct.defs.tag_def import TagDef

pphy_body = Struct("tagdata",
    Bool32("flags",
        "flamethrower particle collision",
        "collides with structures",
        "collides with water surface",
        "uses simple wind",
        "uses damped wind",
        "no gravity"
        ),
    #these next three are courtesy of Sparky. I had
    #no idea these existed till I looked in Eschaton
    Float("wind coefficient", VISIBLE=False),
    Float("wind sine modifier", VISIBLE=False),
    Float("z translation rate", VISIBLE=False),
    Pad(16),
    Float("density", SIDETIP="g/mL"),#g/mL
    Float("air friction"),
    Float("water friction"),
    Float("surface friction"),
    Float("elasticity"),
    SIZE=64
    )

def get():
    return pphy_def

pphy_def = TagDef("pphy",
    h2_blam_header('pphy'),
    pphy_body,

    ext=".point_physics", endian="<", tag_cls=H2Tag
    )
