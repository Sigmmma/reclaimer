#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

def object_reference(name, *args, **kwargs):
    "Macro to cut down on a lot of code"
    block_name = kwargs.pop('block_name', name + 's').replace(' ', '_')

    dyn_type_path = ".....%s_palette.STEPTREE[DYN_I].name.filepath" % block_name
    return Struct(name,
        dyn_senum16('type', DYN_NAME_PATH=dyn_type_path),
        dyn_senum16('name',
            DYN_NAME_PATH=".....object_names.STEPTREE[DYN_I].name"),
        Bool16('not_placed',
            "automatically",
            "on_easy",
            "on_normal",
            "on_hard",
            ),
        SInt16('desired_permutation'),
        QStruct("position", INCLUDE=xyz_float),
        ypr_float_rad("rotation"),
        *args,
        **kwargs
        )

def object_swatch(name, def_id, size=48):
    "Macro to cut down on a lot of code"
    return Struct(name,
        dependency("name", def_id),
        SIZE=size
        )

fl_float_xyz = QStruct("",
    FlFloat("x"),
    FlFloat("y"),
    FlFloat("z"),
    ORIENT="h"
    )

stance_flags = FlBool16("stance",
    "walk",
    "look_only",
    "primary_fire",
    "secondary_fire",
    "jump",
    "crouch",
    "melee",
    "flashlight",
    "action1",
    "action2",
    "action_hold",
    )

unit_control_packet = Struct("unit_control_packet",

    )

r_a_stream_header = Struct("r_a_stream_header",
    UInt8("move_index", DEFAULT=3, MAX=6),
    UInt8("bool_index"),
    stance_flags,
    FlSInt16("weapon", DEFAULT=-1),
    QStruct("speed", FlFloat("x"), FlFloat("y"), ORIENT="h"),
    QStruct("feet", INCLUDE=fl_float_xyz),
    QStruct("body", INCLUDE=fl_float_xyz),
    QStruct("head", INCLUDE=fl_float_xyz),
    QStruct("change", INCLUDE=fl_float_xyz),
    FlUInt16("unknown1"),
    FlUInt16("unknown2"),
    FlUInt16("unknown3", DEFAULT=0xFFFF),
    FlUInt16("unknown4", DEFAULT=0xFFFF),
    SIZE=60
    )

device_flags = (
    "initially_open",  # value of 1.0
    "initially_off",  # value of 0.0
    "can_change_only_once",
    "position_reversed",
    "not_usable_from_any_side"
    )

location_types = (
    "none",
    "ctf",
    "slayer",
    "oddball",
    "king",
    "race",
    "terminator",
    "stub",
    "ignored1",
    "ignored2",
    "ignored3",
    "ignored4",
    "all_games",
    "all_games_except_ctf",
    "all_games_except_ctf_and_race"
    )

group_indices = tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

squad_states = (
    "none",
    "sleeping",
    "alert",
    "moving_repeat_same_position",
    "moving_loop",
    "moving_loop_back_and_forth",
    "moving_loop_randomly",
    "moving_randomly",
    "guarding",
    "guarding_at_position",
    "searching",
    "fleeing"
    )

maneuver_when_states = (
    "never",
    {NAME: "strength_at_75_percent", GUI_NAME: "< 75% strength"},
    {NAME: "strength_at_50_percent", GUI_NAME: "< 50% strength"},
    {NAME: "strength_at_25_percent", GUI_NAME: "< 25% strength"},
    "anybody_dead",
    {NAME: "dead_at_25_percent", GUI_NAME: "25% dead"},
    {NAME: "dead_at_50_percent", GUI_NAME: "50% dead"},
    {NAME: "dead_at_75_percent", GUI_NAME: "75% dead"},
    "all_but_one_dead",
    "all_dead"
    )

atom_types = (
    "pause",
    "goto",
    "goto_and_face",
    "move_in_direction",
    "look",
    "animation_mode",
    "crouch",
    "shoot",
    "grenade",
    "vehicle",
    "running_jump",
    "targeted_jump",
    "script",
    "animate",
    "recording",
    "action",
    "vocalize",
    "targeting",
    "initiative",
    "wait",
    "loop",
    "die",
    "move_immediate",
    "look_random",
    "look_player",
    "look_object",
    "set_radius",
    "teleport"
    )


sky = Struct("sky",
    dependency("sky", "sky "),
    SIZE=16
    )

child_scenario = Struct("child_scenario",
    dependency("child_scenario", "scnr"),
    SIZE=32
    )

