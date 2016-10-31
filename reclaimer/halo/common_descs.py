from copy import copy, deepcopy

from supyr_struct.defs.common_descs import *
from supyr_struct.defs.block_def import BlockDef
from .field_types import *
from .constants import *

compressed_normal_32 = LBitStruct('compressed_norm32',
    Bit1SInt("i", SIZE=11),
    Bit1SInt("j", SIZE=11),
    Bit1SInt("k", SIZE=10)
    )

# coordinates
xyz_float = QStruct('xyz_float',
    Float("x"),
    Float("y"),
    Float("z")
    )
xy_float = QStruct('xy_float',
    LFloat("x"),
    LFloat("y")
    )

# colors
argb_float = QStruct('argb_float',
    LFloat("a", MIN=0.0, MAX=1.0),
    LFloat("r", MIN=0.0, MAX=1.0),
    LFloat("g", MIN=0.0, MAX=1.0),
    LFloat("b", MIN=0.0, MAX=1.0)
    )
rgb_float = QStruct('rgb_float',
    LFloat("r", MIN=0.0, MAX=1.0),
    LFloat("g", MIN=0.0, MAX=1.0),
    LFloat("b", MIN=0.0, MAX=1.0)
    )
rgb_byte = QStruct('rgb_uint8',
    UInt8("r", MIN=0, MAX=255),
    UInt8("g", MIN=0, MAX=255),
    UInt8("b", MIN=0, MAX=255)
    )
argb_byte = QStruct('argb_uint8',
    UInt8("a", MIN=0, MAX=255),
    UInt8("r", MIN=0, MAX=255),
    UInt8("g", MIN=0, MAX=255),
    UInt8("b", MIN=0, MAX=255)
    )

# rotations
ijkw_float = QStruct('ijkw_float',
    LFloat("i"),
    LFloat("j"),
    LFloat("k"),
    LFloat("w")
    )
ijk_float = QStruct('ijk_float',
    LFloat("i"),
    LFloat("j"),
    LFloat("k")
    )
yp_float = QStruct('yp_float',
    LFloat("y"),
    LFloat("p")
    )

# maps tag class four character codes(fccs) in
# their string encoding to their int encoding.
tag_class_fcc_to_be_int = {}
tag_class_fcc_to_le_int = {}
# maps tag class four character codes(fccs) in
# their int encoding to their string encoding.
tag_class_be_int_to_fcc = {}
tag_class_le_int_to_fcc = {}

# maps tag class four character codes to the tags file extension
tag_class_fcc_to_ext = {
    'actr': "actor",
    'actv': "actor_varient",
    'ant!': "antenna",
    'bipd': "biped",
    'bitm': "bitmap",
    'trak': "camera_track",
    'colo': "color_table",
    'cdmg': "continuous_damage_effect",
    'cont': "contrail",
    'jpt!': "damage_effect",
    'deca': "decal",
    'udlg': "dialogue",
    'dobc': "detail_object_collection",
    'devi': "device",
    'ctrl': "device_control",
    'lifi': "device_light_fixture",
    'mach': "device_machine",
    'effe': "effect",
    'eqip': "equipment",
    'flag': "flag",
    'fog ': "fog",
    'font': "font",
    'garb': "garbage",
    'mod2': "gbxmodel",
    'matg': "globals",
    'glw!': "glow",
    'grhi': "grenade_hud_interface",
    'hudg': "hud_globals",
    'hmt ': "hud_message_text",
    'hud#': "hud_number",
    'devc': "input_device_defaults",
    'item': "item",
    'itmc': "item_collection",
    'lens': "lens_flare",
    'ligh': "light",
    'mgs2': "light_volume",
    'elec': "lightning",
    'foot': "material_effects",
    'metr': "meter",
    'mode': "model",
    'antr': "model_animations",
    'coll': "model_collision_geometry",
    'mply': "multiplayer_scenario_description",
    'obje': "object",
    'part': "particle",
    'pctl': "particle_system",
    'phys': "physics",
    'plac': "placeholder",
    'pphy': "point_physics",
    'ngpr': "preferences_network_game",
    'proj': "projectile",
    'scnr': "scenario",
    'sbsp': "scenario_structure_bsp",
    'scen': "scenery",
    'snd!': "sound",
    'snde': "sound_environment",
    'lsnd': "sound_looping",
    'ssce': "sound_scenery",
    'boom': "spheroid",
    'shdr': "shader",
    'schi': "shader_transparent_chicago",
    'scex': "shader_transparent_chicago_extended",
    'sotr': "shader_transparent_generic",
    'senv': "shader_environment",
    'sgla': "shader_transparent_glass",
    'smet': "shader_transparent_meter",
    'soso': "shader_model",
    'spla': "shader_transparent_plasma",
    'swat': "shader_transparent_water",
    'sky ': "sky",
    'str#': "string_list",
    'tagc': "tag_collection",
    'Soul': "ui_widget_collection",
    'DeLa': "ui_widget_definition",
    'ustr': "unicode_string_list",
    'unit': "unit",
    'unhi': "unit_hud_interface",
    'vehi': "vehicle",
    'vcky': "virtual_keyboard",
    'weap': "weapon",
    'wphi': "weapon_hud_interface",
    'rain': "weather_particle_system",
    'wind': "wind",
    }

