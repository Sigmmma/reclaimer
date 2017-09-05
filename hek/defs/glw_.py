from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

velocity_properties = Struct("velocity properties",
    SEnum16("attachment", *function_outputs),
    Pad(2),
    Float("velocity", UNIT_SCALE=per_sec_unit_scale),
    Float("low multiplier"),
    Float("high multiplier")
    )

glw__body = Struct("tagdata",
    ascii_str32("attachment marker"),
    SInt16("number of particles"),
    SEnum16("boundary effect",
        "bounce",
        "wrap",
        ),
    SEnum16("normal particle distribution",
        "random",
        "uniform",
        ),
    SEnum16("trailing particle distribution",
        "vertically",
        "normal",
        "randomly"
        ),
    Bool32("glow flags" ,
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
        SEnum16("attachment", *function_outputs),
        Pad(2),
        Float("min distance"),
        Float("max distance"),
        Float("low multiplier"),
        Float("high multiplier")
        ),

    Pad(8),
    Struct("particle size",
        SEnum16("attachment", *function_outputs),
        Pad(2),
        from_to_wu("size bounds"),  # world units
        QStruct("size attachment multiplier", INCLUDE=from_to),
        ),

    Struct("particle color",
        SEnum16("attachment", *function_outputs),
        Pad(2),
        QStruct("lower bound", INCLUDE=argb_float),
        QStruct("upper bound", INCLUDE=argb_float),
        QStruct("lower scale", INCLUDE=argb_float),
        QStruct("upper scale", INCLUDE=argb_float)
        ),

    Float("color rate of change"),
    Float("fading percentage of glow"),
    Float("particle generation frequency",
           SIDETIP="Hz", UNIT_SCALE=per_sec_unit_scale),
    float_sec("lifetime of trailing particles"),
    float_wu_sec("velocity of trailing particles"),
    float_sec("trailing particle min time"),
    float_sec("trailing particle max time"),

    Pad(52),
    dependency("texture",  "bitm"),
    SIZE=340,
    )

def get():
    return glw__def

glw__def = TagDef("glw!",
    blam_header('glw!'),
    glw__body,

    ext=".glow", endian=">", tag_cls=HekTag
    )
