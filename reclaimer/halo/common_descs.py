from copy import copy, deepcopy

from supyr_struct.defs.common_descs import *
from supyr_struct.defs.block_def import BlockDef
from .fields import *
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
    LFloat("a"),
    LFloat("r"),
    LFloat("g"),
    LFloat("b")
    )
rgb_float = QStruct('rgb_float',
    LFloat("r"),
    LFloat("g"),
    LFloat("b")
    )
rgb_byte = QStruct('rgb_uint8',
    UInt8("r"),
    UInt8("g"),
    UInt8("b")
    )
argb_byte = QStruct('argb_uint8',
    UInt8("a"),
    UInt8("r"),
    UInt8("g"),
    UInt8("b")
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


def tag_class(name, *args):
    return BUEnum32(name, *(tuple(args) + (("none", 0xffffffff),) ),
                    DEFAULT=0xffffffff)

valid_tags = tag_class("tag_class",
    ("actor",          'actr'),
    ("actor_varient",  'actv'),
    ("antenna",        'ant!'),
    ("biped",          'bipd'),
    ("bitmap",         'bitm'),
    ("camera_track",   'trak'),
    ("color_table",    'colo'),
    ("continuous_damage_effect", 'cdmg'),
    ("contrail",       'cont'),
    ("damage_effect",  'jpt!'),
    ("decal",          'deca'),
    ("dialogue",       'udlg'),
    ("detail_object_collection", 'dobc'),
    ("device",         'devi'),
    ("device_control", 'ctrl'),
    ("device_light_fixture", 'lifi'),
    ("device_machine", 'mach'),
    ("effect",         'effe'),
    ("equipment",      'eqip'),
    ("flag",           'flag'),
    ("fog",            'fog '),
    ("font",           'font'),
    ("garbage",        'gar'),
    ("gbxmodel",       'mod2'),
    ("globals",        'matg'),
    ("glow",           'glw!'),
    ("grenade_hud_interface", 'grhi'),
    ("hud_globals",      'hudg'),
    ("hud_message_text", 'hmt '),
    ("hud_number",       'hud#'),
    ("input_device_defaults", 'devc'),
    ("item",             'item'),
    ("item_collection",  'itmc'),
    ("lens_flare",       'lens'),
    ("light",            'ligh'),
    ("light_volume",     'mgs2'),
    ("lightning",        'elec'),
    ("material_effects", 'foot'),
    ("meter",            'metr'),
    ("model",            'mode'),
    ("model_animations", 'antr'),
    ("model_collision_geometry",         'coll'),
    ("multiplayer_scenario_description", 'mply'),
    ("object",           'obje'),
    ("particle",         'part'),
    ("particle_system",  'pctl'),
    ("physics",          'phys'),
    ("placeholder",      'plac'),
    ("point_physics",    'pphy'),
    ("preferences_network_game", 'ngpr'),
    ("projectile",       'proj'),
    ("scenario",         'scnr'),
    ("scenario_structure_bsp", 'sbsp'),
    ("scenery",           'scen'),
    ("sound",             'snd!'),
    ("sound_environment", 'snde'),
    ("sound_looping",     'lsnd'),
    ("sound_scenery",     'ssce'),
    ("spheroid",          'boom'),
    ("shader",            'shdr'),
    ("shader_transparent_chicago", 'schi'),
    ("shader_transparent_chicago_extended", 'scex'),
    ("shader_transparent_generic", 'sotr'),
    ("shader_environment",         'senv'),
    ("shader_transparent_glass",   'sgla'),
    ("shader_transparent_meter",   'smet'),
    ("shader_model",               'soso'),
    ("shader_transparent_plasma",  'spla'),
    ("shader_transparent_water",   'swat'),
    ("sky",                  'sky '),
    ("string_list",          'str#'),
    ("tag_collection",       'tagc'),
    ("ui_widget_collection", 'Soul'),
    ("ui_widget_definition", 'DeLa'),
    ("unicode_string_list",  'ustr'),
    ("unit",                 'unit'),
    ("unit_hud_interface",   'unhi'),
    ("vehicle",              'vehi'),
    ("virtual_keyboard",     'vcky'),
    ("weapon",               'weap'),
    ("weapon_hud_interface", 'wphi'),
    ("weather_particle_system", 'rain'),
    ("wind",                 'wind'),
    )


valid_attachments = tag_class("tag_class",
    ("contrail",        'cont'),
    ("effect",          'effe'),
    ("light",           'ligh'),
    ("light_volume",    'mgs2'),
    ("particle_system", 'pctl'),
    ("sound_looping",   'lsnd'),
    )

valid_effect_events = tag_class("tag_class",
    ("biped",           'bipd'),
    ("damage_effect",   'jpt!'),
    ("decal",           'deca'),
    ("device",          'devi'),
    ("device_control",  'ctrl'),
    ("device_light_fixture", 'lifi'),
    ("device_machine",  'mach'),
    ("equipment",       'eqip'),
    ("garbage",         'gar'),
    ("item",            'item'),
    ("light",           'ligh'),
    ("object",          'obje'),
    ("particle_system", 'pctl'),
    ("placeholder",     'plac'),
    ("projectile",      'proj'),
    ("scenery",         'scen'),
    ("sound",           'snd!'),
    ("sound_scenery",   'ssce'),
    ("unit",            'unit'),
    ("vehicle",         'vehi'),
    ("weapon",          'weap'),
    )

valid_strings = tag_class("tag_class",
    ("unicode_string_list", 'ustr'),
    ("string_list",         'str#'),
    )

valid_effects = tag_class("tag_class",
    ("sound",  'snd!'),
    ("effect", 'effe'),
    )

valid_fogs = tag_class("tag_class", ("fog", 'fog '))
valid_fonts = tag_class("tag_class", ("font", 'font'))
valid_particles = tag_class("tag_class", ("particle", 'part'))
valid_lens_flares = tag_class("tag_class", ("lens_flare", 'lens'))
valid_point_physics = tag_class("tag_class", ("point_physics", 'pphy'))
valid_bitmaps = tag_class("tag_class", ("bitmap", 'bitm'))
valid_sounds  = tag_class("tag_class", ("sound", 'snd!'))
valid_physics = tag_class("tag_class", ("physics", 'phys'))
valid_model_animations = tag_class("tag_class", ("model_animations", 'antr'))
valid_unicode_strings = tag_class("tag_class", ("unicode_string_list", 'ustr'))

valid_model_collision_geometries = tag_class("tag_class",
    ("model_collision_geometry", 'coll')
    )
valid_models = tag_class("tag_class",
    ("model", 'mode'),
    ("gbxmodel", 'mod2')
    )

valid_items = tag_class("tag_class",
    ("equipment", 'eqip'),
    ("garbage",   'gar'),
    ("item",      'item'),
    ("weapon",    'weap'),
    )

valid_objects = tag_class("tag_class",
    ("biped",          'bipd'),
    ("device",         'devi'),
    ("device_control", 'ctrl'),
    ("device_light_fixture", 'lifi'),
    ("device_machine", 'mach'),
    ("equipment",      'eqip'),
    ("object",         'obje'),
    ("projectile",     'proj'),
    ("scenery",        'scen'),
    ("sound_scenery",  'ssce'),
    ("vehicle",        'vehi'),
    ("weapon",         'weap'),
    )


valid_shaders = tag_class("tag_class",
    ("shader",                     'shdr'),
    ("shader_transparent_chicago", 'schi'),
    ("shader_transparent_chicago_extended", 'scex'),
    ("shader_transparent_generic", 'sotr'),
    ("shader_environment",         'senv'),
    ("shader_transparent_glass",   'sgla'),
    ("shader_transparent_meter",   'smet'),
    ("shader_model",               'soso'),
    ("shader_transparent_plasma",  'spla'),
    ("shader_transparent_water",   'swat'),
    )

valid_units = tag_class("tag_class",
    ("biped",   'bipd'),
    ("unit",    'unit'),
    ("vehicle", 'vehi'),
    )

valid_widgets = tag_class("tag_class",
    ("antenna",      'ant!'),
    ("flag",         'flag'),
    ("glow",         'glw!'),
    ("light_volume", 'mgs2'),
    ("lightning",    'elec'),
    )


#The header present at the start of every tag
tag_header = Struct("blam header",
    Pad(36),
    valid_tags,
    LUInt32("base address", DEFAULT=0),#random
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
trans_shdr_fade_mode = (
    "none",
    "fade when perpendicular",
    "fade when parallel",
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

all_shader_enums = (
    ("shader",                     'shdr'),
    ("shader_transparent_chicago", 'schi'),
    ("shader_transparent_chicago_extended", 'scex'),
    ("shader_transparent_generic", 'sotr'),
    ("shader_environment",         'senv'),
    ("shader_transparent_glass",   'sgla'),
    ("shader_transparent_meter",   'smet'),
    ("shader_model",               'soso'),
    ("shader_transparent_plasma",  'spla'),
    ("shader_transparent_water",   'swat'),
    )


#Miscellaneous blocks
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


def reflexive(name, substruct, max_count=MAX_REFLEXIVE_COUNT, *names, **desc):
    '''This function serves to macro the creation of a reflexive'''
    desc.update(
        INCLUDE=reflexive_struct,
        SUBTREE=Array(name+" array",
            SIZE=".size", MAX=max_count, SUB_STRUCT=substruct,
            ),
        SIZE=12
        )
    if names:
        name_map = {}
        for i in range(len(names)):
            e_name = BlockDef.str_to_name(None, names[i])
            name_map[e_name] = i
            
        desc[SUBTREE][NAME_MAP] = name_map
        
    return Reflexive(name, **desc)


def rawdata_ref(name, field=Rawdata):
    '''This function serves to macro the creation of a rawdata reference'''
    return RawdataRef(name,
        EDITABLE=False, INCLUDE=rawdata_ref_struct,
        SUBTREE=field("data", VISIBLE=False, SIZE=".size") )


def dependency(name='tag ref', valid_ids=valid_tags):
    '''This function serves to macro the creation of a tag dependency'''
    return TagIndexRef(name,
        valid_ids,
        BSInt32("path pointer"),
        BSInt32("path length"),
        BUInt32("id", DEFAULT=0xFFFFFFFF),

        SUBTREE=StringVarLen("filepath", SIZE=tag_ref_size),
        EDITABLE=False,
        )

def blam_header(tagid, version=1):
    '''This function serves to macro the creation of a tag header'''
    header_dict = dict(tag_header)
    header_dict[1] = dict(header_dict[1])
    header_dict[5] = dict(header_dict[5])
    header_dict[1][DEFAULT] = tagid
    header_dict[5][DEFAULT] = version
    return header_dict


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

"""Shader Stuff"""

material_type = BSEnum16("material type", *materials_list, OFFSET=34)

#THIS FIELD IS OFTEN INCORRECT ON STOCK TAGS
#This means it likely doesn't matter, but lets not take that chance
shader_id_num = FlSEnum16("numeric shader id",
    ("shdr", -1),#Shader
    ("senv", 3),#Environment
    ("soso", 4),#Model
    ("sotr", 5),#Transparent Generic
    ("schi", 6),#Transparent Chicago
    ("scex", 7),#Transparent Chicago Extended
    ("swat", 8),#Water
    ("sgla", 9),#Glass
    ("smet", 10),#Meter
    ("spla", 11),#Plasma
    OFFSET=36, EDITABLE=False,
    )


"""Radiosity Stuff"""

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

damage_modifiers = QStruct("damage modifiers",
    BFloat("dirt"),
    BFloat("sand"),
    BFloat("stone"),
    BFloat("snow"),
    BFloat("wood"),
    BFloat("metal hollow"),
    BFloat("metal thin"),
    BFloat("metal thick"),
    BFloat("rubber"),
    BFloat("glass"),
    BFloat("force field"),
    BFloat("grunt"),
    BFloat("hunter armor"),
    BFloat("hunter skin"),
    BFloat("elite"),
    BFloat("jackal"),
    BFloat("jackal energy shield"),
    BFloat("engineer skin"),
    BFloat("engineer force field"),
    BFloat("flood combat form"),
    BFloat("flood carrier form"),
    BFloat("cyborg armor"),
    BFloat("cyborg energy shield"),
    BFloat("human armor"),
    BFloat("human skin"),
    BFloat("sentinel"),
    BFloat("moniter"),
    BFloat("plastic"),
    BFloat("water"),
    BFloat("leaves"),
    BFloat("elite energy shield"),
    BFloat("ice"),
    BFloat("hunter shield"),
    Pad(28),
    )

#Transparent Shader Stuff

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
