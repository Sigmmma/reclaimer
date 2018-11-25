from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


chmt_lighting_variable = Struct("lighting_variables",
    Float("lightmap_brightness_offset"),
    ENDIAN=">", SIZE=4
    )


chmt_meta_def = BlockDef("chmt",
    reflexive("lighting_variables", chmt_lighting_variable),
    TYPE=Struct, ENDIAN=">", SIZE=12
    )