#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...os_v3_hek.defs.bipd import *

#import and use the open saucified obje and unit attrs
from .obje import *
from .unit import *

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=0)

bipd_body = dict(bipd_body)
bipd_body[0] = obje_attrs
bipd_body[1] = unit_attrs

def get():
    return bipd_def

bipd_def = TagDef("bipd",
    blam_header('bipd', 3),
    bipd_body,

    ext=".biped", endian=">", tag_cls=BipdTag
    )