for tag_cls in tag_class_fcc_to_ext:
    tag_class_fcc_to_be_int[tag_cls] = fcc(tag_cls, 'big')
    tag_class_be_int_to_fcc[fcc(tag_cls, 'big')] = tag_cls
    tag_class_fcc_to_le_int[tag_cls] = fcc(tag_cls)
    tag_class_le_int_to_fcc[fcc(tag_cls)] = tag_cls

def tag_class(*args):
    '''
    A macro for creating a tag_class enum desc with the
    enumerations set to the provided tag_class fcc's.
    '''
    classes = []
    for four_cc in sorted(args):
        classes.append((tag_class_fcc_to_ext[four_cc], four_cc))

    return BUEnum32('tag_class',
                    *(tuple(classes) + (("none", 0xffffffff),) ),
                    DEFAULT=0xffffffff)

valid_tags = tag_class(*tag_class_fcc_to_ext.keys())

def reflexive(name, substruct, max_count=MAX_REFLEXIVE_COUNT, *names, **desc):
    '''This function serves to macro the creation of a reflexive'''
    desc.update(
        INCLUDE=reflexive_struct,
        STEPTREE=Array(name + " array",
            SIZE=".size", MAX=max_count, SUB_STRUCT=substruct,
            ),
        SIZE=12
        )
    if names:
        name_map = {}
        for i in range(len(names)):
            e_name = BlockDef.str_to_name(None, names[i])
            name_map[e_name] = i
            
        desc[STEPTREE][NAME_MAP] = name_map
        
    return Reflexive(name, **desc)


def rawdata_ref(name, f_type=Rawdata):
    '''This function serves to macro the creation of a rawdata reference'''
    return RawdataRef(name,
        EDITABLE=False, INCLUDE=rawdata_ref_struct,
        STEPTREE=f_type("data", VISIBLE=False, SIZE=".size") )


def dependency(name='tag ref', valid_ids=valid_tags):
    '''This function serves to macro the creation of a tag dependency'''
    return TagIndexRef(name,
        valid_ids,
        BSInt32("path pointer"),
        BSInt32("path length"),
        BUInt32("id", DEFAULT=0xFFFFFFFF),

        STEPTREE=StringVarLen("filepath", SIZE=tag_ref_size),
        EDITABLE=False,
        )

def blam_header(tagid, version=1):
    '''This function serves to macro the creation of a tag header'''
    header_desc= dict(tag_header)
    header_desc[1] = dict(header_desc[1])
    header_desc[5] = dict(header_desc[5])
    header_desc[1][DEFAULT] = tagid
    header_desc[5][DEFAULT] = version
    return header_desc


