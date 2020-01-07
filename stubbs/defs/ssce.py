#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.ssce import *

#import and use the open saucified obje attrs
from .obje import *

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=11)

ssce_body = dict(ssce_body)
ssce_body[0] = obje_attrs

def get():
    return ssce_def

ssce_def = TagDef("ssce",
    blam_header_stubbs('ssce'),
    ssce_body,

    ext=".sound_scenery", endian=">", tag_cls=ObjeTag
    )
