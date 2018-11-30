############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/11/30  01:44
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: DarkShallFall
# 	Idents labled.
# revision: 3		author: Lord Zedd
# 	Basically done.
# revision: 4		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef


wgan_meta_def = BlockDef("wgan", 
    h3_string_id("unknown_0"),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    h3_dependency("widget_color"),
    h3_dependency("widget_position"),
    h3_dependency("widget_rotation"),
    h3_dependency("widget_scale"),
    h3_dependency("widget_texture_coordinate"),
    h3_dependency("widget_sprite"),
    h3_dependency("widget_font"),
    TYPE=Struct, ENDIAN=">", SIZE=120
    )