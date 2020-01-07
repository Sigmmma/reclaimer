#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: Lord Zedd
# 	Cleanup and porting
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


lens_reflection = Struct("reflection",
    Bool16("flags",
        "align_rotation_with_screen_center",
        "radius_not_scaled_by_distance",
        "radius_scaled_by_occlusion_factor",
        "occluded_by_solid_objects",
        "ignore_light_color",
        "not_affected_by_inner_occlusion",
        ),
    SInt16("bitmap_index"),
    Float("position_along_flare_axis"),
    Float("rotation_offset"),
    QStruct("radius", INCLUDE=from_to),
    QStruct("brightness", INCLUDE=from_to),
    Float("tint_modulation_factor"),
    color_rgb_float("tint_color"),
    Float("unknown", VISIBLE=False),
    ENDIAN=">", SIZE=48
    )


lens_brightnes = Struct("brightnes",
    h3_rawdata_ref("function"),
    ENDIAN=">", SIZE=20
    )


lens_color = Struct("color",
    h3_rawdata_ref("function"),
    ENDIAN=">", SIZE=20
    )


lens_unknown_5 = Struct("unknown_5",
    BytesRaw("unknown", SIZE=16, VISIBLE=False),
    h3_rawdata_ref("function"),
    ENDIAN=">", SIZE=36
    )


lens_rotation = Struct("rotation",
    BytesRaw("unknown", SIZE=16, VISIBLE=False),
    h3_rawdata_ref("function"),
    ENDIAN=">", SIZE=36
    )


lens_body = Struct("tagdata",
    float_rad("falloff_angle"),
    float_rad("cutoff_angle"),
    Float("occlusion_radius"),
    SInt32("unknown_0", VISIBLE=False),
    BytesRaw("unknown_1", SIZE=8, VISIBLE=False),
    Float("near_fade_distance"),
    Float("far_fade_distance"),
    h3_dependency("bitmap"),
    Array("unknown_array", SUB_STRUCT=SInt16("unknown"), SIZE=4, VISIBLE=False),
    float_rad("rotation_function_scale"),
    SInt16("unknown_2", VISIBLE=False),
    SInt16("unknown_3", VISIBLE=False),
    h3_reflexive("reflections", lens_reflection),
    BytesRaw("unknown_4", SIZE=4, VISIBLE=False),
    h3_reflexive("brightness", lens_brightnes),
    h3_reflexive("color", lens_color),
    h3_reflexive("unknown_5", lens_unknown_5),
    h3_reflexive("rotation", lens_rotation),
    BytesRaw("unknown_6", SIZE=24, VISIBLE=False),
    ENDIAN=">", SIZE=152
    )


def get():
    return lens_def

lens_def = TagDef("lens",
    h3_blam_header('lens'),
    lens_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["lens"], endian=">", tag_cls=H3Tag
    )
