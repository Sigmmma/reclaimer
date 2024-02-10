#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.lsnd import *

lsnd_flags = Bool32("flags",
    "deafening_to_ai",
    "not_a_loop",
    "stops_music",
    "siege_of_the_madrigal",
    )

lsnd_body = desc_variant(lsnd_body, lsnd_flags)

def get():
    return lsnd_def

lsnd_def = TagDef("lsnd",
    blam_header("lsnd", 3),
    lsnd_body,

    ext=".sound_looping", endian=">", tag_cls=HekTag,
    )
