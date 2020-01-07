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

item_permutation = Struct("permutation",
    Pad(32),
    Float("weight"),
    dependency("item", valid_items),
    SIZE=84,
    )

itmc_body = Struct("tagdata",
    reflexive("item_permutations", item_permutation, 32767,
        DYN_NAME_PATH='.item.filepath'),
    SInt16("spawn_time", SIDETIP="seconds(0 = default)",
            UNIT_SCALE=per_sec_unit_scale),
    SIZE=92,
    )


def get():
    return itmc_def

itmc_def = TagDef("itmc",
    blam_header('itmc',0),
    itmc_body,

    ext=".item_collection", endian=">", tag_cls=HekTag
    )
