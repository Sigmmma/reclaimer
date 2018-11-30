############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/11/30  01:44
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef


trak_camera_point = Struct("camera_point", 
    QStruct("position", INCLUDE=ijk_float, VISIBLE=False),
    QStruct("orientation", INCLUDE=ijkw_float, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=28
    )


trak_meta_def = BlockDef("trak", 
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    h3_reflexive("camera_points", trak_camera_point),
    TYPE=Struct, ENDIAN=">", SIZE=16
    )