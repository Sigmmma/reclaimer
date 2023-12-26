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

def get(): return dobc_def

detail_object_type = Struct("detail_object_type",
    ascii_str32("name"),
    SInt8("sequence_index", SIDETIP="[0,15]"),
    Bool8("scale_flags",
        ("interpolate_color_in_hsv", 4),
        ("more_colors", 8),
        ),
    #UInt8("unknown0", VISIBLE=False),
    Pad(1),
    UInt8("sequence_sprite_count", VISIBLE=False),
    float_zero_to_one("color_override_factor"),
    Pad(8),
    float_wu("near_fade_distance"),
    float_wu("far_fade_distance"),
    Float("size", SIDETIP="world units/pixel"),
    Pad(4),
    QStruct("minimum_color", INCLUDE=rgb_float),
    QStruct("maximum_color", INCLUDE=rgb_float),
    #QStruct("ambient_color", INCLUDE=argb_byte),
    UInt32("ambient_color", INCLUDE=argb_uint32),
    SIZE=96
    )

dobc_body = Struct("tagdata",
    SEnum16("anchor",
        "screen-facing",
        "viewer-facing",
        ),
    Pad(2),
    Float("global_z_offset",
        SIDETIP="applied to all these detail object so they dont float"),
    Pad(44),
    dependency("sprite_plate", "bitm"),
    reflexive("detail_object_types", detail_object_type, 16,
        DYN_NAME_PATH='.name'),
    SIZE=128,
    )

dobc_def = TagDef("dobc",
    blam_header('dobc'),
    dobc_body,

    ext=".detail_object_collection", endian=">", tag_cls=HekTag
    )
