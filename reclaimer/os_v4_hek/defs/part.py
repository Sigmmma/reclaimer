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

part_body = Struct("tagdata",
    flags,
    dependency("bitmap", "bitm"),
    dependency("physics", "pphy"),
    dependency("impact_effect", "foot",
        TOOLTIP="Marty traded his kids for this"),

    Pad(4),
    from_to_sec("lifespan"),
    float_sec("fade_in_time"),
    float_sec("fade_out_time"),

    dependency("collision_effect", valid_event_effects),
    dependency("death_effect", valid_event_effects),

    rendering,
    reflexive("particle_shader_extensions",
        Struct("particle_shader_extension", INCLUDE=os_shader_extension), 1
        ),
    Pad(16),

    secondary_map,
    SIZE=356,
    )


def get():
    return part_def

part_def = TagDef("part",
    blam_header("part", 2),
    part_body,

    ext=".particle", endian=">", tag_cls=HekTag,
    )
