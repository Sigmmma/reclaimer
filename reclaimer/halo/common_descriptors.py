from copy import copy

from supyr_struct.defs.common_descriptors import *
from supyr_struct.defs.block_def import BlockDef
from .fields import *
from .constants import *

com = combine

def tag_class(name, *args):
    return BUEnum32(name, *(tuple(args) + (("none", 0xffffffff),) ),
                    DEFAULT=0xffffffff)

valid_tags = tag_class("Tag_Class",
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


valid_attachments = tag_class("Tag_Class",
    ("contrail",        'cont'),
    ("effect",          'effe'),
    ("light",           'ligh'),
    ("light_volume",    'mgs2'),
    ("particle_system", 'pctl'),
    ("sound_looping",   'lsnd'),
    )

valid_effect_events = tag_class("Tag_Class",
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

valid_strings = tag_class("Tag_Class",
    ("unicode_string_list", 'ustr'),
    ("string_list",         'str#'),
    )

valid_effects = tag_class("Tag_Class",
    ("sound",  'snd!'),
    ("effect", 'effe'),
    )

valid_point_physics = tag_class("Tag_Class", ("point_physics", 'pphy') )
valid_bitmaps = tag_class("Tag_Class", ("bitmap", 'bitm') )
valid_sounds  = tag_class("Tag_Class", ("sound", 'snd!') )
valid_physics = tag_class("Tag_Class", ("physics", 'phys') )
valid_model_animations = tag_class("Tag_Class",
    ("model_animations", 'antr')
    )
valid_model_collision_geometry = tag_class("Tag_Class",
    ("model_collision_geometry", 'coll')
    )

valid_items = tag_class("Tag_Class",
    ("equipment", 'eqip'),
    ("garbage",   'gar'),
    ("item",      'item'),
    ("weapon",    'weap'),
    )

valid_objects = tag_class("Tag_Class",
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


valid_shaders = tag_class("Tag_Class",
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

valid_units = tag_class("Tag_Class",
    ("biped",   'bipd'),
    ("unit",    'unit'),
    ("vehicle", 'vehi'),
    )

valid_widgets = tag_class("Tag_Class",
    ("antenna",      'ant!'),
    ("flag",         'flag'),
    ("glow",         'glw!'),
    ("light_volume", 'mgs2'),
    ("lightning",    'elec'),
    )


#The header present at the start of every tag
Tag_Header = Struct("Blam Header",
    Pad(36),
    valid_tags,
    LUInt32("Base Address", DEFAULT=0),#random
    LUInt32("Header Size",  DEFAULT=64),
    Pad(8),
    LUInt16("Version", DEFAULT=1),
    LUInt16("Unknown", DEFAULT=255),
    LUEnum32("Engine ID",
        ("halo 1", 'blam'),
        ("halo 2", 'BLM!'),
        DEFAULT='blam'),
    EDITABLE=False, SIZE=64
    )

#Shared Enumerator options
Materials_List = (
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

Transparent_Shader_Properties = (
    "alpha tested",
    "decal",
    "two sided",
    "first map is in screenspace",
    "draw before water",
    "ignore effect",
    "scale first map with distance",
    "numeric",
    )
Transparent_Shader_Fade_Mode = (
    "none",
    "fade when perpendicular",
    "fade when parallel",
    )
Transparent_Shader_First_Map_Type = (
    "map 2d",
    "reflection cube map",
    "object centered cube map",
    "viewer centered cube map",
    )

Detail_Mask = (
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

Animation_Functions = (
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
Detail_Map_Functions = (
    "double/biased multiply",
    "multiply",
    "double/biased add",
    )
Device_Functions = (
    "none",
    "power",
    "change in power",
    "position",
    "change in position",
    "locked",
    "delay",
    )
Blend_Functions = (
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
Framebuffer_Blend_Modes = (
    "alpha blend",
    "multiply",
    "double multiply",
    "add",
    "subtract",
    "component min",
    "component max",
    "alpha-multiply add",
    )
Function_Names = (
    "none",
    "A",
    "B",
    "C",
    "D",
    )
Function_Inputs = (
    "none",
    "A in",
    "B in",
    "C in",
    "D in",
    )
Function_Outputs = (
    "none",
    "A out",
    "B out",
    "C out",
    "D out",
    )

All_Shader_Enums = (
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
Anim_Func_Per_Pha = Struct('',
    BSEnum16("function", *Animation_Functions),
    Pad(2),
    BFloat("period"),#seconds
    BFloat("phase"),#seconds
    )
Anim_Func_Per_Sca = Struct('',
    BSEnum16("function", *Animation_Functions),
    Pad(2),
    BFloat("period"),#seconds
    BFloat("scale"),#base map repeats
    )
Anim_Src_Func_Per_Pha_Sca = Struct('',
    BSEnum16("source", *Function_Outputs),
    BSEnum16("function", *Animation_Functions),
    BFloat("period"),#seconds
    BFloat("phase"),#seconds
    BFloat("scale"),#repeats
    )

From_To = Struct('',
    BFloat("from", GUI_NAME=" "),
    BFloat("to"),
    )



def reflexive(name, substruct, max_count=MAX_REFLEXIVE_COUNT, *names, **desc):
    '''This function serves to macro the creation of a reflexive'''
    desc.update(
        INCLUDE=Reflexive_Struct,
        CHILD=Array(name+" array",
            SIZE=".Count", MAX=max_count,
            SUB_STRUCT=substruct
            ),
        SIZE=12
        )
    if names:
        name_map = {}
        for i in range(len(names)):
            e_name = BlockDef.str_to_name(None, names[i])
            name_map[e_name] = i
            
        desc[CHILD][NAME_MAP] = name_map
        
    return Reflexive(name, **desc)

def rawdata_ref(name, field=BytearrayRaw):
    '''This function serves to macro the creation of a rawdata reference'''
    return RawDataRef(name,
        EDITABLE=False, INCLUDE=Raw_Data_Ref_Struct,
        CHILD=field("data", VISIBLE=False, SIZE=".Count") )

def dependency(name='tag ref', valid_ids=valid_tags):
    '''This function serves to macro the creation of a tag dependency'''
    return TagIndexRef(name,
        valid_ids,
        BSInt32("Tag Path Pointer"),#random
        BSInt32("Tag Path Length"),
        BUInt32("Tag ID", DEFAULT=0xFFFFFFFF),#random
                                       
        CHILD=StringVarLen("Filepath", SIZE=tag_ref_size),
        EDITABLE=False,
        )

def blam_header(tagid, version=1):
    '''This function serves to macro the creation of a tag header'''
    return com( {1:{DEFAULT:tagid },
                 5:{DEFAULT:version}}, Tag_Header)


#This is the structure for all points where a tag references a chunk of raw data
Raw_Data_Ref_Struct = RawDataRef('Raw Data Ref', 
    BSInt32("Count"),
    BSInt32("Unknown 1"),#0x00000000 in tags
    BSInt32("Unknown 2"),#random
    BSInt32("Unknown 3"),#random
    BUInt32("ID"),#random
    EDITABLE=False,
    )

#This is the structure for all tag reflexives
Reflexive_Struct = Reflexive('Reflexive',
    BSInt32("Count"),
    BSInt32("ID"),#random
    BUInt32("Reflexive ID"),#random
    EDITABLE=False,
    )

#This is the structure for all points where a tag references another tag
Tag_Index_Ref_Struct = dependency()

"""Shader Stuff"""

Material_Type = BSEnum16("material type", *Materials_List, OFFSET=34)

#THIS FIELD IS OFTEN INCORRECT ON STOCK TAGS
#This means it likely doesn't matter, but lets not take that chance
Numeric_Shader_ID = FlSEnum16("numeric shader id",
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

Radiosity_Block = Struct("radiosity settings",
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
    Struct("radiosity light color", INCLUDE=R_G_B_Float),
    Struct("radiosity tint color",  INCLUDE=R_G_B_Float),
    )


#Transparent Shader Stuff

Extra_Layers_Block = dependency("extra layer", valid_shaders)

Chicago_4_Stage_Maps = Struct("four stage map",
    BBool16("flags" ,
        "unfiltered",
        "alpha replicate",
        "u-clamped",
        "v-clamped",
        ),
    Pad(42),
    BSEnum16("color function", *Blend_Functions),
    BSEnum16("alpha function", *Blend_Functions),
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
    Struct("u-animation", INCLUDE=Anim_Src_Func_Per_Pha_Sca),
    Struct("v-animation", INCLUDE=Anim_Src_Func_Per_Pha_Sca),
    Struct("rotation-animation", INCLUDE=Anim_Src_Func_Per_Pha_Sca),

    Struct("rotation center", INCLUDE=X_Y_Float),
    SIZE=220,
    )


Chicago_2_Stage_Maps = Struct("two stage map", INCLUDE=Chicago_4_Stage_Maps)

Chicago_Extra_Flags = (
    "dont fade active camouflage",
    "numeric countdown timer"
    )
