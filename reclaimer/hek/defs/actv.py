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

change_color = Struct("change_color",
    QStruct("color_lower_bound", INCLUDE=rgb_float),
    QStruct("color_upper_bound", INCLUDE=rgb_float),
    SIZE=32
    )

actv_grenades = Struct("grenades",
    Pad(8),
    SEnum16("grenade_type", *grenade_types),
    SEnum16("trajectory_type",
        "toss",
        "lob",
        "bounce",
        ),
    SEnum16("grenade_stimulus",
        "never",
        "visible_target",
        "seek_cover",
        ),
    SInt16("minimum_enemy_count"),
    float_wu("enemy_radius"),

    Pad(4),
    float_wu_sec("grenade_velocity", UNIT_SCALE=per_sec_unit_scale),
    from_to_wu("grenade_ranges"),
    float_wu("collateral_damage_radius"),
    float_zero_to_one("grenade_chance"),
    float_sec("grenade_check_time", UNIT_SCALE=sec_unit_scale),
    float_sec("encounter_grenade_timeout", UNIT_SCALE=sec_unit_scale)
    )

actv_body = Struct("tagdata",
    Bool32('flags',
        "can_shoot_while_flying",
        "blend_color_in_hsv",
        "has_unlimited_grenades",
        "moveswitch_stay_with_friends",
        "active_camouflage",
        "super_active_camouflage",
        "cannot_use_ranged_weapons",
        "prefer_passenger_seat",
        ),
    dependency("actor_definition", "actr"),
    dependency("unit", valid_units),
    dependency("major_variant", "actv"),
    SEnum16("mcc_actor_type", TOOLTIP="Used to determine score in MCC", *mcc_actor_types),


    #Movement switching
    Struct("movement_switching",
        Pad(22),
        SEnum16("movement_type",
            "always_run",
            "always_crouch",
            "switch_types",
            ),
        Pad(2),
        float_zero_to_one("initial_crouch_chance"),
        from_to_sec("crouch_time", UNIT_SCALE=sec_unit_scale),  # seconds
        from_to_sec("run_time",    UNIT_SCALE=sec_unit_scale)   # seconds
        ),

    #Ranged combat
    Struct("ranged_combat",
        dependency("weapon", "weap"),
        float_wu("maximum_firing_distance"),
        Float("rate_of_fire", UNIT_SCALE=per_sec_unit_scale),  # rounds/sec
        float_rad("projectile_error"),  # radians
        from_to_sec("first_burst_delay_time",
                    UNIT_SCALE=sec_unit_scale),  # seconds
        Float("new_target_firing_pattern_time",
               UNIT_SCALE=sec_unit_scale),  # seconds
        Float("surprise_delay_time", UNIT_SCALE=sec_unit_scale),  # seconds
        Float("surprise_fire_wildly_time",
               UNIT_SCALE=sec_unit_scale),  # seconds
        float_zero_to_one("death_fire_wildly_chance"),
        float_sec("death_fire_wildly_time",
                  UNIT_SCALE=sec_unit_scale),  # seconds
        from_to_wu("desired_combat_range"),
        QStruct("custom_stand_gun_offset", INCLUDE=ijk_float),
        QStruct("custom_crouch_gun_offset", INCLUDE=ijk_float),
        float_zero_to_one("target_tracking"),
        float_zero_to_one("target_leading"),
        Float("weapon_damage_modifier"),
        Float("damage_per_second", UNIT_SCALE=per_sec_unit_scale),  # seconds
        ),

    #Burst geometry
    Struct("burst_geometry",
        float_wu("burst_origin_radius"),
        float_rad("burst_origin_angle"),  # radians
        from_to_wu("burst_return_length"),
        float_rad("burst_return_angle"),  # radians
        from_to_sec("burst_duration", UNIT_SCALE=sec_unit_scale),  # seconds
        from_to_sec("burst_separation"),
        Float("burst_angular_velocity", SIDETIP="degrees/sec",
               UNIT_SCALE=irad_per_sec_unit_scale), # radians/second
        Pad(4),
        float_zero_to_one("special_damage_modifier"),
        float_rad("special_projectile_error")  # radians
        ),

    #Firing patterns"
    Struct("firing_patterns",
        Float("new_target_burst_duration"),
        Float("new_target_burst_separation"),
        Float("new_target_rate_of_fire", UNIT_SCALE=per_sec_unit_scale),
        Float("new_target_projectile_error"),

        Pad(8),
        Float("moving_burst_duration"),
        Float("moving_burst_separation"),
        Float("moving_rate_of_fire", UNIT_SCALE=per_sec_unit_scale),
        Float("moving_projectile_error"),

        Pad(8),
        Float("berserk_burst_duration"),
        Float("berserk_burst_separation"),
        Float("berserk_rate_of_fire", UNIT_SCALE=per_sec_unit_scale),
        Float("berserk_projectile_error")
        ),

    #Special-case firing patterns
    Struct("special_case_firing_patterns",
        Pad(8),
        Float("super_ballistic_range"),
        Float("bombardment_range"),
        Float("modified_vision_range"),
        SEnum16("special_fire_mode",
            "none",
            "overcharge",
            "secondary_trigger",
            ),
        SEnum16("special_fire_situation",
            "never",
            "enemy_visible",
            "enemy_out_of_sight",
            "strafing",
            ),
        float_zero_to_one("special_fire_chance"),
        float_sec("special_fire_delay", UNIT_SCALE=sec_unit_scale)
        ),

    #Berserking and melee
    Struct("berserking_and_melee",
        float_wu("melee_range"),
        float_wu("melee_abort_range"),
        from_to_wu("berserk_firing_ranges", INCLUDE=from_to),
        float_wu("berserk_melee_range"),
        float_wu("berserk_melee_abort_range")
        ),

    #Grenades
    actv_grenades,

    #Items
    Struct("items",
        Pad(20),
        dependency("equipment", "eqip"),
        QStruct("grenade_count",
            SInt16("from", GUI_NAME=""), SInt16("to"), ORIENT='h'
            ),
        float_zero_to_one("dont_drop_grenades_chance"),
        QStruct("drop_weapon_loaded", INCLUDE=from_to),
        QStruct("drop_weapon_ammo",
            SInt16("from", GUI_NAME=""),
            SInt16("to"), ORIENT='h'
            )
        ),

    #Unit properties
    Struct("unit_properties",
        Pad(28),
        Float("body_vitality"),
        Float("shield_vitality"),
        float_wu("shield_sapping_radius"),
        SInt16("forced_shader_permutation"),
        ),

    Pad(30),
    reflexive("change_colors", change_color, 4),
    SIZE=568
    )


def get():
    return actv_def

actv_def = TagDef("actv",
    blam_header('actv'),
    actv_body,

    ext=".actor_variant", endian=">", tag_cls=HekTag
    )
