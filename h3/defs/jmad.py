from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

jmad_animation_desired_compression = (
    "best_score",
    "best_compression",
    "best_accuracy",
    "best_fullframe",
    "best_small_keyframe",
    "best_large_keyframe",
    )

jmad_animation_frame_event_type = (
    "primary_keyframe",
    "secondary_keyframe",
    "left_foot",
    "right_foot",
    "allow_interruption",
    "transition_a",
    "transition_b",
    "transition_c",
    "transition_d",
    "both_feet_shuffle",
    "body_impact",
    )

jmad_animation_frame_info_type = (
    "none",
    "dx_dy",
    "dx_dy_dyaw",
    "dx_dy_dz_dyaw",
    )

jmad_animation_type = (
    "base",
    "overlay",
    "replacement",
    )

jmad_leg_anchors = (
    "false",
    "true",
    )

jmad_mode_weapon_clas_weapon_type_transition_destination_frame_event_link = (
    "no_keyframe",
    "keyframe_type_a",
    "keyframe_type_b",
    "keyframe_type_c",
    "keyframe_type_d",
    )

jmad_object_overlay_function_controls = (
    "frame",
    "scale",
    )


jmad_skeleton_node = Struct("skeleton_nodes",
    string_id_meta("name"),
    SInt16("next_sibling_node_index"),
    SInt16("first_child_node_index"),
    SInt16("parent_node_index"),
    Bool8("model_flags",
        "primary_model",
        "secondary_model",
        "local_root",
        "left_hand",
        "right_hand",
        "left_arm_member",
        ),
    Bool8("node_joint_flags",
        "ball_socket",
        "hinge",
        "no_movement",
        ),
    Float("base_vector_i"),
    Float("base_vector_j"),
    Float("base_vector_k"),
    Float("vector_range"),
    Float("z_position"),
    ENDIAN=">", SIZE=32
    )


jmad_sound_reference = Struct("sound_references",
    dependency("sound"),
    Bool16("flags",
        "allow_on_player",
        "left_arm_only",
        "right_arm_only",
        "first_person_only",
        "forward_only",
        "reverse_only",
        ),
    SInt16("unknown"),
    ENDIAN=">", SIZE=20
    )


jmad_effect_reference = Struct("effect_references",
    dependency("effect"),
    Bool16("flags",
        "allow_on_player",
        "left_arm_only",
        "right_arm_only",
        "first_person_only",
        "forward_only",
        "reverse_only",
        ),
    SInt16("unknown"),
    ENDIAN=">", SIZE=20
    )


jmad_blend_screen = Struct("blend_screens",
    string_id_meta("label"),
    float_rad("right_yaw_per_frame"),
    float_rad("left_yaw_per_frame"),
    SInt16("right_frame_count"),
    SInt16("left_frame_count"),
    float_rad("down_pitch_per_frame"),
    float_rad("up_pitch_per_frame"),
    SInt16("down_pitch_frame_count"),
    SInt16("up_pitch_frame_count"),
    ENDIAN=">", SIZE=28
    )


jmad_leg = Struct("legs",
    string_id_meta("foot_marker"),
    Float("foot_min"),
    Float("foot_max"),
    string_id_meta("ankle_marker"),
    Float("ankle_min"),
    Float("ankle_max"),
    SEnum16("anchors", *jmad_leg_anchors),
    SInt16("unknown"),
    ENDIAN=">", SIZE=28
    )


jmad_animation_frame_event = Struct("frame_events",
    SEnum16("type", *jmad_animation_frame_event_type),
    SInt16("frame"),
    ENDIAN=">", SIZE=4
    )


jmad_animation_sound_event = Struct("sound_events",
    SInt16("sound"),
    SInt16("frame"),
    string_id_meta("marker_name"),
    ENDIAN=">", SIZE=8
    )


jmad_animation_effect_event = Struct("effect_events",
    SInt16("effect"),
    SInt16("frame"),
    string_id_meta("marker_name"),
    ENDIAN=">", SIZE=8
    )


