#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: Lord Zedd
# 	Copypasta H2
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


snmx_body = Struct("tagdata",
    Float("left_stereo_gain_0"),
    Float("right_stereo_gain_0"),
    Float("left_stereo_gain_1"),
    Float("right_stereo_gain_1"),
    Float("left_stereo_gain_2"),
    Float("right_stereo_gain_2"),
    Float("front_speaker_gain_0"),
    Float("rear_speaker_gain_0"),
    Float("front_speaker_gain_1"),
    Float("rear_speaker_gain_1"),
    Float("mono_unspatialized_gain"),
    Float("stereo_to_3d_gain"),
    Float("rear_surround_to_front_stereo_gain"),
    Float("front_speaker_gain_2"),
    Float("center_speaker_gain_0"),
    Float("front_speaker_gain_3"),
    Float("center_speaker_gain_1"),
    Float("stereo_unspatialized_gain"),
    Float("solo_player_fade_out_delay"),
    Float("solo_player_fade_out_time"),
    Float("solo_player_fade_in_time"),
    Float("game_music_fade_out_time"),
    h3_dependency("unknown_0"),
    Float("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    ENDIAN=">", SIZE=112
    )


def get():
    return snmx_def

snmx_def = TagDef("snmx",
    h3_blam_header('snmx'),
    snmx_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["snmx"], endian=">", tag_cls=H3Tag
    )
