#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.soso import *
from .shdr import *
from supyr_struct.util import desc_variant

model_shader_flags = Bool16("flags",
    "detail_after_reflection",
    "two_sided",
    "not_alpha_tested",
    "alpha_blended_decal",
    "true_atmospheric_fog",
    "disable_two_sided_culling",
    "multipurpose_map_uses_og_xbox_channel_order",
    )

model_shader = desc_variant(model_shader,
    ("flags", model_shader_flags),
    )

soso_attrs = desc_variant(soso_attrs,
    ("model_shader", model_shader),
    ("reflection_bump_scale", Pad(4)),
    ("reflection_bump_map", Pad(16)),
    )

soso_body = Struct("tagdata",
    shdr_attrs,
    soso_attrs
    )

def get():
    return soso_def

soso_def = TagDef("soso",
    blam_header('soso', 2),
    soso_body,

    ext=".shader_model", endian=">", tag_cls=ShdrTag
    )
