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


scenario_description = Struct("scenario_description",
    dependency("descriptive_bitmap", "bitm"),
    dependency("displayed_map_name", "ustr"),
    ascii_str32("scenario_tag_directory_path"),
    SIZE=68
    )

mply_body = Struct("tagdata",
    reflexive("multiplayer_scenario_descriptions",
        scenario_description, 32, DYN_NAME_PATH='.scenario_tag_directory_path'),
    SIZE=12,
    )


def get():
    return mply_def

mply_def = TagDef("mply",
    blam_header('mply'),
    mply_body,

    ext=".multiplayer_scenario_description", endian=">", tag_cls=HekTag
    )
