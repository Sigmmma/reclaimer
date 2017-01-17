from copy import copy, deepcopy
from math import pi

from .hek.programs.mozzarilla.field_widgets import *
from supyr_struct.defs.common_descs import *
from supyr_struct.defs.block_def import BlockDef
from .field_types import *
from .constants import *

def tag_class(*args, **kwargs):
    '''
    A macro for creating a tag_class enum desc with the
    enumerations set to the provided tag_class fcc's.
    '''
    classes = []
    for four_cc in args:
        classes.append((tag_class_fcc_to_ext[four_cc], four_cc))

    return BUEnum32(
        'tag_class',
        *(tuple(sorted(classes)) + (("NONE", 0xffffffff),) ),
        DEFAULT=0xffffffff, GUI_NAME='', WIDGET_WIDTH=20, **kwargs
        )


def reflexive(name, substruct, max_count=MAX_REFLEXIVE_COUNT, *names, **desc):
    '''This function serves to macro the creation of a reflexive'''
    desc.update(
        INCLUDE=reflexive_struct,
        STEPTREE=Array(name + " array",
            SIZE=".size", MAX=max_count,
            SUB_STRUCT=substruct, WIDGET=ReflexiveFrame
            ),
        SIZE=12
        )
    if DYN_NAME_PATH in desc:
        desc[STEPTREE][DYN_NAME_PATH] = desc.pop(DYN_NAME_PATH)
    if names:
        name_map = {}
        for i in range(len(names)):
            e_name = BlockDef.str_to_name(None, names[i])
            name_map[e_name] = i
            
        desc[STEPTREE][NAME_MAP] = name_map

    return Reflexive(name, **desc)


def rawdata_ref(name, f_type=Rawdata, max_size=None, widget=HaloRawdataFrame):
    '''This function serves to macro the creation of a rawdata reference'''
    ref_struct = dict(rawdata_ref_struct)
    if max_size is not None:
        ref_struct[0] = dict(ref_struct[0])
        ref_struct[0][MAX] = max_size

    kwargs = {}
    if widget is not None:
        kwargs[WIDGET] = widget

    return RawdataRef(name,
        INCLUDE=ref_struct,
        STEPTREE=f_type("data", GUI_NAME="", SIZE=".size", **kwargs))


def rawtext_ref(name, f_type=StrRawAscii, max_size=None, widget=TextFrame):
    '''This function serves to macro the creation of a rawdata reference'''
    ref_struct = dict(rawdata_ref_struct)
    if max_size is not None:
        ref_struct[0] = dict(ref_struct[0])
        ref_struct[0][MAX] = max_size
        ref_struct[0][VISIBLE] = False

    return RawdataRef(name,
        INCLUDE=ref_struct, GUI_NAME='',
        STEPTREE=f_type("data",
            SIZE=".size", GUI_NAME=name.replace('_', ' '), WIDGET=widget)
            )


def dependency(name='tag ref', valid_ids=None):
    '''This function serves to macro the creation of a tag dependency'''
    if isinstance(valid_ids, tuple):
        valid_ids = tag_class(*valid_ids)
    elif isinstance(valid_ids, str):
        valid_ids = tag_class(valid_ids)
    elif valid_ids is None:
        valid_ids = valid_tags

    return TagIndexRef(name,
        valid_ids,
        BSInt32("path pointer", VISIBLE=False, EDITABLE=False),
        BSInt32("path length", MAX=243, VISIBLE=False, EDITABLE=False),
        BUInt32("id", DEFAULT=0xFFFFFFFF, VISIBLE=False, EDITABLE=False),

        STEPTREE=HaloRefStr(
            "filepath", SIZE=tag_ref_size, GUI_NAME="", MAX=244),
        ORIENT='h'
        )


def blam_header(tagid, version=1):
    '''This function serves to macro the creation of a tag header'''
    header_desc= dict(tag_header)
    header_desc[1] = dict(header_desc[1])
    header_desc[5] = dict(header_desc[5])
    header_desc[1][DEFAULT] = tagid
    header_desc[5][DEFAULT] = version
    return header_desc

irad = 180/pi

def dyn_senum8(name, *args, **kwargs):
    kwargs.setdefault('DEFAULT', -1)
    kwargs.setdefault('WIDGET', DynamicEnumFrame)
    return SInt8(name, *args, **kwargs)

