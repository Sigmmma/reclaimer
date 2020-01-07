#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

def get():
    return unit_def

camera_track = Struct('camera_track',
    dependency('track', "trak"),
    SIZE=28
    )

new_hud_interface = Struct('new_hud_interface',
    dependency('unit_hud_interface', "unhi"),
    SIZE=48
    )

dialogue_variant = Struct('dialogue_variant',
    SInt16('variant_number'),
    Pad(6),
    dependency('dialogue', "udlg"),
    SIZE=24
    )

powered_seat = Struct('powered_seat',
    Pad(4),
    float_sec('driver_powerup_time'),
    float_sec('driver_powerdown_time'),
    SIZE=68
    )

weapon = Struct('weapon',
    dependency('weapon', "weap"),
    SIZE=36
    )

seat = Struct('seat',
    Bool32("flags",
        "invisible",
        "locked",
        "driver",
        "gunner",
        "third_person_camera",
        "allows_weapons",
        "third_person_on_enter",
        "first_person_slaved_to_gun",
        "allow_vehicle_communcation_animation",
        "not_valid_without_driver",
        "allow_ai_noncombatants"
        ),
    ascii_str32('label'),
    ascii_str32('marker_name'),

    Pad(32),
    QStruct("acceleration_scale", INCLUDE=ijk_float),

    Pad(12),
    float_deg_sec('yaw_rate',   UNIT_SCALE=per_sec_unit_scale),  # degrees/sec
    float_deg_sec('pitch_rate', UNIT_SCALE=per_sec_unit_scale),  # degrees/sec
    ascii_str32('camera_marker_name'),
    ascii_str32('camera_submerged_marker_name'),
    float_rad('pitch_auto_level'),  # radians
    from_to_rad('pitch_range'),  # radians

    reflexive("camera_tracks", camera_track, 2, 'loose', 'tight'),
    reflexive("new_hud_interfaces", new_hud_interface, 2,
              'default/solo', 'multiplayer'),

    Pad(4),
    SInt16("hud_text_message_index"),

    Pad(2),
    float_rad('yaw_minimum'),  # radians
    float_rad('yaw_maximum'),  # radians
    dependency('built_in_gunner', "actv"),
    Pad(12),  # open sauce seat extension padding
    SIZE=284
    )

unit_attrs = Struct("unit_attrs",
    Bool32("flags",
        "circular_aiming",
        "destroyed_after_dying",
        "half_speed_interpolation",
        "fires_from_camera",
        "entrance_inside_bounding_sphere",
        "unused",
        "causes_passenger_dialogue",
        "resists_pings",
        "melee_attack_is_fatal",
        "dont_reface_during_pings",
        "has_no_aiming",
        "simple_creature",
        "impact_melee_attaches_to_unit",
        "impact_melee_dies_on_shields",
        "cannot_open_doors_automatically",
        "melee_attackers_cannot_attach",
        "not_instantly_killed_by_melee",
        "shield_sapping",
        "runs_around_flaming",
        "inconsequential",
        "special_cinematic_unit",
        "ignored_by_autoaiming",
        "shields_fry_infection_forms",
        "integrated_light_controls_weapon",
        "integrated_light_lasts_forever",
        ),
    SEnum16('default_team', *unit_teams),
    SEnum16('constant_sound_volume', *sound_volumes),
    float_zero_to_inf('rider_damage_fraction'),
    dependency('integrated_light_toggle', "effe"),
    SEnum16('A_in', *unit_inputs),
    SEnum16('B_in', *unit_inputs),
    SEnum16('C_in', *unit_inputs),
    SEnum16('D_in', *unit_inputs),
    float_rad('camera_field_of_view'),  # radians
    Float('camera_stiffness'),
    ascii_str32('camera_marker_name'),
    ascii_str32('camera_submerged_marker_name'),
    float_rad('pitch_auto_level'),  # radians
    from_to_rad('pitch_range'),  # radians
    reflexive("camera_tracks", camera_track, 2,
              'loose', 'tight'),

    #Miscellaneous
    QStruct("seat_acceleration_scale", INCLUDE=ijk_float),
    Pad(12),
    float_zero_to_one('soft_ping_threshold'),  # [0,1]
    float_sec('soft_ping_interrupt_time', UNIT_SCALE=sec_unit_scale),  # seconds
    float_zero_to_one('hard_ping_threshold'),  # [0,1]
    float_sec('hard_ping_interrupt_time', UNIT_SCALE=sec_unit_scale),  # seconds
    float_zero_to_one('hard_death_threshold'),  # [0,1]
    float_zero_to_one('feign_death_threshold'),  # [0,1]
    float_sec('feign_death_time', UNIT_SCALE=sec_unit_scale),  # seconds
    float_wu('distance_of_evade_aim'),  # world units
    float_wu('distance_of_dive_aim'),  # world units

    Pad(4),
    float_zero_to_one('stunned_movement_threshold'),  # [0,1]
    float_zero_to_one('feign_death_chance'),  # [0,1]
    float_zero_to_one('feign_repeat_chance'),  # [0,1]
    dependency('spawned_actor', "actv"),
    QStruct("spawned_actor_count",
        SInt16("from", GUI_NAME=""), SInt16("to"), ORIENT='h',
        ),
    float_wu_sec('spawned_velocity'),
    float_rad_sec('aiming_velocity_maximum',
                  UNIT_SCALE=irad_per_sec_unit_scale),  # radians/sec
    float_rad_sec_sq('aiming_acceleration_maximum',
                     UNIT_SCALE=irad_per_sec_sq_unit_scale),  # radians/sec^2
    float_zero_to_one('casual_aiming_modifier'),
    float_rad_sec('looking_velocity_maximum',
                  UNIT_SCALE=irad_per_sec_unit_scale),  # radians/sec
    float_rad_sec_sq('looking_acceleration_maximum',
                     UNIT_SCALE=irad_per_sec_sq_unit_scale),  # radians/sec^2

    Pad(8),
    Float('ai_vehicle_radius'),
    Float('ai_danger_radius'),
    dependency('melee_damage', "jpt!"),
    SEnum16('motion_sensor_blip_size',
        "medium",
        "small",
        "large",
        ),
    Pad(2),

    Pad(12),  # open sauce unit extension padding
    reflexive("new_hud_interfaces", new_hud_interface, 2,
        'default/solo', 'multiplayer'),
    reflexive("dialogue_variants", dialogue_variant, 16,
        DYN_NAME_PATH='.dialogue.filepath'),

    #Grenades
    float_wu_sec('grenade_velocity'),
    SEnum16('grenade_type', *grenade_types),
    SInt16('grenade_count', MIN=0),

    Pad(4),
    reflexive("powered_seats", powered_seat, 2,
              "driver", "gunner"),
    reflexive("weapons", weapon, 4, DYN_NAME_PATH='.weapon.filepath'),
    reflexive("seats", seat, 16, DYN_NAME_PATH='.label'),

    SIZE=372
    )

unit_body = Struct('tagdata',
    unit_attrs,
    SIZE=372
    )

unit_def = TagDef("unit",
    blam_header('unit', 2),
    unit_body,

    ext=".unit", endian=">", tag_cls=HekTag
    )
