from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef

from_to_cents = QStruct("", INCLUDE=from_to_sint16, SIDETIP="cents")

promotion_rule = QStruct("promotion_rule",
    SInt16("pitch_range_index"),
    SInt16("maximum_playing_count"),
    Float("supression_time"),
    SInt32("unknown0"),
    SInt32("unknown1"),
    SIZE=16
    )

promotion_runtime_timer = QStruct("runtime_timer", UInt32("unknown"), SIZE=4)

sound_dialogue_info = Struct("sound_dialogue_info",
    UInt32("mouth_data_offset"),
    UInt32("mouth_data_size"),
    UInt32("lipsync_data_offset"),
    UInt32("lipsync_data_size"),
    SIZE=16
    )

# in a map, this struct is contained in a resource block with the
# rawdata of the encoded_data and the reflexive structs of the
# sound_dialogue_infos each following in their own resource section.
# it looks like this:
#
# UInt32("blkh_sig")
#     UInt32("rsrc_section_size")
#     encoded_permutation_section_header
#     UInt32("rsrc_sig")
#         BytesRaw("encoded_data")
#
#     UInt32("rsrc_sig")
#         BytesRaw("sound_dialogue_info_array")
#
# UInt32("blkf_sig")
#
encoded_permutation_section = Struct("encoded_permutation_section",
    h2_rawdata_ref("encoded_data"),
    h2_reflexive("sound_dialogue_infos", sound_dialogue_info),
    SIZE=16
    )

filter_bounds = Struct("resource",
    QStruct("scale_bounds", INCLUDE=from_to_float),
    Float("random_base"),
    Float("random_variance"),
    SIZE=16
    )

custom_playback_filter = Struct("filter",
    UEnum32("filter_type",
        "both",
        "dls2",
        "parametric_eq",
        ),
    SInt32("filter_width", SIDETIP="[0,7]"),
    Struct("left_filter_frequency",  INCLUDE=filter_bounds),
    Struct("left_filter_gain",       INCLUDE=filter_bounds),
    Struct("right_filter_frequency", INCLUDE=filter_bounds),
    Struct("right_filter_gain",      INCLUDE=filter_bounds),
    SIZE=72
    )

custom_playback_pitch_lfo = Struct("pitch_lfo")

custom_playback_filter_lfo = Struct("filter_lfo")

playback_parameter = Struct("playback_parameter",
    from_to_wu("distance_bounds"),
    float_zero_to_one("skip_fraction"),
    Float("maximum_bend_per_second", SIDETIP="cents"),

    Struct("randomization",
        Float("gain_base"),
        Float("gain_variance"),
        QStruct("random_pitch_bounds", INCLUDE=from_to_cents),
        ),
    Struct("directional_sounds",
        float_rad("inner_cone_angle"),
        float_rad("outer_cone_angle"),
        Float("outer_cone_gain", SIDETIP="dB"),
        ),
    Struct("scripted_location_override",
        Bool32("flags",
            "override_azimuth",
            "override_3d_gain",
            "override_speaker_gain",
            ),
        Float("azimuth"),
        Float("positional_gain", SIDETIP="dB"),
        Float("first_person_gain", SIDETIP="dB"),
        ),
    SIZE=56
    )

playback_scale = Struct("playback_scale",
    QStruct("gain_modifier", INCLUDE=from_to_float),
    QStruct("pitch_modifier", INCLUDE=from_to_sint16),
    QStruct("skip_fraction_modifier", INCLUDE=from_to_float),
    SIZE=20
    )

import_name = h2_string_id("import_name")

pitch_range_parameter = Struct("pitch_range_parameter",
    SInt16("natural_pitch"),
    QStruct("bend_bounds", INCLUDE=from_to_sint16),
    QStruct("max_gain_pitch_bounds", INCLUDE=from_to_sint16),
    SIZE=10
    )

pitch_range = QStruct("pitch_range",
    SInt16("import_name_index"),
    SInt16("pitch_range_parameter_index"),
    SInt16("encoded_permutation_data_index"),
    SInt16("encoded_runtime_permutation_flag_index"),
    SInt16("first_permutation"),
    SInt16("permutation_count"),
    SIZE=12
    )

permutation = QStruct("permutation",
    SInt16("import_name_index"),
    SInt16("encoded_skip_fraction"),
    SInt8("encoded_gain"),
    SInt8("permutation_info_index"),  # what is this?
    SInt16("language_neutral_time"),
    SInt32("sample_size"),
    SInt16("first_chunk"),
    SInt16("chunk_count"),
    SIZE=16
    )

custom_playback = Struct("custom_playback",
    UInt32("unknown0"),
    UInt32("unknown1"),
    Bool32("flags",
        "use_3d_radio_hack"
        ),
    UInt32("unknown2"),
    UInt32("unknown3"),
    h2_reflexive("filter", custom_playback_filter),
    h2_reflexive("pitch_lfo", custom_playback_pitch_lfo),
    h2_reflexive("filter_lfo", custom_playback_filter_lfo),
    UInt32("unknown4"),
    SIZE=52
    )

runtime_permutation_flag = QStruct("runtime_permutation_flag",
    UInt8("flags"),
    SIZE=1
    )

permutation_chunk = Struct("permutation_chunk",
    UInt32("pointer"),
    UInt24("size"),  # this uses AT LEAST 3 bytes
    UInt8("flags"),  # sometimes some upper bits are set, which
    #                  would make it add gigabytes of size if
    #                  this were part of the "size" attribute.
    #                  i believe the upper byte is for flags.
    SInt32("runtime_index"),
    SIZE=12
    )

promotion = Struct("promotion",
    h2_reflexive("rules", promotion_rule, 32767),
    h2_reflexive("runtime_timers", promotion_runtime_timer),
    Pad(12),
    SIZE=28
    )

extra_info = Struct("extra_info",
    BytesRaw("unknown0", SIZE=8, VISIBLE=False),
    QStruct("encoded_permutation_section",
        UInt32("block_offset"),
        UInt32("block_size"),
        UInt32("section_data_size"),
        UInt32("resource_data_size"),
        ),
    h2_reflexive("resources", resource),
    dependency_uint32("sound_gestalt"), # points back to this tag?
    SInt32("constant0", VISIBLE=False),
    SInt32("constant1", VISIBLE=False),
    SIZE=44
    )

ugh__body = Struct("tagdata",
    h2_reflexive("playback_parameters", playback_parameter, 32767),
    h2_reflexive("scales",       playback_scale,     32767),
    h2_reflexive("import_names", import_name,        32767),
    h2_reflexive("pitch_range_parameters", pitch_range_parameter, 32767),
    h2_reflexive("pitch_ranges", pitch_range, 32767),
    h2_reflexive("permutations", permutation, 32767),
    h2_reflexive("custom_playbacks",   custom_playback,   127),
    h2_reflexive("runtime_permutation_flags", runtime_permutation_flag, 32767),
    h2_reflexive("permutation_chunks", permutation_chunk, 32767),
    h2_reflexive("promotions",  promotion,  127),
    h2_reflexive("extra_infos", extra_info, 32767),
    ENDIAN="<", SIZE=88
    )


def get():
    return ugh__def

ugh__def = TagDef("ugh!",
    h2_blam_header('ugh!'),
    ugh__body,

    ext=".%s" % h2_tag_class_fcc_to_ext["ugh!"], endian="<"
    )
