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
# revision: 2		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


skya_atmosphere_propertie = Struct("atmosphere_propertie",
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    h3_string_id("name"),
    Float("light_source_y"),
    Float("light_source_x"),
    color_rgb_float("fog_color"),
    Float("brightness"),
    Float("fog_gradient_threshold"),
    Float("light_intensity"),
    Float("sky_invisiblility_through_fog"),
    Float("unknown_2", VISIBLE=False),
    Float("unknown_3", VISIBLE=False),
    Float("light_source_spread"),
    BytesRaw("unknown_4", SIZE=4, VISIBLE=False),
    Float("fog_intensity"),
    Float("unknown_5", VISIBLE=False),
    Float("tint_cyan"),
    Float("tint_magenta"),
    Float("tint_yellow"),
    Float("fog_intensity_cyan"),
    Float("fog_intensity_magenta"),
    Float("fog_intensity_yellow"),
    color_rgb_float("background_color"),
    Float("tint_red"),
    Float("tint2_green"),
    Float("tint2_blue"),
    Float("fog_intensity2"),
    Float("start_distance"),
    Float("end_distance"),
    QStruct("fog_velocity", INCLUDE=xyz_float),
    h3_dependency("weather_effect"),
    BytesRaw("unknown_6", SIZE=8, VISIBLE=False),
    ENDIAN=">", SIZE=164
    )


skya_underwater = Struct("underwater",
    h3_string_id("name"),
    color_argb_float("color"),
    ENDIAN=">", SIZE=20
    )


skya_body = Struct("tagdata",
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    h3_dependency("fog_bitmap"),
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=7, VISIBLE=False),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    h3_reflexive("atmosphere_properties", skya_atmosphere_propertie),
    h3_reflexive("underwater", skya_underwater),
    ENDIAN=">", SIZE=76
    )


def get():
    return skya_def

skya_def = TagDef("skya",
    h3_blam_header('skya'),
    skya_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["skya"], endian=">", tag_cls=H3Tag
    )
