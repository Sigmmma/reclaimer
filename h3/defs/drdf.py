############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/11/30  01:44
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
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef


drdf_response = Struct("response", 
    SEnum16("response_type", *jpt__player_response_response_type),
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
    Array("unknown_array_0", SIZE=4, SUB_STRUCT=Float("unknown"), VISIBLE=False),
    SInt16("unknown_10", VISIBLE=False),
    SInt16("unknown_11", VISIBLE=False),
    Array("unknown_array_1", SIZE=7, SUB_STRUCT=Float("unknown"), VISIBLE=False),
    Float("low_frequency_vibration_duration"),
    h3_rawdata_ref("low_frequency_vibration_function"),
    Float("high_frequency_vibration_duration"),
    h3_rawdata_ref("high_frequency_vibration_function"),
    Float("duration_0"),
    SEnum16("fade_function", *jpt__player_response_fade_function),
    SInt16("unknown_12", VISIBLE=False),
    float_rad("rotation"),
    Float("pushback"),
    QStruct("jitter", INCLUDE=from_to),
    Float("duration_1"),
    SEnum16("falloff_function", *jpt__player_response_fade_function),
    SInt16("unknown_13", VISIBLE=False),
    Float("random_translation"),
    float_rad("random_rotation"),
    SEnum16("wobble_function", *jpt__wobble_function),
    SInt16("unknown_14", VISIBLE=False),
    Float("wobble_function_period"),
    Float("wobble_weight"),
    ENDIAN=">", SIZE=192
    )


drdf_meta_def = BlockDef("drdf", 
    h3_reflexive("responses", drdf_response),
    TYPE=Struct, ENDIAN=">", SIZE=12
    )