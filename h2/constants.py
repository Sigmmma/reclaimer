from ..constants import *


# These are the 4 fourCC that I've found in tag headers
# and this is what I believe the order of their age is.
engine_id_to_name = dict(
    BLM_="halo_2",
    LAMB="halo_2_old",
    MLAB="halo_2_older",
    ambl="halo_2_oldest",
    )

# Here are some of the differences between engine versions:
# ambl: the tbfd struct was 12 bytes instead of 16, with the second and
#       third UInt32 replaced by UInt16, which are the version and bcount
# MLAB: the ascii_str32 instances were replaced with ascii_str_varlen
# LAMB: ???
# BLM!: newest version.

# DO NOT CHANGE THE ORDER OF THESE
HALO2_MAP_TYPES = ("local", "mainmenu", "shared", "single_player_shared")


# bitmap formats
PALLETIZED_FORMATS = (FORMAT_P8_BUMP, FORMAT_P8)


# maps tag class four character codes(fccs) in
# their string encoding to their int encoding.
h2_tag_class_fcc_to_be_int = {}
h2_tag_class_fcc_to_le_int = {}
# maps tag class four character codes(fccs) in
# their int encoding to their string encoding.
h2_tag_class_be_int_to_fcc = {}
h2_tag_class_le_int_to_fcc = {}

# maps tag class four character codes to the tags file extension
# 120 classes, 97 of which are NOT marked with OLD?
h2_tag_class_fcc_to_ext = {
    "adlg": "ai_dialogue_globals",
    "mdlg": "ai_mission_dialogue",
    "ant!": "antenna",
    "bipd": "biped",
    "bitm": "bitmap",
    "bsdt": "breakable_surface",
    "$#!+": "cache_file_sound",  # OLD?
    "trak": "camera_track",
    "devo": "cellular_automata",
    "whip": "cellular_automata2d",
    "char": "character",
    "gldf": "chocolate_mountain",
    "clwd": "cloth",
    "coll": "collision_model",
    "coln": "colony",
    "colo": "color_table",
    "cont": "contrail",
    "bloc": "crate",
    "crea": "creature",
    "jpt!": "damage_effect",
    "deca": "decal",
    "DECR": "decorator_set",
    "DECP": "decorators",
    "dobc": "detail_object_collection",
    "devi": "device",
    "ctrl": "device_control",
    "lifi": "device_light_fixture",
    "mach": "device_machine",
    "udlg": "dialogue",
    "effe": "effect",
    "eqip": "equipment",
    "garb": "garbage",
    "matg": "globals",
    "grhi": "grenade_hud_interface",  # OLD?
    "hudg": "hud_globals",
    "hmt ": "hud_message_text",
    "hud#": "hud_number",
    "item": "item",
    "itmc": "item_collection",
    "lens": "lens_flare",
    "ligh": "light",
    "MGS2": "light_volume",
    "tdtl": "liquid",
    "foot": "material_effects",
    "mpdt": "material_physics",
    "metr": "meter",
    "hlmt": "model",
    "jmad": "model_animation_graph",
    "mcsr": "mouse_cursor_definition",
    "unic": "multilingual_unicode_string_list",
    "mulg": "multiplayer_globals",
    "mply": "multiplayer_scenario_description",
    "goof": "multiplayer_variant_settings_interface_definition",
    "nhdt": "new_hud_definition",
    "obje": "object",
    'pctl': "particle_system",  # still in use in the halo 2 alpha
    "part": "particle_old",     # still in use in the halo 2 alpha
    "prt3": "particle",
    "PRTM": "particle_model",
    "pmov": "particle_physics",
    "fpch": "patchy_fog",
    "phys": "physics",
    "phmo": "physics_model",
    "pixl": "pixel_shader",
    "fog ": "planar_fog",
    "pphy": "point_physics",
    "proj": "projectile",
    "mode": "render_model",
    "sbsp": "scenario_structure_bsp",
    "ltmp": "scenario_structure_lightmap",
    "scnr": "scenario",
    "ai**": "scenario_ai_resource",  # OLD?
    "*ipd": "scenario_bipeds_resource",  # OLD?
    "cin*": "scenario_cinematics_resource",  # OLD?
    "clu*": "scenario_cluster_data_resource",  # OLD?
    "/**/": "scenario_comments_resource",  # OLD?
    "*rea": "scenario_creature_resource",  # OLD?
    "dec*": "scenario_decals_resource",  # OLD?
    "dc*s": "scenario_decorators_resource",  # OLD?
    "dgr*": "scenario_devices_resource",  # OLD?
    "*qip": "scenario_equipment_resource",  # OLD?
    "hsc*": "scenario_hs_source_file",  # OLD?
    "*cen": "scenario_scenery_resource",  # OLD?
    "*sce": "scenario_sound_scenery_resource",  # OLD?
    "sslt": "scenario_structure_lighting_resource",  # OLD?
    "*igh": "scenario_lights_resource",  # OLD?
    "trg*": "scenario_trigger_volumes_resource",  # OLD?
    "*ehi": "scenario_vehicles_resource",  # OLD?
    "*eap": "scenario_weapons_resource",  # OLD?
    "scen": "scenery",
    "egor": "screen_effect",
    "shad": "shader",
    "stem": "shader_template",
    "slit": "shader_light_response",
    "spas": "shader_pass",
    "sky ": "sky",
    "snd!": "sound",
    "ugh!": "sound_cache_file_gestalt",
    "sncl": "sound_classes",
    "spk!": "sound_dialogue_constants",
    "<fx>": "sound_effect_template",
    "sfx+": "sound_effect_collection",
    "snde": "sound_environment",
    "lsnd": "sound_looping",
    "snmx": "sound_mix",
    "ssce": "sound_scenery",
    "BooM": "stereo_system",
    "styl": "style",
    "sily": "text_value_pair_definition",
    "unit": "unit",
    "unhi": "unit_hud_interface",  # OLD?
    "wgtz": "user_interface_globals_definition",
    "skin": "user_interface_list_skin_definition",
    "wgit": "user_interface_screen_widget_definition",
    "wigl": "user_interface_shared_globals_definition",
    "vehi": "vehicle",
    "vehc": "vehicle_collection",
    "vrtx": "vertex_shader",
    "weap": "weapon",
    "wphi": "weapon_hud_interface",  # OLD?
    "weat": "weather_system",
    "wind": "wind",
    }

for tag_cls in h2_tag_class_fcc_to_ext:
    h2_tag_class_fcc_to_be_int[tag_cls] = fcc(tag_cls)
    h2_tag_class_be_int_to_fcc[fcc(tag_cls)] = tag_cls
    h2_tag_class_fcc_to_le_int[tag_cls] = fcc(tag_cls)
    h2_tag_class_le_int_to_fcc[fcc(tag_cls)] = tag_cls