def dyn_senum16(name, *args, **kwargs):
    kwargs.setdefault('DEFAULT', -1)
    kwargs.setdefault('WIDGET', DynamicEnumFrame)
    return BSInt16(name, *args, **kwargs)

def dyn_senum32(name, *args, **kwargs):
    kwargs.setdefault('DEFAULT', -1)
    kwargs.setdefault('WIDGET', DynamicEnumFrame)
    return BSInt32(name, *args, **kwargs)

def ascii_str32(name):
    # encoding used is latin1 to take care of cases
    # where the string has invalid characters in it
    return StrLatin1(str(name), SIZE=32)

def float_zero_to_one(name, *args, **kwargs):
    return BFloat(name, *args, MIN=0.0, MAX=1.0, SIDETIP="[0,1]", **kwargs)
def float_neg_one_to_one(name, *args, **kwargs):
    return BFloat(name, *args, MIN=-1.0, MAX=1.0, SIDETIP="[-1,1]", **kwargs)

def float_sec(name, *args, **kwargs):
    return BFloat(name, *args, SIDETIP="seconds", **kwargs)

def float_deg(name, *args, **kwargs):
    return BFloat(name, *args, SIDETIP="degrees", **kwargs)
def float_deg_sec(name, *args, **kwargs):
    return BFloat(name, *args, SIDETIP="degrees/sec", **kwargs)

def float_rad(name, *args, **kwargs):
    return BFloat(name, *args, SIDETIP="degrees", UNIT_SCALE=irad, **kwargs)
def float_rad_sec(name, *args, **kwargs):
    return BFloat(name, *args, SIDETIP="degrees/sec", UNIT_SCALE=irad, **kwargs)
def float_rad_sec_sq(name, *args, **kwargs):
    return BFloat(
        name, *args, SIDETIP="degrees/(sec^2)", UNIT_SCALE=irad, **kwargs)

def float_wu(name, *args, **kwargs):
    return BFloat(name, *args, SIDETIP="world units", **kwargs)
def float_wu_sec(name, *args, **kwargs):
    return BFloat(name, *args, SIDETIP="world units/sec", **kwargs)
def float_wu_sec_sq(name, *args, **kwargs):
    return BFloat(name, *args, SIDETIP="world units/(sec^2)", **kwargs)

def float_zero_to_inf(name, *args, **kwargs):
    return BFloat(name, *args, SIDETIP="[0,+inf]", **kwargs)


from_to = QStruct('',
    BFloat("from", GUI_NAME=''),
    BFloat("to"),
    ORIENT='h'
    )

def from_to_deg(name, *args, **kwargs):
    return QStruct(name,
        BFloat("from", GUI_NAME=''),
        BFloat("to"), *args,
        ORIENT='h', SIDETIP='degrees', **kwargs
        )

def from_to_rad(name, *args, **kwargs):
    return QStruct(name,
        BFloat("from", UNIT_SCALE=irad, GUI_NAME=''),
        BFloat("to", UNIT_SCALE=irad), *args,
        ORIENT='h', SIDETIP='degrees', **kwargs
        )

def from_to_rad_sec(name, *args, **kwargs):
    return QStruct(name,
        BFloat("from", UNIT_SCALE=irad, GUI_NAME=''),
        BFloat("to", UNIT_SCALE=irad), *args,
        ORIENT='h', SIDETIP='degrees/sec', **kwargs
        )

def from_to_sec(name, *args, **kwargs):
    return QStruct(name,
        BFloat("from", GUI_NAME=''),
        BFloat("to"), *args,
        ORIENT='h', SIDETIP='seconds', **kwargs
        )

def from_to_wu(name, *args, **kwargs):
    return QStruct(name,
        BFloat("from", GUI_NAME=''),
        BFloat("to"), *args,
        ORIENT='h', SIDETIP='world units', **kwargs
        )

def from_to_wu_sec(name, *args, **kwargs):
    return QStruct(name,
        BFloat("from", GUI_NAME=''),
        BFloat("to"), *args,
        ORIENT='h', SIDETIP='world units/sec', **kwargs
        )

