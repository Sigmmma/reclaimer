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


meter_body = Struct("tagdata",
    Pad(4),
    dependency("stencil_bitmap", "bitm"),
    dependency("source_bitmap",  "bitm"),

    SInt16("stencil_sequence_index"),
    SInt16("source_sequence_index"),
    Pad(20),
    SEnum16("interpolate_colors",
        "linearly",
        "faster_near_empty",
        "faster_near_full",
        "through_random_noise"
        ),
    SEnum16("anchor_colors" ,
        "at_both_ends",
        "at_empty",
        "at_full"
        ),
    Pad(8),
    QStruct("empty_color", INCLUDE=argb_float),
    QStruct("full_color",  INCLUDE=argb_float),
    Pad(20),
    Float("unmask_distance", SIDETIP="meter units"),
    Float("mask_distance", SIDETIP="meter units"),
    Pad(12),
    FlUInt16("screen_x_pos", SIDETIP="pixels"),
    FlUInt16("screen_y_pos", SIDETIP="pixels"),
    FlUInt16("width", SIDETIP="pixels"),
    FlUInt16("height", SIDETIP="pixels"),

    rawdata_ref("meter_data", max_size=65536),
    SIZE=172, WIDGET=MeterImageFrame
    )

def get():
    return metr_def

metr_def = TagDef("metr",
    blam_header('metr'),
    meter_body,
    ext=".meter", endian=">", tag_cls=HekTag
    )
