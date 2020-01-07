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
# revision: 2		author: Lord Zedd
# 	Portin'
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef

proj_detonation_timer_starts = (
    "immediately",
    "after_first_bounce",
    "when_at_rest",
    "after_first_bounce_off_any_surface",
    )

proj_material_response_response_0 = (
    "impact_detonate",
    "fizzle",
    "overpenetrate",
    "attach",
    "bounce",
    "bounce_dud",
    "fizzle_ricochet",
    )

proj_material_response_scale_effects_by = (
    "damage",
    "angle",
    )


proj_early_mover_propertie = Struct("early_mover_propertie",
    h3_string_id("name"),
    Pad(36),
    ENDIAN=">", SIZE=40
    )


proj_ai_propertie = Struct("ai_propertie",
    Bool32("flags",
        "destroyable_cover",
        "pathfinding_ignore_when_dead",
        "dynamic_cover",
        ),
    h3_string_id("ai_type_name"),
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    SEnum16("size", *bloc_ai_propertie_size),
    SEnum16("leap_jump_speed", *bloc_ai_propertie_leap_jump_speed),
    ENDIAN=">", SIZE=16
    )


proj_function = Struct("function",
    Bool32("flags",
        "invert",
        "mapping_does_not_controls_active",
        "always_active",
        "random_time_offset",
        ),
    h3_string_id("import_name"),
    h3_string_id("export_name"),
    h3_string_id("turn_off_with"),
    Float("minimum_value"),
    h3_rawdata_ref("default_function"),
    h3_string_id("scale_by"),
    ENDIAN=">", SIZE=44
    )


proj_attachment = Struct("attachment",
    h3_dependency("attachment"),
    h3_string_id("marker"),
    SEnum16("change_color", *bloc_attachment_change_color),
    SInt16("unknown", VISIBLE=False),
    h3_string_id("primary_scale"),
    h3_string_id("secondary_scale"),
    ENDIAN=">", SIZE=32
    )


proj_widget = Struct("widget",
    h3_dependency("type"),
    ENDIAN=">", SIZE=16
    )


proj_change_color_initial_permutation = Struct("initial_permutation",
    Pad(4),
    color_rgb_float("color_lower_bound"),
    color_rgb_float("color_upper_bound"),
    h3_string_id("variant_name"),
    ENDIAN=">", SIZE=32
    )


proj_change_color_function = Struct("function",
    Bool32("scale_flags",
        "blend_in_hsv",
        "more_colors",
        ),
    color_rgb_float("color_lower_bound"),
    color_rgb_float("color_upper_bound"),
    h3_string_id("darken_by"),
    h3_string_id("scale_by"),
    ENDIAN=">", SIZE=32
    )


proj_change_color = Struct("change_color",
    h3_reflexive("initial_permutations", proj_change_color_initial_permutation),
    h3_reflexive("functions", proj_change_color_function),
    ENDIAN=">", SIZE=24
    )


