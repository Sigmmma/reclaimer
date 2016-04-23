from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

ripple = Struct("ripple",
    Pad(4),
    BFloat("contribution factor"),
    Pad(32),
    BFloat("animation angle"),
    BFloat("animation velocity"),
    Struct("map offset",
        BFloat("i"),
        BFloat("j"),
        ),
    BUInt16("map repeats"),
    BUInt16("map index"),
    SIZE=76
    )

swat_body = Struct("Data",
    #Radiosity Properties
    Radiosity_Block,

    #Shader Type
    Material_Type,
    Numeric_Shader_ID,

    Pad(2),
    #Water Shader Properties
    BBool16("flags",
        "base map alpha modulates reflection",
        "base map color modulates background",
        "atmospheric fog",
        "draw before fog",
        ),
    Pad(34),
    dependency("base map", valid_bitmaps),
    Pad(16),
    BFloat("perpendicular brightness"),#[0,1]
    Struct("perpendicular tint color", INCLUDE=R_G_B_Float),
    BFloat("parallel brightness"),#[0,1]
    Struct("parallel tint color",      INCLUDE=R_G_B_Float),
    Pad(16),
    dependency("reflection map", valid_bitmaps),

    Pad(16),
    BFloat("ripple animation angle"),
    BFloat("ripple animation velocity"),
    BFloat("ripple scale"),
    dependency("ripple maps", valid_bitmaps),
    BUInt16("ripple mipmap levels"),
    Pad(2),
    BFloat("ripple mipmap fade factor"),
    BFloat("ripple mipmap detail bias"),

    Pad(64),
    reflexive("ripples", ripple, 4),
    SIZE=320,
    )

def get():
    return swat_def

swat_def = TagDef(
    blam_header('swat', 2),
    swat_body,
    
    NAME="shader_transparent_water",
    
    ext=".shader_transparent_water", def_id="swat", endian=">"
    )
