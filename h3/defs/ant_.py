############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: DeadCanadian
# 	named the tags and Verticies
# revision: 3		author: Lord Zedd
# 	port h2
# revision: 4		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


ant__vertice = Struct("vertice", 
    yp_float_rad("angle"),
    Float("length"),
    SInt16("sequence_index"),
    SInt16("unknown", VISIBLE=False),
    color_argb_float("color"),
    color_argb_float("lod_color"),
    Pad(16),
    ENDIAN=">", SIZE=64
    )


ant__body = Struct("tagdata", 
    h3_string_id("attachment_marker_name"),
    h3_dependency("bitmaps"),
    h3_dependency("physics"),
    BytesRaw("unknown", SIZE=28, VISIBLE=False),
    h3_reflexive("vertices", ant__vertice),
    ENDIAN=">", SIZE=76
    )


def get():
    return ant__def

ant__def = TagDef("ant!",
    h3_blam_header('ant!'),
    ant__body,

    ext=".%s" % h3_tag_class_fcc_to_ext["ant!"], endian=">", tag_cls=H3Tag
    )