#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.sbsp import *
from ..common_descs import *

cluster_unknown = QStruct("unknown",
    Float('float_0'),
    Float('float_1'),
    Float('float_2'),
    Float('float_3'),
    Float('float_4'),
    Float('float_5'),
    SIZE=24
    )

surface_indices = desc_variant(reflexive_struct, NAME="surface_indices")
    
cluster  = desc_variant(cluster, ("pad_8", cluster_unknown), surface_indices)
clusters = reflexive("clusters", cluster, 8192)

sbsp_body      = desc_variant(sbsp_body, clusters)
fast_sbsp_body = desc_variant(fast_sbsp_body, clusters)


def get():
    return sbsp_def

sbsp_def = TagDef("sbsp",
    blam_header_stubbs("sbsp", 5),
    sbsp_body,

    ext=".scenario_structure_bsp", endian=">", tag_cls=SbspTag,
    )

fast_sbsp_def = TagDef("sbsp",
    blam_header_stubbs("sbsp", 5),
    fast_sbsp_body,

    ext=".scenario_structure_bsp", endian=">", tag_cls=SbspTag,
    )
