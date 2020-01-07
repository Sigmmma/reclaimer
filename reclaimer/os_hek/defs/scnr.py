#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.scnr import *
from supyr_struct.util import desc_variant

player_starting_profile = Struct("player_starting_profile",
    ascii_str32("name"),
    float_zero_to_one("starting_health_modifier"),
    float_zero_to_one("starting_shield_modifier"),
    dependency("primary_weapon", "weap"),
    SInt16("primary_rounds_loaded"),
    SInt16("primary_rounds_total"),
    dependency("secondary_weapon", "weap"),
    SInt16("secondary_rounds_loaded"),
    SInt16("secondary_rounds_total"),
    SInt8("starting_frag_grenade_count", MIN=0),
    SInt8("starting_plasma_grenade_count", MIN=0),
    SInt8("starting_custom_2_grenade_count", MIN=0),
    SInt8("starting_custom_3_grenade_count", MIN=0),
    SIZE=104
    )

ai_anim_reference = Struct("ai_animation_reference",
    ascii_str32("animation_name"),
    dependency_os("animation_graph", ("antr", "magy")),
    SIZE=60
    )

reference = Struct("tag_reference",
    Pad(24),
    dependency_os("reference"),
    SIZE=40
    )

# copy the scnr_body and replace the descriptors for certain
# fields with ones that are tweaked for use with open sauce
scnr_body = desc_variant(
    scnr_body,
    ("DONT_USE", dependency_os("project_yellow_definitions", 'yelo')),
    ("player_starting_profiles",
     reflexive("player_starting_profiles",
        player_starting_profile, 256, DYN_NAME_PATH='.name')
     ),
    ("ai_animation_references",
     reflexive("ai_animation_references",
        ai_anim_reference, 128, DYN_NAME_PATH='.animation_name')
     ),
    ("script_syntax_data", rawdata_ref("script_syntax_data", max_size=570076, IGNORE_SAFE_MODE=True)),
    ("script_string_data", rawdata_ref("script_string_data", max_size=393216, IGNORE_SAFE_MODE=True)),
    ("references",
     reflexive("references",
        reference, 256, DYN_NAME_PATH='.reference.filepath')
     ),
    ("structure_bsps",
     reflexive("structure_bsps",
        structure_bsp, 32, DYN_NAME_PATH='.structure_bsp.filepath')
     )
    )

def get():
    return scnr_def

scnr_def = TagDef("scnr",
    blam_header('scnr', 2),
    scnr_body,

    ext=".scenario", endian=">", tag_cls=HekTag
    )
