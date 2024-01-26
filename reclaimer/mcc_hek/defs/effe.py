#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.effe import *
from supyr_struct.util import desc_variant

flags = Bool32("flags",
    {NAME: "deleted_when_inactive", GUI_NAME: "deleted when attachment deactivates"},
    {NAME: "required", GUI_NAME: "required for gameplay (cannot optimize out)"},
    {NAME: "must_be_deterministic", VISIBLE: VISIBILITY_HIDDEN},
    "disabled_in_remastered_by_blood_setting"
    )

effe_body = desc_variant(effe_body,
    ("flags", flags),
    )

def get():
    return effe_def

effe_def = TagDef("effe",
    blam_header("effe", 4),
    effe_body,

    ext=".effect", endian=">", tag_cls=EffeTag,
    )
