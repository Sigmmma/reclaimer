############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/11/30  01:44
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: -DeToX-
# 	Labelled Raw Identifier
# revision: 3		author: Xerax
# 	
# revision: 4		author: Lord Zedd
# 	Standardized
# revision: 5		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef


snd__meta_def = BlockDef("snd_", 
    Bool16("flags", 
        "fit_to_adpcm_blocksize",
        "split_long_sound_into_permutations",
        ),
    SEnum8("sound_class", *snd__sound_class),
    SInt8("unknown_0"),
    SInt16("ugh_platform_codec_index"),
    SInt16("ugh_pitch_range_index"),
    SInt16("ugh_language_b_index"),
    SInt16("unknown_1", VISIBLE=False),
    SInt16("ugh_playback_parameter_index"),
    SInt16("ugh_scale_index"),
    SInt8("ugh_promotion_index"),
    SInt8("ugh_custom_playback_index"),
    SInt16("ugh_extra_info_index"),
    SInt32("unknown_2", VISIBLE=False),
    UInt16("zone_asset_salt"),
    UInt16("zone_asset_index"),
    SInt32("useless_padding", VISIBLE=False),
    TYPE=Struct, ENDIAN=">", SIZE=32
    )