def from_to_zero_to_one(name, *args, **kwargs):
    return QStruct(name,
        BFloat("from", MIN=0.0, MAX=1.0, GUI_NAME=''),
        BFloat("to", MIN=0.0, MAX=1.0), *args,
        ORIENT='h', SIDETIP='[0,1]', **kwargs
        )

def from_to_neg_one_to_one(name, *args, **kwargs):
    return QStruct(name,
        BFloat("from", MIN=-1.0, MAX=1.0, GUI_NAME=''),
        BFloat("to", MIN=-1.0, MAX=1.0), *args,
        ORIENT='h', SIDETIP='[-1,1]', **kwargs
        )

def yp_float_deg(name, *args, **kwargs):
    return QStruct(name,
        BFloat("y"), BFloat("p"), *args,
        ORIENT='h', SIDETIP='degrees', **kwargs
        )

def ypr_float_deg(name, *args, **kwargs):
    return QStruct(name,
        BFloat("y"), BFloat("p"), BFloat("r"), *args,
        ORIENT='h', SIDETIP='degrees', **kwargs
        )

def yp_float_rad(name, *args, **kwargs):
    return QStruct(name,
        BFloat("y", UNIT_SCALE=irad),
        BFloat("p", UNIT_SCALE=irad), *args,
        ORIENT='h', SIDETIP='degrees', **kwargs
        )

def ypr_float_rad(name, *args, **kwargs):
    return QStruct(name,
        BFloat("y", UNIT_SCALE=irad),
        BFloat("p", UNIT_SCALE=irad),
        BFloat("r", UNIT_SCALE=irad), *args,
        ORIENT='h', SIDETIP='degrees', **kwargs
        )


valid_tags = tag_class(*tag_class_fcc_to_ext.keys())
valid_models = tag_class('mode', 'mod2')
valid_event_effects = tag_class('effe', 'snd!')
valid_attachments = tag_class('cont', 'effe', 'ligh', 'mgs2', 'pctl', 'lsnd')
valid_effect_events = tag_class(
    'bipd', 'jpt!', 'deca', 'devi', 'ctrl', 'lifi', 'mach',
    'eqip', 'garb', 'item', 'ligh', 'obje', 'pctl', 'plac',
    'proj', 'scen', 'snd!', 'ssce', 'unit', 'vehi', 'weap'
    )
valid_items = tag_class('eqip', 'garb', 'item', 'weap')
valid_objects = tag_class(
    'bipd', 'ctrl', 'lifi', 'mach', 'eqip', 'garb', 'obje',
    'plac', 'proj', 'scen', 'ssce', 'vehi', 'weap'
    )
valid_units = tag_class('bipd', 'unit', 'vehi')
valid_devices_items_objects_units = tag_class(
    'bipd', 'devi', 'ctrl', 'lifi', 'mach', 'eqip', 'garb', 'item',
    'obje', 'plac', 'proj', 'scen', 'ssce', 'unit', 'vehi', 'weap'
    )
valid_shaders = tag_class(
    'shdr', 'schi', 'scex', 'sotr', 'senv',
    'sgla', 'smet', 'soso', 'spla', 'swat'
    )
valid_widgets = tag_class('ant!', 'flag', 'glw!', 'mgs2', 'elec')


# ###########################################################################
# The order of element in all the enumerators is important(DONT SHUFFLE THEM)
# ###########################################################################

#Shared Enumerator options
materials_list = (
    "dirt",
    "sand",
    "stone",
    "snow",
    "wood",
    "metal hollow",
    "metal thin",
    "metal thick",
    "rubber",
    "glass",
    "force field",
    "grunt",
    "hunter armor",
    "hunter skin",
    "elite",
    "jackal",
    "jackal energy shield",
    "engineer skin",
    "engineer force field",
    "flood combat form",
    "flood carrier form",
    "cyborg armor",
    "cyborg energy shield",
    "human armor",
    "human skin",
    "sentinel",
    "moniter",
    "plastic",
    "water",
    "leaves",
    "elite energy shield",
    "ice",
    "hunter shield",
    )
actor_types = (
    "elite",
    "jackal",
    "grunt",
    "hunter",
    "engineer",
    "assassin",
    "player",
    "marine",
    "crew",
    "combat form",
    "infection form",
    "carrier form",
    "moniter",
    "sentinal",
    "none",
    "mounted weapon"
    )
