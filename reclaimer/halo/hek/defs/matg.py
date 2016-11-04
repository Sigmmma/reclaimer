from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return matg_def

camera = dependency('track', valid_camera_tracks)

sound = dependency('sound', valid_sounds)

look_function = Struct("look function",
    BFloat('scale'),
    SIZE=4
    )

player_control = Struct("player control",
    BFloat('magnetism friction', MIN=0.0, MAX=1.0),
    BFloat('magnetism adhesion', MIN=0.0, MAX=1.0),
    BFloat('inconsequential target scale', MIN=0.0, MAX=1.0),

    Pad(52),
    BFloat('look acceleration time'),
    BFloat('look acceleration scale'),
    BFloat('look peg threshold', MIN=0.0, MAX=1.0),
    BFloat('look default pitch rate'),  # radians
    BFloat('look default yaw rate'),  # radians
    BFloat('look autolevelling scale'),

    Pad(20),
    BSInt16('minimum weapon swap ticks'),
    BSInt16('minimum autolevelling ticks'),
    BFloat('minimum angle for vehicle flip'),  # radians
    reflexive("look function", look_function, 16),

    SIZE=128
    )

difficulty_base = QStruct("",
    BFloat("easy"),
    BFloat("normal"),
    BFloat("hard"),
    BFloat("legendary")
    )

difficulty = Struct("difficulty",
    # Health
    Struct("enemy",
        QStruct("damage", INCLUDE=difficulty_base),
        QStruct("vitality", INCLUDE=difficulty_base),
        QStruct("shield", INCLUDE=difficulty_base),
        QStruct("recharge", INCLUDE=difficulty_base),
        ),
    Struct("friend",
        QStruct("damage", INCLUDE=difficulty_base),
        QStruct("vitality", INCLUDE=difficulty_base),
        QStruct("shield", INCLUDE=difficulty_base),
        QStruct("recharge", INCLUDE=difficulty_base),
        ),
    QStruct("infection forms", INCLUDE=difficulty_base),

    Pad(16),
    # Enemy ranged fire
    Struct("ranged fire",
        QStruct("rate of fire", INCLUDE=difficulty_base),
        QStruct("projectile error", INCLUDE=difficulty_base),
        QStruct("burst error", INCLUDE=difficulty_base),
        QStruct("new target delay", INCLUDE=difficulty_base),
        QStruct("burst separation", INCLUDE=difficulty_base),
        QStruct("target tracking", INCLUDE=difficulty_base),
        QStruct("target leading", INCLUDE=difficulty_base),
        QStruct("overcharge chance", INCLUDE=difficulty_base),
        QStruct("special fire delay", INCLUDE=difficulty_base),
        QStruct("guidance vs player", INCLUDE=difficulty_base),
        QStruct("melee delay base", INCLUDE=difficulty_base),
        QStruct("melee delay scale", INCLUDE=difficulty_base)
        ),

    Pad(16),
    # Grenades
    QStruct("grenade chance scale", INCLUDE=difficulty_base),
    QStruct("grenade timer scale", INCLUDE=difficulty_base),

    Pad(48),
    # Placement
    QStruct("major upgrade normal", INCLUDE=difficulty_base),
    QStruct("major upgrade few", INCLUDE=difficulty_base),
    QStruct("major upgrade many", INCLUDE=difficulty_base),

    SIZE=644
    )

grenade = Struct("grenade",
    BSInt16('maximum count'),
    BSInt16('mp spawn default'),
    dependency('throwing effect', valid_effects),
    dependency('hud interface', valid_grenade_hud_interfaces),
    dependency('equipment', valid_equipment),
    dependency('projectile', valid_projectiles),
    SIZE=68
    )

