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

shader = Struct("shader",
    Pad(36),
    FlUInt32("unknown0"),
    Bool16("shader_flags", *shader_flags),
    SEnum16("framebuffer_blend_function", *framebuffer_blend_functions),
    SEnum16("framebuffer_fade_mode", *render_fade_mode),
    Bool16("map_flags",
        "unfiltered"
        ),
    Pad(40),
    FlUInt32("unknown1"),
    Pad(88),
    SIZE=180
    )

marker = Struct("marker",
    ascii_str32("attachment_marker"),
    Bool16("flags",
        "not_connected_to_next_marker"
        ),

    Pad(2),
    SInt16("octaves_to_next_marker"),

    Pad(78),
    QStruct("random_position_bounds", INCLUDE=ijk_float, SIDETIP="world units"),
    float_wu("random_jitter"),
    float_wu("thickness"),
    QStruct("tint", INCLUDE=argb_float),
    SIZE=228
    )

elec_body = Struct("tagdata",
    Pad(2),
    SInt16("effects_count"),

    Pad(16),
    float_wu("near_fade_distance"),
    float_wu("far_fade_distance"),

    Pad(16),
    SEnum16("jitter_scale_source", *function_outputs),
    SEnum16("thickness_scale_source", *function_outputs),
    SEnum16("tint_modulation_source", *function_names),
    SEnum16("brightness_scale_source", *function_outputs),
    dependency("bitmap", "bitm"),

    Pad(84),
    reflexive("markers", marker, 16, DYN_NAME_PATH='.attachment_marker'),
    reflexive("shaders", shader, 1),

    SIZE=264,
    )


def get():
    return elec_def

elec_def = TagDef("elec",
    blam_header("elec"),
    elec_body,

    ext=".lightning", endian=">", tag_cls=HekTag,
    )
