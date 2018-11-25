from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


uise_meta_def = BlockDef("uise",
    dependency("error"),
    dependency("vertical_navigation"),
    dependency("horizontal_navigation"),
    dependency("a_button"),
    dependency("b_button"),
    dependency("x_button"),
    dependency("y_button"),
    dependency("start_button"),
    dependency("back_button"),
    dependency("left_bumper"),
    dependency("right_bumper"),
    dependency("left_trigger"),
    dependency("right_trigger"),
    dependency("timer_sound"),
    dependency("timer_sound_zero"),
    dependency("alt_timer_sound"),
    dependency("second_alt_timer_sound"),
    dependency("matchmaking_advance_sound"),
    dependency("rank_up"),
    dependency("matchmaking_party_up_sound"),
    TYPE=Struct, ENDIAN=">", SIZE=320
    )