#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from .obje import *
from .devi import *
from .objs.ctrl import CtrlTag
from supyr_struct.defs.tag_def import TagDef
from supyr_struct.util import desc_variant

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = desc_variant(obje_attrs,
    ("object_type", object_type(8))
    )

ctrl_attrs = Struct("ctrl_attrs",
    SEnum16('type',
        'toggle_switch',
        'on_button',
        'off_button',
        'call_button'
        ),
    SEnum16('triggers_when',
        'touched_by_player',
        'destroyed'
        ),
    float_zero_to_one('call_value'),

    Pad(80),
    dependency("on", valid_event_effects),
    dependency("off", valid_event_effects),
    dependency("deny", valid_event_effects),
    )

ctrl_body = Struct("tagdata",
    obje_attrs,
    devi_attrs,
    ctrl_attrs,

    SIZE=792,
    )


def get():
    return ctrl_def

ctrl_def = TagDef("ctrl",
    blam_header('ctrl'),
    ctrl_body,

    ext=".device_control", endian=">", tag_cls=CtrlTag
    )
