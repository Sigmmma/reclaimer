from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

proj_ai_propertie_leap_jump_speed = (
    "none",
    "down",
    "step",
    "crouch",
    "stand",
    "storey",
    "tower",
    "infinite",
    )

proj_ai_propertie_size = (
    "default",
    "tiny",
    "small",
    "medium",
    "large",
    "huge",
    "immobile",
    )

proj_attachment_change_color = (
    "none",
    "primary",
    "secondary",
    "tertiary",
    "quaternary",
    )

proj_damage_reporting_type = (
    "guardians",
    "falling_damage",
    "collision",
    "melee",
    "explosion",
    "magnum",
    "plasma_pistol",
    "needler",
    "mauler",
    "smg",
    "plasma_rifle",
    "battle_rifle",
    "carbine",
    "shotgun",
    "sniper_rifle",
    "beam_rifle",
    "assault_rifle",
    "spiker",
    "fuel_rod_cannon",
    "missile_pod",
    "rocket_launcher",
    "spartan_laser",
    "brute_shot",
    "flamethrower",
    "sentinel_gun",
    "energy_sword",
    "gravity_hammer",
    "frag_grenade",
    "plasma_grenade",
    "spike_grenade",
    "firebomb_grenade",
    "flag",
    "bomb",
    "bomb_explosion",
    "ball",
    "machinegun_turret",
    "plasma_cannon",
    "plasma_mortar",
    "plasma_turret",
    "banshee",
    "ghost",
    "mongoose",
    "scorpion",
    "scorpion_gunner",
    "spectre",
    "spectre_gunner",
    "warthog",
    "warthog_gunner",
    "warthog_gauss_turret",
    "wraith",
    "wraith_gunner",
    "tank",
    "chopper",
    "hornet",
    "mantis",
    "prowler",
    "sentinel_beam",
    "sentinel_rpg",
    "teleporter",
    "tripmine",
    "elephant_turret",
    )

proj_detonation_timer_starts = (
    "immediately",
    "after_first_bounce",
    "when_at_rest",
    "after_first_bounce_off_any_surface",
    )

proj_impact_noise = (
    "silent",
    "medium",
    "loud",
    "shout",
    "quiet",
    )

proj_lightmap_shadow_mode_size = (
    "default",
    "never",
    "always",
    "unknown",
    )

