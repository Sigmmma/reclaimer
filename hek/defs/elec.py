from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

shader = Struct("shader",
    Pad(40),
    BBool16("shader flags", *shader_flags),
    BSEnum16("framebuffer blend function", *framebuffer_blend_functions),
    BSEnum16("framebuffer fade mode", *render_fade_mode),
    BBool16("map flags",
        "unfiltered"
        ),
    SIZE=180
    )

marker = Struct("marker",
    ascii_str32("attachment marker"),
    BBool16("flags",
        "not connected to next marker"
        ),

    Pad(2),
    BSInt16("octaves to next marker"),

    Pad(78),
    QStruct("random position bounds", INCLUDE=ijk_float, SIDETIP="world units"),
    float_wu("random jitter"),
    float_wu("thickness"),
    QStruct("tint", INCLUDE=argb_float),
    SIZE=228
    )

elec_body = Struct("tagdata",
    Pad(2),
    BSInt16("count"),

    Pad(16),
    float_wu("near fade distance"),
    float_wu("far fade distance"),

    Pad(16),
    BSEnum16("jitter scale source", *function_outputs),
    BSEnum16("thickness scale source", *function_outputs),
    BSEnum16("tint modulation source", *function_names),
    BSEnum16("brightness scale source", *function_outputs),
    dependency("bitmap", "bitm"),

    Pad(84),
    reflexive("markers", marker, 16, DYN_NAME_PATH='.attachment_marker'),
    reflexive("shaders", shader, 1),

    SIZE=264,
    )

    
def get():
    return elec_def

elec_def = TagDef("elec",
    blam_header("elec"),
    elec_body,

    ext=".lightning", endian=">", tag_cls=HekTag,
    )
