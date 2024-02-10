#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.senv import *
from .shdr import *

environment_shader_flags = Bool16("flags",
    "alpha_tested",
    "bump_map_is_specular_mask",
    "true_atmospheric_fog",
    "use_variant_2_for_calculation_bump_attention",
    COMMENT=environment_shader_comment
    )

environment_shader = desc_variant(environment_shader, environment_shader_flags)
senv_attrs = desc_variant(senv_attrs, environment_shader)
senv_body  = Struct("tagdata",
    shdr_attrs,
    senv_attrs,
    SIZE=836,
    )


def get():
    return senv_def

senv_def = TagDef("senv",
    blam_header('senv', 2),
    senv_body,

    ext=".shader_environment", endian=">", tag_cls=ShdrTag
    )
