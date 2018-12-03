############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: -DeToX-
# 	Created layout of plugin
# revision: 2		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


flck_body = Struct("tagdata", 
    Pad(64),
    float_rad("perception_angle"),
    Pad(24),
    ENDIAN=">", SIZE=92
    )


def get():
    return flck_def

flck_def = TagDef("flck",
    h3_blam_header('flck'),
    flck_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["flck"], endian=">", tag_cls=H3Tag
    )