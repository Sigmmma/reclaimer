from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

part_body = Struct("tagdata",
    BBool32("flags",
        "can animate backwards",
        "animation stops at rest",
        "animation starts on random frame",
        "animate once per frame",
        "dies at rest",
        "dies on contact with structure",
        "tint from diffuse texture",
        "dies on contact with water",
        "dies on contact with air",
        "self illuminated",
        "random horizontal mirroring",
        "random vertical mirroring",
        ),
    dependency("bitmap", "bitm"),
    dependency("physics", "pphy"),
    # apparently marty traded his kids for this >:3
    dependency("impact effect", "foot"),

    Pad(4),
    from_to_sec("lifespan"),
    float_sec("fade in time"),
    float_sec("fade out time"),

    dependency("collision effect", valid_event_effects),
    dependency("death effect", valid_event_effects),
    BFloat("minimum size", SIDETIP="pixels"),

    Pad(8),
    QStruct("radius animation", INCLUDE=from_to),
    Pad(4),
    QStruct("animation rate",
        BFloat("from", UNIT_SCALE=per_sec_unit_scale, GUI_NAME=''),
        BFloat("to",   UNIT_SCALE=per_sec_unit_scale),
        ORIENT='h', SIDETIP='frames/sec'
        ),
    BFloat("contact deterioration"),
    BFloat("fade start size", SIDETIP="pixels"),
    BFloat("fade end size", SIDETIP="pixels"),

    Pad(4),
    BSInt16("first sequence index"),
    BSInt16("initial sequence count"),
    BSInt16("looping sequence count"),
    BSInt16("final sequence count"),

    Pad(12),
    BSEnum16("orientation", *render_mode),

    Pad(42),
    BBool16("shader flags", *shader_flags),
    BSEnum16("framebuffer blend function", *framebuffer_blend_functions),
    BSEnum16("framebuffer fade mode", *render_fade_mode),
    BBool16("map flags",
        "unfiltered"
        ),
    Pad(12),  # OS v4 shader extension padding
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

    SIZE=356,
    )

    
def get():
    return part_def

part_def = TagDef("part",
    blam_header("part", 2),
    part_body,

    ext=".particle", endian=">", tag_cls=HekTag,
    )