rasterizer_data = Struct("rasterizer data",
    # Function textures
    dependency('distance attenuation', valid_bitmaps),
    dependency('vector normalization', valid_bitmaps),
    dependency('atmospheric fog density', valid_bitmaps),
    dependency('planar fog density', valid_bitmaps),
    dependency('linear corner fade', valid_bitmaps),
    dependency('active camouflage distortion', valid_bitmaps),
    dependency('glow', valid_bitmaps),

    Pad(60),
    # Default textures
    dependency('default 2d', valid_bitmaps),
    dependency('default 3d', valid_bitmaps),
    dependency('default cubemap', valid_bitmaps),

    # Experimental textures
    dependency('test0', valid_bitmaps),
    dependency('test1', valid_bitmaps),
    dependency('test2', valid_bitmaps),
    dependency('test3', valid_bitmaps),

    # video effect textures
    dependency('video scanline map', valid_bitmaps),
    dependency('video noise map', valid_bitmaps),

    Pad(52),
    # Active camouflage
    BBool16("flags",
        "tint edge density"
        ),
    Pad(2),
    BFloat('refration amount'),  # pixels
    BFloat('distance falloff'),
    QStruct('tint color', INCLUDE=rgb_float),
    BFloat('hyper-stealth refration amount'),  # pixels
    BFloat('hyper-stealth distance falloff'),
    QStruct('hyper-stealth tint color', INCLUDE=rgb_float),

    # PC textures
    dependency('distance attenuation 2d', valid_bitmaps),

    SIZE=428
    )

interface_bitmaps = Struct("interface bitmaps",
    dependency('font system', valid_fonts),
    dependency('font terminal', valid_fonts),
    dependency('screen color table', valid_color_tables),
    dependency('hud color table', valid_color_tables),
    dependency('editor color table', valid_color_tables),
    dependency('dialog color table', valid_color_tables),
    dependency('hud globals', valid_hud_globals),
    dependency('motion sensor sweep bitmap', valid_bitmaps),
    dependency('motion sensor sweep bitmap mask', valid_bitmaps),
    dependency('multiplayer hud bitmap', valid_bitmaps),
    dependency('localization', valid_strings),
    dependency('hud digits definition', valid_hud_numbers),
    dependency('motion sensor blip', valid_bitmaps),
    dependency('interface goo map1', valid_bitmaps),
    dependency('interface goo map2', valid_bitmaps),
    dependency('interface goo map3', valid_bitmaps),
    SIZE=304
    )

cheat_weapon = dependency('weapon', valid_items)

cheat_powerup = dependency('powerup', valid_equipment)

vehicle = dependency('powerup', valid_vehicles)

multiplayer_information = Struct("multiplayer information",
    dependency('flag', valid_items),
    dependency('unit', valid_units),
    reflexive('vehicles', vehicle, 20),
    dependency('hill shader', valid_shaders),
    dependency('flag shader', valid_shaders),
    dependency('ball', valid_items),
    reflexive('sounds', sound, 60),
    SIZE=160
    )

player_information = Struct("player information",
    dependency('unit', valid_units),

    Pad(28),
    BFloat("walking speed"),  # world units/second
    BFloat("double speed multiplier"),
    BFloat("run forward"),  # world units/second
    BFloat("run backward"),  # world units/second
    BFloat("run sideways"),  # world units/second
    BFloat("run acceleration"),  # world units/second^2
    BFloat("sneak forward"),  # world units/second
    BFloat("sneak backward"),  # world units/second
    BFloat("sneak sideways"),  # world units/second
    BFloat("sneak acceleration"),  # world units/second^2
    BFloat("airborne acceleration"),  # world units/second^2
    BFloat("speed multiplier"),  # multiplayer only

    Pad(12),
    QStruct("grenade origin", INCLUDE=xyz_float),

    Pad(12),
    BFloat("stun movement penalty", MIN=0.0, MAX=1.0),
    BFloat("stun turning penalty", MIN=0.0, MAX=1.0),
    BFloat("stun jumping penalty", MIN=0.0, MAX=1.0),
    BFloat("minimum stun time"),
    BFloat("maximum stun time"),

    Pad(8),
    QStruct("first person idle time", INCLUDE=from_to),
    BFloat("first person  skip fraction", MIN=0.0, MAX=1.0),

    Pad(16),
    dependency('coop respawn effect', valid_effects),
    SIZE=244
    )

