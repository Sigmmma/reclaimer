from reclaimer.common_descs import *
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

scnr_light_volume_type_1 = (
    "sphere",
    "projective",
    )

scnr_machine_pathfinding_policy = (
    "tag_default",
    "cut_out",
    "sectors",
    "discs",
    "none",
    )

scnr_map_type = (
    "single_player",
    "multiplayer",
    "main_menu",
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

scnr_scenery_shape = (
    "none",
    "sphere",
    "cylinder",
    "box",
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

scnr_scenery_type = (
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
    "spawn_in_passenger",
    "spawn_in_gunner",
    "spawn_in_driver",
    "spawn_out_of_vehicle",
    ("spawn_vehicle_only", 6),
    "spawn_in_passenger_1",
    )

scnr_squad_team = (
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


scnr_structure_bsp = Struct("structure_bsps",
    dependency("structure_bsp"),
    dependency("design"),
    dependency("lighting"),
    SInt32("unknown"),
    Float("unknown_1"),
    Pad(8),
    SInt16("unknown_3"),
    SInt16("unknown_4"),
    SInt16("unknown_5"),
    SInt16("unknown_6"),
    dependency("cubemap"),
    dependency("wind"),
    SInt32("unknown_7"),
    ENDIAN=">", SIZE=108
    )


scnr_sky_reference = Struct("sky_references",
    dependency("sky_object"),
    SInt16("name_index"),
    Bool16("active_bsps",
        "bsp_0",
        "bsp_1",
        "bsp_2",
        "bsp_3",
        "bsp_4",
        "bsp_5",
        "bsp_6",
        "bsp_7",
        "bsp_8",
        "bsp_9",
        "bsp_10",
        "bsp_11",
        "bsp_12",
        "bsp_13",
        "bsp_14",
        "bsp_15",
        ),
    ENDIAN=">", SIZE=20
    )


scnr_bsp_group_bsp_checksum = Struct("bsp_checksums",
    SInt32("structure_checksum"),
    ENDIAN=">", SIZE=4
    )


scnr_bsp_group_bsp_cluster_bsp_unknown = Struct("unknown",
    Bool32("allow",
        ("effects", 1 << 5),
        ("firing_effects", 1 << 16),
        ("decals", 1 << 24),
        ),
    ENDIAN=">", SIZE=4
    )


scnr_bsp_group_bsp_cluster_bsp = Struct("bsps",
    reflexive("unknown", scnr_bsp_group_bsp_cluster_bsp_unknown),
    ENDIAN=">", SIZE=12
    )


scnr_bsp_group_bsp_cluster = Struct("clusters",
    reflexive("bsps", scnr_bsp_group_bsp_cluster_bsp),
    ENDIAN=">", SIZE=12
    )


scnr_bsp_group_bsp_clusters_1_bsp_unknown = Struct("unknown",
    Bool32("allow",
        ("effects", 1 << 5),
        ("firing_effects", 1 << 16),
        ("decals", 1 << 24),
        ),
    ENDIAN=">", SIZE=4
    )


scnr_bsp_group_bsp_clusters_1_bsp = Struct("bsps",
    reflexive("unknown", scnr_bsp_group_bsp_clusters_1_bsp_unknown),
    ENDIAN=">", SIZE=12
    )


scnr_bsp_group_bsp_clusters_1 = Struct("clusters_1",
    reflexive("bsps", scnr_bsp_group_bsp_clusters_1_bsp),
    ENDIAN=">", SIZE=12
    )


scnr_bsp_group_bsp_cluster_skie = Struct("cluster_skies",
    SInt8("sky_index"),
    ENDIAN=">", SIZE=1
    )


scnr_bsp_group_bsp_cluster_visible_skie = Struct("cluster_visible_skies",
    SInt8("sky_index"),
    ENDIAN=">", SIZE=1
    )


scnr_bsp_group_bsp_unknown_1 = Struct("unknown_1",
    Pad(4),
    ENDIAN=">", SIZE=4
    )


scnr_bsp_group_bsp_clusters_2_unknown = Struct("unknown",
    SInt8("unknown"),
    ENDIAN=">", SIZE=1
    )


scnr_bsp_group_bsp_clusters_2 = Struct("clusters_2",
    reflexive("unknown", scnr_bsp_group_bsp_clusters_2_unknown),
    ENDIAN=">", SIZE=12
    )


scnr_bsp_group_bsp = Struct("bsps",
    reflexive("clusters", scnr_bsp_group_bsp_cluster),
    reflexive("clusters_1", scnr_bsp_group_bsp_clusters_1),
    reflexive("cluster_skies", scnr_bsp_group_bsp_cluster_skie),
    reflexive("cluster_visible_skies", scnr_bsp_group_bsp_cluster_visible_skie),
    Pad(12),
    reflexive("unknown_1", scnr_bsp_group_bsp_unknown_1),
    reflexive("clusters_2", scnr_bsp_group_bsp_clusters_2),
    ENDIAN=">", SIZE=84
    )


scnr_bsp_group_bsps_1_unknown = Struct("unknown",
    SInt16("unknown"),
    SInt16("unknown_1"),
    SInt32("unknown_2"),
    SInt16("unknown_3"),
    SInt16("unknown_4"),
    ENDIAN=">", SIZE=12
    )


scnr_bsp_group_bsps_1_unknown_1 = Struct("unknown_1",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


scnr_bsp_group_bsps_1 = Struct("bsps_1",
    reflexive("unknown", scnr_bsp_group_bsps_1_unknown),
    reflexive("unknown_1", scnr_bsp_group_bsps_1_unknown_1),
    ENDIAN=">", SIZE=24
    )


scnr_bsp_group = Struct("bsp_groups",
    Bool32("included_bsps",
        "bsp_0",
        "bsp_1",
        "bsp_2",
        "bsp_3",
        "bsp_4",
        "bsp_5",
        "bsp_6",
        "bsp_7",
        "bsp_8",
        "bsp_9",
        "bsp_10",
        "bsp_11",
        "bsp_12",
        "bsp_13",
        "bsp_14",
        "bsp_15",
        "bsp_16",
        "bsp_17",
        "bsp_18",
        "bsp_19",
        "bsp_20",
        "bsp_21",
        "bsp_22",
        "bsp_23",
        "bsp_24",
        "bsp_25",
        "bsp_26",
        "bsp_27",
        "bsp_28",
        "bsp_29",
        "bsp_30",
        "bsp_31",
        ),
    SInt32("unknown"),
    reflexive("bsp_checksums", scnr_bsp_group_bsp_checksum),
    reflexive("bsps", scnr_bsp_group_bsp),
    reflexive("bsps_1", scnr_bsp_group_bsps_1),
    ENDIAN=">", SIZE=44
    )


scnr_scenario_bsp_audibility_encoded_door_pa = Struct("encoded_door_pas",
    SInt32("unknown"),
    ENDIAN=">", SIZE=4
    )


scnr_scenario_bsp_audibility_cluster_door_portal_encoded_pa = Struct("cluster_door_portal_encoded_pas",
    SInt32("unknown"),
    ENDIAN=">", SIZE=4
    )


scnr_scenario_bsp_audibility_ai_deafening_pa = Struct("ai_deafening_pas",
    SInt32("unknown"),
    ENDIAN=">", SIZE=4
    )


scnr_scenario_bsp_audibility_cluster_distance = Struct("cluster_distances",
    SInt8("unknown"),
    ENDIAN=">", SIZE=1
    )


scnr_scenario_bsp_audibility_bsp = Struct("bsps",
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
    Float("cluster_distance_bounds_min"),
    Float("cluster_distance_bounds_max"),
    reflexive("encoded_door_pas", scnr_scenario_bsp_audibility_encoded_door_pa),
    reflexive("cluster_door_portal_encoded_pas", scnr_scenario_bsp_audibility_cluster_door_portal_encoded_pa),
    reflexive("ai_deafening_pas", scnr_scenario_bsp_audibility_ai_deafening_pa),
    reflexive("cluster_distances", scnr_scenario_bsp_audibility_cluster_distance),
    reflexive("bsps", scnr_scenario_bsp_audibility_bsp),
    reflexive("bsp_cluster_list", scnr_scenario_bsp_audibility_bsp_cluster_list),
    reflexive("cluster_mapping", scnr_scenario_bsp_audibility_cluster_mapping),
    ENDIAN=">", SIZE=100
    )


scnr_scenario_zoneset_group = Struct("scenario_zoneset_groups",
    string_id_meta("name"),
    SInt32("bsp_group_index"),
    SInt32("import_loaded_bsps"),
    Bool32("loaded_bsps",
        "bsp_0",
        "bsp_1",
        "bsp_2",
        "bsp_3",
        "bsp_4",
        "bsp_5",
        "bsp_6",
        "bsp_7",
        "bsp_8",
        "bsp_9",
        "bsp_10",
        "bsp_11",
        "bsp_12",
        "bsp_13",
        "bsp_14",
        "bsp_15",
        "bsp_16",
        "bsp_17",
        "bsp_18",
        "bsp_19",
        "bsp_20",
        "bsp_21",
        "bsp_22",
        "bsp_23",
        "bsp_24",
        "bsp_25",
        "bsp_26",
        "bsp_27",
        "bsp_28",
        "bsp_29",
        "bsp_30",
        "bsp_31",
        ),
    Bool32("loaded_designer_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        "set_16",
        "set_17",
        "set_18",
        "set_19",
        "set_20",
        "set_21",
        "set_22",
        "set_23",
        "set_24",
        "set_25",
        "set_26",
        "set_27",
        "set_28",
        "set_29",
        "set_30",
        "set_31",
        ),
    Bool32("unloaded_designer_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        "set_16",
        "set_17",
        "set_18",
        "set_19",
        "set_20",
        "set_21",
        "set_22",
        "set_23",
        "set_24",
        "set_25",
        "set_26",
        "set_27",
        "set_28",
        "set_29",
        "set_30",
        "set_31",
        ),
    Bool32("loaded_cinematic_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        "set_16",
        "set_17",
        "set_18",
        "set_19",
        "set_20",
        "set_21",
        "set_22",
        "set_23",
        "set_24",
        "set_25",
        "set_26",
        "set_27",
        "set_28",
        "set_29",
        "set_30",
        "set_31",
        ),
    SInt32("bsp_atlas_index"),
    SInt32("scenario_bsp_audibility_index"),
    ENDIAN=">", SIZE=36
    )


scnr_bsp_atla = Struct("bsp_atlas",
    string_id_meta("name"),
    Bool32("bsp",
        "bsp_0",
        "bsp_1",
        "bsp_2",
        "bsp_3",
        "bsp_4",
        "bsp_5",
        "bsp_6",
        "bsp_7",
        "bsp_8",
        "bsp_9",
        "bsp_10",
        "bsp_11",
        "bsp_12",
        "bsp_13",
        "bsp_14",
        "bsp_15",
        "bsp_16",
        "bsp_17",
        "bsp_18",
        "bsp_19",
        "bsp_20",
        "bsp_21",
        "bsp_22",
        "bsp_23",
        "bsp_24",
        "bsp_25",
        "bsp_26",
        "bsp_27",
        "bsp_28",
        "bsp_29",
        "bsp_30",
        "bsp_31",
        ),
    Bool32("connected_bsps",
        "bsp_0",
        "bsp_1",
        "bsp_2",
        "bsp_3",
        "bsp_4",
        "bsp_5",
        "bsp_6",
        "bsp_7",
        "bsp_8",
        "bsp_9",
        "bsp_10",
        "bsp_11",
        "bsp_12",
        "bsp_13",
        "bsp_14",
        "bsp_15",
        "bsp_16",
        "bsp_17",
        "bsp_18",
        "bsp_19",
        "bsp_20",
        "bsp_21",
        "bsp_22",
        "bsp_23",
        "bsp_24",
        "bsp_25",
        "bsp_26",
        "bsp_27",
        "bsp_28",
        "bsp_29",
        "bsp_30",
        "bsp_31",
        ),
    ENDIAN=">", SIZE=12
    )


scnr_object_name = Struct("object_names",
    StrLatin1("name", SIZE=32),
    SEnum16("type", *scnr_object_name_type),
    SInt16("placement_index"),
    ENDIAN=">", SIZE=36
    )


scnr_scenery_node_positioning_node_flags_readable = Struct("node_flags_readable",
    Bool8("flags",
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
    SInt16("rotation_x"),
    SInt16("rotation_y"),
    SInt16("rotation_z"),
    SInt16("rotation_w"),
    ENDIAN=">", SIZE=8
    )


scnr_scenery_node_positioning = Struct("node_positioning",
    SInt16("node_count"),
    SInt16("unknown"),
    reflexive("node_flags_readable", scnr_scenery_node_positioning_node_flags_readable),
    reflexive("orientations_readable", scnr_scenery_node_positioning_orientations_readable),
    ENDIAN=">", SIZE=28
    )


scnr_scenery_pathfinding_reference = Struct("pathfinding_references",
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
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    float_rad("rotation_i"),
    float_rad("rotation_j"),
    float_rad("rotation_k"),
    Float("scale"),
    reflexive("node_positioning", scnr_scenery_node_positioning),
    SInt16("unknown"),
    Bool16("old_manual_bsp_flags_now_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        ),
    string_id_meta("unique_name"),
    UInt16("unique_id_salt"),
    UInt16("unique_id_index"),
    SInt16("origin_bsp_index"),
    SEnum8("type", *scnr_scenery_type),
    SEnum8("source", *scnr_scenery_source),
    SEnum8("bsp_policy", *scnr_scenery_bsp_policy),
    SInt8("unknown_1"),
    SInt16("editor_folder_index"),
    SInt16("unknown_2"),
    SInt16("parent_name_index"),
    string_id_meta("child_name"),
    string_id_meta("unknown_3"),
    Bool16("allowed_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        ),
    SInt16("unknown_4"),
    string_id_meta("variant"),
    Bool8("active_change_colors",
        "primary",
        "secondary",
        "tertiary",
        "quaternary",
        ),
    SInt8("unknown_5"),
    SInt8("unknown_6"),
    SInt8("unknown_7"),
    color_argb_uint32("primary_color"),
    color_argb_uint32("secondary_color"),
    color_argb_uint32("tertiary_color"),
    color_argb_uint32("quaternary_color"),
    SEnum16("pathfinding_policy", *scnr_scenery_pathfinding_policy),
    SEnum16("lightmapping_policy", *scnr_scenery_lightmapping_policy),
    reflexive("pathfinding_references", scnr_scenery_pathfinding_reference),
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
    SInt8("runtime_minimum"),
    SInt8("runtime_maximum"),
    Bool8("multiplayer_flags",
        "is_unique_object",
        "not_placed_at_start",
        ),
    SInt16("spawn_time"),
    SInt16("abandon_time"),
    SInt8("unknown_10"),
    SEnum8("shape", *scnr_scenery_shape),
    SInt8("teleporter_channel"),
    SInt8("unknown_11"),
    SInt16("unknown_12"),
    SInt16("attached_name_index"),
    Pad(8),
    Float("width_radius"),
    Float("depth"),
    Float("top"),
    Float("bottom"),
    Pad(4),
    ENDIAN=">", SIZE=180
    )


scnr_scenery_palette = Struct("scenery_palette",
    dependency("scenery"),
    Pad(32),
    ENDIAN=">", SIZE=48
    )


scnr_biped_node_positioning_node_flags_readable = Struct("node_flags_readable",
    Bool8("flags",
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
    SInt16("rotation_x"),
    SInt16("rotation_y"),
    SInt16("rotation_z"),
    SInt16("rotation_w"),
    ENDIAN=">", SIZE=8
    )


scnr_biped_node_positioning = Struct("node_positioning",
    SInt16("node_count"),
    SInt16("unknown"),
    reflexive("node_flags_readable", scnr_biped_node_positioning_node_flags_readable),
    reflexive("orientations_readable", scnr_biped_node_positioning_orientations_readable),
    ENDIAN=">", SIZE=28
    )


scnr_biped = Struct("bipeds",
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
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    float_rad("rotation_i"),
    float_rad("rotation_j"),
    float_rad("rotation_k"),
    Float("scale"),
    reflexive("node_positioning", scnr_biped_node_positioning),
    SInt16("unknown"),
    Bool16("old_manual_bsp_flags_now_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        ),
    string_id_meta("unique_name"),
    UInt16("unique_id_salt"),
    UInt16("unique_id_index"),
    SInt16("origin_bsp_index"),
    SEnum8("type", *scnr_scenery_type),
    SEnum8("source", *scnr_scenery_source),
    SEnum8("bsp_policy", *scnr_scenery_bsp_policy),
    SInt8("unknown_1"),
    SInt16("editor_folder_index"),
    SInt16("unknown_2"),
    SInt16("parent_name_index"),
    string_id_meta("child_name"),
    string_id_meta("unknown_3"),
    Bool16("allowed_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        ),
    SInt16("unknown_4"),
    string_id_meta("variant"),
    Bool8("active_change_colors",
        "primary",
        "secondary",
        "tertiary",
        "quaternary",
        ),
    SInt8("unknown_5"),
    SInt8("unknown_6"),
    SInt8("unknown_7"),
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
    dependency("biped"),
    Pad(32),
    ENDIAN=">", SIZE=48
    )


scnr_vehicle_node_positioning_node_flags_readable = Struct("node_flags_readable",
    Bool8("flags",
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
    SInt16("rotation_x"),
    SInt16("rotation_y"),
    SInt16("rotation_z"),
    SInt16("rotation_w"),
    ENDIAN=">", SIZE=8
    )


scnr_vehicle_node_positioning = Struct("node_positioning",
    SInt16("node_count"),
    SInt16("unknown"),
    reflexive("node_flags_readable", scnr_vehicle_node_positioning_node_flags_readable),
    reflexive("orientations_readable", scnr_vehicle_node_positioning_orientations_readable),
    ENDIAN=">", SIZE=28
    )


scnr_vehicle = Struct("vehicles",
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
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    float_rad("rotation_i"),
    float_rad("rotation_j"),
    float_rad("rotation_k"),
    Float("scale"),
    reflexive("node_positioning", scnr_vehicle_node_positioning),
    SInt16("unknown"),
    Bool16("old_manual_bsp_flags_now_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        ),
    string_id_meta("unique_name"),
    UInt16("unique_id_salt"),
    UInt16("unique_id_index"),
    SInt16("origin_bsp_index"),
    SEnum8("type", *scnr_scenery_type),
    SEnum8("source", *scnr_scenery_source),
    SEnum8("bsp_policy", *scnr_scenery_bsp_policy),
    SInt8("unknown_1"),
    SInt16("editor_folder_index"),
    SInt16("unknown_2"),
    SInt16("parent_name_index"),
    string_id_meta("child_name"),
    string_id_meta("unknown_3"),
    Bool16("allowed_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        ),
    SInt16("unknown_4"),
    string_id_meta("variant"),
    Bool8("active_change_colors",
        "primary",
        "secondary",
        "tertiary",
        "quaternary",
        ),
    SInt8("unknown_5"),
    SInt8("unknown_6"),
    SInt8("unknown_7"),
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
    SInt8("runtime_minimum"),
    SInt8("runtime_maximum"),
    Bool8("multiplayer_flags",
        "is_unique_object",
        "not_placed_at_start",
        ),
    SInt16("spawn_time"),
    SInt16("abandon_time"),
    SInt8("unknown_8"),
    SEnum8("shape", *scnr_scenery_shape),
    SInt8("teleporter_channel"),
    SInt8("unknown_9"),
    SInt16("unknown_10"),
    SInt16("attached_name_index"),
    Pad(8),
    Float("width_radius"),
    Float("depth"),
    Float("top"),
    Float("bottom"),
    Pad(4),
    ENDIAN=">", SIZE=168
    )


scnr_vehicle_palette = Struct("vehicle_palette",
    dependency("vehicle"),
    Pad(32),
    ENDIAN=">", SIZE=48
    )


scnr_equipment_node_positioning_node_flags_readable = Struct("node_flags_readable",
    Bool8("flags",
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
    SInt16("rotation_x"),
    SInt16("rotation_y"),
    SInt16("rotation_z"),
    SInt16("rotation_w"),
    ENDIAN=">", SIZE=8
    )


scnr_equipment_node_positioning = Struct("node_positioning",
    SInt16("node_count"),
    SInt16("unknown"),
    reflexive("node_flags_readable", scnr_equipment_node_positioning_node_flags_readable),
    reflexive("orientations_readable", scnr_equipment_node_positioning_orientations_readable),
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
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    float_rad("rotation_i"),
    float_rad("rotation_j"),
    float_rad("rotation_k"),
    Float("scale"),
    reflexive("node_positioning", scnr_equipment_node_positioning),
    SInt16("unknown"),
    Bool16("old_manual_bsp_flags_now_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        ),
    string_id_meta("unique_name"),
    UInt16("unique_id_salt"),
    UInt16("unique_id_index"),
    SInt16("origin_bsp_index"),
    SEnum8("type", *scnr_scenery_type),
    SEnum8("source", *scnr_scenery_source),
    SEnum8("bsp_policy", *scnr_scenery_bsp_policy),
    SInt8("unknown_1"),
    SInt16("editor_folder_index"),
    SInt16("unknown_2"),
    SInt16("parent_name_index"),
    string_id_meta("child_name"),
    string_id_meta("unknown_3"),
    Bool16("allowed_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        ),
    SInt16("unknown_4"),
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
    SInt8("runtime_minimum"),
    SInt8("runtime_maximum"),
    Bool8("multiplayer_flags",
        "is_unique_object",
        "not_placed_at_start",
        ),
    SInt16("spawn_time"),
    SInt16("abandon_time"),
    SInt8("unknown_5"),
    SEnum8("shape", *scnr_scenery_shape),
    SInt8("teleporter_channel"),
    SInt8("unknown_6"),
    SInt16("unknown_7"),
    SInt16("attached_name_index"),
    Pad(8),
    Float("width_radius"),
    Float("depth"),
    Float("top"),
    Float("bottom"),
    Pad(4),
    ENDIAN=">", SIZE=140
    )


scnr_equipment_palette = Struct("equipment_palette",
    dependency("equipment"),
    Pad(32),
    ENDIAN=">", SIZE=48
    )


scnr_weapon_node_positioning_node_flags_readable = Struct("node_flags_readable",
    Bool8("flags",
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
    SInt16("rotation_x"),
    SInt16("rotation_y"),
    SInt16("rotation_z"),
    SInt16("rotation_w"),
    ENDIAN=">", SIZE=8
    )


scnr_weapon_node_positioning = Struct("node_positioning",
    SInt16("node_count"),
    SInt16("unknown"),
    reflexive("node_flags_readable", scnr_weapon_node_positioning_node_flags_readable),
    reflexive("orientations_readable", scnr_weapon_node_positioning_orientations_readable),
    ENDIAN=">", SIZE=28
    )


scnr_weapon = Struct("weapons",
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
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    float_rad("rotation_i"),
    float_rad("rotation_j"),
    float_rad("rotation_k"),
    Float("scale"),
    reflexive("node_positioning", scnr_weapon_node_positioning),
    SInt16("unknown"),
    Bool16("old_manual_bsp_flags_now_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        ),
    string_id_meta("unique_name"),
    UInt16("unique_id_salt"),
    UInt16("unique_id_index"),
    SInt16("origin_bsp_index"),
    SEnum8("type", *scnr_scenery_type),
    SEnum8("source", *scnr_scenery_source),
    SEnum8("bsp_policy", *scnr_scenery_bsp_policy),
    SInt8("unknown_1"),
    SInt16("editor_folder_index"),
    SInt16("unknown_2"),
    SInt16("parent_name_index"),
    string_id_meta("child_name"),
    string_id_meta("unknown_3"),
    Bool16("allowed_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        ),
    SInt16("unknown_4"),
    string_id_meta("variant"),
    Bool8("active_change_colors",
        "primary",
        "secondary",
        "tertiary",
        "quaternary",
        ),
    SInt8("unknown_5"),
    SInt8("unknown_6"),
    SInt8("unknown_7"),
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
    SInt8("runtime_minimum"),
    SInt8("runtime_maximum"),
    Bool8("multiplayer_flags",
        "is_unique_object",
        "not_placed_at_start",
        ),
    SInt16("spawn_time"),
    SInt16("abandon_time"),
    SInt8("unknown_8"),
    SEnum8("shape", *scnr_scenery_shape),
    SInt8("teleporter_channel"),
    SInt8("unknown_9"),
    SInt16("unknown_10"),
    SInt16("attached_name_index"),
    Pad(8),
    Float("width_radius"),
    Float("depth"),
    Float("top"),
    Float("bottom"),
    Pad(4),
    ENDIAN=">", SIZE=168
    )


scnr_weapon_palette = Struct("weapon_palette",
    dependency("weapon"),
    Pad(32),
    ENDIAN=">", SIZE=48
    )


scnr_device_group = Struct("device_groups",
    StrLatin1("name", SIZE=32),
    Float("initial_value"),
    Bool32("flags",
        "only_use_once",
        ),
    ENDIAN=">", SIZE=40
    )


scnr_machine_node_positioning_node_flags_readable = Struct("node_flags_readable",
    Bool8("flags",
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
    SInt16("rotation_x"),
    SInt16("rotation_y"),
    SInt16("rotation_z"),
    SInt16("rotation_w"),
    ENDIAN=">", SIZE=8
    )


scnr_machine_node_positioning = Struct("node_positioning",
    SInt16("node_count"),
    SInt16("unknown"),
    reflexive("node_flags_readable", scnr_machine_node_positioning_node_flags_readable),
    reflexive("orientations_readable", scnr_machine_node_positioning_orientations_readable),
    ENDIAN=">", SIZE=28
    )


scnr_machine_pathfinding_reference = Struct("pathfinding_references",
    SInt16("bsp_index"),
    SInt16("pathfinding_object_index"),
    ENDIAN=">", SIZE=4
    )


scnr_machine = Struct("machines",
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
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    float_rad("rotation_i"),
    float_rad("rotation_j"),
    float_rad("rotation_k"),
    Float("scale"),
    reflexive("node_positioning", scnr_machine_node_positioning),
    SInt16("unknown"),
    Bool16("old_manual_bsp_flags_now_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        ),
    string_id_meta("unique_name"),
    UInt16("unique_id_salt"),
    UInt16("unique_id_index"),
    SInt16("origin_bsp_index"),
    SEnum8("type", *scnr_scenery_type),
    SEnum8("source", *scnr_scenery_source),
    SEnum8("bsp_policy", *scnr_scenery_bsp_policy),
    SInt8("unknown_1"),
    SInt16("editor_folder_index"),
    SInt16("unknown_2"),
    SInt16("parent_name_index"),
    string_id_meta("child_name"),
    string_id_meta("unknown_3"),
    Bool16("allowed_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        ),
    SInt16("unknown_4"),
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
    reflexive("pathfinding_references", scnr_machine_pathfinding_reference),
    SEnum16("pathfinding_policy", *scnr_machine_pathfinding_policy),
    SInt16("unknown_5"),
    ENDIAN=">", SIZE=112
    )


scnr_machine_palette = Struct("machine_palette",
    dependency("machine"),
    Pad(32),
    ENDIAN=">", SIZE=48
    )


scnr_terminal_node_positioning_node_flags_readable = Struct("node_flags_readable",
    Bool8("flags",
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
    SInt16("rotation_x"),
    SInt16("rotation_y"),
    SInt16("rotation_z"),
    SInt16("rotation_w"),
    ENDIAN=">", SIZE=8
    )


scnr_terminal_node_positioning = Struct("node_positioning",
    SInt16("node_count"),
    SInt16("unknown"),
    reflexive("node_flags_readable", scnr_terminal_node_positioning_node_flags_readable),
    reflexive("orientations_readable", scnr_terminal_node_positioning_orientations_readable),
    ENDIAN=">", SIZE=28
    )


scnr_terminal = Struct("terminals",
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
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    float_rad("rotation_i"),
    float_rad("rotation_j"),
    float_rad("rotation_k"),
    Float("scale"),
    reflexive("node_positioning", scnr_terminal_node_positioning),
    SInt16("unknown"),
    Bool16("old_manual_bsp_flags_now_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        ),
    string_id_meta("unique_name"),
    UInt16("unique_id_salt"),
    UInt16("unique_id_index"),
    SInt16("origin_bsp_index"),
    SEnum8("type", *scnr_scenery_type),
    SEnum8("source", *scnr_scenery_source),
    SEnum8("bsp_policy", *scnr_scenery_bsp_policy),
    SInt8("unknown_1"),
    SInt16("editor_folder_index"),
    SInt16("unknown_2"),
    SInt16("parent_name_index"),
    string_id_meta("child_name"),
    string_id_meta("unknown_3"),
    Bool16("allowed_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        ),
    SInt16("unknown_4"),
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
    dependency("terminal"),
    Pad(32),
    ENDIAN=">", SIZE=48
    )


scnr_control_node_positioning_node_flags_readable = Struct("node_flags_readable",
    Bool8("flags",
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
    SInt16("rotation_x"),
    SInt16("rotation_y"),
    SInt16("rotation_z"),
    SInt16("rotation_w"),
    ENDIAN=">", SIZE=8
    )


scnr_control_node_positioning = Struct("node_positioning",
    SInt16("node_count"),
    SInt16("unknown"),
    reflexive("node_flags_readable", scnr_control_node_positioning_node_flags_readable),
    reflexive("orientations_readable", scnr_control_node_positioning_orientations_readable),
    ENDIAN=">", SIZE=28
    )


scnr_control = Struct("controls",
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
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    float_rad("rotation_i"),
    float_rad("rotation_j"),
    float_rad("rotation_k"),
    Float("scale"),
    reflexive("node_positioning", scnr_control_node_positioning),
    SInt16("unknown"),
    Bool16("old_manual_bsp_flags_now_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        ),
    string_id_meta("unique_name"),
    UInt16("unique_id_salt"),
    UInt16("unique_id_index"),
    SInt16("origin_bsp_index"),
    SEnum8("type", *scnr_scenery_type),
    SEnum8("source", *scnr_scenery_source),
    SEnum8("bsp_policy", *scnr_scenery_bsp_policy),
    SInt8("unknown_1"),
    SInt16("editor_folder_index"),
    SInt16("unknown_2"),
    SInt16("parent_name_index"),
    string_id_meta("child_name"),
    string_id_meta("unknown_3"),
    Bool16("allowed_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        ),
    SInt16("unknown_4"),
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
    dependency("control"),
    Pad(32),
    ENDIAN=">", SIZE=48
    )


scnr_sound_scenery_node_positioning_node_flags_readable = Struct("node_flags_readable",
    Bool8("flags",
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
    SInt16("rotation_x"),
    SInt16("rotation_y"),
    SInt16("rotation_z"),
    SInt16("rotation_w"),
    ENDIAN=">", SIZE=8
    )


scnr_sound_scenery_node_positioning = Struct("node_positioning",
    SInt16("node_count"),
    SInt16("unknown"),
    reflexive("node_flags_readable", scnr_sound_scenery_node_positioning_node_flags_readable),
    reflexive("orientations_readable", scnr_sound_scenery_node_positioning_orientations_readable),
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
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    float_rad("rotation_i"),
    float_rad("rotation_j"),
    float_rad("rotation_k"),
    Float("scale"),
    reflexive("node_positioning", scnr_sound_scenery_node_positioning),
    SInt16("unknown"),
    Bool16("old_manual_bsp_flags_now_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        ),
    string_id_meta("unique_name"),
    UInt16("unique_id_salt"),
    UInt16("unique_id_index"),
    SInt16("origin_bsp_index"),
    SEnum8("type", *scnr_scenery_type),
    SEnum8("source", *scnr_scenery_source),
    SEnum8("bsp_policy", *scnr_scenery_bsp_policy),
    SInt8("unknown_1"),
    SInt16("editor_folder_index"),
    SInt16("unknown_2"),
    SInt16("parent_name_index"),
    string_id_meta("child_name"),
    string_id_meta("unknown_3"),
    Bool16("allowed_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        ),
    SInt16("unknown_4"),
    SInt32("volume_type"),
    Float("height"),
    Float("override_distance_min"),
    Float("override_distance_max"),
    float_rad("override_cone_angle_min"),
    float_rad("override_cone_angle_max"),
    Float("override_outer_cone_gain"),
    ENDIAN=">", SIZE=112
    )


scnr_sound_scenery_palette = Struct("sound_scenery_palette",
    dependency("sound_scenery"),
    Pad(32),
    ENDIAN=">", SIZE=48
    )


scnr_giant_node_positioning_node_flags_readable = Struct("node_flags_readable",
    Bool8("flags",
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
    SInt16("rotation_x"),
    SInt16("rotation_y"),
    SInt16("rotation_z"),
    SInt16("rotation_w"),
    ENDIAN=">", SIZE=8
    )


scnr_giant_node_positioning = Struct("node_positioning",
    SInt16("node_count"),
    SInt16("unknown"),
    reflexive("node_flags_readable", scnr_giant_node_positioning_node_flags_readable),
    reflexive("orientations_readable", scnr_giant_node_positioning_orientations_readable),
    ENDIAN=">", SIZE=28
    )


scnr_giant_pathfinding_reference = Struct("pathfinding_references",
    SInt16("bsp_index"),
    SInt16("pathfinding_object_index"),
    ENDIAN=">", SIZE=4
    )


scnr_giant = Struct("giants",
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
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    float_rad("rotation_i"),
    float_rad("rotation_j"),
    float_rad("rotation_k"),
    Float("scale"),
    reflexive("node_positioning", scnr_giant_node_positioning),
    SInt16("unknown"),
    Bool16("old_manual_bsp_flags_now_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        ),
    string_id_meta("unique_name"),
    UInt16("unique_id_salt"),
    UInt16("unique_id_index"),
    SInt16("origin_bsp_index"),
    SEnum8("type", *scnr_scenery_type),
    SEnum8("source", *scnr_scenery_source),
    SEnum8("bsp_policy", *scnr_scenery_bsp_policy),
    SInt8("unknown_1"),
    SInt16("editor_folder_index"),
    SInt16("unknown_2"),
    SInt16("parent_name_index"),
    string_id_meta("child_name"),
    string_id_meta("unknown_3"),
    Bool16("allowed_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        ),
    SInt16("unknown_4"),
    string_id_meta("variant"),
    Bool8("active_change_colors",
        "primary",
        "secondary",
        "tertiary",
        "quaternary",
        ),
    SInt8("unknown_5"),
    SInt8("unknown_6"),
    SInt8("unknown_7"),
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
    SEnum16("unknown_8", *scnr_giant_unknown_8),
    SInt16("unknown_9"),
    reflexive("pathfinding_references", scnr_giant_pathfinding_reference),
    ENDIAN=">", SIZE=132
    )


scnr_giant_palette = Struct("giant_palette",
    dependency("giant"),
    Pad(32),
    ENDIAN=">", SIZE=48
    )


scnr_effect_scenery_node_positioning_node_flags_readable = Struct("node_flags_readable",
    Bool8("flags",
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
    SInt16("rotation_x"),
    SInt16("rotation_y"),
    SInt16("rotation_z"),
    SInt16("rotation_w"),
    ENDIAN=">", SIZE=8
    )


scnr_effect_scenery_node_positioning = Struct("node_positioning",
    SInt16("node_count"),
    SInt16("unknown"),
    reflexive("node_flags_readable", scnr_effect_scenery_node_positioning_node_flags_readable),
    reflexive("orientations_readable", scnr_effect_scenery_node_positioning_orientations_readable),
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
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    float_rad("rotation_i"),
    float_rad("rotation_j"),
    float_rad("rotation_k"),
    Float("scale"),
    reflexive("node_positioning", scnr_effect_scenery_node_positioning),
    SInt16("unknown"),
    Bool16("old_manual_bsp_flags_now_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        ),
    string_id_meta("unique_name"),
    UInt16("unique_id_salt"),
    UInt16("unique_id_index"),
    SInt16("origin_bsp_index"),
    SEnum8("type", *scnr_scenery_type),
    SEnum8("source", *scnr_scenery_source),
    SEnum8("bsp_policy", *scnr_scenery_bsp_policy),
    SInt8("unknown_1"),
    SInt16("editor_folder_index"),
    SInt16("unknown_2"),
    SInt16("parent_name_index"),
    string_id_meta("child_name"),
    string_id_meta("unknown_3"),
    Bool16("allowed_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        ),
    SInt16("unknown_4"),
    ENDIAN=">", SIZE=84
    )


scnr_effect_scenery_palette = Struct("effect_scenery_palette",
    dependency("effect_scenery"),
    Pad(32),
    ENDIAN=">", SIZE=48
    )


scnr_light_volume_node_positioning_node_flags_readable = Struct("node_flags_readable",
    Bool8("flags",
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
    SInt16("rotation_x"),
    SInt16("rotation_y"),
    SInt16("rotation_z"),
    SInt16("rotation_w"),
    ENDIAN=">", SIZE=8
    )


scnr_light_volume_node_positioning = Struct("node_positioning",
    SInt16("node_count"),
    SInt16("unknown"),
    reflexive("node_flags_readable", scnr_light_volume_node_positioning_node_flags_readable),
    reflexive("orientations_readable", scnr_light_volume_node_positioning_orientations_readable),
    ENDIAN=">", SIZE=28
    )


scnr_light_volume = Struct("light_volumes",
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
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    float_rad("rotation_i"),
    float_rad("rotation_j"),
    float_rad("rotation_k"),
    Float("scale"),
    reflexive("node_positioning", scnr_light_volume_node_positioning),
    SInt16("unknown"),
    Bool16("old_manual_bsp_flags_now_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        ),
    string_id_meta("unique_name"),
    UInt16("unique_id_salt"),
    UInt16("unique_id_index"),
    SInt16("origin_bsp_index"),
    SEnum8("type", *scnr_scenery_type),
    SEnum8("source", *scnr_scenery_source),
    SEnum8("bsp_policy", *scnr_scenery_bsp_policy),
    SInt8("unknown_1"),
    SInt16("editor_folder_index"),
    SInt16("unknown_2"),
    SInt16("parent_name_index"),
    string_id_meta("child_name"),
    string_id_meta("unknown_3"),
    Bool16("allowed_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        ),
    SInt16("unknown_4"),
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
    Bool16("lightmap_flags",
        ),
    Float("lightmap_half_life"),
    Float("lightmap_light_scale"),
    Float("x"),
    Float("y"),
    Float("z"),
    Float("width"),
    Float("height_scale"),
    float_rad("field_of_view"),
    Float("falloff_distance"),
    Float("cutoff_distance"),
    ENDIAN=">", SIZE=140
    )


scnr_light_volumes_palette = Struct("light_volumes_palette",
    dependency("light_volume"),
    Pad(32),
    ENDIAN=">", SIZE=48
    )


scnr_sandbox_vehicle = Struct("sandbox_vehicles",
    dependency("object"),
    string_id_meta("name"),
    SInt32("max_allowed"),
    Float("cost"),
    Pad(20),
    ENDIAN=">", SIZE=48
    )


scnr_sandbox_weapon = Struct("sandbox_weapons",
    dependency("object"),
    string_id_meta("name"),
    SInt32("max_allowed"),
    Float("cost"),
    Pad(20),
    ENDIAN=">", SIZE=48
    )


scnr_sandbox_equipment = Struct("sandbox_equipment",
    dependency("object"),
    string_id_meta("name"),
    SInt32("max_allowed"),
    Float("cost"),
    Pad(20),
    ENDIAN=">", SIZE=48
    )


scnr_sandbox_scenery = Struct("sandbox_scenery",
    dependency("object"),
    string_id_meta("name"),
    SInt32("max_allowed"),
    Float("cost"),
    Pad(20),
    ENDIAN=">", SIZE=48
    )


scnr_sandbox_teleporter = Struct("sandbox_teleporters",
    dependency("object"),
    string_id_meta("name"),
    SInt32("max_allowed"),
    Float("cost"),
    Pad(20),
    ENDIAN=">", SIZE=48
    )


scnr_sandbox_goal_object = Struct("sandbox_goal_objects",
    dependency("object"),
    string_id_meta("name"),
    SInt32("max_allowed"),
    Float("cost"),
    Pad(20),
    ENDIAN=">", SIZE=48
    )


scnr_sandbox_spawning = Struct("sandbox_spawning",
    dependency("object"),
    string_id_meta("name"),
    SInt32("max_allowed"),
    Float("cost"),
    Pad(20),
    ENDIAN=">", SIZE=48
    )


scnr_soft_ceiling = Struct("soft_ceilings",
    SInt16("type"),
    SInt16("unknown"),
    string_id_meta("name"),
    SInt16("unknown_1"),
    SInt16("unknown_2"),
    ENDIAN=">", SIZE=12
    )


scnr_player_starting_profile = Struct("player_starting_profile",
    StrLatin1("name", SIZE=32),
    Float("starting_health_damage"),
    Float("starting_shield_damage"),
    dependency("primary_weapon"),
    SInt16("rounds_loaded"),
    SInt16("rounds_total"),
    dependency("secondary_weapon"),
    SInt16("rounds_loaded_1"),
    SInt16("rounds_total_1"),
    UInt8("starting_frag_grenade_count"),
    UInt8("starting_plasma_grenade_count"),
    UInt8("starting_spike_grenade_count"),
    UInt8("starting_firebomb_grenade_count"),
    ENDIAN=">", SIZE=84
    )


scnr_player_starting_location = Struct("player_starting_locations",
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    float_rad("facing_y"),
    float_rad("facing_p"),
    SInt16("unknown"),
    SEnum16("campaign_player_type", *scnr_player_starting_location_campaign_player_type),
    ENDIAN=">", SIZE=24
    )


scnr_trigger_volume = Struct("trigger_volumes",
    string_id_meta("name"),
    SInt16("object_name"),
    SInt16("unknown"),
    string_id_meta("node_name"),
    Float("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    Float("unknown_4"),
    Float("unknown_5"),
    Float("unknown_6"),
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    Float("extents_x"),
    Float("extents_y"),
    Float("extents_z"),
    Pad(4),
    SInt16("kill_volume"),
    SInt16("editor_folder_index"),
    ENDIAN=">", SIZE=68
    )


scnr_zoneset_switch_trigger_volume = Struct("zoneset_switch_trigger_volumes",
    SInt16("unknown"),
    SInt16("included_zoneset_index"),
    SInt16("trigger_volume"),
    SInt16("sole_zoneset_index"),
    ENDIAN=">", SIZE=8
    )


scnr_multiplayer_constants_override = Struct("multiplayer_constants_override",
    Float("unknown"),
    Float("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    Float("unknown_4"),
    ENDIAN=">", SIZE=20
    )


scnr_unknown_4 = Struct("unknown_4",
    Pad(20),
    ENDIAN=">", SIZE=20
    )


scnr_unknown_5 = Struct("unknown_5",
    Pad(20),
    ENDIAN=">", SIZE=20
    )


scnr_unknown_6 = Struct("unknown_6",
    Pad(20),
    ENDIAN=">", SIZE=20
    )


scnr_unknown_7 = Struct("unknown_7",
    Pad(20),
    ENDIAN=">", SIZE=20
    )


scnr_decal = Struct("decals",
    SInt16("palette_index"),
    SInt8("yaw"),
    SInt8("pitch"),
    Float("i"),
    Float("j"),
    Float("k"),
    Float("w"),
    Float("x"),
    Float("y"),
    Float("z"),
    Float("scale"),
    ENDIAN=">", SIZE=36
    )


scnr_decal_palette = Struct("decal_palette",
    dependency("decal"),
    ENDIAN=">", SIZE=16
    )


scnr_style_palette = Struct("style_palette",
    dependency("style"),
    ENDIAN=">", SIZE=16
    )


scnr_squad_group = Struct("squad_groups",
    StrLatin1("name", SIZE=32),
    SInt16("parent_index"),
    SInt16("objective_index"),
    SInt16("unknown"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=40
    )


scnr_squad_base_squad_multi_state = Struct("multi_state",
    SInt16("unknown"),
    SInt16("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    string_id_meta("state"),
    Pad(4),
    StrLatin1("command_script_name", SIZE=32),
    SInt16("command_script_index"),
    SInt16("unknown_5"),
    ENDIAN=">", SIZE=56
    )


scnr_squad_base_squad_starting_location_multi_state = Struct("multi_state",
    SInt16("unknown"),
    SInt16("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    string_id_meta("state"),
    Pad(4),
    StrLatin1("command_script_name", SIZE=32),
    SInt16("command_script_index"),
    SInt16("unknown_5"),
    ENDIAN=">", SIZE=56
    )


scnr_squad_base_squad_starting_location = Struct("starting_locations",
    SInt16("unknown"),
    SInt16("unknown_1"),
    string_id_meta("name"),
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    SInt16("reference_frame"),
    SInt16("unknown_2"),
    float_rad("facing_i"),
    float_rad("facing_j"),
    float_rad("facing_k"),
    Bool32("flags",
        ("always_place", 1 << 2),
        "initially_hidden",
        "kill_vehicle_if_no_driver",
        ),
    SInt16("character_type"),
    SInt16("initial_primary_weapon"),
    SInt16("initial_secondary_weapon"),
    SInt16("unknown_3"),
    SInt16("vehicle_type"),
    SEnum16("seat_type", *scnr_squad_base_squad_starting_location_seat_type),
    SEnum16("grenade_type", *scnr_squad_base_squad_grenade_type),
    SInt16("swarm_count"),
    string_id_meta("actor_variant"),
    string_id_meta("vehicle_variant"),
    Float("initial_movement_distance"),
    SInt16("emitter_vehicle"),
    SInt16("emitter_giant"),
    SInt16("emitter_biped"),
    SEnum16("initial_movement_mode", *scnr_squad_base_squad_starting_location_initial_movement_mode),
    StrLatin1("command_script_name", SIZE=32),
    SInt16("command_script_index"),
    SInt16("unknown_4"),
    string_id_meta("initial_state"),
    SInt16("unknown_5"),
    SInt16("unknown_6"),
    SInt16("unknown_7"),
    SInt16("unknown_8"),
    reflexive("multi_state", scnr_squad_base_squad_starting_location_multi_state),
    ENDIAN=">", SIZE=136
    )


scnr_squad_base_squad = Struct("base_squad",
    SInt16("unknown"),
    SInt16("unknown_1"),
    SInt16("size"),
    SInt16("unknown_2"),
    SInt16("character_type"),
    SInt16("initial_primary_weapon"),
    SInt16("initial_secondary_weapon"),
    SEnum16("grenade_type", *scnr_squad_base_squad_grenade_type),
    SInt16("equipment"),
    SInt16("vehicle"),
    string_id_meta("vehicle_variant"),
    StrLatin1("command_script_name", SIZE=32),
    SInt16("command_script_index"),
    SInt16("unknown_3"),
    string_id_meta("initial_state"),
    SInt16("unknown_4"),
    SInt16("unknown_5"),
    SInt16("unknown_6"),
    SInt16("unknown_7"),
    reflexive("multi_state", scnr_squad_base_squad_multi_state),
    reflexive("starting_locations", scnr_squad_base_squad_starting_location),
    ENDIAN=">", SIZE=96
    )


scnr_squad = Struct("squads",
    StrLatin1("name", SIZE=32),
    Bool32("flags",
        ("blind", 1 << 1),
        "deaf",
        "braindead",
        "initially_placed",
        "units_not_enterable_by_player",
        ),
    SEnum16("team", *scnr_squad_team),
    SInt16("parent_squad_group_index"),
    SInt16("parent_zone"),
    SInt16("trigger_index"),
    SInt16("objective_index"),
    SInt16("objective_role_index"),
    reflexive("base_squad", scnr_squad_base_squad),
    SInt16("unknown"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=64
    )


scnr_zone_firing_position = Struct("firing_positions",
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    SInt16("reference_frame"),
    SInt16("unknown"),
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
    SInt16("unknown_1"),
    SInt16("area_index"),
    SInt16("cluster_index"),
    SInt32("unknown_2"),
    float_rad("normal_y"),
    float_rad("normal_p"),
    Pad(4),
    ENDIAN=">", SIZE=40
    )


scnr_zone_area_flight_hint = Struct("flight_hints",
    SInt16("flight_hint_index"),
    SInt16("poit_index"),
    Pad(4),
    ENDIAN=">", SIZE=8
    )


scnr_zone_area = Struct("areas",
    StrLatin1("name", SIZE=32),
    Bool32("area_flags",
        "vehicle_area",
        "perch",
        "manual_reference_frame",
        ),
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    SInt32("unknown"),
    Float("unknown_1"),
    SInt16("firing_position_start_index"),
    SInt16("firing_position_count"),
    SInt16("unknown_2"),
    SInt16("unknown_3"),
    SInt32("unknown_4"),
    Pad(24),
    SInt16("manual_reference_frame"),
    SInt16("unknown_6"),
    reflexive("flight_hints", scnr_zone_area_flight_hint),
    ENDIAN=">", SIZE=108
    )


scnr_zone = Struct("zones",
    StrLatin1("name", SIZE=32),
    Bool32("flags",
        "uses_manual_bsp_index",
        ),
    SInt16("manual_bsp_index"),
    SInt16("unknown"),
    reflexive("firing_positions", scnr_zone_firing_position),
    reflexive("areas", scnr_zone_area),
    ENDIAN=">", SIZE=64
    )


scnr_character_palette = Struct("character_palette",
    dependency("character"),
    ENDIAN=">", SIZE=16
    )


scnr_ai_pathfinding_data_unknown = Struct("unknown",
    Pad(4),
    Float("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    SInt16("unknown_4"),
    SInt16("unknown_5"),
    Float("unknown_6"),
    Float("unknown_7"),
    Float("unknown_8"),
    SInt16("unknown_9"),
    SInt16("unknown_10"),
    ENDIAN=">", SIZE=36
    )


scnr_ai_pathfinding_data_unknown_1 = Struct("unknown_1",
    Pad(4),
    Float("unknown_1"),
    Float("unknown_2"),
    Float("unknown_3"),
    SInt16("unknown_4"),
    SInt16("unknown_5"),
    Float("unknown_6"),
    Float("unknown_7"),
    Float("unknown_8"),
    SInt16("unknown_9"),
    SInt16("unknown_10"),
    Float("unknown_11"),
    Float("unknown_12"),
    Float("unknown_13"),
    SInt16("unknown_14"),
    SInt16("unknown_15"),
    Float("unknown_16"),
    Float("unknown_17"),
    Float("unknown_18"),
    SInt16("unknown_19"),
    SInt16("unknown_20"),
    Pad(4),
    ENDIAN=">", SIZE=72
    )


scnr_ai_pathfinding_data_unknown_2 = Struct("unknown_2",
    SInt16("unknown"),
    SInt16("unknown_1"),
    SInt16("unknown_2"),
    SInt16("unknown_3"),
    ENDIAN=">", SIZE=8
    )


scnr_ai_pathfinding_data_unknown_3 = Struct("unknown_3",
    SInt32("unknown"),
    Pad(4),
    ENDIAN=">", SIZE=8
    )


scnr_ai_pathfinding_data_unknown_4_unknown_1 = Struct("unknown_1",
    Pad(28),
    ENDIAN=">", SIZE=28
    )


scnr_ai_pathfinding_data_unknown_4 = Struct("unknown_4",
    Pad(4),
    reflexive("unknown_1", scnr_ai_pathfinding_data_unknown_4_unknown_1),
    ENDIAN=">", SIZE=16
    )


scnr_ai_pathfinding_data_unknown_5_unknown = Struct("unknown",
    Float("unknown"),
    Float("unknown_1"),
    Float("unknown_2"),
    ENDIAN=">", SIZE=12
    )


scnr_ai_pathfinding_data_unknown_5 = Struct("unknown_5",
    reflexive("unknown", scnr_ai_pathfinding_data_unknown_5_unknown),
    ENDIAN=">", SIZE=12
    )


scnr_ai_pathfinding_data_unknown_6 = Struct("unknown_6",
    string_id_meta("unknown"),
    SInt16("unknown_1"),
    SInt16("unknown_2"),
    Float("unknown_3"),
    Float("unknown_4"),
    Float("unknown_5"),
    Float("unknown_6"),
    Float("unknown_7"),
    Float("unknown_8"),
    Float("unknown_9"),
    Float("unknown_10"),
    Float("unknown_11"),
    Float("unknown_12"),
    Float("unknown_13"),
    Float("unknown_14"),
    Float("unknown_15"),
    Float("unknown_16"),
    SInt32("unknown_17"),
    ENDIAN=">", SIZE=68
    )


scnr_ai_pathfinding_data_unknown_7_unknown_unknown = Struct("unknown",
    Float("unknown"),
    Float("unknown_1"),
    Float("unknown_2"),
    SInt16("unknown_3"),
    SInt16("unknown_4"),
    float_rad("unknown_5"),
    float_rad("unknown_6"),
    ENDIAN=">", SIZE=24
    )


scnr_ai_pathfinding_data_unknown_7_unknown = Struct("unknown",
    reflexive("unknown", scnr_ai_pathfinding_data_unknown_7_unknown_unknown),
    ENDIAN=">", SIZE=12
    )


scnr_ai_pathfinding_data_unknown_7 = Struct("unknown_7",
    reflexive("unknown", scnr_ai_pathfinding_data_unknown_7_unknown),
    ENDIAN=">", SIZE=8
    )


scnr_ai_pathfinding_data_unknown_8 = Struct("unknown_8",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


scnr_ai_pathfinding_data = Struct("ai_pathfinding_data",
    reflexive("unknown", scnr_ai_pathfinding_data_unknown),
    reflexive("unknown_1", scnr_ai_pathfinding_data_unknown_1),
    reflexive("unknown_2", scnr_ai_pathfinding_data_unknown_2),
    reflexive("unknown_3", scnr_ai_pathfinding_data_unknown_3),
    reflexive("unknown_4", scnr_ai_pathfinding_data_unknown_4),
    reflexive("unknown_5", scnr_ai_pathfinding_data_unknown_5),
    reflexive("unknown_6", scnr_ai_pathfinding_data_unknown_6),
    reflexive("unknown_7", scnr_ai_pathfinding_data_unknown_7),
    reflexive("unknown_8", scnr_ai_pathfinding_data_unknown_8),
    ENDIAN=">", SIZE=108
    )


scnr_script_parameter = Struct("parameters",
    StrLatin1("name", SIZE=32),
    SEnum16("type", *scnr_script_return_type),
    SInt16("unknown"),
    ENDIAN=">", SIZE=36
    )


scnr_script = Struct("scripts",
    StrLatin1("script_name", SIZE=32),
    SEnum16("script_type", *scnr_script_script_type),
    SEnum16("return_type", *scnr_script_return_type),
    UInt16("root_expression_salt"),
    UInt16("root_expression_index"),
    reflexive("parameters", scnr_script_parameter),
    ENDIAN=">", SIZE=52
    )


scnr_global = Struct("globals",
    StrLatin1("name", SIZE=32),
    SEnum16("type", *scnr_script_return_type),
    SInt16("unknown"),
    UInt16("initialization_expression_salt"),
    UInt16("initialization_expression_index"),
    ENDIAN=">", SIZE=40
    )


scnr_script_reference = Struct("script_references",
    dependency("reference"),
    ENDIAN=">", SIZE=16
    )


scnr_scripting_data_point_set_point = Struct("points",
    StrLatin1("name", SIZE=32),
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    SInt16("reference_frame"),
    SInt16("unknown"),
    SInt32("surface_index"),
    float_rad("facing_direction_y"),
    float_rad("facing_direction_p"),
    ENDIAN=">", SIZE=60
    )


scnr_scripting_data_point_set = Struct("point_sets",
    StrLatin1("name", SIZE=32),
    reflexive("points", scnr_scripting_data_point_set_point),
    SInt16("bsp_index"),
    SInt16("manual_reference_frame"),
    Bool32("flags",
        ),
    ENDIAN=">", SIZE=52
    )


scnr_scripting_data = Struct("scripting_data",
    reflexive("point_sets", scnr_scripting_data_point_set),
    Pad(120),
    ENDIAN=">", SIZE=132
    )


scnr_cutscene_flag = Struct("cutscene_flags",
    Pad(4),
    string_id_meta("name"),
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    float_rad("facing_y"),
    float_rad("facing_p"),
    ENDIAN=">", SIZE=28
    )


scnr_cutscene_camera_point = Struct("cutscene_camera_points",
    Bool16("flags",
        ),
    SEnum16("type", *scnr_cutscene_camera_point_type),
    StrLatin1("name", SIZE=32),
    SInt32("unknown"),
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    float_rad("orientation_y"),
    float_rad("orientation_p"),
    float_rad("orientation_r"),
    ENDIAN=">", SIZE=64
    )


scnr_cutscene_title = Struct("cutscene_titles",
    string_id_meta("name"),
    SInt16("text_bounds_top"),
    SInt16("text_bounds_left"),
    SInt16("text_bounds_bottom"),
    SInt16("text_bounds_right"),
    SEnum16("horizontal_justification", *scnr_cutscene_title_horizontal_justification),
    SEnum16("vertical_justification", *scnr_cutscene_title_vertical_justification),
    SInt16("font"),
    SInt16("unknown"),
    color_argb_uint32("text_color"),
    color_argb_uint32("shadow_color"),
    Float("fade_in_time"),
    Float("uptime"),
    Float("fade_out_time"),
    ENDIAN=">", SIZE=40
    )


scnr_scenario_resource_script_source = Struct("script_source",
    dependency("hs_source_file"),
    ENDIAN=">", SIZE=16
    )


scnr_scenario_resource_ai_resource = Struct("ai_resources",
    dependency("ai_resource"),
    ENDIAN=">", SIZE=16
    )


scnr_scenario_resource_reference = Struct("references",
    dependency("scenery_resource"),
    dependency("bipeds_resource"),
    dependency("vehicles_resource"),
    dependency("equipment_resource"),
    dependency("weapons_resource"),
    dependency("sound_scenery_resource"),
    dependency("lights_resource"),
    dependency("devices_resource"),
    dependency("effect_scenery_resource"),
    dependency("decals_resource"),
    dependency("cinematics_resource"),
    dependency("trigger_volumes_resource"),
    dependency("cluster_data_resource"),
    dependency("comments_resource"),
    dependency("creature_resource"),
    dependency("structure_lighting_resource"),
    dependency("decorators_resource"),
    dependency("sky_references_resource"),
    dependency("cubemap_resource"),
    ENDIAN=">", SIZE=304
    )


scnr_scenario_resource = Struct("scenario_resources",
    SInt32("unknown"),
    reflexive("script_source", scnr_scenario_resource_script_source),
    reflexive("ai_resources", scnr_scenario_resource_ai_resource),
    reflexive("references", scnr_scenario_resource_reference),
    ENDIAN=">", SIZE=40
    )


scnr_unit_seats_mapping = Struct("unit_seats_mapping",
    UInt32("unit"),
    Bool32("seats",
        "seat_0",
        "seat_1",
        "seat_2",
        "seat_3",
        "seat_4",
        "seat_5",
        "seat_6",
        "seat_7",
        "seat_8",
        "seat_9",
        "seat_10",
        "seat_11",
        "seat_12",
        "seat_13",
        "seat_14",
        "seat_15",
        "seat_16",
        "seat_17",
        "seat_18",
        "seat_19",
        "seat_20",
        "seat_21",
        "seat_22",
        "seat_23",
        "seat_24",
        "seat_25",
        "seat_26",
        "seat_27",
        "seat_28",
        "seat_29",
        "seat_30",
        "seat_31",
        ),
    Bool32("seats_2",
        "seat_32",
        "seat_33",
        "seat_34",
        "seat_35",
        "seat_36",
        "seat_37",
        "seat_38",
        "seat_39",
        "seat_40",
        "seat_41",
        "seat_42",
        "seat_43",
        "seat_44",
        "seat_45",
        "seat_46",
        "seat_47",
        "seat_48",
        "seat_49",
        "seat_50",
        "seat_51",
        "seat_52",
        "seat_53",
        "seat_54",
        "seat_55",
        "seat_56",
        "seat_57",
        "seat_58",
        "seat_59",
        "seat_60",
        "seat_61",
        "seat_62",
        "seat_63",
        ),
    ENDIAN=">", SIZE=12
    )


scnr_scenario_kill_trigger = Struct("scenario_kill_triggers",
    SInt16("trigger_volume"),
    ENDIAN=">", SIZE=2
    )


scnr_scenario_safe_trigger = Struct("scenario_safe_triggers",
    SInt16("trigger_volume"),
    ENDIAN=">", SIZE=2
    )


scnr_script_expression = Struct("script_expressions",
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
    SInt16("unknown"),
    ENDIAN=">", SIZE=24
    )


scnr_ai_trigger_condition = Struct("conditions",
    SEnum16("rule_type", *scnr_ai_trigger_condition_rule_type),
    SInt16("squad"),
    SInt16("squad_group"),
    SInt16("a"),
    Float("x"),
    SInt16("trigger_volume"),
    SInt16("unknown"),
    StrLatin1("exit_condition_script", SIZE=32),
    SInt16("exit_condition_script_index"),
    SInt16("unknown_1"),
    Bool32("flags",
        "not",
        ),
    ENDIAN=">", SIZE=56
    )


scnr_ai_trigger = Struct("ai_triggers",
    StrLatin1("name", SIZE=32),
    Bool32("trigger_flags",
        "latch_on_when_triggered",
        ),
    SEnum16("combination_rule", *scnr_ai_trigger_combination_rule),
    SInt16("unknown"),
    reflexive("conditions", scnr_ai_trigger_condition),
    ENDIAN=">", SIZE=52
    )


scnr_background_sound_environment_palette = Struct("background_sound_environment_palette",
    string_id_meta("name"),
    dependency("sound_environment"),
    Float("cutoff_distance"),
    Float("interpolation_speed"),
    dependency("background_sound"),
    dependency("inside_cluster_sound"),
    Float("cutoff_distance_1"),
    Bool32("scale_flags",
        ),
    Float("interior_scale"),
    Float("portal_scale"),
    Float("exterior_scale"),
    Float("interpolation_speed_1"),
    ENDIAN=">", SIZE=84
    )


scnr_unknown_16 = Struct("unknown_16",
    Pad(120),
    ENDIAN=">", SIZE=120
    )


scnr_fog = Struct("fog",
    string_id_meta("name"),
    SInt16("unknown"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=8
    )


scnr_camera_effect = Struct("camera_effects",
    string_id_meta("name"),
    dependency("effect"),
    SInt8("unknown"),
    SInt8("unknown_1"),
    SInt8("unknown_2"),
    SInt8("unknown_3"),
    Pad(4),
    Float("unknown_5"),
    Float("unknown_6"),
    Float("unknown_7"),
    Pad(8),
    ENDIAN=">", SIZE=48
    )


scnr_scenario_cluster_data_background_sound_environment = Struct("background_sound_environments",
    SInt16("background_sound_environment_index"),
    SInt16("unknown"),
    ENDIAN=">", SIZE=4
    )


scnr_scenario_cluster_data_unknown = Struct("unknown",
    SInt16("unknown"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=4
    )


scnr_scenario_cluster_data_unknown_1 = Struct("unknown_1",
    SInt16("unknown"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=4
    )


scnr_scenario_cluster_data_cluster_centroid = Struct("cluster_centroids",
    Float("centroid_x"),
    Float("centroid_y"),
    Float("centroid_z"),
    ENDIAN=">", SIZE=12
    )


scnr_scenario_cluster_data_unknown_2 = Struct("unknown_2",
    SInt16("unknown"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=4
    )


scnr_scenario_cluster_data_fog = Struct("fog",
    SInt16("fog_index"),
    SInt16("unknown"),
    ENDIAN=">", SIZE=4
    )


scnr_scenario_cluster_data_camera_effect = Struct("camera_effects",
    SInt16("camera_effect_index"),
    SInt16("unknown"),
    ENDIAN=">", SIZE=4
    )


scnr_scenario_cluster_data = Struct("scenario_cluster_data",
    dependency("bsp"),
    reflexive("background_sound_environments", scnr_scenario_cluster_data_background_sound_environment),
    reflexive("unknown", scnr_scenario_cluster_data_unknown),
    reflexive("unknown_1", scnr_scenario_cluster_data_unknown_1),
    SInt32("bsp_checksum"),
    reflexive("cluster_centroids", scnr_scenario_cluster_data_cluster_centroid),
    reflexive("unknown_2", scnr_scenario_cluster_data_unknown_2),
    reflexive("fog", scnr_scenario_cluster_data_fog),
    reflexive("camera_effects", scnr_scenario_cluster_data_camera_effect),
    ENDIAN=">", SIZE=104
    )


scnr_spawn_data_dynamic_spawn_overload = Struct("dynamic_spawn_overloads",
    SInt16("overload_type"),
    SInt16("unknown"),
    Float("inner_radius"),
    Float("outer_radius"),
    Float("weight"),
    ENDIAN=">", SIZE=16
    )


scnr_spawn_data_static_respawn_zone = Struct("static_respawn_zones",
    string_id_meta("name"),
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
    Bool32("relevant_games",
        ),
    Bool32("flags",
        ),
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    Float("lower_height"),
    Float("upper_height"),
    Float("inner_radius"),
    Float("outer_radius"),
    Float("weight"),
    ENDIAN=">", SIZE=48
    )


scnr_spawn_data_static_initial_spawn_zone = Struct("static_initial_spawn_zones",
    string_id_meta("name"),
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
    Bool32("relevant_games",
        ),
    Bool32("flags",
        ),
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
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
    reflexive("dynamic_spawn_overloads", scnr_spawn_data_dynamic_spawn_overload),
    reflexive("static_respawn_zones", scnr_spawn_data_static_respawn_zone),
    reflexive("static_initial_spawn_zones", scnr_spawn_data_static_initial_spawn_zone),
    ENDIAN=">", SIZE=108
    )


scnr_crate_node_positioning_node_flags_readable = Struct("node_flags_readable",
    Bool8("flags",
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
    SInt16("rotation_x"),
    SInt16("rotation_y"),
    SInt16("rotation_z"),
    SInt16("rotation_w"),
    ENDIAN=">", SIZE=8
    )


scnr_crate_node_positioning = Struct("node_positioning",
    SInt16("node_count"),
    SInt16("unknown"),
    reflexive("node_flags_readable", scnr_crate_node_positioning_node_flags_readable),
    reflexive("orientations_readable", scnr_crate_node_positioning_orientations_readable),
    ENDIAN=">", SIZE=28
    )


scnr_crate_unknown_9 = Struct("unknown_9",
    Pad(4),
    ENDIAN=">", SIZE=4
    )


scnr_crate = Struct("crates",
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
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    float_rad("rotation_i"),
    float_rad("rotation_j"),
    float_rad("rotation_k"),
    Float("scale"),
    reflexive("node_positioning", scnr_crate_node_positioning),
    SInt16("unknown"),
    Bool16("old_manual_bsp_flags_now_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        ),
    string_id_meta("unique_name"),
    UInt16("unique_id_salt"),
    UInt16("unique_id_index"),
    SInt16("origin_bsp_index"),
    SEnum8("type", *scnr_scenery_type),
    SEnum8("source", *scnr_scenery_source),
    SEnum8("bsp_policy", *scnr_scenery_bsp_policy),
    SInt8("unknown_1"),
    SInt16("editor_folder_index"),
    SInt16("unknown_2"),
    SInt16("parent_name_index"),
    string_id_meta("child_name"),
    string_id_meta("unknown_3"),
    Bool16("allowed_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        ),
    SInt16("unknown_4"),
    string_id_meta("variant"),
    Bool8("active_change_colors",
        "primary",
        "secondary",
        "tertiary",
        "quaternary",
        ),
    SInt8("unknown_5"),
    SInt8("unknown_6"),
    SInt8("unknown_7"),
    color_argb_uint32("primary_color"),
    color_argb_uint32("secondary_color"),
    color_argb_uint32("tertiary_color"),
    color_argb_uint32("quaternary_color"),
    Pad(4),
    reflexive("unknown_9", scnr_crate_unknown_9),
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
    SInt8("runtime_minimum"),
    SInt8("runtime_maximum"),
    Bool8("multiplayer_flags",
        "is_unique_object",
        "not_placed_at_start",
        ),
    SInt16("spawn_time"),
    SInt16("abandon_time"),
    SInt8("unknown_10"),
    SEnum8("shape", *scnr_scenery_shape),
    SInt8("teleporter_channel"),
    SInt8("unknown_11"),
    SInt16("unknown_12"),
    SInt16("attached_name_index"),
    Pad(8),
    Float("width_radius"),
    Float("depth"),
    Float("top"),
    Float("bottom"),
    Pad(4),
    ENDIAN=">", SIZE=176
    )


scnr_crate_palette = Struct("crate_palette",
    dependency("crate"),
    Pad(32),
    ENDIAN=">", SIZE=48
    )


scnr_flock_palette = Struct("flock_palette",
    dependency("flock"),
    ENDIAN=">", SIZE=16
    )


scnr_flock_source = Struct("sources",
    SInt32("unknown"),
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    float_rad("starting_y"),
    float_rad("starting_p"),
    Float("radius"),
    Float("weight"),
    SInt8("unknown_1"),
    SInt8("unknown_2"),
    SInt8("unknown_3"),
    SInt8("unknown_4"),
    ENDIAN=">", SIZE=36
    )


scnr_flock_sink = Struct("sinks",
    Float("position_x"),
    Float("position_y"),
    Float("position_z"),
    Float("radius"),
    ENDIAN=">", SIZE=16
    )


scnr_flock = Struct("flocks",
    string_id_meta("name"),
    SInt16("flock_palette_index"),
    SInt16("bsp_index"),
    SInt16("bounding_trigger_volume"),
    Bool16("flags",
        ),
    Float("ecology_margin"),
    reflexive("sources", scnr_flock_source),
    reflexive("sinks", scnr_flock_sink),
    Float("production_frequency_min"),
    Float("production_frequency_max"),
    Float("scale_min"),
    Float("scale_max"),
    Float("unknown"),
    Pad(4),
    SInt16("creature_palette_index"),
    SInt16("boid_count_min"),
    SInt16("boid_count_max"),
    SInt16("unknown_2"),
    ENDIAN=">", SIZE=72
    )


scnr_creature_palette = Struct("creature_palette",
    dependency("creature"),
    Pad(32),
    ENDIAN=">", SIZE=48
    )


scnr_editor_folder = Struct("editor_folders",
    SInt32("parent_folder"),
    StrLatin1("name", SIZE=256),
    ENDIAN=">", SIZE=260
    )


scnr_mission_dialogue = Struct("mission_dialogue",
    dependency("mission_dialogue"),
    ENDIAN=">", SIZE=16
    )


scnr_interpolator = Struct("interpolators",
    string_id_meta("name"),
    string_id_meta("accelerator_name"),
    string_id_meta("multiplier_name"),
    rawdata_ref("function"),
    SInt16("unknown"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=36
    )


scnr_simulation_definition_table = Struct("simulation_definition_table",
    UInt32("tag"),
    ENDIAN=">", SIZE=4
    )


scnr_unknown_22 = Struct("unknown_22",
    SInt16("unknown"),
    SInt16("unknown_1"),
    SInt16("unknown_2"),
    SInt16("unknown_3"),
    SInt16("unknown_4"),
    SInt16("unknown_5"),
    SInt16("unknown_6"),
    SInt16("unknown_7"),
    ENDIAN=">", SIZE=16
    )


scnr_ai_objective_role_unknown_84 = Struct("unknown_84",
    Pad(8),
    ENDIAN=">", SIZE=8
    )


scnr_ai_objective_role_condition = Struct("conditions",
    StrLatin1("name", SIZE=32),
    StrLatin1("condition", SIZE=256),
    SInt16("unknown"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=292
    )


scnr_ai_objective_role_unknown_14 = Struct("unknown_14",
    SInt16("unknown"),
    SInt16("unknown_1"),
    SInt16("unknown_2"),
    SInt16("unknown_3"),
    SInt16("unknown_4"),
    ENDIAN=">", SIZE=10
    )


scnr_ai_objective_role_point_geometry = Struct("point_geometry",
    Float("point_0_x"),
    Float("point_0_y"),
    Float("point_0_z"),
    SInt16("reference_frame"),
    SInt16("unknown"),
    Float("point_1_x"),
    Float("point_1_y"),
    Float("point_1_z"),
    SInt16("reference_frame_1"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=32
    )


scnr_ai_objective_role = Struct("roles",
    SInt16("unknown"),
    SInt16("unknown_1"),
    SInt16("unknown_2"),
    SInt16("unknown_3"),
    SInt16("unknown_4"),
    SInt16("unknown_5"),
    Pad(4),
    StrLatin1("command_script_name_1", SIZE=32),
    StrLatin1("command_script_name_2", SIZE=32),
    StrLatin1("command_script_name_3", SIZE=32),
    SInt16("command_script_index_1"),
    SInt16("command_script_index_2"),
    SInt16("command_script_index_3"),
    SInt16("unknown_7"),
    SInt16("unknown_8"),
    SInt16("unknown_9"),
    reflexive("unknown_84", scnr_ai_objective_role_unknown_84),
    string_id_meta("task"),
    SInt16("hierarchy_level_from_100"),
    SInt16("previous_role"),
    SInt16("next_role"),
    SInt16("parent_role"),
    reflexive("conditions", scnr_ai_objective_role_condition),
    SInt16("script_index"),
    SInt16("unknown_10"),
    SInt16("unknown_11"),
    SEnum16("filter", *scnr_ai_objective_role_filter),
    SInt16("min"),
    SInt16("max"),
    SInt16("bodies"),
    SInt16("unknown_12"),
    Pad(4),
    reflexive("unknown_14", scnr_ai_objective_role_unknown_14),
    reflexive("point_geometry", scnr_ai_objective_role_point_geometry),
    ENDIAN=">", SIZE=204
    )


scnr_ai_objective = Struct("ai_objectives",
    string_id_meta("name"),
    SInt16("zone"),
    SInt16("unknown"),
    reflexive("roles", scnr_ai_objective_role),
    ENDIAN=">", SIZE=20
    )


scnr_designer_zoneset_biped = Struct("bipeds",
    SInt16("palette_index"),
    ENDIAN=">", SIZE=2
    )


scnr_designer_zoneset_vehicle = Struct("vehicles",
    SInt16("palette_index"),
    ENDIAN=">", SIZE=2
    )


scnr_designer_zoneset_weapon = Struct("weapons",
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


scnr_designer_zoneset_machine = Struct("machines",
    SInt16("palette_index"),
    ENDIAN=">", SIZE=2
    )


scnr_designer_zoneset_terminal = Struct("terminals",
    SInt16("palette_index"),
    ENDIAN=">", SIZE=2
    )


scnr_designer_zoneset_control = Struct("controls",
    SInt16("palette_index"),
    ENDIAN=">", SIZE=2
    )


scnr_designer_zoneset_unknown_1 = Struct("unknown_1",
    SInt16("palette_index"),
    ENDIAN=">", SIZE=2
    )


scnr_designer_zoneset_crate = Struct("crates",
    SInt16("palette_index"),
    ENDIAN=">", SIZE=2
    )


scnr_designer_zoneset_creature = Struct("creatures",
    SInt16("palette_index"),
    ENDIAN=">", SIZE=2
    )


scnr_designer_zoneset_giant = Struct("giants",
    SInt16("palette_index"),
    ENDIAN=">", SIZE=2
    )


scnr_designer_zoneset_unknown_2 = Struct("unknown_2",
    SInt16("palette_index"),
    ENDIAN=">", SIZE=2
    )


scnr_designer_zoneset_character = Struct("characters",
    SInt16("palette_index"),
    ENDIAN=">", SIZE=2
    )


scnr_designer_zoneset = Struct("designer_zonesets",
    string_id_meta("name"),
    Pad(4),
    reflexive("bipeds", scnr_designer_zoneset_biped),
    reflexive("vehicles", scnr_designer_zoneset_vehicle),
    reflexive("weapons", scnr_designer_zoneset_weapon),
    reflexive("equipment", scnr_designer_zoneset_equipment),
    reflexive("scenery", scnr_designer_zoneset_scenery),
    reflexive("machines", scnr_designer_zoneset_machine),
    reflexive("terminals", scnr_designer_zoneset_terminal),
    reflexive("controls", scnr_designer_zoneset_control),
    reflexive("unknown_1", scnr_designer_zoneset_unknown_1),
    reflexive("crates", scnr_designer_zoneset_crate),
    reflexive("creatures", scnr_designer_zoneset_creature),
    reflexive("giants", scnr_designer_zoneset_giant),
    reflexive("unknown_2", scnr_designer_zoneset_unknown_2),
    reflexive("characters", scnr_designer_zoneset_character),
    Pad(12),
    ENDIAN=">", SIZE=188
    )


scnr_unknown_23 = Struct("unknown_23",
    SInt16("unknown"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=4
    )


scnr_cinematic = Struct("cinematics",
    dependency("cinematic"),
    ENDIAN=">", SIZE=16
    )


scnr_cinematic_lighting = Struct("cinematic_lighting",
    string_id_meta("name"),
    dependency("cinematic_light"),
    ENDIAN=">", SIZE=20
    )


scnr_scenario_metagame_time_multiplier = Struct("time_multipliers",
    Float("time"),
    Float("multiplier"),
    ENDIAN=">", SIZE=8
    )


scnr_scenario_metagame = Struct("scenario_metagame",
    reflexive("time_multipliers", scnr_scenario_metagame_time_multiplier),
    Float("par_score"),
    ENDIAN=">", SIZE=16
    )


scnr_unknown_26 = Struct("unknown_26",
    Pad(8),
    ENDIAN=">", SIZE=8
    )


scnr_unknown_27 = Struct("unknown_27",
    Pad(12),
    SInt16("unknown_1"),
    SInt16("unknown_2"),
    ENDIAN=">", SIZE=16
    )


scnr_cortana_effect = Struct("cortana_effects",
    dependency("unknown"),
    ENDIAN=">", SIZE=16
    )


scnr_lightmap_airprobe = Struct("lightmap_airprobes",
    Pad(12),
    string_id_meta("unknown_1"),
    Bool16("unknown_2",
        ),
    SInt16("unknown_3"),
    ENDIAN=">", SIZE=20
    )


scnr_meta_def = BlockDef("scnr",
    SEnum16("map_type", *scnr_map_type),
    Bool16("flags",
        ("characters_use_previous_mission_weapons", 1 << 5),
        ),
    SInt32("campaign_id"),
    SInt32("map_id"),
    float_rad("local_north"),
    Float("sandbox_budget"),
    reflexive("structure_bsps", scnr_structure_bsp),
    dependency("unknown"),
    reflexive("sky_references", scnr_sky_reference),
    reflexive("bsp_groups", scnr_bsp_group),
    reflexive("scenario_bsp_audibility", scnr_scenario_bsp_audibility),
    reflexive("scenario_zoneset_groups", scnr_scenario_zoneset_group),
    reflexive("bsp_atlas", scnr_bsp_atla),
    Pad(36),
    rawdata_ref("editor_scenario_data"),
    Pad(12),
    reflexive("object_names", scnr_object_name),
    reflexive("scenery", scnr_scenery),
    reflexive("scenery_palette", scnr_scenery_palette),
    reflexive("bipeds", scnr_biped),
    reflexive("biped_palette", scnr_biped_palette),
    reflexive("vehicles", scnr_vehicle),
    reflexive("vehicle_palette", scnr_vehicle_palette),
    reflexive("equipment", scnr_equipment),
    reflexive("equipment_palette", scnr_equipment_palette),
    reflexive("weapons", scnr_weapon),
    reflexive("weapon_palette", scnr_weapon_palette),
    reflexive("device_groups", scnr_device_group),
    reflexive("machines", scnr_machine),
    reflexive("machine_palette", scnr_machine_palette),
    reflexive("terminals", scnr_terminal),
    reflexive("terminal_palette", scnr_terminal_palette),
    reflexive("controls", scnr_control),
    reflexive("control_palette", scnr_control_palette),
    reflexive("sound_scenery", scnr_sound_scenery),
    reflexive("sound_scenery_palette", scnr_sound_scenery_palette),
    reflexive("giants", scnr_giant),
    reflexive("giant_palette", scnr_giant_palette),
    reflexive("effect_scenery", scnr_effect_scenery),
    reflexive("effect_scenery_palette", scnr_effect_scenery_palette),
    reflexive("light_volumes", scnr_light_volume),
    reflexive("light_volumes_palette", scnr_light_volumes_palette),
    reflexive("sandbox_vehicles", scnr_sandbox_vehicle),
    reflexive("sandbox_weapons", scnr_sandbox_weapon),
    reflexive("sandbox_equipment", scnr_sandbox_equipment),
    reflexive("sandbox_scenery", scnr_sandbox_scenery),
    reflexive("sandbox_teleporters", scnr_sandbox_teleporter),
    reflexive("sandbox_goal_objects", scnr_sandbox_goal_object),
    reflexive("sandbox_spawning", scnr_sandbox_spawning),
    reflexive("soft_ceilings", scnr_soft_ceiling),
    reflexive("player_starting_profile", scnr_player_starting_profile),
    reflexive("player_starting_locations", scnr_player_starting_location),
    reflexive("trigger_volumes", scnr_trigger_volume),
    Pad(12),
    reflexive("zoneset_switch_trigger_volumes", scnr_zoneset_switch_trigger_volume),
    reflexive("multiplayer_constants_override", scnr_multiplayer_constants_override),
    reflexive("unknown_4", scnr_unknown_4),
    reflexive("unknown_5", scnr_unknown_5),
    reflexive("unknown_6", scnr_unknown_6),
    reflexive("unknown_7", scnr_unknown_7),
    Pad(144),
    reflexive("decals", scnr_decal),
    reflexive("decal_palette", scnr_decal_palette),
    Pad(12),
    reflexive("style_palette", scnr_style_palette),
    reflexive("squad_groups", scnr_squad_group),
    reflexive("squads", scnr_squad),
    reflexive("zones", scnr_zone),
    Pad(12),
    reflexive("character_palette", scnr_character_palette),
    Pad(12),
    reflexive("ai_pathfinding_data", scnr_ai_pathfinding_data),
    Pad(12),
    rawdata_ref("script_strings"),
    reflexive("scripts", scnr_script),
    reflexive("globals", scnr_global),
    reflexive("script_references", scnr_script_reference),
    Pad(12),
    reflexive("scripting_data", scnr_scripting_data),
    reflexive("cutscene_flags", scnr_cutscene_flag),
    reflexive("cutscene_camera_points", scnr_cutscene_camera_point),
    reflexive("cutscene_titles", scnr_cutscene_title),
    dependency("custom_object_name_strings"),
    dependency("chapter_title_strings"),
    reflexive("scenario_resources", scnr_scenario_resource),
    reflexive("unit_seats_mapping", scnr_unit_seats_mapping),
    reflexive("scenario_kill_triggers", scnr_scenario_kill_trigger),
    reflexive("scenario_safe_triggers", scnr_scenario_safe_trigger),
    reflexive("script_expressions", scnr_script_expression),
    Pad(12),
    reflexive("ai_triggers", scnr_ai_trigger),
    reflexive("background_sound_environment_palette", scnr_background_sound_environment_palette),
    Pad(24),
    reflexive("unknown_16", scnr_unknown_16),
    reflexive("fog", scnr_fog),
    reflexive("camera_effects", scnr_camera_effect),
    Pad(36),
    reflexive("scenario_cluster_data", scnr_scenario_cluster_data),
    Pad(12),
    SInt32("object_salts_1"),
    SInt32("object_salts_2"),
    SInt32("object_salts_3"),
    SInt32("object_salts_4"),
    SInt32("object_salts_5"),
    SInt32("object_salts_6"),
    SInt32("object_salts_7"),
    SInt32("object_salts_8"),
    SInt32("object_salts_9"),
    SInt32("object_salts_10"),
    SInt32("object_salts_11"),
    SInt32("object_salts_12"),
    SInt32("object_salts_13"),
    SInt32("object_salts_14"),
    SInt32("object_salts_15"),
    SInt32("object_salts_16"),
    SInt32("object_salts_17"),
    SInt32("object_salts_18"),
    SInt32("object_salts_19"),
    SInt32("object_salts_20"),
    SInt32("object_salts_21"),
    SInt32("object_salts_22"),
    SInt32("object_salts_23"),
    SInt32("object_salts_24"),
    SInt32("object_salts_25"),
    SInt32("object_salts_26"),
    SInt32("object_salts_27"),
    SInt32("object_salts_28"),
    SInt32("object_salts_29"),
    SInt32("object_salts_30"),
    SInt32("object_salts_31"),
    SInt32("object_salts_32"),
    reflexive("spawn_data", scnr_spawn_data),
    dependency("sound_effects_collection"),
    reflexive("crates", scnr_crate),
    reflexive("crate_palette", scnr_crate_palette),
    reflexive("flock_palette", scnr_flock_palette),
    reflexive("flocks", scnr_flock),
    dependency("subtitle_strings"),
    Pad(12),
    reflexive("creature_palette", scnr_creature_palette),
    reflexive("editor_folders", scnr_editor_folder),
    dependency("territory_location_name_strings"),
    Pad(8),
    reflexive("mission_dialogue", scnr_mission_dialogue),
    dependency("objective_strings"),
    reflexive("interpolators", scnr_interpolator),
    Pad(24),
    reflexive("simulation_definition_table", scnr_simulation_definition_table),
    dependency("default_camera_fx"),
    dependency("default_screen_fx"),
    dependency("sky_parameters"),
    dependency("global_lighing"),
    dependency("lightmap"),
    dependency("performance_throttles"),
    reflexive("unknown_22", scnr_unknown_22),
    reflexive("ai_objectives", scnr_ai_objective),
    reflexive("designer_zonesets", scnr_designer_zoneset),
    reflexive("unknown_23", scnr_unknown_23),
    Pad(12),
    reflexive("cinematics", scnr_cinematic),
    reflexive("cinematic_lighting", scnr_cinematic_lighting),
    Pad(12),
    reflexive("scenario_metagame", scnr_scenario_metagame),
    reflexive("unknown_26", scnr_unknown_26),
    reflexive("unknown_27", scnr_unknown_27),
    reflexive("cortana_effects", scnr_cortana_effect),
    reflexive("lightmap_airprobes", scnr_lightmap_airprobe),
    Pad(12),
    TYPE=Struct, ENDIAN=">", SIZE=1976
    )