proj_predicted_resource = Struct("predicted_resource",
    SInt16("type"),
    SInt16("resource_index"),
    dependency_uint32("tag_index", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=8
    )


proj_multiplayer_object_propertie = Struct("multiplayer_object_propertie",
    Bool16("engine_flags",
        "capture_the_flag",
        "slayer",
        "oddball",
        "king_of_the_hill",
        "juggernaut",
        "territories",
        "assault",
        "vip",
        "infection",
        ),
    SEnum8("object_type", *bloc_multiplayer_object_propertie_object_type),
    Bool8("teleporter_flags",
        "disallows_players",
        "allows_land_vehicles",
        "allows_heavy_vehicles",
        "allows_flying_vehicles",
        "allows_projectiles",
        ),
    Bool16("flags",
        "editor_only",
        ),
    SEnum8("shape", *bloc_multiplayer_object_propertie_shape),
    SEnum8("spawn_timer_mode", *bloc_multiplayer_object_propertie_spawn_timer_mode),
    SInt16("spawn_time"),
    SInt16("abandon_time"),
    Float("radius_width"),
    Float("length"),
    Float("top"),
    Float("bottom"),
    Float("unknown_0", VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    SInt32("unknown_3", VISIBLE=False),
    SInt32("unknown_4", VISIBLE=False),
    h3_dependency("child_object"),
    SInt32("unknown_5"),
    h3_dependency("shape_shader"),
    h3_dependency("unknown_shader"),
    h3_dependency("unknown_6"),
    h3_dependency("unknown_7"),
    h3_dependency("unknown_8"),
    h3_dependency("unknown_9"),
    h3_dependency("unknown_10"),
    h3_dependency("unknown_11"),
    ENDIAN=">", SIZE=196
    )


proj_material_response = Struct("material_response",
    Bool16("flags_0",
        "cannot_be_overpenetrated",
        ),
    SEnum16("response_0", *proj_material_response_response_0),
    h3_string_id("material_name"),
    SInt16("global_material_index"),
    SInt16("unknown_0", VISIBLE=False),
    SEnum16("response_1", *proj_material_response_response_0),
    Bool16("flags_1",
        "only_against_units",
        "never_against_units",
        ),
    Float("chance_fraction"),
    from_to_rad("between_angle"),
    QStruct("and_velocity", INCLUDE=from_to),
    SEnum16("scale_effects_by", *proj_material_response_scale_effects_by),
    SInt16("unknown_1", VISIBLE=False),
    float_rad("angular_noise"),
    Float("velocity_noise"),
    Float("initial_friction"),
    Float("maximum_distance"),
    Float("parallel_friction"),
    Float("perpendicular_friction"),
    ENDIAN=">", SIZE=64
    )


proj_claymore_grenade = Struct("claymore_grenade",
    float_rad("unknown_0"),
    float_rad("unknown_1"),
    float_rad("unknown_2"),
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=9),
    ENDIAN=">", SIZE=48
    )


proj_firebomb_grenade = Struct("firebomb_grenade",
    Float("unknown"),
    ENDIAN=">", SIZE=4
    )


proj_shotgun_propertie = Struct("shotgun_propertie",
    SInt16("amount"),
    SInt16("distance"),
    Float("accuracy"),
    float_rad("spread_cone_angle"),
    ENDIAN=">", SIZE=12
    )


proj_body = Struct("tagdata",
    SEnum16("object_type", *bloc_object_type),
    Bool16("flags_0",
        "does_not_cast_shadow",
        "search_cardinal_direction_lightmaps",
        ("not_a_pathfinding_obstacle", 1 << 3),
        "extension_of_parent",
        "does_not_cause_collision_damage",
        "early_mover",
        "early_mover_localized_physics",
        "use_static_massive_lightmap_sample",
        "object_scales_attachments",
        "inherits_player_s_appearance",
        "dead_bipeds_can_t_localize",
        "attach_to_clusters_by_dynamic_sphere",
        "effects_created_by_this_object_do_not_spawn_objects_in_multiplayer",
        ),
    Float("bounding_radius"),
    QStruct("bounding_offset", INCLUDE=xyz_float),
    Float("acceleration_scale"),
    SEnum16("lightmap_shadow_mode_size", *bloc_lightmap_shadow_mode_size),
    SEnum8("sweetener_size", *bloc_sweetener_size),
    SEnum8("water_density", *bloc_water_density),
    SInt32("unknown_0", VISIBLE=False),
    Float("dynamic_light_sphere_radius"),
    QStruct("dynamic_light_sphere_offset", INCLUDE=xyz_float),
    h3_string_id("default_model_variant"),
    h3_dependency("model"),
    h3_dependency("crate_object"),
    h3_dependency("collision_damage"),
    h3_reflexive("early_mover_properties", proj_early_mover_propertie),
    h3_dependency("creation_effect"),
    h3_dependency("material_effects"),
    h3_dependency("melee_impact"),
    h3_reflexive("ai_properties", proj_ai_propertie),
    h3_reflexive("functions", proj_function),
    SInt16("hud_text_message_index"),
    SInt16("unknown_1", VISIBLE=False),
    h3_reflexive("attachments", proj_attachment),
    h3_reflexive("widgets", proj_widget),
    h3_reflexive("change_colors", proj_change_color),
    h3_reflexive("predicted_resources", proj_predicted_resource),
    h3_reflexive("multiplayer_object_properties", proj_multiplayer_object_propertie),
    Bool32("flags_1",
        "oriented_along_velocity",
        "ai_must_use_ballistic_aiming",
        "detonation_max_time_if_attached",
        "has_super_combining_explosion",
        "damage_scales_based_on_distance",
        "travels_instantaneously",
        "steering_adjusts_orientation",
        "dont_noise_up_steering",
        "can_track_behind_itself",
        "robotron_steering",
        "faster_when_owned_by_player",
        ),
    SEnum16("detonation_timer_starts", *proj_detonation_timer_starts),
    SEnum16("impact_noise", *gint_constant_sound_volume),
    Float("collision_radius"),
    Float("arming_time"),
    Float("danger_radius"),
    QStruct("timer", INCLUDE=from_to),
    Float("minimum_velocity"),
    Float("maximum_range"),
    Float("detonation_charge_time"),
    SEnum16("detonation_noise", *gint_constant_sound_volume),
    SInt16("super_detonation_projectile_count"),
    Float("super_detonation_delay"),
    h3_dependency("detonation_started"),
    h3_dependency("airborne_detonation_effect"),
    h3_dependency("ground_detonation_effect"),
    h3_dependency("detonation_damage"),
    h3_dependency("attached_detonation_damage"),
    h3_dependency("super_detonation"),
    h3_dependency("super_detonation_damage"),
    h3_dependency("detonation_sound"),
    SEnum8("damage_reporting_type", *proj_damage_reporting_type),
    SInt8("unknown_2", VISIBLE=False),
    SInt8("unknown_3", VISIBLE=False),
    SInt8("unknown_4", VISIBLE=False),
    h3_dependency("attached_super_detonation_damage"),
    Float("material_effect_radius"),
    h3_dependency("flyby_sound"),
    h3_dependency("flyby_response"),
    h3_dependency("impact_effect"),
    h3_dependency("impact_damage"),
    Float("boarding_detonation_time"),
    h3_dependency("boarding_detonation_damage"),
    h3_dependency("boarding_attached_detonation_damage"),
    Float("air_gravity_scale"),
    QStruct("air_damage_range", INCLUDE=from_to),
    Float("water_gravity_scale"),
    QStruct("water_damage_scale", INCLUDE=from_to),
    Float("initial_velocity"),
    Float("final_velocity"),
    Float("unknown_5", VISIBLE=False),
    Float("unknown_6", VISIBLE=False),
    float_rad("guided_angular_velocity_lower"),
    float_rad("guided_angular_velocity_upper"),
    float_rad("unknown_7"),
    QStruct("acceleration_range", INCLUDE=from_to),
    Float("unknown_8", VISIBLE=False),
    BytesRaw("unknown_9", SIZE=4, VISIBLE=False),
    Float("targeted_leading_fraction"),
    BytesRaw("unknown_10", SIZE=4, VISIBLE=False),
    h3_reflexive("material_responses", proj_material_response),
    h3_reflexive("claymore_grenade", proj_claymore_grenade),
    h3_reflexive("firebomb_grenade", proj_firebomb_grenade),
    h3_reflexive("shotgun_properties", proj_shotgun_propertie),
    ENDIAN=">", SIZE=672
    )


def get():
    return proj_def

proj_def = TagDef("proj",
    h3_blam_header('proj'),
    proj_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["proj"], endian=">", tag_cls=H3Tag
    )
