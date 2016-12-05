from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

script_variable = Struct("script variable",
    ascii_str32("script variable name"),
    ascii_str32("exposed parameter name"),
    SIZE=80
    )

effect = Struct("effect",
    dependency_os("effect", "efpg"),
    ascii_str32("name"),
    reflexive("script variables", script_variable, 32),
    SIZE=72
    )

activation_control = Struct("activation control",
    BSEnum16("state",
        "initially active",
        "is in cutscene",
        "player is zoomed",
        "player is using a vehicle"
        ),
    BBool16("flags",
        "invert"
        ),
    SIZE=4
    )

effect_instance = Struct("effect instance",
    ascii_str32("name"),
    BSInt16("effect"),
    BSEnum16("render stage",
        "after bsp - before blur",
        "after blur - before alphad faces",
        "after alphad faces - before hud",
        "after hud - before menu",
        "after menu",
        ),
    QStruct("quad tesselation",
        BSInt16("x"), BSInt16("y"), ORIENT="h"
        ),
    QStruct("x screen bounds", INCLUDE=from_to, MIN=0.0, MAX=1.0),
    QStruct("y screen bounds", INCLUDE=from_to, MIN=0.0, MAX=1.0),

    Pad(12),
    BSEnum16("activation operation",
        "all",
        "any"
        ),

    Pad(6),
    reflexive("activation controls", activation_control, 8),

    SIZE=116
    )

efpc_body = Struct("tagdata",
    Pad(12),
    # since there APPEARS to be a reflexive in the tag, but it
    # doesnt show up in Guerilla, I'm gonna turn it into padding
    # and leave this as a reminder that a reflexive might exist.
    #reflexive("unknown", void_desc, 0),
    Pad(12),
    reflexive("effects", effect, 32),
    reflexive("effect instances", effect_instance, 32),
    SIZE=48
    )

def get():
    return efpc_def

efpc_def = TagDef("efpc",
    blam_header_os('efpc'),
    efpc_body,

    ext=".effect_postprocess_collection", endian=">"
    )
