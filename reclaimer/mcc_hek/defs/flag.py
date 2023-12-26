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

def get(): return flag_def

attachment_point = Struct("attachment_point",
    SInt16("height_to_next_attachment", SIDETIP="vertices"),
    Pad(18),
    ascii_str32("marker_name"),
    )

flag_body = Struct("tagdata",
    Pad(4),
    SEnum16("trailing_edge_shape",
        "flat",
        "concave_triangular",
        "convex_triangular",
        "trapezoid_short_top",
        "trapezoid_short_bottom",
        ),

    SInt16("trailing_edge_shape_offset", SIDETIP="vertices"),
    SEnum16("attached_edge_shape",
        "flat",
        "concave_triangular",
        ),
    Pad(2),
    SInt16("width", SIDETIP="vertices"),
    SInt16("height", SIDETIP="vertices"),

    float_wu("cell_width"),
    float_wu("cell_height"),

    dependency("red_flag_shader", valid_shaders),
    dependency("physics", "pphy"),

    float_wu_sec("wind_noise"),
    Pad(8),
    dependency("blue_flag_shader", valid_shaders),
    reflexive("attachment_points", attachment_point, 4,
        DYN_NAME_PATH='.marker_name'),
    SIZE=96,
    )

flag_def = TagDef("flag",
    blam_header('flag'),
    flag_body,

    ext=".flag", endian=">", tag_cls=HekTag
    )
