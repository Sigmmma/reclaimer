from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

density_comment = """Densities(grams per milliliter)\n
air        0.0011
snow       0.128
cork       0.24
cedar      0.43
oak        0.866
ice        0.897
water      1.0
soil       1.1
cotton     1.491
dry earth  1.52
sand       1.7
granite    2.4
glass      2.5
iron       7.65
steel      7.77
lead       11.37
uranium    18.74
gold       19.3"""

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
    FlFloat("wind coefficient", VISIBLE=False),
    FlFloat("wind sine modifier", VISIBLE=False),
    FlFloat("z translation rate", VISIBLE=False),
    Pad(16),
    Float("density", SIDETIP="g/mL", COMMENT=density_comment),#g/mL
    Float("air friction"),
    Float("water friction"),
    Float("surface friction"),
    Float("elasticity"),

    SIZE=64
    )

def get():
    return pphy_def

pphy_def = TagDef("pphy",
    blam_header('pphy'),
    pphy_body,

    ext=".point_physics", endian=">", tag_cls=HekTag
    )
