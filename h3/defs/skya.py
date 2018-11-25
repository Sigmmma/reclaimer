from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


skya_atmosphere_propertie = Struct("atmosphere_properties",
    SInt16("unknown"),
    SInt16("unknown_1"),
    string_id_meta("name"),
    Float("light_source_y"),
    Float("light_source_x"),
    color_rgb_float("fog_color"),
    Float("brightness"),
    Float("fog_gradient_threshold"),
    Float("light_intensity"),
    Float("sky_invisiblility_through_fog"),
    Float("unknown_2"),
    Float("unknown_3"),
    Float("light_source_spread"),
    Pad(4),
    Float("fog_intensity"),
    Float("unknown_5"),
    Float("tint_cyan"),
    Float("tint_magenta"),
    Float("tint_yellow"),
    Float("fog_intensity_cyan"),
    Float("fog_intensity_magenta"),
    Float("fog_intensity_yellow"),
    Float("background_color_red"),
    Float("background_color_green"),
    Float("background_color_blue"),
    Float("tint_red"),
    Float("tint2_green"),
    Float("tint2_blue"),
    Float("fog_intensity2"),
    Float("start_distance"),
    Float("end_distance"),
    Float("fog_velocity_x"),
    Float("fog_velocity_y"),
    Float("fog_velocity_z"),
    dependency("weather_effect"),
    Pad(8),
    ENDIAN=">", SIZE=164
    )


skya_underwater = Struct("underwater",
    string_id_meta("name"),
    color_argb_float("color"),
    ENDIAN=">", SIZE=20
    )


skya_meta_def = BlockDef("skya",
    Pad(4),
    dependency("fog_bitmap"),
    Float("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    Float("unknown_4"),
    Float("unknown_5"),
    Float("unknown_6"),
    Float("unknown_7"),
    Pad(4),
    reflexive("atmosphere_properties", skya_atmosphere_propertie),
    reflexive("underwater", skya_underwater),
    TYPE=Struct, ENDIAN=">", SIZE=76
    )