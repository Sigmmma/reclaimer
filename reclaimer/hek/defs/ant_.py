#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from .objs.ant_ import Ant_Tag
from supyr_struct.defs.tag_def import TagDef

vertex = Struct("vertex",
    Float("spring_strength_coefficient"),

    Pad(24),
    yp_float_rad("angles"),  # radians
    float_wu("length"),
    SInt16("sequence_index"),

    Pad(2),
    QStruct("color", INCLUDE=argb_float),
    QStruct("lod_color", INCLUDE=argb_float),
    Pad(40),
    QStruct('offset', INCLUDE=xyz_float, VISIBLE=False),

    SIZE=128
    )

ant__body = Struct("tagdata",
    ascii_str32("attachment_marker_name"),
    dependency("bitmaps", "bitm"),
    dependency("physics", "pphy"),

    Pad(80),
    Float("spring_strength_coefficient"),
    Float("falloff_pixels"),
    Float("cutoff_pixels"),
    Float("length"),

    Pad(36),
    reflexive("vertices", vertex, 20),
    SIZE=208
    )


def get():
    return ant__def

ant__def = TagDef("ant!",
    blam_header('ant!'),
    ant__body,

    ext=".antenna", endian=">", tag_cls=Ant_Tag
    )
