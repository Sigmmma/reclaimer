from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

shader = Struct("shader",
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
    SIZE=180
    )

marker = Struct("marker",
    StrLatin1("attachment marker", SIZE=32),
    BBool16("flags",
        "not connected to next marker"
        ),

    Pad(2),
    BSInt16("octaves to next marker"),

    Pad(78),
    QStruct("random position bounds", INCLUDE=ijk_float),
    BFloat("random jitter"),
    BFloat("thickness"),
    QStruct("tint", INCLUDE=argb_float),
    SIZE=228
    )

elec_body = Struct("tagdata",
    Pad(2),
    BSInt16("count"),

    Pad(16),
    BFloat("near fade distance"),
    BFloat("far fade distance"),

    Pad(16),
    BSEnum16("jitter scale source", *function_outputs),
    BSEnum16("thickness scale source", *function_outputs),
    BSEnum16("tint modulation source", *function_names),
    BSEnum16("brightness scale source", *function_outputs),
    dependency("bitmap", valid_bitmaps),

    Pad(84),
    reflexive("markers", marker, 16),
    reflexive("shaders", shader, 1),

    SIZE=264,
    )

    
def get():
    return elec_def

elec_def = TagDef("elec",
    blam_header("elec"),
    elec_body,

    ext=".lightning", endian=">",
    )
