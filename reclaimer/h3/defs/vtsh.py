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


vtsh_unknown_1_unknown = Struct("unknown",
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


vtsh_unknown_1 = Struct("unknown_1",
    h3_reflexive("unknown", vtsh_unknown_1_unknown),
    VISIBLE=False,
    ENDIAN=">", SIZE=12
    )


vtsh_vertex_shader_unknown_2 = Struct("unknown_2",
    h3_string_id("unknown_0", VISIBLE=False),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=8
    )


vtsh_vertex_shader = Struct("vertex_shader",
    h3_rawdata_ref("unknown_0", VISIBLE=False),
    h3_rawdata_ref("unknown_1", VISIBLE=False),
    h3_reflexive("unknown_2", vtsh_vertex_shader_unknown_2),
    BytesRaw("unknown_3", SIZE=24, VISIBLE=False),
    UInt32("vertex_shader"),
    ENDIAN=">", SIZE=80
    )


vtsh_body = Struct("tagdata",
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    h3_reflexive("unknown_1", vtsh_unknown_1),
    BytesRaw("unknown_2", SIZE=4, VISIBLE=False),
    h3_reflexive("vertex_shaders", vtsh_vertex_shader),
    ENDIAN=">", SIZE=32
    )


def get():
    return vtsh_def

vtsh_def = TagDef("vtsh",
    h3_blam_header('vtsh'),
    vtsh_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["vtsh"], endian=">", tag_cls=H3Tag
    )
