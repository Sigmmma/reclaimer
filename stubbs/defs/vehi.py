'''
THIS DEFINITION IS INCORRECT BECAUSE THE UNIT STRUCTURE IS DIFFERENT THAN HALO'S
'''
from ...hek.defs.vehi import *
from .obje import *
from .unit import *

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=1)

vehi_attrs = dict(vehi_attrs)
vehi_attrs[1] = SEnum16('type', *vehicle_types)

vehi_body = Struct("tagdata",
    obje_attrs,
    unit_attrs,
    vehi_attrs,
    SIZE=1008,
    )

#def get():
#    return vehi_def
del get

vehi_def = TagDef("vehi",
    blam_header_stubbs('vehi'),
    vehi_body,

    ext=".vehicle", endian=">"
    )
