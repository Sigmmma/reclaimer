

# ########################################################################
# The element order in all the enumerators is important(DONT SHUFFLE THEM)
# ########################################################################

#Shared Enumerator options
materials_list = (
    "dirt",
    "sand",
    "stone",
    "snow",
    "wood",
    "metal_hollow",
    "metal_thin",
    "metal_thick",
    "rubber",
    "glass",
    "force_field",
    "grunt",
    "hunter_armor",
    "hunter_skin",
    "elite",
    "jackal",
    "jackal_energy_shield",
    "engineer_skin",
    "engineer_force_field",
    "flood_combat_form",
    "flood_carrier_form",
    "cyborg_armor",
    "cyborg_energy_shield",
    "human_armor",
    "human_skin",
    "sentinel",
    "moniter",
    "plastic",
    "water",
    "leaves",
    "elite_energy_shield",
    "ice",
    "hunter_shield",
    )
material_effect_types = (
    "walk",
    "run",
    "sliding",
    "shuffle",
    "jump",
    "jump_land",
    "biped_unused1",
    "biped_unused2",
    "impact",
    "vehicle_tire_slip",
    "vehicle_chassis_slip",
    "vehicle_unused1",
    "vehicle_unused2"
    )
actor_types = (
    "elite",
    "jackal",
    "grunt",
    "hunter",
    "engineer",
    "assassin",
    "player",
    "marine",
    "crew",
    "combat_form",
    "infection_form",
    "carrier_form",
    "moniter",
    "sentinal",
    "none",
    "mounted_weapon"
    )
animation_functions = (
    "one",
    "zero",
    "cosine",
    "cosine_variable_period",
    "diagonal_wave",
    "diagonal_wave_variable_period",
    "slide",
    "slide_variable_period",
    "noise",
    "jitter",
    "wander",
    "spark",
    )
sound_volumes = (
    "silent",
    "medium",
    "loud",
    "shout",
    "quiet"
    )
