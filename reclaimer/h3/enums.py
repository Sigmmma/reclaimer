#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.enums import *

play_raw_page_compression_codec = (
    "deflate",
    "lzx",
    ("NONE", -1)
    )

bloc_ai_propertie_leap_jump_speed = (
    "none",
    "down",
    "step",
    "crouch",
    "stand",
    "storey",
    "tower",
    "infinite",
    )

bloc_ai_propertie_size = (
    "default",
    "tiny",
    "small",
    "medium",
    "large",
    "huge",
    "immobile",
    )

bloc_attachment_change_color = (
    "none",
    "primary",
    "secondary",
    "tertiary",
    "quaternary",
    )

bloc_lightmap_shadow_mode_size = (
    "default",
    "never",
    "always",
    "unknown",
    )

bloc_metagame_propertie_classification = (
    "infantry",
    "leader",
    "hero",
    "specialist",
    "light_vehicle",
    "heavy_vehicle",
    "giant_vehicle",
    "standard_vehicle",
    )

bloc_metagame_propertie_unit = (
    "brute",
    "grunt",
    "jackal",
    "marine",
    "bugger",
    "hunter",
    "flood_infection",
    "flood_carrier",
    "flood_combat",
    "flood_pureform",
    "sentinel",
    "elite",
    "turret",
    "mongoose",
    "warthog",
    "scorpion",
    "hornet",
    "pelican",
    "shade",
    "watchtower",
    "ghost",
    "chopper",
    "mauler",
    "wraith",
    "banshee",
    "phantom",
    "scarab",
    "guntower",
    )

bloc_multiplayer_object_propertie_object_type = (
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

bloc_multiplayer_object_propertie_shape = (
    "none",
    "sphere",
    "cylinder",
    "box",
    )

bloc_multiplayer_object_propertie_spawn_timer_mode = (
    "on_death",
    "on_disturbance",
    )

bloc_object_type = (
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

bloc_sweetener_size = (
    "small",
    "medium",
    "large",
    )

bloc_water_density = (
    "default",
    "least",
    "some",
    "equal",
    "more",
    "more_still",
    "lots_more",
    )

bmp3_blend_method = (
    "standard",
    "unknown_0",
    "unknown_1",
    "alpha",
    "overlay",
    "unknown_2",
    "lighter_color",
    "unknown_3",
    "unknown_4",
    "unknown_5",
    "inverted_alpha",
    "unknown_6",
    "unknown_7",
    "unknown_8",
    )

cntl_contrail_system_output_kind_0 = (
    "none",
    "plus",
    "times",
    )

crea_default_team = (
    "default",
    "player",
    "human",
    "covenant",
    "flood",
    "sentinel",
    "heretic",
    "prophet",
    "guilty",
    "unused9",
    "unused10",
    "unused11",
    "unused12",
    "unused13",
    "unused14",
    "unused15",
    )

crea_motion_sensor_blip_size = (
    "medium",
    "small",
    "large",
    )

gint_constant_sound_volume = (
    "silent",
    "medium",
    "loud",
    "shout",
    "quiet",
    )

gint_grenade_type = (
    "human_fragmentation",
    "covenant_plasma",
    "brute_spike",
    "firebomb",
    )

gint_item_scale = (
    "small",
    "medium",
    "large",
    "huge",
    )

gint_seat_ai_seat_type = (
    "none",
    "passenger",
    "gunner",
    "small_cargo",
    "large_cargo",
    "driver",
    )

jpt__player_response_fade_function = (
    "linear",
    "late",
    "very_late",
    "early",
    "very_early",
    "cosine",
    "zero",
    "one",
    )

jpt__player_response_response_type = (
    "shielded",
    "unshielded",
    "all",
    )

jpt__wobble_function = (
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

phmo_node_edge_constraint_type = (
    "hinge",
    "limited_hinge",
    "ragdoll",
    "stiff_spring",
    "ball_and_socket",
    "prismatic",
    )

pmdf_meshe_index_buffer_type = (
    "point_list",
    "line_list",
    "line_strip",
    "triange_list",
    "triange_fan",
    "triange_strip",
    )

pmdf_meshe_prt_type = (
    "none",
    "ambient",
    "linear",
    "quadratic",
    )

pmdf_meshe_vertex_type = (
    "world",
    "rigid",
    "skinned",
    "particle_model",
    "flat_world",
    "flat_rigid",
    "flat_skinned",
    "screen",
    "debug",
    "transparent",
    "particle",
    "contrail",
    "light_volume",
    "chud_simple",
    "chud_fancy",
    "decorator",
    "tiny_position",
    "patchy_fog",
    "water",
    "ripple",
    "implicit",
    "beam",
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

scnr_light_volume_type_1 = (
    "sphere",
    "projective",
    )

sily_text_value_pair_expected_value_type = (
    "integer_index",
    "stringid_reference",
    "incremental",
    )

snd__sound_class = (
    "projectile_impact",
    "projectile_detonation",
    "projectile_flyby",
    "projectile_detonation_lod",
    "weapon_fire",
    "weapon_ready",
    "weapon_reload",
    "weapon_empty",
    "weapon_charge",
    "weapon_overheat",
    "weapon_idle",
    "weapon_melee",
    "weapon_animation",
    "object_impacts",
    "particle_impacts",
    "weapon_fire_lod",
    "unused1_impacts",
    "unused2_impacts",
    "unit_footsteps",
    "unit_dialog",
    "unit_animation",
    "unit_unused",
    "vehicle_collision",
    "vehicle_engine",
    "vehicle_animation",
    "vehicle_engine_lod",
    "device_door",
    "device_unused0",
    "device_machinery",
    "device_stationary",
    "device_unused1",
    "device_unused2",
    "music",
    "ambient_nature",
    "ambient_machinery",
    "ambient_stationary",
    "huge_ass",
    "object_looping",
    "cinematic_music",
    "unknown_unused0",
    "unknown_unused1",
    "ambient_flock",
    "no_pad",
    "no_pad_stationary",
    "mission_unused0",
    "cortana_mission",
    "cortana_gravemind_channel",
    "mission_dialog",
    "cinematic_dialog",
    "scripted_cinematic_foley",
    "game_event",
    "ui",
    "test",
    "multilingual_test",
    )

ugh__language_language = (
    "english",
    "japanese",
    "german",
    "french",
    "spanish",
    "latin_american_spanish",
    "italian",
    "korean",
    "chinese_traditional",
    "chinese_simplified",
    "portuguese",
    "polish",
    )

unknown_flags_16 = tuple("bit_%s" % i for i in range(16))

unknown_flags_32 = tuple("bit_%s" % i for i in range(32))

unknown_flags_8 = tuple("bit_%s" % i for i in range(8))

vehi_friction_point_model_state_destroyed = (
    "default",
    "minor_damage",
    "medium_damage",
    "major_damage",
    "destroyed",
    )

wscl_animation_definition_anchor = (
    "custom",
    "center",
    "top_center",
    "bottom_center",
    "left_center",
    "right_center",
    "top_left",
    "top_right",
    "bottom_right",
    "bottom_left",
    )

zone_map_type = (
    "single_player",
    "multiplayer",
    "main_menu",
    )
