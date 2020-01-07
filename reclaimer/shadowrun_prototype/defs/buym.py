#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return buym_def

buym_def = TagDef("buym",
    blam_header('buym'),
    Struct('tagdata',
        dependency("forward", "snd!"),
        dependency("back", "snd!"),
        dependency("click_1", "snd!"),
        dependency("click_2", "snd!"),
        dependency("click_3", "snd!"),
        dependency("click_4", "snd!"),
        dependency("sound_7", "snd!"),
        dependency("cursor", "snd!"),
        dependency("sound_9", "snd!"),
        dependency("sound_10", "snd!"),
        dependency("sound_11", "snd!"),
        dependency("sound_12", "snd!"),
        dependency("sound_13", "snd!"),
        dependency("sound_14", "snd!"),
        dependency("sound_15", "snd!"),
        dependency("sound_16", "snd!"),
        dependency("sound_17", "snd!"),
        dependency("sound_18", "snd!"),
        dependency("sound_19", "snd!"),
        dependency("sound_20", "snd!"),
        dependency("select_magic", "snd!"),
        dependency("select_tech", "snd!"),
        dependency("assign_magic", "snd!"),
        dependency("assign_tech", "snd!"),
        dependency("sound_25", "snd!"),

        Pad(1344),

        dependency("sound_26", "snd!"),
        dependency("sound_27", "snd!"),
        dependency("sound_28", "snd!"),
        dependency("sound_29", "snd!"),
        SIZE=2000,
        ),

    ext=".buy_menu", endian=">"
    )
