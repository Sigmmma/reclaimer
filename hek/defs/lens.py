from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

reflection = Struct("reflection",
    BBool16("flags",
        "align rotation with screen center",
        "radius not scaled by distance",
        "radius scaled by occlusion factor",
        "occluded by solid objects",
        ),
    Pad(2),
    BSInt16("bitmap index"),
    Pad(22),
    BFloat("position", SIDETIP="along flare axis"), # along flare axis
    float_deg("rotation offset"), # degrees
    Pad(4),
    from_to_wu("radius"),  # world units
    BSEnum16("radius scaled by",
        "none",
        "rotation",
        "rotation and strafing",
        "distance from center",
        ),
    Pad(2),
    from_to_zero_to_one("brightness"),  # [0,1]
    BSEnum16("brightness scaled by",
        "none",
        "rotation",
        "rotation and strafing",
        "distance from center",
        ),
    Pad(2),

    #Tint color
    QStruct("tint color", INCLUDE=argb_float),

    #Animation
    Struct("animation",
        QStruct("color lower bound", INCLUDE=argb_float),
        QStruct("color upper bound", INCLUDE=argb_float),
        BBool16("flags", *blend_flags),
        BSEnum16("function", *animation_functions),
        float_sec("period"),  # seconds
        float_sec("phase"),  # seconds
        ),

    SIZE=128
    )


lens_body = Struct("tagdata",
    float_rad("falloff angle"),  # radians
    float_rad("cutoff angle"),  # radians
    FlFloat("unknown0", DEFAULT=1.0, VISIBLE=False),
    FlFloat("unknown1", DEFAULT=1.0, VISIBLE=False),
    Struct("occlusion",
        float_wu("radius"),
        BSEnum16("offset direction",
            "toward viewer",
            "marker forward",
            "none",
            ),
        Pad(2),
        float_wu("near fade distance"),
        float_wu("far fade distance"),
        ),

    Struct("bitmaps",
        dependency("bitmap", "bitm"),
        BBool16("flags",
            "sun",
            ),
        Pad(78),
        ),

    Struct("corona rotation",
        BSEnum16("function",
            "none",
            "rotation a",
            "rotation b",
            "rotation translation",
            "translation",
            ),
        Pad(2),
        float_rad("function scale"),  # radians
        ),

    Struct("corona radius scale",
        Pad(24),
        BFloat("horizontal scale"),
        BFloat("vertical scale"),
        ),

    Pad(28),

    reflexive("reflections", reflection, 32),

    SIZE=240,
    )

    
def get():
    return lens_def

lens_def = TagDef("lens",
    blam_header("lens", 2),
    lens_body,

    ext=".lens_flare", endian=">", tag_cls=HekTag,
    )
