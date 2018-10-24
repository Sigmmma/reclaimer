from ...common_descs import *
from ...hek.defs.objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

text_value_pair = Struct("text value pair",
    Bool8("flags",
        "default setting",
        "unchanged setting",
        ),
    Pad(3),

    SInt32("integer"),
    Float("real"),
    dependency_os("string id", "sidy"),
    Pad(4),
    dependency_os("label string id", "sidy"),
    Pad(4),
    dependency_os("description string id", "sidy"),

    SIZE=72
    )

sily_body = Struct("tagdata",
    dependency_os("parameter", "sidy"),
    Pad(4),
    dependency_os("title text", "sidy"),
    Pad(4),
    dependency_os("description text", "sidy"),

    Pad(4),
    SEnum16("type",
        "integer",
        "string id",
        "unused",
        "real",
        ),

    Pad(2),
    reflexive("text value pairs", text_value_pair, 32),
    SIZE=76
    )

def get():
    return sily_def

sily_def = TagDef("sily",
    blam_header_os('sily', 0),
    sily_body,

    ext=".text_value_pair_definition", endian=">", tag_cls=HekTag
    )
