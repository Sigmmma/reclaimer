from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

text_value_pair = Struct("effect_instance",
    Bool8("flags",
        "default setting",
        "unchanged setting",
        ),
    Pad(3),

    BSInt32("integer"),
    BFloat("real"),
    dependency("string id", valid_string_id_yelo),
    Pad(4),
    dependency("label string id", valid_string_id_yelo),
    Pad(4),
    dependency("description string id", valid_string_id_yelo),

    SIZE=72
    )

sily_body = Struct("tagdata",
    dependency("parameter", valid_string_id_yelo),
    Pad(4),
    dependency("title text", valid_string_id_yelo),
    Pad(4),
    dependency("description text", valid_string_id_yelo),

    Pad(4),
    BSEnum16("type",
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

    ext=".text_value_pair_definition", endian=">"
    )
