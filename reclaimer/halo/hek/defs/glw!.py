from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

velocity_properties = Struct("velocity properties",
    BSEnum16("attachment", *function_outputs),
    Pad(2),
    BFloat("velocity"),
    BFloat("low multiplier"),
    BFloat("high multiplier")
    )

glw__body = Struct("tagdata",
    ascii_str32("attachment marker"),
    BSInt16("number of particles"),
    BSEnum16("boundary effect",
        "bounce",
        "wrap",
        ),
    BSEnum16("normal particle distribution",
        "random",
        "uniform",
        ),
    BSEnum16("trailing particle distribution",
        "vertically",
        "normal",
        "randomly"
        ),
    BBool32("glow flags" ,
        "modify particle color in range",
        "particles move backwards",
        "particles move in both directions",
        "trailing particles fade over time",
        "trailing particles shrink over time",
        "trailing particles slow over time",
        ),

    Pad(36),
    Struct("particle rotational velocity", INCLUDE=velocity_properties),
    Struct("effect rotational velocity", INCLUDE=velocity_properties),
    Struct("effect translational velocity", INCLUDE=velocity_properties),
    Struct("particle distance to object",
        BSEnum16("attachment", *function_outputs),
        Pad(2),
        BFloat("min distance"),
        BFloat("max distance"),
        BFloat("low multiplier"),
        BFloat("high multiplier")
        ),

    Pad(8),
    Struct("particle size",
        BSEnum16("attachment", *function_outputs),
        Pad(2),
        QStruct("size bounds", INCLUDE=from_to),  # world units
        QStruct("size attachment multiplier", INCLUDE=from_to),
        ),

    Struct("particle color",
        BSEnum16("attachment", *function_outputs),
        Pad(2),
        QStruct("color bound 0", INCLUDE=argb_float),
        QStruct("color bound 1", INCLUDE=argb_float),
        QStruct("scale color 0", INCLUDE=argb_float),
        QStruct("scale color 1", INCLUDE=argb_float)
        ),

    BFloat("color rate of change"),
    BFloat("fading percentage of glow"),
    BFloat("particle generation frequency"),  # Hz
    BFloat("lifetime of trailing particles"),
    BFloat("velocity of trailing particles"),
    BFloat("trailing particle min time"),
    BFloat("trailing particle max time"),

    Pad(52),
    dependency("texture",  valid_bitmaps),
    SIZE=340,
    )

def get():
    return glw__def

glw__def = TagDef("glw!",
    blam_header('glw!'),
    glw__body,

    ext=".glow", endian=">"
    )
