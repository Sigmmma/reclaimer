from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

def get(): return cont_def

point_state = Struct("point state",
    from_to_sec("state duration"),
    from_to_sec("state transition duration"),
    dependency("physics", "pphy"),
    Pad(32),
    float_wu("width"),
    QStruct("color lower bound", INCLUDE=argb_float),
    QStruct("color upper bound", INCLUDE=argb_float),
    Bool32("scale flags",
        "duration",
        "duration delta",
        "transition duration",
        "transition duration delta",
        "color",
        ),
    SIZE=104
    )

cont_body = Struct("tagdata",
    Bool16("flags",
        "first point unfaded",
        "last point unfaded",
        "points start pinned to media",
        "points start pinned to ground",
        "points always pinned to media",
        "points always pinned to ground",
        "edge effect fades slowly",
        ),
    Bool16("scale flags",
        "point generation rate",
        "point velocity",
        "point velocity delta",
        "point velocity cone angle",
        "inherited velocity fraction",
        "sequence animation rate",
        "texture scale u",
        "texture scale v",
        "texture animation u",
        "texture animation v",
        ),

    Struct("point creation",
        Float("generation rate",
               SIDETIP="points/sec", UNIT_SCALE=per_sec_unit_scale),
        from_to_wu_sec("velocity"),
        float_rad("velocity cone angle"),
        Float("inherited velocity fraction"),
        ),

    Struct("rendering",
        SEnum16("render type",
            "vertical orientation",
            "horizontal orientation",
            "media mapped",
            "ground mapped",
            "viewer-facing",
            "double-marker linked",
            ),
        Pad(2),
        Float("texture repeats u"),
        Float("texture repeats v"),

        # according to michelle, these dont need to be given a 60fps unit scale
        Float("texture animation u", SIDETIP="repeats/sec"),
        Float("texture animation v", SIDETIP="repeats/sec"),
        Float("animation rate", SIDETIP="frames/sec"),
        dependency("bitmap", "bitm"),
        SInt16("first sequence index"),
        SInt16("sequence count"),
        Pad(100),

        FlUInt32("unknown0", VISIBLE=False),
        Bool16("shader flags", *shader_flags),
        SEnum16("framebuffer blend function", *framebuffer_blend_functions),
        SEnum16("framebuffer fade mode", *render_fade_mode),
        Bool16("map flags",
            "unfiltered",
            ),
        ),
    Pad(12),  # OS v4 shader extension padding
    Pad(16),

    Struct("secondary map",
        dependency("bitmap", "bitm"),
        SEnum16("anchor", *render_anchor),
        Bool16("map flags",
            "unfiltered",
            ),

        Struct("u-animation", INCLUDE=anim_src_func_per_pha_sca),
        Struct("v-animation", INCLUDE=anim_src_func_per_pha_sca),
        Struct("rotation-animation", INCLUDE=anim_src_func_per_pha_sca_rot),
        QStruct("rotation center", INCLUDE=xy_float),
        Pad(4),
        Float("zsprite radius scale"),
        Pad(20),
        ),
    reflexive("point states", point_state, 16),
    SIZE=324,
    )

cont_def = TagDef("cont",
    blam_header('cont', 3),
    cont_body,

    ext=".contrail", endian=">", tag_cls=HekTag
    )
