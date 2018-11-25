from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


rasg_default_bitmap = Struct("default_bitmaps",
    SInt32("unknown"),
    dependency("bitmap"),
    ENDIAN=">", SIZE=20
    )


rasg_default_rasterizer_bitmap = Struct("default_rasterizer_bitmaps",
    dependency("bitmap"),
    ENDIAN=">", SIZE=16
    )


rasg_default_shader = Struct("default_shaders",
    dependency("vertex_shader"),
    dependency("pixel_shader"),
    ENDIAN=">", SIZE=32
    )


rasg_meta_def = BlockDef("rasg",
    reflexive("default_bitmaps", rasg_default_bitmap),
    reflexive("default_rasterizer_bitmaps", rasg_default_rasterizer_bitmap),
    dependency("vertex_shader_simple"),
    dependency("pixel_shader_simple"),
    reflexive("default_shaders", rasg_default_shader),
    Pad(12),
    SInt32("unknown_1"),
    SInt32("unknown_2"),
    dependency("active_camo_distortion"),
    dependency("default_performance_template"),
    dependency("default_shield_impact"),
    SInt32("unknown_3"),
    Pad(24),
    TYPE=Struct, ENDIAN=">", SIZE=164
    )