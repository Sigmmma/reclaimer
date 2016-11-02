from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

def get(): return cont_def

point_state = Struct("point state",
    QStruct("state duration", INCLUDE=from_to),
    QStruct("state transition duration", INCLUDE=from_to),
    dependency("physics", valid_point_physics),
    Pad(32),
    BFloat("width"),
    QStruct("color lower bound", INCLUDE=argb_float),
    QStruct("color upper bound", INCLUDE=argb_float),
    BBool32("scale flags",
        "duration",
        "duration delta",
        "transition duration",
        "transition duration delta",
        "color",
        ),
    SIZE=104
    )

cont_body = Struct("tagdata",
    BBool16("flags",
        "first point unfaded",
        "last point unfaded",
        "points start pinned to media",
        "points start pinned to ground",
        "points always pinned to media",
        "points always pinned to ground",
        "edge effect fades slowly",
        ),
    BBool16("scale flags",
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
        BFloat("generation rate"),
        QStruct("veloctiy", INCLUDE=from_to),
        BFloat("velocity cone angle"),
        BFloat("inherited velocity fraction"),
        ),

    Struct("rendering",
        BSEnum16("render type",
            "vertical orientation",
            "horizontal orientation",
            "media mapped",
            "ground mapped",
            "viewer-facing",
            "double-marker linked",
            ),
        Pad(2),
        BFloat("texture repeats u"),
        BFloat("texture repeats v"),
        BFloat("texture animation u"),  # repeats per second
        BFloat("texture animation v"),  # repeats per second
        BFloat("animation rate"),  # frames per second
        dependency("bitmap", valid_bitmaps),
        BSInt16("first sequence index"),
        BSInt16("sequence count"),
        Pad(104),

        BBool16("shader flags", *shader_flags),
        BSEnum16("framebuffer blend function", *framebuffer_blend_functions),
        BSEnum16("framebuffer fade mode", *render_fade_mode),
        BBool16("map flags",
            "unfiltered",
            ),
        Pad(28),
        ),

    Struct("secondary map",
        dependency("bitmap", valid_bitmaps),
        BSEnum16("anchor", *render_anchor),
        BBool16("map flags",
            "unfiltered",
            ),

        Struct("u-animation", INCLUDE=anim_src_func_per_pha_sca),
        Struct("v-animation", INCLUDE=anim_src_func_per_pha_sca),
        Struct("rotation-animation", INCLUDE=anim_src_func_per_pha_sca),
        QStruct("rotation center", INCLUDE=xy_float),
        Pad(4),
        BFloat("zsprite radius scale"),
        Pad(20),
        ),
    reflexive("point states", point_state, 16),
    SIZE=324,
    )

cont_def = TagDef("cont",
    blam_header('cont', 3),
    cont_body,

    ext=".contrail", endian=">"
    )
