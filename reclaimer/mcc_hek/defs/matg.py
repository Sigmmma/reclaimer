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
    return matg_def

camera = Struct("camera",
    dependency('camera', "trak"),
    SIZE=16
    )

sound = Struct("sound",
    dependency('sound', "snd!"),
    SIZE=16
    )

look_function = Struct("look_function",
    Float('scale'),
    SIZE=4
    )

player_control = Struct("player_control",
    Float('magnetism_friction'),
    Float('magnetism_adhesion'),
    Float('inconsequential_target_scale'),

    Pad(52),
    float_sec('look_acceleration_time'),
    Float('look_acceleration_scale'),
    float_zero_to_one('look_peg_threshold'),
    float_deg('look_default_pitch_rate'),  # degrees
    float_deg('look_default_yaw_rate'),  # degrees
    Float('look_autolevelling_scale'),

    Pad(20),
    SInt16('minimum_weapon_swap_ticks'),
    SInt16('minimum_autolevelling_ticks'),
    float_rad('minimum_angle_for_vehicle_flip'),  # radians
    reflexive("look_functions", look_function, 16),

    SIZE=128
    )

difficulty_base = QStruct("",
    Float("easy"),
    Float("normal"),
    Float("hard"),
    Float("imposs"),
    ORIENT='h'
    )

difficulty = Struct("difficulty",
    # Health
    Struct("enemy_scales",
        QStruct("damage", INCLUDE=difficulty_base),
        QStruct("vitality", INCLUDE=difficulty_base),
        QStruct("shield", INCLUDE=difficulty_base),
        QStruct("recharge", INCLUDE=difficulty_base),
        ),
    Struct("friend_scales",
        QStruct("damage", INCLUDE=difficulty_base),
        QStruct("vitality", INCLUDE=difficulty_base),
        QStruct("shield", INCLUDE=difficulty_base),
        QStruct("recharge", INCLUDE=difficulty_base),
        ),
    QStruct("infection_form_vitality_scales", INCLUDE=difficulty_base),

    Pad(16),
    # Enemy ranged fire
    Struct("ranged_combat_scales",
        QStruct("rate_of_fire", INCLUDE=difficulty_base),
        QStruct("projectile_error", INCLUDE=difficulty_base),
        QStruct("burst_error", INCLUDE=difficulty_base),
        QStruct("new_target_delay", INCLUDE=difficulty_base),
        QStruct("burst_separation", INCLUDE=difficulty_base),
        QStruct("target_tracking", INCLUDE=difficulty_base),
        QStruct("target_leading", INCLUDE=difficulty_base),
        QStruct("overcharge_chance", INCLUDE=difficulty_base),
        QStruct("special_fire_delay", INCLUDE=difficulty_base),
        QStruct("guidance_vs_player", INCLUDE=difficulty_base),
        ),

    Struct("close_combat_scales",
        QStruct("melee_delay_base",
            GUI_NAME="melee delay base(not a scale)", INCLUDE=difficulty_base
            ),
        QStruct("melee_delay", INCLUDE=difficulty_base),

        Pad(16),
        # Grenades
        QStruct("grenade_chance", INCLUDE=difficulty_base),
        QStruct("grenade_timer", INCLUDE=difficulty_base),
        ),

    Pad(48),
    # Placement
    Struct("major_upgrade_fractions",
        QStruct("normal", INCLUDE=difficulty_base),
        QStruct("few", INCLUDE=difficulty_base),
        QStruct("many", INCLUDE=difficulty_base),
        ),

    SIZE=644
    )

grenade = Struct("grenade",
    SInt16('maximum_count'),
    SInt16('mp_spawn_default'),
    dependency('throwing_effect', "effe"),
    dependency('hud_interface', "grhi"),
    dependency('equipment', "eqip"),
    dependency('projectile', "proj"),
    SIZE=68
    )