first_person_interface = Struct("first person interface",
    dependency('first person hands', valid_models),
    dependency('base bitmap', valid_bitmaps),
    dependency('shield meter', valid_meters),
    QStruct('shield meter origin',
        BSInt16('x'),
        BSInt16('y')
        ),
    dependency('body meter', valid_meters),
    QStruct('body meter origin',
        BSInt16('x'),
        BSInt16('y')
        ),
    dependency('night-vision toggle on effect', valid_effects),
    dependency('night-vision toggle off effect', valid_effects),

    SIZE=192
    )

falling_damage = Struct("falling_damage",
    Pad(8),
    QStruct("harmful falling distance", INCLUDE=from_to),
    dependency('falling damage', valid_damage_effects),

    Pad(8),
    BFloat("maximum falling distance"),
    dependency('distance damage', valid_damage_effects),
    dependency('vehicle environment collision damage', valid_damage_effects),
    dependency('vehicle killed unit damage', valid_damage_effects),
    dependency('vehicle collision damage', valid_damage_effects),
    dependency('flaming death damage', valid_damage_effects),
    SIZE=152
    )

particle_effect = Struct("particle effect",
    dependency('particle type', valid_particles),
    BBool32("flags", *blend_flags),
    BFloat("density"),
    QStruct("velocity scale", INCLUDE=from_to),

    Pad(4),
    QStruct("angular velocity", INCLUDE=from_to),  # radians/second

    Pad(8),
    QStruct("radius", INCLUDE=from_to),  # world units

    Pad(8),
    QStruct("tint lower bound", INCLUDE=argb_float),
    QStruct("tint upper bound", INCLUDE=argb_float),
    SIZE=128
    )

material = Struct("material",
    Pad(148),
    # Vehicle terrain parameters
    BFloat("ground friction scale"),
    BFloat("ground friction normal k1 scale"),
    BFloat("ground friction normal k0 scale"),
    BFloat("ground depth scale"),
    BFloat("ground damp fraction scale"),

    # Breakable surfaceparameters
    Pad(556),
    BFloat("maximum vitality"),

    Pad(12),
    dependency('effect', valid_effects),
    dependency('sound', valid_sounds),

    Pad(24),
    reflexive("particle effects", particle_effect, 8),

    Pad(60),
    dependency('melee hit sound', valid_sounds),
    SIZE=884
    )

playlist_member = Struct("playlist_member",
    ascii_str32("map name"),
    ascii_str32("game variant"),
    BSInt32('minimum experience'),
    BSInt32('maximum experience'),
    BSInt32('minimum player count'),
    BSInt32('maximum player count'),
    BSInt32('rating'),
    SIZE=148
    )

matg_body = Struct('tagdata',
    Pad(248),
    reflexive("sounds", sound, 2,
        "enter water", "exit water"),
    reflexive("camera", camera, 1),
    reflexive("player control", player_control, 1),
    reflexive("difficulty", difficulty, 1),
    reflexive("grenades", grenade, 2, *grenade_types),
    reflexive("rasterizer data", rasterizer_data, 1),
    reflexive("interface bitmaps", interface_bitmaps, 1),
    reflexive("cheat weapons", cheat_weapon, 20),
    reflexive("cheat powerups", cheat_powerup, 20),
    reflexive("multiplayer information", multiplayer_information, 1),
    reflexive("player information", player_information, 1),
    reflexive("first person interface", first_person_interface, 1),
    reflexive("falling damage", falling_damage, 1),
    reflexive("materials", material,
        len(materials_list), *(mat_name for mat_name in materials_list)),
    reflexive("playlist members", playlist_member, 20),

    SIZE=428
    )

matg_def = TagDef("matg",
    blam_header('matg', 3),
    matg_body,

    ext=".globals", endian=">"
    )
