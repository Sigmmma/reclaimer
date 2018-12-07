############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: -DeToX-
# 	Found Raw Identifier
# revision: 3		author: Lord Zedd
# 	Lookin Nice
# revision: 4		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
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


jmad_skeleton_node = Struct("skeleton_node", 
    h3_string_id("name"),
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
    QStruct("base_vector", INCLUDE=ijk_float),
    Float("vector_range"),
    Float("z_position"),
    ENDIAN=">", SIZE=32
    )


jmad_sound_reference = Struct("sound_reference", 
    h3_dependency("sound"),
    Bool16("flags", 
        "allow_on_player",
        "left_arm_only",
        "right_arm_only",
        "first_person_only",
        "forward_only",
        "reverse_only",
        ),
    SInt16("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=20
    )


jmad_effect_reference = Struct("effect_reference", 
    h3_dependency("effect"),
    Bool16("flags", 
        "allow_on_player",
        "left_arm_only",
        "right_arm_only",
        "first_person_only",
        "forward_only",
        "reverse_only",
        ),
    SInt16("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=20
    )


jmad_blend_screen = Struct("blend_screen", 
    h3_string_id("label"),
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


jmad_leg = Struct("leg", 
    h3_string_id("foot_marker"),
    QStruct("foot", INCLUDE=from_to),
    h3_string_id("ankle_marker"),
    QStruct("ankle", INCLUDE=from_to),
    SEnum16("anchors", *jmad_leg_anchors),
    SInt16("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=28
    )


jmad_animation_frame_event = Struct("frame_event", 
    SEnum16("type", *jmad_animation_frame_event_type),
    SInt16("frame"),
    ENDIAN=">", SIZE=4
    )


jmad_animation_sound_event = Struct("sound_event", 
    SInt16("sound"),
    SInt16("frame"),
    h3_string_id("marker_name"),
    ENDIAN=">", SIZE=8
    )


jmad_animation_effect_event = Struct("effect_event", 
    SInt16("effect"),
    SInt16("frame"),
    h3_string_id("marker_name"),
    ENDIAN=">", SIZE=8
    )


jmad_animation_unknown_2 = Struct("unknown_2", 
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


jmad_animation_object_space_parent_node = Struct("object_space_parent_node", 
    SInt16("node_index"),
    Bool16("component_flags", 
        "rotation",
        "translation",
        "scale",
        ),
    QStruct("rotation", INCLUDE=ijkw_sint16),
    QStruct("default_translation", INCLUDE=xyz_float),
    Float("default_scale"),
    ENDIAN=">", SIZE=28
    )


jmad_animation_leg_anchoring_unknown_1 = Struct("unknown_1", 
    SInt16("frame_1a"),
    SInt16("frame_2a"),
    SInt16("frame_1b"),
    SInt16("frame_2b"),
    BytesRaw("unknown", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=20
    )


jmad_animation_leg_anchoring = Struct("leg_anchoring", 
    SInt16("leg_index"),
    SInt16("unknown_0", VISIBLE=False),
    h3_reflexive("unknown_1", jmad_animation_leg_anchoring_unknown_1),
    ENDIAN=">", SIZE=16
    )


jmad_animation = Struct("animation", 
    h3_string_id("name"),
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
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    SInt16("previous_variant_sibling"),
    SInt16("next_variant_sibling"),
    SInt16("raw_information_group_index"),
    SInt16("raw_information_member_index"),
    h3_reflexive("frame_events", jmad_animation_frame_event),
    h3_reflexive("sound_events", jmad_animation_sound_event),
    h3_reflexive("effect_events", jmad_animation_effect_event),
    h3_reflexive("unknown_2", jmad_animation_unknown_2),
    h3_reflexive("object_space_parent_nodes", jmad_animation_object_space_parent_node),
    h3_reflexive("leg_anchoring", jmad_animation_leg_anchoring),
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=5, VISIBLE=False),
    ENDIAN=">", SIZE=136
    )


jmad_mode_weapon_clas_weapon_type_action = Struct("action", 
    h3_string_id("label"),
    SInt16("graph_index"),
    SInt16("animation"),
    ENDIAN=">", SIZE=8
    )


jmad_mode_weapon_clas_weapon_type_overlay = Struct("overlay", 
    h3_string_id("label"),
    SInt16("graph_index"),
    SInt16("animation"),
    ENDIAN=">", SIZE=8
    )


jmad_mode_weapon_clas_weapon_type_death_and_damage_direction_region = Struct("region", 
    SInt16("graph_index"),
    SInt16("animation"),
    ENDIAN=">", SIZE=4
    )


jmad_mode_weapon_clas_weapon_type_death_and_damage_direction = Struct("direction", 
    h3_reflexive("regions", jmad_mode_weapon_clas_weapon_type_death_and_damage_direction_region),
    ENDIAN=">", SIZE=12
    )


jmad_mode_weapon_clas_weapon_type_death_and_damage = Struct("death_and_damage", 
    h3_string_id("label"),
    h3_reflexive("directions", jmad_mode_weapon_clas_weapon_type_death_and_damage_direction),
    ENDIAN=">", SIZE=16
    )


jmad_mode_weapon_clas_weapon_type_transition_destination = Struct("destination", 
    h3_string_id("full_name"),
    h3_string_id("mode_name"),
    h3_string_id("state_name"),
    SEnum8("frame_event_link", *jmad_mode_weapon_clas_weapon_type_transition_destination_frame_event_link),
    SInt8("unknown", VISIBLE=False),
    SInt8("index_a"),
    SInt8("index_b"),
    SInt16("graph_index"),
    SInt16("animation"),
    ENDIAN=">", SIZE=20
    )


jmad_mode_weapon_clas_weapon_type_transition = Struct("transition", 
    h3_string_id("full_name"),
    h3_string_id("state_name"),
    SInt16("unknown", VISIBLE=False),
    SInt8("index_a"),
    SInt8("index_b"),
    h3_reflexive("destinations", jmad_mode_weapon_clas_weapon_type_transition_destination),
    ENDIAN=">", SIZE=24
    )


jmad_mode_weapon_clas_weapon_type = Struct("weapon_type", 
    h3_string_id("label"),
    h3_reflexive("actions", jmad_mode_weapon_clas_weapon_type_action),
    h3_reflexive("overlays", jmad_mode_weapon_clas_weapon_type_overlay),
    h3_reflexive("death_and_damage", jmad_mode_weapon_clas_weapon_type_death_and_damage),
    h3_reflexive("transitions", jmad_mode_weapon_clas_weapon_type_transition),
    ENDIAN=">", SIZE=52
    )


jmad_mode_weapon_clas_weapon_ik = Struct("weapon_ik", 
    h3_string_id("marker"),
    h3_string_id("attach_to_marker"),
    ENDIAN=">", SIZE=8
    )


jmad_mode_weapon_clas = Struct("weapon_clas", 
    h3_string_id("label"),
    h3_reflexive("weapon_type", jmad_mode_weapon_clas_weapon_type),
    h3_reflexive("weapon_ik", jmad_mode_weapon_clas_weapon_ik),
    ENDIAN=">", SIZE=28
    )


jmad_mode_mode_ik = Struct("mode_ik", 
    h3_string_id("marker"),
    h3_string_id("attach_to_marker"),
    ENDIAN=">", SIZE=8
    )


jmad_mode = Struct("mode", 
    h3_string_id("label"),
    h3_reflexive("weapon_class", jmad_mode_weapon_clas),
    h3_reflexive("mode_ik", jmad_mode_mode_ik),
    BytesRaw("unknown", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=40
    )


jmad_vehicle_suspension = Struct("vehicle_suspension", 
    h3_string_id("label"),
    SInt16("graph_index"),
    SInt16("animation"),
    h3_string_id("marker_name"),
    Float("mass_point_offset_0"),
    Float("full_extension_ground_depth"),
    Float("full_compression_ground_depth"),
    h3_string_id("region_name"),
    Float("mass_point_offset_1"),
    Float("expression_ground_depth"),
    Float("compression_ground_depth"),
    ENDIAN=">", SIZE=40
    )


jmad_object_overlay = Struct("object_overlay", 
    h3_string_id("label"),
    SInt16("graph_index"),
    SInt16("animation"),
    SInt16("unknown_0", VISIBLE=False),
    SEnum16("function_controls", *jmad_object_overlay_function_controls),
    h3_string_id("function"),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=20
    )


jmad_inheritance_list_node_map = Struct("node_map", 
    SInt16("local_node"),
    ENDIAN=">", SIZE=2
    )


jmad_inheritance_list_node_map_flag = Struct("node_map_flag", 
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
    h3_dependency("inherited_graph"),
    h3_reflexive("node_map", jmad_inheritance_list_node_map),
    h3_reflexive("node_map_flags", jmad_inheritance_list_node_map_flag),
    Float("root_z_offset"),
    Bool32("inheritance_flags", 
        "tighten_nodes",
        ),
    ENDIAN=">", SIZE=48
    )


jmad_weapon_list = Struct("weapon_list", 
    h3_string_id("weapon_name"),
    h3_string_id("weapon_class"),
    ENDIAN=">", SIZE=8
    )


jmad_raw_information_group = Struct("raw_information_group", 
    SInt32("member_count"),
    zone_asset("asset_data"),
    ENDIAN=">", SIZE=12
    )


jmad_body = Struct("tagdata", 
    h3_dependency("parent_animation_graph"),
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
    h3_reflexive("skeleton_nodes", jmad_skeleton_node),
    h3_reflexive("sound_references", jmad_sound_reference),
    h3_reflexive("effect_references", jmad_effect_reference),
    h3_reflexive("blend_screens", jmad_blend_screen),
    h3_reflexive("legs", jmad_leg),
    h3_reflexive("animations", jmad_animation),
    h3_reflexive("modes", jmad_mode),
    h3_reflexive("vehicle_suspension", jmad_vehicle_suspension),
    h3_reflexive("object_overlays", jmad_object_overlay),
    h3_reflexive("inheritance_list", jmad_inheritance_list),
    h3_reflexive("weapon_list", jmad_weapon_list),
    Bool32("unknown_arm_nodes_1", *("node_%s" % i for i in range(32)), VISIBLE=False),
    Bool32("unknown_arm_nodes_2", *("node_%s" % i for i in range(32, 64)), VISIBLE=False),
    Bool32("unknown_arm_nodes_3", *("node_%s" % i for i in range(64, 96)), VISIBLE=False),
    Bool32("unknown_arm_nodes_4", *("node_%s" % i for i in range(96, 128)), VISIBLE=False),
    Bool32("unknown_arm_nodes_5", *("node_%s" % i for i in range(128, 160)), VISIBLE=False),
    Bool32("unknown_arm_nodes_6", *("node_%s" % i for i in range(160, 192)), VISIBLE=False),
    Bool32("unknown_arm_nodes_7", *("node_%s" % i for i in range(192, 224)), VISIBLE=False),
    Bool32("unknown_arm_nodes_8", *("node_%s" % i for i in range(224, 256)), VISIBLE=False),
    Bool32("unknown_nodes_1", *("node_%s" % i for i in range(32)), VISIBLE=False),
    Bool32("unknown_nodes_2", *("node_%s" % i for i in range(32, 64)), VISIBLE=False),
    Bool32("unknown_nodes_3", *("node_%s" % i for i in range(64, 96)), VISIBLE=False),
    Bool32("unknown_nodes_4", *("node_%s" % i for i in range(96, 128)), VISIBLE=False),
    Bool32("unknown_nodes_5", *("node_%s" % i for i in range(128, 160)), VISIBLE=False),
    Bool32("unknown_nodes_6", *("node_%s" % i for i in range(160, 192)), VISIBLE=False),
    Bool32("unknown_nodes_7", *("node_%s" % i for i in range(192, 224)), VISIBLE=False),
    Bool32("unknown_nodes_8", *("node_%s" % i for i in range(224, 256)), VISIBLE=False),
    h3_rawdata_ref("last_import_results"),
    BytesRaw("unknown", SIZE=12, VISIBLE=False),
    h3_reflexive("raw_information_groups", jmad_raw_information_group),
    ENDIAN=">", SIZE=260
    )


def get():
    return jmad_def

jmad_def = TagDef("jmad",
    h3_blam_header('jmad'),
    jmad_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["jmad"], endian=">", tag_cls=H3Tag
    )
