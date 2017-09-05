from ...common_descs import *
from ...hek.defs.objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

script_variable = Struct("script variable",
    ascii_str32("script variable name"),
    ascii_str32("exposed parameter name"),
    SIZE=80
    )

effect = Struct("effect",
    dependency_os("effect", "efpg"),
    ascii_str32("name"),
    reflexive("script variables", script_variable, 32,
        DYN_NAME_PATH='.script_variable_name'),
    SIZE=72
    )

activation_control = Struct("activation control",
    SEnum16("state",
        "initially active",
        "is in cutscene",
        "player is zoomed",
        "player is using a vehicle"
        ),
    Bool16("flags",
        "invert"
        ),
    SIZE=4
    )

effect_instance = Struct("effect instance",
    ascii_str32("name"),
    dyn_senum16("effect",
        DYN_NAME_PATH="tagdata.effects.STEPTREE[DYN_I].effect.filepath"),
    SEnum16("render stage",
        "after bsp - before blur",
        "after blur - before alphad faces",
        "after alphad faces - before hud",
        "after hud - before menu",
        "after menu",
        ),
    QStruct("quad tesselation",
        SInt16("x"), SInt16("y"), ORIENT="h"
        ),
    from_to_zero_to_one("x screen bounds"),
    from_to_zero_to_one("y screen bounds"),

    Pad(12),
    SEnum16("activation operation",
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
    reflexive("effects", effect, 32,
        DYN_NAME_PATH='.name'),
    reflexive("effect instances", effect_instance, 32,
        DYN_NAME_PATH='.name'),
    SIZE=48
    )

def get():
    return efpc_def

efpc_def = TagDef("efpc",
    blam_header_os('efpc'),
    efpc_body,

    ext=".effect_postprocess_collection", endian=">", tag_cls=HekTag
    )
