from ...common_descs import *
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
    QStruct("lifespan", INCLUDE=from_to),
    BFloat("fade in time"),
    BFloat("fade out time"),

    dependency("collision effect", valid_event_effects),
    dependency("death effect", valid_event_effects),
    BFloat("minimum size"),

    Pad(8),
    QStruct("radius animation", INCLUDE=from_to),

    Pad(4),
    QStruct("animation rate", INCLUDE=from_to),
    BFloat("contact deterioration"),
    BFloat("fade start size"),
    BFloat("fade end size"),

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
    Pad(28),

    #Secondary map
    Struct("secondary map",
        dependency("bitmap", "bitm"),
        BSEnum16("anchor", *render_anchor),
        BBool16("flags",
            "unfiltered"
            ),
        Struct("u-animation", INCLUDE=anim_src_func_per_pha_sca),
        Struct("v-animation", INCLUDE=anim_src_func_per_pha_sca),
        Struct("rotation-animation", INCLUDE=anim_src_func_per_pha_sca),
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

    ext=".particle", endian=">",
    )
