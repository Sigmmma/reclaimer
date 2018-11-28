############# Credits and version info #############
# Definition autogenerated from Assembly XML tag def
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
from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


wgan_meta_def = BlockDef("wgan", 
    string_id_meta("unknown_0"),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    dependency("widget_color"),
    dependency("widget_position"),
    dependency("widget_rotation"),
    dependency("widget_scale"),
    dependency("widget_texture_coordinate"),
    dependency("widget_sprite"),
    dependency("widget_font"),
    TYPE=Struct, ENDIAN=">", SIZE=120
    )