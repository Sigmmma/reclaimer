from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

particle_type = Struct("particle_type",
    ascii_str32("name"),
    BBool32("flags",
        "blend colors in hsv",
        "along long hue path",
        "random rotation",
        ),
    QStruct("fade",
        float_wu("in start distance"),
        float_wu("in end distance"),
        float_wu("out start distance"),
        float_wu("out end distance"),
        float_wu("in start height"),
        float_wu("in end height"),
        float_wu("out start height"),
        float_wu("out end height"),
        ),

    Pad(96),
    QStruct("particle count", INCLUDE=from_to,
        SIDETIP="particles/(world unit^3)"),
    dependency("physics", "pphy"),

    Pad(16),
    Struct("acceleration",
        QStruct("magnitude", INCLUDE=from_to),
        float_rad("turning rate"),  # radians
        BFloat("change rate"),
        ),

    Pad(32),
    from_to_wu("particle radius"),
    QStruct("animation rate",
        BFloat("from", UNIT_SCALE=per_sec_unit_scale, GUI_NAME=''),
        BFloat("to",   UNIT_SCALE=per_sec_unit_scale),
        ORIENT='h', SIDETIP="frames/sec"
        ),
    from_to_rad_sec("rotation rate"),  # radians/sec

    Pad(32),
    QStruct("color lower bound", INCLUDE=argb_float),
    QStruct("color upper bound", INCLUDE=argb_float),

    #Shader
    Struct("shader",
        Pad(64),
        dependency("sprite bitmap", "bitm"),
        BSEnum16("render mode", *render_mode),
        BSEnum16("render direction source",
            "from velocity",
            "from acceleration"
            ),

        Pad(40),
        BBool16("shader flags", *shader_flags),
        BSEnum16("framebuffer blend function", *framebuffer_blend_functions),
        BSEnum16("framebuffer fade mode", *render_fade_mode),
        BBool16("map flags",
            "unfiltered"
            )
        ),

    #Secondary bitmap
    Struct("secondary bitmap",
        Pad(28),
        dependency("bitmap", "bitm"),
        BSEnum16("anchor", *render_anchor),
        BBool16("secondary map flags",
            "unfiltered"
            ),
        Struct("u-animation", INCLUDE=anim_src_func_per_pha_sca),
        Struct("v-animation", INCLUDE=anim_src_func_per_pha_sca),
        Struct("rotation-animation", INCLUDE=anim_src_func_per_pha_sca_rot),
        QStruct("rotation center", INCLUDE=xy_float)
        ),

    Pad(4),
    BFloat("zsprite radius scale"),

    SIZE=604
    )

rain_body = Struct("tagdata",
    Pad(36),
    reflexive("particle types", particle_type, 8, DYN_NAME_PATH='.name'),

    SIZE=48,
    )

    
def get():
    return rain_def

rain_def = TagDef("rain",
    blam_header("rain"),
    rain_body,

    ext=".weather_particle_system", endian=">", tag_cls=HekTag,
    )
