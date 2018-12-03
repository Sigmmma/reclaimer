############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: -DeToX-
# 	Named most reflexives, some values...
# revision: 3		author: -DeToX-
# 	Named alot of things..
# revision: 4		author: DeadCanadian
# 	added plugins, named some structs, and stuff
# revision: 5		author: DeadCanadian
# 	added spawn time for objects placement and vehicle spawn effects
# revision: 6		author: Lord Zedd
# 	Regenerated to bring back deleted sections.
# revision: 7		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef

scnr_ai_objective_role_filter = (
    "none",
    "leader",
    ("arbiter", 3),
    "player",
    ("infantry", 7),
    ("flood", 16),
    "sentinel",
    ("jackal", 21),
    "grunt",
    ("marine", 24),
    "flood_combat",
    "flood_carrier",
    ("brute", 28),
    ("drone", 30),
    "flood_pureform",
    ("warthog", 34),
    ("wraith", 39),
    "phantom",
    ("brute_chopper", 44),
    )

scnr_ai_trigger_combination_rule = (
    "or",
    "and",
    )

scnr_ai_trigger_condition_rule_type = (
    "a_or_greater_alive",
    "a_or_fewer_alive",
    "x_or_greater_strength",
    "x_or_less_strength",
    "if_enemy_sighted",
    "after_a_ticks",
    "if_alerted_by_squad_a",
    "script_reference_true",
    "script_reference_false",
    "if_player_in_trigger_volume",
    "if_all_players_in_trigger_volume",
    "combat_status_a_or_more",
    "combat_status_a_or_less",
    "arrived",
    "in_vehicle",
    "sighted_player",
    "a_or_greater_fighting",
    "a_or_fewer_fighting",
    "player_within_x_world_units",
    "player_shot_more_than_x_seconds_ago",
    "game_safe_to_save",
    )

scnr_cutscene_camera_point_type = (
    "normal",
    "ignore_target_orientation",
    "dolly",
    "ignore_target_updates",
    )

scnr_cutscene_title_horizontal_justification = (
    "left",
    "right",
    "center",
    )

scnr_cutscene_title_vertical_justification = (
    "bottom",
    "top",
    "middle",
    "bottom_2",
    "top_2",
    )

scnr_giant_unknown_8 = (
    "_0",
    "_1",
    "_2",
    "_3",
    "_4",
    )

scnr_light_volume_lightmap_type = (
    "use_light_tag_setting",
    "dynamic_only",
    "dynamic_with_lightmaps",
    "lightmaps_only",
    )

scnr_machine_pathfinding_policy = (
    "tag_default",
    "cut_out",
    "sectors",
    "discs",
    "none",
    )

scnr_object_name_type = (
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
    ("null", 65535),
    )

scnr_player_starting_location_campaign_player_type = (
    "masterchief",
    "dervish",
    "chief_multiplayer",
    "elite_multiplayer",
    "elite_coop",
    "monitor",
    )

scnr_scenery_bsp_policy = (
    "default",
    "always_placed",
    "manual_bsp_index",
    )

scnr_scenery_lightmapping_policy = (
    "tag_default",
    "dynamic",
    "per_vertex",
    )

scnr_scenery_pathfinding_policy = (
    "tag_default",
    "dynamic",
    "cut_out",
    "standard",
    "none",
    )

scnr_scenery_source = (
    "structure",
    "editor",
    "dynamic",
    "legacy",
    )

scnr_scenery_symmetry = (
    "both",
    "symmetric",
    "asymmetric",
    )

scnr_scenery_team = (
    "red",
    "blue",
    "green",
    "orange",
    "purple",
    "yellow",
    "brown",
    "pink",
    "neutral",
    )

scnr_script_expression_value_type = (
    "unparsed",
    "special_form",
    "function_name",
    "passthrough",
    "void",
    "boolean",
    "real",
    "short",
    "long",
    "string",
    "script",
    "string_id",
    "unit_seat_mapping",
    "trigger_volume",
    "cutscene_flag",
    "cutscene_camera_point",
    "cutscene_title",
    "cutscene_recording",
    "device_group",
    "ai",
    "ai_command_list",
    "ai_command_script",
    "ai_behavior",
    "ai_orders",
    "ai_line",
    "starting_profile",
    "conversation",
    "zone_set",
    "designer_zone",
    "point_reference",
    "style",
    "object_list",
    "folder",
    "sound",
    "effect",
    "damage",
    "looping_sound",
    "animation_graph",
    "damage_effect",
    "object_definition",
    "bitmap",
    "shader",
    "render_model",
    "structure_definition",
    "lightmap_definition",
    "cinematic_definition",
    "cinematic_scene_definition",
    "bink_definition",
    "any_tag",
    "any_tag_not_resolving",
    "game_difficulty",
    "team",
    "mp_team",
    "controller",
    "button_preset",
    "joystick_preset",
    "player_color",
    "player_character_type",
    "voice_output_setting",
    "voice_mask",
    "subtitle_setting",
    "actor_type",
    "model_state",
    "event",
    "character_physics",
    "object",
    "unit",
    "vehicle",
    "weapon",
    "device",
    "scenery",
    "effect_scenery",
    "object_name",
    "unit_name",
    "vehicle_name",
    "weapon_name",
    "device_name",
    "scenery_name",
    "effect_scenery_name",
    "cinematic_lightprobe",
    "animation_budget_reference",
    "looping_sound_budget_reference",
    "sound_budget_reference",
    ("invalid", 47802),
    )

scnr_script_return_type = (
    "unparsed",
    "special_form",
    "function_name",
    "passthrough",
    "void",
    "boolean",
    "real",
    "short",
    "long",
    "string",
    "script",
    "string_id",
    "unit_seat_mapping",
    "trigger_volume",
    "cutscene_flag",
    "cutscene_camera_point",
    "cutscene_title",
    "cutscene_recording",
    "device_group",
    "ai",
    "ai_command_list",
    "ai_command_script",
    "ai_behavior",
    "ai_orders",
    "ai_line",
    "starting_profile",
    "conversation",
    "zone_set",
    "designer_zone",
    "point_reference",
    "style",
    "object_list",
    "folder",
    "sound",
    "effect",
    "damage",
    "looping_sound",
    "animation_graph",
    "damage_effect",
    "object_definition",
    "bitmap",
    "shader",
    "render_model",
    "structure_definition",
    "lightmap_definition",
    "cinematic_definition",
    "cinematic_scene_definition",
    "bink_definition",
    "any_tag",
    "any_tag_not_resolving",
    "game_difficulty",
    "team",
    "mp_team",
    "controller",
    "button_preset",
    "joystick_preset",
    "player_color",
    "player_character_type",
    "voice_output_setting",
    "voice_mask",
    "subtitle_setting",
    "actor_type",
    "model_state",
    "event",
    "character_physics",
    "object",
    "unit",
    "vehicle",
    "weapon",
    "device",
    "scenery",
    "effect_scenery",
    "object_name",
    "unit_name",
    "vehicle_name",
    "weapon_name",
    "device_name",
    "scenery_name",
    "effect_scenery_name",
    "cinematic_lightprobe",
    "animation_budget_reference",
    "looping_sound_budget_reference",
    "sound_budget_reference",
    )

scnr_script_script_type = (
    "startup",
    "dormant",
    "continuous",
    "static",
    "command_script",
    "stub",
    )

scnr_squad_base_squad_grenade_type = (
    "none",
    "human_frag",
    "covenant_plasma",
    "spike",
    "firebomb",
    )

scnr_squad_base_squad_starting_location_initial_movement_mode = (
    "default",
    "climbing",
    "flying",
    )

scnr_squad_base_squad_starting_location_seat_type = (
    "default",
    "spawn_in_passenger_0",
    "spawn_in_gunner",
    "spawn_in_driver",
    "spawn_out_of_vehicle",
    ("spawn_vehicle_only", 6),
    "spawn_in_passenger_1",
    )

unknown_flags_1 = tuple("bit_%s" % i for i in range(1))


