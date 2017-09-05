from ...hek.defs.unit import *

# replace the grenade types enumerator with an open sauce one
unit_attrs = dict(unit_attrs)
unit_attrs[49] = SEnum16('grenade type', *grenade_types_os)

unit_body = Struct('tagdata', unit_attrs)

def get():
    return unit_def

unit_def = TagDef("unit",
    blam_header('unit', 2),
    unit_body,

    ext=".unit", endian=">", tag_cls=HekTag
    )
