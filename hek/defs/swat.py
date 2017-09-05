from math import pi

from .shdr import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

ripple = Struct("ripple",
    Pad(4),
    float_zero_to_one("contribution factor"),
    Pad(32),
    Float("animation angle",
        MIN=0.0, MAX=2*pi, UNIT_SCALE=180/pi, SIDETIP="[0,360]"),  # radians
    Float("animation velocity", UNIT_SCALE=per_sec_unit_scale),
    Struct("map offset", INCLUDE=ij_float),
    UInt16("map repeats"),
    UInt16("map index"),
    SIZE=76
    )


swat_attrs = Struct("swat attrs",
    #Water Shader Properties
    Struct("water shader",
        Bool16("flags",
            "base map alpha modulates reflection",
            "base map color modulates background",
            "atmospheric fog",
            "draw before fog",
            ),
        Pad(34),
        dependency("base map", "bitm"),
        Pad(16),
        float_zero_to_one("perpendicular brightness"),
        Struct("perpendicular tint color", INCLUDE=rgb_float),
        float_zero_to_one("parallel brightness"),
        Struct("parallel tint color", INCLUDE=rgb_float),
        Pad(16),
        dependency("reflection map", "bitm"),

        Pad(16),
        Float("ripple animation angle",
            MIN=0.0, MAX=2*pi, UNIT_SCALE=180/pi, SIDETIP="[0,360]"),  # radians
        Float("ripple animation velocity", UNIT_SCALE=per_sec_unit_scale),
        Float("ripple scale"),
        dependency("ripple maps", "bitm"),
        UInt16("ripple mipmap levels"),
        Pad(2),
        float_zero_to_one("ripple mipmap fade factor"),
        Float("ripple mipmap detail bias"),
        ),

    Pad(64),
    reflexive("ripples", ripple, 4),
    SIZE=280
    )

swat_body = Struct("tagdata",
    shdr_attrs,
    swat_attrs,
    SIZE=320,
    )

def get():
    return swat_def

swat_def = TagDef("swat",
    blam_header('swat', 2),
    swat_body,

    ext=".shader_transparent_water", endian=">", tag_cls=HekTag
    )