function = Struct('function',
    Bool32('flags',
        'scripted',
        'invert',
        'additive',
        'always_active',
        ),
    ascii_str32('name'),
    float_sec('period'),  # seconds
    dyn_senum16('scale_period_by', DYN_NAME_PATH="..[DYN_I].name"),
    SEnum16('function', *animation_functions),
    dyn_senum16('scale_function_by', DYN_NAME_PATH="..[DYN_I].name"),
    SEnum16('wobble_function', *animation_functions),
    float_sec('wobble_period'),  # seconds
    Float('wobble_magnitude', SIDETIP="%"),  # percent
    Float('square_wave_threshold'),
    SInt16('step_count'),
    SEnum16('map_to', *fade_functions),
    SInt16('sawtooth_count'),

    Pad(2),
    dyn_senum16('scale_result_by', DYN_NAME_PATH="..[DYN_I].name"),
    SEnum16('bounds_mode',
        'clip',
        'clip_and_normalize',
        'scale_to_fit',
        ),
    QStruct('bounds', INCLUDE=from_to),

    Pad(6),
    dyn_senum16('turn_off_with', DYN_NAME_PATH="..[DYN_I].name"),

    SIZE=120
    )

comment = Struct("comment",
    QStruct("position", INCLUDE=xyz_float),
    Pad(16),
    rawtext_ref("comment_data", StrLatin1, max_size=16384),
    SIZE=48
    )

object_name = Struct("object_name",
    ascii_str32("name"),
    FlSEnum16("object_type",
        *((object_types[i], i - 1) for i in
          range(len(object_types))),
        VISIBLE=False, EDITABLE=False, DEFAULT=-1
        ),
    FlSInt16("reflexive_index", VISIBLE=False, EDITABLE=False),
    SIZE=36
    )

# Object references
scenery = object_reference("scenery", SIZE=72, block_name="sceneries")

biped = object_reference("biped",
    Pad(40),
    float_zero_to_one("body_vitality"),
    Bool32("flags",
        "dead",
        ),
    SIZE=120
    )

vehicle = object_reference("vehicle",
    Pad(40),
    float_zero_to_one("body_vitality"),
    Bool32("flags",
        "dead",
        ),

    Pad(8),
    SInt8("multiplayer_team_index"),
    Pad(1),
    Bool16("multiplayer_spawn_flags",
        "slayer_default",
        "ctf_default",
        "king_default",
        "oddball_default",
        #"unused1",
        #"unused2",
        #"unused3",
        #"unused4",
        ("slayer_allowed", 1<<8),
        ("ctf_allowed", 1<<9),
        ("king_allowed", 1<<10),
        ("oddball_allowed", 1<<11),
        #"unused5",
        #"unused6",
        #"unused7",
        #"unused8",
        ),
    SIZE=120
    )

equipment = object_reference("equipment",
    Pad(2),
    Bool16("flags",
        "initially_at_rest",
        "obsolete",
        {NAME: "can_accelerate", GUI_NAME:"moves due to explosions"},
        ),
    SIZE=40
    )

weapon = object_reference("weapon",
    Pad(40),
    SInt16("rounds_left"),
    SInt16("rounds_loaded"),
    Bool16("flags",
        "initially_at_rest",
        "obsolete",
        {NAME: "can_accelerate", GUI_NAME:"moves due to explosions"},
        ),
    SIZE=92
    )

device_group = Struct("device_group",
    ascii_str32("name"),
    float_zero_to_one("initial_value"),
    Bool32("flags",
        "can_change_only_once"
        ),
    SIZE=52
    )

machine = object_reference("machine",
    Pad(8),
    dyn_senum16("power_group",
        DYN_NAME_PATH=".....device_groups.STEPTREE[DYN_I].name"),
    dyn_senum16("position_group",
        DYN_NAME_PATH=".....device_groups.STEPTREE[DYN_I].name"),
    Bool32("flags", *device_flags),
    Bool32("more_flags",
        "does_not_operate_automatically",
        "one_sided",
        "never_appears_locked",
        "opened_by_melee_attack",
        ),
    SIZE=64
    )

control = object_reference("control",
    Pad(8),
    dyn_senum16("power_group",
        DYN_NAME_PATH=".....device_groups.STEPTREE[DYN_I].name"),
    dyn_senum16("position_group",
        DYN_NAME_PATH=".....device_groups.STEPTREE[DYN_I].name"),
    Bool32("flags", *device_flags),
    Bool32("more_flags",
        "usable_from_both_sides",
        ),
    SInt16("DONT_TOUCH_THIS"),  # why?
    SIZE=64
    )

