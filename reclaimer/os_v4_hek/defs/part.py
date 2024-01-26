#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.part import *

from supyr_struct.util import desc_variant

particle_shader_extensions = reflexive("particle_shader_extensions",
    Struct("particle_shader_extension", INCLUDE=os_shader_extension),
    1
    )

part_body = desc_variant(part_body,
    ("pad_11", particle_shader_extensions)
    )


def get():
    return part_def

part_def = TagDef("part",
    blam_header("part", 2),
    part_body,

    ext=".particle", endian=">", tag_cls=PartTag,
    )
