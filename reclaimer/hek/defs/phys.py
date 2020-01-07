#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from .objs.phys import PhysTag
from supyr_struct.defs.tag_def import TagDef

inertial_matrix = Struct("inertial_matrix",
    QStruct("yy_zz", GUI_NAME="yy+zz    -xy    -zx", INCLUDE=ijk_float),
    QStruct("zz_xx", GUI_NAME="-xy    zz+xx    -yz", INCLUDE=ijk_float),
    QStruct("xx_yy", GUI_NAME="-zx      -yz  xx+yy", INCLUDE=ijk_float),
    SIZE=36,
    )

powered_mass_point = Struct("powered_mass_point",
    ascii_str32("name"),
    Bool32('flags',
        'ground_friction',
        'water_friction',
        'air_friction',
        'water_lift',
        'air_lift',
        'thrust',
        'antigrav',
        ),
    Float("antigrav_strength"),
    Float("antigrav_offset"),
    Float("antigrav_height"),
    Float("antigrav_damp_fraction"),
    Float("antigrav_normal_k1"),
    Float("antigrav_normal_k0"),
    SIZE=128,
    )

mass_point = Struct("mass_point",
    ascii_str32("name"),
    dyn_senum16("powered_mass_point",
        DYN_NAME_PATH="tagdata.powered_mass_points.STEPTREE[DYN_I].name"),
    SInt16("model_node"),
    Bool32('flags',
        'metallic',
        ),
    Float("relative_mass", MIN=0.0),
    Float("mass", VISIBLE=False, MIN=0.0),
    Float("relative_density", MIN=0.0),
    Float("density", VISIBLE=False, MIN=0.0),
    QStruct("position", INCLUDE=xyz_float),
    QStruct("forward", INCLUDE=ijk_float),
    QStruct("up", INCLUDE=ijk_float),
    SEnum16('friction_type',
        'point',
        'forward',
        'left',
        'up',
        ),
    Pad(2),
    Float("friction_parallel_scale"),
    Float("friction_perpendicular_scale"),
    Float("radius", MIN=0.0, ALLOW_MIN=False),
    SIZE=128,
    )

phys_body = Struct("tagdata",
    Float("radius"),
    Float("moment_scale"),
    Float("mass", MIN=0.0),
    QStruct("center_of_mass", INCLUDE=xyz_float, VISIBLE=False),
    Float("density", MIN=0.0),
    Float("gravity_scale"),
    Float("ground_friction", UNIT_SCALE=per_sec_unit_scale),
    Float("ground_depth"),
    Float("ground_damp_fraction"),
    Float("ground_normal_k1"),
    Float("ground_normal_k0"),
    Pad(4),
    Float("water_friction", UNIT_SCALE=per_sec_unit_scale),
    Float("water_depth"),
    Float("water_density"),
    Pad(4),
    Float("air_friction", UNIT_SCALE=per_sec_unit_scale),
    Pad(4),
    Float("xx_moment", VISIBLE=False),
    Float("yy_moment", VISIBLE=False),
    Float("zz_moment", VISIBLE=False),

    reflexive("inertia_matrices", inertial_matrix, 2,
        "regular", "inverse", MIN=2, MAX=2, VISIBLE=False),
    reflexive("powered_mass_points", powered_mass_point, 32,
        DYN_NAME_PATH='.name'),
    reflexive("mass_points", mass_point, 32,
        DYN_NAME_PATH='.name'),
    SIZE=128,
    COMMENT="\
Some fields have been hidden because you cant edit them.\n\n\
This is because they are recalculated when you hit save.\n\
The inertial matrices and xx/yy/zz moments are hidden as\n\
well as the mass and density of the individual mass points."
    )


def get():
    return phys_def

phys_def = TagDef("phys",
    blam_header('phys', 4),
    phys_body,

    ext=".physics", endian=">", tag_cls=PhysTag
    )
