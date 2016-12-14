from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

deca_body = Struct("tagdata",
    #Decal Properties
    BBool16("meter shader flags",
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
    BSEnum16("type",
        "scratch",
        "splatter",
        "burn",
        "painted sign",
        ),
    BSEnum16("layer",
        "primary",
        "secondary",
        "light",
        "alpha-tested",
        "water"
        ),
    Pad(2),
    dependency("next decal in chain", "deca"),

    #Radius and color
    from_to_wu("radius"),  # world units
    Pad(12),
    from_to_zero_to_one("intensity"),  # [0,1]
    Struct("color lower bounds", INCLUDE=rgb_float),
    Struct("color upper bounds", INCLUDE=rgb_float),
    Pad(12),

    #Animation
    BSInt16("animation loop frame"),
    BSInt16("animation speed", MIN=1, MAX=120, SIDETIP="[1,120] ticks/frame"),
    Pad(28),
    from_to_sec("lifetime"),  # seconds
    from_to_sec("decay time"),  # seconds
    Pad(56),

    #Shader
    BSEnum16("framebuffer blend function", *framebuffer_blend_functions),
    Pad(22),
    dependency("shader map", "bitm"),

    #Sprite info
    Pad(20),
    BFloat("maximum sprite extent", SIDETIP="pixels"),

    SIZE=268,
    )



def get():
    return deca_def

deca_def = TagDef("deca",
    blam_header('deca'),
    deca_body,

    ext=".decal", endian=">"
    )
