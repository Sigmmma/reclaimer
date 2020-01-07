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


color = Struct("color",
    ascii_str32('name'),
    QStruct("color", INCLUDE=argb_float),
    SIZE=48,
    )

colo_body = Struct("tagdata",
    reflexive("colors", color, 512, DYN_NAME_PATH='.name'),
    SIZE=12
    )

def get():
    return colo_def

colo_def = TagDef("colo",
    blam_header('colo'),
    colo_body,

    ext=".color_table", endian=">", tag_cls=HekTag
    )
