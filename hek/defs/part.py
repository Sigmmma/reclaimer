from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

part_body = Struct("tagdata",
    Bool32("flags",
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

    Struct("rendering",
        Float("minimum size", SIDETIP="pixels"),
        FlSInt32("unknown0", VISIBLE=False),
        FlFloat("unknown1", VISIBLE=False),
        QStruct("radius animation", INCLUDE=from_to),
        Pad(4),
        QStruct("animation rate",
            Float("from", UNIT_SCALE=per_sec_unit_scale, GUI_NAME=''),
            Float("to",   UNIT_SCALE=per_sec_unit_scale),
            ORIENT='h', SIDETIP='frames/sec'
            ),
        Float("contact deterioration"),
        Float("fade start size", SIDETIP="pixels"),
        Float("fade end size", SIDETIP="pixels"),

        Pad(4),
        SInt16("first sequence index"),
        SInt16("initial sequence count"),
        SInt16("looping sequence count"),
        SInt16("final sequence count"),

        Pad(12),
        SEnum16("orientation", *render_mode),

        Pad(38),
        FlUInt32("unknown2", VISIBLE=False),
        Bool16("shader flags", *shader_flags),
        SEnum16("framebuffer blend function", *framebuffer_blend_functions),
        SEnum16("framebuffer fade mode", *render_fade_mode),
        Bool16("map flags",
            "unfiltered"
            ),
        ),
    Pad(12),  # OS v4 shader extension padding
    Pad(16),

    #Secondary map
    Struct("secondary map",
        dependency("bitmap", "bitm"),
        SEnum16("anchor", *render_anchor),
        Bool16("flags",
            "unfiltered"
            ),
        Struct("u-animation", INCLUDE=anim_src_func_per_pha_sca),
        Struct("v-animation", INCLUDE=anim_src_func_per_pha_sca),
        Struct("rotation-animation", INCLUDE=anim_src_func_per_pha_sca_rot),
        QStruct("rotation center", INCLUDE=xy_float),
        Pad(4),
        Float("zsprite radius scale"),
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
