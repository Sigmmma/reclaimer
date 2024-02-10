#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.wphi import *
from ..common_descs import dependency_stubbs


wphi_body = desc_variant(wphi_body,
    ("pad_11",  Pad(16)),
    ("screen_effect", dependency_stubbs("screen_effect", "imef")),
    verify=False
    )


def get():
    return wphi_def

wphi_def = TagDef("wphi",
    blam_header("wphi", 2),
    wphi_body,

    ext=".weapon_hud_interface", endian=">", tag_cls=WphiTag,
    )