#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from ...hek.defs.objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

animation_comment = """
Played immediately after the old unit's transform out animation.
The new actor is braindead during the animation, and is invincible until it ends.
"""

vitality_inheritance_overrides = (
    'neither',
    'both',
    'shield_only',
    'health_only'
    )

keyframe_action = Struct("keyframe_action",
    SEnum16("keyframe",
        "primary",
        "secondary",
        "final",
        ),
    SEnum16("rider_handling",
        'none',
        'kill',
        'eject',
        ),
    SEnum16("target",
        'self',
        'riders',
        ),
    Pad(2),
    dependency_os("damage_effect", "jpt!"),
    dependency_os("effect", "effe"),
    ascii_str32("effect_marker"),
    SIZE=72
    )

transform_in_target = Struct("transform_in_target",
    ascii_str32("target_name"),
    Bool16("flags",
        'try_to_use_existing_unit',
        'drop_weapon',
        'inherit_seated_units',
        'delete_attached_actors',
        ),

    Pad(2),
    QStruct("selection_chances",
        Float("easy"), Float("normal"), Float("hard"), Float("imposs"),
        ORIENT="h"
        ),

    Struct("ai",
        dependency_os("actor_variant", "actv"),
        SEnum16("encounter_squad_handling",
            'inherit_from_old_unit',
            'inherit_from_attacker',
            'free_actor',
            ),
        Pad(2),
        SEnum16("team_handling",
            'inherit_from_old_unit',
            'inherit_from_attacker',
            'override',
            ),
        SEnum16("team_override", *unit_teams),
        SEnum16("initial_state_handling",
            'inherit',
            'override',
            ),
        SEnum16("initial_state_override", *actor_states),
        SEnum16("return_state_handling",
            'inherit',
            'override',
            'actor_default',
            ),
        SEnum16("return_state_override", *actor_states),
        Pad(4),
        ),

    Struct("animation",
        ascii_str32("transform_in_anim"),
        reflexive("keyframe_actions", keyframe_action, 9,
            DYN_NAME_PATH='.effect_marker'),
        COMMENT=animation_comment
        ),

    Struct("vitality",
        Pad(4),
        SEnum16("inheritance", *vitality_inheritance_overrides),
        SEnum16("override", *vitality_inheritance_overrides),
        Float("shield_override"),
        Float("health_override"),
        ),
    SIZE=172
    )

avti_body = Struct("tagdata",
    reflexive("targets", transform_in_target, 16,
        DYN_NAME_PATH='.target_name'),
    SIZE=36
    )

def get():
    return avti_def

avti_def = TagDef("avti",
    blam_header_os('avti', 1),
    avti_body,

    ext=".actor_variant_transform_in", endian=">", tag_cls=HekTag
    )
