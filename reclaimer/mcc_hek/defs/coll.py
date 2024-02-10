#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.coll import *

coll_body = desc_variant(coll_body,
    reflexive("pathfinding_spheres", pathfinding_sphere, 256),
    )
fast_coll_body = desc_variant(coll_body,
    reflexive("nodes", fast_node, 64, DYN_NAME_PATH='.name'),
    )

def get():
    return coll_def

coll_def = TagDef("coll",
    blam_header("coll", 10),
    coll_body,

    ext=".model_collision_geometry", endian=">", tag_cls=CollTag,
    )

fast_coll_def = TagDef("coll",
    blam_header("coll", 10),
    fast_coll_body,

    ext=".model_collision_geometry", endian=">", tag_cls=CollTag,
    )
