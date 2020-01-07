#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: Lord Zedd
# 	Standardized
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef

ugh__platform_codec_encoding = (
    "mono",
    "stereo",
    "surround",
    "_5_1_surround",
    )

ugh__platform_codec_sample_rate = (
    "_22khz",
    "_44khz",
    "_32khz",
    )


ugh__platform_codec = Struct("platform_codec",
    SEnum8("sample_rate", *ugh__platform_codec_sample_rate),
    SEnum8("encoding", *ugh__platform_codec_encoding),
    SInt8("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=3
    )


ugh__playback_parameter = Struct("playback_parameter",
    Bool32("field_disable_flags",
        "distance_a",
        "distance_b",
        "distance_c",
        "distance_d",
        ),
    Float("distance_a"),
    Float("distance_b"),
    Float("distance_c"),
    Float("distance_d"),
    Float("skip_fraction"),
    Float("maximum_bend_per_second"),
    Float("gain_base"),
    Float("gain_variance"),
    QStruct("random_pitch_bounds", INCLUDE=from_to_sint16),
    float_rad("inner_cone_angle"),
    float_rad("outer_cone_angle"),
    Float("outer_cone_gain"),
    Bool32("flags",
        "override_azimuth",
        "override_3d_gain",
        "override_speaker_gain",
        ),
    float_rad("azimuth"),
    Float("positional_gain"),
    Float("first_person_gain"),
    ENDIAN=">", SIZE=68
    )


ugh__scale = Struct("scale",
    QStruct("gain_modifier", INCLUDE=from_to),
    QStruct("pitch_modifier", INCLUDE=from_to_sint16),
    QStruct("skip_fraction_modifier", INCLUDE=from_to),
    ENDIAN=">", SIZE=20
    )


ugh__import_name = Struct("import_name",
    h3_string_id("name"),
    ENDIAN=">", SIZE=4
    )


ugh__pitch_range_parameter = Struct("pitch_range_parameter",
    SInt16("natural_pitch"),
    QStruct("bend_bounds", INCLUDE=from_to_sint16),
    QStruct("max_gain_pitch_bounds", INCLUDE=from_to_sint16),
    QStruct("unknown_bounds", INCLUDE=from_to_sint16, VISIBLE=False),
    ENDIAN=">", SIZE=14
    )


ugh__pitch_range = Struct("pitch_range",
    SInt16("import_name_index"),
    SInt16("pitch_range_parameter_index"),
    SInt16("encoded_permutation_data_index"),
    SInt16("encoded_runtime_permutation_flag_index"),
    SInt16("encoded_permutation_count"),
    UInt16("first_permuation_index"),
    ENDIAN=">", SIZE=12
    )


ugh__permutation = Struct("permutation",
    SInt16("import_name_index"),
    SInt16("encoded_skip_fraction"),
    UInt32("sample_size"),
    SInt32("first_permutation_chunk"),
    SInt16("permutation_chunk_count"),
    SInt8("gain"),
    SInt8("pitch_range_overall_permutation_index"),
    ENDIAN=">", SIZE=16
    )


ugh__custom_playback_filter = Struct("filter",
    SInt32("filter_type"),
    SInt32("filter_width"),
    QStruct("scale_bounds_0", INCLUDE=from_to),
    Float("random_base_0"),
    Float("random_variance_0"),
    QStruct("scale_bounds_1", INCLUDE=from_to),
    Float("random_base_1"),
    Float("random_variance_1"),
    QStruct("scale_bounds_2", INCLUDE=from_to),
    Float("random_base_2"),
    Float("random_variance_2"),
    QStruct("scale_bounds_3", INCLUDE=from_to),
    Float("random_base_3"),
    Float("random_variance_3"),
    ENDIAN=">", SIZE=72
    )


ugh__custom_playback = Struct("custom_playback",
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    Bool32("flags",
        "use_3d_radio_hack",
        ),
    BytesRaw("unknown_1", SIZE=8, VISIBLE=False),
    h3_reflexive("filter", ugh__custom_playback_filter),
    BytesRaw("unknown_2", SIZE=36, VISIBLE=False),
    ENDIAN=">", SIZE=72
    )


ugh__language_unknown_a = Struct("unknown_a",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


ugh__language_unknown_b = Struct("unknown_b",
    SInt16("unknown_a_start_index"),
    SInt16("unknown_a_count"),
    ENDIAN=">", SIZE=4
    )


ugh__language = Struct("language",
    SEnum32("language", *ugh__language_language),
    h3_reflexive("unknown_a", ugh__language_unknown_a),
    h3_reflexive("unknown_b", ugh__language_unknown_b),
    ENDIAN=">", SIZE=28
    )


ugh__runtime_permutation_flag = Struct("runtime_permutation_flag",
    SInt8("unknown"),
    ENDIAN=">", SIZE=1
    )


ugh__permutation_chunk = Struct("permutation_chunk",
    UInt32("file_offset"),
    Bool8("flags",
        ("has_unknown_a_value", 1 << 5),
        ),
    UInt8("chunk_size_leftmost_byte"),
    UInt16("chunk_size"),
    SInt32("runtime_index"),
    SInt32("unknown_a"),
    SInt32("unknown_size"),
    ENDIAN=">", SIZE=20
    )


ugh__promotion_rule = Struct("rule",
    SInt16("pitch_range_index"),
    SInt16("maximum_playing_count"),
    Float("suppression_time"),
    SInt32("unknown_0", VISIBLE=False),
    SInt32("unknown_1", VISIBLE=False),
    ENDIAN=">", SIZE=16
    )


ugh__promotion_runtime_timer = Struct("runtime_timer",
    SInt32("unknown"),
    ENDIAN=">", SIZE=4
    )


ugh__promotion = Struct("promotion",
    h3_reflexive("rules", ugh__promotion_rule),
    h3_reflexive("runtime_timers", ugh__promotion_runtime_timer),
    SInt32("unknown_0", VISIBLE=False),
    BytesRaw("unknown_1", SIZE=8, VISIBLE=False),
    ENDIAN=">", SIZE=36
    )


ugh__extra_info_encoded_permutation_section_sound_dialogue_info = Struct("sound_dialogue_info",
    UInt32("mouth_data_offset"),
    UInt32("mouth_data_length"),
    UInt32("lipsync_data_offset"),
    UInt32("lipsynce_data_length"),
    ENDIAN=">", SIZE=16
    )


ugh__extra_info_encoded_permutation_section_unknown_unknown_unknown_1 = Struct("unknown_1",
    Pad(8),
    ENDIAN=">", SIZE=8
    )


ugh__extra_info_encoded_permutation_section_unknown_unknown_unknown_2 = Struct("unknown_2",
    Array("unknown_array", SUB_STRUCT=SInt16("unknown"), SIZE=4),
    ENDIAN=">", SIZE=8
    )


ugh__extra_info_encoded_permutation_section_unknown_unknown = Struct("unknown",
    Pad(16),
    h3_reflexive("unknown_1", ugh__extra_info_encoded_permutation_section_unknown_unknown_unknown_1),
    h3_reflexive("unknown_2", ugh__extra_info_encoded_permutation_section_unknown_unknown_unknown_2),
    ENDIAN=">", SIZE=40
    )


ugh__extra_info_encoded_permutation_section_unknown = Struct("unknown",
    h3_reflexive("unknown", ugh__extra_info_encoded_permutation_section_unknown_unknown),
    ENDIAN=">", SIZE=12
    )


ugh__extra_info_encoded_permutation_section = Struct("encoded_permutation_section",
    h3_rawdata_ref("encoded_data"),
    h3_reflexive("sound_dialogue_info", ugh__extra_info_encoded_permutation_section_sound_dialogue_info),
    h3_reflexive("unknown", ugh__extra_info_encoded_permutation_section_unknown),
    ENDIAN=">", SIZE=44
    )


ugh__extra_info = Struct("extra_info",
    h3_reflexive("encoded_permutation_sections", ugh__extra_info_encoded_permutation_section),
    ENDIAN=">", SIZE=12
    )


ugh__body = Struct("tagdata",
    h3_reflexive("platform_codec", ugh__platform_codec),
    h3_reflexive("playback_parameters", ugh__playback_parameter),
    h3_reflexive("scales", ugh__scale),
    h3_reflexive("import_names", ugh__import_name),
    h3_reflexive("pitch_range_parameters", ugh__pitch_range_parameter),
    h3_reflexive("pitch_ranges", ugh__pitch_range),
    h3_reflexive("permutations", ugh__permutation),
    h3_reflexive("custom_playbacks", ugh__custom_playback),
    h3_reflexive("languages", ugh__language),
    h3_reflexive("runtime_permutation_flags", ugh__runtime_permutation_flag),
    h3_rawdata_ref("unknown_0", VISIBLE=False),
    BytesRaw("unknown_1", SIZE=8, VISIBLE=False),
    h3_reflexive("permutation_chunks", ugh__permutation_chunk),
    h3_reflexive("promotions", ugh__promotion),
    h3_reflexive("extra_infos", ugh__extra_info),
    ENDIAN=">", SIZE=184
    )


def get():
    return ugh__def

ugh__def = TagDef("ugh!",
    h3_blam_header('ugh!'),
    ugh__body,

    ext=".%s" % h3_tag_class_fcc_to_ext["ugh!"], endian=">", tag_cls=H3Tag
    )