rasterizer_data = Struct("rasterizer_data",
    Struct("function_textures",
        dependency('distance_attenuation', "bitm"),
        dependency('vector_normalization', "bitm"),
        dependency('atmospheric_fog_density', "bitm"),
        dependency('planar_fog_density', "bitm"),
        dependency('linear_corner_fade', "bitm"),
        dependency('active_camouflage_distortion', "bitm"),
        dependency('glow', "bitm"),
        Pad(60),
        ),

    # Default textures
    Struct("default_textures",
        dependency('default_2d', "bitm"),
        dependency('default_3d', "bitm"),
        dependency('default_cubemap', "bitm"),
        ),

    # Experimental textures
    Struct("experimental_textures",
        dependency('test0', "bitm"),
        dependency('test1', "bitm"),
        dependency('test2', "bitm"),
        dependency('test3', "bitm"),
        ),

    # video effect textures
    Struct("video_effect_textures",
        dependency('video_scanline_map', "bitm"),
        dependency('video_noise_map', "bitm"),
        Pad(52),
        ),

    # Active camouflage
    Struct("active_camouflage",
        Bool16("flags",
            "tint_edge_density"
            ),
        Pad(2),
        Float('refraction_amount', SIDETIP="pixels"),  # pixels
        Float('distance_falloff'),
        QStruct('tint_color', INCLUDE=rgb_float),
        Float('hyper_stealth_refraction_amount', SIDETIP="pixels"),  # pixels
        Float('hyper_stealth_distance_falloff'),
        QStruct('hyper_stealth_tint_color', INCLUDE=rgb_float),
        ),

    # PC textures
    dependency('distance_attenuation_2d', "bitm"),

    SIZE=428
    )

interface_bitmaps = Struct("interface_bitmaps",
    dependency('font_system', "font"),
    dependency('font_terminal', "font"),
    dependency('screen_color_table', "colo"),
    dependency('hud_color_table', "colo"),
    dependency('editor_color_table', "colo"),
    dependency('dialog_color_table', "colo"),
    dependency('hud_globals', "hudg"),
    dependency('motion_sensor_sweep_bitmap', "bitm"),
    dependency('motion_sensor_sweep_bitmap_mask', "bitm"),
    dependency('multiplayer_hud_bitmap', "bitm"),
    dependency('localization', "str#"),
    dependency('hud_digits_definition', "hud#"),
    dependency('motion_sensor_blip', "bitm"),
    dependency('interface_goo_map1', "bitm"),
    dependency('interface_goo_map2', "bitm"),
    dependency('interface_goo_map3', "bitm"),
    SIZE=304
    )

cheat_weapon = Struct("weapon",
    dependency('weapon', valid_items),
    SIZE=16
    )

cheat_powerup = Struct("powerup",
    dependency('powerup', "eqip"),
    SIZE=16
    )

vehicle = Struct("vehicle",
    dependency('vehicle', "vehi"),
    SIZE=16
    )

multiplayer_information = Struct("multiplayer_information",
    dependency('flag', valid_items),
    dependency('unit', valid_units),
    reflexive('vehicles', vehicle, 20, DYN_NAME_PATH='.vehicle.filepath'),
    dependency('hill_shader', valid_shaders),
    dependency('flag_shader', valid_shaders),
    dependency('ball', valid_items),
    reflexive('sounds', sound, 60, DYN_NAME_PATH='.sound.filepath'),
    SIZE=160
    )

player_information = Struct("player_information",
    dependency('unit', valid_units),

    Pad(28),
    float_wu_sec("walking_speed"),  # world units/second
    Float("double_speed_multiplier", SIDETIP="[1.0,+inf]", MIN=1.0),
    float_wu_sec("run_forward"),  # world units/second
    float_wu_sec("run_backward"),  # world units/second
    float_wu_sec("run_sideways"),  # world units/second
    float_wu_sec_sq("run_acceleration",
                    UNIT_SCALE=per_sec_unit_scale),  # world units/second^2
    float_wu_sec("sneak_forward"),  # world units/second
    float_wu_sec("sneak_backward"),  # world units/second
    float_wu_sec("sneak_sideways"),  # world units/second
    float_wu_sec_sq("sneak_acceleration",
                    UNIT_SCALE=per_sec_unit_scale),  # world units/second^2
    float_wu_sec_sq("airborne_acceleration",
                    UNIT_SCALE=per_sec_unit_scale),  # world units/second^2
    Float("speed_multiplier", SIDETIP="multiplayer only"),  # multiplayer only

    Pad(12),
    QStruct("grenade_origin", INCLUDE=xyz_float),

    Pad(12),
    float_zero_to_one("stun_movement_penalty"),
    float_zero_to_one("stun_turning_penalty"),
    float_zero_to_one("stun_jumping_penalty"),
    Float("minimum_stun_time"),
    Float("maximum_stun_time"),

    Pad(8),
    from_to_sec("first_person_idle_time"),
    float_zero_to_one("first_person_skip_fraction"),

    Pad(16),
    dependency('coop_respawn_effect', "effe"),
    SIZE=244
    )