jmad_animation_unknown_2 = Struct("unknown_2",
    SInt16("unknown"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=4
    )


jmad_animation_object_space_parent_node = Struct("object_space_parent_nodes",
    SInt16("node_index"),
    Bool16("component_flags",
        "rotation",
        "translation",
        "scale",
        ),
    SInt16("rotation_x"),
    SInt16("rotation_y"),
    SInt16("rotation_z"),
    SInt16("rotation_w"),
    Float("default_translation_x"),
    Float("default_translation_y"),
    Float("default_translation_z"),
    Float("default_scale"),
    ENDIAN=">", SIZE=28
    )


jmad_animation_leg_anchoring_unknown_1 = Struct("unknown_1",
    SInt16("frame_1a"),
    SInt16("frame_2a"),
    SInt16("frame_1b"),
    SInt16("frame_2b"),
    Pad(12),
    ENDIAN=">", SIZE=20
    )


jmad_animation_leg_anchoring = Struct("leg_anchoring",
    SInt16("leg_index"),
    SInt16("unknown"),
    reflexive("unknown_1", jmad_animation_leg_anchoring_unknown_1),
    ENDIAN=">", SIZE=16
    )


jmad_animation = Struct("animations",
    string_id_meta("name"),
    Float("weight"),
    SInt16("loop_frame_index"),
    Bool16("playback_flags",
        "disable_interpolation_in",
        "disable_interpolation_out",
        "disable_mode_ik",
        "disable_weapon_ik",
        "disable_weapon_aim_first_person",
        "disable_look_screen",
        "disable_transition_adjustment",
        ),
    SInt8("blend_screen"),
    SEnum8("desired_compression", *jmad_animation_desired_compression),
    SEnum8("current_compression", *jmad_animation_desired_compression),
    UInt8("node_count"),
    SInt16("frame_count"),
    SEnum8("type", *jmad_animation_type),
    SEnum8("frame_info_type", *jmad_animation_frame_info_type),
    Bool16("production_flags",
        "do_not_monitor_changes",
        "verify_sound_events",
        "do_not_inherit_for_player_graphs",
        ),
    Bool16("internal_flags",
        ("world_relative", 1 << 1),
        ("compression_disabled", 1 << 5),
        "old_production_checksum",
        "valid_production_checksum",
        ),
    SInt32("node_list_checksum"),
    SInt32("production_checksum"),
    SInt16("unknown"),
    SInt16("unknown_1"),
    SInt16("previous_variant_sibling"),
    SInt16("next_variant_sibling"),
    SInt16("raw_information_group_index"),
    SInt16("raw_information_member_index"),
    reflexive("frame_events", jmad_animation_frame_event),
    reflexive("sound_events", jmad_animation_sound_event),
    reflexive("effect_events", jmad_animation_effect_event),
    reflexive("unknown_2", jmad_animation_unknown_2),
    reflexive("object_space_parent_nodes", jmad_animation_object_space_parent_node),
    reflexive("leg_anchoring", jmad_animation_leg_anchoring),
    Float("unknown_3"),
    Float("unknown_4"),
    Float("unknown_5"),
    Float("unknown_6"),
    Float("unknown_7"),
    ENDIAN=">", SIZE=136
    )


jmad_mode_weapon_clas_weapon_type_action = Struct("actions",
    string_id_meta("label"),
    SInt16("graph_index"),
    SInt16("animation"),
    ENDIAN=">", SIZE=8
    )


jmad_mode_weapon_clas_weapon_type_overlay = Struct("overlays",
    string_id_meta("label"),
    SInt16("graph_index"),
    SInt16("animation"),
    ENDIAN=">", SIZE=8
    )


jmad_mode_weapon_clas_weapon_type_death_and_damage_direction_region = Struct("regions",
    SInt16("graph_index"),
    SInt16("animation"),
    ENDIAN=">", SIZE=4
    )


jmad_mode_weapon_clas_weapon_type_death_and_damage_direction = Struct("directions",
    reflexive("regions", jmad_mode_weapon_clas_weapon_type_death_and_damage_direction_region),
    ENDIAN=">", SIZE=12
    )


jmad_mode_weapon_clas_weapon_type_death_and_damage = Struct("death_and_damage",
    string_id_meta("label"),
    reflexive("directions", jmad_mode_weapon_clas_weapon_type_death_and_damage_direction),
    ENDIAN=">", SIZE=16
    )


jmad_mode_weapon_clas_weapon_type_transition_destination = Struct("destinations",
    string_id_meta("full_name"),
    string_id_meta("mode_name"),
    string_id_meta("state_name"),
    SEnum8("frame_event_link", *jmad_mode_weapon_clas_weapon_type_transition_destination_frame_event_link),
    SInt8("unknown"),
    SInt8("index_a"),
    SInt8("index_b"),
    SInt16("graph_index"),
    SInt16("animation"),
    ENDIAN=">", SIZE=20
    )


jmad_mode_weapon_clas_weapon_type_transition = Struct("transitions",
    string_id_meta("full_name"),
    string_id_meta("state_name"),
    SInt16("unknown"),
    SInt8("index_a"),
    SInt8("index_b"),
    reflexive("destinations", jmad_mode_weapon_clas_weapon_type_transition_destination),
    ENDIAN=">", SIZE=24
    )


jmad_mode_weapon_clas_weapon_type = Struct("weapon_type",
    string_id_meta("label"),
    reflexive("actions", jmad_mode_weapon_clas_weapon_type_action),
    reflexive("overlays", jmad_mode_weapon_clas_weapon_type_overlay),
    reflexive("death_and_damage", jmad_mode_weapon_clas_weapon_type_death_and_damage),
    reflexive("transitions", jmad_mode_weapon_clas_weapon_type_transition),
    ENDIAN=">", SIZE=52
    )


jmad_mode_weapon_clas_weapon_ik = Struct("weapon_ik",
    string_id_meta("marker"),
    string_id_meta("attach_to_marker"),
    ENDIAN=">", SIZE=8
    )


jmad_mode_weapon_clas = Struct("weapon_class",
    string_id_meta("label"),
    reflexive("weapon_type", jmad_mode_weapon_clas_weapon_type),
    reflexive("weapon_ik", jmad_mode_weapon_clas_weapon_ik),
    ENDIAN=">", SIZE=28
    )


jmad_mode_mode_ik = Struct("mode_ik",
    string_id_meta("marker"),
    string_id_meta("attach_to_marker"),
    ENDIAN=">", SIZE=8
    )


jmad_mode = Struct("modes",
    string_id_meta("label"),
    reflexive("weapon_class", jmad_mode_weapon_clas),
    reflexive("mode_ik", jmad_mode_mode_ik),
    Pad(12),
    ENDIAN=">", SIZE=40
    )


jmad_vehicle_suspension = Struct("vehicle_suspension",
    string_id_meta("label"),
    SInt16("graph_index"),
    SInt16("animation"),
    string_id_meta("marker_name"),
    Float("mass_point_offset"),
    Float("full_extension_ground_depth"),
    Float("full_compression_ground_depth"),
    string_id_meta("region_name"),
    Float("mass_point_offset_1"),
    Float("expression_ground_depth"),
    Float("compression_ground_depth"),
    ENDIAN=">", SIZE=40
    )


jmad_object_overlay = Struct("object_overlays",
    string_id_meta("label"),
    SInt16("graph_index"),
    SInt16("animation"),
    SInt16("unknown"),
    SEnum16("function_controls", *jmad_object_overlay_function_controls),
    string_id_meta("function"),
    Pad(4),
    ENDIAN=">", SIZE=20
    )


jmad_inheritance_list_node_map = Struct("node_map",
    SInt16("local_node"),
    ENDIAN=">", SIZE=2
    )


jmad_inheritance_list_node_map_flag = Struct("node_map_flags",
    Bool32("local_node_flags",
        "node_0_32_64_96_128_160_192_224",
        "node_1_33_65_97_129_161_193_225",
        "node_2_34_66_98_130_162_194_226",
        "node_3_35_67_99_131_163_195_227",
        "node_4_36_68_100_132_164_196_228",
        "node_5_37_69_101_133_165_197_229",
        "node_6_38_70_102_134_166_198_230",
        "node_7_39_71_103_135_167_199_231",
        "node_8_40_72_104_136_168_200_232",
        "node_9_41_73_105_137_169_201_233",
        "node_10_42_74_106_138_170_202_234",
        "node_11_43_75_107_139_171_203_235",
        "node_12_44_76_108_140_172_204_236",
        "node_13_45_77_109_141_173_205_237",
        "node_14_46_78_110_142_174_206_238",
        "node_15_47_79_111_143_175_207_239",
        "node_16_48_80_112_144_176_208_240",
        "node_17_49_81_113_145_177_209_241",
        "node_18_50_82_114_146_178_210_242",
        "node_19_51_83_115_147_179_211_243",
        "node_20_52_84_116_148_180_212_244",
        "node_21_53_85_117_149_181_213_245",
        "node_22_54_86_118_150_182_214_246",
        "node_23_55_87_119_151_183_215_247",
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


jmad_inheritance_list = Struct("inheritance_list",
    dependency("inherited_graph"),
    reflexive("node_map", jmad_inheritance_list_node_map),
    reflexive("node_map_flags", jmad_inheritance_list_node_map_flag),
    Float("root_z_offset"),
    Bool32("inheritance_flags",
        "tighten_nodes",
        ),
    ENDIAN=">", SIZE=48
    )


jmad_weapon_list = Struct("weapon_list",
    string_id_meta("weapon_name"),
    string_id_meta("weapon_class"),
    ENDIAN=">", SIZE=8
    )


jmad_raw_information_group = Struct("raw_information_groups",
    SInt32("member_count"),
    UInt16("zone_asset_salt"),
    UInt16("zone_asset_index"),
    SInt32("useless_padding"),
    ENDIAN=">", SIZE=12
    )


jmad_meta_def = BlockDef("jmad",
    dependency("parent_animation_graph"),
    Bool8("inheritance_flags",
        "inherit_root_trans_scale_only",
        "inherit_for_use_on_player",
        ),
    Bool8("private_flags",
        "prepared_for_cache",
        ("imported_with_codec_compressors", 1 << 2),
        ("written_to_cache", 1 << 4),
        "animation_data_reordered",
        ),
    SInt16("animation_codec_pack"),
    reflexive("skeleton_nodes", jmad_skeleton_node),
    reflexive("sound_references", jmad_sound_reference),
    reflexive("effect_references", jmad_effect_reference),
    reflexive("blend_screens", jmad_blend_screen),
    reflexive("legs", jmad_leg),
    reflexive("animations", jmad_animation),
    reflexive("modes", jmad_mode),
    reflexive("vehicle_suspension", jmad_vehicle_suspension),
    reflexive("object_overlays", jmad_object_overlay),
    reflexive("inheritance_list", jmad_inheritance_list),
    reflexive("weapon_list", jmad_weapon_list),
    Bool32("unknown_arm_nodes_1",
        "node_0",
        "node_1",
        "node_2",
        "node_3",
        "node_4",
        "node_5",
        "node_6",
        "node_7",
        "node_8",
        "node_9",
        "node_10",
        "node_11",
        "node_12",
        "node_13",
        "node_14",
        "node_15",
        "node_16",
        "node_17",
        "node_18",
        "node_19",
        "node_20",
        "node_21",
        "node_22",
        "node_23",
        "node_24",
        "node_25",
        "node_26",
        "node_27",
        "node_28",
        "node_29",
        "node_30",
        "node_31",
        ),
    Bool32("unknown_arm_nodes_2",
        "node_32",
        "node_33",
        "node_34",
        "node_35",
        "node_36",
        "node_37",
        "node_38",
        "node_39",
        "node_40",
        "node_41",
        "node_42",
        "node_43",
        "node_44",
        "node_45",
        "node_46",
        "node_47",
        "node_48",
        "node_49",
        "node_50",
        "node_51",
        "node_52",
        "node_53",
        "node_54",
        "node_55",
        "node_56",
        "node_57",
        "node_58",
        "node_59",
        "node_60",
        "node_61",
        "node_62",
        "node_63",
        ),
    Bool32("unknown_arm_nodes_3",
        "node_64",
        "node_65",
        "node_66",
        "node_67",
        "node_68",
        "node_69",
        "node_70",
        "node_71",
        "node_72",
        "node_73",
        "node_74",
        "node_75",
        "node_76",
        "node_77",
        "node_78",
        "node_79",
        "node_80",
        "node_81",
        "node_82",
        "node_83",
        "node_84",
        "node_85",
        "node_86",
        "node_87",
        "node_88",
        "node_89",
        "node_90",
        "node_91",
        "node_92",
        "node_93",
        "node_94",
        "node_95",
        ),
    Bool32("unknown_arm_nodes_4",
        "node_96",
        "node_97",
        "node_98",
        "node_99",
        "node_100",
        "node_101",
        "node_102",
        "node_103",
        "node_104",
        "node_105",
        "node_106",
        "node_107",
        "node_108",
        "node_109",
        "node_110",
        "node_111",
        "node_112",
        "node_113",
        "node_114",
        "node_115",
        "node_116",
        "node_117",
        "node_118",
        "node_119",
        "node_120",
        "node_121",
        "node_122",
        "node_123",
        "node_124",
        "node_125",
        "node_126",
        "node_127",
        ),
    Bool32("unknown_arm_nodes_5",
        "node_128",
        "node_129",
        "node_130",
        "node_131",
        "node_132",
        "node_133",
        "node_134",
        "node_135",
        "node_136",
        "node_137",
        "node_138",
        "node_139",
        "node_140",
        "node_141",
        "node_142",
        "node_143",
        "node_144",
        "node_145",
        "node_146",
        "node_147",
        "node_148",
        "node_149",
        "node_150",
        "node_151",
        "node_152",
        "node_153",
        "node_154",
        "node_155",
        "node_156",
        "node_157",
        "node_158",
        "node_159",
        ),
    Bool32("unknown_arm_nodes_6",
        "node_160",
        "node_161",
        "node_162",
        "node_163",
        "node_164",
        "node_165",
        "node_166",
        "node_167",
        "node_168",
        "node_169",
        "node_170",
        "node_171",
        "node_172",
        "node_173",
        "node_174",
        "node_175",
        "node_176",
        "node_177",
        "node_178",
        "node_179",
        "node_180",
        "node_181",
        "node_182",
        "node_183",
        "node_184",
        "node_185",
        "node_186",
        "node_187",
        "node_188",
        "node_189",
        "node_190",
        "node_191",
        ),
    Bool32("unknown_arm_nodes_7",
        "node_192",
        "node_193",
        "node_194",
        "node_195",
        "node_196",
        "node_197",
        "node_198",
        "node_199",
        "node_200",
        "node_201",
        "node_202",
        "node_203",
        "node_204",
        "node_205",
        "node_206",
        "node_207",
        "node_208",
        "node_209",
        "node_210",
        "node_211",
        "node_212",
        "node_213",
        "node_214",
        "node_215",
        "node_216",
        "node_217",
        "node_218",
        "node_219",
        "node_220",
        "node_221",
        "node_222",
        "node_223",
        ),
    Bool32("unknown_arm_nodes_8",
        "node_224",
        "node_225",
        "node_226",
        "node_227",
        "node_228",
        "node_229",
        "node_230",
        "node_231",
        "node_232",
        "node_233",
        "node_234",
        "node_235",
        "node_236",
        "node_237",
        "node_238",
        "node_239",
        "node_240",
        "node_241",
        "node_242",
        "node_243",
        "node_244",
        "node_245",
        "node_246",
        "node_247",
        "node_248",
        "node_249",
        "node_250",
        "node_251",
        "node_252",
        "node_253",
        "node_254",
        "node_255",
        ),
    Bool32("unknown_nodes_1",
        "node_0",
        "node_1",
        "node_2",
        "node_3",
        "node_4",
        "node_5",
        "node_6",
        "node_7",
        "node_8",
        "node_9",
        "node_10",
        "node_11",
        "node_12",
        "node_13",
        "node_14",
        "node_15",
        "node_16",
        "node_17",
        "node_18",
        "node_19",
        "node_20",
        "node_21",
        "node_22",
        "node_23",
        "node_24",
        "node_25",
        "node_26",
        "node_27",
        "node_28",
        "node_29",
        "node_30",
        "node_31",
        ),
    Bool32("unknown_nodes_2",
        "node_32",
        "node_33",
        "node_34",
        "node_35",
        "node_36",
        "node_37",
        "node_38",
        "node_39",
        "node_40",
        "node_41",
        "node_42",
        "node_43",
        "node_44",
        "node_45",
        "node_46",
        "node_47",
        "node_48",
        "node_49",
        "node_50",
        "node_51",
        "node_52",
        "node_53",
        "node_54",
        "node_55",
        "node_56",
        "node_57",
        "node_58",
        "node_59",
        "node_60",
        "node_61",
        "node_62",
        "node_63",
        ),
    Bool32("unknown_nodes_3",
        "node_64",
        "node_65",
        "node_66",
        "node_67",
        "node_68",
        "node_69",
        "node_70",
        "node_71",
        "node_72",
        "node_73",
        "node_74",
        "node_75",
        "node_76",
        "node_77",
        "node_78",
        "node_79",
        "node_80",
        "node_81",
        "node_82",
        "node_83",
        "node_84",
        "node_85",
        "node_86",
        "node_87",
        "node_88",
        "node_89",
        "node_90",
        "node_91",
        "node_92",
        "node_93",
        "node_94",
        "node_95",
        ),
    Bool32("unknown_nodes_4",
        "node_96",
        "node_97",
        "node_98",
        "node_99",
        "node_100",
        "node_101",
        "node_102",
        "node_103",
        "node_104",
        "node_105",
        "node_106",
        "node_107",
        "node_108",
        "node_109",
        "node_110",
        "node_111",
        "node_112",
        "node_113",
        "node_114",
        "node_115",
        "node_116",
        "node_117",
        "node_118",
        "node_119",
        "node_120",
        "node_121",
        "node_122",
        "node_123",
        "node_124",
        "node_125",
        "node_126",
        "node_127",
        ),
    Bool32("unknown_nodes_5",
        "node_128",
        "node_129",
        "node_130",
        "node_131",
        "node_132",
        "node_133",
        "node_134",
        "node_135",
        "node_136",
        "node_137",
        "node_138",
        "node_139",
        "node_140",
        "node_141",
        "node_142",
        "node_143",
        "node_144",
        "node_145",
        "node_146",
        "node_147",
        "node_148",
        "node_149",
        "node_150",
        "node_151",
        "node_152",
        "node_153",
        "node_154",
        "node_155",
        "node_156",
        "node_157",
        "node_158",
        "node_159",
        ),
    Bool32("unknown_nodes_6",
        "node_160",
        "node_161",
        "node_162",
        "node_163",
        "node_164",
        "node_165",
        "node_166",
        "node_167",
        "node_168",
        "node_169",
        "node_170",
        "node_171",
        "node_172",
        "node_173",
        "node_174",
        "node_175",
        "node_176",
        "node_177",
        "node_178",
        "node_179",
        "node_180",
        "node_181",
        "node_182",
        "node_183",
        "node_184",
        "node_185",
        "node_186",
        "node_187",
        "node_188",
        "node_189",
        "node_190",
        "node_191",
        ),
    Bool32("unknown_nodes_7",
        "node_192",
        "node_193",
        "node_194",
        "node_195",
        "node_196",
        "node_197",
        "node_198",
        "node_199",
        "node_200",
        "node_201",
        "node_202",
        "node_203",
        "node_204",
        "node_205",
        "node_206",
        "node_207",
        "node_208",
        "node_209",
        "node_210",
        "node_211",
        "node_212",
        "node_213",
        "node_214",
        "node_215",
        "node_216",
        "node_217",
        "node_218",
        "node_219",
        "node_220",
        "node_221",
        "node_222",
        "node_223",
        ),
    Bool32("unknown_nodes_8",
        "node_224",
        "node_225",
        "node_226",
        "node_227",
        "node_228",
        "node_229",
        "node_230",
        "node_231",
        "node_232",
        "node_233",
        "node_234",
        "node_235",
        "node_236",
        "node_237",
        "node_238",
        "node_239",
        "node_240",
        "node_241",
        "node_242",
        "node_243",
        "node_244",
        "node_245",
        "node_246",
        "node_247",
        "node_248",
        "node_249",
        "node_250",
        "node_251",
        "node_252",
        "node_253",
        "node_254",
        "node_255",
        ),
    rawdata_ref("last_import_results"),
    Pad(12),
    reflexive("raw_information_groups", jmad_raw_information_group),
    TYPE=Struct, ENDIAN=">", SIZE=260
    )