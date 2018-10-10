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

look_function = Struct("look function",
    Float('scale'),
    SIZE=4
    )

player_control = Struct("player control",
    Float('magnetism friction'),
    Float('magnetism adhesion'),
    Float('inconsequential target scale'),

    Pad(52),
    float_sec('look acceleration time'),
    Float('look acceleration scale'),
    float_zero_to_one('look peg threshold'),
    float_deg('look default pitch rate'),  # degrees
    float_deg('look default yaw rate'),  # degrees
    Float('look autolevelling scale'),

    Pad(20),
    SInt16('minimum weapon swap ticks'),
    SInt16('minimum autolevelling ticks'),
    float_rad('minimum angle for vehicle flip'),  # radians
    reflexive("look functions", look_function, 16),

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
    Struct("enemy scales",
        QStruct("damage", INCLUDE=difficulty_base),
        QStruct("vitality", INCLUDE=difficulty_base),
        QStruct("shield", INCLUDE=difficulty_base),
        QStruct("recharge", INCLUDE=difficulty_base),
        ),
    Struct("friend scales",
        QStruct("damage", INCLUDE=difficulty_base),
        QStruct("vitality", INCLUDE=difficulty_base),
        QStruct("shield", INCLUDE=difficulty_base),
        QStruct("recharge", INCLUDE=difficulty_base),
        ),
    QStruct("infection form vitality scales", INCLUDE=difficulty_base),

    Pad(16),
    # Enemy ranged fire
    Struct("ranged combat scales",
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
        ),

    Struct("close combat scales",
        QStruct("melee delay base",
            GUI_NAME="melee delay base(not a scale)", INCLUDE=difficulty_base
            ),
        QStruct("melee delay", INCLUDE=difficulty_base),
           
        Pad(16),
        # Grenades
        QStruct("grenade chance", INCLUDE=difficulty_base),
        QStruct("grenade timer", INCLUDE=difficulty_base),
        ),

    Pad(48),
    # Placement
    Struct("major upgrade fractions",
        QStruct("normal", INCLUDE=difficulty_base),
        QStruct("few", INCLUDE=difficulty_base),
        QStruct("many", INCLUDE=difficulty_base),
        ),

    SIZE=644
    )

grenade = Struct("grenade",
    SInt16('maximum count'),
    SInt16('mp spawn default'),
    dependency('throwing effect', "effe"),
    dependency('hud interface', "grhi"),
    dependency('equipment', "eqip"),
    dependency('projectile', "proj"),
    SIZE=68
    )

rasterizer_data = Struct("rasterizer data",
    Struct("function textures",
        dependency('distance attenuation', "bitm"),
        dependency('vector normalization', "bitm"),
        dependency('atmospheric fog density', "bitm"),
        dependency('planar fog density', "bitm"),
        dependency('linear corner fade', "bitm"),
        dependency('active camouflage distortion', "bitm"),
        dependency('glow', "bitm"),
        Pad(60),
        ),

    # Default textures
    Struct("default textures",
        dependency('default 2d', "bitm"),
        dependency('default 3d', "bitm"),
        dependency('default cubemap', "bitm"),
        ),

    # Experimental textures
    Struct("experimental textures",
        dependency('test0', "bitm"),
        dependency('test1', "bitm"),
        dependency('test2', "bitm"),
        dependency('test3', "bitm"),
        ),

    # video effect textures
    Struct("video effect textures",
        dependency('video scanline map', "bitm"),
        dependency('video noise map', "bitm"),
        Pad(52),
        ),

    # Active camouflage
    Struct("active camouflage",
        Bool16("flags",
            "tint edge density"
            ),
        Pad(2),
        Float('refraction amount', SIDETIP="pixels"),  # pixels
        Float('distance falloff'),
        QStruct('tint color', INCLUDE=rgb_float),
        Float('hyper-stealth refraction amount', SIDETIP="pixels"),  # pixels
        Float('hyper-stealth distance falloff'),
        QStruct('hyper-stealth tint color', INCLUDE=rgb_float),
        ),

    # PC textures
    dependency('distance attenuation 2d', "bitm"),

    SIZE=428
    )

