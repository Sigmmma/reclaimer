#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from ...hek.defs.objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

build_info = Struct("build_info",
    Pad(2),
    SEnum16("build_stage",
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

scripted_ui_widget = Struct("scripted_ui_widget",
    ascii_str32("name"),
    dependency_os("definition", "DeLa"),
    SIZE=76
    )

parameter = Struct("parameter",
    SEnum16("type", *script_object_types),
    SIZE=2
    )

new_function = Struct("new_function",
    ascii_str32("name1"),
    ascii_str32("name2"),
    SInt16("override_index"),
    SEnum16("return_type", *script_object_types),
    reflexive("parameters", parameter, 32),
    SIZE=80
    )

new_global = Struct("new_global",
    ascii_str32("name1"),
    ascii_str32("name2"),
    SInt16("override_index"),
    SEnum16("type", *script_object_types),
    SIZE=68
    )

yelo_scripting = Struct("yelo_scripting",
    reflexive("new_functions", new_function, 464,
        DYN_NAME_PATH='.name1'),
    reflexive("new_globals", new_global, 880,
        DYN_NAME_PATH='.name1'),
    SIZE=24
    )

yelo_body = Struct("tagdata",
    SInt16("version"),
    Bool16("flags",
        "dont_fix_ui_game_globals",
        "game_updates_ignore_player_pvs_hack",
        ),
    dependency_os("yelo_globals", "gelo"),
    dependency_os("globals_override", "matg"),
    dependency_os("scenario_explicit_references", "tagc"),
    reflexive("build_info", build_info, 1),

    Pad(40),
    reflexive("scripted_ui_widgets", scripted_ui_widget, 128,
        DYN_NAME_PATH='.name'),

    Pad(16),
    # Physics
    Float("gravity_scale",      MIN=0.0, MAX=2.0, SIDETIP="[0,2]"),
    Float("player_speed_scale", MIN=0.0, MAX=6.0, SIDETIP="[0,6]"),

    Pad(44),
    Bool32("gameplay_model",
        "prohibit_multi_team_vehicles",
        ),

    Pad(20),
    reflexive("yelo_scripting", yelo_scripting, 1),
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
