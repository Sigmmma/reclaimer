#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from .jpt_ import damage, camera_shaking
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef
from supyr_struct.util import desc_variant

damage = desc_variant(damage,
    ("aoe_core_radius", Pad(4)),
    ("active_camouflage_damage", Pad(4)),
    )

camera_shaking = desc_variant(camera_shaking,
    ("duration", Pad(4)),
    ("fade_function", Pad(2)),
    )

cdmg_body = Struct("tagdata",
    from_to_wu("radius"),
    float_zero_to_one("cutoff_scale"),
    Pad(24),

    QStruct("vibrate_parameters",
        float_zero_to_one("low_frequency"),
        float_zero_to_one("high_frequency"),
        Pad(16),
        ),

    camera_shaking,
    Pad(160),

    damage,
    damage_modifiers,
    SIZE=512,
    )


def get():
    return cdmg_def

cdmg_def = TagDef("cdmg",
    blam_header('cdmg'),
    cdmg_body,

    ext=".continuous_damage_effect", endian=">", tag_cls=HekTag
    )
