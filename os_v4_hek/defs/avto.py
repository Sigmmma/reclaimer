from .avti import *
from ...hek.defs.objs.tag import HekTag

instigators_comment = """
Controls which attacking unit type can trigger this transform.
Transforms with instigators will only be used when transform on damage is enabled.
"""

animations_comment = """
Played when the transform criteria have been met.
The actor is made braindead during the animation, and if the invincibility
flag is set, they cannot be killed once the animation begins.
"""

attachments_comment = """
The listed attachments will be added to the unit when it's transformation
begins. When specifying a single destination marker the destination marker
name will be used as-is(ex: 'marker'), however when the marker count is
more than 1, an index will be appended('marker0', 'marker1', etc.)
"""

instigator = Struct("instigator",
    dependency_os("unit", valid_units),
    SEnum16("damage type",
        'both',
        'weapon damage only',
        'melee damage only',
        ),
    SIZE=32, COMMENT=instigators_comment
    )

attachment = Struct("attachment",
    dependency_os("object", valid_objects),
    ascii_str32("object marker"),
    ascii_str32("destination marker"),
    SInt16("destination marker count"),
    Pad(2),
    SEnum16("team handling",
        'inherit from old unit',
        'inherit from attacker',
        'override',
        ),
    SEnum16("team override", *unit_teams),
    QStruct("attachment scale", INCLUDE=from_to),
    SIZE=120
    )

avto_body = Struct("tagdata",
    Bool16("flags",
        'invincible_during_transform_out',
        ),
    Pad(2),

    Struct("transform criteria",
        Bool16("flags",
            'transform_on_damage',
            'ignore_friendly_fire',
            'transform_on_actor_action',
            'transform_on_actor_state',
            'transform_on_shield_range',
            'transform_on_health_range',
            ),
        Pad(2),
        Bool16("actor action",
            'none',
            'sleep',
            'alert',
            'fight',
            'flee',
            'uncover',
            'guard',
            'search',
            'wait',
            'vehicle',
            'charge',
            'obey',
            'converse',
            'avoid',
            ),
        Bool16("actor state",
            'none',
            'sleeping',
            'alert',
            'moving_repeat_same_position',
            'moving_loop',
            'moving_loop_back_and_forth',
            'moving_loop_randomly',
            'moving_randomly',
            'guarding',
            'guarding_at_guard_position',
            'searching',
            'fleeing',
            ),
        from_to_zero_to_one("shield range"),
        from_to_zero_to_one("health range"),
        Pad(24),
        ),

    reflexive("transform instigators", instigator, 16,
        DYN_NAME_PATH='.unit.filepath'),

    Struct("animation",
        ascii_str32("transform in anim"),
        reflexive("keyframe actions", keyframe_action, 9,
            DYN_NAME_PATH='.effect_marker'),
        COMMENT=animation_comment
        ),

    Struct("attachments",
        Bool16("flags",
            "destroy attachments on death",
            ),
        Pad(2),
        reflexive("attachments", attachment, 16,
            DYN_NAME_PATH='.object.filepath'),
        Pad(24),
        COMMENT=attachments_comment,
        ),
    SIZE=148
    )

def get():
    return avto_def

avto_def = TagDef("avto",
    blam_header_os('avto', 1),
    avto_body,

    ext=".actor_variant_transform_out", endian=">", tag_cls=HekTag
    )
