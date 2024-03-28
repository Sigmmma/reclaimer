#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.unit import *

unit_attrs = desc_variant(unit_attrs, SEnum16('grenade_type', *grenade_types_os))
unit_body = Struct('tagdata', unit_attrs)

def get():
    return unit_def

unit_def = TagDef("unit",
    blam_header('unit', 2),
    unit_body,

    ext=".unit", endian=">", tag_cls=HekTag
    )
