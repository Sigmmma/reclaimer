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
# 	Oh the xex has names.
# revision: 3		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef


perf_performance = Struct("performance",
    Bool32("flags",
        ("disable_self_shadowing", 1 << 1),
        "disable_player_shadows",
        ),
    Float("water"),
    Float("decorators"),
    Float("effects"),
    Float("instanced_geometry"),
    Float("object_fade"),
    Float("object_lod"),
    Float("decals"),
    SInt32("cpu_light_count"),
    Float("cpu_light_quality"),
    SInt32("gpu_light_count"),
    Float("gpu_light_quality"),
    SInt32("shadow_count"),
    Float("shadow_quality"),
    ENDIAN=">", SIZE=56
    )


perf_body = Struct("tagdata",
    h3_reflexive("performance", perf_performance),
    ENDIAN=">", SIZE=12
    )


def get():
    return perf_def

perf_def = TagDef("perf",
    h3_blam_header('perf'),
    perf_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["perf"], endian=">", tag_cls=H3Tag
    )
