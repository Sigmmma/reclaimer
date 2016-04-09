from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

fog__body = Struct("Data",
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
    Struct("fog color", INCLUDE=R_G_B_Float),

    #Screen Layers
    BBool16("flags",
        "no environment multipass",
        "no model multipass",
        "no texture-based falloff",
        ),
    BUInt16("layer count"),

    Struct("distance gradient", INCLUDE=From_To),
    Struct("density gradient",  INCLUDE=From_To),

    BFloat("start distance from fog plane"),
    Pad(5),

    Struct("color", INCLUDE=R_G_B_Byte),
    BFloat("rotation multiplier"),
    BFloat("strafing multiplier"),
    BFloat("zoom multiplier"),
    Pad(8),
    BFloat("map scale"),
    TagIndexRef("fog map", INCLUDE=Tag_Index_Ref_Struct),

    #Screen Layer Animation
    BFloat("animation period"),
    Pad(4),
    Struct("wind velocity", INCLUDE=From_To),
    Struct("wind period",   INCLUDE=From_To),
    BFloat("wind acceleration weight"),
    BFloat("wind perpendicular weight"),

    Pad(8),
    #Sound
    TagIndexRef("background sound",  INCLUDE=Tag_Index_Ref_Struct),
    TagIndexRef("sound environment", INCLUDE=Tag_Index_Ref_Struct),
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