first_person_interface = Struct("first_person_interface",
    dependency('first_person_hands', valid_models),
    dependency('base_bitmap', "bitm"),
    dependency('shield_meter', "metr"),
    QStruct('shield_meter_origin',
        SInt16('x'), SInt16('y'), ORIENT='h'
        ),
    dependency('body_meter', "metr"),
    QStruct('body_meter_origin',
        SInt16('x'), SInt16('y'), ORIENT='h'
        ),
    dependency('night_vision_toggle_on_effect', "effe"),
    dependency('night_vision_toggle_off_effect', "effe"),

    SIZE=192
    )

falling_damage = Struct("falling_damage",
    Pad(8),
    QStruct("harmful_falling_distance", INCLUDE=from_to),
    dependency('falling_damage', "jpt!"),

    Pad(8),
    Float("maximum_falling_distance"),
    dependency('distance_damage', "jpt!"),
    dependency('vehicle_environment_collision_damage', "jpt!"),
    dependency('vehicle_killed_unit_damage', "jpt!"),
    dependency('vehicle_collision_damage', "jpt!"),
    dependency('flaming_death_damage', "jpt!"),
    SIZE=152
    )

particle_effect = Struct("particle_effect",
    dependency('particle_type', "part"),
    Bool32("flags", *blend_flags),
    float_wu("density"),
    QStruct("velocity_scale", INCLUDE=from_to),

    Pad(4),
    from_to_rad_sec("angular_velocity"),  # radians/second

    Pad(8),
    from_to_wu("radius"),  # world units

    Pad(8),
    QStruct("tint_lower_bound", INCLUDE=argb_float),
    QStruct("tint_upper_bound", INCLUDE=argb_float),
    SIZE=128
    )

material = Struct("material",
    Pad(148),
    # Vehicle terrain parameters
    Float("ground_friction_scale"),
    Float("ground_friction_normal_k1_scale"),
    Float("ground_friction_normal_k0_scale"),
    Float("ground_depth_scale"),
    Float("ground_damp_fraction_scale"),

    # Breakable surface parameters
    Pad(556),
    Float("maximum_vitality"),

    Pad(12),
    dependency('effect', "effe"),
    dependency('sound', "snd!"),

    Pad(24),
    reflexive("particle_effects", particle_effect, 8,
        DYN_NAME_PATH='.particle_type.filepath'),

    Pad(60),
    dependency('melee_hit_sound', "snd!"),
    SIZE=884
    )

playlist_member = Struct("playlist_member",
    ascii_str32("map_name"),
    ascii_str32("game_variant"),
    SInt32('minimum_experience'),
    SInt32('maximum_experience'),
    SInt32('minimum_player_count'),
    SInt32('maximum_player_count'),
    SInt32('rating'),
    SIZE=148
    )

matg_body = Struct('tagdata',
    Pad(248),
    reflexive("sounds", sound, 2,
        "enter water", "exit water"),
    reflexive("cameras", camera, 1),
    reflexive("player_controls", player_control, 1),
    reflexive("difficulties", difficulty, 1),
    reflexive("grenades", grenade, 2, *grenade_types),
    reflexive("rasterizer_datas", rasterizer_data, 1),
    reflexive("interface_bitmaps", interface_bitmaps, 1),
    reflexive("cheat_weapons", cheat_weapon, 20,
        DYN_NAME_PATH='.weapon.filepath'),
    reflexive("cheat_powerups", cheat_powerup, 20,
        DYN_NAME_PATH='.powerup.filepath'),
    reflexive("multiplayer_informations", multiplayer_information, 1),
    reflexive("player_informations", player_information, 1),
    reflexive("first_person_interfaces", first_person_interface, 1),
    reflexive("falling_damages", falling_damage, 1),
    reflexive("materials", material, len(materials_list), *materials_list),
    reflexive("playlist_members", playlist_member, 20,
        DYN_NAME_PATH='.map_name'),

    SIZE=428
    )

matg_def = TagDef("matg",
    blam_header('matg', 3),
    matg_body,

    ext=".globals", endian=">", tag_cls=HekTag
    )
