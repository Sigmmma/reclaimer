from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

def object_reference(name, *args, **kwargs):
    "Macro to cut down on a lot of code"
    block_name = kwargs.pop('block_name', name + 's').replace(' ', '_')

    dyn_type_path = ".....%s_palette.STEPTREE[DYN_I].name.filepath" % block_name
    return Struct(name,
        dyn_senum16('type', DYN_NAME_PATH=dyn_type_path),
        dyn_senum16('name',
            DYN_NAME_PATH=".....object_names.STEPTREE[DYN_I].name"),
        Bool16('not placed',
            "automatically",
            "on easy",
            "on normal",
            "on hard",
            ),
        SInt16('desired permutation'),
        QStruct("position", INCLUDE=xyz_float),
        ypr_float_rad("rotation"),
        *args,
        **kwargs
        )

def object_swatch(name, def_id, size=48):
    "Macro to cut down on a lot of code"
    return Struct(name,
        dependency("name", def_id),
        SIZE=size
        )

fl_float_xyz = QStruct("",
    FlFloat("x"),
    FlFloat("y"),
    FlFloat("z"),
    ORIENT="h"
    )

stance_flags = FlBool16("stance",
    "walk",
    "look only",
    "primary fire",
    "secondary fire",
    "jump",
    "crouch",
    "melee",
    "flashlight",
    "action1",
    "action2",
    "action hold",
    )

unit_control_packet = Struct("unit control packet",
    
    )

r_a_stream_header = Struct("r a stream header",
    UInt8("move index", DEFAULT=3, MAX=6),
    UInt8("bool index"),
    stance_flags,
    FlSInt16("weapon", DEFAULT=-1),
    QStruct("speed", FlFloat("x"), FlFloat("y"), ORIENT="h"),
    QStruct("feet", INCLUDE=fl_float_xyz),
    QStruct("body", INCLUDE=fl_float_xyz),
    QStruct("head", INCLUDE=fl_float_xyz),
    QStruct("change", INCLUDE=fl_float_xyz),
    FlUInt32("unknown1"),
    FlUInt32("unknown2", DEFAULT=0xFFFFFFFF),
    SIZE=60
    )