light_fixture = object_reference("light_fixture",
    Pad(8),
    dyn_senum16("power_group",
        DYN_NAME_PATH=".....device_groups.STEPTREE[DYN_I].name"),
    dyn_senum16("position_group",
        DYN_NAME_PATH=".....device_groups.STEPTREE[DYN_I].name"),
    Bool32("flags", *device_flags),
    QStruct("color", INCLUDE=rgb_float),
    Float("intensity"),
    Float("falloff_angle"),  # radians
    Float("cutoff_angle"),  # radians
    SIZE=88
    )

sound_scenery = object_reference("sound_scenery", SIZE=40, block_name="sound_sceneries")

# Object swatches
scenery_swatch = object_swatch("scenery_swatch", "scen")
biped_swatch = object_swatch("biped_swatch", "bipd")
vehicle_swatch = object_swatch("vehicle_swatch", "vehi")
equipment_swatch = object_swatch("equipment_swatch", "eqip")
weapon_swatch = object_swatch("weapon_swatch", "weap")
machine_swatch = object_swatch("machine_swatch", "mach")
control_swatch = object_swatch("control_swatch", "ctrl")
light_fixture_swatch = object_swatch("light_fixture_swatch", "lifi")
sound_scenery_swatch = object_swatch("sound_scenery_swatch", "ssce")

player_starting_profile = Struct("player_starting_profile",
    ascii_str32("name"),
    float_zero_to_one("starting_health_modifier"),
    float_zero_to_one("starting_shield_modifier"),
    dependency("primary_weapon", "weap"),
    SInt16("primary_rounds_loaded"),
    SInt16("primary_rounds_total"),
    dependency("secondary_weapon", "weap"),
    SInt16("secondary_rounds_loaded"),
    SInt16("secondary_rounds_total"),
    SInt8("starting_frag_grenade_count", MIN=0),
    SInt8("starting_plasma_grenade_count", MIN=0),
    SIZE=104
    )

player_starting_location = Struct("player_starting_location",
    QStruct("position", INCLUDE=xyz_float),
    float_rad("facing"),  # radians
    SInt16("team_index"),
    dyn_senum16("bsp_index",
        DYN_NAME_PATH=".....structure_bsps.STEPTREE[DYN_I].structure_bsp.filepath"),
    SEnum16("type_0", *location_types),
    SEnum16("type_1", *location_types),
    SEnum16("type_2", *location_types),
    SEnum16("type_3", *location_types),
    SIZE=52
    )

player_starting_location2 = dict(player_starting_location)
player_starting_location2[3] = dyn_senum16("bsp_index",
        DYN_NAME_PATH=("........structure_bsps.STEPTREE"
                       "[DYN_I].structure_bsp.filepath")
        )

trigger_volume = Struct("trigger_volume",
    # if this unknown != 1, the trigger volume is disabled
    FlUInt16("unknown0", DEFAULT=1, EDITABLE=False, VISIBLE=False),
    Pad(2),
    ascii_str32("name"),
    BytesRaw("unknown1", SIZE=12, VISIBLE=False),
    QStruct("binormal", INCLUDE=ijk_float),
    QStruct("normal",   INCLUDE=ijk_float),
    QStruct("position", INCLUDE=xyz_float,
        TOOLTIP=("Volume sides extend in one direction from this position.\n"
                 "This position is the origin corner for the trigger volume.")),
    QStruct("sides",
        Float("w", TOOLTIP="Along local y axis"),
        Float("h", TOOLTIP="Along local z axis"),
        Float("l", TOOLTIP="Along local x axis"),
        ORIENT='h'
        ),
    SIZE=96,
    COMMENT=(
        "To make the trigger volumes rotation be zero, the normal and\n"
        "binormal should be (1, 0, 0) and (0, 1, 0) respectively.")
    )

recorded_animation = Struct("recorded_animation",
    ascii_str32("name"),
    SInt8("version"),
    SInt8("raw_animation_data"),
    SInt8("unit_control_data_version"),
    Pad(1),
    SInt16("length_of_animation", SIDETIP="ticks"),  # ticks
    Pad(6),
    rawdata_ref("recorded_animation_event_stream", max_size=2097152),
    SIZE=64
    )