def ascii_str32(name):
    return StrAscii(str(name), SIZE=32)

valid_strings = tag_class('ustr', 'str#')
valid_effects = tag_class('snd!', 'effe')
valid_continuous_damages = tag_class('cdmg')
valid_fogs = tag_class('fog ')
valid_fonts = tag_class('font')
valid_particles = tag_class('part')
valid_lens_flares = tag_class('lens')
valid_point_physics = tag_class('pphy')
valid_bitmaps = tag_class('bitm')
valid_decals = tag_class('deca')
valid_sounds  = tag_class('snd!')
valid_physics = tag_class('phys')
valid_model_animations = tag_class('antr')
valid_unicode_strings = tag_class('ustr')
valid_model_collision_geometries = tag_class('coll')
valid_models = tag_class('mode', 'mod2')
valid_attachments = tag_class('cont', 'effe', 'ligh', 'mgs2', 'pctl', 'lsnd')
valid_widgets = tag_class('ant!', 'flag', 'glw!', 'mgs2', 'elec')
valid_effect_events = tag_class(
    'bipd', 'jpt!', 'deca', 'devi', 'ctrl', 'lifi', 'mach',
    'eqip', 'garb', 'item', 'ligh', 'obje', 'pctl', 'plac',
    'proj', 'scen', 'snd!', 'ssce', 'unit', 'vehi', 'weap'
    )
valid_shaders = tag_class(
    'shdr', 'schi', 'scex', 'sotr', 'senv',
    'sgla', 'smet', 'soso', 'spla', 'swat'
    )
valid_items = tag_class('eqip', 'garb', 'item', 'weap')
valid_objects = tag_class(
    'obje', 'bipd', 'vehi', 'weap', 'eqip', 'garb', 'proj',
    'scen', 'mach', 'ctrl', 'lifi', 'plac', 'ssce'
    )
valid_units = tag_class('bipd', 'unit', 'vehi')


#The header present at the start of every tag
tag_header = Struct("blam header",
    Pad(36),
    valid_tags,
    LUInt32("base address", DEFAULT=0),  #random
    LUInt32("header size",  DEFAULT=64),
    Pad(8),
    LUInt16("version", DEFAULT=1),
    LUInt16("unknown", DEFAULT=255),
    LUEnum32("engine id",
        ("halo 1", 'blam'),
        ("halo 2", 'BLM!'),
        DEFAULT='blam'),
    EDITABLE=False, SIZE=64
    )