damage_category = (
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
grenade_types = (
    'human_frag',
    'covenant_plasma'
    )
fade_functions = (
    "linear",
    "early",
    "very_early",
    "late",
    "very_late",
    "cosine",
    )
detail_map_functions = (
    "double_biased_multiply",
    "multiply",
    "double_biased_add",
    )
device_functions = (
    "none",
    "power",
    "change_in_power",
    "position",
    "change_in_position",
    "locked",
    "delay",
    )
render_anchor = (
    "with_primary",
    "with_screen_space",
    "with_zsprite"
    )
render_fade_mode = (
    "none",
    "fade_when_perpendicular",
    "fade_when_parallel",
    )
render_mode = (
    "screen_facing",
    "parallel_to_direction",
    "perpendicular_to_direction"
    )
shader_flags = (
    "sort_bias",
    "nonlinear_tint",
    "dont_overdraw_fp_weapon"
    )
blend_flags = (
    "blend_in_hsv",
    "more_colors"
    )
hud_scaling_flags = (
    "dont_scale_offset",
    "dont_scale_size",
    "use_high_res_scale"
    )
hud_flash_flags = (
    "reverse_default_and_flashing_colors",
    )
hud_anchors = (
    "top_left",
    "top_right",
    "bottom_left",
    "bottom_right",
    "center"
    )
hud_panel_meter_flags = (
    "use_min_max_for_state_changes",
    "interpolate_between_min_max_flash_colors",
    "interpolate_color_along_hsv_space",
    "more_colors_for_hsv_interpolation ",
    "invert_interpolation"
    )
multitex_anchors = (
    "texture",
    "screen",
    )
multitex_wrap_modes = (
    "clamp",
    "wrap",
    )
blending_funcs = (
    "add",
    "subtract",
    "multiply",
    "multiply_2x",
    "dot",
    )
blend_functions = (
    "current",
    "next_map",
    "multiply",
    "double_multiply",
    "add",
    "add_signed_current",
    "add_signed_next_map",
    "subtract_signed_current",
    "subtract_signed_next_map",
    "blend_current_alpha",
    "blend_current_alpha_inverse",
    "blend_next_map_alpha",
    "blend_next_map_alpha_inverse",
    )
framebuffer_blend_functions = (
    "alpha_blend",
    "multiply",
    "double_multiply",
    "add",
    "subtract",
    "component_min",
    "component_max",
    "alpha_multiply_add",
    )

# DO NOT MODIFY ANY OF THESE SCRIPT ENUMS.
# The exact lettering is important as the script extractor uses
# these strings to reconstruct scripts
script_types = (
    "startup",
    "dormant",
    "continuous",
    "static",
    "stub",
    )
script_object_types = (
    "unparsed",
    "special form",
    "function name",
    "passthrough",
    "void",
    "boolean",
    "real",
    "short",
    "long",

# DO NOT MODIFY ANY OF THESE SCRIPT ENUMS.
# The exact lettering is important as the script extractor
# uses these strings to reconstruct scripts

    "string",
    "script",

    "trigger_volume",
    "cutscene_flag",
    "cutscene_camera_point",
    "cutscene_title",
    "cutscene_recording",

    "device_group",
    "ai",
    "ai_command_list",
    "starting_profile",

    "conversation",
    "navpoint",
    "hud_message",
    "object_list",

    "sound",
    "effect",
    "damage",
    "looping_sound",
    "animation_graph",
    "actor_variant",
    "damage_effect",

    "object_definition",
    "game_difficulty",
    "team",
    "ai_default_state",
    "actor_type",
    "hud_corner",

    "object",
    "unit",
    "vehicle",
    "weapon",
    "device",
    "scenery",

    "object_name",
    "unit_name",
    "vehicle_name",
    "weapon_name",
    "device_name",
    "scenery_name"
    )


function_names = (
    "none",
    "A",
    "B",
    "C",
    "D",
    )
function_inputs_outputs = (
    "none",
    "A_in",
    "B_in",
    "C_in",
    "D_in",
    "A_out",
    "B_out",
    "C_out",
    "D_out",
    )
function_inputs = (
    "none",
    "A_in",
    "B_in",
    "C_in",
    "D_in",
    )
function_outputs = (
    "none",
    "A_out",
    "B_out",
    "C_out",
    "D_out",
    )
#Tag class specific enumerators
object_export_to = (
    'none',
    'body_vitality',
    'shield_vitality',
    'recent_body_damage',
    'recent_shield_damage',
    'random_constant',
    'umbrella_shield_vitality',
    'shield_stun',
    'recent_umbrella_shield_vitality',
    'umbrella_shield_stun',
    'region_0_damage',
    'region_1_damage',
    'region_2_damage',
    'region_3_damage',
    'region_4_damage',
    'region_5_damage',
    'region_6_damage',
    'region_7_damage',
    'alive',
    'compass',
    )
weapon_export_to = (
    'none',
    'heat',
    'primary_ammunition',
    'secondary_ammunition',
    'primary_rate_of_fire',
    'secondary_rate_of_fire',
    'ready',
    'primary_ejection_port',
    'secondary_ejection_port',
    'overheated',
    'primary_charged',
    'secondary_charged',
    'illumination',
    'age',
    'integrated_light',
    'primary_firing',
    'secondary_firing',
    'primary_firing_on',
    'secondary_firing_on',
    )
biped_inputs = (
    'none',
    'flying_velocity'
    )
projectile_inputs = (
    "none",
    "range_remaining",
    "time_remaining",
    "tracer",
    )
unit_inputs = (
    "none",
    "driver_seat_power",
    "gunner_seat_power",
    "aiming_change",
    "mouth_aperture",
    "integrated_light_power",
    "can_blink",
    "shield_sapping"
    )
unit_teams = (
    "none",
    "player",
    "human",
    "covenant",
    "flood",
    "sentinel",
    "unused6",
    "unused7",
    "unused8",
    "unused9",
    )
vehicle_inputs = (
    "none",
    "speed_absolute",
    "speed_forward",
    "speed_backward",
    "slide_absolute",
    "slide_left",
    "slide_right",
    "speed_slide_maximum",
    "turn_absolute",
    "turn_left",
    "turn_right",
    "crouch",
    "jump",
    "walk",
    "velocity_air",
    "velocity_water",
    "velocity_ground",
    "velocity_forward",
    "velocity_left",
    "velocity_up",
    "left_tread_position",
    "right_tread_position",
    "left_tread_velocity",
    "right_tread_velocity",
    "front_left_tire_position",
    "front_right_tire_position",
    "back_left_tire_position",
    "back_right_tire_position",
    "front_left_tire_velocity",
    "front_right_tire_velocity",
    "back_left_tire_velocity",
    "back_right_tire_velocity",
    "wingtip_contrail",
    "hover",
    "thrust",
    "engine_hack",
    "wingtip_contrail_new",
    )
vehicle_types = (
    "human_tank",
    "human_jeep",
    "human_boat",
    "human_plane",
    "alien_scout",
    "alien_fighter",
    "turret",
    )
weapon_types = (
    "undefined",
    "shotgun",
    "needler",
    "plasma_pistol",
    "plasma_rifle",
    )
trans_shdr_properties = (
    "alpha_tested",
    "decal",
    "two_sided",
    "first_map_is_in_screenspace",
    "draw_before_water",
    "ignore_effect",
    "scale_first_map_with_distance",
    "numeric",
    )
trans_shdr_first_map_type = (
    "map_2d",
    "reflection_cube_map",
    "object_centered_cube_map",
    "viewer_centered_cube_map",
    )
detail_mask = (
    "none",
    "reflection_mask_inverse",
    "reflection_mask",
    "self_illumination_mask_inverse",
    "self_illumination_mask",
    "color_change_mask_inverse",
    "color_change_mask",
    "auxiliary_mask_inverse",
    "auxiliary_mask"
    )
anim_types = (
    "base",
    "overlay",
    "replacement"
    )
anim_frame_info_types = (
    "none",
    "dx,dy",
    "dx,dy,dyaw",
    "dx,dy,dz,dyaw",
    )


# ########################################################################
# The element order in all the enumerators is important(DONT SHUFFLE THEM)
# ########################################################################

#Shared Enumerator options
grenade_types_os = (
    'human frag',
    'covenant plasma',
    'custom 2',
    'custom 3',
    )

actor_states = (
    'none',
    'sleeping',
    'alert',
    'moving repeat same position',
    'moving loop',
    'moving loop back and forth',
    'moving loop randomly',
    'moving randomly',
    'guarding',
    'guarding at guard position',
    'searching',
    'fleeing'
    )
