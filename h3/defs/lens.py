from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


lens_reflection = Struct("reflections",
    Bool16("flags",
        "align_rotation_with_screen_center",
        "radius_not_scaled_by_distance",
        "radius_scaled_by_occlusion_factor",
        "occluded_by_solid_objects",
        "ignore_light_color",
        "not_affected_by_inner_occlusion",
        ),
    SInt16("bitmap_index"),
    Float("position_along_flare_axis"),
    Float("rotation_offset"),
    Float("radius_min"),
    Float("radius_max"),
    Float("brightness_min"),
    Float("brightness_max"),
    Float("tint_modulation_factor"),
    Float("tint_color_r"),
    Float("tint_color_g"),
    Float("tint_color_b"),
    Float("unknown"),
    ENDIAN=">", SIZE=48
    )


lens_brightnes = Struct("brightness",
    rawdata_ref("function"),
    ENDIAN=">", SIZE=20
    )


lens_color = Struct("color",
    rawdata_ref("function"),
    ENDIAN=">", SIZE=20
    )


lens_unknown_9 = Struct("unknown_9",
    Pad(16),
    rawdata_ref("function"),
    ENDIAN=">", SIZE=36
    )


lens_rotation = Struct("rotation",
    Pad(16),
    rawdata_ref("function"),
    ENDIAN=">", SIZE=36
    )


lens_meta_def = BlockDef("lens",
    float_rad("falloff_angle"),
    float_rad("cutoff_angle"),
    Float("occlusion_radius"),
    SInt32("unknown"),
    Pad(8),
    Float("near_fade_distance"),
    Float("far_fade_distance"),
    dependency("bitmap"),
    SInt16("unknown_2"),
    SInt16("unknown_3"),
    SInt16("unknown_4"),
    SInt16("unknown_5"),
    float_rad("rotation_function_scale"),
    SInt16("unknown_6"),
    SInt16("unknown_7"),
    reflexive("reflections", lens_reflection),
    Pad(4),
    reflexive("brightness", lens_brightnes),
    reflexive("color", lens_color),
    reflexive("unknown_9", lens_unknown_9),
    reflexive("rotation", lens_rotation),
    Pad(24),
    TYPE=Struct, ENDIAN=">", SIZE=152
    )