netgame_flag = Struct("netgame_flag",
    QStruct("position", INCLUDE=xyz_float),
    float_rad("facing"),  # radians
    SEnum16("type",
        "ctf_flag",
        "ctf_vehicle",
        "oddball_ball_spawn",
        "race_track",
        "race_vehicle",
        "vegas_bank",
        "teleport_from",
        "teleport_to",
        "hill_flag",
        ),
    SInt16("team_index"),
    dependency("weapon_group", "itmc"),
    SIZE=148
    )

netgame_equipment = Struct("netgame_equipment",
    Bool32("flags",
        "levitate"
        ),
    SEnum16("type_0", *location_types),
    SEnum16("type_1", *location_types),
    SEnum16("type_2", *location_types),
    SEnum16("type_3", *location_types),
    SInt16("team_index"),
    SInt16("spawn_time", SIDETIP="seconds(0 = default)",
            UNIT_SCALE=sec_unit_scale),  # seconds

    Pad(48),
    QStruct("position", INCLUDE=xyz_float),
    float_rad("facing"),  # radians
    dependency("item_collection", "itmc"),
    SIZE=144
    )

starting_equipment = Struct("starting_equipment",
    Bool32("flags",
        "no_grenades",
        "plasma_grenades",
        ),
    SEnum16("type_0", *location_types),
    SEnum16("type_1", *location_types),
    SEnum16("type_2", *location_types),
    SEnum16("type_3", *location_types),

    Pad(48),
    dependency("item_collection_1", "itmc"),
    dependency("item_collection_2", "itmc"),
    dependency("item_collection_3", "itmc"),
    dependency("item_collection_4", "itmc"),
    dependency("item_collection_5", "itmc"),
    dependency("item_collection_6", "itmc"),
    SIZE=204
    )

bsp_switch_trigger_volume = Struct("bsp_switch_trigger_volume",
    dyn_senum16("trigger_volume",
        DYN_NAME_PATH=".....trigger_volumes.STEPTREE[DYN_I].name"),
    dyn_senum16("source",
        DYN_NAME_PATH=".....structure_bsps.STEPTREE[DYN_I].structure_bsp.filepath"),
    dyn_senum16("destination",
        DYN_NAME_PATH=".....structure_bsps.STEPTREE[DYN_I].structure_bsp.filepath"),
    FlUInt16("unknown", EDITABLE=False),
    SIZE=8
    )

decal = Struct("decal",
    dyn_senum16("decal_type",
        DYN_NAME_PATH=".....decals_palette.STEPTREE[DYN_I].name.filepath"),
    SInt8("yaw"),
    SInt8("pitch"),
    QStruct("position", INCLUDE=xyz_float),
    SIZE=16
    )

decal_swatch = object_swatch("decal_swatch", "deca", 16)
detail_object_collection_swatch = object_swatch(
    "detail_object_collection_swatch", "dobc")
actor_swatch = object_swatch("actor_swatch", "actv", 16)

ai_anim_reference = Struct("ai_animation_reference",
    ascii_str32("animation_name"),
    dependency("animation_graph", "antr"),
    SIZE=60
    )

ai_script_reference = Struct("ai_script_reference",
    ascii_str32("script_name"),
    SIZE=40
    )

ai_recording_reference = Struct("ai_recording_reference",
    ascii_str32("recording_name"),
    SIZE=40
    )

halo_script = Struct("script",
    ascii_str32("name", EDITABLE=False),
    SEnum16("type", *script_types),
    SEnum16("return_type", *script_object_types, EDITABLE=False),
    UInt32("root_expression_index", EDITABLE=False),
    Computed("decompiled_script", WIDGET=HaloScriptTextFrame),
    SIZE=92,
    )

halo_global = Struct("global",
    ascii_str32("name", EDITABLE=False),
    SEnum16("type", *script_object_types, EDITABLE=False),
    Pad(6),
    UInt32("initialization_expression_index", EDITABLE=False),
    Computed("decompiled_script", WIDGET=HaloScriptTextFrame),
    SIZE=92,
    )

reference = Struct("tag_reference",
    Pad(24),
    dependency("reference"),
    SIZE=40
    )

source_file = Struct("source_file",
    ascii_str32("source_name"),
    rawdata_ref("source", max_size=262144, widget=HaloScriptSourceFrame),
    SIZE=52
    )

cutscene_flag = Struct("cutscene_flag",
    Pad(4),
    ascii_str32("name"),
    QStruct("position", INCLUDE=xyz_float),
    yp_float_rad("facing"),  # radians
    SIZE=92
    )

