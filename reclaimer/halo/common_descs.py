from copy import copy, deepcopy

from supyr_struct.defs.common_descs import *
from supyr_struct.defs.block_def import BlockDef
from .field_types import *
from .constants import *

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

valid_actors = tag_class('actr')
valid_actor_variants = tag_class('actv')
valid_bitmaps = tag_class('bitm')
valid_camera_tracks = tag_class('trak')
valid_continuous_damages = tag_class('cdmg')
valid_damage_effects = tag_class('jpt!')
valid_decals = tag_class('deca')
valid_effects = tag_class('effe')
valid_event_effects = tag_class('effe', 'snd!')
valid_equipment = tag_class('eqip')
valid_fogs = tag_class('fog ')
valid_fonts = tag_class('font')
valid_lens_flares = tag_class('lens')
valid_material_effects = tag_class('foot')
valid_models = tag_class('mode', 'mod2')
valid_model_animations = tag_class('antr')
valid_model_collision_models = tag_class('coll')
valid_particles = tag_class('part')
valid_physics = tag_class('phys')
valid_point_physics = tag_class('pphy')
valid_projectiles = tag_class('proj')
valid_sounds  = tag_class('snd!')
valid_strings = tag_class('ustr', 'str#')
valid_unicode_strings = tag_class('ustr')
valid_unit_hud_interfaces = tag_class('unhi')
valid_unit_dialogues = tag_class('udlg')
valid_weapons  = tag_class('weap')
valid_weapon_hud_interfaces = tag_class('wphi')
valid_widgets = tag_class('ant!', 'flag', 'glw!', 'mgs2', 'elec')

valid_attachments = tag_class('cont', 'effe', 'ligh', 'mgs2', 'pctl', 'lsnd')
valid_effect_events = tag_class(
    'bipd', 'jpt!', 'deca', 'devi', 'ctrl', 'lifi', 'mach',
    'eqip', 'garb', 'item', 'ligh', 'obje', 'pctl', 'plac',
    'proj', 'scen', 'snd!', 'ssce', 'unit', 'vehi', 'weap'
    )
valid_items = tag_class('eqip', 'garb', 'item', 'weap')
valid_objects = tag_class(
    'obje', 'bipd', 'vehi', 'weap', 'eqip', 'garb', 'proj',
    'scen', 'mach', 'ctrl', 'lifi', 'plac', 'ssce'
    )
valid_shaders = tag_class(
    'shdr', 'schi', 'scex', 'sotr', 'senv',
    'sgla', 'smet', 'soso', 'spla', 'swat'
    )
valid_units = tag_class('bipd', 'unit', 'vehi')


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
    "covenant",
    "human",
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
    "veolcity air",
    "veolcity water",
    "veolcity ground",
    "veolcity forward",
    "veolcity left",
    "veolcity up",
    "left tread position",
    "right tread position",
    "left tread veolcity",
    "right tread veolcity",
    "front left tire position",
    "front right tire position",
    "back left tire position",
    "back right tire position",
    "front left tire veolcity",
    "front right tire veolcity",
    "back left tire veolcity",
    "back right tire veolcity",
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

# Miscellaneous, Halo specific descriptors
anim_func_per_pha = Struct('',
    BSEnum16("function", *animation_functions),
    Pad(2),
    BFloat("period"),  # seconds
    BFloat("phase"),  # seconds
    )
anim_func_per_sca = Struct('',
    BSEnum16("function", *animation_functions),
    Pad(2),
    BFloat("period"),  # seconds
    BFloat("scale"),  # base map repeats
    )
anim_src_func_per_pha_sca = Struct('',
    BSEnum16("source", *function_outputs),
    BSEnum16("function", *animation_functions),
    BFloat("period"),  # seconds
    BFloat("phase"),  # seconds
    BFloat("scale"),  # repeats
    # when scale is for rotation, its actually in degrees, not radians. weird!
    )
from_to = QStruct('',
    BFloat("from", GUI_NAME=" "),
    BFloat("to"),
    )


# This is the descriptor used wherever a tag references a rawdata chunk
rawdata_ref_struct = RawdataRef('rawdata ref', 
    BSInt32("size"),
    BSInt32("unknown 1"),  # 0x00000000 in tags(and meta it seems)
    BSInt32("unknown 2"),  # random(low number in meta)
    BSInt32("pointer"),
    BUInt32("id"),  # 0x00000000 in meta it seems
    EDITABLE=False,
    )

# This is the descriptor used wherever a tag reference a reflexive
reflexive_struct = Reflexive('reflexive',
    BSInt32("size"),
    BSInt32("pointer"),  # random
    BUInt32("id"),  # 0x00000000 in meta it seems
    EDITABLE=False,
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
    *(BFloat(material_name) for material_name in materials_list)
    )

# Miscellaneous shared descriptors
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
