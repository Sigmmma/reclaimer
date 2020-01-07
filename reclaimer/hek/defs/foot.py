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

material = Struct("material",
    dependency("effect", "effe"),
    dependency("sound", "snd!"),
    SIZE=48,
    )

effect = Struct("effect",
    reflexive("materials", material, len(materials_list), *materials_list),
    SIZE=28,
    )

foot_body = Struct("tagdata",
    reflexive("effects", effect, 13, *material_effect_types),
    SIZE=140,
    )



def get():
    return foot_def

foot_def = TagDef("foot",
    blam_header('foot'),
    foot_body,

    ext=".material_effects", endian=">", tag_cls=HekTag
    )
