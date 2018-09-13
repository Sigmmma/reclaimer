from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

decal_comment = """COMPOUND DECALS:
A 'compound decal' is a chain of decals which are instantiated simultaneously. 
Compound decals are created by choosing a <next_decal_in_chain> below. 
NOTE: Do not attempt to create a circularly linked decal chain, i.e. A->B->C->A! 
Also, do not reference a decal from an effect if it is not the 'head' of the chain;
for example an effect should not instantiate decal B if the chain was A->B->C. 
Compound decals can have seperate bitmaps, seperate framebuffer blend functions, 
and can be drawn in seperate layers. In addition, each decal in the chain can either 
inherit its parent's <radius>, rotation, <color>, <fade>, and <sequence> - 
or it can randomly choose its own. This behavior is controlled by the 
'geometry_inherited_by_next_decal_in_chain' flag, below. 

DECAL TYPING AND LAYERING:
The decal <type> (or layer) determines the drawing order of the decal with respect 
to the rest of the environment. Decals in the primary layer are drawn after the 
environment diffuse texture, hence they affect the already-lit texture of the surface.
Decals in the secondary layer are drawn immediately after decals in the primary layer,
so they 'cover up' the primary decals. Decals in the 'light' layer are drawn before
the environment diffuse texture, hence they affect the accumulated diffuse light and
only indirectly affect the lit texture."""

deca_body = Struct("tagdata",
    #Decal Properties
    Bool16("flags",
        "geometry inherited by next decal in chain",
        "interpolate color in hsv",
        "more colors",
        "no random rotation",
        "water effect",
        "SAPIEN-snap to axis",
        "SAPIEN-incremental counter",
        "animation loop",
        "preserve aspect",
        COMMENT=decal_comment
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
