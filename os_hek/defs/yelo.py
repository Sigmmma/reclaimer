from ...common_descs import *
from ...hek.defs.objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

build_info = Struct("build info",
    Pad(2),
    SEnum16("build stage",
        "ship",
        "alpha",
        "beta",
        "delta",
        "epsilon",
        "release",
        ),
    SInt32("revision"),
    SIZE=48
    )

scripted_ui_widget = Struct("scripted ui widget",
    ascii_str32("name"),
    dependency_os("definition", "DeLa"),
    SIZE=76
    )

parameter = Struct("parameter",
    SEnum16("type", *script_object_types),
    SIZE=2
    )

new_function = Struct("new function",
    ascii_str32("name1"),
    ascii_str32("name2"),
    SInt16("override index"),
    SEnum16("return type", *script_object_types),
    reflexive("parameters", parameter),
    SIZE=80
    )

new_global = Struct("new global",
    ascii_str32("name1"),
    ascii_str32("name2"),
    SInt16("override index"),
    SEnum16("type", *script_object_types),
    SIZE=68
    )

yelo_scripting = Struct("yelo scripting",
    reflexive("new functions", new_function,
        DYN_NAME_PATH='.name1'),
    reflexive("new globals", new_global,
        DYN_NAME_PATH='.name1'),
    SIZE=24
    )

yelo_body = Struct("tagdata",
    SInt16("version"),
    Bool16("flags",
        "dont fix ui game globals",
        "game updates ignore player pvs hack",
        ),
    dependency_os("yelo globals", "gelo"),
    dependency_os("globals override", "matg"),
    dependency_os("scenario explicit references", "tagc"),
    reflexive("build info", build_info, 1),

    Pad(40),
    reflexive("scripted ui widgets", scripted_ui_widget, 128,
        DYN_NAME_PATH='.name'),

    Pad(16),
    # Physics
    Float("gravity scale",      MIN=0.0, MAX=2.0, SIDETIP="[0,2]"),
    Float("player speed scale", MIN=0.0, MAX=6.0, SIDETIP="[0,6]"),

    Pad(44),
    Bool32("gameplay model",
        "prohibit multi-team vehicles",
        ),

    Pad(20),
    reflexive("yelo scripting", yelo_scripting, 1),
    Pad(12),#reflexive("unknown", void_desc),

    SIZE=312
    )

def get():
    return yelo_def

yelo_def = TagDef("yelo",
    blam_header_os('yelo', 2),
    yelo_body,

    ext=".project_yellow", endian=">", tag_cls=HekTag
    )
