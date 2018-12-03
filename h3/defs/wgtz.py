############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
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
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


wgtz_screen_widget = Struct("screen_widget", 
    h3_dependency("widget"),
    ENDIAN=">", SIZE=16
    )


wgtz_body = Struct("tagdata", 
    h3_dependency("shared_ui_globals"),
    h3_dependency("editable_settings"),
    h3_dependency("matchmaking_hopper_strings"),
    h3_reflexive("screen_widgets", wgtz_screen_widget),
    ENDIAN=">", SIZE=60
    )


def get():
    return wgtz_def

wgtz_def = TagDef("wgtz",
    h3_blam_header('wgtz'),
    wgtz_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["wgtz"], endian=">", tag_cls=H3Tag
    )