animation_functions = (
    "one",
    "zero",
    "cosine",
    "cosine variable period",
    "diagonal wave",
    "diagonal wave variable period",
    "slide",
    "slide variable period",
    "noise",
    "jitter",
    "wander",
    "spark",
    )
sound_volumes = (
    "silent",
    "medium",
    "loud",
    "shout",
    "quiet"
    )
damage_category = (
    "none",
    "falling",
    "bullet",
    "grenade",
    "high explosive",
    "sniper",
    "melee",
    "flame",
    "mounted weapon",
    "vehicle",
    "plasma",
    "needle",
    "shotgun",
    )
grenade_types = (
    'human frag',
    'covenant plasma'
    )
fade_functions = (
    "linear",
    "early",
    "very early",
    "late",
    "very late",
    "cosine",
    )
detail_map_functions = (
    "double/biased multiply",
    "multiply",
    "double/biased add",
    )
device_functions = (
    "none",
    "power",
    "change in power",
    "position",
    "change in position",
    "locked",
    "delay",
    )
render_anchor = (
    "with primary",
    "with screen space",
    "with zsprite"
    )
render_fade_mode = (
    "none",
    "fade when perpendicular",
    "fade when parallel",
    )
render_mode = (
    "screen facing",
    "parallel to direction",
    "perpendicular to direction"
    )
shader_flags = (
    "sort bias",
    "nonlinear tint",
    "dont overdraw fp weapon"
    )
blend_flags = (
    "blend in hsv",
    "more colors"
    )
hud_scaling_flags = (
    "dont scale offset",
    "dont scale size",
    "use high res scale"
    )
hud_flash_flags = (
    "reverse default and flashing colors",
    )
hud_anchors = (
    "top left",
    "top right",
    "bottom left",
    "bottom right",
    "center"
    )
hud_panel_meter_flags = (
    "use min/max for state changes",
    "interpolate between min/max flash colors",
    "interpolate color along hsv space",
    "more colors for hsv interpolation ",
    "invert interpolation"
    )
multitex_anchors = (
    "texture",
    "screen",
    )
multitex_wrap_modes = (
    "clamp",
    "wrap",
    )
blending_funcs = (
    "add",
    "subtract",
    "multiply",
    "multiply 2x",
    "dot",
    )
blend_functions = (
    "current",
    "next map",
    "multiply",
    "double multiply",
    "add",
    "add-signed current",
    "add-signed next map",
    "subtract-signed current",
    "subtract-signed next map",
    "blend current alpha",
    "blend current alpha-inverse",
    "blend next map alpha",
    "blend next map alpha-inverse",
    )
framebuffer_blend_functions = (
    "alpha blend",
    "multiply",
    "double multiply",
    "add",
    "subtract",
    "component min",
    "component max",
    "alpha-multiply add",
    )
script_types = (
    "startup",
    "dormant",
    "continuous",
    "static",
    "stub",
    )
script_object_types = (
    "unparsed",
    "special form",
    "function name",
    "passthrough",
    "void",
    "boolean",
    "real",
    "short",
    "long",
    "string",
    "script",

    "trigger volume",
    "cutscene flag",
    "cutscene camera point",
    "cutscene title",
    "cutscene recording",

    "device group",
    "ai",
    "ai command list",
    "starting profile",

    "conversation",
    "navpoint",
    "hud message",
    "object list",

    "sound",
    "effect",
    "damage",
    "looping sound",
    "animation graph",
    "actor variant",
    "damage effect",

    "object definition",
    "game difficulty",
    "team",
    "ai default state",
    "actor type",
    "hud corner",

    "object",
    "unit",
    "vehicle",
    "weapon",
    "device",
    "scenery",

    "object name",
    "unit name",
    "vehicle name",
    "weapon name",
    "device name",
    "scenery name"
    )
function_names = (
    "none",
    "A",
    "B",
    "C",
    "D",
    )
function_inputs_outputs = (
    "none",
    "A in",
    "B in",
    "C in",
    "D in",
    "A out",
    "B out",
    "C out",
    "D out",
    )
function_inputs = (
    "none",
    "A in",
    "B in",
    "C in",
    "D in",
    )
function_outputs = (
    "none",
    "A out",
    "B out",
    "C out",
    "D out",
    )
