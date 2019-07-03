from reclaimer.constants import *


# maps tag class four character codes(fccs) in
# their string encoding to their int encoding.
h3_tag_class_fcc_to_be_int = {}
h3_tag_class_fcc_to_le_int = {}
# maps tag class four character codes(fccs) in
# their int encoding to their string encoding.
h3_tag_class_be_int_to_fcc = {}
h3_tag_class_le_int_to_fcc = {}


HALO3_SHARED_MAP_TYPES = ("mainmenu", "shared", "campaign")

# maps tag class four character codes to the tags file extension
# 177 tag classes
nul_char = b"\x00".decode(encoding="latin-1")
h3_tag_class_fcc_to_ext = {
    nul_char + "rmc": "shader_contrail",
    nul_char + "rmp": "shader_particle",
    "$#!+": "cache_file_sound",
    "*cen": "scenario_scenery_resource",
    "*eap": "scenario_weapons_resource",
    "*ehi": "scenario_vehicles_resource",
    "*fsc": "scenario_effect_scenery_resource",
    "*igh": "scenario_lights_resource",
    "*ipd": "scenario_bipeds_resource",
    "*qip": "scenario_equipment_resource",
    "*rea": "scenario_creature_resource",
    "*sce": "scenario_sound_scenery_resource",
    "/**/": "scenario_comments_resource",
    "<fx>": "sound_effect_template",
    "BooM": "stereo_system",
    "adlg": "ai_dialogue_globals",
    "ai**": "scenario_ai_resource",
    "ant!": "antenna",
    "beam": "beam_system",
    "bink": "bink",
    "bipd": "biped",
    "bitm": "bitmap",
    "bkey": "gui_button_key_definition",
    "bloc": "crate",
    "bmp3": "gui_bitmap_widget_definition",
    "bsdt": "breakable_surface",
    "cddf": "collision_damage",
    "cfxs": "camera_fx_settings",
    "chad": "chud_animation_definition",
    "char": "character",
    "chdt": "chud_definition",
    "chgd": "chud_globals_definition",
    "chmt": "chocolate_mountain_new",
    "cin*": "scenario_cinematics_resource",
    "cine": "cinematic",
    "cisc": "cinematic_scene",
    "clu*": "scenario_cluster_data_resource",
    "clwd": "cloth",
    "cntl": "contrail_system",
    "coll": "collision_model",
    "colo": "color_table",
    "crea": "creature",
    "crte": "cortana_effect_definition",
    "ctrl": "device_control",
    "cub*": "scenario_cubemap_resource",
    "dc*s": "scenario_decorators_resource",
    "dctr": "decorator_set",
    "dec*": "scenario_decals_resource",
    "decs": "decal_system",
    "devi": "device",
    "devo": "cellular_automata",
    "dgr*": "scenario_devices_resource",
    "dobc": "detail_object_collection",
    "draw": "rasterizer_cache_file_globals",
    "drdf": "damage_response_definition",
    "dsrc": "gui_datasource_definition",
    "effe": "effect",
    "effg": "effect_globals",
    "efsc": "effect_scenery",
    "egor": "screen_effect",
    "eqip": "equipment",
    "flck": "flock",
    "fldy": "fluid_dynamics",
    "fog ": "planar_fog",
    "foot": "material_effects",
    "fpch": "patchy_fog",
    "frag": "fragment",
    "gint": "giant",
    "glps": "global_pixel_shader",
    "glvs": "global_vertex_shader",
    "goof": "multiplayer_variant_settings_interface_definition",
    "grup": "gui_group_widget_definition",
    "hlmt": "model",
    "hlsl": "hlsl_include",
    "hsc*": "scenario_hs_source_file",
    "item": "item",
    "itmc": "item_collection",
    "jmad": "model_animation_graph",
    "jmrq": "sandbox_text_value_pair_definition",
    "jpt!": "damage_effect",
    "lens": "lens_flare",
    "ligh": "light",
    "lsnd": "sound_looping",
    "lst3": "gui_list_widget_definition",
    "lswd": "leaf_system",
    "ltvl": "light_volume_system",
    "mach": "device_machine",
    "matg": "globals",
    "mdl3": "gui_model_widget_definition",
    "mdlg": "ai_mission_dialogue",
    "metr": "meter",
    "mffn": "muffin",
    "mode": "render_model",
    "mply": "multiplayer_scenario_description",
    "mulg": "multiplayer_globals",
    "nclt": "new_cinematic_lighting",
    "obje": "object",
    "perf": "performance_throttles",
    "phmo": "physics_model",
    "pixl": "pixel_shader",
    "play": "cache_file_resource_layout_table",
    "pmdf": "particle_model",
    "pmov": "particle_physics",
    "pphy": "point_physics",
    "proj": "projectile",
    "prt3": "particle",
    "rasg": "rasterizer_globals",
    "rm  ": "render_method",
    "rmb ": "shader_beam",
    "rmcs": "shader_custom",
    "rmct": "shader_cortana",
    "rmd ": "shader_decal",
    "rmdf": "render_method_definition",
    "rmfl": "shader_foliage",
    "rmhg": "shader_halogram",
    "rmlv": "shader_light_volume",
    "rmop": "render_method_option",
    "rmsh": "shader",
    "rmsk": "shader_skin",
    "rmt2": "render_method_template",
    "rmtr": "shader_terrain",
    "rmw ": "shader_water",
    "rwrd": "render_water_ripple",
    "sFdT": "scenario_faux_data",
    "sLdT": "scenario_lightmap",
    "sbsp": "scenario_structure_bsp",
    "scen": "scenery",
    "scn3": "gui_screen_widget_definition",
    "scnr": "scenario",
    "sddt": "structure_design",
    "sefc": "area_screen_effect",
    "sfx+": "sound_effect_collection",
    "sgp!": "sound_global_propagation",
    "shit": "shield_impact",
    "sily": "text_value_pair_definition",
    "skn3": "gui_skin_definition",
    "sky*": "scenario_sky_references_resource",
    "skya": "sky_atm_parameters",
    "smap": "shared_cache_file_layout",
    "sncl": "sound_classes",
    "snd!": "sound",
    "snde": "sound_environment",
    "snmx": "sound_mix",
    "spk!": "sound_dialogue_constants",
    "ssce": "sound_scenery",
    "sslt": "scenario_structure_lighting_resource",
    "stli": "scenario_structure_lighting_info",
    "stse": "structure_seams",
    "styl": "style",
    "term": "device_terminal",
    "trak": "camera_track",
    "trg*": "scenario_trigger_volumes_resource",
    "txt3": "gui_text_widget_definition",
    "udlg": "dialogue",
    "ugh!": "sound_cache_file_gestalt",
    "uise": "user_interface_sounds_definition",
    "unic": "multilingual_unicode_string_list",
    "unit": "unit",
    "vehc": "vehicle_collection",
    "vehi": "vehicle",
    "vtsh": "vertex_shader",
    "wacd": "gui_widget_animation_collection_definition",
    "wclr": "gui_widget_color_animation_definition",
    "weap": "weapon",
    "wezr": "game_engine_settings_definition",
    "wfon": "gui_widget_font_animation_definition",
    "wgan": "gui_widget_animation_definition",
    "wgtz": "user_interface_globals_definition",
    "whip": "cellular_automata2d",
    "wigl": "user_interface_shared_globals_definition",
    "wind": "wind",
    "wpos": "gui_widget_position_animation_definition",
    "wrot": "gui_widget_rotation_animation_definition",
    "wscl": "gui_widget_scale_animation_definition",
    "wspr": "gui_widget_sprite_animation_definition",
    "wtuv": "gui_widget_texture_coordinate_animation_definition",
    "zone": "cache_file_resource_gestalt",
    }

for tag_cls in h3_tag_class_fcc_to_ext:
    h3_tag_class_fcc_to_be_int[tag_cls] = fcc(tag_cls)
    h3_tag_class_be_int_to_fcc[fcc(tag_cls)] = tag_cls
    h3_tag_class_fcc_to_le_int[tag_cls] = fcc(tag_cls)
    h3_tag_class_le_int_to_fcc[fcc(tag_cls)] = tag_cls
