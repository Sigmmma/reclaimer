############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/11/30  01:44
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: DarkShallFall
# 	Easy enough...
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef


wgtz_screen_widget = Struct("screen_widget", 
    h3_dependency("widget"),
    ENDIAN=">", SIZE=16
    )


wgtz_meta_def = BlockDef("wgtz", 
    h3_dependency("shared_ui_globals"),
    h3_dependency("editable_settings"),
    h3_dependency("matchmaking_hopper_strings"),
    h3_reflexive("screen_widgets", wgtz_screen_widget),
    TYPE=Struct, ENDIAN=">", SIZE=60
    )