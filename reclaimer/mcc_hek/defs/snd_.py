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
# found from sapien error log:
#   EXCEPTION halt in c:\mcc\qfe1\h1\code\h1a2\sources\cache\pc_sound_cache.c,#157: !TEST_FLAG(sound->runtime_flags, _sound_permutation_cached_bit)
mcc_runtime_perm_flags = UInt32("runtime_flags",
    # NOTES: 
    #   this is set, even if the samples are NOT cached. not sure why
    #   also, seems like the above exception trips if ANY bits are set
    VISIBLE=False
    )
permutation = desc_variant(permutation,
    ("parent_tag_id", mcc_runtime_perm_flags),
    ("parent_tag_id2", UInt32("parent_tag_id")),
    )
pitch_range = desc_variant(pitch_range,
    ("permutations", reflexive("permutations", permutation, 256, DYN_NAME_PATH='.name', IGNORE_SAFE_MODE=True)),
    )

mcc_snd__body = desc_variant(snd__body,
    ("flags", mcc_snd__flags),
    ("pitch_ranges", reflexive("pitch_ranges", pitch_range, 8, DYN_NAME_PATH='.name')),
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