#Tag class specific enumerators
object_export_to = (
    'none',
    'body vitality',
    'shield vitality',
    'recent body damage',
    'recent shield damage',
    'random constant',
    'umbrella shield vitality',
    'shield stun',
    'recent umbrella shield vitality',
    'umbrella shield stun',
    'region 0 damage',
    'region 1 damage',
    'region 2 damage',
    'region 3 damage',
    'region 4 damage',
    'region 5 damage',
    'region 6 damage',
    'region 7 damage',
    'alive',
    'compass',
    )
weapon_export_to = (
    'none',
    'heat',
    'primary ammunition',
    'secondary ammunition',
    'primary rate of fire',
    'secondary rate of fire',
    'ready',
    'primary ejection port',
    'secondary ejection port',
    'overheated',
    'primary charged',
    'secondary charged',
    'illumination',
    'age',
    'integrated light',
    'primary firing',
    'secondary firing',
    'primary firing on',
    'secondary firing on',
    )
biped_inputs = (
    'none',
    'flying velocity'
    )
projectile_inputs = (
    "none",
    "range remaining",
    "time remaining",
    "tracer",
    )
unit_inputs = (
    "none",
    "driver seat power",
    "gunner seat power",
    "aiming change",
    "mouth aperture",
    "integrated light power",
    "can blink",
    "shield sapping"
    )
unit_teams = (
    "none",
    "player",
    "human",
    "covenant",
    "flood",
    "sentinel",
    "unused6",
    "unused7",
    "unused8",
    "unused9",
    )
vehicle_inputs = (
    "none",
    "speed absolute",
    "speed forward",
    "speed backward",
    "slide absolute",
    "slide left",
    "slide right",
    "speed slide maximum",
    "turn absolute",
    "turn left",
    "turn right",
    "crouch",
    "jump",
    "walk",
    "velocity air",
    "velocity water",
    "velocity ground",
    "velocity forward",
    "velocity left",
    "velocity up",
    "left tread position",
    "right tread position",
    "left tread velocity",
    "right tread velocity",
    "front left tire position",
    "front right tire position",
    "back left tire position",
    "back right tire position",
    "front left tire velocity",
    "front right tire velocity",
    "back left tire velocity",
    "back right tire velocity",
    "wingtip contrail",
    "hover",
    "thrust",
    "engine hack",
    "wingtip contrail new",
    )
vehicle_types = (
    "human tank",
    "human jeep",
    "human boat",
    "human plane",
    "alien scout",
    "alien fighter",
    "turret",
    )
weapon_types = (
    "undefined",
    "shotgun",
    "needler",
    "plasma pistol",
    "plasma rifle",
    )
trans_shdr_properties = (
    "alpha tested",
    "decal",
    "two sided",
    "first map is in screenspace",
    "draw before water",
    "ignore effect",
    "scale first map with distance",
    "numeric",
    )
trans_shdr_first_map_type = (
    "map 2d",
    "reflection cube map",
    "object centered cube map",
    "viewer centered cube map",
    )
detail_mask = (
    "none",
    "red inverse",
    "red",
    "green inverse",
    "green",
    "blue inverse",
    "blue",
    "alpha inverse",
    "alpha"
    )

# Descriptors
tag_header = Struct("blam header",
    Pad(36),
    BUEnum32("tag_class",
        GUI_NAME="tag class", INCLUDE=valid_tags, EDITABLE=False
        ),
    LUInt32("base address", DEFAULT=0x4D6F7A7A,
        EDITABLE=False, VISIBLE=False),  #random
    LUInt32("header size",  DEFAULT=64, EDITABLE=False, VISIBLE=False),
    Pad(8),
    LUInt16("version", DEFAULT=1, EDITABLE=False),
    LUInt16("unknown", DEFAULT=255, EDITABLE=False, VISIBLE=False),
    LUEnum32("engine id",
        ("halo 1", 'blam'),
        DEFAULT='blam', EDITABLE=False
        ),
    VISIBLE=False, SIZE=64
    )

# Miscellaneous, Halo specific descriptors
anim_func_per_pha = Struct('',
    BSEnum16("function", *animation_functions),
    Pad(2),
    BFloat("period", SIDETIP='seconds'),  # seconds
    BFloat("phase", SIDETIP='seconds'),  # seconds
    )
