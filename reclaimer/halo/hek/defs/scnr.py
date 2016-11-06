from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

def object_reference(name, *args, **kwargs):
    return Struct(name,
        BSInt16('type'),
        BSInt16('name'),
        BBool16('not placed',
            "automatically",
            "on easy",
            "on normal",
            "on hard",
            ),
        BSInt16('desired permutation'),
        QStruct("position", INCLUDE=xyz_float),
        QStruct("rotation", INCLUDE=ypr_float),
        *args,
        **kwargs
        )

def object_palette(name, def_id):
    return Struct(name,
        dependency("name", def_id),
        SIZE=48
        )

device_flags = (
    "initially open",  # value of 1.0
    "initially off",  #  value of 0.0
    "can only change once",
    "position reversed",
    "initially",
    "not usable from any side"
    )

starting_location_types = (
    "none",
    "ctf",
    "slayer",
    "oddball",
    "king",
    "race",
    "terminator",
    "stub",
    "ignored1",
    "ignored2",
    "ignored3",
    "ignored4",
    "all games",
    "all games except ctf",
    "all games except ctf and race"
    )

sky = Struct("sky",
    dependency("sky", "sky "),
    SIZE=16
    )

child_scenario = Struct("child scenario",
    dependency("child scenario", "scnr"),
    SIZE=32
    )

function = Struct('function',
    BBool32('flags',
        'scripted',
        'invert',
        'additive',
        'always active',
        ),
    ascii_str32('name'),
    BFloat('period'),
    BSInt16('scale period by'),
    BSEnum16('function', *animation_functions),
    BSInt16('scale function by'),
    BSEnum16('wobble function', *animation_functions),
    BFloat('wobble period'),  # seconds
    BFloat('wobble magnitude'),  # percent
    BFloat('square wave threshold'),
    BSInt16('step count'),
    BSEnum16('map to', *fade_functions),
    BSInt16('sawtooth count'),

    Pad(2),
    BSInt16('scale result by'),
    BSEnum16('bounds mode',
        'clip',
        'clip and normalize',
        'scale to fit',
        ),
    QStruct('bounds', INCLUDE=from_to),

    Pad(6),
    BSInt16('turn off with'),

    SIZE=120
    )

comment = Struct("comment",
    QStruct("position", INCLUDE=xyz_float),
    Pad(16),
    rawdata_ref("comment data"),
    SIZE=48
    )

object_name = Struct("object name",
    ascii_str32("name"),
    SIZE=36
    )

# Object references
scenery = object_reference("scenery", SIZE=72)

biped = object_reference("biped",
    Pad(40),
    BFloat("body vitality", MIN=0.0, MAX=1.0),
    BBool32("flags",
        "dead",
        ),
    SIZE=120
    )

vehicle = object_reference("vehicle",
    Pad(40),
    BFloat("body vitality", MIN=0.0, MAX=1.0),
    BBool32("flags",
        "dead",
        ),

    Pad(8),
    SInt8("multiplayer team index"),
    Pad(1),
    BBool16("multiplayer spawn flags",
        "slayer default",
        "ctf default",
        "king default",
        "oddball default",
        #"unused1",
        #"unused2",
        #"unused3",
        #"unused4",
        ("slayer allowed", 1<<8),
        ("ctf allowed", 1<<9),
        ("king allowed", 1<<10),
        ("oddball allowed", 1<<11),
        #"unused5",
        #"unused6",
        #"unused7",
        #"unused8",
        ),
    SIZE=120
    )

equipment = object_reference("equipment",
    BBool32("misc flags",
        "initially at rest",
        # "obsolete",
        ("does accelerate", 1<<2),  # moves due to explosions
        ),
    SIZE=40
    )

weapon = object_reference("weapon",
    Pad(40),
    BSInt16("rounds left"),
    BSInt16("rounds loaded"),
    BBool16("flags",
        "initially at rest",
        # "obsolete",
        ("does accelerate", 1<<2),  # moves due to explosions
        ),
    SIZE=92
    )

device_group = Struct("device group",
    ascii_str32("name"),
    BFloat("initial value", MIN=0.0, MAX=1.0),
    BBool32("flags",
        "can change only once"
        ),
    SIZE=52
    )

