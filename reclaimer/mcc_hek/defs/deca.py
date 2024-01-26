#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.deca import *
from supyr_struct.util import desc_variant

flags = Bool16("flags",
    "geometry_inherited_by_next_decal_in_chain",
    "interpolate_color_in_hsv",
    "more_colors",
    "no_random_rotation",
    "water_effect",
    "SAPIEN_snap_to_axis",
    "SAPIEN_incremental_counter",
    "animation_loop",
    "preserve_aspect",
    "disabled_in_remastered_by_blood_setting",
    COMMENT=decal_comment
    )

deca_body = desc_variant(deca_body,
    ("flags", flags)
    )

def get():
    return deca_def

deca_def = TagDef("deca",
    blam_header('deca'),
    deca_body,

    ext=".decal", endian=">", tag_cls=DecaTag
    )
