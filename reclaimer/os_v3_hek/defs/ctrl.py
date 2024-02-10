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

obje_attrs = obje_attrs_variant(obje_attrs, "ctrl")
ctrl_body  = desc_variant(ctrl_body, obje_attrs)

def get():
    return ctrl_def

ctrl_def = TagDef("ctrl",
    blam_header('ctrl'),
    ctrl_body,

    ext=".device_control", endian=">", tag_cls=CtrlTag
    )
