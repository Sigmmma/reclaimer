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
# revision: 2		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef

lsnd_track_output_effect = (
    "none",
    "output_front_speakers",
    "output_rear_speakers",
    "output_center_speakers",
    )


lsnd_track = Struct("track",
    h3_string_id("name"),
    Bool32("flags",
        "fade_in_at_start",
        "fade_out_at_stop",
        ),
    Float("gain"),
    Float("fade_in_duration"),
    Float("fade_out_duration"),
    h3_dependency("in"),
    h3_dependency("loop"),
    h3_dependency("out"),
    h3_dependency("alternate_loop"),
    h3_dependency("alternate_out"),
    SEnum16("output_effect", *lsnd_track_output_effect),
    SInt16("unknown", VISIBLE=False),
    h3_dependency("alternate_transition_in"),
    h3_dependency("alternate_transition_out"),
    Float("alternate_crossfade_duration"),
    Float("alternate_fade_out_duration"),
    ENDIAN=">", SIZE=144
    )


lsnd_detail_sound = Struct("detail_sound",
    h3_string_id("name"),
    h3_dependency("sound"),
    QStruct("random_period_bounds", INCLUDE=from_to),
    Float("unknown", VISIBLE=False),
    Bool32("flags",
        "dont_play_with_alternate",
        "dont_play_without_alternate",
        "start_immediately_with_loop",
        ),
    from_to_rad("yaw_bounds"),
    from_to_rad("pitch_bounds"),
    QStruct("distance_bounds", INCLUDE=from_to),
    ENDIAN=">", SIZE=60
    )


lsnd_body = Struct("tagdata",
    Bool32("flags",
        "deafening_to_ais",
        "not_a_loop",
        "stops_music",
        "always_spatialize",
        "synchronize_playback",
        "synchronize_tracks",
        "fake_spatialization_with_distance",
        "combine_all_3d_playback",
        ),
    Float("marty_s_music_time"),
    Float("unknown_0", VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    h3_dependency("unused"),
    SEnum16("sound_class", *snd__sound_class),
    SInt16("unknown_3", VISIBLE=False),
    h3_reflexive("tracks", lsnd_track),
    h3_reflexive("detail_sounds", lsnd_detail_sound),
    ENDIAN=">", SIZE=64
    )


def get():
    return lsnd_def

lsnd_def = TagDef("lsnd",
    h3_blam_header('lsnd'),
    lsnd_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["lsnd"], endian=">", tag_cls=H3Tag
    )
