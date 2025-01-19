#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.grhi import *

# NOTE: used by unhi and wphi
mcc_hud_anchor = SEnum16("anchor", *hud_anchors_mcc)

grhi_body = desc_variant(grhi_body, mcc_hud_anchor)

def get():
    return grhi_def

grhi_def = TagDef("grhi",
    blam_header("grhi"),
    grhi_body,

    ext=".grenade_hud_interface", endian=">", tag_cls=HekTag,
    )
