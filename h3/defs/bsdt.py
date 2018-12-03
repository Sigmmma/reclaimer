############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: -DeToX-
# 	Created layout of plugin
# revision: 2		author: DeadCanadian
# 	naming tags
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


bsdt_unknown0 = Struct("unknown0", 
    BytesRaw("unknown_0", SIZE=8, VISIBLE=False),
    h3_rawdata_ref("unknown_1", VISIBLE=False),
    BytesRaw("unknown_2", SIZE=8, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=36
    )


bsdt_unknown1 = Struct("unknown1", 
    BytesRaw("unknown_0", SIZE=8, VISIBLE=False),
    h3_rawdata_ref("unknown_1", VISIBLE=False),
    BytesRaw("unknown_2", SIZE=8, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=36
    )


bsdt_body = Struct("tagdata", 
    Float("maximum_vitality"),
    h3_dependency("effect"),
    h3_dependency("sound"),
    BytesRaw("unknown_0", SIZE=16, VISIBLE=False),
    h3_dependency("crack_bitmap"),
    h3_dependency("hole_bitmap"),
    BytesRaw("unknown_1", SIZE=36, VISIBLE=False),
    h3_reflexive("unknown0", bsdt_unknown0),
    BytesRaw("unknown_2", SIZE=12, VISIBLE=False),
    h3_reflexive("unknown1", bsdt_unknown1),
    BytesRaw("unknown_3", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=160
    )


def get():
    return bsdt_def

bsdt_def = TagDef("bsdt",
    h3_blam_header('bsdt'),
    bsdt_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["bsdt"], endian=">", tag_cls=H3Tag
    )