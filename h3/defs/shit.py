from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


shit_meta_def = BlockDef("shit",
    dependency("unknown"),
    dependency("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    Float("unknown_4"),
    Float("unknown_5"),
    Float("unknown_6"),
    Float("unknown_7"),
    Float("unknown_8"),
    Float("unknown_9"),
    Float("unknown_10"),
    color_rgb_float("color"),
    Float("unknown_11"),
    color_rgb_float("color_1"),
    Float("unknown_12"),
    color_rgb_float("color_2"),
    Float("unknown_13"),
    color_rgb_float("color_3"),
    Float("unknown_14"),
    color_rgb_float("color_4"),
    Float("unknown_15"),
    color_rgb_float("color_5"),
    Float("unknown_16"),
    TYPE=Struct, ENDIAN=">", SIZE=164
    )