anim_func_per_sca = Struct('',
    BSEnum16("function", *animation_functions),
    Pad(2),
    BFloat("period", SIDETIP='seconds'),  # seconds
    BFloat("scale", SIDETIP='base map repeats'),  # base map repeats
    )
anim_src_func_per_pha_sca = Struct('',
    BSEnum16("source", *function_outputs),
    BSEnum16("function", *animation_functions),
    BFloat("period", SIDETIP='seconds'),  # seconds
    BFloat("phase", SIDETIP='seconds'),  # seconds
    BFloat("scale", SIDETIP='repeats'),  # repeats
    )
anim_src_func_per_pha_sca_rot = Struct('',
    BSEnum16("source", *function_outputs),
    BSEnum16("function", *animation_functions),
    BFloat("period", SIDETIP='seconds'),  # seconds
    BFloat("phase", SIDETIP='seconds'),  # seconds
    BFloat("scale", SIDETIP='degrees'),  # repeats
    )


# This is the descriptor used wherever a tag references a rawdata chunk
rawdata_ref_struct = RawdataRef('rawdata ref', 
    BSInt32("size", EDITABLE=False, GUI_NAME="", SIDETIP="bytes"),
    BSInt32("unknown 1", EDITABLE=False, VISIBLE=False),  # 0x00 in tags(and meta it seems)
    BSInt32("unknown 2", EDITABLE=False, VISIBLE=False),  # random(low number in meta)
    BSInt32("pointer", EDITABLE=False, VISIBLE=False, DEFAULT=-1),
    BUInt32("id", EDITABLE=False, VISIBLE=False),  # 0x00000000 in meta it seems,
    ORIENT='h'
    )

# This is the descriptor used wherever a tag reference a reflexive
reflexive_struct = Reflexive('reflexive',
    BSInt32("size", EDITABLE=False, VISIBLE=False),
    BSInt32("pointer", DEFAULT=-1, EDITABLE=False, VISIBLE=False),  # random
    BUInt32("id", EDITABLE=False, VISIBLE=False),  # 0x00000000 in meta it seems
    )

predicted_resource = Struct('predicted_resource',
    BSInt16('type',
        'bitmap',
        'sound',
        ),
    BSInt16('resource index'),
    BSInt32('tag index'),
    )

# This is the descriptor used wherever a tag references another tag
tag_index_ref_struct = dependency()

extra_layers_block = dependency("extra layer", valid_shaders)

damage_modifiers = QStruct("damage modifiers",
    *(float_zero_to_inf(material_name) for material_name in materials_list)
    )

# Miscellaneous shared descriptors
compressed_normal_32 = BitStruct('compressed_norm32',
    Bit1SInt("i",
        SIZE=11, UNIT_SCALE=1/1023, MIN=-1023, MAX=1023, WIDGET_WIDTH=10),
    Bit1SInt("j",
        SIZE=11, UNIT_SCALE=1/1023, MIN=-1023, MAX=1023, WIDGET_WIDTH=10),
    Bit1SInt("k",
        SIZE=10, UNIT_SCALE=1/511, MIN=-511, MAX=511, WIDGET_WIDTH=10),
    ORIENT='h'
    )

# coordinates
xyz_float = QStruct('xyz_float',
    Float("x"), Float("y"), Float("z"), ORIENT='h' 
    )
xy_float = QStruct('xy_float',
    Float("x"), Float("y"), ORIENT='h'
    )

# colors
argb_float = QStruct('argb_float',
    Float("a", MIN=0.0, MAX=1.0),
    Float("r", MIN=0.0, MAX=1.0),
    Float("g", MIN=0.0, MAX=1.0),
    Float("b", MIN=0.0, MAX=1.0),
    ORIENT='h', WIDGET=ColorPickerFrame
    )
rgb_float = QStruct('rgb_float',
    Float("r", MIN=0.0, MAX=1.0),
    Float("g", MIN=0.0, MAX=1.0),
    Float("b", MIN=0.0, MAX=1.0),
    ORIENT='h', WIDGET=ColorPickerFrame
    )
rgb_byte = QStruct('rgb_uint8',
    UInt8("r"), UInt8("g"), UInt8("b"),
    ORIENT='h', WIDGET=ColorPickerFrame
    )
