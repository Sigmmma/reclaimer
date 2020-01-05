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
# revision: 2		author: DarkShallFall
# 	Values, Attachments. Effects, Projectile, jpt!, Impact sound, Pickup Sound, Activation Sound, HUD, and other small things
# revision: 3		author: DeadCanadian
# 	fixed the death properties
# revision: 4		author: Lord Zedd
# 	Portin'
# revision: 5		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef

eqip_powerup_powerup_trait_set = (
    "red",
    "blue",
    "yellow",
    )


eqip_early_mover_propertie = Struct("early_mover_propertie",
    h3_string_id("name"),
    Pad(36),
    ENDIAN=">", SIZE=40
    )


eqip_ai_propertie = Struct("ai_propertie",
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


eqip_function = Struct("function",
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


eqip_attachment = Struct("attachment",
    h3_dependency("attachment"),
    h3_string_id("marker"),
    SEnum16("change_color", *bloc_attachment_change_color),
    SInt16("unknown", VISIBLE=False),
    h3_string_id("primary_scale"),
    h3_string_id("secondary_scale"),
    ENDIAN=">", SIZE=32
    )


eqip_widget = Struct("widget",
    h3_dependency("type"),
    ENDIAN=">", SIZE=16
    )


eqip_change_color_initial_permutation = Struct("initial_permutation",
    Pad(4),
    color_rgb_float("color_lower_bound"),
    color_rgb_float("color_upper_bound"),
    h3_string_id("variant_name"),
    ENDIAN=">", SIZE=32
    )


eqip_change_color_function = Struct("function",
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


eqip_change_color = Struct("change_color",
    h3_reflexive("initial_permutations", eqip_change_color_initial_permutation),
    h3_reflexive("functions", eqip_change_color_function),
    ENDIAN=">", SIZE=24
    )


eqip_predicted_resource = Struct("predicted_resource",
    SInt16("type"),
    SInt16("resource_index"),
    dependency_uint32("tag_index", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=8
    )


eqip_multiplayer_object_propertie = Struct("multiplayer_object_propertie",
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


eqip_predicted_bitmap = Struct("predicted_bitmap",
    h3_dependency("bitmap", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


eqip_health_pack = Struct("health_pack",
    Float("unknown_0", VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    Float("shields_given"),
    h3_dependency("unknown_2"),
    h3_dependency("unknown_3"),
    h3_dependency("unknown_4"),
    ENDIAN=">", SIZE=60
    )


eqip_powerup = Struct("powerup",
    SEnum32("powerup_trait_set", *eqip_powerup_powerup_trait_set),
    ENDIAN=">", SIZE=4
    )


eqip_object_creation = Struct("object_creation",
    h3_dependency("object"),
    h3_dependency("unknown_0"),
    Float("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    Float("unknown_3", VISIBLE=False),
    Float("object_force"),
    Float("unknown_4", VISIBLE=False),
    ENDIAN=">", SIZE=52
    )


eqip_destruction = Struct("destruction",
    h3_dependency("destroy_effect"),
    h3_dependency("destroy_damage_effect"),
    Float("unknown_0", VISIBLE=False),
    Float("self_destruction_time"),
    Float("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    ENDIAN=">", SIZE=48
    )


eqip_radar_manipulation = Struct("radar_manipulation",
    Float("unknown_0", VISIBLE=False),
    Float("fake_blip_radius"),
    SInt32("fake_blip_count"),
    Float("unknown_1", VISIBLE=False),
    ENDIAN=">", SIZE=16
    )


eqip_invisibility = Struct("invisibility",
    Float("unknown_0"),
    Float("unknown_1"),
    ENDIAN=">", SIZE=8
    )


eqip_invincibility = Struct("invincibility",
    h3_string_id("material_name"),
    SInt16("global_material_index"),
    SInt16("unknown_0", VISIBLE=False),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    h3_dependency("activation_effect"),
    h3_dependency("active_effect"),
    h3_dependency("deactivation_effect"),
    ENDIAN=">", SIZE=60
    )


eqip_regenerator = Struct("regenerator",
    Float("unknown"),
    ENDIAN=">", SIZE=4
    )


eqip_body = Struct("tagdata",
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
    h3_reflexive("early_mover_properties", eqip_early_mover_propertie),
    h3_dependency("creation_effect"),
    h3_dependency("material_effects"),
    h3_dependency("melee_impact"),
    h3_reflexive("ai_properties", eqip_ai_propertie),
    h3_reflexive("functions", eqip_function),
    SInt16("hud_text_message_index"),
    SInt16("unknown_1", VISIBLE=False),
    h3_reflexive("attachments", eqip_attachment),
    h3_reflexive("widgets", eqip_widget),
    h3_reflexive("change_colors", eqip_change_color),
    h3_reflexive("predicted_resources", eqip_predicted_resource),
    h3_reflexive("multiplayer_object_properties", eqip_multiplayer_object_propertie),
    Bool32("flags_1",
        "always_maintains_z_up",
        "destroyed_by_explosions",
        "unaffected_by_gravity",
        ),
    SInt16("old_message_index"),
    SInt16("sort_order"),
    Float("old_multiplayer_on_ground_scale"),
    Float("old_campaign_on_ground_scale"),
    h3_string_id("pickup_message"),
    h3_string_id("swap_message"),
    h3_string_id("pickup_or_dual_wield_message"),
    h3_string_id("swap_or_dual_wield_message"),
    h3_string_id("picked_up_message"),
    h3_string_id("switch_to_message"),
    h3_string_id("switch_to_from_ai_message"),
    h3_string_id("all_weapons_empty_message"),
    h3_dependency("collision_sound"),
    h3_reflexive("predicted_bitmaps", eqip_predicted_bitmap),
    h3_dependency("detonation_damage_effect"),
    QStruct("detonation_delay", INCLUDE=from_to),
    h3_dependency("detonating_effect"),
    h3_dependency("detonation_effect"),
    Float("campaign_ground_scale"),
    Float("multiplayer_ground_scale"),
    Float("small_hold_scale"),
    Float("small_holster_scale"),
    Float("medium_hold_scale"),
    Float("medium_holster_scale"),
    Float("large_hold_scale"),
    Float("large_holster_scale"),
    Float("huge_hold_scale"),
    Float("huge_holster_scale"),
    Float("grounded_friction_length"),
    Float("grounded_friction_unknown"),
    Float("use_duration"),
    Float("unknown_2", VISIBLE=False),
    SInt16("number_of_uses"),
    Bool16("flags_2", *unknown_flags_16),
    Float("unknown_3", VISIBLE=False),
    Float("unknown_4", VISIBLE=False),
    Float("unknown_5", VISIBLE=False),
    h3_reflexive("health_pack", eqip_health_pack),
    h3_reflexive("powerup", eqip_powerup),
    h3_reflexive("object_creation", eqip_object_creation),
    h3_reflexive("destruction", eqip_destruction),
    h3_reflexive("radar_manipulation", eqip_radar_manipulation),
    BytesRaw("null", SIZE=12, VISIBLE=False),
    h3_reflexive("invisibility", eqip_invisibility),
    h3_reflexive("invincibility", eqip_invincibility),
    h3_reflexive("regenerator", eqip_regenerator),
    h3_dependency("hud_interface"),
    h3_dependency("pickup_sound"),
    h3_dependency("activation_effect"),
    h3_dependency("active_effect"),
    h3_dependency("deactivation_effect"),
    ENDIAN=">", SIZE=640
    )


def get():
    return eqip_def

eqip_def = TagDef("eqip",
    h3_blam_header('eqip'),
    eqip_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["eqip"], endian=">", tag_cls=H3Tag
    )
