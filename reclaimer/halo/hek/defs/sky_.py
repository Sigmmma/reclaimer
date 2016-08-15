from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

shader_function = Struct('shader function',
    Pad(4),
    StrLatin1("global function name", SIZE=32),
    SIZE=36
    )

animation = Struct('animation',
    BSInt16('animation index'),
    Pad(2),
    BFloat("period"),
    SIZE=36
    )

light = Struct('light',
    dependency("lens flare", valid_lens_flare),
    StrLatin1("global function name", SIZE=32),
    Pad(28),
    BBool32('flags',
        'affects exteriors',
        'affects interiors',
        ),
    Struct("color", INCLUDE=rgb_float),
    BFloat("power"),
    BFloat("test distance"),
    Pad(4),
    Struct("direction", INCLUDE=yp_float),  # measured in radians
    BFloat("diameter"),  # displayed_value == internal_value * 180/pi
    SIZE=116
    )


sky__body = Struct("tagdata",
    dependency("model", valid_models),
    dependency("animation graph", valid_model_animations),
    Pad(24),

    Struct("indoor ambient radiosity color", INCLUDE=rgb_float),
    BFloat("indoor ambient radiosity power"),

    Struct("outdoor ambient radiosity color", INCLUDE=rgb_float),
    BFloat("outdoor ambient radiosity power"),

    Struct("outdoor fog color", INCLUDE=rgb_float),
    Pad(8),
    BFloat("outdoor fog maximum density"),
    BFloat("outdoor fog start distance"),
    BFloat("outdoor fog opaque distance"),

    Struct("indoor fog color", INCLUDE=rgb_float),
    Pad(8),
    BFloat("indoor fog maximum density"),
    BFloat("indoor fog start distance"),
    BFloat("indoor fog opaque distance"),

    dependency("indoor fog screen", valid_fog),
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