scnr_structure_bsp = Struct("structure_bsp", 
    h3_dependency("structure_bsp"),
    h3_dependency("design"),
    h3_dependency("lighting"),
    SInt32("unknown_0", VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    BytesRaw("unknown_2", SIZE=8, VISIBLE=False),
    Array("unknown_array", SUB_STRUCT=SInt16("unknown"), SIZE=4, VISIBLE=False),
    h3_dependency("cubemap"),
    h3_dependency("wind"),
    SInt32("unknown_3", VISIBLE=False),
    ENDIAN=">", SIZE=108
    )


scnr_sky_reference = Struct("sky_reference", 
    h3_dependency("sky_object"),
    SInt16("name_index"),
    Bool16("active_bsps", *("bsp_%s" % i for i in range(16))),
    ENDIAN=">", SIZE=20
    )


scnr_bsp_group_bsp_checksum = Struct("bsp_checksum", 
    SInt32("structure_checksum"),
    ENDIAN=">", SIZE=4
    )


scnr_bsp_group_bsps_0_clusters_0_bsp_unknown = Struct("unknown", 
    Bool32("allow", 
        ("effects", 1 << 5),
        ("firing_effects", 1 << 16),
        ("decals", 1 << 24),
        ),
    ENDIAN=">", SIZE=4
    )


scnr_bsp_group_bsps_0_clusters_0_bsp = Struct("bsp", 
    h3_reflexive("unknown", scnr_bsp_group_bsps_0_clusters_0_bsp_unknown),
    ENDIAN=">", SIZE=12
    )


scnr_bsp_group_bsps_0_clusters_0 = Struct("clusters_0", 
    h3_reflexive("bsps", scnr_bsp_group_bsps_0_clusters_0_bsp),
    ENDIAN=">", SIZE=12
    )


scnr_bsp_group_bsps_0_clusters_1_bsp_unknown = Struct("unknown", 
    Bool32("allow", 
        ("effects", 1 << 5),
        ("firing_effects", 1 << 16),
        ("decals", 1 << 24),
        ),
    ENDIAN=">", SIZE=4
    )


scnr_bsp_group_bsps_0_clusters_1_bsp = Struct("bsp", 
    h3_reflexive("unknown", scnr_bsp_group_bsps_0_clusters_1_bsp_unknown),
    ENDIAN=">", SIZE=12
    )


scnr_bsp_group_bsps_0_clusters_1 = Struct("clusters_1", 
    h3_reflexive("bsps", scnr_bsp_group_bsps_0_clusters_1_bsp),
    ENDIAN=">", SIZE=12
    )


scnr_bsp_group_bsps_0_cluster_skie = Struct("cluster_skie", 
    SInt8("sky_index"),
    ENDIAN=">", SIZE=1
    )


scnr_bsp_group_bsps_0_cluster_visible_skie = Struct("cluster_visible_skie", 
    SInt8("sky_index"),
    ENDIAN=">", SIZE=1
    )


scnr_bsp_group_bsps_0_unknown_1 = Struct("unknown_1", 
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


scnr_bsp_group_bsps_0_clusters_2_unknown = Struct("unknown", 
    SInt8("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=1
    )


scnr_bsp_group_bsps_0_clusters_2 = Struct("clusters_2", 
    h3_reflexive("unknown", scnr_bsp_group_bsps_0_clusters_2_unknown),
    VISIBLE=False,
    ENDIAN=">", SIZE=12
    )


scnr_bsp_group_bsps_0 = Struct("bsps_0", 
    h3_reflexive("clusters_0", scnr_bsp_group_bsps_0_clusters_0),
    h3_reflexive("clusters_1", scnr_bsp_group_bsps_0_clusters_1),
    h3_reflexive("cluster_skies", scnr_bsp_group_bsps_0_cluster_skie),
    h3_reflexive("cluster_visible_skies", scnr_bsp_group_bsps_0_cluster_visible_skie),
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    h3_reflexive("unknown_1", scnr_bsp_group_bsps_0_unknown_1),
    h3_reflexive("clusters_2", scnr_bsp_group_bsps_0_clusters_2),
    ENDIAN=">", SIZE=84
    )


scnr_bsp_group_bsps_1_unknown_0 = Struct("unknown_0", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    SInt32("unknown_2", VISIBLE=False),
    SInt16("unknown_3", VISIBLE=False),
    SInt16("unknown_4", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=12
    )


scnr_bsp_group_bsps_1_unknown_1 = Struct("unknown_1", 
    SInt16("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=2
    )


scnr_bsp_group_bsps_1 = Struct("bsps_1", 
    h3_reflexive("unknown_0", scnr_bsp_group_bsps_1_unknown_0),
    h3_reflexive("unknown_1", scnr_bsp_group_bsps_1_unknown_1),
    VISIBLE=False,
    ENDIAN=">", SIZE=24
    )


scnr_bsp_group = Struct("bsp_group", 
    Bool32("included_bsps", *("bsp_%s" % i for i in range(32))),
    SInt32("unknown", VISIBLE=False),
    h3_reflexive("bsp_checksums", scnr_bsp_group_bsp_checksum),
    h3_reflexive("bsps_0", scnr_bsp_group_bsps_0),
    h3_reflexive("bsps_1", scnr_bsp_group_bsps_1),
    ENDIAN=">", SIZE=44
    )


scnr_scenario_bsp_audibility_encoded_door_pa = Struct("encoded_door_pa", 
    SInt32("unknown"),
    ENDIAN=">", SIZE=4
    )


scnr_scenario_bsp_audibility_cluster_door_portal_encoded_pa = Struct("cluster_door_portal_encoded_pa", 
    SInt32("unknown"),
    ENDIAN=">", SIZE=4
    )


scnr_scenario_bsp_audibility_ai_deafening_pa = Struct("ai_deafening_pa", 
    SInt32("unknown"),
    ENDIAN=">", SIZE=4
    )


scnr_scenario_bsp_audibility_cluster_distance = Struct("cluster_distance", 
    SInt8("unknown"),
    ENDIAN=">", SIZE=1
    )


scnr_scenario_bsp_audibility_bsp = Struct("bsp", 
    SInt32("start"),
    SInt32("size"),
    ENDIAN=">", SIZE=8
    )


scnr_scenario_bsp_audibility_bsp_cluster_list = Struct("bsp_cluster_list", 
    SInt32("start_index"),
    SInt32("cluster_count"),
    ENDIAN=">", SIZE=8
    )


scnr_scenario_bsp_audibility_cluster_mapping = Struct("cluster_mapping", 
    SInt16("idx"),
    ENDIAN=">", SIZE=2
    )


scnr_scenario_bsp_audibility = Struct("scenario_bsp_audibility", 
    SInt32("door_portal_count"),
    SInt32("unique_cluster_count"),
    QStruct("cluster_distance_bounds", INCLUDE=from_to),
    h3_reflexive("encoded_door_pas", scnr_scenario_bsp_audibility_encoded_door_pa),
    h3_reflexive("cluster_door_portal_encoded_pas", scnr_scenario_bsp_audibility_cluster_door_portal_encoded_pa),
    h3_reflexive("ai_deafening_pas", scnr_scenario_bsp_audibility_ai_deafening_pa),
    h3_reflexive("cluster_distances", scnr_scenario_bsp_audibility_cluster_distance),
    h3_reflexive("bsps", scnr_scenario_bsp_audibility_bsp),
    h3_reflexive("bsp_cluster_list", scnr_scenario_bsp_audibility_bsp_cluster_list),
    h3_reflexive("cluster_mapping", scnr_scenario_bsp_audibility_cluster_mapping),
    ENDIAN=">", SIZE=100
    )


scnr_scenario_zoneset_group = Struct("scenario_zoneset_group", 
    h3_string_id("name"),
    SInt32("bsp_group_index"),
    SInt32("import_loaded_bsps"),
    Bool32("loaded_bsps", *("bsp_%s" % i for i in range(32))),
    Bool32("loaded_designer_zonesets", *("set_%s" % i for i in range(32))),
    Bool32("unloaded_designer_zonesets", *("set_%s" % i for i in range(32))),
    Bool32("loaded_cinematic_zonesets", *("set_%s" % i for i in range(32))),
    SInt32("bsp_atlas_index"),
    SInt32("scenario_bsp_audibility_index"),
    ENDIAN=">", SIZE=36
    )


scnr_bsp_atla = Struct("bsp_atla", 
    h3_string_id("name"),
    Bool32("bsp", *("bsp_%s" % i for i in range(32))),
    Bool32("connected_bsps", *("bsp_%s" % i for i in range(32))),
    ENDIAN=">", SIZE=12
    )


scnr_object_name = Struct("object_name", 
    ascii_str32("name"),
    SEnum16("type", *scnr_object_name_type),
    SInt16("placement_index"),
    ENDIAN=">", SIZE=36
    )


scnr_scenery_node_positioning_node_flags_readable = Struct("node_flags_readable", 
    Bool8("flags_0", 
        "node_0_32_64_96_128_160_192_224",
        "node_1_33_65_97_129_161_193_225",
        "node_2_34_66_98_130_162_194_226",
        "node_3_35_67_99_131_163_195_227",
        "node_4_36_68_100_132_164_196_228",
        "node_5_37_69_101_133_165_197_229",
        "node_6_38_70_102_134_166_198_230",
        "node_7_39_71_103_135_167_199_231",
        ),
    Bool8("flags_1", 
        "node_8_40_72_104_136_168_200_232",
        "node_9_41_73_105_137_169_201_233",
        "node_10_42_74_106_138_170_202_234",
        "node_11_43_75_107_139_171_203_235",
        "node_12_44_76_108_140_172_204_236",
        "node_13_45_77_109_141_173_205_237",
        "node_14_46_78_110_142_174_206_238",
        "node_15_47_79_111_143_175_207_239",
        ),
    Bool8("flags_2", 
        "node_16_48_80_112_144_176_208_240",
        "node_17_49_81_113_145_177_209_241",
        "node_18_50_82_114_146_178_210_242",
        "node_19_51_83_115_147_179_211_243",
        "node_20_52_84_116_148_180_212_244",
        "node_21_53_85_117_149_181_213_245",
        "node_22_54_86_118_150_182_214_246",
        "node_23_55_87_119_151_183_215_247",
        ),
    Bool8("flags_3", 
        "node_24_56_88_120_152_184_216_248",
        "node_25_57_89_121_153_185_217_249",
        "node_26_58_90_122_154_186_218_250",
        "node_27_59_91_123_155_187_219_251",
        "node_28_60_92_124_156_188_220_252",
        "node_29_61_93_125_157_189_221_253",
        "node_30_62_94_126_158_190_222_254",
        "node_31_63_95_127_159_191_223_255",
        ),
    ENDIAN=">", SIZE=4
    )


scnr_scenery_node_positioning_orientations_readable = Struct("orientations_readable", 
    QStruct("rotation", INCLUDE=ijkw_sint16),
    ENDIAN=">", SIZE=8
    )


scnr_scenery_node_positioning = Struct("node_positioning", 
    SInt16("node_count"),
    SInt16("unknown", VISIBLE=False),
    h3_reflexive("node_flags_readable", scnr_scenery_node_positioning_node_flags_readable),
    h3_reflexive("orientations_readable", scnr_scenery_node_positioning_orientations_readable),
    ENDIAN=">", SIZE=28
    )


scnr_scenery_pathfinding_reference = Struct("pathfinding_reference", 
    SInt16("bsp_index"),
    SInt16("pathfinding_object_index"),
    ENDIAN=">", SIZE=4
    )


scnr_scenery = Struct("scenery", 
    SInt16("palette_index"),
    SInt16("name_index"),
    Bool32("placement_flags", 
        "not_automatically",
        "not_on_easy",
        "not_on_normal",
        "not_on_hard",
        "lock_type_to_env_object",
        "lock_transform_to_env_object",
        "never_placed",
        "lock_name_to_env_object",
        "create_at_rest",
        ),
    QStruct("position", INCLUDE=xyz_float),
    ypr_float_rad("rotation"),
    Float("scale"),
    h3_reflexive("node_positioning", scnr_scenery_node_positioning),
    SInt16("unknown_0", VISIBLE=False),
    Bool16("old_manual_bsp_flags_now_zonesets", *("set_%s" % i for i in range(16))),
    h3_string_id("unique_name"),
    UInt16("unique_id_salt"),
    UInt16("unique_id_index"),
    SInt16("origin_bsp_index"),
    SEnum8("type", *bloc_object_type),
    SEnum8("source", *scnr_scenery_source),
    SEnum8("bsp_policy", *scnr_scenery_bsp_policy),
    SInt8("unknown_1", VISIBLE=False),
    SInt16("editor_folder_index"),
    SInt16("unknown_2", VISIBLE=False),
    SInt16("parent_name_index"),
    h3_string_id("child_name"),
    h3_string_id("unknown_3"),
    Bool16("allowed_zonesets", *("set_%s" % i for i in range(16))),
    SInt16("unknown_4", VISIBLE=False),
    h3_string_id("variant"),
    Bool8("active_change_colors", 
        "primary",
        "secondary",
        "tertiary",
        "quaternary",
        ),
    SInt8("unknown_5", VISIBLE=False),
    SInt8("unknown_6", VISIBLE=False),
    SInt8("unknown_7", VISIBLE=False),
    color_argb_uint32("primary_color"),
    color_argb_uint32("secondary_color"),
    color_argb_uint32("tertiary_color"),
    color_argb_uint32("quaternary_color"),
    SEnum16("pathfinding_policy", *scnr_scenery_pathfinding_policy),
    SEnum16("lightmapping_policy", *scnr_scenery_lightmapping_policy),
    h3_reflexive("pathfinding_references", scnr_scenery_pathfinding_reference),
    SInt16("unknown_8"),
    SInt16("unknown_9"),
    SEnum32("symmetry", *scnr_scenery_symmetry),
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
    SEnum16("team", *scnr_scenery_team),
    SInt8("spawn_sequence"),
    QStruct("runtime", INCLUDE=from_to_sint8),
    Bool8("multiplayer_flags", 
        "is_unique_object",
        "not_placed_at_start",
        ),
    SInt16("spawn_time"),
    SInt16("abandon_time"),
    SInt8("unknown_10", VISIBLE=False),
    SEnum8("shape", *bloc_multiplayer_object_propertie_shape),
    SInt8("teleporter_channel"),
    SInt8("unknown_11", VISIBLE=False),
    SInt16("unknown_12", VISIBLE=False),
    SInt16("attached_name_index"),
    BytesRaw("unknown_13", SIZE=8, VISIBLE=False),
    Float("width_radius"),
    Float("depth"),
    Float("top"),
    Float("bottom"),
    BytesRaw("unknown_14", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=180
    )


scnr_scenery_palette = Struct("scenery_palette", 
    h3_dependency("scenery"),
    BytesRaw("unknown", SIZE=32, VISIBLE=False),
    ENDIAN=">", SIZE=48
    )


scnr_biped_node_positioning_node_flags_readable = Struct("node_flags_readable", 
    Bool8("flags_0", 
        "node_0_32_64_96_128_160_192_224",
        "node_1_33_65_97_129_161_193_225",
        "node_2_34_66_98_130_162_194_226",
        "node_3_35_67_99_131_163_195_227",
        "node_4_36_68_100_132_164_196_228",
        "node_5_37_69_101_133_165_197_229",
        "node_6_38_70_102_134_166_198_230",
        "node_7_39_71_103_135_167_199_231",
        ),
    Bool8("flags_1", 
        "node_8_40_72_104_136_168_200_232",
        "node_9_41_73_105_137_169_201_233",
        "node_10_42_74_106_138_170_202_234",
        "node_11_43_75_107_139_171_203_235",
        "node_12_44_76_108_140_172_204_236",
        "node_13_45_77_109_141_173_205_237",
        "node_14_46_78_110_142_174_206_238",
        "node_15_47_79_111_143_175_207_239",
        ),
    Bool8("flags_2", 
        "node_16_48_80_112_144_176_208_240",
        "node_17_49_81_113_145_177_209_241",
        "node_18_50_82_114_146_178_210_242",
        "node_19_51_83_115_147_179_211_243",
        "node_20_52_84_116_148_180_212_244",
        "node_21_53_85_117_149_181_213_245",
        "node_22_54_86_118_150_182_214_246",
        "node_23_55_87_119_151_183_215_247",
        ),
    Bool8("flags_3", 
        "node_24_56_88_120_152_184_216_248",
        "node_25_57_89_121_153_185_217_249",
        "node_26_58_90_122_154_186_218_250",
        "node_27_59_91_123_155_187_219_251",
        "node_28_60_92_124_156_188_220_252",
        "node_29_61_93_125_157_189_221_253",
        "node_30_62_94_126_158_190_222_254",
        "node_31_63_95_127_159_191_223_255",
        ),
    ENDIAN=">", SIZE=4
    )


scnr_biped_node_positioning_orientations_readable = Struct("orientations_readable", 
    QStruct("rotation", INCLUDE=ijkw_sint16),
    ENDIAN=">", SIZE=8
    )


scnr_biped_node_positioning = Struct("node_positioning", 
    SInt16("node_count"),
    SInt16("unknown", VISIBLE=False),
    h3_reflexive("node_flags_readable", scnr_biped_node_positioning_node_flags_readable),
    h3_reflexive("orientations_readable", scnr_biped_node_positioning_orientations_readable),
    ENDIAN=">", SIZE=28
    )


scnr_biped = Struct("biped", 
    SInt16("palette_index"),
    SInt16("name_index"),
    Bool32("placement_flags", 
        "not_automatically",
        "not_on_easy",
        "not_on_normal",
        "not_on_hard",
        "lock_type_to_env_object",
        "lock_transform_to_env_object",
        "never_placed",
        "lock_name_to_env_object",
        "create_at_rest",
        ),
    QStruct("position", INCLUDE=xyz_float),
    ypr_float_rad("rotation"),
    Float("scale"),
    h3_reflexive("node_positioning", scnr_biped_node_positioning),
    SInt16("unknown_0", VISIBLE=False),
    Bool16("old_manual_bsp_flags_now_zonesets", *("set_%s" % i for i in range(16))),
    h3_string_id("unique_name"),
    UInt16("unique_id_salt"),
    UInt16("unique_id_index"),
    SInt16("origin_bsp_index"),
    SEnum8("type", *bloc_object_type),
    SEnum8("source", *scnr_scenery_source),
    SEnum8("bsp_policy", *scnr_scenery_bsp_policy),
    SInt8("unknown_1", VISIBLE=False),
    SInt16("editor_folder_index"),
    SInt16("unknown_2", VISIBLE=False),
    SInt16("parent_name_index"),
    h3_string_id("child_name"),
    h3_string_id("unknown_3"),
    Bool16("allowed_zonesets", *("set_%s" % i for i in range(16))),
    SInt16("unknown_4", VISIBLE=False),
    h3_string_id("variant"),
    Bool8("active_change_colors", 
        "primary",
        "secondary",
        "tertiary",
        "quaternary",
        ),
    SInt8("unknown_5", VISIBLE=False),
    SInt8("unknown_6", VISIBLE=False),
    SInt8("unknown_7", VISIBLE=False),
    color_argb_uint32("primary_color"),
    color_argb_uint32("secondary_color"),
    color_argb_uint32("tertiary_color"),
    color_argb_uint32("quaternary_color"),
    Float("body_vitality_percentage"),
    Bool32("flags", 
        "dead",
        "closed",
        "not_enterable_by_player",
        ),
    ENDIAN=">", SIZE=116
    )


scnr_biped_palette = Struct("biped_palette", 
    h3_dependency("biped"),
    BytesRaw("unknown", SIZE=32, VISIBLE=False),
    ENDIAN=">", SIZE=48
    )


scnr_vehicle_node_positioning_node_flags_readable = Struct("node_flags_readable", 
    Bool8("flags_0", 
        "node_0_32_64_96_128_160_192_224",
        "node_1_33_65_97_129_161_193_225",
        "node_2_34_66_98_130_162_194_226",
        "node_3_35_67_99_131_163_195_227",
        "node_4_36_68_100_132_164_196_228",
        "node_5_37_69_101_133_165_197_229",
        "node_6_38_70_102_134_166_198_230",
        "node_7_39_71_103_135_167_199_231",
        ),
    Bool8("flags_1", 
        "node_8_40_72_104_136_168_200_232",
        "node_9_41_73_105_137_169_201_233",
        "node_10_42_74_106_138_170_202_234",
        "node_11_43_75_107_139_171_203_235",
        "node_12_44_76_108_140_172_204_236",
        "node_13_45_77_109_141_173_205_237",
        "node_14_46_78_110_142_174_206_238",
        "node_15_47_79_111_143_175_207_239",
        ),
    Bool8("flags_2", 
        "node_16_48_80_112_144_176_208_240",
        "node_17_49_81_113_145_177_209_241",
        "node_18_50_82_114_146_178_210_242",
        "node_19_51_83_115_147_179_211_243",
        "node_20_52_84_116_148_180_212_244",
        "node_21_53_85_117_149_181_213_245",
        "node_22_54_86_118_150_182_214_246",
        "node_23_55_87_119_151_183_215_247",
        ),
    Bool8("flags_3", 
        "node_24_56_88_120_152_184_216_248",
        "node_25_57_89_121_153_185_217_249",
        "node_26_58_90_122_154_186_218_250",
        "node_27_59_91_123_155_187_219_251",
        "node_28_60_92_124_156_188_220_252",
        "node_29_61_93_125_157_189_221_253",
        "node_30_62_94_126_158_190_222_254",
        "node_31_63_95_127_159_191_223_255",
        ),
    ENDIAN=">", SIZE=4
    )


scnr_vehicle_node_positioning_orientations_readable = Struct("orientations_readable", 
    QStruct("rotation", INCLUDE=ijkw_sint16),
    ENDIAN=">", SIZE=8
    )


scnr_vehicle_node_positioning = Struct("node_positioning", 
    SInt16("node_count"),
    SInt16("unknown", VISIBLE=False),
    h3_reflexive("node_flags_readable", scnr_vehicle_node_positioning_node_flags_readable),
    h3_reflexive("orientations_readable", scnr_vehicle_node_positioning_orientations_readable),
    ENDIAN=">", SIZE=28
    )


scnr_vehicle = Struct("vehicle", 
    SInt16("palette_index"),
    SInt16("name_index"),
    Bool32("placement_flags", 
        "not_automatically",
        "not_on_easy",
        "not_on_normal",
        "not_on_hard",
        "lock_type_to_env_object",
        "lock_transform_to_env_object",
        "never_placed",
        "lock_name_to_env_object",
        "create_at_rest",
        ),
    QStruct("position", INCLUDE=xyz_float),
    ypr_float_rad("rotation"),
    Float("scale"),
    h3_reflexive("node_positioning", scnr_vehicle_node_positioning),
    SInt16("unknown_0", VISIBLE=False),
    Bool16("old_manual_bsp_flags_now_zonesets", *("set_%s" % i for i in range(16))),
    h3_string_id("unique_name"),
    UInt16("unique_id_salt"),
    UInt16("unique_id_index"),
    SInt16("origin_bsp_index"),
    SEnum8("type", *bloc_object_type),
    SEnum8("source", *scnr_scenery_source),
    SEnum8("bsp_policy", *scnr_scenery_bsp_policy),
    SInt8("unknown_1", VISIBLE=False),
    SInt16("editor_folder_index"),
    SInt16("unknown_2", VISIBLE=False),
    SInt16("parent_name_index"),
    h3_string_id("child_name"),
    h3_string_id("unknown_3"),
    Bool16("allowed_zonesets", *("set_%s" % i for i in range(16))),
    SInt16("unknown_4", VISIBLE=False),
    h3_string_id("variant"),
    Bool8("active_change_colors", 
        "primary",
        "secondary",
        "tertiary",
        "quaternary",
        ),
    SInt8("unknown_5", VISIBLE=False),
    SInt8("unknown_6", VISIBLE=False),
    SInt8("unknown_7", VISIBLE=False),
    color_argb_uint32("primary_color"),
    color_argb_uint32("secondary_color"),
    color_argb_uint32("tertiary_color"),
    color_argb_uint32("quaternary_color"),
    Float("body_vitality_percentage"),
    Bool32("flags", 
        "dead",
        "closed",
        "not_enterable_by_player",
        ),
    SEnum32("symmetry", *scnr_scenery_symmetry),
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
    SEnum16("team", *scnr_scenery_team),
    SInt8("spawn_sequence"),
    QStruct("runtime", INCLUDE=from_to_sint8),
    Bool8("multiplayer_flags", 
        "is_unique_object",
        "not_placed_at_start",
        ),
    SInt16("spawn_time"),
    SInt16("abandon_time"),
    SInt8("unknown_8", VISIBLE=False),
    SEnum8("shape", *bloc_multiplayer_object_propertie_shape),
    SInt8("teleporter_channel"),
    SInt8("unknown_9", VISIBLE=False),
    SInt16("unknown_10", VISIBLE=False),
    SInt16("attached_name_index"),
    BytesRaw("unknown_11", SIZE=8, VISIBLE=False),
    Float("width_radius"),
    Float("depth"),
    Float("top"),
    Float("bottom"),
    BytesRaw("unknown_12", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=168
    )


scnr_vehicle_palette = Struct("vehicle_palette", 
    h3_dependency("vehicle"),
    BytesRaw("unknown", SIZE=32, VISIBLE=False),
    ENDIAN=">", SIZE=48
    )


scnr_equipment_node_positioning_node_flags_readable = Struct("node_flags_readable", 
    Bool8("flags_0", 
        "node_0_32_64_96_128_160_192_224",
        "node_1_33_65_97_129_161_193_225",
        "node_2_34_66_98_130_162_194_226",
        "node_3_35_67_99_131_163_195_227",
        "node_4_36_68_100_132_164_196_228",
        "node_5_37_69_101_133_165_197_229",
        "node_6_38_70_102_134_166_198_230",
        "node_7_39_71_103_135_167_199_231",
        ),
    Bool8("flags_1", 
        "node_8_40_72_104_136_168_200_232",
        "node_9_41_73_105_137_169_201_233",
        "node_10_42_74_106_138_170_202_234",
        "node_11_43_75_107_139_171_203_235",
        "node_12_44_76_108_140_172_204_236",
        "node_13_45_77_109_141_173_205_237",
        "node_14_46_78_110_142_174_206_238",
        "node_15_47_79_111_143_175_207_239",
        ),
    Bool8("flags_2", 
        "node_16_48_80_112_144_176_208_240",
        "node_17_49_81_113_145_177_209_241",
        "node_18_50_82_114_146_178_210_242",
        "node_19_51_83_115_147_179_211_243",
        "node_20_52_84_116_148_180_212_244",
        "node_21_53_85_117_149_181_213_245",
        "node_22_54_86_118_150_182_214_246",
        "node_23_55_87_119_151_183_215_247",
        ),
    Bool8("flags_3", 
        "node_24_56_88_120_152_184_216_248",
        "node_25_57_89_121_153_185_217_249",
        "node_26_58_90_122_154_186_218_250",
        "node_27_59_91_123_155_187_219_251",
        "node_28_60_92_124_156_188_220_252",
        "node_29_61_93_125_157_189_221_253",
        "node_30_62_94_126_158_190_222_254",
        "node_31_63_95_127_159_191_223_255",
        ),
    ENDIAN=">", SIZE=4
    )


scnr_equipment_node_positioning_orientations_readable = Struct("orientations_readable", 
    QStruct("rotation", INCLUDE=ijkw_sint16),
    ENDIAN=">", SIZE=8
    )


scnr_equipment_node_positioning = Struct("node_positioning", 
    SInt16("node_count"),
    SInt16("unknown", VISIBLE=False),
    h3_reflexive("node_flags_readable", scnr_equipment_node_positioning_node_flags_readable),
    h3_reflexive("orientations_readable", scnr_equipment_node_positioning_orientations_readable),
    ENDIAN=">", SIZE=28
    )


scnr_equipment = Struct("equipment", 
    SInt16("palette_index"),
    SInt16("name_index"),
    Bool32("placement_flags", 
        "not_automatically",
        "not_on_easy",
        "not_on_normal",
        "not_on_hard",
        "lock_type_to_env_object",
        "lock_transform_to_env_object",
        "never_placed",
        "lock_name_to_env_object",
        "create_at_rest",
        ),
    QStruct("position", INCLUDE=xyz_float),
    ypr_float_rad("rotation"),
    Float("scale"),
    h3_reflexive("node_positioning", scnr_equipment_node_positioning),
    SInt16("unknown_0", VISIBLE=False),
    Bool16("old_manual_bsp_flags_now_zonesets", *("set_%s" % i for i in range(16))),
    h3_string_id("unique_name"),
    UInt16("unique_id_salt"),
    UInt16("unique_id_index"),
    SInt16("origin_bsp_index"),
    SEnum8("type", *bloc_object_type),
    SEnum8("source", *scnr_scenery_source),
    SEnum8("bsp_policy", *scnr_scenery_bsp_policy),
    SInt8("unknown_1", VISIBLE=False),
    SInt16("editor_folder_index"),
    SInt16("unknown_2", VISIBLE=False),
    SInt16("parent_name_index"),
    h3_string_id("child_name"),
    h3_string_id("unknown_3"),
    Bool16("allowed_zonesets", *("set_%s" % i for i in range(16))),
    SInt16("unknown_4", VISIBLE=False),
    Bool32("equipment_flags", 
        "initially_at_rest_does_not_fall",
        ("does_accelerate_moves_due_to_explosions", 1 << 2),
        ),
    SEnum32("symmetry", *scnr_scenery_symmetry),
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
    SEnum16("team", *scnr_scenery_team),
    SInt8("spawn_sequence"),
    QStruct("runtime", INCLUDE=from_to_sint8),
    Bool8("multiplayer_flags", 
        "is_unique_object",
        "not_placed_at_start",
        ),
    SInt16("spawn_time"),
    SInt16("abandon_time"),
    SInt8("unknown_5", VISIBLE=False),
    SEnum8("shape", *bloc_multiplayer_object_propertie_shape),
    SInt8("teleporter_channel"),
    SInt8("unknown_6", VISIBLE=False),
    SInt16("unknown_7", VISIBLE=False),
    SInt16("attached_name_index"),
    BytesRaw("unknown_8", SIZE=8, VISIBLE=False),
    Float("width_radius"),
    Float("depth"),
    Float("top"),
    Float("bottom"),
    BytesRaw("unknown_9", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=140
    )


scnr_equipment_palette = Struct("equipment_palette", 
    h3_dependency("equipment"),
    BytesRaw("unknown", SIZE=32, VISIBLE=False),
    ENDIAN=">", SIZE=48
    )


scnr_weapon_node_positioning_node_flags_readable = Struct("node_flags_readable", 
    Bool8("flags_0", 
        "node_0_32_64_96_128_160_192_224",
        "node_1_33_65_97_129_161_193_225",
        "node_2_34_66_98_130_162_194_226",
        "node_3_35_67_99_131_163_195_227",
        "node_4_36_68_100_132_164_196_228",
        "node_5_37_69_101_133_165_197_229",
        "node_6_38_70_102_134_166_198_230",
        "node_7_39_71_103_135_167_199_231",
        ),
    Bool8("flags_1", 
        "node_8_40_72_104_136_168_200_232",
        "node_9_41_73_105_137_169_201_233",
        "node_10_42_74_106_138_170_202_234",
        "node_11_43_75_107_139_171_203_235",
        "node_12_44_76_108_140_172_204_236",
        "node_13_45_77_109_141_173_205_237",
        "node_14_46_78_110_142_174_206_238",
        "node_15_47_79_111_143_175_207_239",
        ),
    Bool8("flags_2", 
        "node_16_48_80_112_144_176_208_240",
        "node_17_49_81_113_145_177_209_241",
        "node_18_50_82_114_146_178_210_242",
        "node_19_51_83_115_147_179_211_243",
        "node_20_52_84_116_148_180_212_244",
        "node_21_53_85_117_149_181_213_245",
        "node_22_54_86_118_150_182_214_246",
        "node_23_55_87_119_151_183_215_247",
        ),
    Bool8("flags_3", 
        "node_24_56_88_120_152_184_216_248",
        "node_25_57_89_121_153_185_217_249",
        "node_26_58_90_122_154_186_218_250",
        "node_27_59_91_123_155_187_219_251",
        "node_28_60_92_124_156_188_220_252",
        "node_29_61_93_125_157_189_221_253",
        "node_30_62_94_126_158_190_222_254",
        "node_31_63_95_127_159_191_223_255",
        ),
    ENDIAN=">", SIZE=4
    )


scnr_weapon_node_positioning_orientations_readable = Struct("orientations_readable", 
    QStruct("rotation", INCLUDE=ijkw_sint16),
    ENDIAN=">", SIZE=8
    )


scnr_weapon_node_positioning = Struct("node_positioning", 
    SInt16("node_count"),
    SInt16("unknown", VISIBLE=False),
    h3_reflexive("node_flags_readable", scnr_weapon_node_positioning_node_flags_readable),
    h3_reflexive("orientations_readable", scnr_weapon_node_positioning_orientations_readable),
    ENDIAN=">", SIZE=28
    )


scnr_weapon = Struct("weapon", 
    SInt16("palette_index"),
    SInt16("name_index"),
    Bool32("placement_flags", 
        "not_automatically",
        "not_on_easy",
        "not_on_normal",
        "not_on_hard",
        "lock_type_to_env_object",
        "lock_transform_to_env_object",
        "never_placed",
        "lock_name_to_env_object",
        "create_at_rest",
        ),
    QStruct("position", INCLUDE=xyz_float),
    ypr_float_rad("rotation"),
    Float("scale"),
    h3_reflexive("node_positioning", scnr_weapon_node_positioning),
    SInt16("unknown_0", VISIBLE=False),
    Bool16("old_manual_bsp_flags_now_zonesets", *("set_%s" % i for i in range(16))),
    h3_string_id("unique_name"),
    UInt16("unique_id_salt"),
    UInt16("unique_id_index"),
    SInt16("origin_bsp_index"),
    SEnum8("type", *bloc_object_type),
    SEnum8("source", *scnr_scenery_source),
    SEnum8("bsp_policy", *scnr_scenery_bsp_policy),
    SInt8("unknown_1", VISIBLE=False),
    SInt16("editor_folder_index"),
    SInt16("unknown_2", VISIBLE=False),
    SInt16("parent_name_index"),
    h3_string_id("child_name"),
    h3_string_id("unknown_3"),
    Bool16("allowed_zonesets", *("set_%s" % i for i in range(16))),
    SInt16("unknown_4", VISIBLE=False),
    h3_string_id("variant"),
    Bool8("active_change_colors", 
        "primary",
        "secondary",
        "tertiary",
        "quaternary",
        ),
    SInt8("unknown_5", VISIBLE=False),
    SInt8("unknown_6", VISIBLE=False),
    SInt8("unknown_7", VISIBLE=False),
    color_argb_uint32("primary_color"),
    color_argb_uint32("secondary_color"),
    color_argb_uint32("tertiary_color"),
    color_argb_uint32("quaternary_color"),
    SInt16("rounds_left"),
    SInt16("rounds_loaded"),
    Bool32("weapon_flags", 
        "initially_at_rest_does_not_fall",
        ("does_accelerate_moves_due_to_explosions", 1 << 2),
        ),
    SEnum32("symmetry", *scnr_scenery_symmetry),
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
    SEnum16("team", *scnr_scenery_team),
    SInt8("spawn_sequence"),
    QStruct("runtime", INCLUDE=from_to_sint8),
    Bool8("multiplayer_flags", 
        "is_unique_object",
        "not_placed_at_start",
        ),
    SInt16("spawn_time"),
    SInt16("abandon_time"),
    SInt8("unknown_8", VISIBLE=False),
    SEnum8("shape", *bloc_multiplayer_object_propertie_shape),
    SInt8("teleporter_channel"),
    SInt8("unknown_9", VISIBLE=False),
    SInt16("unknown_10", VISIBLE=False),
    SInt16("attached_name_index"),
    BytesRaw("unknown_11", SIZE=8, VISIBLE=False),
    Float("width_radius"),
    Float("depth"),
    Float("top"),
    Float("bottom"),
    BytesRaw("unknown_12", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=168
    )


scnr_weapon_palette = Struct("weapon_palette", 
    h3_dependency("weapon"),
    BytesRaw("unknown", SIZE=32, VISIBLE=False),
    ENDIAN=">", SIZE=48
    )


scnr_device_group = Struct("device_group", 
    ascii_str32("name"),
    Float("initial_value"),
    Bool32("flags", 
        "only_use_once",
        ),
    ENDIAN=">", SIZE=40
    )


scnr_machine_node_positioning_node_flags_readable = Struct("node_flags_readable", 
    Bool8("flags_0", 
        "node_0_32_64_96_128_160_192_224",
        "node_1_33_65_97_129_161_193_225",
        "node_2_34_66_98_130_162_194_226",
        "node_3_35_67_99_131_163_195_227",
        "node_4_36_68_100_132_164_196_228",
        "node_5_37_69_101_133_165_197_229",
        "node_6_38_70_102_134_166_198_230",
        "node_7_39_71_103_135_167_199_231",
        ),
    Bool8("flags_1", 
        "node_8_40_72_104_136_168_200_232",
        "node_9_41_73_105_137_169_201_233",
        "node_10_42_74_106_138_170_202_234",
        "node_11_43_75_107_139_171_203_235",
        "node_12_44_76_108_140_172_204_236",
        "node_13_45_77_109_141_173_205_237",
        "node_14_46_78_110_142_174_206_238",
        "node_15_47_79_111_143_175_207_239",
        ),
    Bool8("flags_2", 
        "node_16_48_80_112_144_176_208_240",
        "node_17_49_81_113_145_177_209_241",
        "node_18_50_82_114_146_178_210_242",
        "node_19_51_83_115_147_179_211_243",
        "node_20_52_84_116_148_180_212_244",
        "node_21_53_85_117_149_181_213_245",
        "node_22_54_86_118_150_182_214_246",
        "node_23_55_87_119_151_183_215_247",
        ),
    Bool8("flags_3", 
        "node_24_56_88_120_152_184_216_248",
        "node_25_57_89_121_153_185_217_249",
        "node_26_58_90_122_154_186_218_250",
        "node_27_59_91_123_155_187_219_251",
        "node_28_60_92_124_156_188_220_252",
        "node_29_61_93_125_157_189_221_253",
        "node_30_62_94_126_158_190_222_254",
        "node_31_63_95_127_159_191_223_255",
        ),
    ENDIAN=">", SIZE=4
    )


scnr_machine_node_positioning_orientations_readable = Struct("orientations_readable", 
    QStruct("rotation", INCLUDE=ijkw_sint16),
    ENDIAN=">", SIZE=8
    )


scnr_machine_node_positioning = Struct("node_positioning", 
    SInt16("node_count"),
    SInt16("unknown", VISIBLE=False),
    h3_reflexive("node_flags_readable", scnr_machine_node_positioning_node_flags_readable),
    h3_reflexive("orientations_readable", scnr_machine_node_positioning_orientations_readable),
    ENDIAN=">", SIZE=28
    )


scnr_machine_pathfinding_reference = Struct("pathfinding_reference", 
    SInt16("bsp_index"),
    SInt16("pathfinding_object_index"),
    ENDIAN=">", SIZE=4
    )


scnr_machine = Struct("machine", 
    SInt16("palette_index"),
    SInt16("name_index"),
    Bool32("placement_flags", 
        "not_automatically",
        "not_on_easy",
        "not_on_normal",
        "not_on_hard",
        "lock_type_to_env_object",
        "lock_transform_to_env_object",
        "never_placed",
        "lock_name_to_env_object",
        "create_at_rest",
        ),
    QStruct("position", INCLUDE=xyz_float),
    ypr_float_rad("rotation"),
    Float("scale"),
    h3_reflexive("node_positioning", scnr_machine_node_positioning),
    SInt16("unknown_0", VISIBLE=False),
    Bool16("old_manual_bsp_flags_now_zonesets", *("set_%s" % i for i in range(16))),
    h3_string_id("unique_name"),
    UInt16("unique_id_salt"),
    UInt16("unique_id_index"),
    SInt16("origin_bsp_index"),
    SEnum8("type", *bloc_object_type),
    SEnum8("source", *scnr_scenery_source),
    SEnum8("bsp_policy", *scnr_scenery_bsp_policy),
    SInt8("unknown_1", VISIBLE=False),
    SInt16("editor_folder_index"),
    SInt16("unknown_2", VISIBLE=False),
    SInt16("parent_name_index"),
    h3_string_id("child_name"),
    h3_string_id("unknown_3"),
    Bool16("allowed_zonesets", *("set_%s" % i for i in range(16))),
    SInt16("unknown_4", VISIBLE=False),
    SInt16("power_group"),
    SInt16("position_group"),
    Bool32("device_flags", 
        "initially_open",
        "initially_closed",
        "can_only_change_once",
        "position_reversed",
        "usable_from_both_sides",
        ),
    Bool32("machine_flags", 
        "does_not_operate_automatically",
        "one_sided",
        "never_appears_locked",
        "opened_by_melee_attack",
        "one_sided_for_player",
        "does_not_close_automatically",
        ),
    h3_reflexive("pathfinding_references", scnr_machine_pathfinding_reference),
    SEnum16("pathfinding_policy", *scnr_machine_pathfinding_policy),
    SInt16("unknown_5"),
    ENDIAN=">", SIZE=112
    )


scnr_machine_palette = Struct("machine_palette", 
    h3_dependency("machine"),
    BytesRaw("unknown", SIZE=32, VISIBLE=False),
    ENDIAN=">", SIZE=48
    )


scnr_terminal_node_positioning_node_flags_readable = Struct("node_flags_readable", 
    Bool8("flags_0", 
        "node_0_32_64_96_128_160_192_224",
        "node_1_33_65_97_129_161_193_225",
        "node_2_34_66_98_130_162_194_226",
        "node_3_35_67_99_131_163_195_227",
        "node_4_36_68_100_132_164_196_228",
        "node_5_37_69_101_133_165_197_229",
        "node_6_38_70_102_134_166_198_230",
        "node_7_39_71_103_135_167_199_231",
        ),
    Bool8("flags_1", 
        "node_8_40_72_104_136_168_200_232",
        "node_9_41_73_105_137_169_201_233",
        "node_10_42_74_106_138_170_202_234",
        "node_11_43_75_107_139_171_203_235",
        "node_12_44_76_108_140_172_204_236",
        "node_13_45_77_109_141_173_205_237",
        "node_14_46_78_110_142_174_206_238",
        "node_15_47_79_111_143_175_207_239",
        ),
    Bool8("flags_2", 
        "node_16_48_80_112_144_176_208_240",
        "node_17_49_81_113_145_177_209_241",
        "node_18_50_82_114_146_178_210_242",
        "node_19_51_83_115_147_179_211_243",
        "node_20_52_84_116_148_180_212_244",
        "node_21_53_85_117_149_181_213_245",
        "node_22_54_86_118_150_182_214_246",
        "node_23_55_87_119_151_183_215_247",
        ),
    Bool8("flags_3", 
        "node_24_56_88_120_152_184_216_248",
        "node_25_57_89_121_153_185_217_249",
        "node_26_58_90_122_154_186_218_250",
        "node_27_59_91_123_155_187_219_251",
        "node_28_60_92_124_156_188_220_252",
        "node_29_61_93_125_157_189_221_253",
        "node_30_62_94_126_158_190_222_254",
        "node_31_63_95_127_159_191_223_255",
        ),
    ENDIAN=">", SIZE=4
    )


scnr_terminal_node_positioning_orientations_readable = Struct("orientations_readable", 
    QStruct("rotation", INCLUDE=ijkw_sint16),
    ENDIAN=">", SIZE=8
    )


scnr_terminal_node_positioning = Struct("node_positioning", 
    SInt16("node_count"),
    SInt16("unknown", VISIBLE=False),
    h3_reflexive("node_flags_readable", scnr_terminal_node_positioning_node_flags_readable),
    h3_reflexive("orientations_readable", scnr_terminal_node_positioning_orientations_readable),
    ENDIAN=">", SIZE=28
    )


scnr_terminal = Struct("terminal", 
    SInt16("palette_index"),
    SInt16("name_index"),
    Bool32("placement_flags", 
        "not_automatically",
        "not_on_easy",
        "not_on_normal",
        "not_on_hard",
        "lock_type_to_env_object",
        "lock_transform_to_env_object",
        "never_placed",
        "lock_name_to_env_object",
        "create_at_rest",
        ),
    QStruct("position", INCLUDE=xyz_float),
    ypr_float_rad("rotation"),
    Float("scale"),
    h3_reflexive("node_positioning", scnr_terminal_node_positioning),
    SInt16("unknown_0", VISIBLE=False),
    Bool16("old_manual_bsp_flags_now_zonesets", *("set_%s" % i for i in range(16))),
    h3_string_id("unique_name"),
    UInt16("unique_id_salt"),
    UInt16("unique_id_index"),
    SInt16("origin_bsp_index"),
    SEnum8("type", *bloc_object_type),
    SEnum8("source", *scnr_scenery_source),
    SEnum8("bsp_policy", *scnr_scenery_bsp_policy),
    SInt8("unknown_1", VISIBLE=False),
    SInt16("editor_folder_index"),
    SInt16("unknown_2", VISIBLE=False),
    SInt16("parent_name_index"),
    h3_string_id("child_name"),
    h3_string_id("unknown_3"),
    Bool16("allowed_zonesets", *("set_%s" % i for i in range(16))),
    SInt16("unknown_4", VISIBLE=False),
    SInt16("power_group"),
    SInt16("position_group"),
    Bool32("device_flags", 
        "initially_open",
        "initially_closed",
        "can_only_change_once",
        "position_reversed",
        "usable_from_both_sides",
        ),
    Pad(4),
    ENDIAN=">", SIZE=96
    )


scnr_terminal_palette = Struct("terminal_palette", 
    h3_dependency("terminal"),
    BytesRaw("unknown", SIZE=32, VISIBLE=False),
    ENDIAN=">", SIZE=48
    )


scnr_control_node_positioning_node_flags_readable = Struct("node_flags_readable", 
    Bool8("flags_0", 
        "node_0_32_64_96_128_160_192_224",
        "node_1_33_65_97_129_161_193_225",
        "node_2_34_66_98_130_162_194_226",
        "node_3_35_67_99_131_163_195_227",
        "node_4_36_68_100_132_164_196_228",
        "node_5_37_69_101_133_165_197_229",
        "node_6_38_70_102_134_166_198_230",
        "node_7_39_71_103_135_167_199_231",
        ),
    Bool8("flags_1", 
        "node_8_40_72_104_136_168_200_232",
        "node_9_41_73_105_137_169_201_233",
        "node_10_42_74_106_138_170_202_234",
        "node_11_43_75_107_139_171_203_235",
        "node_12_44_76_108_140_172_204_236",
        "node_13_45_77_109_141_173_205_237",
        "node_14_46_78_110_142_174_206_238",
        "node_15_47_79_111_143_175_207_239",
        ),
    Bool8("flags_2", 
        "node_16_48_80_112_144_176_208_240",
        "node_17_49_81_113_145_177_209_241",
        "node_18_50_82_114_146_178_210_242",
        "node_19_51_83_115_147_179_211_243",
        "node_20_52_84_116_148_180_212_244",
        "node_21_53_85_117_149_181_213_245",
        "node_22_54_86_118_150_182_214_246",
        "node_23_55_87_119_151_183_215_247",
        ),
    Bool8("flags_3", 
        "node_24_56_88_120_152_184_216_248",
        "node_25_57_89_121_153_185_217_249",
        "node_26_58_90_122_154_186_218_250",
        "node_27_59_91_123_155_187_219_251",
        "node_28_60_92_124_156_188_220_252",
        "node_29_61_93_125_157_189_221_253",
        "node_30_62_94_126_158_190_222_254",
        "node_31_63_95_127_159_191_223_255",
        ),
    ENDIAN=">", SIZE=4
    )


scnr_control_node_positioning_orientations_readable = Struct("orientations_readable", 
    QStruct("rotation", INCLUDE=ijkw_sint16),
    ENDIAN=">", SIZE=8
    )


scnr_control_node_positioning = Struct("node_positioning", 
    SInt16("node_count"),
    SInt16("unknown", VISIBLE=False),
    h3_reflexive("node_flags_readable", scnr_control_node_positioning_node_flags_readable),
    h3_reflexive("orientations_readable", scnr_control_node_positioning_orientations_readable),
    ENDIAN=">", SIZE=28
    )


scnr_control = Struct("control", 
    SInt16("palette_index"),
    SInt16("name_index"),
    Bool32("placement_flags", 
        "not_automatically",
        "not_on_easy",
        "not_on_normal",
        "not_on_hard",
        "lock_type_to_env_object",
        "lock_transform_to_env_object",
        "never_placed",
        "lock_name_to_env_object",
        "create_at_rest",
        ),
    QStruct("position", INCLUDE=xyz_float),
    ypr_float_rad("rotation"),
    Float("scale"),
    h3_reflexive("node_positioning", scnr_control_node_positioning),
    SInt16("unknown_0", VISIBLE=False),
    Bool16("old_manual_bsp_flags_now_zonesets", *("set_%s" % i for i in range(16))),
    h3_string_id("unique_name"),
    UInt16("unique_id_salt"),
    UInt16("unique_id_index"),
    SInt16("origin_bsp_index"),
    SEnum8("type", *bloc_object_type),
    SEnum8("source", *scnr_scenery_source),
    SEnum8("bsp_policy", *scnr_scenery_bsp_policy),
    SInt8("unknown_1", VISIBLE=False),
    SInt16("editor_folder_index"),
    SInt16("unknown_2", VISIBLE=False),
    SInt16("parent_name_index"),
    h3_string_id("child_name"),
    h3_string_id("unknown_3"),
    Bool16("allowed_zonesets", *("set_%s" % i for i in range(16))),
    SInt16("unknown_4", VISIBLE=False),
    SInt16("power_group"),
    SInt16("position_group"),
    Bool32("device_flags", 
        "initially_open",
        "initially_closed",
        "can_only_change_once",
        "position_reversed",
        "usable_from_both_sides",
        ),
    Bool32("control_flags", 
        "usable_from_both_sides",
        ),
    SInt16("unknown_5"),
    SInt16("unknown_6"),
    ENDIAN=">", SIZE=100
    )


scnr_control_palette = Struct("control_palette", 
    h3_dependency("control"),
    BytesRaw("unknown", SIZE=32, VISIBLE=False),
    ENDIAN=">", SIZE=48
    )


scnr_sound_scenery_node_positioning_node_flags_readable = Struct("node_flags_readable", 
    Bool8("flags_0", 
        "node_0_32_64_96_128_160_192_224",
        "node_1_33_65_97_129_161_193_225",
        "node_2_34_66_98_130_162_194_226",
        "node_3_35_67_99_131_163_195_227",
        "node_4_36_68_100_132_164_196_228",
        "node_5_37_69_101_133_165_197_229",
        "node_6_38_70_102_134_166_198_230",
        "node_7_39_71_103_135_167_199_231",
        ),
    Bool8("flags_1", 
        "node_8_40_72_104_136_168_200_232",
        "node_9_41_73_105_137_169_201_233",
        "node_10_42_74_106_138_170_202_234",
        "node_11_43_75_107_139_171_203_235",
        "node_12_44_76_108_140_172_204_236",
        "node_13_45_77_109_141_173_205_237",
        "node_14_46_78_110_142_174_206_238",
        "node_15_47_79_111_143_175_207_239",
        ),
    Bool8("flags_2", 
        "node_16_48_80_112_144_176_208_240",
        "node_17_49_81_113_145_177_209_241",
        "node_18_50_82_114_146_178_210_242",
        "node_19_51_83_115_147_179_211_243",
        "node_20_52_84_116_148_180_212_244",
        "node_21_53_85_117_149_181_213_245",
        "node_22_54_86_118_150_182_214_246",
        "node_23_55_87_119_151_183_215_247",
        ),
    Bool8("flags_3", 
        "node_24_56_88_120_152_184_216_248",
        "node_25_57_89_121_153_185_217_249",
        "node_26_58_90_122_154_186_218_250",
        "node_27_59_91_123_155_187_219_251",
        "node_28_60_92_124_156_188_220_252",
        "node_29_61_93_125_157_189_221_253",
        "node_30_62_94_126_158_190_222_254",
        "node_31_63_95_127_159_191_223_255",
        ),
    ENDIAN=">", SIZE=4
    )


scnr_sound_scenery_node_positioning_orientations_readable = Struct("orientations_readable", 
    QStruct("rotation", INCLUDE=ijkw_sint16),
    ENDIAN=">", SIZE=8
    )


scnr_sound_scenery_node_positioning = Struct("node_positioning", 
    SInt16("node_count"),
    SInt16("unknown", VISIBLE=False),
    h3_reflexive("node_flags_readable", scnr_sound_scenery_node_positioning_node_flags_readable),
    h3_reflexive("orientations_readable", scnr_sound_scenery_node_positioning_orientations_readable),
    ENDIAN=">", SIZE=28
    )


scnr_sound_scenery = Struct("sound_scenery", 
    SInt16("palette_index"),
    SInt16("name_index"),
    Bool32("placement_flags", 
        "not_automatically",
        "not_on_easy",
        "not_on_normal",
        "not_on_hard",
        "lock_type_to_env_object",
        "lock_transform_to_env_object",
        "never_placed",
        "lock_name_to_env_object",
        "create_at_rest",
        ),
    QStruct("position", INCLUDE=xyz_float),
    ypr_float_rad("rotation"),
    Float("scale"),
    h3_reflexive("node_positioning", scnr_sound_scenery_node_positioning),
    SInt16("unknown_0", VISIBLE=False),
    Bool16("old_manual_bsp_flags_now_zonesets", *("set_%s" % i for i in range(16))),
    h3_string_id("unique_name"),
    UInt16("unique_id_salt"),
    UInt16("unique_id_index"),
    SInt16("origin_bsp_index"),
    SEnum8("type", *bloc_object_type),
    SEnum8("source", *scnr_scenery_source),
    SEnum8("bsp_policy", *scnr_scenery_bsp_policy),
    SInt8("unknown_1", VISIBLE=False),
    SInt16("editor_folder_index"),
    SInt16("unknown_2", VISIBLE=False),
    SInt16("parent_name_index"),
    h3_string_id("child_name"),
    h3_string_id("unknown_3"),
    Bool16("allowed_zonesets", *("set_%s" % i for i in range(16))),
    SInt16("unknown_4", VISIBLE=False),
    SInt32("volume_type"),
    Float("height"),
    QStruct("override_distance", INCLUDE=from_to),
    from_to_rad("override_cone_angle"),
    Float("override_outer_cone_gain"),
    ENDIAN=">", SIZE=112
    )


scnr_sound_scenery_palette = Struct("sound_scenery_palette", 
    h3_dependency("sound_scenery"),
    BytesRaw("unknown", SIZE=32, VISIBLE=False),
    ENDIAN=">", SIZE=48
    )


scnr_giant_node_positioning_node_flags_readable = Struct("node_flags_readable", 
    Bool8("flags_0", 
        "node_0_32_64_96_128_160_192_224",
        "node_1_33_65_97_129_161_193_225",
        "node_2_34_66_98_130_162_194_226",
        "node_3_35_67_99_131_163_195_227",
        "node_4_36_68_100_132_164_196_228",
        "node_5_37_69_101_133_165_197_229",
        "node_6_38_70_102_134_166_198_230",
        "node_7_39_71_103_135_167_199_231",
        ),
    Bool8("flags_1", 
        "node_8_40_72_104_136_168_200_232",
        "node_9_41_73_105_137_169_201_233",
        "node_10_42_74_106_138_170_202_234",
        "node_11_43_75_107_139_171_203_235",
        "node_12_44_76_108_140_172_204_236",
        "node_13_45_77_109_141_173_205_237",
        "node_14_46_78_110_142_174_206_238",
        "node_15_47_79_111_143_175_207_239",
        ),
    Bool8("flags_2", 
        "node_16_48_80_112_144_176_208_240",
        "node_17_49_81_113_145_177_209_241",
        "node_18_50_82_114_146_178_210_242",
        "node_19_51_83_115_147_179_211_243",
        "node_20_52_84_116_148_180_212_244",
        "node_21_53_85_117_149_181_213_245",
        "node_22_54_86_118_150_182_214_246",
        "node_23_55_87_119_151_183_215_247",
        ),
    Bool8("flags_3", 
        "node_24_56_88_120_152_184_216_248",
        "node_25_57_89_121_153_185_217_249",
        "node_26_58_90_122_154_186_218_250",
        "node_27_59_91_123_155_187_219_251",
        "node_28_60_92_124_156_188_220_252",
        "node_29_61_93_125_157_189_221_253",
        "node_30_62_94_126_158_190_222_254",
        "node_31_63_95_127_159_191_223_255",
        ),
    ENDIAN=">", SIZE=4
    )


scnr_giant_node_positioning_orientations_readable = Struct("orientations_readable", 
    QStruct("rotation", INCLUDE=ijkw_sint16),
    ENDIAN=">", SIZE=8
    )


scnr_giant_node_positioning = Struct("node_positioning", 
    SInt16("node_count"),
    SInt16("unknown", VISIBLE=False),
    h3_reflexive("node_flags_readable", scnr_giant_node_positioning_node_flags_readable),
    h3_reflexive("orientations_readable", scnr_giant_node_positioning_orientations_readable),
    ENDIAN=">", SIZE=28
    )


scnr_giant_pathfinding_reference = Struct("pathfinding_reference", 
    SInt16("bsp_index"),
    SInt16("pathfinding_object_index"),
    ENDIAN=">", SIZE=4
    )


scnr_giant = Struct("giant", 
    SInt16("palette_index"),
    SInt16("name_index"),
    Bool32("placement_flags", 
        "not_automatically",
        "not_on_easy",
        "not_on_normal",
        "not_on_hard",
        "lock_type_to_env_object",
        "lock_transform_to_env_object",
        "never_placed",
        "lock_name_to_env_object",
        "create_at_rest",
        ),
    QStruct("position", INCLUDE=xyz_float),
    ypr_float_rad("rotation"),
    Float("scale"),
    h3_reflexive("node_positioning", scnr_giant_node_positioning),
    SInt16("unknown_0", VISIBLE=False),
    Bool16("old_manual_bsp_flags_now_zonesets", *("set_%s" % i for i in range(16))),
    h3_string_id("unique_name"),
    UInt16("unique_id_salt"),
    UInt16("unique_id_index"),
    SInt16("origin_bsp_index"),
    SEnum8("type", *bloc_object_type),
    SEnum8("source", *scnr_scenery_source),
    SEnum8("bsp_policy", *scnr_scenery_bsp_policy),
    SInt8("unknown_1", VISIBLE=False),
    SInt16("editor_folder_index"),
    SInt16("unknown_2", VISIBLE=False),
    SInt16("parent_name_index"),
    h3_string_id("child_name"),
    h3_string_id("unknown_3"),
    Bool16("allowed_zonesets", *("set_%s" % i for i in range(16))),
    SInt16("unknown_4", VISIBLE=False),
    h3_string_id("variant"),
    Bool8("active_change_colors", 
        "primary",
        "secondary",
        "tertiary",
        "quaternary",
        ),
    SInt8("unknown_5", VISIBLE=False),
    SInt8("unknown_6", VISIBLE=False),
    SInt8("unknown_7", VISIBLE=False),
    color_argb_uint32("primary_color"),
    color_argb_uint32("secondary_color"),
    color_argb_uint32("tertiary_color"),
    color_argb_uint32("quaternary_color"),
    Float("body_vitality_percentage"),
    Bool32("flags", 
        "dead",
        "closed",
        "not_enterable_by_player",
        ),
    SEnum16("unknown_8", *scnr_giant_unknown_8, VISIBLE=False),
    SInt16("unknown_9"),
    h3_reflexive("pathfinding_references", scnr_giant_pathfinding_reference),
    ENDIAN=">", SIZE=132
    )


scnr_giant_palette = Struct("giant_palette", 
    h3_dependency("giant"),
    BytesRaw("unknown", SIZE=32, VISIBLE=False),
    ENDIAN=">", SIZE=48
    )


scnr_effect_scenery_node_positioning_node_flags_readable = Struct("node_flags_readable", 
    Bool8("flags_0", 
        "node_0_32_64_96_128_160_192_224",
        "node_1_33_65_97_129_161_193_225",
        "node_2_34_66_98_130_162_194_226",
        "node_3_35_67_99_131_163_195_227",
        "node_4_36_68_100_132_164_196_228",
        "node_5_37_69_101_133_165_197_229",
        "node_6_38_70_102_134_166_198_230",
        "node_7_39_71_103_135_167_199_231",
        ),
    Bool8("flags_1", 
        "node_8_40_72_104_136_168_200_232",
        "node_9_41_73_105_137_169_201_233",
        "node_10_42_74_106_138_170_202_234",
        "node_11_43_75_107_139_171_203_235",
        "node_12_44_76_108_140_172_204_236",
        "node_13_45_77_109_141_173_205_237",
        "node_14_46_78_110_142_174_206_238",
        "node_15_47_79_111_143_175_207_239",
        ),
    Bool8("flags_2", 
        "node_16_48_80_112_144_176_208_240",
        "node_17_49_81_113_145_177_209_241",
        "node_18_50_82_114_146_178_210_242",
        "node_19_51_83_115_147_179_211_243",
        "node_20_52_84_116_148_180_212_244",
        "node_21_53_85_117_149_181_213_245",
        "node_22_54_86_118_150_182_214_246",
        "node_23_55_87_119_151_183_215_247",
        ),
    Bool8("flags_3", 
        "node_24_56_88_120_152_184_216_248",
        "node_25_57_89_121_153_185_217_249",
        "node_26_58_90_122_154_186_218_250",
        "node_27_59_91_123_155_187_219_251",
        "node_28_60_92_124_156_188_220_252",
        "node_29_61_93_125_157_189_221_253",
        "node_30_62_94_126_158_190_222_254",
        "node_31_63_95_127_159_191_223_255",
        ),
    ENDIAN=">", SIZE=4
    )


scnr_effect_scenery_node_positioning_orientations_readable = Struct("orientations_readable", 
    QStruct("rotation", INCLUDE=ijkw_sint16),
    ENDIAN=">", SIZE=8
    )


scnr_effect_scenery_node_positioning = Struct("node_positioning", 
    SInt16("node_count"),
    SInt16("unknown", VISIBLE=False),
    h3_reflexive("node_flags_readable", scnr_effect_scenery_node_positioning_node_flags_readable),
    h3_reflexive("orientations_readable", scnr_effect_scenery_node_positioning_orientations_readable),
    ENDIAN=">", SIZE=28
    )


scnr_effect_scenery = Struct("effect_scenery", 
    SInt16("palette_index"),
    SInt16("name_index"),
    Bool32("placement_flags", 
        "not_automatically",
        "not_on_easy",
        "not_on_normal",
        "not_on_hard",
        "lock_type_to_env_object",
        "lock_transform_to_env_object",
        "never_placed",
        "lock_name_to_env_object",
        "create_at_rest",
        ),
    QStruct("position", INCLUDE=xyz_float),
    ypr_float_rad("rotation"),
    Float("scale"),
    h3_reflexive("node_positioning", scnr_effect_scenery_node_positioning),
    SInt16("unknown_0", VISIBLE=False),
    Bool16("old_manual_bsp_flags_now_zonesets", *("set_%s" % i for i in range(16))),
    h3_string_id("unique_name"),
    UInt16("unique_id_salt"),
    UInt16("unique_id_index"),
    SInt16("origin_bsp_index"),
    SEnum8("type", *bloc_object_type),
    SEnum8("source", *scnr_scenery_source),
    SEnum8("bsp_policy", *scnr_scenery_bsp_policy),
    SInt8("unknown_1", VISIBLE=False),
    SInt16("editor_folder_index"),
    SInt16("unknown_2", VISIBLE=False),
    SInt16("parent_name_index"),
    h3_string_id("child_name"),
    h3_string_id("unknown_3"),
    Bool16("allowed_zonesets", *("set_%s" % i for i in range(16))),
    SInt16("unknown_4", VISIBLE=False),
    ENDIAN=">", SIZE=84
    )


scnr_effect_scenery_palette = Struct("effect_scenery_palette", 
    h3_dependency("effect_scenery"),
    BytesRaw("unknown", SIZE=32, VISIBLE=False),
    ENDIAN=">", SIZE=48
    )


scnr_light_volume_node_positioning_node_flags_readable = Struct("node_flags_readable", 
    Bool8("flags_0", 
        "node_0_32_64_96_128_160_192_224",
        "node_1_33_65_97_129_161_193_225",
        "node_2_34_66_98_130_162_194_226",
        "node_3_35_67_99_131_163_195_227",
        "node_4_36_68_100_132_164_196_228",
        "node_5_37_69_101_133_165_197_229",
        "node_6_38_70_102_134_166_198_230",
        "node_7_39_71_103_135_167_199_231",
        ),
    Bool8("flags_1", 
        "node_8_40_72_104_136_168_200_232",
        "node_9_41_73_105_137_169_201_233",
        "node_10_42_74_106_138_170_202_234",
        "node_11_43_75_107_139_171_203_235",
        "node_12_44_76_108_140_172_204_236",
        "node_13_45_77_109_141_173_205_237",
        "node_14_46_78_110_142_174_206_238",
        "node_15_47_79_111_143_175_207_239",
        ),
    Bool8("flags_2", 
        "node_16_48_80_112_144_176_208_240",
        "node_17_49_81_113_145_177_209_241",
        "node_18_50_82_114_146_178_210_242",
        "node_19_51_83_115_147_179_211_243",
        "node_20_52_84_116_148_180_212_244",
        "node_21_53_85_117_149_181_213_245",
        "node_22_54_86_118_150_182_214_246",
        "node_23_55_87_119_151_183_215_247",
        ),
    Bool8("flags_3", 
        "node_24_56_88_120_152_184_216_248",
        "node_25_57_89_121_153_185_217_249",
        "node_26_58_90_122_154_186_218_250",
        "node_27_59_91_123_155_187_219_251",
        "node_28_60_92_124_156_188_220_252",
        "node_29_61_93_125_157_189_221_253",
        "node_30_62_94_126_158_190_222_254",
        "node_31_63_95_127_159_191_223_255",
        ),
    ENDIAN=">", SIZE=4
    )


scnr_light_volume_node_positioning_orientations_readable = Struct("orientations_readable", 
    QStruct("rotation", INCLUDE=ijkw_sint16),
    ENDIAN=">", SIZE=8
    )


scnr_light_volume_node_positioning = Struct("node_positioning", 
    SInt16("node_count"),
    SInt16("unknown", VISIBLE=False),
    h3_reflexive("node_flags_readable", scnr_light_volume_node_positioning_node_flags_readable),
    h3_reflexive("orientations_readable", scnr_light_volume_node_positioning_orientations_readable),
    ENDIAN=">", SIZE=28
    )


scnr_light_volume = Struct("light_volume", 
    SInt16("palette_index"),
    SInt16("name_index"),
    Bool32("placement_flags", 
        "not_automatically",
        "not_on_easy",
        "not_on_normal",
        "not_on_hard",
        "lock_type_to_env_object",
        "lock_transform_to_env_object",
        "never_placed",
        "lock_name_to_env_object",
        "create_at_rest",
        ),
    QStruct("position_0", INCLUDE=xyz_float),
    ypr_float_rad("rotation"),
    Float("scale"),
    h3_reflexive("node_positioning", scnr_light_volume_node_positioning),
    SInt16("unknown_0", VISIBLE=False),
    Bool16("old_manual_bsp_flags_now_zonesets", *("set_%s" % i for i in range(16))),
    h3_string_id("unique_name"),
    UInt16("unique_id_salt"),
    UInt16("unique_id_index"),
    SInt16("origin_bsp_index"),
    SEnum8("type_0", *bloc_object_type),
    SEnum8("source", *scnr_scenery_source),
    SEnum8("bsp_policy", *scnr_scenery_bsp_policy),
    SInt8("unknown_1", VISIBLE=False),
    SInt16("editor_folder_index"),
    SInt16("unknown_2", VISIBLE=False),
    SInt16("parent_name_index"),
    h3_string_id("child_name"),
    h3_string_id("unknown_3"),
    Bool16("allowed_zonesets", *("set_%s" % i for i in range(16))),
    SInt16("unknown_4", VISIBLE=False),
    SInt16("power_group"),
    SInt16("position_group"),
    Bool32("device_flags", 
        "initially_open",
        "initially_closed",
        "can_only_change_once",
        "position_reversed",
        "usable_from_both_sides",
        ),
    SEnum16("type_1", *scnr_light_volume_type_1),
    Bool16("flags", 
        "custom_geometry",
        ("cinematic_only", 1 << 2),
        ),
    SEnum16("lightmap_type", *scnr_light_volume_lightmap_type),
    Bool16("lightmap_flags", *unknown_flags_1),
    Float("lightmap_half_life"),
    Float("lightmap_light_scale"),
    QStruct("position_1", INCLUDE=xyz_float),
    Float("width"),
    Float("height_scale"),
    float_rad("field_of_view"),
    Float("falloff_distance"),
    Float("cutoff_distance"),
    ENDIAN=">", SIZE=140
    )


scnr_light_volumes_palette = Struct("light_volumes_palette", 
    h3_dependency("light_volume"),
    BytesRaw("unknown", SIZE=32, VISIBLE=False),
    ENDIAN=">", SIZE=48
    )


scnr_sandbox_vehicle = Struct("sandbox_vehicle", 
    h3_dependency("object"),
    h3_string_id("name"),
    SInt32("max_allowed"),
    Float("cost"),
    BytesRaw("unknown", SIZE=20, VISIBLE=False),
    ENDIAN=">", SIZE=48
    )


scnr_sandbox_weapon = Struct("sandbox_weapon", 
    h3_dependency("object"),
    h3_string_id("name"),
    SInt32("max_allowed"),
    Float("cost"),
    BytesRaw("unknown", SIZE=20, VISIBLE=False),
    ENDIAN=">", SIZE=48
    )


scnr_sandbox_equipment = Struct("sandbox_equipment", 
    h3_dependency("object"),
    h3_string_id("name"),
    SInt32("max_allowed"),
    Float("cost"),
    BytesRaw("unknown", SIZE=20, VISIBLE=False),
    ENDIAN=">", SIZE=48
    )


scnr_sandbox_scenery = Struct("sandbox_scenery", 
    h3_dependency("object"),
    h3_string_id("name"),
    SInt32("max_allowed"),
    Float("cost"),
    BytesRaw("unknown", SIZE=20, VISIBLE=False),
    ENDIAN=">", SIZE=48
    )


scnr_sandbox_teleporter = Struct("sandbox_teleporter", 
    h3_dependency("object"),
    h3_string_id("name"),
    SInt32("max_allowed"),
    Float("cost"),
    BytesRaw("unknown", SIZE=20, VISIBLE=False),
    ENDIAN=">", SIZE=48
    )


scnr_sandbox_goal_object = Struct("sandbox_goal_object", 
    h3_dependency("object"),
    h3_string_id("name"),
    SInt32("max_allowed"),
    Float("cost"),
    BytesRaw("unknown", SIZE=20, VISIBLE=False),
    ENDIAN=">", SIZE=48
    )


scnr_sandbox_spawning = Struct("sandbox_spawning", 
    h3_dependency("object"),
    h3_string_id("name"),
    SInt32("max_allowed"),
    Float("cost"),
    BytesRaw("unknown", SIZE=20, VISIBLE=False),
    ENDIAN=">", SIZE=48
    )


scnr_soft_ceiling = Struct("soft_ceiling", 
    SInt16("type"),
    SInt16("unknown_0"),
    h3_string_id("name"),
    SInt16("unknown_1"),
    SInt16("unknown_2"),
    ENDIAN=">", SIZE=12
    )


scnr_player_starting_profile = Struct("player_starting_profile", 
    ascii_str32("name"),
    Float("starting_health_damage"),
    Float("starting_shield_damage"),
    h3_dependency("primary_weapon"),
    SInt16("rounds_loaded_0"),
    SInt16("rounds_total_0"),
    h3_dependency("secondary_weapon"),
    SInt16("rounds_loaded_1"),
    SInt16("rounds_total_1"),
    UInt8("starting_frag_grenade_count"),
    UInt8("starting_plasma_grenade_count"),
    UInt8("starting_spike_grenade_count"),
    UInt8("starting_firebomb_grenade_count"),
    ENDIAN=">", SIZE=84
    )


scnr_player_starting_location = Struct("player_starting_location", 
    QStruct("position", INCLUDE=xyz_float),
    yp_float_rad("facing"),
    SInt16("unknown", VISIBLE=False),
    SEnum16("campaign_player_type", *scnr_player_starting_location_campaign_player_type),
    ENDIAN=">", SIZE=24
    )


scnr_trigger_volume = Struct("trigger_volume", 
    h3_string_id("name"),
    SInt16("object_name"),
    SInt16("unknown_0", VISIBLE=False),
    h3_string_id("node_name"),
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=6, VISIBLE=False),
    QStruct("position", INCLUDE=xyz_float),
    QStruct("extents", INCLUDE=xyz_float),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    SInt16("kill_volume"),
    SInt16("editor_folder_index"),
    ENDIAN=">", SIZE=68
    )


scnr_zoneset_switch_trigger_volume = Struct("zoneset_switch_trigger_volume", 
    SInt16("unknown"),
    SInt16("included_zoneset_index"),
    SInt16("trigger_volume"),
    SInt16("sole_zoneset_index"),
    ENDIAN=">", SIZE=8
    )


scnr_multiplayer_constants_override = Struct("multiplayer_constants_override", 
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=5),
    ENDIAN=">", SIZE=20
    )


scnr_unknown_4 = Struct("unknown_4", 
    BytesRaw("unknown", SIZE=20, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=20
    )


scnr_unknown_5 = Struct("unknown_5", 
    BytesRaw("unknown", SIZE=20, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=20
    )


scnr_unknown_6 = Struct("unknown_6", 
    BytesRaw("unknown", SIZE=20, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=20
    )


scnr_unknown_7 = Struct("unknown_7", 
    BytesRaw("unknown", SIZE=20, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=20
    )


scnr_decal = Struct("decal", 
    SInt16("palette_index"),
    SInt8("yaw"),
    SInt8("pitch"),
    QStruct("rotation", INCLUDE=ijkw_float),
    QStruct("position", INCLUDE=xyz_float),
    Float("scale"),
    ENDIAN=">", SIZE=36
    )


scnr_decal_palette = Struct("decal_palette", 
    h3_dependency("decal"),
    ENDIAN=">", SIZE=16
    )


scnr_style_palette = Struct("style_palette", 
    h3_dependency("style"),
    ENDIAN=">", SIZE=16
    )


scnr_squad_group = Struct("squad_group", 
    ascii_str32("name"),
    SInt16("parent_index"),
    SInt16("objective_index"),
    SInt16("unknown_0"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=40
    )


scnr_squad_base_squad_multi_state = Struct("multi_state", 
    SInt16("unknown_0"),
    SInt16("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    h3_string_id("state"),
    Pad(4),
    ascii_str32("command_script_name"),
    SInt16("command_script_index"),
    SInt16("unknown_5", VISIBLE=False),
    ENDIAN=">", SIZE=56
    )


scnr_squad_base_squad_starting_location_multi_state = Struct("multi_state", 
    SInt16("unknown_0"),
    SInt16("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    h3_string_id("state"),
    Pad(4),
    ascii_str32("command_script_name"),
    SInt16("command_script_index"),
    SInt16("unknown_5", VISIBLE=False),
    ENDIAN=">", SIZE=56
    )


scnr_squad_base_squad_starting_location = Struct("starting_location", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    h3_string_id("name"),
    QStruct("position", INCLUDE=xyz_float),
    SInt16("reference_frame"),
    SInt16("unknown_2", VISIBLE=False),
    ypr_float_rad("facing"),
    Bool32("flags", 
        ("always_place", 1 << 2),
        "initially_hidden",
        "kill_vehicle_if_no_driver",
        ),
    SInt16("character_type"),
    SInt16("initial_primary_weapon"),
    SInt16("initial_secondary_weapon"),
    SInt16("unknown_3", VISIBLE=False),
    SInt16("vehicle_type"),
    SEnum16("seat_type", *scnr_squad_base_squad_starting_location_seat_type),
    SEnum16("grenade_type", *scnr_squad_base_squad_grenade_type),
    SInt16("swarm_count"),
    h3_string_id("actor_variant"),
    h3_string_id("vehicle_variant"),
    Float("initial_movement_distance"),
    SInt16("emitter_vehicle"),
    SInt16("emitter_giant"),
    SInt16("emitter_biped"),
    SEnum16("initial_movement_mode", *scnr_squad_base_squad_starting_location_initial_movement_mode),
    ascii_str32("command_script_name"),
    SInt16("command_script_index"),
    SInt16("unknown_4", VISIBLE=False),
    h3_string_id("initial_state"),
    Array("unknown_array", SUB_STRUCT=SInt16("unknown"), SIZE=4, VISIBLE=False),
    h3_reflexive("multi_state", scnr_squad_base_squad_starting_location_multi_state),
    ENDIAN=">", SIZE=136
    )


scnr_squad_base_squad = Struct("base_squad", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    SInt16("size"),
    SInt16("unknown_2", VISIBLE=False),
    SInt16("character_type"),
    SInt16("initial_primary_weapon"),
    SInt16("initial_secondary_weapon"),
    SEnum16("grenade_type", *scnr_squad_base_squad_grenade_type),
    SInt16("equipment"),
    SInt16("vehicle"),
    h3_string_id("vehicle_variant"),
    ascii_str32("command_script_name"),
    SInt16("command_script_index"),
    SInt16("unknown_3", VISIBLE=False),
    h3_string_id("initial_state"),
    Array("unknown_array", SUB_STRUCT=SInt16("unknown"), SIZE=4, VISIBLE=False),
    h3_reflexive("multi_state", scnr_squad_base_squad_multi_state),
    h3_reflexive("starting_locations", scnr_squad_base_squad_starting_location),
    ENDIAN=">", SIZE=96
    )


scnr_squad = Struct("squad", 
    ascii_str32("name"),
    Bool32("flags", 
        ("blind", 1 << 1),
        "deaf",
        "braindead",
        "initially_placed",
        "units_not_enterable_by_player",
        ),
    SEnum16("team", *crea_default_team),
    SInt16("parent_squad_group_index"),
    SInt16("parent_zone"),
    SInt16("trigger_index"),
    SInt16("objective_index"),
    SInt16("objective_role_index", VISIBLE=False),
    h3_reflexive("base_squad", scnr_squad_base_squad),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    ENDIAN=">", SIZE=64
    )


scnr_zone_firing_position = Struct("firing_position", 
    QStruct("position", INCLUDE=xyz_float),
    SInt16("reference_frame"),
    SInt16("unknown_0", VISIBLE=False),
    Bool16("flags", 
        "open",
        "partial",
        "closed",
        "mobile",
        "wall_lean",
        "perch",
        "ground_point",
        "dynamic_cover_point",
        ),
    SInt16("unknown_1", VISIBLE=False),
    SInt16("area_index"),
    SInt16("cluster_index"),
    SInt32("unknown_2", VISIBLE=False),
    yp_float_rad("normal"),
    BytesRaw("unknown_3", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=40
    )


scnr_zone_area_flight_hint = Struct("flight_hint", 
    SInt16("flight_hint_index"),
    SInt16("poit_index"),
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=8
    )


scnr_zone_area = Struct("area", 
    ascii_str32("name"),
    Bool32("area_flags", 
        "vehicle_area",
        "perch",
        "manual_reference_frame",
        ),
    QStruct("position", INCLUDE=xyz_float),
    SInt32("unknown_0", VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    SInt16("firing_position_start_index"),
    SInt16("firing_position_count"),
    SInt16("unknown_2", VISIBLE=False),
    SInt16("unknown_3", VISIBLE=False),
    SInt32("unknown_4", VISIBLE=False),
    BytesRaw("unknown_5", SIZE=24, VISIBLE=False),
    SInt16("manual_reference_frame"),
    SInt16("unknown_6", VISIBLE=False),
    h3_reflexive("flight_hints", scnr_zone_area_flight_hint),
    ENDIAN=">", SIZE=108
    )


scnr_zone = Struct("zone", 
    ascii_str32("name"),
    Bool32("flags", 
        "uses_manual_bsp_index",
        ),
    SInt16("manual_bsp_index"),
    SInt16("unknown", VISIBLE=False),
    h3_reflexive("firing_positions", scnr_zone_firing_position),
    h3_reflexive("areas", scnr_zone_area),
    ENDIAN=">", SIZE=64
    )


scnr_character_palette = Struct("character_palette", 
    h3_dependency("character"),
    ENDIAN=">", SIZE=16
    )


scnr_ai_pathfinding_data_unknown_0 = Struct("unknown_0", 
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    Float("unknown_3", VISIBLE=False),
    SInt16("unknown_4", VISIBLE=False),
    SInt16("unknown_5", VISIBLE=False),
    Float("unknown_6", VISIBLE=False),
    Float("unknown_7", VISIBLE=False),
    Float("unknown_8", VISIBLE=False),
    SInt16("unknown_9", VISIBLE=False),
    SInt16("unknown_10", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=36
    )


scnr_ai_pathfinding_data_unknown_1 = Struct("unknown_1", 
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    Float("unknown_3", VISIBLE=False),
    SInt16("unknown_4", VISIBLE=False),
    SInt16("unknown_5", VISIBLE=False),
    Float("unknown_6", VISIBLE=False),
    Float("unknown_7", VISIBLE=False),
    Float("unknown_8", VISIBLE=False),
    SInt16("unknown_9", VISIBLE=False),
    SInt16("unknown_10", VISIBLE=False),
    Float("unknown_11", VISIBLE=False),
    Float("unknown_12", VISIBLE=False),
    Float("unknown_13", VISIBLE=False),
    SInt16("unknown_14", VISIBLE=False),
    SInt16("unknown_15", VISIBLE=False),
    Float("unknown_16", VISIBLE=False),
    Float("unknown_17", VISIBLE=False),
    Float("unknown_18", VISIBLE=False),
    SInt16("unknown_19", VISIBLE=False),
    SInt16("unknown_20", VISIBLE=False),
    BytesRaw("unknown_21", SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=72
    )


scnr_ai_pathfinding_data_unknown_2 = Struct("unknown_2", 
    Array("unknown_array", SUB_STRUCT=SInt16("unknown"), SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=8
    )


scnr_ai_pathfinding_data_unknown_3 = Struct("unknown_3", 
    SInt32("unknown_0", VISIBLE=False),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=8
    )


scnr_ai_pathfinding_data_unknown_4_unknown_1 = Struct("unknown_1", 
    BytesRaw("unknown", SIZE=28, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=28
    )


scnr_ai_pathfinding_data_unknown_4 = Struct("unknown_4", 
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    h3_reflexive("unknown_1", scnr_ai_pathfinding_data_unknown_4_unknown_1),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


scnr_ai_pathfinding_data_unknown_5_unknown = Struct("unknown", 
    Float("unknown_0", VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=12
    )


scnr_ai_pathfinding_data_unknown_5 = Struct("unknown_5", 
    h3_reflexive("unknown", scnr_ai_pathfinding_data_unknown_5_unknown),
    VISIBLE=False,
    ENDIAN=">", SIZE=12
    )


scnr_ai_pathfinding_data_unknown_6 = Struct("unknown_6", 
    h3_string_id("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    SInt16("unknown_2", VISIBLE=False),
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=14, VISIBLE=False),
    SInt32("unknown_3", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=68
    )


scnr_ai_pathfinding_data_unknown_7_unknown_unknown = Struct("unknown", 
    Float("unknown_0", VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    SInt16("unknown_3", VISIBLE=False),
    SInt16("unknown_4", VISIBLE=False),
    float_rad("unknown_5", VISIBLE=False),
    float_rad("unknown_6", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=24
    )


scnr_ai_pathfinding_data_unknown_7_unknown = Struct("unknown", 
    h3_reflexive("unknown", scnr_ai_pathfinding_data_unknown_7_unknown_unknown),
    VISIBLE=False,
    ENDIAN=">", SIZE=12
    )


scnr_ai_pathfinding_data_unknown_7 = Struct("unknown_7", 
    h3_reflexive("unknown", scnr_ai_pathfinding_data_unknown_7_unknown),
    VISIBLE=False,
    ENDIAN=">", SIZE=8
    )


scnr_ai_pathfinding_data_unknown_8 = Struct("unknown_8", 
    SInt16("unknown", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=2
    )


scnr_ai_pathfinding_data = Struct("ai_pathfinding_data", 
    h3_reflexive("unknown_0", scnr_ai_pathfinding_data_unknown_0),
    h3_reflexive("unknown_1", scnr_ai_pathfinding_data_unknown_1),
    h3_reflexive("unknown_2", scnr_ai_pathfinding_data_unknown_2),
    h3_reflexive("unknown_3", scnr_ai_pathfinding_data_unknown_3),
    h3_reflexive("unknown_4", scnr_ai_pathfinding_data_unknown_4),
    h3_reflexive("unknown_5", scnr_ai_pathfinding_data_unknown_5),
    h3_reflexive("unknown_6", scnr_ai_pathfinding_data_unknown_6),
    h3_reflexive("unknown_7", scnr_ai_pathfinding_data_unknown_7),
    h3_reflexive("unknown_8", scnr_ai_pathfinding_data_unknown_8),
    VISIBLE=False,
    ENDIAN=">", SIZE=108
    )


scnr_script_parameter = Struct("parameter", 
    ascii_str32("name"),
    SEnum16("type", *scnr_script_return_type),
    SInt16("unknown"),
    ENDIAN=">", SIZE=36
    )


scnr_script = Struct("script", 
    ascii_str32("script_name"),
    SEnum16("script_type", *scnr_script_script_type),
    SEnum16("return_type", *scnr_script_return_type),
    UInt16("root_expression_salt"),
    UInt16("root_expression_index"),
    h3_reflexive("parameters", scnr_script_parameter),
    ENDIAN=">", SIZE=52
    )


scnr_global = Struct("global", 
    ascii_str32("name"),
    SEnum16("type", *scnr_script_return_type),
    SInt16("unknown"),
    UInt16("initialization_expression_salt"),
    UInt16("initialization_expression_index"),
    ENDIAN=">", SIZE=40
    )


scnr_script_reference = Struct("script_reference", 
    h3_dependency("reference"),
    ENDIAN=">", SIZE=16
    )


scnr_scripting_data_point_set_point = Struct("point", 
    ascii_str32("name"),
    QStruct("position", INCLUDE=xyz_float),
    SInt16("reference_frame"),
    SInt16("unknown", VISIBLE=False),
    SInt32("surface_index"),
    yp_float_rad("facing_direction"),
    ENDIAN=">", SIZE=60
    )


scnr_scripting_data_point_set = Struct("point_set", 
    ascii_str32("name"),
    h3_reflexive("points", scnr_scripting_data_point_set_point),
    SInt16("bsp_index"),
    SInt16("manual_reference_frame"),
    Bool32("flags", *unknown_flags_32),
    ENDIAN=">", SIZE=52
    )


scnr_scripting_data = Struct("scripting_data", 
    h3_reflexive("point_sets", scnr_scripting_data_point_set),
    BytesRaw("unknown", SIZE=120, VISIBLE=False),
    ENDIAN=">", SIZE=132
    )


scnr_cutscene_flag = Struct("cutscene_flag", 
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    h3_string_id("name"),
    QStruct("position", INCLUDE=xyz_float),
    yp_float_rad("facing"),
    ENDIAN=">", SIZE=28
    )


scnr_cutscene_camera_point = Struct("cutscene_camera_point", 
    Bool16("flags", *unknown_flags_16),
    SEnum16("type", *scnr_cutscene_camera_point_type),
    ascii_str32("name"),
    SInt32("unknown", VISIBLE=False),
    QStruct("position", INCLUDE=xyz_float),
    ypr_float_rad("orientation"),
    ENDIAN=">", SIZE=64
    )


scnr_cutscene_title = Struct("cutscene_title", 
    h3_string_id("name"),
    SInt16("text_bounds_top"),
    SInt16("text_bounds_left"),
    SInt16("text_bounds_bottom"),
    SInt16("text_bounds_right"),
    SEnum16("horizontal_justification", *scnr_cutscene_title_horizontal_justification),
    SEnum16("vertical_justification", *scnr_cutscene_title_vertical_justification),
    SInt16("font"),
    SInt16("unknown", VISIBLE=False),
    color_argb_uint32("text_color"),
    color_argb_uint32("shadow_color"),
    Float("fade_in_time"),
    Float("uptime"),
    Float("fade_out_time"),
    ENDIAN=">", SIZE=40
    )


scnr_scenario_resource_script_source = Struct("script_source", 
    h3_dependency("hs_source_file", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


scnr_scenario_resource_ai_resource = Struct("ai_resource", 
    h3_dependency("ai_resource", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


scnr_scenario_resource_reference = Struct("reference", 
    h3_dependency("scenery_resource", VISIBLE=False),
    h3_dependency("bipeds_resource", VISIBLE=False),
    h3_dependency("vehicles_resource", VISIBLE=False),
    h3_dependency("equipment_resource", VISIBLE=False),
    h3_dependency("weapons_resource", VISIBLE=False),
    h3_dependency("sound_scenery_resource", VISIBLE=False),
    h3_dependency("lights_resource", VISIBLE=False),
    h3_dependency("devices_resource", VISIBLE=False),
    h3_dependency("effect_scenery_resource", VISIBLE=False),
    h3_dependency("decals_resource", VISIBLE=False),
    h3_dependency("cinematics_resource", VISIBLE=False),
    h3_dependency("trigger_volumes_resource", VISIBLE=False),
    h3_dependency("cluster_data_resource", VISIBLE=False),
    h3_dependency("comments_resource", VISIBLE=False),
    h3_dependency("creature_resource", VISIBLE=False),
    h3_dependency("structure_lighting_resource", VISIBLE=False),
    h3_dependency("decorators_resource", VISIBLE=False),
    h3_dependency("sky_references_resource", VISIBLE=False),
    h3_dependency("cubemap_resource", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=304
    )


scnr_scenario_resource = Struct("scenario_resource", 
    SInt32("unknown", VISIBLE=False),
    h3_reflexive("script_source", scnr_scenario_resource_script_source),
    h3_reflexive("ai_resources", scnr_scenario_resource_ai_resource),
    h3_reflexive("references", scnr_scenario_resource_reference),
    VISIBLE=False,
    ENDIAN=">", SIZE=40
    )


scnr_unit_seats_mapping = Struct("unit_seats_mapping", 
    dependency_uint32("unit", VISIBLE=False),
    Bool32("seats", *("seat_%s" % i for i in range(32))),
    Bool32("seats_2", *("seat_%s" % i for i in range(32, 64))),
    ENDIAN=">", SIZE=12
    )


scnr_scenario_kill_trigger = Struct("scenario_kill_trigger", 
    SInt16("trigger_volume"),
    ENDIAN=">", SIZE=2
    )


scnr_scenario_safe_trigger = Struct("scenario_safe_trigger", 
    SInt16("trigger_volume"),
    ENDIAN=">", SIZE=2
    )


scnr_script_expression = Struct("script_expression", 
    UInt16("salt"),
    UInt16("opcode"),
    SEnum16("value_type", *scnr_script_expression_value_type),
    SInt16("expression_type"),
    UInt16("next_expression_salt"),
    UInt16("next_expression_index"),
    UInt32("string_address"),
    SInt8("value_03_msb"),
    SInt8("value_02_byte"),
    SInt8("value_01_byte"),
    SInt8("value_00_lsb"),
    SInt16("line_number"),
    SInt16("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=24
    )


scnr_ai_trigger_condition = Struct("condition", 
    SEnum16("rule_type", *scnr_ai_trigger_condition_rule_type),
    SInt16("squad"),
    SInt16("squad_group"),
    SInt16("a"),
    Float("x"),
    SInt16("trigger_volume"),
    SInt16("unknown_0", VISIBLE=False),
    ascii_str32("exit_condition_script"),
    SInt16("exit_condition_script_index"),
    SInt16("unknown_1", VISIBLE=False),
    Bool32("flags", 
        "not",
        ),
    ENDIAN=">", SIZE=56
    )


scnr_ai_trigger = Struct("ai_trigger", 
    ascii_str32("name"),
    Bool32("trigger_flags", 
        "latch_on_when_triggered",
        ),
    SEnum16("combination_rule", *scnr_ai_trigger_combination_rule),
    SInt16("unknown", VISIBLE=False),
    h3_reflexive("conditions", scnr_ai_trigger_condition),
    ENDIAN=">", SIZE=52
    )


scnr_background_sound_environment_palette = Struct("background_sound_environment_palette", 
    h3_string_id("name"),
    h3_dependency("sound_environment"),
    Float("cutoff_distance_0"),
    Float("interpolation_speed_0"),
    h3_dependency("background_sound"),
    h3_dependency("inside_cluster_sound"),
    Float("cutoff_distance_1"),
    Bool32("scale_flags", *unknown_flags_32),
    Float("interior_scale"),
    Float("portal_scale"),
    Float("exterior_scale"),
    Float("interpolation_speed_1"),
    ENDIAN=">", SIZE=84
    )


scnr_unknown_16 = Struct("unknown_16", 
    BytesRaw("unknown", SIZE=120, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=120
    )


scnr_fog = Struct("fog", 
    h3_string_id("name"),
    SInt16("unknown_0"),
    SInt16("unknown_1", VISIBLE=False),
    ENDIAN=">", SIZE=8
    )


scnr_camera_effect = Struct("camera_effect", 
    h3_string_id("name"),
    h3_dependency("effect"),
    Array("unknown_array", SUB_STRUCT=SInt8("unknown"), SIZE=4, VISIBLE=False),
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    Float("unknown_3", VISIBLE=False),
    BytesRaw("unknown_4", SIZE=8, VISIBLE=False),
    ENDIAN=">", SIZE=48
    )


scnr_scenario_cluster_data_background_sound_environment = Struct("background_sound_environment", 
    SInt16("background_sound_environment_index"),
    SInt16("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=4
    )


scnr_scenario_cluster_data_unknown_0 = Struct("unknown_0", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


scnr_scenario_cluster_data_unknown_1 = Struct("unknown_1", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


scnr_scenario_cluster_data_cluster_centroid = Struct("cluster_centroid", 
    QStruct("centroid", INCLUDE=xyz_float),
    ENDIAN=">", SIZE=12
    )


scnr_scenario_cluster_data_unknown_2 = Struct("unknown_2", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


scnr_scenario_cluster_data_fog = Struct("fog", 
    SInt16("fog_index"),
    SInt16("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=4
    )


scnr_scenario_cluster_data_camera_effect = Struct("camera_effect", 
    SInt16("camera_effect_index"),
    SInt16("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=4
    )


scnr_scenario_cluster_data = Struct("scenario_cluster_data", 
    h3_dependency("bsp"),
    h3_reflexive("background_sound_environments", scnr_scenario_cluster_data_background_sound_environment),
    h3_reflexive("unknown_0", scnr_scenario_cluster_data_unknown_0),
    h3_reflexive("unknown_1", scnr_scenario_cluster_data_unknown_1),
    SInt32("bsp_checksum"),
    h3_reflexive("cluster_centroids", scnr_scenario_cluster_data_cluster_centroid),
    h3_reflexive("unknown_2", scnr_scenario_cluster_data_unknown_2),
    h3_reflexive("fog", scnr_scenario_cluster_data_fog),
    h3_reflexive("camera_effects", scnr_scenario_cluster_data_camera_effect),
    ENDIAN=">", SIZE=104
    )


scnr_spawn_data_dynamic_spawn_overload = Struct("dynamic_spawn_overload", 
    SInt16("overload_type"),
    SInt16("unknown"),
    Float("inner_radius"),
    Float("outer_radius"),
    Float("weight"),
    ENDIAN=">", SIZE=16
    )


scnr_spawn_data_static_respawn_zone = Struct("static_respawn_zone", 
    h3_string_id("name"),
    Bool32("relevant_teams", 
        "red",
        "blue",
        "green",
        "orange",
        "purple",
        "yellow",
        "brown",
        "pink",
        "neutral",
        ),
    Bool32("relevant_games", *unknown_flags_32),
    Bool32("flags", *unknown_flags_32),
    QStruct("position", INCLUDE=xyz_float),
    Float("lower_height"),
    Float("upper_height"),
    Float("inner_radius"),
    Float("outer_radius"),
    Float("weight"),
    ENDIAN=">", SIZE=48
    )


scnr_spawn_data_static_initial_spawn_zone = Struct("static_initial_spawn_zone", 
    h3_string_id("name"),
    Bool32("relevant_teams", 
        "red",
        "blue",
        "green",
        "orange",
        "purple",
        "yellow",
        "brown",
        "pink",
        "neutral",
        ),
    Bool32("relevant_games", *unknown_flags_32),
    Bool32("flags", *unknown_flags_32),
    QStruct("position", INCLUDE=xyz_float),
    Float("lower_height"),
    Float("upper_height"),
    Float("inner_radius"),
    Float("outer_radius"),
    Float("weight"),
    ENDIAN=">", SIZE=48
    )


scnr_spawn_data = Struct("spawn_data", 
    Float("dynamic_spawn_lower_height"),
    Float("dynamic_spawn_upper_height"),
    Float("game_object_reset_height"),
    Pad(60),
    h3_reflexive("dynamic_spawn_overloads", scnr_spawn_data_dynamic_spawn_overload),
    h3_reflexive("static_respawn_zones", scnr_spawn_data_static_respawn_zone),
    h3_reflexive("static_initial_spawn_zones", scnr_spawn_data_static_initial_spawn_zone),
    ENDIAN=">", SIZE=108
    )


scnr_crate_node_positioning_node_flags_readable = Struct("node_flags_readable", 
    Bool8("flags_0", 
        "node_0_32_64_96_128_160_192_224",
        "node_1_33_65_97_129_161_193_225",
        "node_2_34_66_98_130_162_194_226",
        "node_3_35_67_99_131_163_195_227",
        "node_4_36_68_100_132_164_196_228",
        "node_5_37_69_101_133_165_197_229",
        "node_6_38_70_102_134_166_198_230",
        "node_7_39_71_103_135_167_199_231",
        ),
    Bool8("flags_1", 
        "node_8_40_72_104_136_168_200_232",
        "node_9_41_73_105_137_169_201_233",
        "node_10_42_74_106_138_170_202_234",
        "node_11_43_75_107_139_171_203_235",
        "node_12_44_76_108_140_172_204_236",
        "node_13_45_77_109_141_173_205_237",
        "node_14_46_78_110_142_174_206_238",
        "node_15_47_79_111_143_175_207_239",
        ),
    Bool8("flags_2", 
        "node_16_48_80_112_144_176_208_240",
        "node_17_49_81_113_145_177_209_241",
        "node_18_50_82_114_146_178_210_242",
        "node_19_51_83_115_147_179_211_243",
        "node_20_52_84_116_148_180_212_244",
        "node_21_53_85_117_149_181_213_245",
        "node_22_54_86_118_150_182_214_246",
        "node_23_55_87_119_151_183_215_247",
        ),
    Bool8("flags_3", 
        "node_24_56_88_120_152_184_216_248",
        "node_25_57_89_121_153_185_217_249",
        "node_26_58_90_122_154_186_218_250",
        "node_27_59_91_123_155_187_219_251",
        "node_28_60_92_124_156_188_220_252",
        "node_29_61_93_125_157_189_221_253",
        "node_30_62_94_126_158_190_222_254",
        "node_31_63_95_127_159_191_223_255",
        ),
    ENDIAN=">", SIZE=4
    )


scnr_crate_node_positioning_orientations_readable = Struct("orientations_readable", 
    QStruct("rotation", INCLUDE=ijkw_sint16),
    ENDIAN=">", SIZE=8
    )


scnr_crate_node_positioning = Struct("node_positioning", 
    SInt16("node_count"),
    SInt16("unknown", VISIBLE=False),
    h3_reflexive("node_flags_readable", scnr_crate_node_positioning_node_flags_readable),
    h3_reflexive("orientations_readable", scnr_crate_node_positioning_orientations_readable),
    ENDIAN=">", SIZE=28
    )


scnr_crate_unknown_9 = Struct("unknown_9", 
    Pad(4),
    ENDIAN=">", SIZE=4
    )


scnr_crate = Struct("crate", 
    SInt16("palette_index"),
    SInt16("name_index"),
    Bool32("placement_flags", 
        "not_automatically",
        "not_on_easy",
        "not_on_normal",
        "not_on_hard",
        "lock_type_to_env_object",
        "lock_transform_to_env_object",
        "never_placed",
        "lock_name_to_env_object",
        "create_at_rest",
        ),
    QStruct("position", INCLUDE=xyz_float),
    ypr_float_rad("rotation"),
    Float("scale"),
    h3_reflexive("node_positioning", scnr_crate_node_positioning),
    SInt16("unknown_0", VISIBLE=False),
    Bool16("old_manual_bsp_flags_now_zonesets", *("set_%s" % i for i in range(16))),
    h3_string_id("unique_name"),
    UInt16("unique_id_salt"),
    UInt16("unique_id_index"),
    SInt16("origin_bsp_index"),
    SEnum8("type", *bloc_object_type),
    SEnum8("source", *scnr_scenery_source),
    SEnum8("bsp_policy", *scnr_scenery_bsp_policy),
    SInt8("unknown_1", VISIBLE=False),
    SInt16("editor_folder_index"),
    SInt16("unknown_2", VISIBLE=False),
    SInt16("parent_name_index"),
    h3_string_id("child_name"),
    h3_string_id("unknown_3"),
    Bool16("allowed_zonesets", *("set_%s" % i for i in range(16))),
    SInt16("unknown_4", VISIBLE=False),
    h3_string_id("variant"),
    Bool8("active_change_colors", 
        "primary",
        "secondary",
        "tertiary",
        "quaternary",
        ),
    SInt8("unknown_5", VISIBLE=False),
    SInt8("unknown_6", VISIBLE=False),
    SInt8("unknown_7", VISIBLE=False),
    color_argb_uint32("primary_color"),
    color_argb_uint32("secondary_color"),
    color_argb_uint32("tertiary_color"),
    color_argb_uint32("quaternary_color"),
    Pad(4),
    h3_reflexive("unknown_9", scnr_crate_unknown_9),
    SEnum32("symmetry", *scnr_scenery_symmetry),
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
    SEnum16("team", *scnr_scenery_team),
    SInt8("spawn_sequence"),
    QStruct("runtime", INCLUDE=from_to_sint8),
    Bool8("multiplayer_flags", 
        "is_unique_object",
        "not_placed_at_start",
        ),
    SInt16("spawn_time"),
    SInt16("abandon_time"),
    SInt8("unknown_10", VISIBLE=False),
    SEnum8("shape", *bloc_multiplayer_object_propertie_shape),
    SInt8("teleporter_channel"),
    SInt8("unknown_11", VISIBLE=False),
    SInt16("unknown_12", VISIBLE=False),
    SInt16("attached_name_index"),
    BytesRaw("unknown_13", SIZE=8, VISIBLE=False),
    Float("width_radius"),
    Float("depth"),
    Float("top"),
    Float("bottom"),
    BytesRaw("unknown_14", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=176
    )


scnr_crate_palette = Struct("crate_palette", 
    h3_dependency("crate"),
    BytesRaw("unknown", SIZE=32, VISIBLE=False),
    ENDIAN=">", SIZE=48
    )


scnr_flock_palette = Struct("flock_palette", 
    h3_dependency("flock"),
    ENDIAN=">", SIZE=16
    )


scnr_flock_source = Struct("source", 
    SInt32("unknown", VISIBLE=False),
    QStruct("position", INCLUDE=xyz_float),
    yp_float_rad("starting"),
    Float("radius"),
    Float("weight"),
    Array("unknown_array", SUB_STRUCT=SInt8("unknown"), SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=36
    )


scnr_flock_sink = Struct("sink", 
    QStruct("position", INCLUDE=xyz_float),
    Float("radius"),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


scnr_flock = Struct("flock", 
    h3_string_id("name"),
    SInt16("flock_palette_index"),
    SInt16("bsp_index"),
    SInt16("bounding_trigger_volume"),
    Bool16("flags", *unknown_flags_16),
    Float("ecology_margin"),
    h3_reflexive("sources", scnr_flock_source),
    h3_reflexive("sinks", scnr_flock_sink),
    QStruct("production_frequency", INCLUDE=from_to),
    QStruct("scale", INCLUDE=from_to),
    Float("unknown_0", VISIBLE=False),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    SInt16("creature_palette_index"),
    QStruct("boid_count", INCLUDE=from_to_sint16),
    SInt16("unknown_2", VISIBLE=False),
    ENDIAN=">", SIZE=72
    )


scnr_creature_palette = Struct("creature_palette", 
    h3_dependency("creature"),
    BytesRaw("unknown", SIZE=32, VISIBLE=False),
    ENDIAN=">", SIZE=48
    )


scnr_editor_folder = Struct("editor_folder", 
    SInt32("parent_folder"),
    StrLatin1("name", SIZE=256),
    ENDIAN=">", SIZE=260
    )


scnr_mission_dialogue = Struct("mission_dialogue", 
    h3_dependency("mission_dialogue"),
    ENDIAN=">", SIZE=16
    )


scnr_interpolator = Struct("interpolator", 
    h3_string_id("name"),
    h3_string_id("accelerator_name"),
    h3_string_id("multiplier_name"),
    h3_rawdata_ref("function"),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    ENDIAN=">", SIZE=36
    )


scnr_simulation_definition_table = Struct("simulation_definition_table", 
    dependency_uint32("tag", VISIBLE=False),
    ENDIAN=">", SIZE=4
    )


scnr_unknown_22 = Struct("unknown_22", 
    Array("unknown_array", SUB_STRUCT=SInt16("unknown"), SIZE=8, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


scnr_ai_objective_role_unknown_84 = Struct("unknown_84", 
    BytesRaw("unknown", SIZE=8, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=8
    )


scnr_ai_objective_role_condition = Struct("condition", 
    ascii_str32("name"),
    StrLatin1("condition", SIZE=256),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    ENDIAN=">", SIZE=292
    )


scnr_ai_objective_role_unknown_8 = Struct("unknown_8", 
    Array("unknown_array", SUB_STRUCT=SInt16("unknown"), SIZE=5, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=10
    )


scnr_ai_objective_role_point_geometry = Struct("point_geometry", 
    QStruct("point_0", INCLUDE=xyz_float),
    SInt16("reference_frame_0"),
    SInt16("unknown_0", VISIBLE=False),
    QStruct("point_1", INCLUDE=xyz_float),
    SInt16("reference_frame_1"),
    SInt16("unknown_1", VISIBLE=False),
    ENDIAN=">", SIZE=32
    )


scnr_ai_objective_role = Struct("role", 
    Array("unknown_array", SUB_STRUCT=SInt16("unknown"), SIZE=6, VISIBLE=False),
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    ascii_str32("command_script_name_1"),
    ascii_str32("command_script_name_2"),
    ascii_str32("command_script_name_3"),
    SInt16("command_script_index_1"),
    SInt16("command_script_index_2"),
    SInt16("command_script_index_3"),
    SInt16("unknown_1", VISIBLE=False),
    SInt16("unknown_2", VISIBLE=False),
    SInt16("unknown_3", VISIBLE=False),
    h3_reflexive("unknown_84", scnr_ai_objective_role_unknown_84),
    h3_string_id("task"),
    SInt16("hierarchy_level_from_100"),
    SInt16("previous_role"),
    SInt16("next_role"),
    SInt16("parent_role"),
    h3_reflexive("conditions", scnr_ai_objective_role_condition),
    SInt16("script_index"),
    SInt16("unknown_4", VISIBLE=False),
    SInt16("unknown_5", VISIBLE=False),
    SEnum16("filter", *scnr_ai_objective_role_filter),
    SInt16("min"),
    SInt16("max"),
    SInt16("bodies"),
    SInt16("unknown_6", VISIBLE=False),
    BytesRaw("unknown_7", SIZE=4, VISIBLE=False),
    h3_reflexive("unknown_8", scnr_ai_objective_role_unknown_8),
    h3_reflexive("point_geometry", scnr_ai_objective_role_point_geometry),
    ENDIAN=">", SIZE=204
    )


scnr_ai_objective = Struct("ai_objective", 
    h3_string_id("name"),
    SInt16("zone"),
    SInt16("unknown", VISIBLE=False),
    h3_reflexive("roles", scnr_ai_objective_role),
    ENDIAN=">", SIZE=20
    )


scnr_designer_zoneset_biped = Struct("biped", 
    SInt16("palette_index"),
    ENDIAN=">", SIZE=2
    )


scnr_designer_zoneset_vehicle = Struct("vehicle", 
    SInt16("palette_index"),
    ENDIAN=">", SIZE=2
    )


scnr_designer_zoneset_weapon = Struct("weapon", 
    SInt16("palette_index"),
    ENDIAN=">", SIZE=2
    )


scnr_designer_zoneset_equipment = Struct("equipment", 
    SInt16("palette_index"),
    ENDIAN=">", SIZE=2
    )


scnr_designer_zoneset_scenery = Struct("scenery", 
    SInt16("palette_index"),
    ENDIAN=">", SIZE=2
    )


scnr_designer_zoneset_machine = Struct("machine", 
    SInt16("palette_index"),
    ENDIAN=">", SIZE=2
    )


scnr_designer_zoneset_terminal = Struct("terminal", 
    SInt16("palette_index"),
    ENDIAN=">", SIZE=2
    )


scnr_designer_zoneset_control = Struct("control", 
    SInt16("palette_index"),
    ENDIAN=">", SIZE=2
    )


scnr_designer_zoneset_unknown_1 = Struct("unknown_1", 
    SInt16("palette_index"),
    VISIBLE=False,
    ENDIAN=">", SIZE=2
    )


scnr_designer_zoneset_crate = Struct("crate", 
    SInt16("palette_index"),
    ENDIAN=">", SIZE=2
    )


scnr_designer_zoneset_creature = Struct("creature", 
    SInt16("palette_index"),
    ENDIAN=">", SIZE=2
    )


scnr_designer_zoneset_giant = Struct("giant", 
    SInt16("palette_index"),
    ENDIAN=">", SIZE=2
    )


scnr_designer_zoneset_unknown_2 = Struct("unknown_2", 
    SInt16("palette_index"),
    VISIBLE=False,
    ENDIAN=">", SIZE=2
    )


scnr_designer_zoneset_character = Struct("character", 
    SInt16("palette_index"),
    ENDIAN=">", SIZE=2
    )


scnr_designer_zoneset = Struct("designer_zoneset", 
    h3_string_id("name"),
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    h3_reflexive("bipeds", scnr_designer_zoneset_biped),
    h3_reflexive("vehicles", scnr_designer_zoneset_vehicle),
    h3_reflexive("weapons", scnr_designer_zoneset_weapon),
    h3_reflexive("equipment", scnr_designer_zoneset_equipment),
    h3_reflexive("scenery", scnr_designer_zoneset_scenery),
    h3_reflexive("machines", scnr_designer_zoneset_machine),
    h3_reflexive("terminals", scnr_designer_zoneset_terminal),
    h3_reflexive("controls", scnr_designer_zoneset_control),
    h3_reflexive("unknown_1", scnr_designer_zoneset_unknown_1),
    h3_reflexive("crates", scnr_designer_zoneset_crate),
    h3_reflexive("creatures", scnr_designer_zoneset_creature),
    h3_reflexive("giants", scnr_designer_zoneset_giant),
    h3_reflexive("unknown_2", scnr_designer_zoneset_unknown_2),
    h3_reflexive("characters", scnr_designer_zoneset_character),
    BytesRaw("unknown_3", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=188
    )


scnr_unknown_23 = Struct("unknown_23", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


scnr_cinematic = Struct("cinematic", 
    h3_dependency("cinematic"),
    ENDIAN=">", SIZE=16
    )


scnr_cinematic_lighting = Struct("cinematic_lighting", 
    h3_string_id("name"),
    h3_dependency("cinematic_light"),
    ENDIAN=">", SIZE=20
    )


scnr_scenario_metagame_time_multiplier = Struct("time_multiplier", 
    Float("time"),
    Float("multiplier"),
    ENDIAN=">", SIZE=8
    )


scnr_scenario_metagame = Struct("scenario_metagame", 
    h3_reflexive("time_multipliers", scnr_scenario_metagame_time_multiplier),
    Float("par_score"),
    ENDIAN=">", SIZE=16
    )


scnr_unknown_26 = Struct("unknown_26", 
    BytesRaw("unknown", SIZE=8, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=8
    )


scnr_unknown_27 = Struct("unknown_27", 
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    SInt16("unknown_2", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


scnr_cortana_effect = Struct("cortana_effect", 
    h3_dependency("unknown"),
    ENDIAN=">", SIZE=16
    )


scnr_lightmap_airprobe = Struct("lightmap_airprobe", 
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    h3_string_id("unknown_1", VISIBLE=False),
    Bool16("unknown_2", *unknown_flags_16),
    SInt16("unknown_3", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=20
    )


scnr_body = Struct("tagdata", 
    SEnum16("map_type", *zone_map_type),
    Bool16("flags", 
        ("characters_use_previous_mission_weapons", 1 << 5),
        ),
    SInt32("campaign_id"),
    SInt32("map_id"),
    float_rad("local_north"),
    Float("sandbox_budget"),
    h3_reflexive("structure_bsps", scnr_structure_bsp),
    h3_dependency("unknown_0"),
    h3_reflexive("sky_references", scnr_sky_reference),
    h3_reflexive("bsp_groups", scnr_bsp_group),
    h3_reflexive("scenario_bsp_audibility", scnr_scenario_bsp_audibility),
    h3_reflexive("scenario_zoneset_groups", scnr_scenario_zoneset_group),
    h3_reflexive("bsp_atlas", scnr_bsp_atla),
    BytesRaw("unknown_1", SIZE=36, VISIBLE=False),
    h3_rawdata_ref("editor_scenario_data"),
    BytesRaw("unknown_2", SIZE=12, VISIBLE=False),
    h3_reflexive("object_names", scnr_object_name),
    h3_reflexive("scenery", scnr_scenery),
    h3_reflexive("scenery_palette", scnr_scenery_palette),
    h3_reflexive("bipeds", scnr_biped),
    h3_reflexive("biped_palette", scnr_biped_palette),
    h3_reflexive("vehicles", scnr_vehicle),
    h3_reflexive("vehicle_palette", scnr_vehicle_palette),
    h3_reflexive("equipment", scnr_equipment),
    h3_reflexive("equipment_palette", scnr_equipment_palette),
    h3_reflexive("weapons", scnr_weapon),
    h3_reflexive("weapon_palette", scnr_weapon_palette),
    h3_reflexive("device_groups", scnr_device_group),
    h3_reflexive("machines", scnr_machine),
    h3_reflexive("machine_palette", scnr_machine_palette),
    h3_reflexive("terminals", scnr_terminal),
    h3_reflexive("terminal_palette", scnr_terminal_palette),
    h3_reflexive("controls", scnr_control),
    h3_reflexive("control_palette", scnr_control_palette),
    h3_reflexive("sound_scenery", scnr_sound_scenery),
    h3_reflexive("sound_scenery_palette", scnr_sound_scenery_palette),
    h3_reflexive("giants", scnr_giant),
    h3_reflexive("giant_palette", scnr_giant_palette),
    h3_reflexive("effect_scenery", scnr_effect_scenery),
    h3_reflexive("effect_scenery_palette", scnr_effect_scenery_palette),
    h3_reflexive("light_volumes", scnr_light_volume),
    h3_reflexive("light_volumes_palette", scnr_light_volumes_palette),
    h3_reflexive("sandbox_vehicles", scnr_sandbox_vehicle),
    h3_reflexive("sandbox_weapons", scnr_sandbox_weapon),
    h3_reflexive("sandbox_equipment", scnr_sandbox_equipment),
    h3_reflexive("sandbox_scenery", scnr_sandbox_scenery),
    h3_reflexive("sandbox_teleporters", scnr_sandbox_teleporter),
    h3_reflexive("sandbox_goal_objects", scnr_sandbox_goal_object),
    h3_reflexive("sandbox_spawning", scnr_sandbox_spawning),
    h3_reflexive("soft_ceilings", scnr_soft_ceiling),
    h3_reflexive("player_starting_profile", scnr_player_starting_profile),
    h3_reflexive("player_starting_locations", scnr_player_starting_location),
    h3_reflexive("trigger_volumes", scnr_trigger_volume),
    BytesRaw("unknown_3", SIZE=12, VISIBLE=False),
    h3_reflexive("zoneset_switch_trigger_volumes", scnr_zoneset_switch_trigger_volume),
    h3_reflexive("multiplayer_constants_override", scnr_multiplayer_constants_override),
    h3_reflexive("unknown_4", scnr_unknown_4),
    h3_reflexive("unknown_5", scnr_unknown_5),
    h3_reflexive("unknown_6", scnr_unknown_6),
    h3_reflexive("unknown_7", scnr_unknown_7),
    BytesRaw("unknown_8", SIZE=144, VISIBLE=False),
    h3_reflexive("decals", scnr_decal),
    h3_reflexive("decal_palette", scnr_decal_palette),
    BytesRaw("unknown_9", SIZE=12, VISIBLE=False),
    h3_reflexive("style_palette", scnr_style_palette),
    h3_reflexive("squad_groups", scnr_squad_group),
    h3_reflexive("squads", scnr_squad),
    h3_reflexive("zones", scnr_zone),
    BytesRaw("unknown_10", SIZE=12, VISIBLE=False),
    h3_reflexive("character_palette", scnr_character_palette),
    BytesRaw("unknown_11", SIZE=12, VISIBLE=False),
    h3_reflexive("ai_pathfinding_data", scnr_ai_pathfinding_data),
    BytesRaw("unknown_12", SIZE=12, VISIBLE=False),
    h3_rawdata_ref("script_strings"),
    h3_reflexive("scripts", scnr_script),
    h3_reflexive("globals", scnr_global),
    h3_reflexive("script_references", scnr_script_reference),
    BytesRaw("unknown_13", SIZE=12, VISIBLE=False),
    h3_reflexive("scripting_data", scnr_scripting_data),
    h3_reflexive("cutscene_flags", scnr_cutscene_flag),
    h3_reflexive("cutscene_camera_points", scnr_cutscene_camera_point),
    h3_reflexive("cutscene_titles", scnr_cutscene_title),
    h3_dependency("custom_object_name_strings"),
    h3_dependency("chapter_title_strings"),
    h3_reflexive("scenario_resources", scnr_scenario_resource),
    h3_reflexive("unit_seats_mapping", scnr_unit_seats_mapping),
    h3_reflexive("scenario_kill_triggers", scnr_scenario_kill_trigger),
    h3_reflexive("scenario_safe_triggers", scnr_scenario_safe_trigger),
    h3_reflexive("script_expressions", scnr_script_expression),
    BytesRaw("unknown_14", SIZE=12, VISIBLE=False),
    h3_reflexive("ai_triggers", scnr_ai_trigger),
    h3_reflexive("background_sound_environment_palette", scnr_background_sound_environment_palette),
    BytesRaw("unknown_15", SIZE=24, VISIBLE=False),
    h3_reflexive("unknown_16", scnr_unknown_16),
    h3_reflexive("fog", scnr_fog),
    h3_reflexive("camera_effects", scnr_camera_effect),
    BytesRaw("unknown_17", SIZE=36, VISIBLE=False),
    h3_reflexive("scenario_cluster_data", scnr_scenario_cluster_data),
    BytesRaw("unknown_18", SIZE=12, VISIBLE=False),
    Array("object_salts_array", SUB_STRUCT=SInt32("object_salts"), SIZE=32, VISIBLE=False),
    h3_reflexive("spawn_data", scnr_spawn_data),
    h3_dependency("sound_effects_collection"),
    h3_reflexive("crates", scnr_crate),
    h3_reflexive("crate_palette", scnr_crate_palette),
    h3_reflexive("flock_palette", scnr_flock_palette),
    h3_reflexive("flocks", scnr_flock),
    h3_dependency("subtitle_strings"),
    BytesRaw("unknown_19", SIZE=12, VISIBLE=False),
    h3_reflexive("creature_palette", scnr_creature_palette),
    h3_reflexive("editor_folders", scnr_editor_folder),
    h3_dependency("territory_location_name_strings"),
    BytesRaw("unknown_20", SIZE=8, VISIBLE=False),
    h3_reflexive("mission_dialogue", scnr_mission_dialogue),
    h3_dependency("objective_strings"),
    h3_reflexive("interpolators", scnr_interpolator),
    BytesRaw("unknown_21", SIZE=24, VISIBLE=False),
    h3_reflexive("simulation_definition_table", scnr_simulation_definition_table),
    h3_dependency("default_camera_fx"),
    h3_dependency("default_screen_fx"),
    h3_dependency("sky_parameters"),
    h3_dependency("global_lighing"),
    h3_dependency("lightmap"),
    h3_dependency("performance_throttles"),
    h3_reflexive("unknown_22", scnr_unknown_22),
    h3_reflexive("ai_objectives", scnr_ai_objective),
    h3_reflexive("designer_zonesets", scnr_designer_zoneset),
    h3_reflexive("unknown_23", scnr_unknown_23),
    BytesRaw("unknown_24", SIZE=12, VISIBLE=False),
    h3_reflexive("cinematics", scnr_cinematic),
    h3_reflexive("cinematic_lighting", scnr_cinematic_lighting),
    BytesRaw("unknown_25", SIZE=12, VISIBLE=False),
    h3_reflexive("scenario_metagame", scnr_scenario_metagame),
    h3_reflexive("unknown_26", scnr_unknown_26),
    h3_reflexive("unknown_27", scnr_unknown_27),
    h3_reflexive("cortana_effects", scnr_cortana_effect),
    h3_reflexive("lightmap_airprobes", scnr_lightmap_airprobe),
    BytesRaw("unknown_28", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=1976
    )


def get():
    return scnr_def

scnr_def = TagDef("scnr",
    h3_blam_header('scnr'),
    scnr_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["scnr"], endian=">", tag_cls=H3Tag
    )