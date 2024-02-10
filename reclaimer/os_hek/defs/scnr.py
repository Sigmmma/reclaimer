#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.scnr import *
from .objs.scnr import OsScnrTag

player_starting_profile = desc_variant(player_starting_profile,
    ("pad_11", SInt8("starting_custom_2_grenade_count", MIN=0)),
    ("pad_12", SInt8("starting_custom_3_grenade_count", MIN=0)),
    )

ai_anim_reference = desc_variant(ai_anim_reference,
    dependency_os("animation_graph", ("antr", "magy"))
    )

reference = desc_variant(reference, dependency_os("reference"))

scnr_body = desc_variant(scnr_body,
    ("DONT_USE", dependency_os("project_yellow_definitions", 'yelo')),
    reflexive("player_starting_profiles", player_starting_profile, 256, DYN_NAME_PATH='.name'),
    reflexive("ai_animation_references", ai_anim_reference, 128, DYN_NAME_PATH='.animation_name'),
    rawdata_ref("script_syntax_data", max_size=570076, IGNORE_SAFE_MODE=True),
    rawdata_ref("script_string_data", max_size=393216, IGNORE_SAFE_MODE=True),
    reflexive("references", reference, 256, DYN_NAME_PATH='.reference.filepath'),
    reflexive("structure_bsps", structure_bsp, 32, DYN_NAME_PATH='.structure_bsp.filepath'),
    )

def get():
    return scnr_def

# TODO: update dependencies
scnr_def = TagDef("scnr",
    blam_header('scnr', 2),
    scnr_body,

    ext=".scenario", endian=">", tag_cls=OsScnrTag
    )
