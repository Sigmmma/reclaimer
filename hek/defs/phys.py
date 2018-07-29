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
    Bool32('flags',
        'ground friction',
        'water friction',
        'air friction',
        'water lift',
        'air lift',
        'thrust',
        'antigrav',
        ),
    Float("antigrav strength"),
    Float("antigrav offset"),
    Float("antigrav height"),
    Float("antigrav damp fraction"),
    Float("antigrav normal k1"),
    Float("antigrav normal k0"),
    SIZE=128,
    )

mass_point = Struct("mass point",
    ascii_str32("name"),
    dyn_senum16("powered mass point",
        DYN_NAME_PATH="tagdata.powered_mass_points.STEPTREE[DYN_I].name"),
    SInt16("model node"),
    Bool32('flags',
        'metallic',
        ),
    Float("relative mass", MIN=0.0),
    Float("mass", VISIBLE=False, MIN=0.0),
    Float("relative density", MIN=0.0),
    Float("density", VISIBLE=False, MIN=0.0),
    QStruct("position", INCLUDE=xyz_float),
    QStruct("forward", INCLUDE=ijk_float),
    QStruct("up", INCLUDE=ijk_float),
    SEnum16('friction type',
        'point',
        'forward',
        'left',
        'up',
        ),
    Pad(2),
    Float("friction parallel scale"),
    Float("friction perpendicular scale"),
    Float("radius", MIN=0.0, ALLOW_MIN=False),
    SIZE=128,
    )

phys_body = Struct("tagdata",
    Float("radius"),
    Float("moment scale"),
    Float("mass", MIN=0.0),
    QStruct("center of mass", INCLUDE=xyz_float, VISIBLE=False),
    Float("density", MIN=0.0),
    Float("gravity scale"),
    Float("ground friction", UNIT_SCALE=per_sec_unit_scale),
    Float("ground depth"),
    Float("ground damp fraction"),
    Float("ground normal k1"),
    Float("ground normal k0"),
    Pad(4),
    Float("water friction", UNIT_SCALE=per_sec_unit_scale),
    Float("water depth"),
    Float("water density"),
    Pad(4),
    Float("air friction", UNIT_SCALE=per_sec_unit_scale),
    Pad(4),
    Float("xx moment", VISIBLE=False),
    Float("yy moment", VISIBLE=False),
    Float("zz moment", VISIBLE=False),

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
