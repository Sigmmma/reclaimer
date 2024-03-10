#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from math import pi
from supyr_struct.field_types import *
from supyr_struct.defs.tag_def import TagDef
from reclaimer.common_descs import *

import traceback

# Faster than if/elif chain
FUNCTION_MAP = {
    "end_anim"                  : None,
    "set_anim_state"            : "anim_state",
    "set_aim_speed"             : "aim_speed",
    "set_control_flags"         : "control_flags",
    "set_weapon_index"          : "weapon_index",
    "set_throttle"              : "throttle",
    "set_face_char"             : "angle_delta_byte",
    "set_aim_char"              : "angle_delta_byte",
    "set_face_aim_char"         : "angle_delta_byte",
    "set_look_char"             : "angle_delta_byte",
    "set_face_look_char"        : "angle_delta_byte",
    "set_aim_look_char"         : "angle_delta_byte",
    "set_face_aim_look_char"    : "angle_delta_byte",
    "set_face_short"            : "angle_delta_short",
    "set_aim_short"             : "angle_delta_short",
    "set_face_aim_short"        : "angle_delta_short",
    "set_look_short"            : "angle_delta_short",
    "set_face_look_short"       : "angle_delta_short",
    "set_aim_look_short"        : "angle_delta_short",
    "set_face_aim_look_short"   : "angle_delta_short",
    }
ANGLE_DELTA_SCALE = pi/1000


def build_r_a_stream_block(version, rawdata, simple=False):
    v0_def = r_a_stream_v0_simple_def if simple else r_a_stream_v0_def
    v3_def = r_a_stream_v3_simple_def if simple else r_a_stream_v3_def
    v4_def = r_a_stream_v4_simple_def if simple else r_a_stream_v4_def
    return (
        v0_def.build(rawdata=rawdata) if version == 0 else
        v3_def.build(rawdata=rawdata) if version == 3 else
        v4_def.build(rawdata=rawdata) if version == 4 else
        None
        )


def has_next_event(parent=None, rawdata=None, **kwargs):
    try:        
        # Proper case
        if len(parent) and parent[-1].event_function.function.enum_name == "end_anim":
            return False
        # End of stream reached before end packet read from stream
        elif len(rawdata.peek(1)) < 1:
            print("Warning: End of data reached before an end packet was read. Tag may be corrupt!")
            return False
        return True
    except AttributeError:
        return False


def time_delta_case(parent=None, **kwargs):
    return parent.event_function.size.enum_name if parent else None


def parameter_case(parent=None, **kwargs):    
    func_name = parent.event_function.function.enum_name if parent else None
    return FUNCTION_MAP.get(func_name, None)


def get_event_summary_string(parent=None, **kw):
    if parent is None:
        return None

    try:
        param_strs = []

        time_type  = parent.event_function.time_delay_type.enum_name
        func_type  = parent.event_function.function.enum_name
        param_strs.append(
            "[%.3fs] " % ((
                1 if time_type == "tick"    else
                0 if time_type == "instant" else
                parent.time.delay
                ) / 30)
            )

        if func_type != "end_anim":
            param_strs.append("%s {" % func_type.\
                replace("char", "").replace("short", "").strip("_")
                )
        else:
            param_strs.append("end_anim")

        params_desc = ""
        params = parent.parameters
        if func_type == "set_anim_state":
            params_desc = "%s}" % params.animation_state.enum_name
        elif func_type == "set_aim_speed":
            params_desc = "%s}" % params.aim_speed.enum_name
        elif func_type == "set_control_flags":
            flags = params.control_flags
            params_desc = "%s}" % "|".join(
                name.split("_")[0] for name in flags.NAME_MAP
                if flags[name]
                ) or "None"
        elif func_type == "set_weapon_index":
            params_desc = "%s}" % params.weapon_index
        elif func_type != "end_anim":
            scale = 1 if func_type == "set_throttle" else ANGLE_DELTA_SCALE

            params_desc = ", ".join(
                "%.3f" % (
                    params[name] * scale
                    )
                for name in params.NAME_MAP
                ) + "}"
        
        if params_desc:
            param_strs.append(params_desc)

        parent.summary = "".join(param_strs)
    except Exception:
        print(traceback.format_exc())


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
    "crouch",
    "jump",
    "user1",
    "user2",
    "flashlight",
    "lock_facing",
    "action",
    "melee",
    "unlock_facing",
    "walk",
    "reload",
    "primary_trigger",
    "secondary_trigger",
    "grenade",
    "exchange",
    )

angle_delta_byte = QStruct("",
    SInt8("x"), SInt8("y"), ORIENT="h"
    )

angle_delta_short = QStruct("",
    SInt16("x"), SInt16("y"), ORIENT="h"
    )

event_function = BitStruct("event_function",
    UBitEnum("time_delay_type",
        "instant",
        "tick",
        "byte",                                 # Suggested edit: The code asserts 1 < time_delta < UNSIGNED_CHAR_MAX
        "short",                                # Suggested edit: The code asserts UNSIGNED_CHAR_MAX < time_delta
        SIZE=2
        ),
    UBitEnum("function",                        # Suggested edit: The code asserts this to being n < NUMBEROF(apply_funcs) [0x5b]
        ("end_anim", 1),                # 1
        "set_anim_state",               # 2
        "set_aim_speed",                # 3
        "set_control_flags",            # 4
        "set_weapon_index",             # 5
        "set_throttle",                 # 6
        # start of char difference      # 7      For future mgmt: This isn't skipped, we just precalculated the flags below
        ("set_face_char", 8),           # 8
        "set_aim_char",                 # 9
        "set_face_aim_char",            # 10
        "set_look_char",                # 11
        "set_face_look_char",           # 12
        "set_aim_look_char",            # 13
        "set_face_aim_look_char",       # 14
        # start of short difference     # 15     For future mgmt: This isn't skipped, we just precalculated the flags below
        ("set_face_short", 16),         # 16
        "set_aim_short",                # 17
        "set_face_aim_short",           # 18
        "set_look_short",               # 19
        "set_face_look_short",          # 20
        "set_aim_look_short",           # 21
        "set_face_aim_look_short",      # 22
        SIZE=6
        ),
    SIZE=1, HIDE_TITLE=True
    )

