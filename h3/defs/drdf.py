from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

drdf_response_fade_function = (
    "linear",
    "late",
    "very_late",
    "early",
    "very_early",
    "cosine",
    "zero",
    "one",
    )

drdf_response_response_type = (
    "shielded",
    "unshielded",
    "all",
    )

drdf_response_wobble_function = (
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


drdf_response = Struct("responses",
    SEnum16("response_type", *drdf_response_response_type),
    SInt16("unknown"),
    SInt16("unknown_1"),
    SInt16("unknown_2"),
    Pad(12),
    Float("unknown_4"),
    Pad(8),
    Float("unknown_6"),
    Float("unknown_7"),
    SInt16("unknown_8"),
    SInt16("unknown_9"),
    Float("unknown_10"),
    Float("unknown_11"),
    Float("unknown_12"),
    Float("unknown_13"),
    SInt16("unknown_14"),
    SInt16("unknown_15"),
    Float("unknown_16"),
    Float("unknown_17"),
    Float("unknown_18"),
    Float("unknown_19"),
    Float("unknown_20"),
    Float("unknown_21"),
    Float("unknown_22"),
    Float("low_frequency_vibration_duration"),
    rawdata_ref("low_frequency_vibration_function"),
    Float("high_frequency_vibration_duration"),
    rawdata_ref("high_frequency_vibration_function"),
    Float("duration"),
    SEnum16("fade_function", *drdf_response_fade_function),
    SInt16("unknown_23"),
    float_rad("rotation"),
    Float("pushback"),
    Float("jitter_min"),
    Float("jitter_max"),
    Float("duration_1"),
    SEnum16("falloff_function", *drdf_response_fade_function),
    SInt16("unknown_24"),
    Float("random_translation"),
    float_rad("random_rotation"),
    SEnum16("wobble_function", *drdf_response_wobble_function),
    SInt16("unknown_25"),
    Float("wobble_function_period"),
    Float("wobble_weight"),
    ENDIAN=">", SIZE=192
    )


drdf_meta_def = BlockDef("drdf",
    reflexive("responses", drdf_response),
    TYPE=Struct, ENDIAN=">", SIZE=12
    )