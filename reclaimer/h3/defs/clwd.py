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
# revision: 2		author: DarkShallFall
# 	Labeled most of the tag
# revision: 3		author: DarkShallFall
# 	H2
# revision: 4		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef

clwd_integration_type = (
    "verlet",
    )


clwd_vertice = Struct("vertice",
    QStruct("initial_position", INCLUDE=xyz_float),
    QStruct("uv", INCLUDE=ij_float),
    ENDIAN=">", SIZE=20
    )


clwd_indice = Struct("indice",
    SInt16("idx"),
    ENDIAN=">", SIZE=2
    )


clwd_link = Struct("link",
    SInt16("index_1"),
    SInt16("index_2"),
    Float("default_distance"),
    ENDIAN=">", SIZE=8
    )


clwd_body = Struct("tagdata",
    Bool32("flags",
        "doesn_t_use_wind",
        "uses_grid_attach_top",
        ),
    h3_string_id("marker_attachment_name"),
    h3_string_id("second_marker_attachment_name"),
    h3_dependency("shader"),
    SInt16("grid_x_dimension"),
    SInt16("grid_y_dimension"),
    QStruct("grid_spacing", INCLUDE=xy_float),
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    SEnum16("integration_type", *clwd_integration_type),
    SInt16("number_iterations"),
    Float("weight"),
    Float("drag"),
    Float("wind_scale"),
    Float("wind_flappiness_scale"),
    Float("longest_rod"),
    BytesRaw("unknown_1", SIZE=24, VISIBLE=False),
    h3_reflexive("vertices", clwd_vertice),
    h3_reflexive("indices", clwd_indice),
    BytesRaw("unknown_2", SIZE=12, VISIBLE=False),
    h3_reflexive("links", clwd_link),
    ENDIAN=">", SIZE=148
    )


def get():
    return clwd_def

clwd_def = TagDef("clwd",
    h3_blam_header('clwd'),
    clwd_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["clwd"], endian=">", tag_cls=H3Tag
    )
