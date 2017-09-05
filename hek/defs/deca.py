from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

deca_body = Struct("tagdata",
    #Decal Properties
    Bool16("meter shader flags",
        "geometry inherited by next decal in chain",
        "interpolate color in hsv",
        "more colors",
        "no random rotation",
        "water effect",
        "SAPIEN-snap to axis",
        "SAPIEN-incremental counter",
        "animation loop",
        "preserve aspect",
        ),
    SEnum16("type",
        "scratch",
        "splatter",
        "burn",
        "painted sign",
        ),
    SEnum16("layer",
        "primary",
        "secondary",
        "light",
        "alpha-tested",
        "water"
        ),
    Pad(2),
    dependency("next decal in chain", "deca"),
    from_to_wu("radius"),  # world units
    Pad(12),

    Struct("color",
        from_to_zero_to_one("intensity"),  # [0,1]
        Struct("lower bounds", INCLUDE=rgb_float),
        Struct("upper bounds", INCLUDE=rgb_float),
        Pad(12),
        ),

    #Animation
    Struct("animation",
        SInt16("loop frame"),
        SInt16("speed", MIN=1, MAX=120,
                SIDETIP="[1,120] ticks/frame", UNIT_SCALE=per_sec_unit_scale),
        Pad(28),
        from_to_sec("lifetime"),  # seconds
        from_to_sec("decay time"),  # seconds
        Pad(56),
        ),

    #Shader
    Struct("shader",
        SEnum16("framebuffer blend function", *framebuffer_blend_functions),
        Pad(22),
        dependency("shader map", "bitm"),
        ),

    #Sprite info
    Pad(20),
    Float("maximum sprite extent", SIDETIP="pixels"),

    SIZE=268,
    )



def get():
    return deca_def

deca_def = TagDef("deca",
    blam_header('deca'),
    deca_body,

    ext=".decal", endian=">", tag_cls=HekTag
    )
