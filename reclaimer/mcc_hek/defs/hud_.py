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

hud__body = Struct("tagdata",
    dependency("digits_bitmap", "bitm"),
    SInt8("bitmap_digit_width"),
    SInt8("screen_digit_width"),
    SInt8("x_offset"),
    SInt8("y_offset"),
    SInt8("decimal_point_width"),
    SInt8("colon_width"),
    SIZE=100,
    )


def get():
    return hud__def

hud__def = TagDef("hud#",
    blam_header('hud#'),
    hud__body,

    ext=".hud_number", endian=">", tag_cls=HekTag
    )
