from ...hek.defs.pctl import *

particle_state = Struct("particle state",
    ascii_str32("name"),
    from_to_sec("duration bounds"),
    from_to_sec("transition time bounds"),

    dependency("bitmaps", "bitm"),
    BSInt16("sequence index"),

    Pad(6),
    QStruct("scale", INCLUDE=from_to,
        UNIT_SCALE="world units/pixel"),  # world units/sec
    QStruct("animation rate", INCLUDE=from_to,
        UNIT_SCALE="frames/sec"),  # frames/sec
    from_to_rad_sec("rotation rate"),  # radians/sec
    QStruct("color 1", INCLUDE=argb_float),
    QStruct("color 2", INCLUDE=argb_float),
    BFloat("radius multiplier"),
    dependency("physics", "pphy"),

    Pad(76),
    BBool16("shader flags", *shader_flags),
    BSEnum16("framebuffer blend function", *framebuffer_blend_functions),
    BSEnum16("framebuffer fade mode", *render_fade_mode),
    BBool16("map flags",
        "unfiltered"
        ),

    reflexive("particle shader extensions", particle_shader_extension, 1),
    Pad(16),
    #Secondary map
    Struct("secondary map",
        dependency("bitmap", "bitm"),
        BSEnum16("anchor", *render_anchor),
        BBool16("flags",
            "unfiltered"
            ),
        Struct("u-animation", INCLUDE=anim_src_func_per_pha_sca),
        Struct("v-animation", INCLUDE=anim_src_func_per_pha_sca),
        Struct("rotation-animation", INCLUDE=anim_src_func_per_pha_sca_rot),
        QStruct("rotation center", INCLUDE=xy_float),
        Pad(4),
        BFloat("zsprite radius scale"),
        ),

    Pad(20),
    reflexive("physics constants", physics_constant, 16),
    SIZE=376
    )

particle_type = dict(particle_type)
pctl_body = dict(pctl_body)
particle_type[12] = reflexive(
    "particle states", particle_state, 8, DYN_NAME_PATH='.name')
pctl_body[5] = reflexive(
    "particle types", particle_type, 4, DYN_NAME_PATH='.name')

    
def get():
    return pctl_def

pctl_def = TagDef("pctl",
    blam_header("pctl", 4),
    pctl_body,

    ext=".particle_system", endian=">", tag_cls=HekTag,
    )