argb_byte = QStruct('argb_uint8',
    UInt8("a"), UInt8("r"), UInt8("g"), UInt8("b"),
    ORIENT='h', WIDGET=ColorPickerFrame
    )

# rotations
ijkw_float = QStruct('ijkw_float',
    Float("i"), Float("j"), Float("k"), Float("w"),
    ORIENT='h'
    )
ijk_float = QStruct('ijk_float',
    Float("i"), Float("j"), Float("k"),
    ORIENT='h'
    )
ij_float = QStruct('ij_float',
    Float("i"), Float("j"),
    ORIENT='h'
    )
yp_float = QStruct('yp_float',
    BFloat("y"), BFloat("p"),
    ORIENT='h',
    )
ypr_float = QStruct('ypr_float',
    BFloat("y"), BFloat("p"), BFloat("r"),
    ORIENT='h',
    )


#############################
# Open Sauce related things #
#############################
def tag_class_os(*args):
    '''
    A macro for creating an Open Sauce tag_class enum desc
    with the enumerations set to the provided tag_class fcc's.
    '''
    classes = []
    for four_cc in sorted(args):
        classes.append((tag_class_fcc_to_ext_os[four_cc], four_cc))

    return BUEnum32(
        'tag_class',
        *(tuple(classes) + (("NONE", 0xffffffff),) ),
        DEFAULT=0xffffffff, GUI_NAME=''
        )


def dependency_os(name='tag ref', valid_ids=None):
    '''This function serves to macro the creation of a tag dependency'''
    if isinstance(valid_ids, tuple):
        valid_ids = tag_class_os(*valid_ids)
    elif isinstance(valid_ids, str):
        valid_ids = tag_class_os(valid_ids)
    elif valid_ids is None:
        valid_ids = valid_tags_os

    return TagIndexRef(name,
        valid_ids,
        BSInt32("path pointer", VISIBLE=False, EDITABLE=False),
        BSInt32("path length", MAX=243, VISIBLE=False, EDITABLE=False),
        BUInt32("id", DEFAULT=0xFFFFFFFF, VISIBLE=False, EDITABLE=False),

        STEPTREE=HaloRefStr(
            "filepath", SIZE=tag_ref_size, GUI_NAME="", MAX=244),
        ORIENT='h'
        )


def blam_header_os(tagid, version=1):
    '''This function serves to macro the creation of a tag header'''
    header_desc= dict(tag_header_os)
    header_desc[1] = dict(header_desc[1])
    header_desc[5] = dict(header_desc[5])
    header_desc[1][DEFAULT] = tagid
    header_desc[5][DEFAULT] = version
    return header_desc


valid_tags_os = tag_class_os(*tag_class_fcc_to_ext_os.keys())


# ###########################################################################
# The order of element in all the enumerators is important(DONT SHUFFLE THEM)
# ###########################################################################

#Shared Enumerator options
grenade_types_os = (
    'human frag',
    'covenant plasma',
    'custom 2',
    'custom 3',
    )

# Descriptors
tag_header_os = Struct("blam header",
    Pad(36),
    BUEnum32("tag_class",
        GUI_NAME="tag class", INCLUDE=valid_tags_os, EDITABLE=False
        ),
    LUInt32("base address", DEFAULT=0x4D6F7A7A,
        EDITABLE=False, VISIBLE=False),  #random
    LUInt32("header size",  DEFAULT=64, EDITABLE=False, VISIBLE=False),
    Pad(8),
    LUInt16("version", DEFAULT=1, EDITABLE=False),
    LUInt16("unknown", DEFAULT=255, EDITABLE=False, VISIBLE=False),
    LUEnum32("engine id",
        ("halo 1", 'blam'),
        DEFAULT='blam', EDITABLE=False
        ),
    VISIBLE=False, SIZE=64
    )

valid_model_animations_yelo = tag_class_os('antr', 'magy')

particle_shader_extension = Struct("particle shader extension",
    Struct("fade controls",
        Float("depth fade distance"),
        Float("camera fade distance"),
        COMMENT="Controls the softness of an effect"
        ),
    SIZE=48
    )

actor_states = (
    'none',
    'sleeping',
    'alert',
    'moving repeat same position',
    'moving loop',
    'moving loop back and forth',
    'moving loop randomly',
    'moving randomly',
    'guarding',
    'guarding at guard position',
    'searching',
    'fleeing'
    )
