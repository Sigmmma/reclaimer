from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

shader = Struct("shader",
    Pad(40),
    Bool16("shader flags", *shader_flags),
    SEnum16("framebuffer blend function", *framebuffer_blend_functions),
    SEnum16("framebuffer fade mode", *render_fade_mode),
    Bool16("map flags",
        "unfiltered"
        ),
    SIZE=180
    )

marker = Struct("marker",
    ascii_str32("attachment marker"),
    Bool16("flags",
        "not connected to next marker"
        ),

    Pad(2),
    SInt16("octaves to next marker"),

    Pad(78),
    QStruct("random position bounds", INCLUDE=ijk_float, SIDETIP="world units"),
    float_wu("random jitter"),
    float_wu("thickness"),
    QStruct("tint", INCLUDE=argb_float),
    SIZE=228
    )

elec_body = Struct("tagdata",
    Pad(2),
    SInt16("effects count"),

    Pad(16),
    float_wu("near fade distance"),
    float_wu("far fade distance"),

    Pad(16),
    SEnum16("jitter scale source", *function_outputs),
    SEnum16("thickness scale source", *function_outputs),
    SEnum16("tint modulation source", *function_names),
    SEnum16("brightness scale source", *function_outputs),
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
