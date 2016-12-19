from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

'''
To calculate center of mass, add up all of the mass point
position vectors multiplied by their relative mass, then
divide the resulting vector by:
    (total_relative_mass * number_of_mass_points).
This will give the center of mass as a vector.

xx, yy, and zz moments are affected by mass point radius
Remember that moments are the mass times the distance from
the respective axis on a path perpendicular to the axis.

This will mean doing sqrt(y^2+z^2) for xx,
sqrt(x^2+z^2) for yy, and sqrt(x^2+y^2) for zz

The second matrix is an inverse of the first matrix.
Both matricies must exist.
'''

inertial_matrix = Struct("inertial matrix",
    QStruct("yy_zz", GUI_NAME="yy+zz    -xy    -zx", INCLUDE=ijk_float),
    QStruct("zz_xx", GUI_NAME="-xy    zz+xx    -yz", INCLUDE=ijk_float),
    QStruct("xx_yy", GUI_NAME="-zx      -yz  xx+yy", INCLUDE=ijk_float),
    SIZE=36,
    )

powered_mass_point = Struct("powered mass point",
    ascii_str32("name"),
    BBool32('flags',
        'ground friction',
        'water friction',
        'air friction',
        'water lift',
        'air lift',
        'thrust',
        'antigrav',
        ),
    BFloat("antigrav strength"),
    BFloat("antigrav offset"),
    BFloat("antigrav height"),
    BFloat("antigrav damp fraction"),
    BFloat("antigrav normal k1"),
    BFloat("antigrav normal k0"),
    SIZE=128,
    )

mass_point = Struct("mass point",
    ascii_str32("name"),
    dyn_senum16("powered mass point"),
    BSInt16("model node"),
    BBool32('flags',
        'metallic',
        ),
    BFloat("relative mass"),
    BFloat("mass"),
    BFloat("relative density"),
    BFloat("density"),
    QStruct("position", INCLUDE=ijk_float),
    QStruct("forward", INCLUDE=ijk_float),
    QStruct("up", INCLUDE=ijk_float),
    BSEnum16('friction type',
        'point',
        'forward',
        'left',
        'up',
        ),
    Pad(2),
    BFloat("friction parallel scale"),
    BFloat("friction perpendicular scale"),
    BFloat("radius"),
    SIZE=128,
    )

phys_body = Struct("tagdata",
    BFloat("radius"),
    BFloat("moment scale"),
    BFloat("mass"),
    QStruct("center of mass", INCLUDE=xyz_float),
    BFloat("density"),
    BFloat("gravity scale"),
    BFloat("ground friction"),
    BFloat("ground depth"),
    BFloat("ground damp fraction"),
    BFloat("ground normal k1"),
    BFloat("ground normal k0"),
    Pad(4),
    BFloat("water friction"),
    BFloat("water depth"),
    BFloat("water density"),
    Pad(4),
    BFloat("air friction"),
    Pad(4),
    BFloat("xx moment"),
    BFloat("yy moment"),
    BFloat("zz moment"),

    reflexive("inertial matrix and inverse", inertial_matrix, 2),
    reflexive("powered mass points", powered_mass_point, 32),
    reflexive("mass points", mass_point, 32),
    SIZE=128,
    )


def get():
    return phys_def

phys_def = TagDef("phys",
    blam_header('phys', 4),
    phys_body,

    ext=".physics", endian=">"
    )
