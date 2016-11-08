from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

def object_reference(name, *args, **kwargs):
    "Macro to cut down on a lot of code"
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

def object_palette(name, def_id, size=48):
    "Macro to cut down on a lot of code"
    return Struct(name,
        dependency("name", def_id),
        SIZE=size
        )

device_flags = (
    "initially open",  # value of 1.0
    "initially off",  #  value of 0.0
    "can change only once",
    "position reversed",
    "not usable from any side"
    )

location_types = (
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

group_indices = tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

squad_states = (
    "none",
    "sleeping",
    "alert",
    "moving - repeat same position",
    "moving - loop",
    "moving - loop back and forth",
    "moving - loop randomly",
    "moving - randomly",
    "guarding",
    "guarding at position",
    "searching",
    "fleeing"
    )

manuever_when_states = (
    "never",
    {NAME: "strength at 75 percent", GUI_NAME: "< 75% strength"},
    {NAME: "strength at 50 percent", GUI_NAME: "< 50% strength"},
    {NAME: "strength at 25 percent", GUI_NAME: "< 25% strength"},
    "anybody dead",
    {NAME: "dead at 25 percent", GUI_NAME: "25% dead"},
    {NAME: "dead at 50 percent", GUI_NAME: "50% dead"},
    {NAME: "dead at 75 percent", GUI_NAME: "75% dead"},
    "all but one dead",
    "all dead"
    )

atom_types = (
    "pause",
    "goto",
    "goto and face",
    "move in direction",
    "look",
    "animation mode",
    "crouch",
    "shoot",
    "grenade",
    "vehicle",
    "running jump",
    "targeted jump",
    "script",
    "animate",
    "recording",
    "action",
    "vocalize",
    "targeting",
    "initiative",
    "wait",
    "loop",
    "die",
    "move immediate",
    "look random",
    "look player",
    "look object",
    "set radius",
    "teleport"
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
    SInt8("starting frag grenade count"),
    SInt8("starting plasma grenade count"),
    SIZE=104
    )

player_starting_location = Struct("player starting location",
    QStruct("position", INCLUDE=xyz_float),
    BFloat("facing"),  # radians
    BSInt16("team index"),
    BSInt16("bsp index"),
    BSEnum16("type 0", *location_types),
    BSEnum16("type 1", *location_types),
    BSEnum16("type 2", *location_types),
    BSEnum16("type 3", *location_types),
    SIZE=52
    )

trigger_volume = Struct("trigger volume",
    Pad(4),
    ascii_str32("name"),
    # find out what these fields actually are and name them
    BFloat("field1"),
    BFloat("field2"),
    BFloat("field3"),
    BFloat("field4", DEFAULT=1.0),
    BFloat("field5"),
    BFloat("field6"),
    BFloat("field7", DEFAULT=-0.0),
    BFloat("field8", DEFAULT=-0.0),
    BFloat("field9", DEFAULT=1.0),
    QStruct("position", INCLUDE=xyz_float),
    QStruct("dimensions",
        BFloat("width"), BFloat("length"), BFloat("height")
        ),
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
    rawdata_ref("recorded animation event stream"),
    SIZE=64
    )

netgame_flag = Struct("netgame flag",
    QStruct("position", INCLUDE=xyz_float),
    BFloat("facing"),  # radians
    BSEnum16("type",
        "ctf - flag",
        "ctf - vehicle",
        "oddball - ball spawn",
        "race - track",
        "race - vehicle",
        "vegas - bank",
        "teleport - from",
        "teleport - to",
        "hill - flag",
        ),
    BSInt16("team index"),
    dependency("weapon group", "itmc"),
    SIZE=148
    )

netgame_equipment = Struct("netgame equipment",
    BBool32("type",
        "levitate"
        ),
    BSEnum16("type 0", *location_types),
    BSEnum16("type 1", *location_types),
    BSEnum16("type 2", *location_types),
    BSEnum16("type 3", *location_types),
    BSInt16("team index"),
    BSInt16("spawn time"),  # seconds

    Pad(48),
    QStruct("position", INCLUDE=xyz_float),
    BFloat("facing"),  # radians
    dependency("item collection", "itmc"),
    SIZE=144
    )

starting_equipment = Struct("starting equipment",
    BBool32("type",
        "no grenades",
        "plasma grenades",
        ),
    BSEnum16("type 0", *location_types),
    BSEnum16("type 1", *location_types),
    BSEnum16("type 2", *location_types),
    BSEnum16("type 3", *location_types),

    Pad(48),
    dependency("item collection 1", "itmc"),
    dependency("item collection 2", "itmc"),
    dependency("item collection 3", "itmc"),
    dependency("item collection 4", "itmc"),
    dependency("item collection 5", "itmc"),
    dependency("item collection 6", "itmc"),
    SIZE=204
    )

bsp_switch_trigger_volume = Struct("bsp switch trigger volume",
    BSInt16("trigger volume"),
    BSInt16("source"),
    BSInt16("destination"),
    SIZE=8
    )

decal = Struct("decal",
    BSInt16("decal type"),
    SInt8("yaw"),
    SInt8("pitch"),
    QStruct("position", INCLUDE=xyz_float),
    SIZE=16
    )

decal_palette = object_palette("decal palette", "deca", 16)
detail_object_collection_palette = object_palette(
    "detail object collection palette", "dobc")
actor_palette = object_palette("actor palette", "actv", 16)

ai_anim_reference = Struct("ai animation reference",
    ascii_str32("animation name"),
    dependency("animation graph", "antr"),
    SIZE=60
    )

ai_script_reference = Struct("ai script reference",
    ascii_str32("script name"),
    SIZE=40
    )

ai_recording_reference = Struct("ai recording reference",
    ascii_str32("recording name"),
    SIZE=40
    )

script = Struct("script",
    ascii_str32("script name"),
    BSEnum16("script type", *script_types),
    BSEnum16("return type", *script_object_types),
    BSInt32("root expression index"),
    SIZE=92
    )

halo_global = Struct("halo global",
    ascii_str32("script name"),
    BSEnum16("type", *script_object_types),
    Pad(6),
    BSInt32("initialization expression index"),
    SIZE=92
    )

reference = Struct("tag reference",
    Pad(24),
    dependency("reference"),
    SIZE=40
    )

source_file = Struct("source_file",
    ascii_str32("script name"),
    rawdata_ref("source"),
    SIZE=52
    )

cutscene_flag = Struct("cutscene flag",
    Pad(4),
    ascii_str32("name"),
    QStruct("position", INCLUDE=xyz_float),
    QStruct("facing", INCLUDE=yp_float),  # radians
    SIZE=92
    )

cutscene_camera_point = Struct("cutscene camera point",
    Pad(4),
    ascii_str32("name"),
    Pad(4),
    QStruct("position", INCLUDE=xyz_float),
    QStruct("orientation", INCLUDE=ypr_float),  # radians
    BFloat("field of view"),  # radians
    SIZE=104
    )

cutscene_title = Struct("cutscene title",
    Pad(4),
    ascii_str32("name"),
    Pad(4),
    QStruct("text bounds",
        BSInt16("t"), BSInt16("l"), BSInt16("b"), BSInt16("r"),
        ),
    BSInt16("string index"),
    BSEnum16("text style",
        "plain",
        "bold",
        "italic",
        "condense",
        "underline",
        ),
    BSEnum16("justification",
        "left",
        "right",
        "center",
        ),

    Pad(6),
    QStruct("text color", INCLUDE=argb_byte),
    QStruct("shadow color", INCLUDE=argb_byte),
    BFloat("fade in time"),  # seconds
    BFloat("up time"),  # seconds
    BFloat("fade out time"),  # seconds
    SIZE=96
    )

structure_bsp = Struct("structure bsp",
    Pad(16),
    dependency("structure bsp", "sbsp"),
    SIZE=32
    )


move_position = Struct("move position",
    QStruct("position", INCLUDE=xyz_float),
    BFloat("facing"),  # radians
    BFloat("weight"),
    QStruct("time", INCLUDE=from_to),
    BSInt16("animation"),
    SInt8("sequence id"),

    Pad(45),
    BSInt32("surface index"),
    SIZE=80
    )

actor_starting_location = Struct("starting location",
    QStruct("position", INCLUDE=xyz_float),
    BFloat("facing"),  # radians
    Pad(2),
    SInt8("sequence id"),
    Bool8("flags",
        "required",
        ),
    BSEnum16("return state", *squad_states),
    BSEnum16("initial state", *squad_states),
    BSInt16("actor type"),
    BSInt16("command list"),
    SIZE=28
    )

squad = Struct("squad",
    ascii_str32("name"),
    BSInt16("actor type"),
    BSInt16("platoon"),
    BSEnum16("initial state", *squad_states),
    BSEnum16("return state", *squad_states),
    BBool32("flags",
        "unused",
        "never search",
        "start timer immediately",
        "no timer, delay forever",
        "magic sight after timer",
        "automatic migration",
        ),
    BSEnum16("unique leader type",
        "normal",
        "none",
        "random",
        "sgt johnson",
        "sgt lehto",
        ),

    Pad(32),
    BSInt16("manuever to squad"),
    BFloat("squad delay time"),  # seconds
    BBool32("attacking", *group_indices),
    BBool32("attacking search", *group_indices),
    BBool32("attacking guard", *group_indices),
    BBool32("defending", *group_indices),
    BBool32("defending search", *group_indices),
    BBool32("defending guard", *group_indices),
    BBool32("pursuing", *group_indices),

    Pad(12),
    BSInt16("normal diff count"),
    BSInt16("insane diff count"),
    BSEnum16("major upgrade",
        "normal",
        "few",
        "many",
        "none",
        "all",
        ),

    Pad(2),
    BSInt16("respawn min actors"),
    BSInt16("respawn max actors"),
    BSInt16("respawn total"),

    Pad(2),
    QStruct("respawn delay", INCLUDE=from_to),

    Pad(48),
    reflexive("move positions", move_position, 31),
    reflexive("starting locations", actor_starting_location, 31),
    SIZE=232
    )

platoon = Struct("platoon",
    ascii_str32("name"),
    BBool32("flags",
        "flee when manuevering",
        "say advancing when manuevering",
        "start in defending state",
        ),

    Pad(12),
    BSEnum16("change attacking/defending state", *manuever_when_states),
    BSInt16("change happens to"),

    Pad(8),
    BSEnum16("manuever when", *manuever_when_states),
    BSInt16("manuever happens to"),
    SIZE=172
    )

firing_position = Struct("firing position",
    QStruct("position", INCLUDE=xyz_float),
    BSEnum16("group index", *group_indices),
    SIZE=24
    )

encounter = Struct("encounter",
    ascii_str32("name"),
    BBool32("flags",
        "not initially created",
        "respawn enabled",
        "initially blind",
        "initially deaf",
        "initially braindead",
        "firing positions are 3d",
        "manual bsp index specified",
        ),
    BSEnum16("team index",
        "0 / default by unit",
        "1 / player",
        "2 / human",
        "3 / covenant",
        "4 / flood",
        "5 / sentinel",
        "6 / unused6",
        "7 / unused7",
        "8 / unused8",
        "9 / unused9"
        ),
    Pad(2),
    BSEnum16("search behavior",
        "normal",
        "never",
        "tenacious"
        ),
    BSInt16("manual bsp index"),
    QStruct("respawn delay", INCLUDE=from_to),

    Pad(76),
    reflexive("squads", squad, 64),
    reflexive("platoons", platoon, 32),
    reflexive("firing positions", firing_position, 512),
    reflexive("player starting locations", player_starting_location, 256),
    
    SIZE=176
    )

command = Struct("command",
    BSEnum16("atom type", *atom_types),
    BSInt16("atom modifier"),
    BFloat("parameter 1"),
    BFloat("parameter 2"),
    BSInt16("point 1"),
    BSInt16("point 2"),
    BSInt16("animation"),
    BSInt16("script"),
    BSInt16("recording"),
    BSInt16("command"),
    BSInt16("object name"),
    SIZE=32
    )

point = Struct("point",
    QStruct("position", INCLUDE=xyz_float),
    SIZE=20
    )

command_list = Struct("command list",
    ascii_str32("name"),
    BBool32("flags",
        "allow initiative",
        "allow targeting",
        "disable looking",
        "disable communication",
        "disable falling damage",
        "manual bsp index",
        ),

    Pad(8),
    BSInt16("manual bsp index"),

    Pad(2),
    reflexive("commands", command, 64),
    reflexive("points", point, 64),
    SIZE=96
    )

participant = Struct("participant",
    Pad(3),
    Bool8("flags",
        "optional",
        "has alternate",
        "is alternate",
        ),
    BSEnum16("selection type",
        "friendly actor",
        "disembodied",
        "in players vehicle",
        "not in a vehicle",
        "prefer sergeant",
        "any actor",
        "radio unit",
        "radio sergeant",
        ),
    BSEnum16("actor type", *actor_types),
    BSInt16("use this object"),
    BSInt16("set new name"),

    Pad(12),
    BytesRaw("unknown", DEFAULT=b"\xFF"*12, SIZE=12),
    ascii_str32("encounter name"),
    SIZE=84
    )

line = Struct("line",
    BBool16("flags",
        "addressee look at speaker",
        "everyone look at speaker",
        "everyone look at addressee",
        "wait until told to advance",
        "wait until speaker nearby",
        "wait until everyone nearby",
        ),
    BSInt16("participant"),
    BSEnum16("addressee",
        "none",
        "player",
        "participant",
        ),
    BSInt16("addressee participant"),

    Pad(4),
    BFloat("line delay time"),

    Pad(12),
    dependency("variant 1", "snd!"),
    dependency("variant 2", "snd!"),
    dependency("variant 3", "snd!"),
    dependency("variant 4", "snd!"),
    dependency("variant 5", "snd!"),
    dependency("variant 6", "snd!"),
    SIZE=124
    )

ai_conversation = Struct("ai conversation",
    ascii_str32("name"),
    BBool16("flags",
        "stop if death",
        "stop if damaged",
        "stop if visible enemy",
        "stop if alerted to enemy",
        "player must be visible",
        "stop other actions",
        "keep trying to play",
        "player must be looking",
        ),

    Pad(2),
    BFloat("trigger distance"),
    BFloat("run-to-player distance"),

    Pad(36),
    reflexive("participants", participant, 8),
    reflexive("lines", line, 32),
    SIZE=116
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
    reflexive("decals", decal, 65536),
    reflexive("decal palette", decal_palette, 128),
    reflexive("detail object collection palette",
              detail_object_collection_palette, 32),

    Pad(84),
    reflexive("actor palette", actor_palette, 64),
    reflexive("encounters", encounter, 128),
    reflexive("command lists", command_list, 256),
    reflexive("ai animation references", ai_anim_reference, 128),
    reflexive("ai script references", ai_script_reference, 128),
    reflexive("ai recording references", ai_recording_reference, 128),
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

def get():
    return scnr_def

scnr_def = TagDef("scnr",
    blam_header('scnr', 2),
    scnr_body,

    ext=".scenario", endian=">"
    )
