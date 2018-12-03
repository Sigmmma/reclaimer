############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: Lord Zedd
# 	Updated and standardized.
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


uise_body = Struct("tagdata", 
    h3_dependency("error"),
    h3_dependency("vertical_navigation"),
    h3_dependency("horizontal_navigation"),
    h3_dependency("a_button"),
    h3_dependency("b_button"),
    h3_dependency("x_button"),
    h3_dependency("y_button"),
    h3_dependency("start_button"),
    h3_dependency("back_button"),
    h3_dependency("left_bumper"),
    h3_dependency("right_bumper"),
    h3_dependency("left_trigger"),
    h3_dependency("right_trigger"),
    h3_dependency("timer_sound"),
    h3_dependency("timer_sound_zero"),
    h3_dependency("alt_timer_sound"),
    h3_dependency("second_alt_timer_sound"),
    h3_dependency("matchmaking_advance_sound"),
    h3_dependency("rank_up"),
    h3_dependency("matchmaking_party_up_sound"),
    ENDIAN=">", SIZE=320
    )


def get():
    return uise_def

uise_def = TagDef("uise",
    h3_blam_header('uise'),
    uise_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["uise"], endian=">", tag_cls=H3Tag
    )