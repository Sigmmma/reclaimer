from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

ssce_ai_propertie_leap_jump_speed = (
    "none",
    "down",
    "step",
    "crouch",
    "stand",
    "storey",
    "tower",
    "infinite",
    )

ssce_ai_propertie_size = (
    "default",
    "tiny",
    "small",
    "medium",
    "large",
    "huge",
    "immobile",
    )

ssce_attachment_change_color = (
    "none",
    "primary",
    "secondary",
    "tertiary",
    "quaternary",
    )

ssce_lightmap_shadow_mode_size = (
    "default",
    "never",
    "always",
    "unknown",
    )

ssce_multiplayer_object_propertie_object_type = (
    "ordinary",
    "weapon",
    "grenade",
    "projectile",
    "powerup",
    "equipment",
    "light_land_vehicle",
    "heavy_land_vehicle",
    "flying_vehicle",
    "teleporter_2way",
    "teleporter_sender",
    "teleporter_receiver",
    "player_spawn_location",
    "player_respawn_zone",
    "hold_spawn_objective",
    "capture_spawn_objective",
    "hold_destination_objective",
    "capture_destination_objective",
    "hill_objective",
    "infection_haven_objective",
    "territory_objective",
    "vip_boundary_objective",
    "vip_destination_objective",
    "juggernaut_destination_objective",
    )

ssce_multiplayer_object_propertie_shape = (
    "none",
    "sphere",
    "cylinder",
    "box",
    )

ssce_multiplayer_object_propertie_spawn_timer_mode = (
    "on_death",
    "on_disturbance",
    )

ssce_object_type = (
    "biped",
    "vehicle",
    "weapon",
    "equipment",
    "terminal",
    "projectile",
    "scenery",
    "machine",
    "control",
    "sound_scenery",
    "crate",
    "creature",
    "giant",
    "effect_scenery",
    )

ssce_sweetener_size = (
    "small",
    "medium",
    "large",
    )

ssce_water_density = (
    "default",
    "least",
    "some",
    "equal",
    "more",
    "more_still",
    "lots_more",
    )


ssce_early_mover_propertie = Struct("early_mover_properties",
    string_id_meta("name"),
    Pad(36),
    ENDIAN=">", SIZE=40
    )


ssce_ai_propertie = Struct("ai_properties",
    Bool32("flags",
        "destroyable_cover",
        "pathfinding_ignore_when_dead",
        "dynamic_cover",
        ),
    string_id_meta("ai_type_name"),
    Pad(4),
    SEnum16("size", *ssce_ai_propertie_size),
    SEnum16("leap_jump_speed", *ssce_ai_propertie_leap_jump_speed),
    ENDIAN=">", SIZE=16
    )


ssce_function = Struct("functions",
    Bool32("flags",
        "invert",
        "mapping_does_not_controls_active",
        "always_active",
        "random_time_offset",
        ),
    string_id_meta("import_name"),
    string_id_meta("export_name"),
    string_id_meta("turn_off_with"),
    Float("minimum_value"),
    rawdata_ref("default_function"),
    string_id_meta("scale_by"),
    ENDIAN=">", SIZE=44
    )


ssce_attachment = Struct("attachments",
    dependency("attachment"),
    string_id_meta("marker"),
    SEnum16("change_color", *ssce_attachment_change_color),
    SInt16("unknown"),
    string_id_meta("primary_scale"),
    string_id_meta("secondary_scale"),
    ENDIAN=">", SIZE=32
    )


ssce_widget = Struct("widgets",
    dependency("type"),
    ENDIAN=">", SIZE=16
    )


ssce_change_color_initial_permutation = Struct("initial_permutations",
    Pad(4),
    color_rgb_float("color_lower_bound"),
    color_rgb_float("color_upper_bound"),
    string_id_meta("variant_name"),
    ENDIAN=">", SIZE=32
    )


ssce_change_color_function = Struct("functions",
    Bool32("scale_flags",
        "blend_in_hsv",
        "more_colors",
        ),
    color_rgb_float("color_lower_bound"),
    color_rgb_float("color_upper_bound"),
    string_id_meta("darken_by"),
    string_id_meta("scale_by"),
    ENDIAN=">", SIZE=32
    )


ssce_change_color = Struct("change_colors",
    reflexive("initial_permutations", ssce_change_color_initial_permutation),
    reflexive("functions", ssce_change_color_function),
    ENDIAN=">", SIZE=24
    )


ssce_predicted_resource = Struct("predicted_resources",
    SInt16("type"),
    SInt16("resource_index"),
    UInt32("tag_index"),
    ENDIAN=">", SIZE=8
    )


ssce_multiplayer_object_propertie = Struct("multiplayer_object_properties",
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
    SEnum8("object_type", *ssce_multiplayer_object_propertie_object_type),
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
    SEnum8("shape", *ssce_multiplayer_object_propertie_shape),
    SEnum8("spawn_timer_mode", *ssce_multiplayer_object_propertie_spawn_timer_mode),
    SInt16("spawn_time"),
    SInt16("abandon_time"),
    Float("radius_width"),
    Float("length"),
    Float("top"),
    Float("bottom"),
    Float("unknown"),
    Float("unknown_1"),
    Float("unknown_2"),
    SInt32("unknown_3"),
    SInt32("unknown_4"),
    dependency("child_object"),
    SInt32("unknown_5"),
    dependency("shape_shader"),
    dependency("unknown_shader"),
    dependency("unknown_6"),
    dependency("unknown_7"),
    dependency("unknown_8"),
    dependency("unknown_9"),
    dependency("unknown_10"),
    dependency("unknown_11"),
    ENDIAN=">", SIZE=196
    )


ssce_meta_def = BlockDef("ssce",
    SEnum16("object_type", *ssce_object_type),
    Bool16("flags",
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
    Float("bounding_offset_x"),
    Float("bounding_offset_y"),
    Float("bounding_offset_z"),
    Float("acceleration_scale"),
    SEnum16("lightmap_shadow_mode_size", *ssce_lightmap_shadow_mode_size),
    SEnum8("sweetener_size", *ssce_sweetener_size),
    SEnum8("water_density", *ssce_water_density),
    SInt32("unknown"),
    Float("dynamic_light_sphere_radius"),
    Float("dynamic_light_sphere_offset_x"),
    Float("dynamic_light_sphere_offset_y"),
    Float("dynamic_light_sphere_offset_z"),
    string_id_meta("default_model_variant"),
    dependency("model"),
    dependency("crate_object"),
    dependency("collision_damage"),
    reflexive("early_mover_properties", ssce_early_mover_propertie),
    dependency("creation_effect"),
    dependency("material_effects"),
    dependency("melee_impact"),
    reflexive("ai_properties", ssce_ai_propertie),
    reflexive("functions", ssce_function),
    SInt16("hud_text_message_index"),
    SInt16("unknown_1"),
    reflexive("attachments", ssce_attachment),
    reflexive("widgets", ssce_widget),
    reflexive("change_colors", ssce_change_color),
    reflexive("predicted_resources", ssce_predicted_resource),
    reflexive("multiplayer_object_properties", ssce_multiplayer_object_propertie),
    Float("distance_min"),
    Float("distance_max"),
    float_rad("cone_angle_min"),
    float_rad("cone_angle_max"),
    TYPE=Struct, ENDIAN=">", SIZE=264
    )