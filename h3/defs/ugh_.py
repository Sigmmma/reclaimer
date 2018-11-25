from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

ugh_language_language = (
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

ugh_platform_codec_encoding = (
    "mono",
    "stereo",
    "surround",
    "_5_1_surround",
    )

ugh_platform_codec_sample_rate = (
    "_22khz",
    "_44khz",
    "_32khz",
    )


ugh_platform_codec = Struct("platform_codec",
    SEnum8("sample_rate", *ugh_platform_codec_sample_rate),
    SEnum8("encoding", *ugh_platform_codec_encoding),
    SInt8("unknown"),
    ENDIAN=">", SIZE=3
    )


ugh_playback_parameter = Struct("playback_parameters",
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
    SInt16("random_pitch_bounds_min"),
    SInt16("random_pitch_bounds_max"),
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


ugh_scale = Struct("scales",
    Float("gain_modifier_min"),
    Float("gain_modifier_max"),
    SInt16("pitch_modifier_min"),
    SInt16("pitch_modifier_max"),
    Float("skip_fraction_modifier_min"),
    Float("skip_fraction_modifier_max"),
    ENDIAN=">", SIZE=20
    )


ugh_import_name = Struct("import_names",
    string_id_meta("name"),
    ENDIAN=">", SIZE=4
    )


ugh_pitch_range_parameter = Struct("pitch_range_parameters",
    SInt16("natural_pitch"),
    SInt16("bend_bounds_min"),
    SInt16("bend_bounds_max"),
    SInt16("max_gain_pitch_bounds_min"),
    SInt16("max_gain_pitch_bounds_max"),
    SInt16("unknown_bounds_min"),
    SInt16("unknown_bounds_max"),
    ENDIAN=">", SIZE=14
    )


ugh_pitch_range = Struct("pitch_ranges",
    SInt16("import_name_index"),
    SInt16("pitch_range_parameter_index"),
    SInt16("encoded_permutation_data_index"),
    SInt16("encoded_runtime_permutation_flag_index"),
    SInt16("encoded_permutation_count"),
    UInt16("first_permuation_index"),
    ENDIAN=">", SIZE=12
    )


ugh_permutation = Struct("permutations",
    SInt16("import_name_index"),
    SInt16("encoded_skip_fraction"),
    UInt32("sample_size"),
    SInt32("first_permutation_chunk"),
    SInt16("permutation_chunk_count"),
    SInt8("gain"),
    SInt8("pitch_range_overall_permutation_index"),
    ENDIAN=">", SIZE=16
    )


ugh_custom_playback_filter = Struct("filter",
    SInt32("filter_type"),
    SInt32("filter_width"),
    Float("scale_bounds_min"),
    Float("scale_bounds_max"),
    Float("random_base"),
    Float("random_variance"),
    Float("scale_bounds_min_1"),
    Float("scale_bounds_max_1"),
    Float("random_base_1"),
    Float("random_variance_1"),
    Float("scale_bounds_min_2"),
    Float("scale_bounds_max_2"),
    Float("random_base_2"),
    Float("random_variance_2"),
    Float("scale_bounds_min_3"),
    Float("scale_bounds_max_3"),
    Float("random_base_3"),
    Float("random_variance_3"),
    ENDIAN=">", SIZE=72
    )


ugh_custom_playback = Struct("custom_playbacks",
    Pad(12),
    Bool32("flags",
        "use_3d_radio_hack",
        ),
    Pad(8),
    reflexive("filter", ugh_custom_playback_filter),
    Pad(36),
    ENDIAN=">", SIZE=72
    )


ugh_language_unknown_a = Struct("unknown_a",
    SInt16("unknown"),
    ENDIAN=">", SIZE=2
    )


ugh_language_unknown_b = Struct("unknown_b",
    SInt16("unknown_a_start_index"),
    SInt16("unknown_a_count"),
    ENDIAN=">", SIZE=4
    )


ugh_language = Struct("languages",
    SEnum32("language", *ugh_language_language),
    reflexive("unknown_a", ugh_language_unknown_a),
    reflexive("unknown_b", ugh_language_unknown_b),
    ENDIAN=">", SIZE=28
    )


ugh_runtime_permutation_flag = Struct("runtime_permutation_flags",
    SInt8("unknown"),
    ENDIAN=">", SIZE=1
    )


ugh_permutation_chunk = Struct("permutation_chunks",
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


ugh_promotion_rule = Struct("rules",
    SInt16("pitch_range_index"),
    SInt16("maximum_playing_count"),
    Float("suppression_time"),
    SInt32("unknown"),
    SInt32("unknown_1"),
    ENDIAN=">", SIZE=16
    )


ugh_promotion_runtime_timer = Struct("runtime_timers",
    SInt32("unknown"),
    ENDIAN=">", SIZE=4
    )


ugh_promotion = Struct("promotions",
    reflexive("rules", ugh_promotion_rule),
    reflexive("runtime_timers", ugh_promotion_runtime_timer),
    SInt32("unknown"),
    Pad(8),
    ENDIAN=">", SIZE=36
    )


ugh_extra_info_encoded_permutation_section_sound_dialogue_info = Struct("sound_dialogue_info",
    UInt32("mouth_data_offset"),
    UInt32("mouth_data_length"),
    UInt32("lipsync_data_offset"),
    UInt32("lipsynce_data_length"),
    ENDIAN=">", SIZE=16
    )


ugh_extra_info_encoded_permutation_section_unknown_unknown_unknown_1 = Struct("unknown_1",
    Pad(8),
    ENDIAN=">", SIZE=8
    )


ugh_extra_info_encoded_permutation_section_unknown_unknown_unknown_2 = Struct("unknown_2",
    SInt16("unknown"),
    SInt16("unknown_1"),
    SInt16("unknown_2"),
    SInt16("unknown_3"),
    ENDIAN=">", SIZE=8
    )


ugh_extra_info_encoded_permutation_section_unknown_unknown = Struct("unknown",
    Pad(16),
    reflexive("unknown_1", ugh_extra_info_encoded_permutation_section_unknown_unknown_unknown_1),
    reflexive("unknown_2", ugh_extra_info_encoded_permutation_section_unknown_unknown_unknown_2),
    ENDIAN=">", SIZE=40
    )


ugh_extra_info_encoded_permutation_section_unknown = Struct("unknown",
    reflexive("unknown", ugh_extra_info_encoded_permutation_section_unknown_unknown),
    ENDIAN=">", SIZE=12
    )


ugh_extra_info_encoded_permutation_section = Struct("encoded_permutation_sections",
    rawdata_ref("encoded_data"),
    reflexive("sound_dialogue_info", ugh_extra_info_encoded_permutation_section_sound_dialogue_info),
    reflexive("unknown", ugh_extra_info_encoded_permutation_section_unknown),
    ENDIAN=">", SIZE=44
    )


ugh_extra_info = Struct("extra_info",
    reflexive("encoded_permutation_sections", ugh_extra_info_encoded_permutation_section),
    ENDIAN=">", SIZE=12
    )


ugh__meta_def = BlockDef("ugh!",
    reflexive("platform_codec", ugh_platform_codec),
    reflexive("playback_parameters", ugh_playback_parameter),
    reflexive("scales", ugh_scale),
    reflexive("import_names", ugh_import_name),
    reflexive("pitch_range_parameters", ugh_pitch_range_parameter),
    reflexive("pitch_ranges", ugh_pitch_range),
    reflexive("permutations", ugh_permutation),
    reflexive("custom_playbacks", ugh_custom_playback),
    reflexive("languages", ugh_language),
    reflexive("runtime_permutation_flags", ugh_runtime_permutation_flag),
    rawdata_ref("unknown"),
    Pad(8),
    reflexive("permutation_chunks", ugh_permutation_chunk),
    reflexive("promotions", ugh_promotion),
    reflexive("extra_info", ugh_extra_info),
    TYPE=Struct, ENDIAN=">", SIZE=184
    )