device_flags = (
    "initially open",  # value of 1.0
    "initially off",  # value of 0.0
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

maneuver_when_states = (
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
    Bool32('flags',
        'scripted',
        'invert',
        'additive',
        'always active',
        ),
    ascii_str32('name'),
    float_sec('period'),  # seconds
    dyn_senum16('scale period by', DYN_NAME_PATH="..[DYN_I].name"),
    SEnum16('function', *animation_functions),
    dyn_senum16('scale function by', DYN_NAME_PATH="..[DYN_I].name"),
    SEnum16('wobble function', *animation_functions),
    float_sec('wobble period'),  # seconds
    Float('wobble magnitude', SIDETIP="%"),  # percent
    Float('square wave threshold'),
    SInt16('step count'),
    SEnum16('map to', *fade_functions),
    SInt16('sawtooth count'),

    Pad(2),
    dyn_senum16('scale result by', DYN_NAME_PATH="..[DYN_I].name"),
    SEnum16('bounds mode',
        'clip',
        'clip and normalize',
        'scale to fit',
        ),
    QStruct('bounds', INCLUDE=from_to),

    Pad(6),
    dyn_senum16('turn off with', DYN_NAME_PATH="..[DYN_I].name"),

    SIZE=120
    )

comment = Struct("comment",
    QStruct("position", INCLUDE=xyz_float),
    Pad(16),
    rawtext_ref("comment data", StrLatin1, max_size=16384),
    SIZE=48
    )

object_name = Struct("object name",
    ascii_str32("name"),
    FlUInt16("unknown1", VISIBLE=False),
    FlUInt16("unknown2", VISIBLE=False),
    SIZE=36
    )

# Object references
scenery = object_reference("scenery", SIZE=72, block_name="sceneries")

biped = object_reference("biped",
    Pad(40),
    float_zero_to_one("body vitality"),
    Bool32("flags",
        "dead",
        ),
    SIZE=120
    )

vehicle = object_reference("vehicle",
    Pad(40),
    float_zero_to_one("body vitality"),
    Bool32("flags",
        "dead",
        ),

    Pad(8),
    SInt8("multiplayer team index"),
    Pad(1),
    Bool16("multiplayer spawn flags",
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
    Pad(2),
    Bool16("flags",
        "initially at rest",
        "obsolete",
        {NAME: "can accelerate", GUI_NAME:"moves due to explosions"},
        ),
    SIZE=40
    )

weapon = object_reference("weapon",
    Pad(40),
    SInt16("rounds left"),
    SInt16("rounds loaded"),
    Bool16("flags",
        "initially at rest",
        "obsolete",
        {NAME: "can accelerate", GUI_NAME:"moves due to explosions"},
        ),
    SIZE=92
    )

device_group = Struct("device group",
    ascii_str32("name"),
    float_zero_to_one("initial value"),
    Bool32("flags",
        "can change only once"
        ),
    SIZE=52
    )

machine = object_reference("machine",
    Pad(8),
    dyn_senum16("power group",
        DYN_NAME_PATH=".....device_groups.STEPTREE[DYN_I].name"),
    dyn_senum16("position group",
        DYN_NAME_PATH=".....device_groups.STEPTREE[DYN_I].name"),
    Bool32("flags", *device_flags),
    Bool32("more flags",
        "does not operate automatically",
        "one-sided",
        "never appears locked",
        "opened by melee attack",
        ),
    SIZE=64
    )

control = object_reference("control",
    Pad(8),
    dyn_senum16("power group",
        DYN_NAME_PATH=".....device_groups.STEPTREE[DYN_I].name"),
    dyn_senum16("position group",
        DYN_NAME_PATH=".....device_groups.STEPTREE[DYN_I].name"),
    Bool32("flags", *device_flags),
    Bool32("more flags",
        "usable from both sides",
        ),
    SInt16("DONT TOUCH THIS"),  # why?
    SIZE=64
    )

light_fixture = object_reference("light fixture",
    Pad(8),
    dyn_senum16("power group",
        DYN_NAME_PATH=".....device_groups.STEPTREE[DYN_I].name"),
    dyn_senum16("position group",
        DYN_NAME_PATH=".....device_groups.STEPTREE[DYN_I].name"),
    Bool32("flags", *device_flags),
    QStruct("color", INCLUDE=rgb_float),
    Float("intensity"),
    Float("falloff angle"),  # radians
    Float("cutoff angle"),  # radians
    SIZE=88
    )

sound_scenery = object_reference("sound scenery", SIZE=40, block_name="sound_sceneries")

# Object swatches
scenery_swatch = object_swatch("scenery swatch", "scen")
biped_swatch = object_swatch("biped swatch", "bipd")
vehicle_swatch = object_swatch("vehicle swatch", "vehi")
equipment_swatch = object_swatch("equipment swatch", "eqip")
weapon_swatch = object_swatch("weapon swatch", "weap")
machine_swatch = object_swatch("machine swatch", "mach")
control_swatch = object_swatch("control swatch", "ctrl")
light_fixture_swatch = object_swatch("light fixture swatch", "lifi")
sound_scenery_swatch = object_swatch("sound scenery swatch", "ssce")

player_starting_profile = Struct("player starting profile",
    ascii_str32("name"),
    float_zero_to_one("starting health modifier"),
    float_zero_to_one("starting shield modifier"),
    dependency("primary weapon", "weap"),
    SInt16("primary rounds loaded"),
    SInt16("primary rounds total"),
    dependency("secondary weapon", "weap"),
    SInt16("secondary rounds loaded"),
    SInt16("secondary rounds total"),
    SInt8("starting frag grenade count", MIN=0),
    SInt8("starting plasma grenade count", MIN=0),
    SIZE=104
    )

player_starting_location = Struct("player starting location",
    QStruct("position", INCLUDE=xyz_float),
    float_rad("facing"),  # radians
    SInt16("team index"),
    dyn_senum16("bsp index",
        DYN_NAME_PATH=".....structure_bsps.STEPTREE[DYN_I].structure_bsp.filepath"),
    SEnum16("type 0", *location_types),
    SEnum16("type 1", *location_types),
    SEnum16("type 2", *location_types),
    SEnum16("type 3", *location_types),
    SIZE=52
    )

player_starting_location2 = dict(player_starting_location)
player_starting_location2[3] = dyn_senum16("bsp index",
        DYN_NAME_PATH=("........structure_bsps.STEPTREE"
                       "[DYN_I].structure_bsp.filepath")
        )

trigger_volume = Struct("trigger volume",
    FlUInt32("unknown", DEFAULT=1, EDITABLE=False),
    ascii_str32("name"),
    # find out what if these fields actually what i'm calling them
    QStruct("normal",   INCLUDE=ijk_float),
    QStruct("binormal", INCLUDE=ijk_float),
    QStruct("tangent",  INCLUDE=ijk_float),
    QStruct("position", INCLUDE=xyz_float),
    QStruct("sides",
        Float("w"), Float("l"), Float("h"),
        ORIENT='h'
        ),
    SIZE=96,
    COMMENT="I'm not sure if these are the actual names, but they seem to fit."
    )

recorded_animation = Struct("recorded animation",
    ascii_str32("name"),
    SInt8("version"),
    SInt8("raw animation data"),
    SInt8("unit control data version"),
    Pad(1),
    SInt16("length of animation", SIDETIP="ticks"),  # ticks
    Pad(6),
    rawdata_ref("recorded animation event stream", max_size=2097152),
    SIZE=64
    )

netgame_flag = Struct("netgame flag",
    QStruct("position", INCLUDE=xyz_float),
    float_rad("facing"),  # radians
    SEnum16("type",
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
    SInt16("team index"),
    dependency("weapon group", "itmc"),
    SIZE=148
    )

netgame_equipment = Struct("netgame equipment",
    Bool32("flags",
        "levitate"
        ),
    SEnum16("type 0", *location_types),
    SEnum16("type 1", *location_types),
    SEnum16("type 2", *location_types),
    SEnum16("type 3", *location_types),
    SInt16("team index"),
    SInt16("spawn time", SIDETIP="seconds(0 = default)",
            UNIT_SCALE=sec_unit_scale),  # seconds

    Pad(48),
    QStruct("position", INCLUDE=xyz_float),
    float_rad("facing"),  # radians
    dependency("item collection", "itmc"),
    SIZE=144
    )

starting_equipment = Struct("starting equipment",
    Bool32("flags",
        "no grenades",
        "plasma grenades",
        ),
    SEnum16("type 0", *location_types),
    SEnum16("type 1", *location_types),
    SEnum16("type 2", *location_types),
    SEnum16("type 3", *location_types),

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
    dyn_senum16("trigger volume",
        DYN_NAME_PATH=".....trigger_volumes.STEPTREE[DYN_I].name"),
    dyn_senum16("source",
        DYN_NAME_PATH=".....structure_bsps.STEPTREE[DYN_I].structure_bsp.filepath"),
    dyn_senum16("destination",
        DYN_NAME_PATH=".....structure_bsps.STEPTREE[DYN_I].structure_bsp.filepath"),
    SIZE=8
    )

decal = Struct("decal",
    dyn_senum16("decal type",
        DYN_NAME_PATH=".....decals_palette.STEPTREE[DYN_I].name.filepath"),
    SInt8("yaw"),
    SInt8("pitch"),
    QStruct("position", INCLUDE=xyz_float),
    SIZE=16
    )

decal_swatch = object_swatch("decal swatch", "deca", 16)
detail_object_collection_swatch = object_swatch(
    "detail object collection swatch", "dobc")
actor_swatch = object_swatch("actor swatch", "actv", 16)

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

halo_script = Struct("script",
    ascii_str32("name", EDITABLE=False),
    SEnum16("type", *script_types),
    SEnum16("return type", *script_object_types, EDITABLE=False),
    UInt32("root expression index", EDITABLE=False),
    Void("decompiled script", WIDGET=HaloScriptTextFrame),
    SIZE=92,
    )

halo_global = Struct("global",
    ascii_str32("name", EDITABLE=False),
    SEnum16("type", *script_object_types, EDITABLE=False),
    Pad(6),
    UInt32("initialization expression index", EDITABLE=False),
    Void("decompiled script", WIDGET=HaloScriptTextFrame),
    SIZE=92,
    )

reference = Struct("tag reference",
    Pad(24),
    dependency("reference"),
    SIZE=40
    )

source_file = Struct("source_file",
    ascii_str32("source name"),
    rawdata_ref("source", max_size=262144, widget=HaloScriptSourceFrame),
    SIZE=52
    )

cutscene_flag = Struct("cutscene flag",
    Pad(4),
    ascii_str32("name"),
    QStruct("position", INCLUDE=xyz_float),
    yp_float_rad("facing"),  # radians
    SIZE=92
    )

cutscene_camera_point = Struct("cutscene camera point",
    Pad(4),
    ascii_str32("name"),
    Pad(4),
    QStruct("position", INCLUDE=xyz_float),
    ypr_float_rad("orientation"),  # radians
    float_rad("field of view"),  # radians
    SIZE=104
    )

cutscene_title = Struct("cutscene title",
    Pad(4),
    ascii_str32("name"),
    Pad(4),
    QStruct("text bounds",
        SInt16("t"), SInt16("l"), SInt16("b"), SInt16("r"),
        ORIENT='h',
        ),
    SInt16("string index"),
    SEnum16("text style",
        "plain",
        "bold",
        "italic",
        "condense",
        "underline",
        ),
    SEnum16("justification",
        "left",
        "right",
        "center",
        ),

    Pad(6),
    #QStruct("text color", INCLUDE=argb_byte),
    #QStruct("shadow color", INCLUDE=argb_byte),
    UInt32("text color", INCLUDE=argb_uint32),
    UInt32("shadow color", INCLUDE=argb_uint32),
    float_sec("fade in time"),  # seconds
    float_sec("up time"),  # seconds
    float_sec("fade out time"),  # seconds
    SIZE=96
    )


move_position = Struct("move position",
    QStruct("position", INCLUDE=xyz_float),
    float_rad("facing"),  # radians
    Float("weight"),
    from_to_sec("time"),
    dyn_senum16("animation",
        DYN_NAME_PATH="tagdata.ai_animation_references.STEPTREE[DYN_I].animation_name"),
    SInt8("sequence id"),

    Pad(45),
    SInt32("surface index"),
    SIZE=80
    )

actor_starting_location = Struct("starting location",
    QStruct("position", INCLUDE=xyz_float),
    float_rad("facing"),  # radians
    Pad(2),
    SInt8("sequence id"),
    Bool8("flags",
        "required",
        ),
    SEnum16("return state",  *(dict(NAME=n, GUI_NAME=n) for n in squad_states)),
    SEnum16("initial state", *(dict(NAME=n, GUI_NAME=n) for n in squad_states)),
    dyn_senum16("actor type",
        DYN_NAME_PATH="tagdata.actors_palette.STEPTREE[DYN_I].name.filepath"),
    dyn_senum16("command list",
        DYN_NAME_PATH="tagdata.command_lists.STEPTREE[DYN_I].name"),
    SIZE=28
    )

squad = Struct("squad",
    ascii_str32("name"),
    dyn_senum16("actor type",
        DYN_NAME_PATH="tagdata.actors_palette.STEPTREE[DYN_I].name.filepath"),
    dyn_senum16("platoon",
        DYN_NAME_PATH=".....platoons.STEPTREE[DYN_I].name"),
    SEnum16("initial state", *(dict(NAME=n, GUI_NAME=n) for n in squad_states)),
    SEnum16("return state",  *(dict(NAME=n, GUI_NAME=n) for n in squad_states)),
    Bool32("flags",
        "unused",
        "never search",
        "start timer immediately",
        "no timer, delay forever",
        "magic sight after timer",
        "automatic migration",
        ),
    SEnum16("unique leader type",
        "normal",
        "none",
        "random",
        "sgt johnson",
        "sgt lehto",
        ),

    Pad(32),
    dyn_senum16("maneuver to squad", DYN_NAME_PATH="..[DYN_I].name"),
    float_sec("squad delay time"),  # seconds
    Bool32("attacking", *group_indices),
    Bool32("attacking search", *group_indices),
    Bool32("attacking guard", *group_indices),
    Bool32("defending", *group_indices),
    Bool32("defending search", *group_indices),
    Bool32("defending guard", *group_indices),
    Bool32("pursuing", *group_indices),

    Pad(12),
    SInt16("normal diff count"),
    SInt16("insane diff count"),
    SEnum16("major upgrade",
        "normal",
        "few",
        "many",
        "none",
        "all",
        ),
    Pad(2),

    SInt16("respawn min actors"),
    SInt16("respawn max actors"),
    SInt16("respawn total"),
    Pad(2),

    from_to_sec("respawn delay"),

    Pad(48),
    reflexive("move positions", move_position, 31),
    reflexive("starting locations", actor_starting_location, 31),
    SIZE=232
    )

platoon = Struct("platoon",
    ascii_str32("name"),
    Bool32("flags",
        "flee when maneuvering",
        "say advancing when maneuvering",
        "start in defending state",
        ),

    Pad(12),
    SEnum16("change attacking/defending state", *maneuver_when_states),
    dyn_senum16("change happens to", DYN_NAME_PATH="..[DYN_I].name"),

    Pad(8),
    SEnum16("maneuver when", *maneuver_when_states),
    dyn_senum16("maneuver happens to", DYN_NAME_PATH="..[DYN_I].name"),
    SIZE=172
    )

firing_position = Struct("firing position",
    QStruct("position", INCLUDE=xyz_float),
    SEnum16("group index", *group_indices),
    SIZE=24
    )

encounter = Struct("encounter",
    ascii_str32("name"),
    Bool32("flags",
        "not initially created",
        "respawn enabled",
        "initially blind",
        "initially deaf",
        "initially braindead",
        "firing positions are 3d",
        "manual bsp index specified",
        ),
    SEnum16("team index",
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
    SInt16('unknown', VISIBLE=False),
    SEnum16("search behavior",
        "normal",
        "never",
        "tenacious"
        ),
    dyn_senum16("manual bsp index",
        DYN_NAME_PATH=".....structure_bsps.STEPTREE[DYN_I].structure_bsp.filepath"),
    from_to_sec("respawn delay"),

    Pad(76),
    reflexive("squads", squad, 64),
    reflexive("platoons", platoon, 32, DYN_NAME_PATH='.name'),
    reflexive("firing positions", firing_position, 512),
    reflexive("player starting locations", player_starting_location2, 256),
    
    SIZE=176
    )

command = Struct("command",
    SEnum16("atom type", *atom_types),
    SInt16("atom modifier"),
    Float("parameter 1"),
    Float("parameter 2"),
    dyn_senum16("point 1", DYN_NAME_PATH=".....points.STEPTREE[DYN_I]"),
    dyn_senum16("point 2", DYN_NAME_PATH=".....points.STEPTREE[DYN_I]"),
    dyn_senum16("animation",
        DYN_NAME_PATH="tagdata.ai_animation_references.STEPTREE[DYN_I].animation_name"),
    dyn_senum16("script",
        DYN_NAME_PATH="tagdata.scripts.STEPTREE[DYN_I].name"),
    dyn_senum16("recording",
        DYN_NAME_PATH="tagdata.ai_recording_references.STEPTREE[DYN_I].recording_name"),
    dyn_senum16("command", DYN_NAME_PATH="..[DYN_I].atom_type.enum_name"),
    dyn_senum16("object name", DYN_NAME_PATH="tagdata.object_names.STEPTREE[DYN_I].name"),
    SIZE=32
    )

point = Struct("point",
    QStruct("position", INCLUDE=xyz_float),
    SIZE=20
    )

command_list = Struct("command list",
    ascii_str32("name"),
    Bool32("flags",
        "allow initiative",
        "allow targeting",
        "disable looking",
        "disable communication",
        "disable falling damage",
        "manual bsp index",
        ),

    Pad(8),
    dyn_senum16("manual bsp index",
        DYN_NAME_PATH=".....structure_bsps.STEPTREE[DYN_I].structure_bsp.filepath"),

    Pad(2),
    reflexive("commands", command, 64),
    reflexive("points", point, 64),
    SIZE=96
    )

participant = Struct("participant",
    Pad(2),
    Bool16("flags",
        "optional",
        "has alternate",
        "is alternate",
        ),
    SEnum16("selection type",
        "friendly actor",
        "disembodied",
        "in players vehicle",
        "not in a vehicle",
        "prefer sergeant",
        "any actor",
        "radio unit",
        "radio sergeant",
        ),
    SEnum16("actor type", *actor_types),
    dyn_senum16("use this object", DYN_NAME_PATH="tagdata.object_names.STEPTREE[DYN_I].name"),
    dyn_senum16("set new name", DYN_NAME_PATH="tagdata.object_names.STEPTREE[DYN_I].name"),

    Pad(12),
    BytesRaw("unknown", DEFAULT=b"\xFF"*12, SIZE=12, VISIBLE=False),
    ascii_str32("encounter name"),
    SIZE=84
    )

line = Struct("line",
    Bool16("flags",
        "addressee look at speaker",
        "everyone look at speaker",
        "everyone look at addressee",
        "wait until told to advance",
        "wait until speaker nearby",
        "wait until everyone nearby",
        ),
    dyn_senum16("participant",
        DYN_NAME_PATH=".....participants.STEPTREE[DYN_I].encounter_name"),
    SEnum16("addressee",
        "none",
        "player",
        "participant",
        ),
    dyn_senum16("addressee participant",
        DYN_NAME_PATH=".....participants.STEPTREE[DYN_I].encounter_name"),

    Pad(4),
    Float("line delay time"),

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
    Bool16("flags",
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
    float_wu("trigger distance"),
    float_wu("run-to-player distance"),

    Pad(36),
    reflexive("participants", participant, 8,
        DYN_NAME_PATH='.encounter_name'),
    reflexive("lines", line, 32),
    SIZE=116
    )

structure_bsp = Struct("structure bsp",
    FlUInt32("bsp pointer", VISIBLE=False),
    FlUInt32("bsp size", VISIBLE=False),
    FlUInt32("bsp magic", VISIBLE=False),
    Pad(4),
    dependency("structure bsp", "sbsp"),
    SIZE=32
    )

scnr_body = Struct("tagdata",
    dependency("DONT USE", 'sbsp'),
    dependency("WONT USE", 'sbsp'),
    dependency("CANT USE", 'sky '),
    reflexive("skies", sky, 8, DYN_NAME_PATH='.sky.filepath'),
    SEnum16("type",
        "singleplayer",
        "multiplayer",
        "main menu"
        ),
    Bool16("flags",
        "cortana hack",
        "use demo ui"
        ),
    reflexive("child scenarios", child_scenario, 16,
        DYN_NAME_PATH='.child_scenario.filepath'),
    float_rad("local north"),  # radians

    Pad(156),
    reflexive("predicted resources", predicted_resource, 1024, VISIBLE=False),
    reflexive("functions", function, 32,
        DYN_NAME_PATH='.name'),
    rawdata_ref("scenario editor data", max_size=65536),
    reflexive("comments", comment, 1024),

    Pad(224),
    reflexive("object names", object_name, 512,
        DYN_NAME_PATH='.name'),
    reflexive("sceneries", scenery, 2000),
    reflexive("sceneries palette", scenery_swatch, 100,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("bipeds", biped, 128),
    reflexive("bipeds palette", biped_swatch, 100,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("vehicles", vehicle, 80),
    reflexive("vehicles palette", vehicle_swatch, 100,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("equipments", equipment, 256),
    reflexive("equipments palette", equipment_swatch, 100,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("weapons", weapon, 128),
    reflexive("weapons palette", weapon_swatch, 100,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("device groups", device_group, 128,
        DYN_NAME_PATH='.name'),
    reflexive("machines", machine, 400),
    reflexive("machines palette", machine_swatch, 100,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("controls", control, 100),
    reflexive("controls palette", control_swatch, 100,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("light fixtures", light_fixture, 500),
    reflexive("light fixtures palette", light_fixture_swatch, 100,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("sound sceneries", sound_scenery, 256),
    reflexive("sound sceneries palette", sound_scenery_swatch, 100,
        DYN_NAME_PATH='.name.filepath'),

    Pad(84),
    reflexive("player starting profiles", player_starting_profile, 256,
        DYN_NAME_PATH='.name'),
    reflexive("player starting locations", player_starting_location, 256),
    reflexive("trigger volumes", trigger_volume, 256,
        DYN_NAME_PATH='.name'),
    reflexive("recorded animations", recorded_animation, 1024,
        DYN_NAME_PATH='.name'),
    reflexive("netgame flags", netgame_flag, 200,
        DYN_NAME_PATH='.type.enum_name'),
    reflexive("netgame equipments", netgame_equipment, 200,
        DYN_NAME_PATH='.item_collection.filepath'),
    reflexive("starting equipments", starting_equipment, 200),
    reflexive("bsp switch trigger volumes", bsp_switch_trigger_volume, 256),
    reflexive("decals", decal, 65535),
    reflexive("decals palette", decal_swatch, 128,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("detail object collection palette",
        detail_object_collection_swatch, 32, DYN_NAME_PATH='.name.filepath'),

    Pad(84),
    reflexive("actors palette", actor_swatch, 64,
        DYN_NAME_PATH='.name.filepath'),
    reflexive("encounters", encounter, 128, DYN_NAME_PATH='.name'),
    reflexive("command lists", command_list, 256, DYN_NAME_PATH='.name'),
    reflexive("ai animation references", ai_anim_reference, 128,
        DYN_NAME_PATH='.animation_name'),
    reflexive("ai script references", ai_script_reference, 128,
        DYN_NAME_PATH='.script_name'),
    reflexive("ai recording references", ai_recording_reference, 128,
        DYN_NAME_PATH='.recording_name'),
    reflexive("ai conversations", ai_conversation, 128,
        DYN_NAME_PATH='.name'),
    rawdata_ref("script syntax data", max_size=380076),
    rawdata_ref("script string data", max_size=262144),
    reflexive("scripts", halo_script, 512, DYN_NAME_PATH='.name'),
    reflexive("globals", halo_global, 128, DYN_NAME_PATH='.name'),
    reflexive("references", reference, 256,
              DYN_NAME_PATH='.reference.filepath'),
    reflexive("source files", source_file, 8, DYN_NAME_PATH='.source_name'),

    Pad(24),
    reflexive("cutscene flags", cutscene_flag, 512, DYN_NAME_PATH='.name'),
    reflexive("cutscene camera points", cutscene_camera_point, 512,
        DYN_NAME_PATH='.name'),
    reflexive("cutscene titles", cutscene_title, 64, DYN_NAME_PATH='.name'),
    Pad(12), # OS bsp_modifiers reflexive

    Pad(96),
    dependency("custom object names", 'ustr'),
    dependency("ingame help text", 'ustr'),
    dependency("hud messages", 'hmt '),
    reflexive("structure bsps", structure_bsp, 16,
        DYN_NAME_PATH='.structure_bsp.filepath'),
    SIZE=1456,
    )

def get():
    return scnr_def

scnr_def = TagDef("scnr",
    blam_header('scnr', 2),
    scnr_body,

    ext=".scenario", endian=">", tag_cls=HekTag
    )
