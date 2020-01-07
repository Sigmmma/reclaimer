#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

scale_comment = """DETAIL SOUND PERIOD SCALING
As the sound's input scale changes from zero to one, these modifiers move between
the two values specified here. The sound will play using the current scale modifier
multiplied by the value specified below. (0 values are ignored.)"""

random_spatialisation_comment = """RANDOM SPATIALIZATION
If the sound specified above is not stereo it will be randomly spatialized according
to the following contraints. If both lower and upper bounds are zero for any of
the following fields, the sound's position will be randomly selected from
all the possible directions or distances."""

detail_sound = Struct("detail_sound",
    dependency("sound", "snd!"),
    from_to_sec('random_period_bounds'),
    Float("gain"),
    Bool32("flags",
        "dont_play_with_alternate",
        "dont_play_without_alternate",
        ),

    Pad(48),
    from_to_rad('yaw_bounds', COMMENT=random_spatialisation_comment),  # radians
    from_to_rad('pitch_bounds'),  # radians
    from_to_wu('distance_bounds'),  # world units

    SIZE=104
    )

track = Struct("track",
    Bool32("flags",
        "fade_in_at_start",
        "fade_out_at_stop",
        "fade_in_alternate",
        ),
    Float("gain"),
    float_sec("fade_in_duration"),
    float_sec("fade_out_duration"),

    Pad(32),
    dependency("start", "snd!"),
    dependency("loop", "snd!"),
    dependency("end", "snd!"),

    Pad(32),
    dependency("alternate_loop", "snd!"),
    dependency("alternate_end", "snd!"),
    SIZE=160
    )


lsnd_body = Struct("tagdata",
    Bool32("flags",
        "deafening_to_ai",
        "not_a_loop",
        "stops_music",
        ),
    Float("detail_sound_period_at_zero", COMMENT=scale_comment),
    FlFloat("unknown0", DEFAULT=1.0, VISIBLE=False),
    FlFloat("unknown1", DEFAULT=1.0, VISIBLE=False),
    Float("detail_sound_period_at_one"),
    FlFloat("unknown2", DEFAULT=1.0, VISIBLE=False),
    FlFloat("unknown3", DEFAULT=1.0, VISIBLE=False),
    FlSInt16("unknown4", DEFAULT=-1, VISIBLE=False),
    FlSInt16("unknown5", DEFAULT=-1, VISIBLE=False),
    FlFloat("unknown6", DEFAULT=1.0, VISIBLE=False),
    Pad(8),
    dependency("continuous_damage_effect", "cdmg"),

    reflexive("tracks", track, 4),
    reflexive("detail_sounds", detail_sound, 32,
        DYN_NAME_PATH='.sound.filepath'),

    SIZE=84,
    )


def get():
    return lsnd_def

lsnd_def = TagDef("lsnd",
    blam_header("lsnd", 3),
    lsnd_body,

    ext=".sound_looping", endian=">", tag_cls=HekTag,
    )
