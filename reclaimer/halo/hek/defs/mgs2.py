from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

frame = Struct("frame",
    Pad(16),
    BFloat("offset from marker"),
    BFloat("offset exponent"),
    BFloat("length"),

    Pad(32),
    BFloat("radius hither"),
    BFloat("radius yon"),
    BFloat("radius exponent"),

    Pad(32),
    QStruct("tint color hither", INCLUDE=argb_float),
    QStruct("tint color yon", INCLUDE=argb_float),
    BFloat("tint color exponent"),
    BFloat("brightness exponent"),
    SIZE=176
    )

mgs2_body = Struct("tagdata",
    #Light volume
    ascii_str32("attachment marker"),
    BBool32("flags",
        "interpolate color in hsv",
        "more colors"
        ),
    Pad(16),

    #Brightness scale
    BFloat("near fade distance"),
    BFloat("far fade distance"),
    BFloat("perpendicular brightness scale"),
    BFloat("parallel brightness scale"),
    BSEnum16("brightness scale source", *function_outputs),
    Pad(22),

    #Bitmaps
    dependency("map", valid_bitmaps),
    BSInt16("sequence index"),
    BSInt16("count"),
    Pad(72),

    #Frame animation
    BSEnum16("frame animation source", *function_outputs),
    Pad(102),

    reflexive("frames", frame, 2),

    SIZE=332,
    )

    
def get():
    return mgs2_def

mgs2_def = TagDef("mgs2",
    blam_header("mgs2"),
    mgs2_body,

    ext=".light_volume", endian=">",
    )
