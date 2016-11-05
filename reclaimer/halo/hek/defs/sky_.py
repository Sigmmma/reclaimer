from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

shader_function = Struct('shader function',
    Pad(4),
    ascii_str32("global function name"),
    SIZE=36
    )

animation = Struct('animation',
    BSInt16('animation index'),
    Pad(2),
    BFloat("period"),
    SIZE=36
    )

light = Struct('light',
    dependency("lens flare", "lens"),
    ascii_str32("global function name"),
    Pad(28),
    BBool32('flags',
        'affects exteriors',
        'affects interiors',
        ),
    QStruct("color", INCLUDE=rgb_float),
    BFloat("power"),
    BFloat("test distance"),
    Pad(4),
    QStruct("direction", INCLUDE=yp_float),  # radians
    BFloat("diameter"),  # radians (yeah, it sounds weird, but this
    #                      value is stored as a radian coefficient)
    SIZE=116
    )


sky__body = Struct("tagdata",
    dependency("model", valid_models),
    dependency("animation graph", "antr"),
    Pad(24),

    QStruct("indoor ambient radiosity color", INCLUDE=rgb_float),
    BFloat("indoor ambient radiosity power"),

    QStruct("outdoor ambient radiosity color", INCLUDE=rgb_float),
    BFloat("outdoor ambient radiosity power"),

    QStruct("outdoor fog color", INCLUDE=rgb_float),
    Pad(8),
    BFloat("outdoor fog maximum density"),
    BFloat("outdoor fog start distance"),
    BFloat("outdoor fog opaque distance"),

    QStruct("indoor fog color", INCLUDE=rgb_float),
    Pad(8),
    BFloat("indoor fog maximum density"),
    BFloat("indoor fog start distance"),
    BFloat("indoor fog opaque distance"),

    dependency("indoor fog screen", "fog "),
    Pad(4),
    reflexive("shader functions", shader_function, 8),
    reflexive("animations", animation, 8),
    reflexive("lights", light, 8),

    SIZE=208,
    )

    
def get():
    return sky__def

sky__def = TagDef("sky ",
    blam_header('sky '),
    sky__body,

    ext=".sky", endian=">",
    )
