from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

fog__body = Struct("tagdata",
    #fog flags
    BBool32("flags",
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
    QStruct("fog color", INCLUDE=rgb_float),

    #Screen Layers
    Struct("screen layers",
        BBool16("flags",
            "no environment multipass",
            "no model multipass",
            "no texture-based falloff",
            ),
        BUInt16("layer count"),

        QStruct("distance gradient", INCLUDE=from_to),
        QStruct("density gradient",  INCLUDE=from_to),

        BFloat("start distance from fog plane"),
        Pad(5),

        QStruct("color", INCLUDE=rgb_byte),
        BFloat("rotation multiplier"),
        BFloat("strafing multiplier"),
        BFloat("zoom multiplier"),
        Pad(8),
        BFloat("map scale"),
        dependency("fog map", "bitm")
        ),

    #Screen Layer Animation
    Struct("screen layer animation",
        BFloat("animation period"),
        Pad(4),
        QStruct("wind velocity", INCLUDE=from_to),
        QStruct("wind period",   INCLUDE=from_to),
        BFloat("wind acceleration weight"),
        BFloat("wind perpendicular weight")
        ),

    Pad(8),
    #Sound
    dependency("background sound", "lsnd"),
    dependency("sound environment", "snde"),
    SIZE=396,
    )

def get():
    return fog__def

fog__def = TagDef("fog ",
    blam_header('fog '),
    fog__body,
    
    ext=".fog", endian=">"
    )
