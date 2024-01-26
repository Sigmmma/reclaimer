#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.obje import *
from ..common_descs import *
from supyr_struct.util import desc_variant

def get():
    return obje_def

obje_attrs = desc_variant(obje_attrs,
    ("model", dependency_stubbs('model', 'mode')),
    )

obje_body = Struct('tagdata',
    obje_attrs,
    SIZE=380
    )

obje_def = TagDef("obje",
    blam_header_stubbs('obje'),
    obje_body,

    ext=".object", endian=">", tag_cls=ObjeTag
    )
