from copy import copy, deepcopy

try:
    from mozzarilla.field_widgets import *
except Exception:
    ReflexiveFrame = HaloRawdataFrame = TextFrame = ColorPickerFrame =\
                     EntryFrame = SoundSampleFrame = DynamicArrayFrame =\
                     H2BitmapTagFrame = None
from ..common_descs import *
from .field_types import *
from .constants import *
from .enums import *


resource = Struct("resource",
    SEnum8("type",
        "tag_block",  # reflexive
        "tag_data",   # rawdata
        "vertex_buffer",
        ),
    SInt8("unknown0", DEFAULT=2, VISIBLE=False),
    SInt16("primary_locator2", VISIBLE=False),
    SInt16("primary_locator",
        TOOLTIP="offset into the block section that the tag block/\n"
                "tag data/vertex buffer header block is located at."),
    SInt16("secondary_locator",
        TOOLTIP="tag block size in bytes(-1 if not a tag block)"),
    UInt32("resource_data_size",
        TOOLTIP="size of the rsrc section in bytes"),
    UInt32("resource_data_offset",
        TOOLTIP="offset into the block section that the rsrc section\n"
                "is located at."),
    SIZE=16
    )

def h2_tag_class(*args, **kwargs):
    '''
    A macro for creating a tag_class enum desc with the
    enumerations set to the provided tag_class fcc's.
    '''
    classes = []
    for four_cc in args:
        classes.append((h2_tag_class_fcc_to_ext[four_cc], four_cc))

    return UEnum32(
        'tag_class',
        *(tuple(sorted(classes)) + (("NONE", 0xffffffff),) ),
        DEFAULT=0xffffffff, GUI_NAME='', WIDGET_WIDTH=20, **kwargs
        )

def h2_reflexive(name, substruct, max_count=MAX_REFLEXIVE_COUNT, *names, **desc):
    '''This function serves to macro the creation of a reflexive'''
    desc.update(
        INCLUDE=h2_reflexive_struct,
        STEPTREE=Array(name + " array",
            SIZE=".size", MAX=max_count,
            SUB_STRUCT=substruct, WIDGET=ReflexiveFrame
            ),
        SIZE=8
        )
    if DYN_NAME_PATH in desc:
        desc[STEPTREE][DYN_NAME_PATH] = desc.pop(DYN_NAME_PATH)
    if names:
        name_map = {}
        for i in range(len(names)):
            e_name = BlockDef.str_to_name(None, names[i])
            name_map[e_name] = i
            
        desc[STEPTREE][NAME_MAP] = name_map

    return H2Reflexive(name, **desc)


def h2_rawtext_ref(name, f_type=StrRawLatin1, max_size=None,
                   widget=TextFrame, **kwargs):
    '''This function serves to macro the creation of a rawdata reference'''
    ref_struct = dict(h2_rawdata_ref_struct)
    if COMMENT in kwargs: ref_struct[COMMENT] = kwargs.pop(COMMENT)
    if TOOLTIP in kwargs: ref_struct[TOOLTIP] = kwargs.pop(TOOLTIP)
    kwargs.update(WIDGET=widget)
    ref_struct[0] = dict(ref_struct[0])
    ref_struct[0][VISIBLE] = False
    if max_size is not None:
        ref_struct[0][MAX] = max_size
        kwargs[MAX] = max_size

    return H2RawdataRef(name,
        INCLUDE=ref_struct, ORIENT="v",
        STEPTREE=f_type("data",
            SIZE=".size", GUI_NAME=name.replace('_', ' '), **kwargs)
        )

def h2_rawdata_ref(name, f_type=BytearrayRaw, max_size=None,
                   widget=HaloRawdataFrame, **kwargs):
    '''This function serves to macro the creation of a rawdata reference'''
    ref_struct = dict(h2_rawdata_ref_struct)
    if COMMENT in kwargs: ref_struct[COMMENT] = kwargs.pop(COMMENT)
    if TOOLTIP in kwargs: ref_struct[TOOLTIP] = kwargs.pop(TOOLTIP)
    if max_size is not None:
        ref_struct[0] = dict(ref_struct[0])
        ref_struct[0][MAX] = max_size
        kwargs[MAX] = max_size

    if widget is not None:
        kwargs[WIDGET] = widget

    return H2RawdataRef(name,
        INCLUDE=ref_struct,
        STEPTREE=f_type("data", GUI_NAME="", SIZE=".size", **kwargs)
        )


