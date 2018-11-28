############# Credits and version info #############
# Definition autogenerated from Assembly XML tag def
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: OrangeMohawk
# 	Rumble/Camera Shake from RMBL/CSDT
# revision: 3		author: Lord Zedd
# 	Updating and standardizing
# revision: 4		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################
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


drdf_response = Struct("response", 
    SEnum16("response_type", *drdf_response_response_type),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    SInt16("unknown_2", VISIBLE=False),
    BytesRaw("unknown_3", SIZE=12, VISIBLE=False),
    Float("unknown_4", VISIBLE=False),
    BytesRaw("unknown_5", SIZE=8, VISIBLE=False),
    Float("unknown_6", VISIBLE=False),
    Float("unknown_7", VISIBLE=False),
    SInt16("unknown_8", VISIBLE=False),
    SInt16("unknown_9", VISIBLE=False),
    Array("unknown_array_0", SUB_STRUCT=Float("unknown"), SIZE=4, VISIBLE=False),
    SInt16("unknown_10", VISIBLE=False),
    SInt16("unknown_11", VISIBLE=False),
    Array("unknown_array_1", SUB_STRUCT=Float("unknown"), SIZE=7, VISIBLE=False),
    Float("low_frequency_vibration_duration"),
    rawdata_ref("low_frequency_vibration_function"),
    Float("high_frequency_vibration_duration"),
    rawdata_ref("high_frequency_vibration_function"),
    Float("duration_0"),
    SEnum16("fade_function", *drdf_response_fade_function),
    SInt16("unknown_12", VISIBLE=False),
    float_rad("rotation"),
    Float("pushback"),
    QStruct("jitter", INCLUDE=from_to),
    Float("duration_1"),
    SEnum16("falloff_function", *drdf_response_fade_function),
    SInt16("unknown_13", VISIBLE=False),
    Float("random_translation"),
    float_rad("random_rotation"),
    SEnum16("wobble_function", *drdf_response_wobble_function),
    SInt16("unknown_14", VISIBLE=False),
    Float("wobble_function_period"),
    Float("wobble_weight"),
    ENDIAN=">", SIZE=192
    )


drdf_meta_def = BlockDef("drdf", 
    reflexive("responses", drdf_response),
    TYPE=Struct, ENDIAN=">", SIZE=12
    )