############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


crte_unknown_6_unknown_0 = Struct("unknown_0", 
    BytesRaw("unknown", SIZE=32, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=32
    )


crte_unknown_6_unknown_1_unknown_1_unknown_0 = Struct("unknown_0", 
    BytesRaw("unknown", SIZE=16, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


crte_unknown_6_unknown_1_unknown_1 = Struct("unknown_1", 
    h3_reflexive("unknown_0", crte_unknown_6_unknown_1_unknown_1_unknown_0),
    h3_rawdata_ref("unknown_1", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=32
    )


crte_unknown_6_unknown_1 = Struct("unknown_1", 
    BytesRaw("unknown_0", SIZE=28, VISIBLE=False),
    h3_reflexive("unknown_1", crte_unknown_6_unknown_1_unknown_1),
    VISIBLE=False,
    ENDIAN=">", SIZE=40
    )


crte_unknown_6 = Struct("unknown_6", 
    h3_reflexive("unknown_0", crte_unknown_6_unknown_0),
    h3_reflexive("unknown_1", crte_unknown_6_unknown_1),
    VISIBLE=False,
    ENDIAN=">", SIZE=24
    )


crte_unknown_7_unknown_0_unknown_1_unknown_0 = Struct("unknown_0", 
    BytesRaw("unknown", SIZE=16, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


crte_unknown_7_unknown_0_unknown_1 = Struct("unknown_1", 
    h3_reflexive("unknown_0", crte_unknown_7_unknown_0_unknown_1_unknown_0),
    h3_rawdata_ref("unknown_1", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=32
    )


crte_unknown_7_unknown_0 = Struct("unknown_0", 
    BytesRaw("unknown_0", SIZE=28, VISIBLE=False),
    h3_reflexive("unknown_1", crte_unknown_7_unknown_0_unknown_1),
    BytesRaw("unknown_2", SIZE=12, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=52
    )


crte_unknown_7_unknown_1 = Struct("unknown_1", 
    BytesRaw("unknown", SIZE=52, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=52
    )


crte_unknown_7_unknown_2_unknown_1_unknown_0 = Struct("unknown_0", 
    BytesRaw("unknown", SIZE=12, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=12
    )


crte_unknown_7_unknown_2_unknown_1 = Struct("unknown_1", 
    h3_reflexive("unknown_0", crte_unknown_7_unknown_2_unknown_1_unknown_0),
    h3_rawdata_ref("unknown_1", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=32
    )


crte_unknown_7_unknown_2 = Struct("unknown_2", 
    BytesRaw("unknown_0", SIZE=24, VISIBLE=False),
    h3_reflexive("unknown_1", crte_unknown_7_unknown_2_unknown_1),
    BytesRaw("unknown_2", SIZE=12, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=48
    )


crte_unknown_7_unknown_3_unknown_1_unknown_0 = Struct("unknown_0", 
    BytesRaw("unknown", SIZE=16, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


crte_unknown_7_unknown_3_unknown_1 = Struct("unknown_1", 
    h3_reflexive("unknown_0", crte_unknown_7_unknown_3_unknown_1_unknown_0),
    h3_rawdata_ref("unknown_1", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=32
    )


crte_unknown_7_unknown_3 = Struct("unknown_3", 
    BytesRaw("unknown_0", SIZE=28, VISIBLE=False),
    h3_reflexive("unknown_1", crte_unknown_7_unknown_3_unknown_1),
    BytesRaw("unknown_2", SIZE=12, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=52
    )


crte_unknown_7 = Struct("unknown_7", 
    h3_reflexive("unknown_0", crte_unknown_7_unknown_0),
    h3_reflexive("unknown_1", crte_unknown_7_unknown_1),
    h3_reflexive("unknown_2", crte_unknown_7_unknown_2),
    h3_reflexive("unknown_3", crte_unknown_7_unknown_3),
    VISIBLE=False,
    ENDIAN=">", SIZE=48
    )


crte_unknown_9_unknown_0 = Struct("unknown_0", 
    BytesRaw("unknown", SIZE=48, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=48
    )


crte_unknown_9_unknown_1_unknown_1_unknown_0 = Struct("unknown_0", 
    BytesRaw("unknown", SIZE=16, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


crte_unknown_9_unknown_1_unknown_1 = Struct("unknown_1", 
    h3_reflexive("unknown_0", crte_unknown_9_unknown_1_unknown_1_unknown_0),
    h3_rawdata_ref("unknown_1", VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=32
    )


crte_unknown_9_unknown_1 = Struct("unknown_1", 
    BytesRaw("unknown_0", SIZE=28, VISIBLE=False),
    h3_reflexive("unknown_1", crte_unknown_9_unknown_1_unknown_1),
    BytesRaw("unknown_2", SIZE=12, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=52
    )


crte_unknown_9_unknown_2 = Struct("unknown_2", 
    BytesRaw("unknown", SIZE=12, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=12
    )


crte_unknown_9 = Struct("unknown_9", 
    h3_reflexive("unknown_0", crte_unknown_9_unknown_0),
    h3_reflexive("unknown_1", crte_unknown_9_unknown_1),
    h3_reflexive("unknown_2", crte_unknown_9_unknown_2),
    VISIBLE=False,
    ENDIAN=">", SIZE=36
    )


crte_body = Struct("tagdata", 
    h3_string_id("unknown_0", VISIBLE=False),
    BytesRaw("unknown_1", SIZE=16, VISIBLE=False),
    h3_rawdata_ref("unknown_2", VISIBLE=False),
    h3_rawdata_ref("unknown_3", VISIBLE=False),
    h3_dependency("unknown_4", VISIBLE=False),
    h3_string_id("unknown_5", VISIBLE=False),
    h3_reflexive("unknown_6", crte_unknown_6),
    h3_reflexive("unknown_7", crte_unknown_7),
    BytesRaw("unknown_8", SIZE=12, VISIBLE=False),
    h3_reflexive("unknown_9", crte_unknown_9),
    ENDIAN=">", SIZE=128
    )


def get():
    return crte_def

crte_def = TagDef("crte",
    h3_blam_header('crte'),
    crte_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["crte"], endian=">", tag_cls=H3Tag
    )