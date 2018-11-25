from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


snmx_meta_def = BlockDef("snmx",
    Float("left_stereo_gain"),
    Float("right_stereo_gain"),
    Float("left_stereo_gain_1"),
    Float("right_stereo_gain_1"),
    Float("left_stereo_gain_2"),
    Float("right_stereo_gain_2"),
    Float("front_speaker_gain"),
    Float("rear_speaker_gain"),
    Float("front_speaker_gain_1"),
    Float("rear_speaker_gain_1"),
    Float("mono_unspatialized_gain"),
    Float("stereo_to_3d_gain"),
    Float("rear_surround_to_front_stereo_gain"),
    Float("front_speaker_gain_2"),
    Float("center_speaker_gain"),
    Float("front_speaker_gain_3"),
    Float("center_speaker_gain_1"),
    Float("stereo_unspatialized_gain"),
    Float("solo_player_fade_out_delay"),
    Float("solo_player_fade_out_time"),
    Float("solo_player_fade_in_time"),
    Float("game_music_fade_out_time"),
    dependency("unknown"),
    Float("unknown_1"),
    Float("unknown_2"),
    TYPE=Struct, ENDIAN=">", SIZE=112
    )