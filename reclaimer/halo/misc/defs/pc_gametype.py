'''
    Adapted from source files located here
    https://github.com/Halogen002/Flare-Qt

    My thanks go to Halogen002 for providing me with
    the information I needed to write this definition.
    I extended it to include xbox gametypes as well
'''

from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef
from .objs.pc_gametype import PcGametypeTag

def get(): return pc_gametype_def

def is_xbox_gametype(node=None, parent=None, **kwargs):
    if parent is None:
        return node.get_root().is_xbox
    return parent.get_root().is_xbox

##################################################
'''Shared enumerators, booleans, and bitstructs'''
##################################################

enum_off_on = LUEnum32('',
    'off',
    'on',
    )
#why is is that two of the slayer specific booleans reverse the truthyness?
enum_on_off = LUEnum32('',
    'on',
    'off',
    )

speed_with_ball = LUEnum32('speed with ball',
    'slow',
    'normal',
    'fast',
    )

trait_with_ball = LUEnum32('trait with ball',
    'none',
    'invisible',
    'extra damage',
    'damage resistance',
    )

trait_without_ball = LUEnum32('trait without ball',
    'none',
    'invisible',
    'extra damage',
    'damage resistance',
    )

ball_type = LUEnum32('ball type',
    'normal',
    'reverse tag',
    'juggernaut',
    )

race_order = UEnum8('order',
    'normal',
    'any order',
    'rally',
    )

race_points_used = LUEnum32('points used',
    'minimum',
    'maximum',
    'sum'
    )

vehicle_spawn = LBitStruct("vehicle spawn",
    BitUEnum('vehicle type',
        'default',
        'none',
        'warthogs',
        'ghosts',
        'scorpions',
        'rocket warthogs',
        'banshees',
        'gun turrets',
        'custom',
        SIZE=4,
        ),
    BitUInt('warthogs',  SIZE=3),
    BitUInt('ghosts',    SIZE=3),
    BitUInt('scorpions', SIZE=3),
    BitUInt('rocket warthogs', SIZE=3),
    BitUInt('banshees',  SIZE=3),
    BitUInt('gun turrets', SIZE=3),
    SIZE=4,
    )

player_setting = LBool32("player setting",
    'radar enabled',
    'friend on hud',
    'infinite grenades',
    'shields disabled',
    'invisible',
    'generic weapons',
    'enemies not on radar',
    )

game_type = LUEnum32('game type',
    ('ctf', 1),
    ('slayer', 2),
    ('oddball', 3),
    ('king', 4),
    ('race', 5),
    DEFAULT=1
    )

objective_indicator = LUEnum32('objective indicator',
    'motion tracker',
    'nav point',
    'none',
    )

weapon_type = LUEnum32('weapon type',
    'default',
    'pistols',
    'rifles',
    'plasma rifles',
    'sniper',
    'no sniper',
    'rocket launchers',
    'shotguns',
    'short range',
    'human',
    'covenant',
    'classic',
    'heavy weapons',
    )

friendly_fire = LUEnum32('friendly fire',
    'off',
    'on',
    'shields',
    'explosions',
    )

vehicle_type = LUEnum32('vehicle type',
    'all',
    'none',
    'warthog',
    'ghost',
    'scorpion',
    )

##################################################
'''Structs for each of the different game types'''
##################################################

ctf_settings = Struct('ctf settings',
    #UEnum8('assault', INCLUDE=enum_off_on),
    #UInt8('unknown', VISIBLE=False),
    #UEnum8('flag must reset', INCLUDE=enum_off_on),
    #UEnum8('flag must be at home', INCLUDE=enum_off_on),

    # It looks better this way.
    # Make it a FlBool32 so it doesnt get screwed up for powerpc
    FlBool32('flags',
        ('assault', 1<<0),
        ('flag must reset', 1<<16),
        ('flag must be at home', 1<<24),
        ),
    LUInt32('single_flag_time'),# ticks
    SIZE=28,
    )

slayer_settings = Struct('slayer settings',
    #UEnum8('death bonus',   INCLUDE=enum_on_off),
    #UEnum8('kill penalty',  INCLUDE=enum_on_off),
    #UEnum8('kill in order', INCLUDE=enum_off_on),
    # It looks better this way.
    # Make it a FlBool32 so it doesnt get screwed up for powerpc
    FlBool32('flags',
        ('no death bonus', 1<<0),
        ('no kill penalty', 1<<8),
        ('kill in order', 1<<16),
        ),
    SIZE=28,
    )

oddball_settings = Struct('oddball settings',
    UEnum8('random ball', INCLUDE=enum_off_on),
    Pad(3),
    speed_with_ball,
    trait_with_ball,
    trait_without_ball,
    ball_type,
    LUInt32('ball_count', MIN=1, MAX=16),
    SIZE=28,
    )

