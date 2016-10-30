from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

particle_type = Struct("particle_type",
    StrLatin1("name", SIZE=32),
    BBool32("flags",
        "interpolate colors in hsv",
        "along long hue path",
        "random rotation",
        ),
    BFloat("fade-in start distance"),
    BFloat("fade-in end distance"),
    BFloat("fade-out start distance"),
    BFloat("fade-out end distance"),
    BFloat("fade-in start height"),
    BFloat("fade-in end height"),
    BFloat("fade-out start height"),
    BFloat("fade-out end height"),

    Pad(96),
    QStruct("particle count", INCLUDE=from_to),
    dependency("physics", valid_point_physics),

    Pad(16),
    QStruct("acceleration count", INCLUDE=from_to),
    BFloat("acceleration turning rate"),  # measured in radians
    BFloat("acceleration change rate"),

    Pad(32),
    QStruct("particle radius", INCLUDE=from_to),
    QStruct("animation rate", INCLUDE=from_to),
    QStruct("rotation rate", INCLUDE=from_to),  # measured in radians

    Pad(32),
    QStruct("color lower bound", INCLUDE=argb_float),
    QStruct("color upper bound", INCLUDE=argb_float),

    #Shader
    Pad(64),
    dependency("sprite bitmap", valid_bitmaps),
    BSEnum16("render mode",
        "screen facing",
        "parallel to direction",
        "perpendicular to direction",
        ),
    BSEnum16("render direction source",
        "from velocity",
        "from acceleration",
        ),

    Pad(40),
    BBool16("shader flags",
        "sort bias",
        "nonlinear tint",
        "dont overdraw fp weapon",
        ),
    BSEnum16("framebuffer blend function", *framebuffer_blend_functions),
    BSEnum16("framebuffer fade mode", *shader_fade_mode),
    BBool16("map flags",
        "unfiltered"
        ),
    Pad(28),

    #Secondary bitmap
    dependency("bitmap", valid_bitmaps),
    BSEnum16("anchor",
        "with primary",
        "with screen space",
        "with zsprite",
        ),
    BBool16("secondary map flags",
        "unfiltered"
        ),
    Struct("u-animation", INCLUDE=anim_src_func_per_pha_sca),
    Struct("v-animation", INCLUDE=anim_src_func_per_pha_sca),
    Struct("rotation-animation", INCLUDE=anim_src_func_per_pha_sca),
    QStruct("rotation center", INCLUDE=xy_float),
    Pad(4),
    BFloat("zsprite radius scale"),

    SIZE=604
    )

rain_body = Struct("tagdata",
    Pad(36),
    reflexive("particle types", particle_type, 8),

    SIZE=48,
    )

    
def get():
    return rain_def

rain_def = TagDef("rain",
    blam_header("rain"),
    rain_body,

    ext=".weather_particle_system", endian=">",
    )
