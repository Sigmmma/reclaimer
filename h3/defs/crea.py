############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: DeadCanadian
# 	named some types
# revision: 3		author: Lord Zedd
# 	Portin'
# revision: 4		author: Lord Zedd
# 	Movement physics cleaning.
# revision: 5		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


crea_early_mover_propertie = Struct("early_mover_propertie", 
    h3_string_id("name"),
    Pad(36),
    ENDIAN=">", SIZE=40
    )


crea_ai_propertie = Struct("ai_propertie", 
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


crea_function = Struct("function", 
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


crea_attachment = Struct("attachment", 
    h3_dependency("attachment"),
    h3_string_id("marker"),
    SEnum16("change_color", *bloc_attachment_change_color),
    SInt16("unknown", VISIBLE=False),
    h3_string_id("primary_scale"),
    h3_string_id("secondary_scale"),
    ENDIAN=">", SIZE=32
    )


crea_widget = Struct("widget", 
    h3_dependency("type"),
    ENDIAN=">", SIZE=16
    )


crea_change_color_initial_permutation = Struct("initial_permutation", 
    Pad(4),
    color_rgb_float("color_lower_bound"),
    color_rgb_float("color_upper_bound"),
    h3_string_id("variant_name"),
    ENDIAN=">", SIZE=32
    )


crea_change_color_function = Struct("function", 
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


crea_change_color = Struct("change_color", 
    h3_reflexive("initial_permutations", crea_change_color_initial_permutation),
    h3_reflexive("functions", crea_change_color_function),
    ENDIAN=">", SIZE=24
    )


crea_predicted_resource = Struct("predicted_resource", 
    SInt16("type"),
    SInt16("resource_index"),
    dependency_uint32("tag_index", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=8
    )


crea_multiplayer_object_propertie = Struct("multiplayer_object_propertie", 
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


crea_dead_sphere_shape = Struct("dead_sphere_shape", 
    h3_string_id("name"),
    SInt8("material_index"),
    SInt8("unknown_0", VISIBLE=False),
    SInt16("global_material_index"),
    Float("relative_mass_scale"),
    Float("friction"),
    Float("restitution"),
    Float("volume"),
    Float("mass"),
    SInt16("overall_shape_index"),
    SInt8("phantom_index"),
    SInt8("interaction_unknown"),
    SInt32("unknown_1", VISIBLE=False),
    SInt16("size_0"),
    SInt16("size_1"),
    SInt32("offset_0"),
    SInt32("unknown_2"),
    Float("radius_0"),
    BytesRaw("unknown_3", SIZE=12, VISIBLE=False),
    SInt32("unknown_4", VISIBLE=False),
    SInt16("size_2"),
    SInt16("size_3"),
    SInt32("offset_1"),
    SInt32("unknown_5"),
    Float("radius_1"),
    BytesRaw("unknown_6", SIZE=12, VISIBLE=False),
    QStruct("translation", INCLUDE=ijk_float),
    Float("translation_radius"),
    ENDIAN=">", SIZE=112
    )


crea_pill_shape = Struct("pill_shape", 
    h3_string_id("name"),
    SInt8("material_index"),
    SInt8("unknown_0", VISIBLE=False),
    SInt16("global_material_index"),
    Float("relative_mass_scale"),
    Float("friction"),
    Float("restitution"),
    Float("volume"),
    Float("mass"),
    SInt16("overall_shape_index"),
    SInt8("phantom_index"),
    SInt8("interaction_unknown"),
    SInt32("unknown_1", VISIBLE=False),
    SInt16("size_0"),
    SInt16("size_1"),
    SInt32("offset"),
    SInt32("unknown_2"),
    Float("radius"),
    Pad(12),
    QStruct("bottom", INCLUDE=ijk_float),
    Float("bottom_radius"),
    QStruct("top", INCLUDE=ijk_float),
    Float("top_radius"),
    ENDIAN=">", SIZE=96
    )


crea_sphere_shape = Struct("sphere_shape", 
    h3_string_id("name"),
    SInt8("material_index"),
    SInt8("unknown_0", VISIBLE=False),
    SInt16("global_material_index"),
    Float("relative_mass_scale"),
    Float("friction"),
    Float("restitution"),
    Float("volume"),
    Float("mass"),
    SInt16("overall_shape_index"),
    SInt8("phantom_index"),
    SInt8("interaction_unknown"),
    SInt32("unknown_1", VISIBLE=False),
    SInt16("size_0"),
    SInt16("size_1"),
    SInt32("offset_0"),
    SInt32("unknown_2"),
    Float("radius_0"),
    BytesRaw("unknown_3", SIZE=12, VISIBLE=False),
    SInt32("unknown_4", VISIBLE=False),
    SInt16("size_2"),
    SInt16("size_3"),
    SInt32("offset_1"),
    SInt32("unknown_5"),
    Float("radius_1"),
    BytesRaw("unknown_6", SIZE=12, VISIBLE=False),
    QStruct("translation", INCLUDE=ijk_float),
    Float("translation_radius"),
    ENDIAN=">", SIZE=112
    )


crea_metagame_propertie = Struct("metagame_propertie", 
    Bool8("flags", 
        "must_have_active_seats",
        ),
    SEnum8("unit", *bloc_metagame_propertie_unit),
    SEnum8("classification", *bloc_metagame_propertie_classification),
    SInt8("unknown_0", VISIBLE=False),
    SInt16("points"),
    SInt16("unknown_1", VISIBLE=False),
    ENDIAN=">", SIZE=8
    )


crea_body = Struct("tagdata", 
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
    h3_reflexive("early_mover_properties", crea_early_mover_propertie),
    h3_dependency("creation_effect"),
    h3_dependency("material_effects"),
    h3_dependency("melee_impact"),
    h3_reflexive("ai_properties", crea_ai_propertie),
    h3_reflexive("functions", crea_function),
    SInt16("hud_text_message_index"),
    SInt16("unknown_1", VISIBLE=False),
    h3_reflexive("attachments", crea_attachment),
    h3_reflexive("widgets", crea_widget),
    h3_reflexive("change_colors", crea_change_color),
    h3_reflexive("predicted_resources", crea_predicted_resource),
    h3_reflexive("multiplayer_object_properties", crea_multiplayer_object_propertie),
    Bool32("flags_1", 
        ("infection_form", 1 << 1),
        "immune_to_falling_damage",
        "rotate_while_airborne",
        "zapped_by_shields",
        "attach_upon_impact",
        "not_on_motion_sensor",
        ),
    SEnum16("default_team", *crea_default_team),
    SEnum16("motion_sensor_blip_size", *crea_motion_sensor_blip_size),
    float_rad("turning_velocity_maximum"),
    float_rad("turning_acceleration_maximum"),
    Float("casual_turing_modifer"),
    Float("autoaim_width"),
    Bool32("flags_2", 
        "centered_at_origin",
        "shape_sperical",
        "use_player_physics",
        "climb_any_surface",
        "flying",
        "not_physical",
        "dead_character_collision_group",
        ("never_rests", 1 << 8),
        ),
    Float("height_standing"),
    Float("height_crouching"),
    Float("radius"),
    Float("mass"),
    h3_string_id("living_material_name"),
    h3_string_id("dead_material_name"),
    SInt16("living_global_material_index"),
    SInt16("dead_global_material_index"),
    h3_reflexive("dead_sphere_shapes", crea_dead_sphere_shape),
    h3_reflexive("pill_shapes", crea_pill_shape),
    h3_reflexive("sphere_shapes", crea_sphere_shape),
    float_rad("maximum_slope_angle"),
    float_rad("downhill_falloff_angle"),
    float_rad("downhill_cutoff_angle"),
    float_rad("uphill_falloff_angle"),
    float_rad("uphill_cutoff_angle"),
    Float("downhill_velocity_scale"),
    Float("uphill_velocity_scale"),
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=7, VISIBLE=False),
    Float("falling_velocity_scale"),
    Float("unknown_2", VISIBLE=False),
    float_rad("bank_angle"),
    Float("bank_apply_time"),
    Float("bank_decay_time"),
    Float("pitch_ratio"),
    Float("maximum_velocity"),
    Float("maximum_sidestep_velocity"),
    Float("acceleration"),
    Float("deceleration"),
    float_rad("angular_velocity_maximum"),
    float_rad("angular_acceleration_maximum"),
    Float("crouch_velocity_modifier"),
    BytesRaw("unknown_3", SIZE=4, VISIBLE=False),
    h3_dependency("impact_damage"),
    h3_dependency("impact_shield_damage"),
    h3_reflexive("metagame_properties", crea_metagame_propertie),
    QStruct("destroy_after_death_time", INCLUDE=from_to),
    ENDIAN=">", SIZE=504
    )


def get():
    return crea_def

crea_def = TagDef("crea",
    h3_blam_header('crea'),
    crea_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["crea"], endian=">", tag_cls=H3Tag
    )