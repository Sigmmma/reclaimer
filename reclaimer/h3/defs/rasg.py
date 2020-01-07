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
# revision: 2		author: -DeToX-
# 	Mapped out most of the tag
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


rasg_default_bitmap = Struct("default_bitmap",
    SInt32("unknown", VISIBLE=False),
    h3_dependency("bitmap"),
    ENDIAN=">", SIZE=20
    )


rasg_default_rasterizer_bitmap = Struct("default_rasterizer_bitmap",
    h3_dependency("bitmap"),
    ENDIAN=">", SIZE=16
    )


rasg_default_shader = Struct("default_shader",
    h3_dependency("vertex_shader"),
    h3_dependency("pixel_shader"),
    ENDIAN=">", SIZE=32
    )


rasg_body = Struct("tagdata",
    h3_reflexive("default_bitmaps", rasg_default_bitmap),
    h3_reflexive("default_rasterizer_bitmaps", rasg_default_rasterizer_bitmap),
    h3_dependency("vertex_shader_simple"),
    h3_dependency("pixel_shader_simple"),
    h3_reflexive("default_shaders", rasg_default_shader),
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    SInt32("unknown_1", VISIBLE=False),
    SInt32("unknown_2", VISIBLE=False),
    h3_dependency("active_camo_distortion"),
    h3_dependency("default_performance_template"),
    h3_dependency("default_shield_impact"),
    SInt32("unknown_3", VISIBLE=False),
    BytesRaw("unknown_4", SIZE=24, VISIBLE=False),
    ENDIAN=">", SIZE=164
    )


def get():
    return rasg_def

rasg_def = TagDef("rasg",
    h3_blam_header('rasg'),
    rasg_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["rasg"], endian=">", tag_cls=H3Tag
    )
