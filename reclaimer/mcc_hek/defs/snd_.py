#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.snd_ import *
from supyr_struct.util import desc_variant


mcc_snd__flags = Bool32("flags",
    "fit_to_adpcm_blocksize",
    "split_long_sound_into_permutations",
    "thirsty_grunt",
    )

mcc_snd__body = desc_variant(snd__body,
    ("flags", mcc_snd__flags),
    )


def get():
    return snd__def

snd__def = TagDef("snd!",
    blam_header('snd!', 4),
    mcc_snd__body,

    ext=".sound", endian=">", tag_cls=Snd_Tag,
    )

snd__meta_stub = desc_variant(
    mcc_snd__body, ("pitch_ranges", Pad(12))
    )
snd__meta_stub_blockdef = BlockDef(snd__meta_stub)
