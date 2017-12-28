from copy import copy, deepcopy
from math import pi
try:
    from mozzarilla.field_widgets import *
except Exception:
    ReflexiveFrame = HaloRawdataFrame = HaloUInt32ColorPickerFrame =\
                     TextFrame = ColorPickerFrame = EntryFrame =\
                     HaloScriptSourceFrame = SoundSampleFrame =\
                     DynamicArrayFrame = DynamicEnumFrame =\
                     HaloScriptTextFrame = HaloBitmapTagFrame = None

from supyr_struct.defs.common_descs import *
from supyr_struct.defs.block_def import BlockDef
from supyr_struct.defs.util import *
from .field_types import *
from .constants import *

# before we do anything, we need to inject these constants so any definitions
# that are built that use them will have them in their descriptor entries.
inject_halo_constants()

def tag_class(*args, **kwargs):
    '''
    A macro for creating a tag_class enum desc with the
    enumerations set to the provided tag_class fcc's.
    '''
    classes = []
    default = 0xffffffff
    for four_cc in args:
        classes.append((tag_class_fcc_to_ext[four_cc], four_cc))

    if len(classes) == 1:
        default = classes[0][1]

    return UEnum32(
        'tag_class',
        *(tuple(sorted(classes)) + (("NONE", 0xffffffff),) ),
        DEFAULT=default, GUI_NAME='', WIDGET_WIDTH=20, **kwargs
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

def get_raw_reflexive_offsets(desc, two_byte_offs, four_byte_offs, off=0):
    if INCLUDE in desc:
        desc = BlockDef.include_attrs(None, dict(desc))
        BlockDef.set_entry_count(None, desc)

    for i in range(desc.get(ENTRIES, 0)):
        f_desc = desc[i]
        f_type = f_desc[TYPE]
        size   = f_desc.get(SIZE, f_type.size)
        if f_type.is_data:
            big = f_type.big
            little = f_type.little
            if big is little or big.enc == little.enc:
                # endianness is forced. dont swap anything
                pass
            elif size == 4:
                four_byte_offs.append(off)
            elif size == 2:
                two_byte_offs.append(off)
            off += size
        elif f_type is Pad:
            off += size
        else:
            off = get_raw_reflexive_offsets(
                f_desc, two_byte_offs, four_byte_offs, off)
    return off


def raw_reflexive(name, substruct, max_count=MAX_REFLEXIVE_COUNT, *names, **desc):
    '''
    This function serves to macro the creation
    of a reflexive treated as rawdata
    '''
    desc = reflexive(name, substruct, max_count, *names, **desc)
    info = desc[RAW_REFLEXIVE_INFO] = [0, [], []]
    sub_desc = desc[STEPTREE][SUB_STRUCT]
    sub_size = info[0] = sub_desc.get(SIZE)
    two_byte_offs, four_byte_offs = info[1], info[2]
    if sub_size is None:
        raise KeyError("Cannot make a raw_reflexive without a substruct size.")

    def data_size(parent=None, new_value=None, struct_size=sub_size, *a, **kw):
        if new_value is None:
            return parent.size*struct_size
        else:
            parent.size = new_value//struct_size

    desc[STEPTREE] = BytearrayRaw(desc[STEPTREE][NAME], SIZE=data_size)
    desc[STEPTREE][SUB_STRUCT] = sub_desc  # store this here in case its needed
    desc[TYPE] = RawReflexive
    get_raw_reflexive_offsets(sub_desc, two_byte_offs, four_byte_offs)
    return desc


def rawdata_ref(name, f_type=BytearrayRaw, max_size=None,
                widget=HaloRawdataFrame, **kwargs):
    '''This function serves to macro the creation of a rawdata reference'''
    ref_struct = dict(rawdata_ref_struct)
    if COMMENT in kwargs: ref_struct[COMMENT] = kwargs.pop(COMMENT)
    if TOOLTIP in kwargs: ref_struct[TOOLTIP] = kwargs.pop(TOOLTIP)
    if max_size is not None:
        ref_struct[0] = dict(ref_struct[0])
        ref_struct[0][MAX] = max_size
        kwargs[MAX] = max_size

    if widget is not None:
        kwargs[WIDGET] = widget

    return RawdataRef(name,
        INCLUDE=ref_struct,
        STEPTREE=f_type("data", GUI_NAME="", SIZE=".size", **kwargs))


def rawtext_ref(name, f_type=StrRawLatin1, max_size=None,
                widget=TextFrame, **kwargs):
    '''This function serves to macro the creation of a rawdata reference'''
    ref_struct = dict(rawdata_ref_struct)
    kwargs.update(WIDGET=widget)
    ref_struct[0] = dict(ref_struct[0])
    ref_struct[0][VISIBLE] = False
    if COMMENT in kwargs: ref_struct[COMMENT] = kwargs.pop(COMMENT)
    if TOOLTIP in kwargs: ref_struct[TOOLTIP] = kwargs.pop(TOOLTIP)
    if max_size is not None:
        ref_struct[0][MAX] = max_size
        kwargs[MAX] = max_size

    return RawdataRef(name,
        INCLUDE=ref_struct, ORIENT="v",
        STEPTREE=f_type("data",
            SIZE=".size", GUI_NAME=name.replace('_', ' '), **kwargs)
            )

tag_id_struct = QStruct("id",
    UInt16("tag table index", DEFAULT=0xFFFF),
    UInt16("table index", DEFAULT=0xFFFF),
    VISIBLE=False, EDITABLE=False
    )


def dependency(name='tag ref', valid_ids=None, **kwargs):
    '''This function serves to macro the creation of a tag dependency'''
    if isinstance(valid_ids, tuple):
        valid_ids = tag_class(*valid_ids)
    elif isinstance(valid_ids, str):
        valid_ids = tag_class(valid_ids)
    elif valid_ids is None:
        valid_ids = valid_tags

    return TagRef(name,
        valid_ids,
        INCLUDE=tag_ref_struct,
        STEPTREE=StrTagRef(
            "filepath", SIZE=tag_ref_str_size, GUI_NAME="", MAX=234),
        **kwargs
        )


def blam_header(tagid, version=1):
    '''This function serves to macro the creation of a tag header'''
    header_desc = dict(tag_header)
    header_desc[1] = dict(header_desc[1])
    header_desc[5] = dict(header_desc[5])
    header_desc[1][DEFAULT] = tagid
    header_desc[5][DEFAULT] = version
    return header_desc


_func_unit_scales = {}  # holds created unit_scales for reuse

def get_unit_scale(scale60, val30=1):
    """
    Returns a function to be used in the UNIT_SCALE of a descriptor that
    will change the scale depending on if the 60fps flag is set or not.
    """
    assert 0 not in (val30, scale60), ("60fps scale and default 30fps " +
                                       "value must both be non-zero.")
    val60 = val30*scale60

    key = (val30, val60)
    if key in _func_unit_scales:
        return _func_unit_scales[key]

    def unit_scale(*args, **kwargs):
        w = kwargs.get('f_widget')
        if kwargs.get('get_scales'):
            # used for getting both the 30 and 60 fps scales
            return (val30, val60)

        try:
            if w.tag_window.save_as_60:
                return val60
        except AttributeError:
            return val30

    _func_unit_scales[key] = unit_scale
    unit_scale.fps_60_scale = True
    return unit_scale

# typical unit_scales for seconds and seconds squared fields
per_sec_unit_scale    = get_unit_scale(2)
per_sec_sq_unit_scale = get_unit_scale(4)
sec_unit_scale    = get_unit_scale(1/2)
sec_sq_unit_scale = get_unit_scale(1/4)

irad = 180/pi
irad_per_sec_unit_scale = get_unit_scale(1/2, irad)
irad_per_sec_sq_unit_scale = get_unit_scale(1/4, irad)

def dyn_senum8(name, *args, **kwargs):
    kwargs.setdefault('DEFAULT', -1)
    kwargs.setdefault('WIDGET', DynamicEnumFrame)
    return SInt8(name, *args, **kwargs)

def dyn_senum16(name, *args, **kwargs):
    kwargs.setdefault('DEFAULT', -1)
    kwargs.setdefault('WIDGET', DynamicEnumFrame)
    return SInt16(name, *args, **kwargs)

def dyn_senum32(name, *args, **kwargs):
    kwargs.setdefault('DEFAULT', -1)
    kwargs.setdefault('WIDGET', DynamicEnumFrame)
    return SInt32(name, *args, **kwargs)

def ascii_str32(name, **kwargs):
    # encoding used is latin1 to take care of cases
    # where the string has invalid characters in it
    return StrLatin1(str(name), SIZE=32, **kwargs)

def float_zero_to_one(name, *args, **kwargs):
    return Float(name, *args, MIN=0.0, MAX=1.0, SIDETIP="[0,1]", **kwargs)
def float_neg_one_to_one(name, *args, **kwargs):
    return Float(name, *args, MIN=-1.0, MAX=1.0, SIDETIP="[-1,1]", **kwargs)

def float_sec(name, *args, **kwargs):
    kwargs.setdefault('SIDETIP', "seconds")
    kwargs.setdefault('UNIT_SCALE', sec_unit_scale)
    return Float(name, *args, **kwargs)

def float_deg(name, *args, **kwargs):
    kwargs.setdefault('SIDETIP', "degrees")
    return Float(name, *args, **kwargs)

def float_deg_sec(name, *args, **kwargs):
    kwargs.setdefault('SIDETIP', "degrees/sec")
    kwargs.setdefault('UNIT_SCALE', per_sec_unit_scale)
    return Float(name, *args, **kwargs)

def float_rad(name, *args, **kwargs):
    return Float(name, *args, SIDETIP="degrees",
                 UNIT_SCALE=irad, **kwargs)
def float_rad_sec(name, *args, **kwargs):
    kwargs.setdefault('SIDETIP', "degrees/sec")
    kwargs.setdefault('UNIT_SCALE', irad_per_sec_unit_scale)
    return Float(name, *args, **kwargs)
def float_rad_sec_sq(name, *args, **kwargs):
    # yes, keep this as per_sec and not per_sec_sq.
    # this is because of how halo uses these values.
    kwargs.setdefault('SIDETIP', "degrees/(sec^2)")
    kwargs.setdefault('UNIT_SCALE', irad_per_sec_unit_scale)
    return Float(name, *args, **kwargs)

def float_wu(name, *args, **kwargs):
    kwargs.setdefault('SIDETIP', "world units")
    return Float(name, *args, **kwargs)
def float_wu_sec(name, *args, **kwargs):
    kwargs.setdefault('SIDETIP', "world units/sec")
    kwargs.setdefault('UNIT_SCALE', per_sec_unit_scale)
    return Float(name, *args, **kwargs)
def float_wu_sec_sq(name, *args, **kwargs):
    kwargs.setdefault('SIDETIP', "world units/(sec^2)")
    kwargs.setdefault('UNIT_SCALE', per_sec_sq_unit_scale)
    return Float(name, *args, **kwargs)

def float_zero_to_inf(name, *args, **kwargs):
    return Float(name, *args, SIDETIP="[0,+inf]", **kwargs)


from_to = QStruct('',
    Float("from", GUI_NAME=''),
    Float("to"),
    ORIENT='h'
    )

def from_to_deg(name, *args, **kwargs):
    return QStruct(name,
        Float("from", GUI_NAME=''),
        Float("to"), *args,
        ORIENT='h', SIDETIP='degrees', **kwargs
        )

def from_to_rad(name, *args, **kwargs):
    return QStruct(name,
        Float("from", UNIT_SCALE=irad, GUI_NAME=''),
        Float("to",   UNIT_SCALE=irad), *args,
        ORIENT='h', SIDETIP='degrees', **kwargs
        )

def from_to_rad_sec(name, *args, **kwargs):
    return QStruct(name,
        Float("from", UNIT_SCALE=irad_per_sec_unit_scale, GUI_NAME=''),
        Float("to",   UNIT_SCALE=irad_per_sec_unit_scale), *args,
        ORIENT='h', SIDETIP='degrees/sec', **kwargs
        )

def from_to_sec(name, *args, **kwargs):
    return QStruct(name,
        Float("from", UNIT_SCALE=sec_unit_scale, GUI_NAME=''),
        Float("to",   UNIT_SCALE=sec_unit_scale), *args,
        ORIENT='h', SIDETIP='seconds', **kwargs
        )

def from_to_wu(name, *args, **kwargs):
    return QStruct(name,
        Float("from", GUI_NAME=''),
        Float("to"), *args,
        ORIENT='h', SIDETIP='world units', **kwargs
        )

def from_to_wu_sec(name, *args, **kwargs):
    return QStruct(name,
        Float("from", UNIT_SCALE=per_sec_unit_scale, GUI_NAME=''),
        Float("to",   UNIT_SCALE=per_sec_unit_scale), *args,
        ORIENT='h', SIDETIP='world units/sec', **kwargs
        )

def from_to_zero_to_one(name, *args, **kwargs):
    return QStruct(name,
        Float("from", MIN=0.0, MAX=1.0, GUI_NAME=''),
        Float("to", MIN=0.0, MAX=1.0), *args,
        ORIENT='h', SIDETIP='[0,1]', **kwargs
        )

def from_to_neg_one_to_one(name, *args, **kwargs):
    return QStruct(name,
        Float("from", MIN=-1.0, MAX=1.0, GUI_NAME=''),
        Float("to", MIN=-1.0, MAX=1.0), *args,
        ORIENT='h', SIDETIP='[-1,1]', **kwargs
        )

def yp_float_deg(name, *args, **kwargs):
    return QStruct(name,
        Float("y"), Float("p"), *args,
        ORIENT='h', SIDETIP='degrees', **kwargs
        )

def ypr_float_deg(name, *args, **kwargs):
    return QStruct(name,
        Float("y"), Float("p"), Float("r"), *args,
        ORIENT='h', SIDETIP='degrees', **kwargs
        )

def yp_float_rad(name, *args, **kwargs):
    return QStruct(name,
        Float("y", UNIT_SCALE=irad),
        Float("p", UNIT_SCALE=irad), *args,
        ORIENT='h', SIDETIP='degrees', **kwargs
        )

def ypr_float_rad(name, *args, **kwargs):
    return QStruct(name,
        Float("y", UNIT_SCALE=irad),
        Float("p", UNIT_SCALE=irad),
        Float("r", UNIT_SCALE=irad), *args,
        ORIENT='h', SIDETIP='degrees', **kwargs
        )

def anim_func_per_pha_macro(name, **desc):
    desc.setdefault("HIDE_TITLE", True)
    return Struct(name,
        SEnum16("function", *animation_functions,
            GUI_NAME="%s function" % name),
        Pad(2),
        Float("period", SIDETIP='seconds',
            GUI_NAME="%s period" % name, UNIT_SCALE=sec_unit_scale),
        Float("phase",  SIDETIP='seconds',
            GUI_NAME="%s phase" % name,  UNIT_SCALE=sec_unit_scale),
        **desc
        )

def anim_func_per_sca_macro(name, **desc):
    desc.setdefault("HIDE_TITLE", True)
    return Struct(name,
        SEnum16("function", *animation_functions,
            GUI_NAME="%s function" % name),
        Pad(2),
        Float("period", SIDETIP='seconds',
            GUI_NAME="%s period" % name, UNIT_SCALE=sec_unit_scale),
        Float("scale",  SIDETIP='base map repeats',
            GUI_NAME="%s scale" % name),  # base map repeats
        **desc
        )

def anim_src_func_per_pha_sca_macro(name, **desc):
    desc.setdefault("HIDE_TITLE", True)
    return Struct(name,
        SEnum16("source", *function_outputs,
            GUI_NAME="%s source" % name),
        SEnum16("function", *animation_functions,
            GUI_NAME="%s function" % name),
        Float("period", SIDETIP='seconds',
            GUI_NAME="%s period" % name, UNIT_SCALE=sec_unit_scale),
        Float("phase", SIDETIP='seconds',
            GUI_NAME="%s phase" % name, UNIT_SCALE=sec_unit_scale),
        Float("scale",  SIDETIP='repeats',
            GUI_NAME="%s scale" % name),  # repeats
        **desc
        )

def anim_src_func_per_pha_sca_rot_macro(name, **desc):
    desc.setdefault("HIDE_TITLE", True)
    return Struct(name,
        SEnum16("source", *function_outputs,
            GUI_NAME="%s source" % name),
        SEnum16("function", *animation_functions,
            GUI_NAME="%s function" % name),
        Float("period", SIDETIP='seconds',
            GUI_NAME="%s period" % name, UNIT_SCALE=sec_unit_scale),
        Float("phase", SIDETIP='seconds',
            GUI_NAME="%s phase" % name, UNIT_SCALE=sec_unit_scale),
        Float("scale",  SIDETIP='degrees',
            GUI_NAME="%s scale" % name),  # repeats
        **desc
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


# ########################################################################
# The element order in all the enumerators is important(DONT SHUFFLE THEM)
# ########################################################################

#Shared Enumerator options
materials_list = (
    "dirt",
    "sand",
    "stone",
    "snow",
    "wood",
    "metal_hollow",
    "metal_thin",
    "metal_thick",
    "rubber",
    "glass",
    "force_field",
    "grunt",
    "hunter_armor",
    "hunter_skin",
    "elite",
    "jackal",
    "jackal_energy_shield",
    "engineer_skin",
    "engineer_force_field",
    "flood_combat_form",
    "flood_carrier_form",
    "cyborg_armor",
    "cyborg_energy_shield",
    "human_armor",
    "human_skin",
    "sentinel",
    "moniter",
    "plastic",
    "water",
    "leaves",
    "elite_energy_shield",
    "ice",
    "hunter_shield",
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
    "combat_form",
    "infection_form",
    "carrier_form",
    "moniter",
    "sentinal",
    "none",
    "mounted_weapon"
    )
animation_functions = (
    "one",
    "zero",
    "cosine",
    "cosine_variable_period",
    "diagonal_wave",
    "diagonal_wave_variable_period",
    "slide",
    "slide_variable_period",
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
    "high_explosive",
    "sniper",
    "melee",
    "flame",
    "mounted_weapon",
    "vehicle",
    "plasma",
    "needle",
    "shotgun",
    )
grenade_types = (
    'human_frag',
    'covenant_plasma'
    )
fade_functions = (
    "linear",
    "early",
    "very_early",
    "late",
    "very_late",
    "cosine",
    )
detail_map_functions = (
    "double_biased_multiply",
    "multiply",
    "double_biased_add",
    )
device_functions = (
    "none",
    "power",
    "change_in_power",
    "position",
    "change_in_position",
    "locked",
    "delay",
    )
render_anchor = (
    "with_primary",
    "with_screen_space",
    "with_zsprite"
    )
render_fade_mode = (
    "none",
    "fade_when_perpendicular",
    "fade_when_parallel",
    )
render_mode = (
    "screen_facing",
    "parallel_to_direction",
    "perpendicular_to_direction"
    )
shader_flags = (
    "sort_bias",
    "nonlinear_tint",
    "dont_overdraw_fp_weapon"
    )
blend_flags = (
    "blend_in_hsv",
    "more_colors"
    )
hud_scaling_flags = (
    "dont_scale_offset",
    "dont_scale_size",
    "use_high_res_scale"
    )
hud_flash_flags = (
    "reverse_default_and_flashing_colors",
    )
hud_anchors = (
    "top_left",
    "top_right",
    "bottom_left",
    "bottom_right",
    "center"
    )
hud_panel_meter_flags = (
    "use_min_max_for_state_changes",
    "interpolate_between_min_max_flash_colors",
    "interpolate_color_along_hsv_space",
    "more_colors_for_hsv_interpolation ",
    "invert_interpolation"
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
    "multiply_2x",
    "dot",
    )
blend_functions = (
    "current",
    "next_map",
    "multiply",
    "double_multiply",
    "add",
    "add_signed_current",
    "add_signed_next_map",
    "subtract_signed_current",
    "subtract_signed_next_map",
    "blend_current_alpha",
    "blend_current_alpha_inverse",
    "blend_next_map_alpha",
    "blend_next_map_alpha_inverse",
    )
framebuffer_blend_functions = (
    "alpha_blend",
    "multiply",
    "double_multiply",
    "add",
    "subtract",
    "component_min",
    "component_max",
    "alpha_multiply_add",
    )

# DO NOT MODIFY ANY OF THESE SCRIPT ENUMS.
# The exact lettering is important as the script extractor uses
# these strings to reconstruct scripts
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

# DO NOT MODIFY ANY OF THESE SCRIPT ENUMS.
# The exact lettering is important as the script extractor
# uses these strings to reconstruct scripts

    "string",
    "script",

    "trigger_volume",
    "cutscene_flag",
    "cutscene_camera_point",
    "cutscene_title",
    "cutscene_recording",

    "device_group",
    "ai",
    "ai_command_list",
    "starting_profile",

    "conversation",
    "navpoint",
    "hud_message",
    "object_list",

    "sound",
    "effect",
    "damage",
    "looping_sound",
    "animation_graph",
    "actor_variant",
    "damage_effect",

    "object_definition",
    "game_difficulty",
    "team",
    "ai_default_state",
    "actor_type",
    "hud_corner",

    "object",
    "unit",
    "vehicle",
    "weapon",
    "device",
    "scenery",

    "object_name",
    "unit_name",
    "vehicle_name",
    "weapon_name",
    "device_name",
    "scenery_name"
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
    "A_in",
    "B_in",
    "C_in",
    "D_in",
    "A_out",
    "B_out",
    "C_out",
    "D_out",
    )
function_inputs = (
    "none",
    "A_in",
    "B_in",
    "C_in",
    "D_in",
    )
function_outputs = (
    "none",
    "A_out",
    "B_out",
    "C_out",
    "D_out",
    )
#Tag class specific enumerators
object_export_to = (
    'none',
    'body_vitality',
    'shield_vitality',
    'recent_body_damage',
    'recent_shield_damage',
    'random_constant',
    'umbrella_shield_vitality',
    'shield_stun',
    'recent_umbrella_shield_vitality',
    'umbrella_shield_stun',
    'region_0_damage',
    'region_1_damage',
    'region_2_damage',
    'region_3_damage',
    'region_4_damage',
    'region_5_damage',
    'region_6_damage',
    'region_7_damage',
    'alive',
    'compass',
    )
weapon_export_to = (
    'none',
    'heat',
    'primary_ammunition',
    'secondary_ammunition',
    'primary_rate_of_fire',
    'secondary_rate_of_fire',
    'ready',
    'primary_ejection_port',
    'secondary_ejection_port',
    'overheated',
    'primary_charged',
    'secondary_charged',
    'illumination',
    'age',
    'integrated_light',
    'primary_firing',
    'secondary_firing',
    'primary_firing_on',
    'secondary_firing_on',
    )
biped_inputs = (
    'none',
    'flying_velocity'
    )
projectile_inputs = (
    "none",
    "range_remaining",
    "time_remaining",
    "tracer",
    )
unit_inputs = (
    "none",
    "driver_seat_power",
    "gunner_seat_power",
    "aiming_change",
    "mouth_aperture",
    "integrated_light_power",
    "can_blink",
    "shield_sapping"
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
    "speed_absolute",
    "speed_forward",
    "speed_backward",
    "slide_absolute",
    "slide_left",
    "slide_right",
    "speed_slide_maximum",
    "turn_absolute",
    "turn_left",
    "turn_right",
    "crouch",
    "jump",
    "walk",
    "velocity_air",
    "velocity_water",
    "velocity_ground",
    "velocity_forward",
    "velocity_left",
    "velocity_up",
    "left_tread_position",
    "right_tread_position",
    "left_tread_velocity",
    "right_tread_velocity",
    "front_left_tire_position",
    "front_right_tire_position",
    "back_left_tire_position",
    "back_right_tire_position",
    "front_left_tire_velocity",
    "front_right_tire_velocity",
    "back_left_tire_velocity",
    "back_right_tire_velocity",
    "wingtip_contrail",
    "hover",
    "thrust",
    "engine_hack",
    "wingtip_contrail_new",
    )
vehicle_types = (
    "human_tank",
    "human_jeep",
    "human_boat",
    "human_plane",
    "alien_scout",
    "alien_fighter",
    "turret",
    )
weapon_types = (
    "undefined",
    "shotgun",
    "needler",
    "plasma_pistol",
    "plasma_rifle",
    )
trans_shdr_properties = (
    "alpha_tested",
    "decal",
    "two_sided",
    "first_map_is_in_screenspace",
    "draw_before_water",
    "ignore_effect",
    "scale_first_map_with_distance",
    "numeric",
    )
trans_shdr_first_map_type = (
    "map_2d",
    "reflection_cube_map",
    "object_centered_cube_map",
    "viewer_centered_cube_map",
    )
detail_mask = (
    "none",
    "red_inverse",
    "red",
    "green_inverse",
    "green",
    "blue_inverse",
    "blue",
    "alpha_inverse",
    "alpha"
    )

# Descriptors
tag_header = Struct("blam header",
    Pad(36),
    UEnum32("tag class",
        GUI_NAME="tag class", INCLUDE=valid_tags, EDITABLE=False
        ),
    UInt32("checksum", DEFAULT=0x4D6F7A7A, EDITABLE=False),
    UInt32("header size",  DEFAULT=64, EDITABLE=False),
    BBool64("flags",
        "edited with mozz",
        EDITABLE=False
        ),
    UInt16("version", DEFAULT=1, EDITABLE=False),
    UInt8("integrity0", DEFAULT=0, EDITABLE=False),
    UInt8("integrity1", DEFAULT=255, EDITABLE=False),
    UEnum32("engine id",
        ("halo 1", 'blam'),
        DEFAULT='blam', EDITABLE=False
        ),
    VISIBLE=False, SIZE=64, ENDIAN=">"  # KEEP THE ENDIAN SPECIFICATION
    )

# Miscellaneous, Halo specific descriptors
anim_func_per_pha = Struct('',
    SEnum16("function", *animation_functions),
    Pad(2),
    Float("period", SIDETIP='seconds', UNIT_SCALE=sec_unit_scale),
    Float("phase", SIDETIP='seconds',  UNIT_SCALE=sec_unit_scale),
    )

anim_func_per_sca = Struct('',
    SEnum16("function", *animation_functions),
    Pad(2),
    Float("period", SIDETIP='seconds', UNIT_SCALE=sec_unit_scale),
    Float("scale", SIDETIP='base map repeats'),  # base map repeats
    )

anim_src_func_per_pha_sca = Struct('',
    SEnum16("source", *function_outputs),
    SEnum16("function", *animation_functions),
    Float("period", SIDETIP='seconds', UNIT_SCALE=sec_unit_scale),
    Float("phase", SIDETIP='seconds',  UNIT_SCALE=sec_unit_scale),
    Float("scale", SIDETIP='repeats'),  # repeats
    )

anim_src_func_per_pha_sca_rot = Struct('',
    SEnum16("source", *function_outputs),
    SEnum16("function", *animation_functions),
    Float("period", SIDETIP='seconds', UNIT_SCALE=sec_unit_scale),
    Float("phase", SIDETIP='seconds',  UNIT_SCALE=sec_unit_scale),
    Float("scale", SIDETIP='degrees'),  # repeats
    )


# This is the descriptor used wherever a tag references a rawdata chunk
rawdata_ref_struct = RawdataRef('rawdata ref', 
    SInt32("size", GUI_NAME="", SIDETIP="bytes", EDITABLE=False),
    FlBool32("flags",
        "data in resource map",
        VISIBLE=False,
        ),
    FlUInt32("raw pointer", VISIBLE=False),  # doesnt use magic
    FlUInt32("pointer", VISIBLE=False, DEFAULT=0xFFFFFFFF),
    FlUInt32("id", VISIBLE=False),
    ORIENT='h'
    )

# This is the descriptor used wherever a tag reference a reflexive
reflexive_struct = Reflexive('reflexive',
    SInt32("size", VISIBLE=False),
    FlUInt32("pointer", VISIBLE=False, DEFAULT=0xFFFFFFFF),
    FlUInt32("id", VISIBLE=False),  # 0 in meta it seems
    )

# This is the descriptor used wherever a tag references another tag
tag_ref_struct = TagRef('dependency',
    valid_tags,
    SInt32("path pointer", VISIBLE=False, EDITABLE=False),
    SInt32("path length", MAX=243, VISIBLE=False, EDITABLE=False),
    tag_id_struct,
    ORIENT='h'
    )

predicted_resource = Struct('predicted resource',
    SInt16('type',
        'bitmap',
        'sound',
        ),
    SInt16('resource index'),
    UInt32('tag index'),
    )

extra_layers_block = dependency("extra layer", valid_shaders)

damage_modifiers = QStruct("damage modifiers",
    *(float_zero_to_inf(material_name) for material_name in materials_list)
    )

# Miscellaneous shared descriptors
compressed_normal_32 = BitStruct('compressed_norm32',
    S1BitInt("i",
        SIZE=11, UNIT_SCALE=1/1023, MIN=-1023, MAX=1023, WIDGET_WIDTH=10),
    S1BitInt("j",
        SIZE=11, UNIT_SCALE=1/1023, MIN=-1023, MAX=1023, WIDGET_WIDTH=10),
    S1BitInt("k",
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
xrgb_byte = QStruct('xrgb_uint8',
    Pad(1), UInt8("r"), UInt8("g"), UInt8("b"),
    ORIENT='h', WIDGET=ColorPickerFrame
    )

argb_byte = QStruct('argb_uint8',
    UInt8("a"), UInt8("r"), UInt8("g"), UInt8("b"),
    ORIENT='h', WIDGET=ColorPickerFrame
    )

xrgb_uint32 = UInt32('xrgb_uint32',
    WIDGET=HaloUInt32ColorPickerFrame, COLOR_CHANNELS="rgb", ORIENT="h")
argb_uint32 = UInt32('argb_uint32',
    WIDGET=HaloUInt32ColorPickerFrame, COLOR_CHANNELS="argb", ORIENT="h")

# rotations
ijkw_float = QStruct('ijkw_float',
    Float("i"), Float("j"), Float("k"), Float("w", DEFAULT=1.0),
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
    Float("y"), Float("p"),
    ORIENT='h',
    )
ypr_float = QStruct('ypr_float',
    Float("y"), Float("p"), Float("r"),
    ORIENT='h',
    )

# texture coordinates
uv_float = QStruct('uv_float',
    Float("u"), Float("v"),
    ORIENT='h'
    )

#############################
# Open Sauce related things #
#############################
def tag_class_os(*args):
    '''
    A macro for creating an Open Sauce tag_class enum desc
    with the enumerations set to the provided tag_class fcc's.
    '''
    default = 0xffffffff
    classes = []
    for four_cc in args:
        classes.append((tag_class_fcc_to_ext_os[four_cc], four_cc))

    if len(classes) == 1:
        default = classes[0][1]

    return UEnum32(
        'tag_class',
        *(tuple(classes) + (("NONE", 0xffffffff),) ),
        DEFAULT=0xffffffff, GUI_NAME=''
        )


def dependency_os(name='tag ref', valid_ids=None, **kwargs):
    '''This function serves to macro the creation of a tag dependency'''
    if isinstance(valid_ids, tuple):
        valid_ids = tag_class_os(*valid_ids)
    elif isinstance(valid_ids, str):
        valid_ids = tag_class_os(valid_ids)
    elif valid_ids is None:
        valid_ids = valid_tags_os

    return TagRef(name,
        valid_ids,
        INCLUDE=tag_ref_struct,
        STEPTREE=StrTagRef(
            "filepath", SIZE=tag_ref_str_size, GUI_NAME="", MAX=234),  # 10 < Halo1
        **kwargs
        )


def blam_header_os(tagid, version=1):
    '''This function serves to macro the creation of a tag header'''
    header_desc = dict(tag_header_os)
    header_desc[1] = dict(header_desc[1])
    header_desc[5] = dict(header_desc[5])
    header_desc[1][DEFAULT] = tagid
    header_desc[5][DEFAULT] = version
    return header_desc


valid_tags_os = tag_class_os(*tag_class_fcc_to_ext_os.keys())


# ########################################################################
# The element order in all the enumerators is important(DONT SHUFFLE THEM)
# ########################################################################

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
    UEnum32("tag_class",
        GUI_NAME="tag class", INCLUDE=valid_tags_os, EDITABLE=False
        ),
    UInt32("checksum", DEFAULT=0x4D6F7A7A, EDITABLE=False), 
    UInt32("header size", DEFAULT=64, EDITABLE=False),
    Bool64("flags",
        "edited with mozz",
        EDITABLE=False
        ),
    UInt16("version", DEFAULT=1, EDITABLE=False),
    UInt8("integrity0", DEFAULT=0, EDITABLE=False),
    UInt8("integrity1", DEFAULT=255, EDITABLE=False),
    UEnum32("engine id",
        ("halo 1", 'blam'),
        DEFAULT='blam', EDITABLE=False
        ),
    VISIBLE=False, SIZE=64, ENDIAN=">"  # KEEP THE ENDIAN SPECIFICATION
    )

valid_model_animations_yelo = tag_class_os('antr', 'magy')

os_shader_extension = Struct("os shader extension",
    Pad(4),
    QStruct("fade controls",
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