interface_bitmaps = Struct("interface bitmaps",
    dependency('font system', "font"),
    dependency('font terminal', "font"),
    dependency('screen color table', "colo"),
    dependency('hud color table', "colo"),
    dependency('editor color table', "colo"),
    dependency('dialog color table', "colo"),
    dependency('hud globals', "hudg"),
    dependency('motion sensor sweep bitmap', "bitm"),
    dependency('motion sensor sweep bitmap mask', "bitm"),
    dependency('multiplayer hud bitmap', "bitm"),
    dependency('localization', "str#"),
    dependency('hud digits definition', "hud#"),
    dependency('motion sensor blip', "bitm"),
    dependency('interface goo map1', "bitm"),
    dependency('interface goo map2', "bitm"),
    dependency('interface goo map3', "bitm"),
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

multiplayer_information = Struct("multiplayer information",
    dependency('flag', valid_items),
    dependency('unit', valid_units),
    reflexive('vehicles', vehicle, 20, DYN_NAME_PATH='.vehicle.filepath'),
    dependency('hill shader', valid_shaders),
    dependency('flag shader', valid_shaders),
    dependency('ball', valid_items),
    reflexive('sounds', sound, 60, DYN_NAME_PATH='.sound.filepath'),
    SIZE=160
    )

player_information = Struct("player information",
    dependency('unit', valid_units),

    Pad(28),
    ####################################################
    #####                   IMPORTANT              #####
    ##### Because of how halo handles some things, #####
    ##### the below accelerations unit scales for  #####
    ##### 60fps must be cut by 2 rather than 4     #####
    ####################################################

    float_wu_sec("walking speed"),  # world units/second
    Float("double speed multiplier", SIDETIP="[1.0,+inf]", MIN=1.0),
    float_wu_sec("run forward"),  # world units/second
    float_wu_sec("run backward"),  # world units/second
    float_wu_sec("run sideways"),  # world units/second
    float_wu_sec_sq("run acceleration",
                    UNIT_SCALE=per_sec_unit_scale),  # world units/second^2
    float_wu_sec("sneak forward"),  # world units/second
    float_wu_sec("sneak backward"),  # world units/second
    float_wu_sec("sneak sideways"),  # world units/second
    float_wu_sec_sq("sneak acceleration",
                    UNIT_SCALE=per_sec_unit_scale),  # world units/second^2
    float_wu_sec_sq("airborne acceleration",
                    UNIT_SCALE=per_sec_unit_scale),  # world units/second^2
    Float("speed multiplier", SIDETIP="multiplayer only"),  # multiplayer only

    Pad(12),
    QStruct("grenade origin", INCLUDE=xyz_float),

    Pad(12),
    float_zero_to_one("stun movement penalty"),
    float_zero_to_one("stun turning penalty"),
    float_zero_to_one("stun jumping penalty"),
    Float("minimum stun time"),
    Float("maximum stun time"),

    Pad(8),
    from_to_sec("first person idle time"),
    float_zero_to_one("first person skip fraction"),

    Pad(16),
    dependency('coop respawn effect', "effe"),
    SIZE=244
    )

first_person_interface = Struct("first person interface",
    dependency('first person hands', valid_models),
    dependency('base bitmap', "bitm"),
    dependency('shield meter', "metr"),
    QStruct('shield meter origin',
        SInt16('x'), SInt16('y'), ORIENT='h'
        ),
    dependency('body meter', "metr"),
    QStruct('body meter origin',
        SInt16('x'), SInt16('y'), ORIENT='h'
        ),
    dependency('night-vision toggle on effect', "effe"),
    dependency('night-vision toggle off effect', "effe"),

    SIZE=192
    )

falling_damage = Struct("falling_damage",
    Pad(8),
    QStruct("harmful falling distance", INCLUDE=from_to),
    dependency('falling damage', "jpt!"),

    Pad(8),
    Float("maximum falling distance"),
    dependency('distance damage', "jpt!"),
    dependency('vehicle environment collision damage', "jpt!"),
    dependency('vehicle killed unit damage', "jpt!"),
    dependency('vehicle collision damage', "jpt!"),
    dependency('flaming death damage', "jpt!"),
    SIZE=152
    )

particle_effect = Struct("particle effect",
    dependency('particle type', "part"),
    Bool32("flags", *blend_flags),
    float_wu("density"),
    QStruct("velocity scale", INCLUDE=from_to),

    Pad(4),
    from_to_rad_sec("angular velocity"),  # radians/second

    Pad(8),
    from_to_wu("radius"),  # world units

    Pad(8),
    QStruct("tint lower bound", INCLUDE=argb_float),
    QStruct("tint upper bound", INCLUDE=argb_float),
    SIZE=128
    )

material = Struct("material",
    Pad(148),
    # Vehicle terrain parameters
    Float("ground friction scale"),
    Float("ground friction normal k1 scale"),
    Float("ground friction normal k0 scale"),
    Float("ground depth scale"),
    Float("ground damp fraction scale"),

    # Breakable surface parameters
    Pad(556),
    Float("maximum vitality"),

    Pad(12),
    dependency('effect', "effe"),
    dependency('sound', "snd!"),

    Pad(24),
    reflexive("particle effects", particle_effect, 8,
        DYN_NAME_PATH='.particle_type.filepath'),

    Pad(60),
    dependency('melee hit sound', "snd!"),
    SIZE=884
    )

playlist_member = Struct("playlist_member",
    ascii_str32("map name"),
    ascii_str32("game variant"),
    SInt32('minimum experience'),
    SInt32('maximum experience'),
    SInt32('minimum player count'),
    SInt32('maximum player count'),
    SInt32('rating'),
    SIZE=148
    )

matg_body = Struct('tagdata',
    Pad(248),
    reflexive("sounds", sound, 2,
        "enter water", "exit water"),
    reflexive("cameras", camera, 1),
    reflexive("player controls", player_control, 1),
    reflexive("difficulties", difficulty, 1),
    reflexive("grenades", grenade, 2, *grenade_types),
    reflexive("rasterizer datas", rasterizer_data, 1),
    reflexive("interface bitmaps", interface_bitmaps, 1),
    reflexive("cheat weapons", cheat_weapon, 20,
        DYN_NAME_PATH='.weapon.filepath'),
    reflexive("cheat powerups", cheat_powerup, 20,
        DYN_NAME_PATH='.powerup.filepath'),
    reflexive("multiplayer informations", multiplayer_information, 1),
    reflexive("player informations", player_information, 1),
    reflexive("first person interfaces", first_person_interface, 1),
    reflexive("falling damages", falling_damage, 1),
    reflexive("materials", material, len(materials_list), *materials_list),
    reflexive("playlist members", playlist_member, 20,
        DYN_NAME_PATH='.map_name'),

    SIZE=428
    )

matg_def = TagDef("matg",
    blam_header('matg', 3),
    matg_body,

    ext=".globals", endian=">", tag_cls=HekTag
    )