cutscene_camera_point = Struct("cutscene_camera_point",
    Pad(4),
    ascii_str32("name"),
    Pad(4),
    QStruct("position", INCLUDE=xyz_float),
    ypr_float_rad("orientation"),  # radians
    float_rad("field_of_view"),  # radians
    SIZE=104
    )

cutscene_title = Struct("cutscene_title",
    Pad(4),
    ascii_str32("name"),
    Pad(4),
    QStruct("text_bounds",
        SInt16("t"), SInt16("l"), SInt16("b"), SInt16("r"),
        ORIENT='h',
        ),
    SInt16("string_index"),
    SEnum16("text_style",
        "plain",
        "bold",
        "italic",
        "condense",
        "underline",
        ),
    SEnum16("justification",
        "left",
        "right",
        "center",
        ),

    Pad(6),
    #QStruct("text_color", INCLUDE=argb_byte),
    #QStruct("shadow_color", INCLUDE=argb_byte),
    UInt32("text_color", INCLUDE=argb_uint32),
    UInt32("shadow_color", INCLUDE=argb_uint32),
    float_sec("fade_in_time"),  # seconds
    float_sec("up_time"),  # seconds
    float_sec("fade_out_time"),  # seconds
    SIZE=96
    )


move_position = Struct("move_position",
    QStruct("position", INCLUDE=xyz_float),
    float_rad("facing"),  # radians
    Float("weight"),
    from_to_sec("time"),
    dyn_senum16("animation",
        DYN_NAME_PATH="tagdata.ai_animation_references.STEPTREE[DYN_I].animation_name"),
    SInt8("sequence_id"),

    Pad(45),
    SInt32("surface_index"),
    SIZE=80
    )

actor_starting_location = Struct("starting_location",
    QStruct("position", INCLUDE=xyz_float),
    float_rad("facing"),  # radians
    Pad(2),
    SInt8("sequence_id"),
    Bool8("flags",
        "required",
        ),
    SEnum16("return_state",  *(dict(NAME=n, GUI_NAME=n) for n in squad_states)),
    SEnum16("initial_state", *(dict(NAME=n, GUI_NAME=n) for n in squad_states)),
    dyn_senum16("actor_type",
        DYN_NAME_PATH="tagdata.actors_palette.STEPTREE[DYN_I].name.filepath"),
    dyn_senum16("command_list",
        DYN_NAME_PATH="tagdata.command_lists.STEPTREE[DYN_I].name"),
    SIZE=28
    )

squad = Struct("squad",
    ascii_str32("name"),
    dyn_senum16("actor_type",
        DYN_NAME_PATH="tagdata.actors_palette.STEPTREE[DYN_I].name.filepath"),
    dyn_senum16("platoon",
        DYN_NAME_PATH=".....platoons.STEPTREE[DYN_I].name"),
    SEnum16("initial_state", *(dict(NAME=n, GUI_NAME=n) for n in squad_states)),
    SEnum16("return_state",  *(dict(NAME=n, GUI_NAME=n) for n in squad_states)),
    Bool32("flags",
        "unused",
        "never_search",
        "start_timer_immediately",
        "no_timer_delay_forever",
        "magic_sight_after_timer",
        "automatic_migration",
        ),
    SEnum16("unique_leader_type",
        "normal",
        "none",
        "random",
        "sgt_johnson",
        "sgt_lehto",
        ),

    Pad(32),
    dyn_senum16("maneuver_to_squad", DYN_NAME_PATH="..[DYN_I].name"),
    float_sec("squad_delay_time"),  # seconds
    Bool32("attacking", *group_indices),
    Bool32("attacking_search", *group_indices),
    Bool32("attacking_guard", *group_indices),
    Bool32("defending", *group_indices),
    Bool32("defending_search", *group_indices),
    Bool32("defending_guard", *group_indices),
    Bool32("pursuing", *group_indices),

    Pad(12),
    SInt16("normal_diff_count"),
    SInt16("insane_diff_count"),
    SEnum16("major_upgrade",
        "normal",
        "few",
        "many",
        "none",
        "all",
        ),
    Pad(2),

    SInt16("respawn_min_actors"),
    SInt16("respawn_max_actors"),
    SInt16("respawn_total"),
    Pad(2),

    from_to_sec("respawn_delay"),

    Pad(48),
    reflexive("move_positions", move_position, 31),
    reflexive("starting_locations", actor_starting_location, 31),
    SIZE=232
    )

