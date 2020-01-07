#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...os_v3_hek.defs.unit import *

region_targeting_comment="""
When a target region is defined, melee damage is directed at it until it is destroyed.
"""

unit_keyframe_action = Struct("unit_keyframe_action",
    SEnum16("keyframe",
        "primary",
        "secondary",
        "final",
        ),
    Bool16("flags",
        "eject_mounted_units",
        ),
    SEnum16("target",
        "all_seats",
        "mounted_trigger_seats",
        ),
    Pad(2),

    dependency('damage_effect', "jpt!"),
    dependency('effect', "effe"),
    ascii_str32("effect_marker"),
    SIZE=96
    )

seat_keyframe_action = Struct("seat_keyframe_action",
    SEnum16("keyframe",
        "primary",
        "secondary",
        "final",
        ),
    Bool16("flags",
        "control_powered_seat",
        ),
    SEnum16("self_seat_action",
        "none",
        "exit_current_seat",
        "enter_target_seat",
        ),
    SEnum16("target_seat_unit_action",
        "none",
        "exit_seat",
        "eject_from_seat",
        ),
    SEnum16("unit_door_action",
        "neither",
        "open",
        "close",
        ),
    Pad(2),
    SEnum16("apply_damage_to",
        "none",
        "mounted_unit",
        "mounted_unit_region",
        "seated_unit",
        ),
    Pad(2),

    ascii_str32("region_name"),
    dependency('damage_effect', "jpt!"),

    SEnum16("apply_effect_to",
        "none",
        "mounted_unit",
        "seated_unit",
        ),
    Pad(2),

    dependency('effect', "effe"),
    ascii_str32("effect_marker"),

    SIZE=152
    )

mounted_state = Struct("mounted_state",
    Bool16("flags",
        "third_person_camera"
        ),
    Pad(2),

    ascii_str32("camera_marker_name"),
    ascii_str32("camera_submerged_marker_name"),
    float_deg("pitch_autolevel"),
    from_to_deg("pitch_range"),
    reflexive("camera_tracks", camera_track, 2,
        'loose', 'tight'),
    reflexive("keyframe_actions", unit_keyframe_action, 12,
        DYN_NAME_PATH='.effect_marker'),
    SIZE=128
    )

seat_access = Struct("seat_access",
    Bool16("flags",
        "requires_target_seat_occupied",
        "enemy_access_only",
        "restrict_by_unit_sight",
        "restrict_by_mounting_unit_sight",
        "restrict_by_unit_shield",
        "restrict_by_unit_health",
        "restrict_by_ai_state",
        ),
    Pad(2),
    float_rad("unit_sight_angle"),
    ascii_str32("unit_sight_marker_name"),
    float_rad("mounting_unit_sight_angle"),
    ascii_str32("mounting_unit_sight_marker_name"),
    float_zero_to_one("unit_shield_threshold"),
    float_zero_to_one("unit_health_threshold"),
    Bool16("permitted_ai_states", *actor_states),

    SIZE=124
    )

seat_boarding = Struct("seat_boarding",
    SEnum16("boarding_type",
        "immediate",
        "delayed"
        ),
    Bool16("delay_until",
        "empty_target_seat",
        "unit_shield_threshold",
        "unit_health_threshold",
        "region_destroyed",
        ),
    SEnum16("unit_vitality_source",
        "mounted_unit",
        "seated_unit"
        ),
    Pad(2),

    float_zero_to_one("unit_shield_threshold"),
    float_zero_to_one("unit_health_threshold"),
    Pad(4),

    ascii_str32("region_name"),
    Pad(24),

    reflexive("seat_keyframe_actions", seat_keyframe_action, 12,
        DYN_NAME_PATH='.region_name'),

    SIZE=112
    )

seat_damage = Struct("seat_damage",
    Bool16("flags",
        "use_weapon_damage_melee_effect",
        "exit_after_grenade_plant",
        ),
    Struct("melee_damage",
        SEnum16("melee",
            "normal",
            "mounted_unit",
            "target_seat_unit"
            ),
        dependency("damage_effect", "jpt!"),
        ),

    Struct("grenade_damage",
        SEnum16("grenade",
            "normal",
            "disabled",
            "plant_on_mounted_unit",
            "plant_on_target_seat_unit"
            ),
        Bool16("disabled_types",
            "fragmentation_grenade",
            "plasma_grenade",
            "custom_grenade_1",
            "custom_grenade_2",
            ),
        float_zero_to_inf("detonation_time", UNIT_SCALE=sec_unit_scale),
        ascii_str32("attach_marker"),
        ),

    Struct("region_targeting",
        Bool16("flags",
            "disable_grenades_until_destroyed"
            ),
        Pad(2),

        ascii_str32("region_name"),
        dependency("damage_effect", "jpt!"),
        COMMENT=region_targeting_comment
        ),
    SIZE=136
    )

unit_extension = Struct("unit_extension",
    reflexive("mounted_states", mounted_state, 1),
    SIZE=60
    )

seat_extension = Struct("seat_extension",
    Bool16("flags",
        "triggers_mounted_state",
        "exit_on_unit_death",
        "exit_on_target_seat_empty",
        "prevent_death_when_unit_dies",
        "ignored_by_seated_ai",
        "ignored_by_mounted_ai",
        "cant_enter_seats_when_occupied",
        ),
    dyn_senum16("target_seat",
        DYN_NAME_PATH="tagdata.unit_attrs.seats.STEPTREE[DYN_I].label"),
    Pad(12),  # reflexive("unknown", unknown),
    reflexive("seat_access", seat_access, 1),
    reflexive("seat_boarding", seat_boarding, 1),
    reflexive("seat_damage", seat_damage, 1),
    SIZE=100
    )

seat = dict(seat)
unit_attrs = dict(unit_attrs)

seat[0] = Bool32("flags",
    "invisible",
    "locked",
    "driver",
    "gunner",
    "third_person_camera",
    "allows_weapons",
    "third_person_on_enter",
    "first_person_slaved_to_gun",
    "allow_vehicle_communcation_animation",
    "not_valid_without_driver",
    "allow_ai_noncombatants",
    ("allows_melee", 1<<20)
    )
seat[20] = reflexive("seat_extensions", seat_extension, 1)
unit_attrs[45] = reflexive("unit_extensions", unit_extension, 1)
unit_attrs[54] = reflexive("seats", seat, 16, DYN_NAME_PATH='.label')

unit_body = Struct('tagdata', unit_attrs)

def get():
    return unit_def

unit_def = TagDef("unit",
    blam_header('unit', 2),
    unit_body,

    ext=".unit", endian=">", tag_cls=HekTag
    )