king_settings = Struct('king settings',
    UEnum8('moving hill', INCLUDE=enum_off_on),
    SIZE=28,
    )

race_settings = Struct('race settings',
    race_order,
    Pad(3),
    race_points_used,
    SIZE=28,
    )

header_comment = \
'''  The length of an Xbox gametypes name is capped at 11
  characters, whereas a PC gametype name is capped at 23.

  Respawn times of 0 are "instant", which is still 3 seconds.
  Respawn times cap at 300 seconds(5 minutes or 9000 ticks)

  Health can be anywhere between 50% and 400%

  For PC gametypes, the max spawn for each kind of vehicle is 7.

  The score limit minimum is 1, and is measured in different
  units depending on what gametype this is:
      CTF -------- flags
      Slayer ----- kills
      King ------- minutes
      Oddball ---- points/minutes
      Race ------- laps'''

xbox_gametype_header = Struct("gametype header",
    LStrUtf16('name', SIZE=24),
    game_type,
    LUEnum32('teamplay', INCLUDE=enum_off_on),
    player_setting,
    objective_indicator,
    LUEnum32('odd man out', INCLUDE=enum_off_on),

    LUInt32('respawn time growth', SIDETIP="ticks [30 == 1 second]"), #ticks
    LUInt32('respawn time', SIDETIP="ticks [30 == 1 second]", MAX=300*30),
    LUInt32('respawn suicide penalty', SIDETIP="ticks [30 == 1 second]"), #ticks
    LUInt32('lives', SIDETIP='[0 == unlimited]'),
    LFloat('health', MIN=0.5, MAX=4.0, UNIT_SCALE=100, SIDETIP="%"),
    LUInt32('score limit', MIN=1),
    weapon_type,
    vehicle_type,
    SIZE=76, COMMENT=header_comment
    )


pc_gametype_header = Struct("gametype header",
    LStrUtf16('name', SIZE=48),
    game_type,
    LUEnum32('teamplay', INCLUDE=enum_off_on),
    player_setting,
    objective_indicator,
    LUEnum32('odd man out', INCLUDE=enum_off_on),

    LUInt32('respawn time growth', SIDETIP="ticks [30 == 1 second]"), #ticks
    LUInt32('respawn time', SIDETIP="ticks [30 == 1 second]", MAX=300*30),
    LUInt32('respawn suicide penalty', SIDETIP="ticks [30 == 1 second]"), #ticks
    LUInt32('lives', SIDETIP='[0 == unlimited]'),
    LFloat('health', MIN=0.5, MAX=4.0, UNIT_SCALE=100, SIDETIP="%"),
    LUInt32('score limit', MIN=1),
    weapon_type,

    LBitStruct('red vehicles',  INCLUDE=vehicle_spawn),
    LBitStruct('blue vehicles', INCLUDE=vehicle_spawn),

    LUInt32('vehicle respawn time', SIDETIP="ticks [30 == 1 second]"), #ticks
    friendly_fire,
    LUInt32('respawn betrayal penalty', SIDETIP="ticks [30 == 1 second]"), #ticks
    LUEnum32('auto team balance', INCLUDE=enum_off_on),
    LUInt32('time limit', SIDETIP="ticks [30 == 1 second]"), #ticks
    SIZE=124, COMMENT=header_comment
    )

xbox_gametype_footer = Container('gametype footer',
    #20 byte hmac sha1 digest of the save file
    BytesRaw('hmac_sig', SIZE=20),
    Pad(388),
    VISIBLE=False
    )

pc_gametype_footer = Struct('gametype footer',
    LUInt32('crc 32'),
    #its possible to make a gametype platform independent by keeping
    #a copy of the settings here as well in a bytearray buffer
    BytearrayRaw('hybrid settings', SIZE=28),
    Pad(32),
    LUInt32('crc 32 ce'),
    Pad(7972),
    VISIBLE=False
    )


header_switch = Switch('gametype header',
    DEFAULT=pc_gametype_header,
    CASE=is_xbox_gametype,
    CASES={True: xbox_gametype_header},
    )

union_settings_comment = '''
After you change these settings you'll still need to go into the
header and choose this gametypes type(ctf, slayer, race, etc).
'''

settings = Union('gametype settings',
    CASE='.gametype_header.game_type.enum_name',
    CASES={
        'ctf':ctf_settings,
        'slayer':slayer_settings ,
        'oddball':oddball_settings,
        'king':king_settings,
        'race':race_settings,
        },
    COMMENT=union_settings_comment
    )

footer_switch = Switch('gametype footer',
    DEFAULT=pc_gametype_footer,
    CASE=is_xbox_gametype,
    CASES={True: xbox_gametype_footer},
    )


pc_gametype_def = TagDef('pc_gametype',
    header_switch,
    settings,
    footer_switch,

    ext='.lst', endian='<', tag_cls=PcGametypeTag,
    )
