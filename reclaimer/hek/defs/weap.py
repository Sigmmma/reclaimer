#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from .obje import *
from .item import *
from .objs.weap import WeapTag

# replace the object_type enum one that uses
# the correct default value for this object
obje_attrs = dict(obje_attrs)
obje_attrs[0] = dict(obje_attrs[0], DEFAULT=2)

magazine_item = Struct("magazine_item",
    SInt16("rounds"),

    Pad(10),
    dependency('equipment', "eqip"),
    SIZE=28
    )

magazine = Struct("magazine",
    Bool32("flags",
        "wastes_rounds_when_reloaded",
        "every_round_must_be_chambered"
        ),
    SInt16("rounds_recharged", SIDETIP="per second"),
    SInt16("rounds_total_initial"),
    SInt16("rounds_total_maximum"),
    SInt16("rounds_loaded_maximum"),

    Pad(8),
    float_sec("reload_time"),
    SInt16("rounds_reloaded"),

    Pad(2),
    float_sec("chamber_time"),

    Pad(24),
    dependency('reloading_effect', valid_event_effects),
    dependency('chambering_effect', valid_event_effects),

    Pad(12),
    reflexive("magazine_items", magazine_item, 2,
        "primary", "secondary"),
    SIZE=112
    )

firing_effect = Struct("firing_effect",
    SInt16("shot_count_lower_bound"),
    SInt16("shot_count_upper_bound"),

    Pad(32),
    dependency('firing_effect', valid_event_effects),
    dependency('misfire_effect', valid_event_effects),
    dependency('empty_effect', valid_event_effects),
    dependency('firing_damage', "jpt!"),
    dependency('misfire_damage', "jpt!"),
    dependency('empty_damage', "jpt!"),
    SIZE=132
    )

trigger = Struct("trigger",
    Bool32("flags",
        "tracks_fired_projectile",
        "random_firing_effects",
        "can_fire_with_partial_ammo",
        "does_not_repeat_automatically",
        "locks_in_on_off_state",
        "projectiles_use_weapon_origin",
        "sticks_when_dropped",
        "ejects_during_chamber",
        "discharging_spews",
        "analog_rate_of_fire",
        "use_error_when_unzoomed",
        "projectile_vector_cannot_be_adjusted",
        "projectiles_have_identical_error",
        "projectile_is_client_side_only",
        ),
    Struct("firing",
        QStruct("rounds_per_second",
            Float("from", UNIT_SCALE=per_sec_unit_scale, GUI_NAME=''),
            Float("to",   UNIT_SCALE=per_sec_unit_scale),
            ORIENT='h'
            ),
        float_sec("acceleration_time"),
        float_sec("deceleration_time"),
        Float("blurred_rate_of_fire", UNIT_SCALE=per_sec_unit_scale),

        Pad(8),
        SEnum16("magazine",
            'primary',
            'secondary',
            ('NONE', -1),
            DEFAULT=-1
            ),
        SInt16("rounds_per_shot"),
        SInt16("minimum_rounds_loaded"),
        SInt16("rounds_between_tracers"),

        Pad(6),
        SEnum16("firing_noise", *sound_volumes),
        from_to_zero_to_one("error"),
        float_sec("error_acceleration_time"),
        float_sec("error_deceleration_time"),
        ),

    Pad(8),
    Struct("charging",
        float_sec("charging_time"),
        float_sec("charge_hold_time"),
        SEnum16("overcharged_action",
            'none',
            'explode',
            'discharge',
            ),

        Pad(2),
        float_zero_to_one("charged_illumination"),
        float_sec("spew_time"),
        dependency('charging_effect', valid_event_effects),
        ),

    Struct("projectile",
        SEnum16("distribution_function",
            'point',
            'horizontal_fan',
            ),
        SInt16("projectiles_per_shot"),
        float_deg("distribution_angle"),  # degrees

        Pad(4),
        float_rad("minimum_error"),  # radians
        from_to_rad("error_angle"),  # radians
        QStruct("first_person_offset", INCLUDE=xyz_float),

        Pad(4),
        dependency('projectile', valid_objects),
        ),

    Struct("misc",
        float_sec("ejection_port_recovery_time"),
        float_sec("illumination_recovery_time"),

        Pad(12),
        float_zero_to_one("heat_generated_per_round"),
        float_zero_to_one("age_generated_per_round"),

        Pad(4),
        float_sec("overload_time"),

        Pad(40),
        ),

    QStruct("misc_rates",
        Float("ejection_port_recovery_rate"),
        Float("illumination_recovery_rate"),
        Float("acceleration_rate"),
        Float("deceleration_rate"),
        Float("error_acceleration_rate"),
        Float("error_deceleration_rate"),
        VISIBLE=False,
        COMMENT="\
These are various rates that are calculated when the weapon is compiled into a map."
        ),
    reflexive("firing_effects", firing_effect, 8),

    SIZE=276
    )

