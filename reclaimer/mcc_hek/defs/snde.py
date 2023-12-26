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

snde_body = QStruct("tagdata",
    Pad(4),
    UInt16("priority"),
    Pad(2),
    Float("room_intensity"),
    Float("room_intensity_hf"),
    Float("room_rolloff", MIN=0.0, MAX=10.0),
    float_sec("decay_time", MIN=0.1, MAX=20.0),
    Float("decay_hf_ratio", MIN=0.1, MAX=2.0),
    Float("reflections_intensity"),
    float_sec("reflections_delay", MIN=0.0, MAX=0.3),
    Float("reverb_intensity"),
    float_sec("reverb_delay", MIN=0.0, MAX=0.1),
    Float("diffusion"),
    Float("density"),
    Float("hf_reference", MIN=20.0, MAX=20000.0, SIDETIP="Hz"),
    SIZE=72,
    )

def get():
    return snde_def

snde_def = TagDef("snde",
    blam_header('snde'),
    snde_body,

    ext=".sound_environment", endian=">", tag_cls=HekTag
    )