machine = object_reference("machine",
    Pad(8),
    BSInt16("power group"),
    BSInt16("position group"),
    BBool32("flags", *device_flags),
    BBool32("more flags",
        "does not operate automatically",
        "one-sided",
        "never appears locked",
        "opened by melee attack",
        ),
    SIZE=64
    )

control = object_reference("control",
    Pad(8),
    BSInt16("power group"),
    BSInt16("position group"),
    BBool32("flags", *device_flags),
    BBool32("more flags",
        "usable from both sides",
        ),
    BSInt16("DONT TOUCH THIS"),  # why?
    SIZE=64
    )

light_fixture = object_reference("light fixture",
    Pad(8),
    BSInt16("power group"),
    BSInt16("position group"),
    BBool32("flags", *device_flags),
    QStruct("color", INCLUDE=rgb_float),
    BFloat("intensity"),
    BFloat("falloff angle"),  # radians
    BFloat("cutoff angle"),  # radians
    SIZE=88
    )

sound_scenery = object_reference("sound scenery", SIZE=40)

# Object palettes
scenery_palette = object_palette("scenery palette", "scen")
biped_palette = object_palette("biped palette", "bipd")
vehicle_palette = object_palette("vehicle palette", "vehi")
equipment_palette = object_palette("equipment palette", "eqip")
weapon_palette = object_palette("weapon palette", "weap")
machine_palette = object_palette("machine palette", "mach")
control_palette = object_palette("control palette", "ctrl")
light_fixture_palette = object_palette("light fixture palette", "lifi")
sound_scenery_palette = object_palette("sound scenery palette", "ssce")

player_starting_profile = Struct("player starting profile",
    ascii_str32("name"),
    BFloat("starting health modifier"),
    BFloat("starting shield modifier"),
    dependency("primary weapon", "weap"),
    BSInt16("primary rounds loaded"),
    BSInt16("primary rounds total"),
    dependency("secondary weapon", "weap"),
    BSInt16("secondary rounds loaded"),
    BSInt16("secondary rounds total"),
    SInt8("starting fragmentation count"),
    SInt8("starting plasma count"),
    SIZE=104
    )

player_starting_location = Struct("player starting location",
    QStruct("position", INCLUDE=xyz_float),
    BFloat("facing"),  # radians
    BSInt16("team index"),
    BSInt16("bsp index"),
    BSInt16("type 0", *starting_location_types),
    BSInt16("type 1", *starting_location_types),
    BSInt16("type 2", *starting_location_types),
    BSInt16("type 3", *starting_location_types),
    SIZE=52
    )

trigger_volume = Struct("trigger volume",
    Pad(4),
    ascii_str32("name"),
    # find out what these fields actually are and name them
    *(BFloat("field" + str(i + 1)) for i in range(15)),
    SIZE=96
    )

recorded_animation = Struct("recorded animation",
    ascii_str32("name"),
    SInt8("version"),
    SInt8("raw animation data"),
    SInt8("unit control data version"),
    Pad(1),
    BSInt16("length of animation"),  # ticks
    Pad(6),
    SIZE=64
    )

netgame_flag = Struct("netgame flag",
    )

netgame_equipment = Struct("netgame equipment",
    )

starting_equipment = Struct("starting equipment",
    )

bsp_switch_trigger_volume = Struct("bsp switch trigger volume",
    )

decal = Struct("decal",
    )

decal_palette = Struct("decal palette",
    )

detail_object_collection_palette = Struct("detail object collection palette",
    )

actor_palette = Struct("actor_palette",
    )

encounter = Struct("encounter",
    )

command_list = Struct("command list",
    )

ai_animation_reference = Struct("ai animation reference",
    )

ai_script_reference = Struct("ai script reference",
    )

ai_recording_reference = Struct("ai recording reference",
    )

ai_conversation = Struct("ai conversation",
    )

script = Struct("script",
    )

halo_global = Struct("halo global",
    )

reference = Struct("reference",
    )

source_file = Struct("source_file",
    )

cutscene_flag = Struct("cutscene flag",
    )

cutscene_camera_point = Struct("cutscene camera point",
    )

