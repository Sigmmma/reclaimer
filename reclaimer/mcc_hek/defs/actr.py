#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from .objs.actr import ActrTag
from supyr_struct.defs.tag_def import TagDef

danger_triggers = (
    "never",
    "visible",
    "shooting",
    "shooting_near_us",
    "damaging_us",
    "unused1",
    "unused2",
    "unused3",
    "unused4",
    "unused5",
    )

actr_body = Struct("tagdata",
    Bool32('flags',
        "can_see_in_darkness",
        "sneak_uncovering_target",
        "sneak_uncovering_pursuit_location",
        "unused1",
        "shoot_at_targets_last_location",
        "try_to_stay_still_when_crouched",
        "crouch_when_not_in_combat",
        "crouch_when_guarding",
        "unused2",
        "must_crouch_to_shoot",
        "panic_when_surprised",
        "always_charge_at_enemies",
        "gets_in_vehicles_with_player",
        "starts_firing_before_aligned",
        "standing_must_move_forward",
        "crouching_must_move_forward",
        "defensive_crouch_while_charging",
        "use_stalking_behavior",
        "stalking_freeze_if_exposed",
        "always_berserk_in_attacking_mode",
        "berserking_uses_panicked_movement",
        "flying",
        "panicked_by_unopposable_enemy",
        "crouch_when_hiding_from_unopposable",
        "always_charge_in_attacking_mode",
        "dive_off_ledges",
        "swarm",
        "suicidal_melee_attack",
        "cannot_move_while_crouching",
        "fixed_crouch_facing",
        "crouch_when_in_line_of_fire",
        "avoid_friends_line_of_fire"
        ),
    Bool32('more_flags',
        "avoid_all_enemy_attack_vectors",
        "must_stand_to_fire",
        "must_stop_to_fire",
        "disallow_vehicle_combat",
        "pathfinding_ignores_danger",
        "panic_in_groups",
        "no_corpse_shooting"
        ),

    Pad(12),
    SEnum16("type", *actor_types),

    Pad(2),
    Struct("perception",
        float_wu("max_vision_distance"),  # world units
        float_rad("central_vision_angle"),  # radians
        float_rad("max_vision_angle"),  # radians

        Pad(4),
        float_rad("peripheral_vision_angle"),  # radians
        float_wu("peripheral_distance"),  # world units

        Pad(4),
        QStruct("standing_gun_offset", INCLUDE=ijk_float),
        QStruct("crouching_gun_offset", INCLUDE=ijk_float),
        float_wu("hearing_distance"),  # world units
        float_zero_to_one("notice_projectile_chance"),
        float_zero_to_one("notice_vehicle_chance"),

        Pad(8),
        float_sec("combat_perception_time",
                  UNIT_SCALE=sec_unit_scale),  # seconds
        float_sec("guard_perception_time",
                  UNIT_SCALE=sec_unit_scale),  # seconds
        float_sec("non_combat_perception_time",
                  UNIT_SCALE=sec_unit_scale),  # seconds

        float_sec("inv_combat_perception_time",
                  UNIT_SCALE=sec_unit_scale, VISIBLE=False),
        float_sec("inv_guard_perception_time",
                  UNIT_SCALE=sec_unit_scale, VISIBLE=False),
        float_sec("inv_non_combat_perception_time",
                  UNIT_SCALE=sec_unit_scale, VISIBLE=False),
        ),

    Pad(8),
    Struct("movement",
        float_zero_to_one("dive_into_cover_chance"),
        float_zero_to_one("emerge_from_cover_chance"),
        float_zero_to_one("dive_from_grenade_cover_chance"),
        float_wu("pathfinding_radius"),  # world units
        float_zero_to_one("glass_ignorance_chance"),
        float_wu("stationary_movement_dist"),  # world units
        float_wu("free_flying_sidestep"),  # world units
        float_rad("begin_moving_angle"),  # radians
        ),

    Pad(4),
    Struct("looking",
        yp_float_rad("maximum_aiming_deviation"),  # radians
        yp_float_rad("maximum_looking_deviation"),  # radians
        float_rad("noncombat_look_delta_l"),  # radians
        float_rad("noncombat_look_delta_r"),  # radians
        float_rad("combat_look_delta_l"),  # radians
        float_rad("combat_look_delta_r"),  # radians
        from_to_rad("idle_aiming_range"),  # radians
        from_to_rad("idle_looking_range"),  # radians
        QStruct("event_look_time_modifier", INCLUDE=from_to),
        from_to_sec("noncombat_idle_facing"),  # seconds
        from_to_sec("noncombat_idle_aiming"),  # seconds
        from_to_sec("noncombat_idle_looking"),  # seconds
        from_to_sec("guard_idle_facing"),  # seconds
        from_to_sec("guard_idle_aiming"),  # seconds
        from_to_sec("guard_idle_looking"),  # seconds
        from_to_sec("combat_idle_facing"),  # seconds
        from_to_sec("combat_idle_aiming"),  # seconds
        from_to_sec("combat_idle_looking"),  # seconds
        Pad(8),
        from_to_neg_one_to_one("cosine_maximum_aiming_deviation", VISIBLE=False),
        from_to_neg_one_to_one("cosine_maximum_looking_deviation", VISIBLE=False),

        dependency("DO_NOT_USE_1", "weap"),

        Pad(268),
        dependency("DO_NOT_USE_2", "proj")
        ),

    Struct("unopposable",
        SEnum16("unreachable_danger_trigger", *danger_triggers),
        SEnum16("vehicle_danger_trigger", *danger_triggers),
        SEnum16("player_danger_trigger", *danger_triggers),

        Pad(2),
        from_to_sec("danger_trigger_time"),  # seconds
        SInt16("friends_killed_trigger"),
        SInt16("friends_retreating_trigger"),

        Pad(12),
        from_to_sec("retreat_time"),  # seconds
        ),

    Pad(8),
    Struct("panic",
        from_to_sec("cowering_time"),  # seconds
        float_zero_to_one("friend_killed_panic_chance"),
        SEnum16("leader_type", *actor_types),

        Pad(2),
        float_zero_to_one("leader_killed_panic_chance"),
        float_zero_to_one("panic_damage_threshold"),
        float_wu("surprise_distance"),  # world units
        ),

    Pad(28),
    Struct("defensive",
        from_to_sec("hide_behind_cover_time"),  # seconds
        float_sec("hide_target_not_visible_time",
                  UNIT_SCALE=sec_unit_scale),  # seconds
        float_zero_to_one("hide_shield_fraction"),
        float_zero_to_one("attack_shield_fraction"),
        float_zero_to_one("pursue_shield_fraction"),

        Pad(16),
        SEnum16("defensive_crouch_type",
            "never",
            "danger",
            "low_shields",
            "hide_behind_shield",
            "any_target",
            "flood_shamble"
            ),

        Pad(2),
        Float("attacking_crouch_threshold"),
        Float("defending_crouch_threshold"),
        float_sec("mim_stand_time",  UNIT_SCALE=sec_unit_scale),  # seconds
        float_sec("mim_crouch_time", UNIT_SCALE=sec_unit_scale),  # seconds
        Float("defending_hide_time_modifier"),
        Float("attacking_evasion_threshold"),
        Float("defending_evasion_threshold"),
        float_zero_to_one("evasion_seek_cover_chance"),
        float_sec("evasion_delay_time", UNIT_SCALE=sec_unit_scale),  # seconds
        float_wu("max_seek_cover_distance"),  # world units
        float_zero_to_one("cover_damage_threshold"),
        float_sec("stalking_discovery_time",
                  UNIT_SCALE=sec_unit_scale),  # seconds
        float_wu("stalking_max_distance"),  # world units
        float_rad("stationary_facing_angle"),  # radians
        float_sec("change_facing_stand_time",
                  UNIT_SCALE=sec_unit_scale),  # seconds
        ),

    Pad(4),
    Struct("pursuit",
        from_to_sec("uncover_delay_time"),  # seconds
        from_to_sec("target_search_time"),  # seconds
        from_to_sec("pursuit_position_time"),  # seconds
        SInt16("coordinated_position_count", MIN=0),
        SInt16("normal_position_count", MIN=0),
        ),

    Pad(32),
    QStruct("berserk",
        float_sec("melee_attack_delay", UNIT_SCALE=sec_unit_scale),  # seconds
        float_wu("melee_fudge_factor"),  # world units
        float_sec("melee_charge_time",  UNIT_SCALE=sec_unit_scale),  # seconds
        float_wu("melee_leap_range_lower_bound"),  # world units
        float_wu("melee_leap_range_upper_bound"),  # world units
        Float("melee_leap_velocity", SIDETIP="world units/tick",
               UNIT_SCALE=per_sec_unit_scale),  # world units/tick
        float_zero_to_one("melee_leap_chance"),
        float_zero_to_one("melee_leap_ballistic"),
        float_zero_to_one("berserk_damage_amount"),
        float_zero_to_one("berserk_damage_threshold"),
        float_wu("berserk_proximity"),  # world units
        float_wu("suicide_sensing_dist"),  # world units
        float_zero_to_one("berserk_grenade_chance"),
        ),

    Pad(12),
    Struct("firing_positions",
        from_to_sec("guard_position_time"),  # seconds
        from_to_sec("combat_position_time"),  # seconds
        Float("old_position_avoid_dist"),  # world units
        Float("friend_avoid_dist"),  # world units
        ),

    Pad(40),
    Struct("communication",
        from_to_sec("noncombat_idle_speech_time"),  # seconds
        from_to_sec("combat_idle_speech_time"),  # seconds

        Pad(176),
        dependency("DO_NOT_USE_3", "actr"),
        ),
    SIZE=1272
    )


def get():
    return actr_def

actr_def = TagDef("actr",
    blam_header('actr', 2),
    actr_body,

    ext=".actor", endian=">", tag_cls=ActrTag
    )
