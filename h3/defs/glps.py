from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


glps_unknown_unknown_unknown_1 = Struct("unknown_1",
    UInt32("unknown"),
    ENDIAN=">", SIZE=4
    )


glps_unknown_unknown = Struct("unknown",
    UInt32("unknown"),
    reflexive("unknown_1", glps_unknown_unknown_unknown_1),
    ENDIAN=">", SIZE=16
    )


glps_unknown = Struct("unknown",
    reflexive("unknown", glps_unknown_unknown),
    Pad(4),
    ENDIAN=">", SIZE=16
    )


glps_pixel_shader_unknown_2 = Struct("unknown_2",
    string_id_meta("unknown"),
    Pad(4),
    ENDIAN=">", SIZE=8
    )


glps_pixel_shader = Struct("pixel_shaders",
    rawdata_ref("unknown"),
    rawdata_ref("unknown_1"),
    reflexive("unknown_2", glps_pixel_shader_unknown_2),
    Pad(24),
    UInt32("pixel_shader"),
    ENDIAN=">", SIZE=80
    )


glps_meta_def = BlockDef("glps",
    reflexive("unknown", glps_unknown),
    Pad(4),
    reflexive("pixel_shaders", glps_pixel_shader),
    TYPE=Struct, ENDIAN=">", SIZE=28
    )