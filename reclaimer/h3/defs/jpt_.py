#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: Veegie
# 	Completed plugin
# revision: 3		author: Lord Zedd
# 	Updated and standardized and restored shit veegie deleted
# revision: 4		author: Lord Zedd
# 	Now with comments.
# revision: 5		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef

jpt__category = (
    "none",
    "falling",
    "bullet",
    "grenade",
    "high_explosive",
    "sniper",
    "melee",
    "flame",
    "mounted_weapon",
    "vehicle",
    "plasma",
    "needle",
    "shotgun",
    )

jpt__player_response_priority = (
    "low",
    "medium",
    "high",
    )

jpt__player_response_type = (
    "none",
    "lighten",
    "darken",
    "max",
    "min",
    "invert",
    "tint",
    )

jpt__side_effect = (
    "none",
    "harmless",
    "lethal_to_the_unsuspecting",
    "emp",
    )


jpt__player_response = Struct("player_response",
    SEnum16("response_type", *jpt__player_response_response_type),
    SInt16("unknown_0", VISIBLE=False),
    SEnum16("type", *jpt__player_response_type),
    SEnum16("priority", *jpt__player_response_priority),
    Float("duration_0"),
    SEnum16("fade_function", *jpt__player_response_fade_function),
    SInt16("unknown_1", VISIBLE=False),
    Float("maximum_intensity"),
    color_argb_float("color"),
    Float("low_frequency_vibration_duration"),
    h3_rawdata_ref("low_frequency_vibration_function"),
    Float("high_frequency_vibration_duration"),
    h3_rawdata_ref("high_frequency_vibration_function"),
    h3_string_id("effect_name"),
    Float("duration_1"),
    h3_rawdata_ref("effect_scale_function"),
    ENDIAN=">", SIZE=112
    )


jpt__body = Struct("tagdata",
    QStruct("radius", INCLUDE=from_to),
    Float("cutoff_scale"),
    Bool32("flags_0",
        "dont_scale_damage_by_distance",
        "area_damage_players_only",
        ),
    SEnum16("side_effect", *jpt__side_effect),
    SEnum16("category", *jpt__category),
    Bool32("flags_1",
        "does_not_hurt_owner",
        "can_cause_headshots",
        "pings_resistant_units",
        "does_not_hurt_friends",
        "does_not_ping_units",
        "detonates_explosives",
        "only_hurts_shields",
        "causes_flaming_death",
        "damage_indicators_always_point_down",
        "skips_shields",
        "only_hurts_one_infection_form",
        ("infection_form_pop", 1 << 12),
        "ignore_seat_scale_for_direct_damage",
        "forces_hard_ping",
        "does_not_hurt_players",
        ),
    Float("area_of_effect_core_radius"),
    Float("damage_lower_bound"),
    QStruct("damage_upper_bound", INCLUDE=from_to),
    float_rad("damage_inner_cone_angle"),
    float_rad("damage_outer_cone_angle"),
    Float("active_camoflage_damage"),
    Float("stun"),
    Float("max_stun"),
    Float("stun_time"),
    Float("instantaneous_acceleration"),
    Float("rider_direct_damage_scale"),
    Float("rider_max_transfer_damage_scale"),
    Float("rider_min_transfer_damage_scale"),
    h3_string_id("general_damage"),
    h3_string_id("specific_damage"),
    h3_string_id("special_damage"),
    Float("ai_stun_radius"),
    QStruct("ai_stun_bounds", INCLUDE=from_to),
    Float("shake_radius"),
    Float("emp_radius"),
    Float("unknown_0", VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    h3_reflexive("player_responses", jpt__player_response),
    h3_dependency("damage_response"),
    Float("duration_0"),
    SEnum16("fade_function", *jpt__player_response_fade_function),
    SInt16("unknown_2", VISIBLE=False),
    float_rad("rotation"),
    Float("pushback"),
    QStruct("jitter", INCLUDE=from_to),
    Float("duration_1"),
    SEnum16("falloff_function", *jpt__player_response_fade_function),
    SInt16("unknown_3", VISIBLE=False),
    Float("random_translation"),
    float_rad("random_rotation"),
    SEnum16("wobble_function", *jpt__wobble_function),
    SInt16("unknown_4", VISIBLE=False),
    Float("wobble_function_period"),
    Float("wobble_weight"),
    h3_dependency("sound"),
    Float("forward_velocity"),
    Float("forward_radius"),
    Float("forward_exponent"),
    Float("outward_velocity"),
    Float("outward_radius"),
    Float("outward_exponent"),
    ENDIAN=">", SIZE=240
    )


def get():
    return jpt__def

jpt__def = TagDef("jpt!",
    h3_blam_header('jpt!'),
    jpt__body,

    ext=".%s" % h3_tag_class_fcc_to_ext["jpt!"], endian=">", tag_cls=H3Tag
    )
