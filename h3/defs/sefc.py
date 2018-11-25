from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


sefc_screen_effect = Struct("screen_effect",
    string_id_meta("name"),
    SInt16("unknown"),
    SInt16("unknown_1"),
    Float("unknown_2"),
    rawdata_ref("function"),
    Float("duration"),
    rawdata_ref("function_1"),
    rawdata_ref("function_2"),
    Float("light_intensity"),
    Pad(8),
    Float("saturation"),
    Float("color_muting"),
    Float("brightness"),
    Float("darkness"),
    Float("shadow_brightness"),
    color_rgb_float("tint"),
    color_rgb_float("tone"),
    ENDIAN=">", SIZE=132
    )


sefc_meta_def = BlockDef("sefc",
    reflexive("screen_effect", sefc_screen_effect),
    TYPE=Struct, ENDIAN=">", SIZE=12
    )