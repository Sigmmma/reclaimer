'''
    adapted from source file located here
    https://github.com/Halogen002/Flare-Qt
'''

typedef uint16_t unichar;

typedef struct HaloVehicleSpawn {
    unsigned int type : 4;
    unsigned int warthogs : 3;
    unsigned int ghosts : 3;
    unsigned int scorpions : 3;
    unsigned int rocket_warthogs : 3;
    unsigned int banshees : 3;
    unsigned int gun_turrets : 3;
    unsigned int padding : 10;
} HaloVehicleSpawn;

typedef struct HaloPlayerSetting {
    unsigned int playerOnRadar : 1;
    unsigned int friendOnHud : 1;
    unsigned int infiniteGrenades : 1;
    unsigned int shieldsDisabled : 1;
    unsigned int invisible : 1;
    unsigned int weaponsGeneric : 1;
    unsigned int hideEnemiesFromRadar : 1;
    unsigned int padding : 25;
} HaloPlayerSetting;

typedef struct HaloGametypeBase {
    unichar name[24]; #0 - null terminated
    int32_t gametype; #0x30 - 1 = CTF, 2 = Slayer, 3 = Oddball, 4 = King, 5 = Race
    int32_t team_play; #0x34 - 0/1
    HaloPlayerSetting player_settings;   #0x38 - BITMASK: 0 = players on radar, 1 = friends on hud, 2 = infinite grenades, 3 = shields disabled, 4 = invisible, 5 = weapons generic, 6 don't show enemies on radar
    int32_t objective_indicator; #0x3C - 0 = motion tracker, 1 = NAV point, 2 = none
    int32_t odd_man_out; #0x40 - 0/1
    int32_t respawn_time_growth; #0x44 - ticks
    int32_t respawn_time; #0x48 - ticks - 0 or less is "instant" (3 seconds), respawning caps at 300 seconds
    int32_t respawn_suicide_penalty; #0x4C - ticks
    int32_t lives; #0x50 - 0 = unlimited
    float health; #0x54 - can be anywhere from 50% to 400%
    int32_t score_limit; #0x58 - CTF = flags, Slayer = kills, King = minutes, Oddball = points/minutes, Race = laps
    int32_t weapon_type; #0x5C - 0 = default, 1 = pistols, 2 = rifles, 3 = plasma rifles, 4 = sniper, 5 = no sniper, 6 = rocket launchers, 7 = shotguns, 8 = short range, 9 = human, 10 = covenant, 11 = classic, 12 = heavy weapons

    #VEHICLES
    HaloVehicleSpawn vehicle_red; #0x60
    HaloVehicleSpawn vehicle_blue; #0x64
    #__________TTTBBBRRRSSSGGGWWWoooo - Vehicles are stored as a bitmask (each letter is a bit); oooo = mode (0 = default, 1 = none, 2 = warthogs, 3 = ghosts, 4 = scorpions, 5 = rocket warthogs, 6 = banshees, 7 = gun turrets, 8 = custom); WWW = warthog count; GGG = ghost count; SSS = scorpion count; RRR = rocket warthog count; BBB = banshee count; TTT = gun turret count. Maximum 7.

    int32_t vehicle_respawn_time; #0x68 - ticks
    int32_t friendly_fire; #0x6C - 0 = off, 1 = on, 2 = shields, 3 = explosions
    int32_t respawn_betrayal_penalty; #0x70 - ticks
    int32_t auto_team_balance; #0x74 - 0/1
    int32_t time_limit; #0x78 - ticks
} HaloGametypeBase;

typedef struct HaloGametypeEnd {
    uint32_t crc32; #0x98
    char ce_padding[0x3C]; #0x9C
    uint32_t crc32_ce; #0xD8
    char padding[0x1F24]; #0xDC
} HaloGametypeEnd;

typedef struct HaloGametypeCTF {
    HaloGametypeBase base; #0x0
    char assault; #0x7C - 0/1
    char unknown; #0x7D
    char flag_must_reset; #0x7E - 0/1
    char flag_must_be_at_home; #0x7F - 0/1
    int32_t single_flag_time; #0x80 - ticks
    int32_t padding[5]; #0x84
    HaloGametypeEnd end; #0x98
} HaloGametypeCTF;

