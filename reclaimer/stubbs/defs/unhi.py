#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.unhi import *
from ..common_descs import dependency_stubbs


health_panel_meter = desc_variant(health_panel_meter,
    SIZE=148, verify=False
    )

auxilary_meter = desc_variant(auxilary_meter,
    SEnum16("type", 
        "integrated_light",
        "unknown",
        VISIBLE=False
        ),
    )

unhi_body = desc_variant(unhi_body,
    health_panel_meter,
    # yeah, they're swapped around
    ("warning_sounds",  reflexive("auxilary_meters", auxilary_meter, 16)),
    ("auxilary_meters", dependency_stubbs("screen_effect", "imef")),
    verify=False
    )


def get():
    return unhi_def

unhi_def = TagDef("unhi",
    blam_header("unhi"),
    unhi_body,

    ext=".unit_hud_interface", endian=">", tag_cls=HekTag,
    )