event_fields = (
    event_function,
    Switch("time",
        CASES={
            "byte"  : QStruct("time", UInt8("delay")),      # Renamed to "delay" as I feel it better represents what's going on here
            "short" : QStruct("time", UInt16("delay")),
            },
        CASE=".event_function.time_delay_type.enum_name"
        ),
    Switch("parameters",
        CASES={
            "aim_speed"         : Struct("aim_speed",       aim_speed),
            "control_flags"     : Struct("control_flags",   control_flags),
            "anim_state"        : Struct("anim_state",      animation_state),
            "weapon_index"      : QStruct("weapon_index",   SInt16("weapon_index")),
            "throttle"          : QStruct("throttle",       INCLUDE=xy_float),
            "angle_delta_byte"  : QStruct("angle_delta",    INCLUDE=angle_delta_byte),
            "angle_delta_short" : QStruct("angle_delta",    INCLUDE=angle_delta_short),
            },
        CASE=parameter_case,
        )
    )

event = Container("event",
    *event_fields,
    # NOTE: summary is after event so the event data is already parsed
    Computed("summary",
        COMPUTE_READ=get_event_summary_string, WIDGET_WIDTH=60
        )
    )

event_simple = Container("event",
    *event_fields,
    )

events_simple = WhileArray("events", 
    SUB_STRUCT=event_simple, CASE=has_next_event
    )

events = WhileArray("events",
    SUB_STRUCT=event, CASE=has_next_event,
    DYN_NAME_PATH=".summary", WIDGET=DynamicArrayFrame
    )

# Suggested edit: the "stream_headers" versions are actually "control" versions internally
r_a_stream_header_fields_0 = (
    animation_state,
    aim_speed,
    control_flags,
    # This is weird and I hate it. Still trying to figure out what is going on here
    SInt8("unknown_01",    DEFAULT=-1),
    SInt8("weapon_index",  DEFAULT=-1, MIN=-1, MAX=3),        # clamped[-1,4)

    UInt8("unknown_02"),
    UInt8("unknown_03"),

    QStruct("velocity",       INCLUDE=xy_float),
    QStruct("facing_vector",  INCLUDE=xyz_float), #, EDITABLE=False), # For now I'm gonna keep editable
    QStruct("aiming_vector",  INCLUDE=xyz_float), #, EDITABLE=False),
    QStruct("looking_vector", INCLUDE=xyz_float), #, EDITABLE=False),
    )

r_a_stream_header_fields_1 = (
    QStruct("facing",  INCLUDE=angle_delta_short),
    QStruct("aiming",  INCLUDE=angle_delta_short),
    QStruct("looking", INCLUDE=angle_delta_short),
    )

r_a_stream_header_v0 = Struct("r_a_stream_header_v0",
    *r_a_stream_header_fields_0,
    *r_a_stream_header_fields_1,
    SIZE=64
    )

r_a_stream_header_v3 = Struct("r_a_stream_header_v3",
    *r_a_stream_header_fields_0,

    SInt16("unknown_04"),
    SInt16("unknown_05"),
    SInt16("grenade_index", MIN=0, MAX=3),

    *r_a_stream_header_fields_1,
    SIZE=70
    )

r_a_stream_header_v4 = Struct("r_a_stream_header_v4",
    *r_a_stream_header_fields_0,

    SInt16("unknown_04"),
    SInt16("unknown_05"),
    SInt16("grenade_index", MIN=0, MAX=3),    # Must be -1 < n < 4
    SInt16("zoom_level",    MIN=0),       # Must be positive

    *r_a_stream_header_fields_1,
    SIZE=72
    )

r_a_stream_v0 = Container("r_a_stream", r_a_stream_header_v0, events)
r_a_stream_v3 = Container("r_a_stream", r_a_stream_header_v3, events)
r_a_stream_v4 = Container("r_a_stream", r_a_stream_header_v4, events)

r_a_stream_v0_def = BlockDef(r_a_stream_v0)
r_a_stream_v3_def = BlockDef(r_a_stream_v3)
r_a_stream_v4_def = BlockDef(r_a_stream_v4)

r_a_stream_v0_simple_def = BlockDef("r_a_stream", r_a_stream_header_v0, events_simple)
r_a_stream_v3_simple_def = BlockDef("r_a_stream", r_a_stream_header_v3, events_simple)
r_a_stream_v4_simple_def = BlockDef("r_a_stream", r_a_stream_header_v4, events_simple)

r_a_stream_v0_tagdef = TagDef(r_a_stream_v0, endian="<")
r_a_stream_v3_tagdef = TagDef(r_a_stream_v3, endian="<")
r_a_stream_v4_tagdef = TagDef(r_a_stream_v4, endian="<")

def get():
    return r_a_stream_v0_tagdef, r_a_stream_v3_tagdef, r_a_stream_v4_tagdef
