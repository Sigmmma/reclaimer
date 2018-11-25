from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


chad_position_animation = Struct("animation",
    SInt32("frame_number"),
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    ENDIAN=">", SIZE=16
    )


chad_position = Struct("position",
    reflexive("animation", chad_position_animation),
    rawdata_ref("function"),
    ENDIAN=">", SIZE=32
    )


chad_rotation_animation = Struct("animation",
    SInt32("frame_number"),
    float_rad("x_angle"),
    float_rad("y_angle"),
    float_rad("z_angle"),
    ENDIAN=">", SIZE=16
    )


chad_rotation = Struct("rotation",
    reflexive("animation", chad_rotation_animation),
    rawdata_ref("function"),
    ENDIAN=">", SIZE=32
    )


chad_size_animation = Struct("animation",
    SInt32("frame_number"),
    Float("stretch_x"),
    Float("stretch_y"),
    ENDIAN=">", SIZE=12
    )


chad_size = Struct("size",
    reflexive("animation", chad_size_animation),
    rawdata_ref("unknown"),
    ENDIAN=">", SIZE=32
    )


chad_color_animation = Struct("animation",
    SInt32("frame_number"),
    Pad(4),
    ENDIAN=">", SIZE=8
    )


chad_color = Struct("color",
    reflexive("animation", chad_color_animation),
    rawdata_ref("function"),
    ENDIAN=">", SIZE=32
    )


chad_alpha_animation = Struct("animation",
    SInt32("frame_number"),
    Float("alpha"),
    ENDIAN=">", SIZE=8
    )


chad_alpha = Struct("alpha",
    reflexive("animation", chad_alpha_animation),
    rawdata_ref("function"),
    ENDIAN=">", SIZE=32
    )


chad_alpha_unknown_animation = Struct("animation",
    SInt32("frame_number"),
    Float("alpha"),
    ENDIAN=">", SIZE=8
    )


chad_alpha_unknown = Struct("alpha_unknown",
    reflexive("animation", chad_alpha_unknown_animation),
    rawdata_ref("function"),
    ENDIAN=">", SIZE=32
    )


chad_bitmap_animation = Struct("animation",
    SInt32("frame_number"),
    Float("movement_1_x"),
    Float("movement_1_y"),
    Float("movement_2_x"),
    Float("movement_2_y"),
    ENDIAN=">", SIZE=20
    )


chad_bitmap = Struct("bitmap",
    reflexive("animation", chad_bitmap_animation),
    rawdata_ref("function"),
    ENDIAN=">", SIZE=32
    )


chad_meta_def = BlockDef("chad",
    Bool16("flags",
        ("loops", 1 << 1),
        ),
    SInt16("unknown"),
    reflexive("position", chad_position),
    reflexive("rotation", chad_rotation),
    reflexive("size", chad_size),
    reflexive("color", chad_color),
    reflexive("alpha", chad_alpha),
    reflexive("alpha_unknown", chad_alpha_unknown),
    reflexive("bitmap", chad_bitmap),
    SInt32("number_of_frames"),
    TYPE=Struct, ENDIAN=">", SIZE=92
    )