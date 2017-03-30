from ...common_descs import *
from .objs.phys import PhysTag
from supyr_struct.defs.tag_def import TagDef

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
    dyn_senum16("powered mass point",
        DYN_NAME_PATH="tagdata.powered_mass_points.STEPTREE[DYN_I].name"),
    BSInt16("model node"),
    BBool32('flags',
        'metallic',
        ),
    BFloat("relative mass", MIN=0.0),
    BFloat("mass", VISIBLE=False, MIN=0.0),
    BFloat("relative density", MIN=0.0),
    BFloat("density", VISIBLE=False, MIN=0.0),
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
    BFloat("radius", MIN=0.0, ALLOW_MIN=False),
    SIZE=128,
    )

phys_body = Struct("tagdata",
    BFloat("radius"),
    BFloat("moment scale"),
    BFloat("mass", MIN=0.0),
    QStruct("center of mass", INCLUDE=xyz_float, VISIBLE=False),
    BFloat("density", MIN=0.0),
    BFloat("gravity scale"),
    BFloat("ground friction", UNIT_SCALE=per_sec_unit_scale),
    BFloat("ground depth"),
    BFloat("ground damp fraction"),
    BFloat("ground normal k1"),
    BFloat("ground normal k0"),
    Pad(4),
    BFloat("water friction", UNIT_SCALE=per_sec_unit_scale),
    BFloat("water depth"),
    BFloat("water density"),
    Pad(4),
    BFloat("air friction", UNIT_SCALE=per_sec_unit_scale),
    Pad(4),
    BFloat("xx moment", VISIBLE=False),
    BFloat("yy moment", VISIBLE=False),
    BFloat("zz moment", VISIBLE=False),

    reflexive("inertia matrices", inertial_matrix, 2,
        "regular", "inverse", MIN=2, MAX=2, VISIBLE=False),
    reflexive("powered mass points", powered_mass_point, 32,
        DYN_NAME_PATH='.name'),
    reflexive("mass points", mass_point, 32,
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
