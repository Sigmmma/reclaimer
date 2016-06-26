from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

pphy_body = Struct("tagdata",
    BBool32("flags",
        "flamethrower particle collision",
        "collides with structures",
        "collides with water surface",
        "uses simple wind",
        "uses damped wind",
        "no gravity"
        ),
    #these next three are courtesy of Sparky. I had
    #no idea these existed till I looked in Eschaton
    FlFloat("wind coefficient"),
    FlFloat("wind sine modifier"),
    FlFloat("z translation rate"),
    Pad(16),
    BFloat("density"),#g/mL
    BFloat("air friction"),
    BFloat("water friction"),
    BFloat("surface friction"),
    BFloat("elasticity"),

    SIZE=64
    )

def get():
    return pphy_def

pphy_def = TagDef("pphy",
    blam_header('pphy'),
    pphy_body,

    ext=".point_physics", endian=">"
    )
