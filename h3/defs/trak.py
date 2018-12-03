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


trak_camera_point = Struct("camera_point", 
    QStruct("position", INCLUDE=ijk_float, VISIBLE=False),
    QStruct("orientation", INCLUDE=ijkw_float, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=28
    )


trak_body = Struct("tagdata", 
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    h3_reflexive("camera_points", trak_camera_point),
    ENDIAN=">", SIZE=16
    )


def get():
    return trak_def

trak_def = TagDef("trak",
    h3_blam_header('trak'),
    trak_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["trak"], endian=">", tag_cls=H3Tag
    )