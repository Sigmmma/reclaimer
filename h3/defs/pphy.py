from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


pphy_meta_def = BlockDef("pphy",
    Bool32("flags",
        ),
    Float("unknown"),
    Float("unknown_1"),
    Float("unknown_2"),
    Pad(16),
    Float("density"),
    Float("air_friction"),
    Float("water_friction"),
    Float("surface_friction"),
    Float("elasticity"),
    Pad(12),
    TYPE=Struct, ENDIAN=">", SIZE=64
    )