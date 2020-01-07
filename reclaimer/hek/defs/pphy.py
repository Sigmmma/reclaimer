#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from .objs.pphy import PphyTag
from supyr_struct.defs.tag_def import TagDef

density_comment = """Densities(grams per milliliter)\n
air        0.0011
snow       0.128
cork       0.24
cedar      0.43
oak        0.866
ice        0.897
water      1.0
soil       1.1
cotton     1.491
dry earth  1.52
sand       1.7
granite    2.4
glass      2.5
iron       7.65
steel      7.77
lead       11.37
uranium    18.74
gold       19.3"""

pphy_body = Struct("tagdata",
    Bool32("flags",
        "flamethrower_particle_collision",
        "collides_with_structures",
        "collides_with_water_surface",
        "uses_simple_wind",
        "uses_damped_wind",
        "no_gravity"
        ),
    # these next three are courtesy of Sparky. I had
    # no idea these existed till I looked in Eschaton.
    # kavawuvi figured out how to calculate them(see PphyTag)
    FlFloat("scaled_density", VISIBLE=False),
    FlFloat("water_gravity_scale", VISIBLE=False),
    FlFloat("air_gravity_scale", VISIBLE=False),
    Pad(16),
    Float("density", SIDETIP="g/mL", COMMENT=density_comment),#g/mL
    Float("air_friction"),
    Float("water_friction"),
    Float("surface_friction"),
    Float("elasticity"),

    SIZE=64
    )

def get():
    return pphy_def

pphy_def = TagDef("pphy",
    blam_header('pphy'),
    pphy_body,

    ext=".point_physics", endian=">", tag_cls=PphyTag
    )
