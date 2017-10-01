from ..common_descs import *
from supyr_struct.defs.block_def import BlockDef

pphy_meta_def = BlockDef("pphy",
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
    ENDIAN="<", TYPE=Struct,
    )
