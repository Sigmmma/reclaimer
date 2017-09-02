from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

particle_creation_physics = (
    "default",
    "explosion",
    "jet"
    )

physics_constant = QStruct("physics constant",
    BFloat("k", UNIT_SCALE=per_sec_unit_scale),
    )

state = Struct("state",
    ascii_str32("name"),
    from_to_sec("duration bounds"),
    from_to_sec("transition time bounds"),

    Pad(4),
    BFloat("scale multiplier"),
    BFloat("animation rate multiplier"),
    BFloat("rotation rate multiplier"),
    QStruct("color multiplier", INCLUDE=argb_float),
    BFloat("radius multiplier"),
    BFloat("minimum particle count"),
    BFloat("particle creation rate",
           SIDETIP="particles/sec", UNIT_SCALE=per_sec_unit_scale),

    Pad(84),
    BSEnum16("particle creation physics", *particle_creation_physics),
    Pad(2),  # BSEnum16("particle update physics", "default"),
    reflexive("physics constants", physics_constant, 16),
    SIZE=192
    )

particle_state = Struct("particle state",
    ascii_str32("name"),
    from_to_sec("duration bounds"),
    from_to_sec("transition time bounds"),

    dependency("bitmaps", "bitm"),
    BSInt16("sequence index"),
    Pad(6),
    QStruct("scale", INCLUDE=from_to, SIDETIP="world units/pixel"),
    QStruct("animation rate",
        BFloat("from", UNIT_SCALE=per_sec_unit_scale, GUI_NAME=''),
        BFloat("to",   UNIT_SCALE=per_sec_unit_scale),
        ORIENT='h', SIDETIP="frames/sec"
        ),
    from_to_rad_sec("rotation rate"),  # radians/sec
    QStruct("color 1", INCLUDE=argb_float),
    QStruct("color 2", INCLUDE=argb_float),
    BFloat("radius multiplier"),
    dependency("physics", "pphy"),

    Pad(72),
    FlUInt32("unknown0", VISIBLE=False),
    BBool16("shader flags", *shader_flags),
    BSEnum16("framebuffer blend function", *framebuffer_blend_functions),
    BSEnum16("framebuffer fade mode", *render_fade_mode),
    BBool16("map flags",
        "unfiltered"
        ),

    Pad(12),  # open sauce particle shader extension
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


particle_type = Struct("particle type",
    ascii_str32("name"),
    BBool32("flags",
        "type states loop",
        "type states loops forward/backward",
        "particle states loop",
        "particle states loops forward/backward",
        "particles die in water",
        "particles die in air",
        "particles die on ground",
        "rotational sprites animate sideways",
        "disabled",
        "tint by effect color",
        "initial count scales with effect",
        "minimum count scales with effect",
        "creation rate scales with effect",
        "radius scales with effect",
        "animation rate scales with effect",
        "rotation rate scales with effect",
        "dont draw in first person",
        "dont draw in third person",
        ),
    BSInt16("initial particle count"),

    Pad(2),
    BSEnum16("complex sprite render modes",
        "simple",
        "rotational"
        ),

    Pad(2),
    float_wu("radius"),

    Pad(36),
    BSEnum16("particle creation physics", *particle_creation_physics),

    Pad(6),
    reflexive("physics constants", physics_constant, 16),
    reflexive("states", state, 8, DYN_NAME_PATH='.name'),
    reflexive("particle states", particle_state, 8, DYN_NAME_PATH='.name'),
    SIZE=128
    )

pctl_body = Struct("tagdata",
    Pad(56),
    dependency("point physics", "pphy"),
    BSEnum16("system update physics",
        "default",
        "explosion"
        ),
    Pad(6),
    reflexive("physics constants", physics_constant, 16),
    reflexive("particle types", particle_type, 4, DYN_NAME_PATH='.name'),
    SIZE=104,
    )

    
def get():
    return pctl_def

pctl_def = TagDef("pctl",
    blam_header("pctl", 4),
    pctl_body,

    ext=".particle_system", endian=">", tag_cls=HekTag,
    )
