#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.ctrl import *
from .obje import *
from .devi import *

obje_attrs = obje_attrs_variant(obje_attrs, "ctrl")

ctrl_body = Struct("tagdata",
    obje_attrs,
    devi_attrs,
    ctrl_attrs,

    SIZE=792,
    )

def get():
    return ctrl_def

ctrl_def = TagDef("ctrl",
    blam_header_stubbs('ctrl'),
    ctrl_body,

    ext=".device_control", endian=">", tag_cls=CtrlTag
    )