platoon = Struct("platoon",
    ascii_str32("name"),
    Bool32("flags",
        "flee_when_maneuvering",
        "say_advancing_when_maneuvering",
        "start_in_defending_state",
        ),

    Pad(12),
    SEnum16("change_attacking_defending_state", *maneuver_when_states),
    dyn_senum16("change_happens_to", DYN_NAME_PATH="..[DYN_I].name"),

    Pad(8),
    SEnum16("maneuver_when", *maneuver_when_states),
    dyn_senum16("maneuver_happens_to", DYN_NAME_PATH="..[DYN_I].name"),
    SIZE=172
    )

firing_position = Struct("firing_position",
    QStruct("position", INCLUDE=xyz_float),
    SEnum16("group_index", *group_indices),
    FlUInt16('bsp_cluster', VISIBLE=False),  # calculated on map compile
    Pad(4),
    FlSInt32('bsp_surface', VISIBLE=False),  # calculated on map compile
    SIZE=24
    )

encounter = Struct("encounter",
    ascii_str32("name"),
    Bool32("flags",
        "not_initially_created",
        "respawn_enabled",
        "initially_blind",
        "initially_deaf",
        "initially_braindead",
        "firing_positions_are_3d",
        "manual_bsp_index_specified",
        ),
    SEnum16("team_index",
        {NAME: "default",  GUI_NAME: "0 / default_by_unit"},
        {NAME: "player",   GUI_NAME: "1 / player"},
        {NAME: "human",    GUI_NAME: "2 / human"},
        {NAME: "covenant", GUI_NAME: "3 / covenant"},
        {NAME: "flood",    GUI_NAME: "4 / flood"},
        {NAME: "sentinel", GUI_NAME: "5 / sentinel"},
        {NAME: "unused6",  GUI_NAME: "6 / unused6"},
        {NAME: "unused7",  GUI_NAME: "7 / unused7"},
        {NAME: "unused8",  GUI_NAME: "8 / unused8"},
        {NAME: "unused9",  GUI_NAME: "9 / unused9"}
        ),
    SInt16('unknown', VISIBLE=False),
    SEnum16("search_behavior",
        "normal",
        "never",
        "tenacious"
        ),
    dyn_senum16("manual_bsp_index",
        DYN_NAME_PATH=".....structure_bsps.STEPTREE[DYN_I].structure_bsp.filepath"),
    from_to_sec("respawn_delay"),

    Pad(74),
    FlSInt16('bsp_index', VISIBLE=False),  # calculated on map compile
    reflexive("squads", squad, 64),
    reflexive("platoons", platoon, 32, DYN_NAME_PATH='.name'),
    reflexive("firing_positions", firing_position, 512),
    reflexive("player_starting_locations", player_starting_location2, 256),

    SIZE=176
    )

command = Struct("command",
    SEnum16("atom_type", *atom_types),
    SInt16("atom_modifier"),
    Float("parameter_1"),
    Float("parameter_2"),
    dyn_senum16("point_1", DYN_NAME_PATH=".....points.STEPTREE[DYN_I]"),
    dyn_senum16("point_2", DYN_NAME_PATH=".....points.STEPTREE[DYN_I]"),
    dyn_senum16("animation",
        DYN_NAME_PATH="tagdata.ai_animation_references.STEPTREE[DYN_I].animation_name"),
    dyn_senum16("script",
        DYN_NAME_PATH="tagdata.scripts.STEPTREE[DYN_I].name"),
    dyn_senum16("recording",
        DYN_NAME_PATH="tagdata.ai_recording_references.STEPTREE[DYN_I].recording_name"),
    dyn_senum16("command", DYN_NAME_PATH="..[DYN_I].atom_type.enum_name"),
    dyn_senum16("object_name", DYN_NAME_PATH="tagdata.object_names.STEPTREE[DYN_I].name"),
    SIZE=32
    )

point = Struct("point",
    QStruct("position", INCLUDE=xyz_float),
    SIZE=20
    )

command_list = Struct("command_list",
    ascii_str32("name"),
    Bool32("flags",
        "allow_initiative",
        "allow_targeting",
        "disable_looking",
        "disable_communication",
        "disable_falling_damage",
        "manual_bsp_index",
        ),

    Pad(8),
    dyn_senum16("manual_bsp_index",
        DYN_NAME_PATH=".....structure_bsps.STEPTREE[DYN_I].structure_bsp.filepath"),
    dyn_senum16("bsp_index",
        DYN_NAME_PATH=".....structure_bsps.STEPTREE[DYN_I].structure_bsp.filepath",
        VISIBLE=False
        ),
    reflexive("commands", command, 64),
    reflexive("points", point, 64),
    SIZE=96
    )

