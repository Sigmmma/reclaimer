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


control_point = Struct("control_point",
    QStruct("position", INCLUDE=ijk_float),
    QStruct("orientation", INCLUDE=ijkw_float),
    SIZE=60,
    )

trak_body = Struct("tagdata",
    Pad(4),
    reflexive("control_points", control_point, 16),
    SIZE=48,
    )


def get():
    return trak_def

trak_def = TagDef("trak",
    blam_header('trak', 2),
    trak_body,

    ext=".camera_track", endian=">", tag_cls=HekTag
    )
