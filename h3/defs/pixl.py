from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


pixl_unknown_1 = Struct("unknown_1",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


pixl_pixel_shader_unknown_2 = Struct("unknown_2",
    string_id_meta("unknown"),
    Pad(4),
    ENDIAN=">", SIZE=8
    )


pixl_pixel_shader = Struct("pixel_shaders",
    rawdata_ref("unknown"),
    rawdata_ref("unknown_1"),
    reflexive("unknown_2", pixl_pixel_shader_unknown_2),
    Pad(20),
    SInt32("unknown_4"),
    UInt32("pixel_shader"),
    ENDIAN=">", SIZE=80
    )


pixl_meta_def = BlockDef("pixl",
    Pad(4),
    reflexive("unknown_1", pixl_unknown_1),
    Pad(4),
    reflexive("pixel_shaders", pixl_pixel_shader),
    TYPE=Struct, ENDIAN=">", SIZE=32
    )