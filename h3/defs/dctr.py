from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


dctr_meta_def = BlockDef("dctr",
    dependency("model"),
    Pad(12),
    SInt32("unknown_1"),
    dependency("texture"),
    SInt16("affects_visibility"),
    SInt16("unknown_2"),
    color_rgb_float("color"),
    Pad(20),
    Float("brightness_base"),
    Float("brightness_shadow"),
    Pad(36),
    TYPE=Struct, ENDIAN=">", SIZE=128
    )