weap_attrs = Struct("weap_attrs",
    Bool32("flags",
        "vertical_heat_display",
        "mutually_exclusive_triggers",
        "attacks_automatically_on_bump",
        "must_be_readied",
        "doesnt_count_toward_maximum",
        "aim_assists_only_when_zoomed",
        "prevents_grenade_throwing",
        "must_be_picked_up",
        "holds_triggers_when_dropped",
        "prevents_melee_attack",
        "detonates_when_dropped",
        "cannot_fire_at_maximum_age",
        "secondary_trigger_overrides_grenades",
        "does_not_depower_active_camo_in_multiplayer",  # obsolete
        "enables_integrated_night_vision",
        "ai_uses_weapon_melee_damage"
        ),
    ascii_str32('label'),
    SEnum16('secondary_trigger_mode',
        "normal",
        "slaved_to_primary",
        "inhibits_primary",
        "loads_alternate_ammunition",
        "loads_multiple_primary_ammunition",
        ),
    SInt16("max_alternate_shots_loaded"),
    SEnum16('A_in', *weapon_export_to),
    SEnum16('B_in', *weapon_export_to),
    SEnum16('C_in', *weapon_export_to),
    SEnum16('D_in', *weapon_export_to),
    float_sec("ready_time"),
    dependency('ready_effect', valid_event_effects),

    Struct("heat",
        float_zero_to_one("recovery_threshold"),
        float_zero_to_one("overheated_threshold"),
        float_zero_to_one("detonation_threshold"),
        float_zero_to_one("detonation_fraction"),
        float_zero_to_inf("loss_per_second", UNIT_SCALE=per_sec_unit_scale),
        float_zero_to_one("illumination"),

        Pad(16),
        dependency('overheated', valid_event_effects),
        dependency('detonation', valid_event_effects),
        ),

    Struct("melee",
        dependency('player_damage', "jpt!"),
        dependency('player_response', "jpt!"),
        ),

    Pad(8),
    Struct("aiming",
        dependency("actor_firing_parameters", "actv"),
        float_wu("near_reticle_range"),  # world units
        float_wu("far_reticle_range"),  # world units
        float_wu("intersection_reticle_range"),  # world units

        Pad(2),
        SInt16("zoom_levels"),
        QStruct("zoom_ranges", INCLUDE=from_to),
        float_rad("autoaim_angle"),  # radians
        float_wu("autoaim_range"),  # world units
        float_rad("magnetism_angle"),  # radians
        float_wu("magnetism_range"),  # world units
        float_rad("deviation_angle"),  # radians
        ),

    Pad(4),
    Struct("movement",
        SEnum16('penalized',
            "always",
            "when_zoomed",
            "when_zoomed_or_reloading",
            ),
        Pad(2),
        Float("forward_penalty"),
        Float("sideways_penalty"),
        ),

    Pad(4),
    Struct("ai_targeting",
        Float("minimum_target_range"),
        Float("looking_time_modifier")
        ),

    Pad(4),
    Struct("light",
        float_sec('power_on_time',  UNIT_SCALE=sec_unit_scale),
        float_sec('power_off_time', UNIT_SCALE=sec_unit_scale),
        dependency('power_on_effect', valid_event_effects),
        dependency('power_off_effect', valid_event_effects)
        ),

    Struct("age",
        Float("heat_penalty"),
        Float("rate_of_fire_penalty"),
        float_zero_to_one("misfire_start"),
        float_zero_to_one("misfire_chance")
        ),

    Pad(12),
    Struct("interface",
        dependency('first_person_model', valid_models),
        dependency('first_person_animations', "antr"),

        Pad(4),
        dependency('hud_interface', "wphi"),
        dependency('pickup_sound', "snd!"),
        dependency('zoom_in_sound', "snd!"),
        dependency('zoom_out_sound', "snd!"),

        Pad(12),
        Float('active_camo_ding'),
        Float('active_camo_regrowth_rate', UNIT_SCALE=per_sec_unit_scale),
        ),

    Pad(14),
    SEnum16('weapon_type', *weapon_types),

    reflexive("predicted_resources", predicted_resource, 1024, VISIBLE=False),
    reflexive("magazines", magazine, 2,
        "primary", "secondary"),
    reflexive("triggers", trigger, 2,
        "primary", "secondary"),

    SIZE=512
    )

weap_body = Struct("tagdata",
    obje_attrs,
    item_attrs,
    weap_attrs,
    SIZE=1288,
    )


def get():
    return weap_def

weap_def = TagDef("weap",
    blam_header('weap', 2),
    weap_body,

    ext=".weapon", endian=">", tag_cls=WeapTag
    )