proj_material_response_response = (
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

proj_multiplayer_object_propertie_object_type = (
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

proj_multiplayer_object_propertie_shape = (
    "none",
    "sphere",
    "cylinder",
    "box",
    )

proj_multiplayer_object_propertie_spawn_timer_mode = (
    "on_death",
    "on_disturbance",
    )

proj_object_type = (
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

proj_sweetener_size = (
    "small",
    "medium",
    "large",
    )

proj_water_density = (
    "default",
    "least",
    "some",
    "equal",
    "more",
    "more_still",
    "lots_more",
    )


proj_early_mover_propertie = Struct("early_mover_properties",
    string_id_meta("name"),
    Pad(36),
    ENDIAN=">", SIZE=40
    )


proj_ai_propertie = Struct("ai_properties",
    Bool32("flags",
        "destroyable_cover",
        "pathfinding_ignore_when_dead",
        "dynamic_cover",
        ),
    string_id_meta("ai_type_name"),
    Pad(4),
    SEnum16("size", *proj_ai_propertie_size),
    SEnum16("leap_jump_speed", *proj_ai_propertie_leap_jump_speed),
    ENDIAN=">", SIZE=16
    )


proj_function = Struct("functions",
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


proj_attachment = Struct("attachments",
    dependency("attachment"),
    string_id_meta("marker"),
    SEnum16("change_color", *proj_attachment_change_color),
    SInt16("unknown"),
    string_id_meta("primary_scale"),
    string_id_meta("secondary_scale"),
    ENDIAN=">", SIZE=32
    )


proj_widget = Struct("widgets",
    dependency("type"),
    ENDIAN=">", SIZE=16
    )


proj_change_color_initial_permutation = Struct("initial_permutations",
    Pad(4),
    color_rgb_float("color_lower_bound"),
    color_rgb_float("color_upper_bound"),
    string_id_meta("variant_name"),
    ENDIAN=">", SIZE=32
    )


proj_change_color_function = Struct("functions",
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


proj_change_color = Struct("change_colors",
    reflexive("initial_permutations", proj_change_color_initial_permutation),
    reflexive("functions", proj_change_color_function),
    ENDIAN=">", SIZE=24
    )


proj_predicted_resource = Struct("predicted_resources",
    SInt16("type"),
    SInt16("resource_index"),
    UInt32("tag_index"),
    ENDIAN=">", SIZE=8
    )


proj_multiplayer_object_propertie = Struct("multiplayer_object_properties",
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
    SEnum8("object_type", *proj_multiplayer_object_propertie_object_type),
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
    SEnum8("shape", *proj_multiplayer_object_propertie_shape),
    SEnum8("spawn_timer_mode", *proj_multiplayer_object_propertie_spawn_timer_mode),
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


proj_material_response = Struct("material_responses",
    Bool16("flags",
        "cannot_be_overpenetrated",
        ),
    SEnum16("response", *proj_material_response_response),
    string_id_meta("material_name"),
    SInt16("global_material_index"),
    SInt16("unknown"),
    SEnum16("response_1", *proj_material_response_response),
    Bool16("flags_1",
        "only_against_units",
        "never_against_units",
        ),
    Float("chance_fraction"),
    float_rad("between_angle_min"),
    float_rad("between_angle_max"),
    Float("and_velocity_min"),
    Float("and_velocity_max"),
    SEnum16("scale_effects_by", *proj_material_response_scale_effects_by),
    SInt16("unknown_1"),
    float_rad("angular_noise"),
    Float("velocity_noise"),
    Float("initial_friction"),
    Float("maximum_distance"),
    Float("parallel_friction"),
    Float("perpendicular_friction"),
    ENDIAN=">", SIZE=64
    )


proj_claymore_grenade = Struct("claymore_grenade",
    float_rad("unknown"),
    float_rad("unknown_1"),
    float_rad("unknown_2"),
    Float("unknown_3"),
    Float("unknown_4"),
    Float("unknown_5"),
    Float("unknown_6"),
    Float("unknown_7"),
    Float("unknown_8"),
    Float("unknown_9"),
    Float("unknown_10"),
    Float("unknown_11"),
    ENDIAN=">", SIZE=48
    )


proj_firebomb_grenade = Struct("firebomb_grenade",
    Float("unknown"),
    ENDIAN=">", SIZE=4
    )


proj_shotgun_propertie = Struct("shotgun_properties",
    SInt16("amount"),
    SInt16("distance"),
    Float("accuracy"),
    float_rad("spread_cone_angle"),
    ENDIAN=">", SIZE=12
    )


proj_meta_def = BlockDef("proj",
    SEnum16("object_type", *proj_object_type),
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
    SEnum16("lightmap_shadow_mode_size", *proj_lightmap_shadow_mode_size),
    SEnum8("sweetener_size", *proj_sweetener_size),
    SEnum8("water_density", *proj_water_density),
    SInt32("unknown"),
    Float("dynamic_light_sphere_radius"),
    Float("dynamic_light_sphere_offset_x"),
    Float("dynamic_light_sphere_offset_y"),
    Float("dynamic_light_sphere_offset_z"),
    string_id_meta("default_model_variant"),
    dependency("model"),
    dependency("crate_object"),
    dependency("collision_damage"),
    reflexive("early_mover_properties", proj_early_mover_propertie),
    dependency("creation_effect"),
    dependency("material_effects"),
    dependency("melee_impact"),
    reflexive("ai_properties", proj_ai_propertie),
    reflexive("functions", proj_function),
    SInt16("hud_text_message_index"),
    SInt16("unknown_1"),
    reflexive("attachments", proj_attachment),
    reflexive("widgets", proj_widget),
    reflexive("change_colors", proj_change_color),
    reflexive("predicted_resources", proj_predicted_resource),
    reflexive("multiplayer_object_properties", proj_multiplayer_object_propertie),
    Bool32("flags_1",
        "oriented_along_velocity",
        "ai_must_use_ballistic_aiming",
        "detonation_max_time_if_attached",
        "has_super_combining_explosion",
        "damage_scales_based_on_distance",
        "travels_instantaneously",
        "steering_adjusts_orientation",
        "don_t_noise_up_steering",
        "can_track_behind_itself",
        "robotron_steering",
        "faster_when_owned_by_player",
        ),
    SEnum16("detonation_timer_starts", *proj_detonation_timer_starts),
    SEnum16("impact_noise", *proj_impact_noise),
    Float("collision_radius"),
    Float("arming_time"),
    Float("danger_radius"),
    Float("timer_min"),
    Float("timer_max"),
    Float("minimum_velocity"),
    Float("maximum_range"),
    Float("detonation_charge_time"),
    SEnum16("detonation_noise", *proj_impact_noise),
    SInt16("super_detonation_projectile_count"),
    Float("super_detonation_delay"),
    dependency("detonation_started"),
    dependency("airborne_detonation_effect"),
    dependency("ground_detonation_effect"),
    dependency("detonation_damage"),
    dependency("attached_detonation_damage"),
    dependency("super_detonation"),
    dependency("super_detonation_damage"),
    dependency("detonation_sound"),
    SEnum8("damage_reporting_type", *proj_damage_reporting_type),
    SInt8("unknown_2"),
    SInt8("unknown_3"),
    SInt8("unknown_4"),
    dependency("attached_super_detonation_damage"),
    Float("material_effect_radius"),
    dependency("flyby_sound"),
    dependency("flyby_response"),
    dependency("impact_effect"),
    dependency("impact_damage"),
    Float("boarding_detonation_time"),
    dependency("boarding_detonation_damage"),
    dependency("boarding_attached_detonation_damage"),
    Float("air_gravity_scale"),
    Float("air_damage_range_min"),
    Float("air_damage_range_max"),
    Float("water_gravity_scale"),
    Float("water_damage_scale_min"),
    Float("water_damage_scale_max"),
    Float("initial_velocity"),
    Float("final_velocity"),
    Float("unknown_5"),
    Float("unknown_6"),
    float_rad("guided_angular_velocity_lower"),
    float_rad("guided_angular_velocity_upper"),
    float_rad("unknown_7"),
    Float("acceleration_range_min"),
    Float("acceleration_range_max"),
    Float("unknown_8"),
    Pad(4),
    Float("targeted_leading_fraction"),
    Pad(4),
    reflexive("material_responses", proj_material_response),
    reflexive("claymore_grenade", proj_claymore_grenade),
    reflexive("firebomb_grenade", proj_firebomb_grenade),
    reflexive("shotgun_properties", proj_shotgun_propertie),
    TYPE=Struct, ENDIAN=">", SIZE=672
    )