from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

shader_function = Struct('shader function',
    Pad(4),
    ascii_str32("global function name"),
    SIZE=36
    )

animation = Struct('animation',
    SInt16('animation index'),
    Pad(2),
    float_sec("period"),
    SIZE=36
    )

light = Struct('light',
    dependency("lens flare", "lens"),
    ascii_str32("global function name"),
    Pad(28),
    Bool32('flags',
        'affects exteriors',
        'affects interiors',
        ),
    QStruct("color", INCLUDE=rgb_float),
    Float("power"),
    Float("test distance"),
    Pad(4),
    yp_float_rad("direction"),  # radians
    float_rad("diameter"),  # radians (yeah, it sounds weird, but this
    #                         value is stored as a radian coefficient)
    SIZE=116
    )


sky__body = Struct("tagdata",
    dependency("model", valid_models),
    dependency("animation graph", "antr"),
    Pad(24),

    QStruct("indoor ambient radiosity color", INCLUDE=rgb_float),
    Float("indoor ambient radiosity power"),

    QStruct("outdoor ambient radiosity color", INCLUDE=rgb_float),
    Float("outdoor ambient radiosity power"),

    QStruct("outdoor fog color", INCLUDE=rgb_float),
    Pad(8),
    float_zero_to_one("outdoor fog maximum density"),
    float_wu("outdoor fog start distance"),
    float_wu("outdoor fog opaque distance"),

    QStruct("indoor fog color", INCLUDE=rgb_float),
    Pad(8),
    float_zero_to_one("indoor fog maximum density"),
    float_wu("indoor fog start distance"),
    float_wu("indoor fog opaque distance"),

    dependency("indoor fog screen", "fog "),
    Pad(4),
    reflexive("shader functions", shader_function, 8,
        DYN_NAME_PATH='.global_function_name'),
    reflexive("animations", animation, 8),
    reflexive("lights", light, 8,
        DYN_NAME_PATH='.lens_flare.filepath'),

    SIZE=208,
    )

    
def get():
    return sky__def

sky__def = TagDef("sky ",
    blam_header('sky '),
    sky__body,

    ext=".sky", endian=">", tag_cls=HekTag,
    )
