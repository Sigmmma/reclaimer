#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

'''
THIS DEFINITION IS INCORRECT BECAUSE THE UNIT STRUCTURE IS DIFFERENT THAN HALO'S
'''
from ...hek.defs.bipd import *
from .obje import *
from .unit import *

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=0)

bipd_body = Struct("tagdata",
    obje_attrs,
    unit_attrs,
    bipd_attrs,
    SIZE=1268,
    )

#def get():
#    return bipd_def
del get

bipd_def = TagDef("bipd",
    blam_header_stubbs('bipd', 3),
    bipd_body,

    ext=".biped", endian=">", tag_cls=BipdTag
    )