def h2_dependency(name='tag ref', valid_ids=None, **kwargs):
    '''This function serves to macro the creation of a tag dependency'''
    if isinstance(valid_ids, tuple):
        valid_ids = h2_tag_class(*valid_ids)
    elif isinstance(valid_ids, str):
        valid_ids = h2_tag_class(valid_ids)
    elif valid_ids is None:
        valid_ids = valid_h2_tags

    kwargs.setdefault(ORIENT, "h")

    return H2TagRef(name,
        valid_ids,
        UInt32("id", VISIBLE=False),
        SInt32("path length",
            MAX=MAX_TAG_PATH_LEN, OFFSET=4, VISIBLE=False, EDITABLE=False),
        STEPTREE=StrTagRef(
            "filepath", SIZE=tag_ref_str_size, GUI_NAME="", MAX=254),
        **kwargs
        )


def h2_blam_header(tagid, version=1):
    '''This function serves to macro the creation of a tag header'''
    header_desc = dict(h2_tag_header)
    header_desc[1] = dict(header_desc[1])
    header_desc[5] = dict(header_desc[5])
    header_desc[1][DEFAULT] = tagid
    header_desc[5][DEFAULT] = version
    return header_desc


valid_h2_tags = h2_tag_class(*h2_tag_class_fcc_to_ext.keys())


# ###########################################################################
# The order of element in all the enumerators is important(DONT SHUFFLE THEM)
# ###########################################################################

# DO NOT MODIFY ANY OF THESE SCRIPT ENUMS.
# The exact wording is important as the script extractor uses
# these strings to reconstruct scripts
script_types = (
    "startup",
    "dormant",
    "continuous",
    "static",
    "stub",
    "command_script",
    )
script_object_types = (
    "unparsed",
    "special form",
    "function name",
    "passthrough",
    "void",
    "boolean",
    "short",
    "long",
    "string_id",
    "unit_seat_mapping",

    "trigger_volume",
    "cutscene_flag",
    "cutscene_camera_point",
    "cutscene_title",
    "cutscene_recording",

    "device_group",
    "ai_command_list",
    "ai_command_script",
    "ai_behavior",
    "ai_orders",

# DO NOT MODIFY ANY OF THESE SCRIPT ENUMS.
# The exact wording is important as the script extractor uses
# these strings to reconstruct scripts

    "starting_profile",

    "conversation",
    "structure_bsp",
    "navpoint",
    "point reference",
    "hud_message",
    "object_list",

    "effect",
    "damage",
    "looping_sound",
    "animation_graph",
    "damage_effect",

    "object_definition",
    "shader",
    "render model",
    "structure definition",
    "lightmap definition",
    "game_difficulty",
    "actor_type",
    "hud_corner",

    "model_state",
    "unit",
    "object_name",
    "unit_name",
    "vehicle_name",
    "weapon_name",
    "device_name",
    "scenery_name",
    )

#Shared Enumerator options
old_materials_list = materials_list
# old materials list that is referenced in tags, but seems to be unused
del materials_list


# Descriptors
h2_blam_engine_id = dict(blam_engine_id)
h2_blam_engine_id[DEFAULT] = "b2am"
h2_tag_header = Struct("blam_header",
    Pad(36),
    UEnum32("tag class",
        GUI_NAME="tag class", INCLUDE=valid_h2_tags, EDITABLE=False
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
    h2_blam_engine_id,
    VISIBLE=False, SIZE=64
    )


h2_reflexive_struct = H2Reflexive('reflexive',
    SInt32("size", VISIBLE=False),
    UInt32("pointer", VISIBLE=False, DEFAULT=0xFFFFFFFF),
    )

h2_rawdata_ref_struct = H2RawdataRef('rawdata_ref', 
    SInt32("size", GUI_NAME="", SIDETIP="bytes", EDITABLE=False),
    UInt32("pointer", VISIBLE=False, DEFAULT=0xFFFFFFFF),
    ORIENT='h'
    )

def h2_string_id(name, **kwargs):
    return string_id(name, 16, 8, 8, **kwargs)
