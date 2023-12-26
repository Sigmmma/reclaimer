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

ngpr_body = Struct("tagdata",
    ascii_str32("name"),
    QStruct("primary_color",   INCLUDE=rgb_float),
    QStruct("secondary_color", INCLUDE=rgb_float),

    dependency("pattern", "bitm"),
    SInt16("pattern_bitmap_index"),
    Pad(2),
    dependency("decal", "bitm"),
    SInt16("decal_bitmap_index"),
    SIZE=896
    )


def get():
    return ngpr_def

ngpr_def = TagDef("ngpr",
    blam_header('ngpr', 2),
    ngpr_body,

    ext=".preferences_network_game", endian=">", tag_cls=HekTag
    )