typedef struct HaloGametypeSlayer {
    HaloGametypeBase base; #0x0
    char death_bonus; #0x7C - 0/1
    char kill_penalty; #0x7D - 0/1
    char kill_in_order; #0x7E - 0/1
    char nothing; #0x7F - 0/1
    int32_t padding[6]; #0x80
    HaloGametypeEnd end; #0x98
} HaloGametypeSlayer;

typedef struct HaloGametypeKing {
    HaloGametypeBase base; #0x0
    char moving_hill; #0x7C - 0/1
    char nothing[3]; #0x7D
    int32_t padding[6]; #0x80
    HaloGametypeEnd end; #0x98
} HaloGametypeKing;

typedef struct HaloGametypeOddball {
    HaloGametypeBase base; #0x0
    char random_ball; #0x7C
    char nothing[3]; #0x7D
    int32_t speed_with_ball; #0x80 - 0 = slow, 1 = normal, 2 = fast
    int32_t trait_with_ball; #0x84 - 0 = none, 1 = invisible, 2 = extra damage, 3 = damage resistance
    int32_t trait_without_ball; #0x88 - 0 = none, 1 = invisible, 2 = extra damage, 3 = damage resistance
    int32_t ball_type; #0x8C - 0 = normal, 1 = reverse tag, 2 = juggernaut
    int32_t ball_count; #0x90
    int32_t padding; #0x94
    HaloGametypeEnd end; #0x98
} HaloGametypeOddball;

typedef struct HaloGametypeRace {
    HaloGametypeBase base; #0x0
    char order; #0x7C
    char nothing[3]; #0x7D
    int32_t pointsUsed; #0x80 - 0 = minimum, 1 = maximum, 2 = sum
    int32_t padding[5]; #0x84
    HaloGametypeEnd end; #0x98
} HaloGametypeRace;

typedef struct HaloGametype {
    HaloGametypeBase base; #0x0
    char settings[4]; #0x7C
    int32_t moresettings[6]; #0x80
    HaloGametypeEnd end; #0x98
} HaloGametype;

typedef enum HaloGametypeType {
    GAMETYPE_CTF = 1,
    GAMETYPE_SLAYER = 2,
    GAMETYPE_ODDBALL = 3,
    GAMETYPE_KING = 4,
    GAMETYPE_RACE = 5
} HaloGametypeType;

typedef enum {
    VEHICLE_DEFAULT = 0,
    VEHICLE_NONE = 1,
    VEHICLE_WARTHOGS = 2,
    VEHICLE_GHOSTS = 3,
    VEHICLE_SCORPIONS = 4,
    VEHICLE_ROCKET_WARTHOGS = 5,
    VEHICLE_BANSHEES = 6,
    VEHICLE_GUN_TURRETS = 7,
    VEHICLE_CUSTOM = 8
} HaloVehicleType;


uint32_t calculateGametypeChecksum(const void *gametype) {
    return 0xFFFFFFFF - crc32(0,gametype,0x98);
}

uint32_t calculateCEGametypeChecksum(const void *gametype) {
    return 0xFFFFFFFF - crc32(0,gametype,0xD8);
}

void convertCEGametypeToPC(void *gametype) {
    memcpy(gametype + 0x7C,gametype+0x9C,0x18);
    memset(gametype + 0x9C,0,0x18);
    memcpy(gametype + 0x94,gametype+0xD4,0x08);
    memset(gametype + 0xD4,0,0x08);
}

void convertPCGametypeToCE(void *gametype) {
    memcpy(gametype + 0xD4,gametype+0x94,0x08);
    memset(gametype + 0x94,0,0x08);
    memcpy(gametype + 0x9C,gametype+0x7C,0x18);
    memset(gametype + 0x7C,0,0x18);
}

void convertPCGametypeToHybrid(void *gametype) {
    memcpy(gametype + 0xD4,gametype + 0x94,0x08);
    memcpy(gametype + 0x9C,gametype + 0x7C,0x18);
}

#LOOK HERE FOR CRC32 CODE
#https://github.com/Halogen002/Flare-Qt/blob/master/crc32.c
