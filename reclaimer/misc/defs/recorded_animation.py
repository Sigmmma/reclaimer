#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from supyr_struct.field_types import *
from supyr_struct.defs.tag_def import TagDef


def has_next_event(rawdata=None, **kwargs):
    try:
        return bool(rawdata.peek(1))
    except AttributeError:
        return False


def parameter_case(parent=None, **kwargs):
    function = parent.event_function.function.enum_name
    if function == "update_animation_state":
        return "animation_state"

    elif function == "update_aim_speed":
        return "aim_speed"

    elif function == "update_control":
        return "control_flags"

    elif function in "update_weapon_index":
        return "short"

    elif function == "update_velocity":
        return "float_xy"

    elif function in (
            "set_facing", "set_aim", "set_facing_aim", "set_head",
            "set_facing_head", "set_head_aim", "set_all"
            ):
        return "byte_xy"

    elif function == "unknown2":
        return "short_xy"


byte_xy = QStruct("",
    SInt8("x"),
    SInt8("y"),
    ORIENT="h"
    )

short_xy = QStruct("",
    SInt16("x"),
    SInt16("y"),
    ORIENT="h"
    )

float_xy = QStruct("",
    Float("x"),
    Float("y"),
    ORIENT="h"
    )

float_xyz = QStruct("",
    Float("x"),
    Float("y"),
    Float("z"),
    ORIENT="h"
    )

event_function = BitStruct("event_function",
    UBitEnum("size",
        "instant",
        "tick",
        "byte",
        "short",
        SIZE=2
        ),
    UBitEnum("function",
        {"NAME": "end", "VALUE": 1},
        "update_animation_state",
        "update_aim_speed",
        "update_control",
        "update_weapon_index",
        "update_velocity",

        "unknown1",

        "set_facing",
        "set_aim",
        "set_facing_aim",
        "set_head",
        "set_facing_head",
        "set_head_aim",
        "set_all",

        "unused1",
        "unused2",
        "unused3",
        "unused4",
        "unused5",
        "unused6",
        "unused7",

        "unknown2",
        SIZE=6
        ),
    SIZE=1
    )

animation_state = UEnum8("animation_state",
    "sleep",
    "alert1",
    "alert2",
    "stand1",
    "stand2",
    "flee",
    "flaming",
    )

aim_speed = UEnum8("aim_speed",
    "alert",
    "relaxed",
    )

control_flags = Bool16("control_flags",
    # to set to standing, unset all flags
    "crouch",
    "jump",
    "user1",
    "user2",
    "light",
    "lock_facing",
    "action",
    "melee",
    "vector_desync",
    "walk",
    "reload",
    "primary_trigger",
    "secondary_trigger",
    "grenade",
    "exchange",
    )

event = Container("event",
    event_function,
    Switch("time",
        CASES={
            "byte"  : QStruct("data", UInt8("value")),
            "short" : QStruct("data", UInt16("value")),
            },
        CASE=".event_function.size.enum_name"
        ),
    Switch("parameters",
        CASE=parameter_case,
        CASES={
            "aim_speed"       : Struct("data", aim_speed),
            "control_flags"   : Struct("data", control_flags),
            "animation_state" : Struct("data", animation_state),
            "short"    : QStruct("data", SInt16("value")),
            "byte_xy"  : QStruct("data", INCLUDE=byte_xy),
            "short_xy" : QStruct("data", INCLUDE=short_xy),
            "float_xy" : QStruct("data", INCLUDE=float_xy),
            },
        )
    )

events = WhileArray("events",
    SUB_STRUCT=event,
    CASE=has_next_event
    )

r_a_stream_header_v0 = Struct("r_a_stream_header_v0",
    animation_state,
    aim_speed,
    control_flags,
    SInt16("weapon_index",  DEFAULT=-1),
    SInt16("grenade_index", DEFAULT=-1),

    QStruct("velocity", INCLUDE=float_xy),
    QStruct("facing",   INCLUDE=float_xyz),
    QStruct("aiming",   INCLUDE=float_xyz),
    QStruct("looking",  INCLUDE=float_xyz),

    QStruct("init_facing_displacement",  INCLUDE=short_xy),
    QStruct("init_aiming_displacement",  INCLUDE=short_xy),
    QStruct("init_looking_displacement", INCLUDE=short_xy),
    SIZE=64
    )

r_a_stream_header_v3 = Struct("r_a_stream_header_v3",
    animation_state,
    aim_speed,
    control_flags,
    SInt16("weapon_index",  DEFAULT=-1),
    SInt16("grenade_index", DEFAULT=-1),

    QStruct("velocity", INCLUDE=float_xy),
    QStruct("facing",   INCLUDE=float_xyz),
    QStruct("aiming",   INCLUDE=float_xyz),
    QStruct("looking",  INCLUDE=float_xyz),

    QStruct("unknown",
        SInt16("unknown1"),
        SInt16("unknown2"),
        SInt16("unknown3"),
        ORIENT="h",
        ),

    QStruct("init_facing_displacement",  INCLUDE=short_xy),
    QStruct("init_aiming_displacement",  INCLUDE=short_xy),
    QStruct("init_looking_displacement", INCLUDE=short_xy),
    SIZE=70
    )

r_a_stream_header_v4 = Struct("r_a_stream_header_v4",
    animation_state,
    aim_speed,
    control_flags,
    SInt16("weapon_index",  DEFAULT=-1),
    SInt16("grenade_index", DEFAULT=-1),

    QStruct("velocity", INCLUDE=float_xy),
    QStruct("facing",   INCLUDE=float_xyz),
    QStruct("aiming",   INCLUDE=float_xyz),
    QStruct("looking",  INCLUDE=float_xyz),

    QStruct("unknown",
        SInt16("unknown1"),
        SInt16("unknown2"),
        SInt16("unknown3"),
        SInt16("unknown4"),
        ORIENT="h",
        ),

    QStruct("init_facing_displacement",  INCLUDE=short_xy),
    QStruct("init_aiming_displacement",  INCLUDE=short_xy),
    QStruct("init_looking_displacement", INCLUDE=short_xy),
    SIZE=72
    )


def get():
    return r_a_stream_v0_def, r_a_stream_v3_def, r_a_stream_v4_def


r_a_stream_v0_def = TagDef("r_a_stream_v0",
    r_a_stream_header_v0,
    events,
    endian="<"
    )

r_a_stream_v3_def = TagDef("r_a_stream_v3",
    r_a_stream_header_v3,
    events,
    endian="<"
    )

r_a_stream_v4_def = TagDef("r_a_stream_v4",
    r_a_stream_header_v4,
    events,
    endian="<"
    )