#Shared Enumerator options
materials_list = (
    # the order of these elements is important(DONT SHUFFLE IT)
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


#Transparent Shader Shared Functions
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

#Shared Functions
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
shader_fade_mode = (
    "none",
    "fade when perpendicular",
    "fade when parallel",
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
function_names = (
    "none",
    "A",
    "B",
    "C",
    "D",
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

#Miscellaneous descs
anim_func_per_pha = Struct('',
    BSEnum16("function", *animation_functions),
    Pad(2),
    BFloat("period"),#seconds
    BFloat("phase"),#seconds
    )
anim_func_per_sca = Struct('',
    BSEnum16("function", *animation_functions),
    Pad(2),
    BFloat("period"),#seconds
    BFloat("scale"),#base map repeats
    )
anim_src_func_per_pha_sca = Struct('',
    BSEnum16("source", *function_outputs),
    BSEnum16("function", *animation_functions),
    BFloat("period"),#seconds
    BFloat("phase"),#seconds
    BFloat("scale"),#repeats
    # when scale is for rotation, its actually in degrees, not radians. weird!
    )

from_to = QStruct('',
    BFloat("from", GUI_NAME=" "),
    BFloat("to"),
    )


#This is the structure for all points where a tag references a rawdata chunk
rawdata_ref_struct = RawdataRef('rawdata ref', 
    BSInt32("size"),
    BSInt32("unknown 1"),#0x00000000 in tags(and meta it seems)
    BSInt32("unknown 2"),#random(low number in meta)
    BSInt32("pointer"),
    BUInt32("id"),#0x00000000 in meta it seems
    EDITABLE=False,
    )


#This is the structure for all tag reflexives
reflexive_struct = Reflexive('reflexive',
    BSInt32("size"),
    BSInt32("pointer"),#random
    BUInt32("id"),#0x00000000 in meta it seems
    EDITABLE=False,
    )

#This is the structure for all points where a tag references another tag
tag_index_ref_struct = dependency()

"""Objects"""

FlSEnum16("object type",
    ("bipd", 0),
    ("vehi", 1),
    ("weap", 2),
    ("eqip", 3),
    ("garb", 4),
    ("proj", 5),
    ("scen", 6),
    ("mach", 7),
    ("ctrl", 8),
    ("lifi", 9),
    ("plac", 10),
    ("ssce", 11),
    DEFAULT=0, EDITABLE=False,
    ),


"""Shader radiosity"""
radiosity_settings = Struct("radiosity settings",
    BBool16("radiosity flags",
        "simple parameterization",
        "ignore normals",
        "transparent lit",
        ),
    BSEnum16("radiosity detail level" ,
        "high",
        "medium",
        "low",
        "turd",
        ),
    BFloat("radiosity light power"),
    QStruct("radiosity light color", INCLUDE=rgb_float),
    QStruct("radiosity tint color",  INCLUDE=rgb_float),
    )

"""Shader physics"""
shader_physics = Struct('physics',
    Pad(2),
    BSEnum16("material type", *materials_list),

    # THIS FIELD IS OFTEN INCORRECT ON STOCK TAGS.
    # This seems to be a Guerilla-only optimization value
    FlSEnum16("shader type",
        ("shdr", -1),  # Shader
        ("senv", 3),   # Environment
        ("soso", 4),   # Model
        ("sotr", 5),   # Transparent Generic
        ("schi", 6),   # Transparent Chicago
        ("scex", 7),   # Transparent Chicago Extended
        ("swat", 8),   # Water
        ("sgla", 9),   # Glass
        ("smet", 10),  # Meter
        ("spla", 11),  # Plasma
        DEFAULT=-1, EDITABLE=False,
        ),
    Pad(2)
    )

"""Transparent Shader"""
extra_layers_block = dependency("extra layer", valid_shaders)

chicago_4_stage_maps = Struct("four stage map",
    BBool16("flags" ,
        "unfiltered",
        "alpha replicate",
        "u-clamped",
        "v-clamped",
        ),
    Pad(42),
    BSEnum16("color function", *blend_functions),
    BSEnum16("alpha function", *blend_functions),
    Pad(36),
    #shader transformations
    BFloat("map u-scale"),
    BFloat("map v-scale"),
    BFloat("map u-offset"),
    BFloat("map v-offset"),
    BFloat("map rotation"),#degrees
    BFloat("map bias"),#[0,1]
    dependency("bitmap", valid_bitmaps),

    Pad(40),

    #shader animations
    Struct("u-animation", INCLUDE=anim_src_func_per_pha_sca),
    Struct("v-animation", INCLUDE=anim_src_func_per_pha_sca),
    Struct("rotation-animation", INCLUDE=anim_src_func_per_pha_sca),

    QStruct("rotation center", INCLUDE=xy_float),
    SIZE=220,
    )


chicago_2_stage_maps = Struct("two stage map", INCLUDE=chicago_4_stage_maps)

chicago_extra_flags = (
    "dont fade active camouflage",
    "numeric countdown timer"
    )

"""Misc"""
damage_modifiers = QStruct("damage modifiers",
    *(BFloat(material_name) for material_name in materials_list)
    )