cutscene_title = Struct("cutscene title",
    )

structure_bsp = Struct("structure bsp",
    )

scnr_body = Struct("tagdata",
    dependency("DONT USE", 'sbsp'),
    dependency("WONT USE", 'sbsp'),
    dependency("CANT USE", 'sky '),
    reflexive("skies", sky, 8),
    BSEnum16("type",
        "singleplayer",
        "multiplayer",
        "main menu"
        ),
    BBool16("flags",
        "cortana hack",
        "use demo ui"
        ),
    reflexive("child scenarios", child_scenario, 16),
    BFloat("local north"),  # radians

    Pad(156),
    reflexive("predicted resources", predicted_resource, 1024),
    reflexive("functions", function, 32),
    rawdata_ref("scenario editor data"),
    reflexive("comments", comment, 1024),

    Pad(224),
    reflexive("object names", object_name, 512),
    reflexive("scenery", scenery, 2000),
    reflexive("scenery palette", scenery_palette, 100),
    reflexive("bipeds", biped, 128),
    reflexive("biped palette", biped_palette, 100),
    reflexive("vehicles", vehicle, 80),
    reflexive("vehicle palette", vehicle_palette, 100),
    reflexive("equipment", equipment, 256),
    reflexive("equipment palette", equipment_palette, 100),
    reflexive("weapons", weapon, 128),
    reflexive("weapon palette", weapon_palette, 100),
    reflexive("device groups", device_group, 128),
    reflexive("machine", machine, 400),
    reflexive("machine palette", machine_palette, 100),
    reflexive("control", control, 100),
    reflexive("control palette", control_palette, 100),
    reflexive("light fixture", light_fixture, 500),
    reflexive("light fixture palette", light_fixture_palette, 100),
    reflexive("sound scenery", sound_scenery, 256),
    reflexive("sound scenery palette", sound_scenery_palette, 100),

    Pad(84),
    reflexive("player starting profiles", player_starting_profile, 256),
    reflexive("player starting locations", player_starting_location, 256),
    reflexive("trigger volumes", trigger_volume, 256),
    reflexive("recorded animations", recorded_animation, 1024),
    reflexive("netgame flags", netgame_flag, 200),
    reflexive("netgame equipment", netgame_equipment, 200),
    reflexive("starting equipment", starting_equipment, 200),
    reflexive("bsp switch trigger volumes", bsp_switch_trigger_volume, 256),
    reflexive("decals", decal),  # dont know the max reflexive count
    reflexive("decal palette", decal_palette, 128),
    reflexive("detail object collection palette",
              detail_object_collection_palette, 32),

    Pad(84),
    reflexive("actor palette", actor_palette, 64),
    reflexive("encounters", encounter, 128),
    reflexive("command lists", command_list, 256),
    reflexive("ai animation reference", ai_animation_reference, 128),
    reflexive("ai script reference", ai_script_reference, 128),
    reflexive("ai recording reference", ai_recording_reference, 128),
    reflexive("ai conversations", ai_conversation, 128),
    rawdata_ref("script syntax data"),
    rawdata_ref("script string data"),
    reflexive("scripts", script, 512),
    reflexive("globals", halo_global, 128),
    reflexive("references", reference, 256),
    reflexive("source files", source_file, 8),

    Pad(24),
    reflexive("cutscene flags", cutscene_flag, 512),
    reflexive("cutscene camera points", cutscene_camera_point, 512),
    reflexive("cutscene titles", cutscene_title, 64),

    Pad(108),
    dependency("custom object names", 'ustr'),
    dependency("ingame help text", 'ustr'),
    dependency("hud messages", 'hmt '),
    reflexive("structure bsps", structure_bsp, 16),
    SIZE=1456,
    )

# PLAYER STARTING PROFILES HAVE 2 MORE FIELDS FOR EXTRA GRENADES IN OPEN SAUCE
# ALSO ai animation reference WILL NEED magy INCLUDED IN ITS GRAPHS

def get():
    return scnr_def

scnr_def = TagDef("scnr",
    blam_header('scnr', 2),
    scnr_body,

    ext=".scenario", endian=">"
    )