participant = Struct("participant",
    Pad(2),
    Bool16("flags",
        "optional",
        "has_alternate",
        "is_alternate",
        ),
    SEnum16("selection_type",
        "friendly_actor",
        "disembodied",
        "in_players_vehicle",
        "not_in_a_vehicle",
        "prefer_sergeant",
        "any_actor",
        "radio_unit",
        "radio_sergeant",
        ),
    SEnum16("actor_type", *actor_types),
    dyn_senum16("use_this_object", DYN_NAME_PATH="tagdata.object_names.STEPTREE[DYN_I].name"),
    dyn_senum16("set_new_name", DYN_NAME_PATH="tagdata.object_names.STEPTREE[DYN_I].name"),

    Pad(12),
    BytesRaw("unknown", DEFAULT=b"\xFF"*12, SIZE=12, VISIBLE=False),
    ascii_str32("encounter_name"),
    SIZE=84
    )

line = Struct("line",
    Bool16("flags",
        "addressee_look_at_speaker",
        "everyone_look_at_speaker",
        "everyone_look_at_addressee",
        "wait_until_told_to_advance",
        "wait_until_speaker_nearby",
        "wait_until_everyone_nearby",
        ),
    dyn_senum16("participant",
        DYN_NAME_PATH=".....participants.STEPTREE[DYN_I].encounter_name"),
    SEnum16("addressee",
        "none",
        "player",
        "participant",
        ),
    dyn_senum16("addressee_participant",
        DYN_NAME_PATH=".....participants.STEPTREE[DYN_I].encounter_name"),

    Pad(4),
    Float("line_delay_time"),

    Pad(12),
    dependency("variant_1", "snd!"),
    dependency("variant_2", "snd!"),
    dependency("variant_3", "snd!"),
    dependency("variant_4", "snd!"),
    dependency("variant_5", "snd!"),
    dependency("variant_6", "snd!"),
    SIZE=124
    )

ai_conversation = Struct("ai_conversation",
    ascii_str32("name"),
    Bool16("flags",
        "stop_if_death",
        "stop_if_damaged",
        "stop_if_visible_enemy",
        "stop_if_alerted_to_enemy",
        "player_must_be_visible",
        "stop_other_actions",
        "keep_trying_to_play",
        "player_must_be_looking",
        ),

    Pad(2),
    float_wu("trigger_distance"),
    float_wu("run_to_player_distance"),

    Pad(36),
    reflexive("participants", participant, 8,
        DYN_NAME_PATH='.encounter_name'),
    reflexive("lines", line, 32),
    SIZE=116
    )

structure_bsp = Struct("structure_bsp",
    UInt32("bsp_pointer", VISIBLE=False),
    UInt32("bsp_size", VISIBLE=False),
    UInt32("bsp_magic", VISIBLE=False),
    Pad(4),
    dependency("structure_bsp", "sbsp"),
    SIZE=32
    )

