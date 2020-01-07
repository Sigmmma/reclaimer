#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from ...hek.defs.objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

bloom_global = Struct("bloom_global",
    Bool16("shader_model",
        "enabled",
        "apply_after_hud",
        ),
    Pad(2),
    Float("bloom_size"),
    Float("bloom_exposure"),
    Float("bloom_mix_amount", MIN=0.0, MAX=1.0),
    QStruct("bloom_minimum_color", INCLUDE=rgb_float),
    QStruct("bloom_maximum_color", INCLUDE=rgb_float),
    SIZE=40,
    )

sppg_body = Struct("tagdata",
    Pad(4),
    reflexive("bloom_globals", bloom_global, 1),
    SIZE=244
    )

def get():
    return sppg_def

sppg_def = TagDef("sppg",
    blam_header_os('sppg'),
    sppg_body,

    ext=".shader_postprocess_globals", endian=">", tag_cls=HekTag
    )
