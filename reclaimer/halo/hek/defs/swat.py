from .shdr import *
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

swat_body = Struct("tagdata",
    shader_attrs,

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
    Struct("perpendicular tint color", INCLUDE=rgb_float),
    BFloat("parallel brightness"),#[0,1]
    Struct("parallel tint color",      INCLUDE=rgb_float),
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

swat_def = TagDef("swat",
    blam_header('swat', 2),
    swat_body,

    ext=".shader_transparent_water", endian=">"
    )