scnr_body = Struct("tagdata",
    dependency("DONT_USE", 'sbsp'),
    dependency("WONT_USE", 'sbsp'),
    dependency("CANT_USE", 'sky '),
    reflexive("skies", sky, 8, DYN_NAME_PATH='.sky.filepath'),
    SEnum16("type",
        "singleplayer",
        "multiplayer",
        "main_menu"
        ),
    Bool16("flags",
        "cortana_hack",
        "use_demo_ui"
        ),
    reflexive("child_scenarios", child_scenario, 16,
        DYN_NAME_PATH='.child_scenario.filepath'),
    float_rad("local_north"),  # radians

    Pad(156),
    reflexive("predicted_resources", predicted_resource, 1024, VISIBLE=False),
    reflexive("functions", function, 32,
        DYN_NAME_PATH='.name'),
    rawdata_ref("scenario_editor_data", max_size=65536),
    reflexive("comments", comment, 1024),

    Pad(224),
    reflexive("object_names", object_name, 512,
        DYN_NAME_PATH='.name', IGNORE_SAFE_MODE=True),
    reflexive("sceneries", scenery, 2000, IGNORE_SAFE_MODE=True),
    reflexive("sceneries_palette", scenery_swatch, 100,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("bipeds", biped, 128, IGNORE_SAFE_MODE=True),
    reflexive("bipeds_palette", biped_swatch, 100,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("vehicles", vehicle, 80, IGNORE_SAFE_MODE=True),
    reflexive("vehicles_palette", vehicle_swatch, 100,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("equipments", equipment, 256, IGNORE_SAFE_MODE=True),
    reflexive("equipments_palette", equipment_swatch, 100,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("weapons", weapon, 128, IGNORE_SAFE_MODE=True),
    reflexive("weapons_palette", weapon_swatch, 100,
        DYN_NAME_PATH='.name.filepath'),

    reflexive("device_groups", device_group, 128,
        DYN_NAME_PATH='.name', IGNORE_SAFE_MODE=True),
    reflexive("machines", machine, 400, IGNORE_SAFE_MODE=True),
    reflexive("machines_palette", machine_swatch, 100,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("controls", control, 100, IGNORE_SAFE_MODE=True),
    reflexive("controls_palette", control_swatch, 100,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("light_fixtures", light_fixture, 500, IGNORE_SAFE_MODE=True),
    reflexive("light_fixtures_palette", light_fixture_swatch, 100,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("sound_sceneries", sound_scenery, 256, IGNORE_SAFE_MODE=True),
    reflexive("sound_sceneries_palette", sound_scenery_swatch, 100,
        DYN_NAME_PATH='.name.filepath'),

    Pad(84),
    reflexive("player_starting_profiles", player_starting_profile, 256,
        DYN_NAME_PATH='.name'),
    reflexive("player_starting_locations", player_starting_location, 256),
    reflexive("trigger_volumes", trigger_volume, 256,
        DYN_NAME_PATH='.name'),
    reflexive("recorded_animations", recorded_animation, 1024,
        DYN_NAME_PATH='.name', IGNORE_SAFE_MODE=True),
    reflexive("netgame_flags", netgame_flag, 200,
        DYN_NAME_PATH='.type.enum_name'),
    reflexive("netgame_equipments", netgame_equipment, 200,
        DYN_NAME_PATH='.item_collection.filepath'),
    reflexive("starting_equipments", starting_equipment, 200),
    reflexive("bsp_switch_trigger_volumes", bsp_switch_trigger_volume, 256),
    reflexive("decals", decal, 65535),
    reflexive("decals_palette", decal_swatch, 128,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("detail_object_collection_palette",
        detail_object_collection_swatch, 32, DYN_NAME_PATH='.name.filepath'),

    Pad(84),
    reflexive("actors_palette", actor_swatch, 64,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("encounters", encounter, 128, DYN_NAME_PATH='.name'),
    reflexive("command_lists", command_list, 256, DYN_NAME_PATH='.name'),
    reflexive("ai_animation_references", ai_anim_reference, 128,
        DYN_NAME_PATH='.animation_name'),
    reflexive("ai_script_references", ai_script_reference, 128,
        DYN_NAME_PATH='.script_name'),
    reflexive("ai_recording_references", ai_recording_reference, 128,
        DYN_NAME_PATH='.recording_name'),
    reflexive("ai_conversations", ai_conversation, 128,
        DYN_NAME_PATH='.name'),
    rawdata_ref("script_syntax_data", max_size=380076, IGNORE_SAFE_MODE=True),
    rawdata_ref("script_string_data", max_size=262144, IGNORE_SAFE_MODE=True),
    reflexive("scripts", halo_script, 512, DYN_NAME_PATH='.name'),
    reflexive("globals", halo_global, 128, DYN_NAME_PATH='.name'),
    reflexive("references", reference, 256,
              DYN_NAME_PATH='.reference.filepath'),
    reflexive("source_files", source_file, 8, DYN_NAME_PATH='.source_name'),

    Pad(24),
    reflexive("cutscene_flags", cutscene_flag, 512, DYN_NAME_PATH='.name'),
    reflexive("cutscene_camera_points", cutscene_camera_point, 512,
        DYN_NAME_PATH='.name'),
    reflexive("cutscene_titles", cutscene_title, 64, DYN_NAME_PATH='.name'),
    Pad(12), # OS bsp_modifiers reflexive

    Pad(96),
    dependency("custom_object_names", 'ustr'),
    dependency("ingame_help_text", 'ustr'),
    dependency("hud_messages", 'hmt '),
    reflexive("structure_bsps", structure_bsp, 16,
        DYN_NAME_PATH='.structure_bsp.filepath'),
    SIZE=1456,
    )

def get():
    return scnr_def

scnr_def = TagDef("scnr",
    blam_header('scnr', 2),
    scnr_body,

    ext=".scenario", endian=">", tag_cls=HekTag
    )
