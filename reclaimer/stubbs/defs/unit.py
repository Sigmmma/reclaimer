#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

'''
THIS DEFINITION IS INCORRECT BECAUSE THE UNIT STRUCTURE IS DIFFERENT THAN HALO'S
'''

from ...hek.defs.unit import *
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef

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
        "unknown24",
        "unknown25"
        ),
    ascii_str32('unknown1'),
    SEnum16('default_team', *unit_teams),
    SEnum16('constant_sound_volume', *sound_volumes),
    float_zero_to_inf('rider_damage_fraction'),
    dependency_stubbs('integrated_light_toggle', "effe"),
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

    BytearrayRaw('unknown2', SIZE=68),

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
    dependency_stubbs('spawned_actor', "actv"),
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
    dependency_stubbs('melee_damage', "jpt!"),
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

#def get():
#    return unit_def
del get

unit_def = TagDef("unit",
    blam_header_stubbs('unit', 2),
    unit_body,

    ext=".unit", endian=">"
    )
