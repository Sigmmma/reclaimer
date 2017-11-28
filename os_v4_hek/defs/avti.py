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

keyframe_action = Struct("keyframe action",
    SEnum16("keyframe",
        "primary",
        "secondary",
        "final",
        ),
    SEnum16("rider handling",
        'none',
        'kill',
        'eject',
        ),
    SEnum16("target",
        'self',
        'riders',
        ),
    Pad(2),
    dependency_os("damage effect", "jpt!"),
    dependency_os("effect", "effe"),
    ascii_str32("effect marker"),
    SIZE=72
    )

transform_in_target = Struct("transform in target",
    ascii_str32("target name"),
    Bool16("flags",
        'try to use existing unit',
        'drop weapon',
        'inherit seated units',
        'delete attached actors',
        ),

    Pad(2),
    QStruct("selection chances",
        Float("easy"), Float("normal"), Float("hard"), Float("imposs"),
        ORIENT="h"
        ),

    Struct("ai",
        dependency_os("actor variant", "actv"),
        SEnum16("encounter squad handling",
            'inherit from old unit',
            'inherit from attacker',
            'free actor',
            ),
        Pad(2),
        SEnum16("team handling",
            'inherit from old unit',
            'inherit from attacker',
            'override',
            ),
        SEnum16("team override", *unit_teams),
        SEnum16("initial state handling",
            'inherit',
            'override',
            ),
        SEnum16("initial state override", *actor_states),
        SEnum16("return state handling",
            'inherit',
            'override',
            'actor default',
            ),
        SEnum16("return state override", *actor_states),
        Pad(4),
        ),

    Struct("animation",
        ascii_str32("transform in anim"),
        reflexive("keyframe actions", keyframe_action, 9,
            DYN_NAME_PATH='.effect_marker'),
        COMMENT=animation_comment
        ),

    Struct("vitality",
        Pad(4),
        SEnum16("inheritance", *vitality_inheritance_overrides),
        SEnum16("override", *vitality_inheritance_overrides),
        Float("shield override"),
        Float("health override"),
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
