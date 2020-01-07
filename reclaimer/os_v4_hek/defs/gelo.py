#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from .yelo import *

gelo_body = Struct("tagdata",
    SInt16("version", DEFAULT=2),
    Bool16("flags",
        "hide_health_when_zoomed",
        "hide_shield_when_zoomed",
        "hide_motion_sensor_when_zoomed",
        "force_game_to_use_stun_jumping_penalty"
        ),
    SInt32("base_address"),
    ascii_str32("mod_name"),
    dependency_os("global_explicit_references", "tagc"),
    #dependency_os("chokin_victim_globals", "gelc"),
    Pad(16),  # removed_chokin_victim_globals

    Pad(16),
    Pad(12), #reflexive("unknown1", void_desc),
    Pad(52),
    reflexive("scripted_ui_widgets", scripted_ui_widget, 128),

    Pad(12), #reflexive("unknown2", void_desc),
    Pad(20),
    reflexive("yelo_scripting", yelo_scripting, 1),

    SIZE=288
    )

def get():
    return gelo_def

gelo_def = TagDef("gelo",
    blam_header_os('gelo', 2),
    gelo_body,

    ext=".project_yellow_globals", endian=">", tag_cls=HekTag
    )
