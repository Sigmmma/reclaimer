############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: DeadCanadian
# 	item types... for the ones i could figure out
# revision: 3		author: Lord Zedd
# 	h2 port
# revision: 4		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


_fx__additional_sound_input = Struct("additional_sound_input", 
    h3_string_id("dsp_effect"),
    h3_rawdata_ref("low_frequency_sound_function"),
    Float("time_period"),
    ENDIAN=">", SIZE=28
    )


_fx__body = Struct("tagdata", 
    BytesRaw("template_collection_block", SIZE=12, VISIBLE=False),
    SInt32("input_effect_name"),
    h3_reflexive("additional_sound_inputs", _fx__additional_sound_input),
    ENDIAN=">", SIZE=28
    )


def get():
    return _fx__def


_fx__def = TagDef("<fx>",
    h3_blam_header('<fx>'),
    _fx__body,

    ext=".%s" % h3_tag_class_fcc_to_ext["<fx>"], endian=">", tag_cls=H3Tag
    )
