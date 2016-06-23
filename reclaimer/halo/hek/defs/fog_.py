from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

fog__body = Struct("tagdata",
    #fog flags
    BBool32("fog flags",
        "is water",
        "atmospheric dominant",
        "fog screen only",
        ),
                   
    Pad(84),
    #Density
    BFloat("maximum density"),
    Pad(4),
    BFloat("opaque distance"),
    Pad(4),
    BFloat("opaque depth"),
    Pad(8),
    BFloat("distance to water plane"),

    #Color
    Struct("fog color", INCLUDE=rgb_float),

    #Screen Layers
    BBool16("flags",
        "no environment multipass",
        "no model multipass",
        "no texture-based falloff",
        ),
    BUInt16("layer count"),

    Struct("distance gradient", INCLUDE=from_to),
    Struct("density gradient",  INCLUDE=from_to),

    BFloat("start distance from fog plane"),
    Pad(5),

    Struct("color", INCLUDE=rgb_byte),
    BFloat("rotation multiplier"),
    BFloat("strafing multiplier"),
    BFloat("zoom multiplier"),
    Pad(8),
    BFloat("map scale"),
    dependency("fog map"),

    #Screen Layer Animation
    BFloat("animation period"),
    Pad(4),
    Struct("wind velocity", INCLUDE=from_to),
    Struct("wind period",   INCLUDE=from_to),
    BFloat("wind acceleration weight"),
    BFloat("wind perpendicular weight"),

    Pad(8),
    #Sound
    dependency("background sound"),
    dependency("sound environment"),
    SIZE=396,
    )

def get():
    return fog__def

fog__def = TagDef(
    blam_header('fog '),
    fog__body,
    
    NAME="fog",
    
    ext=".fog", def_id="fog ", endian=">"
    )
