from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

occlusion_comment = """Occlusion factor affects overall lens flare brightness and can also affect scale.
Occlusion never affects rotation."""

corona_rotation_comment = """Controls how corona rotation is affected by the viewer and light angles."""

reflection = Struct("reflection",
    Bool16("flags",
        "align rotation with screen center",
        "radius not scaled by distance",
        "radius scaled by occlusion factor",
        "occluded by solid objects",
        ),
    Pad(2),
    SInt16("bitmap index"),
    Pad(22),
    Float("position", SIDETIP="along flare axis"), # along flare axis
    float_deg("rotation offset"), # degrees
    Pad(4),
    from_to_wu("radius"),  # world units
    SEnum16("radius scaled by",
        "none",
        "rotation",
        "rotation and strafing",
        "distance from center",
        ),
    Pad(2),
    from_to_zero_to_one("brightness"),  # [0,1]
    SEnum16("brightness scaled by",
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
        Bool16("flags", *blend_flags),
        SEnum16("function", *animation_functions),
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
        SEnum16("offset direction",
            "toward viewer",
            "marker forward",
            "none",
            ),
        Pad(2),
        float_wu("near fade distance"),
        float_wu("far fade distance"),
		COMMENT=occlusion_comment
        ),

    Struct("bitmaps",
        dependency("bitmap", "bitm"),
        Bool16("flags",
            "sun",
            ),
        Pad(78),
        ),

    Struct("corona rotation",
        SEnum16("function",
            "none",
            "rotation a",
            "rotation b",
            "rotation translation",
            "translation",
            ),
        Pad(2),
        float_rad("function scale"),  # radians
		COMMENT=corona_rotation_comment
        ),

    Struct("corona radius scale",
        Pad(24),
        Float("horizontal scale"),
        Float("vertical scale"),
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
