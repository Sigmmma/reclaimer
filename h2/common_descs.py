from copy import copy, deepcopy

try:
    from mozzarilla.field_widgets import *
except Exception:
    ReflexiveFrame = HaloRawdataFrame = TextFrame = ColorPickerFrame =\
                     EntryFrame = SoundSampleFrame = DynamicArrayFrame =\
                     H2BitmapTagFrame = None
from supyr_struct.defs.common_descs import *
from supyr_struct.defs.block_def import BlockDef
from .field_types import *
from .constants import *
from supyr_struct.defs.util import *

from ..common_descs import pi, irad, from_to, get_unit_scale,\
     per_sec_unit_scale, per_sec_sq_unit_scale, sec_unit_scale,\
     sec_sq_unit_scale, irad_per_sec_unit_scale, irad_per_sec_sq_unit_scale,\
     dyn_senum8, dyn_senum16, dyn_senum32, ascii_str32,\
     float_zero_to_one, float_neg_one_to_one,\
     float_sec, float_deg, float_deg_sec,\
     float_rad, float_rad_sec, float_rad_sec_sq,\
     float_wu, float_wu_sec, float_wu_sec_sq, float_zero_to_inf,\
     from_to_rad, from_to_wu, from_to_sec, from_to_deg, from_to_zero_to_one,\
     from_to_rad_sec, from_to_wu_sec, from_to_neg_one_to_one,\
     yp_float_deg, ypr_float_deg, yp_float_rad, ypr_float_rad,\
     xyz_float, xy_float, argb_float, rgb_float, xrgb_byte, argb_byte,\
     ijkw_float, ijk_float, ij_float, yp_float, ypr_float,\
     compressed_normal_32, materials_list, tag_id_struct,\
     rawdata_ref_struct, reflexive_struct, tag_ref_struct


def string_id_meta(name):
    return StringID(name,
        UInt16('id'),  # cant name it "index" as that is a method name
        UInt8('unused', VISIBLE=False),
        UInt8('length'),
        )

def string_id_tag(name):
    # encoding used is latin1 to take care of cases
    # where the string has invalid characters in it
    return StringID(name,
        UInt16('id', VISIBLE=False),
        UInt8('unused', VISIBLE=False),
        UInt8('length', VISIBLE=False),
        STEPTREE=StrRawLatin1("data",
            SIZE='.length', GUI_NAME=str(name), MAX=255
            ),
        GUI_NAME="%s struct" % name
        )


#def h2_tagdata_switch(*args, **kwargs):
#    '''
#    Each arg should conform to (desc, bsize, engine_id='BLM_', version=0)
#    '''
#    engine_cases = {}
#    assert len(args)
#
#    def_desc = None
#    new_ver = -1
#    new_bsize = -1
#
#    for case in args:
#        assert hasattr(case, '__len__') and len(case) in (2, 3, 4)
#        engine_id = 'BLM_'
#        version = 0
#        case_desc = case[0]
#        if len(case) > 1:
#            bsize = case[1]
#        if len(case) > 2:
#            engine_id = case[2]
#        if len(case) > 3:
#            version = case[3]
#
#        engine = engine_id_to_name[engine_id]
#        cases = engine_cases.get(engine, [])
#        engine_cases[engine] = cases
#        cases.append((case_desc, bsize, version))
#
#    for engine in tuple(engine_cases.keys()):
#        cases = engine_cases[engine]
#
#        engine_cases[engine] = tbfd_container("tagdata", *cases, def_count=1)
#
#        if engine == 'halo_2':
#            def_desc = engine_cases[engine]
#
#    kwargs.setdefault(VISIBLE, False)
#    kwargs.setdefault(EDITABLE, False)
#    kwargs.setdefault(DEFAULT, def_desc)
#    assert kwargs[DEFAULT] is not None
#
#    return Switch("tagdata",
#        CASES=engine_cases, CASE='.blam_header.engine_id.enum_name', **kwargs)


#def tbfd_container(name, *args, def_case=None, def_count=0, **kwargs):
#    '''
#    Each arg should conform to (desc, bsize, version=0)
#
#    These are the fourCC's of the currently discovered unknown structs
#    tbfd
#
#    MAPP
#    PRPS
#    PRPC
#
#    snpl
#    snsc
#    snpr
#    '''
#    # I'm not 100% certain, but I'm very sure that
#    # tbfd is an acronym for tag_block_field_definition
#
#    # ############################################### #
#    #               !!!!!WARNING!!!!!                 #
#    # When the tag's engine_id is ambl, the FieldType #
#    # of the version and bcount is actually UInt16    #
#    # ############################################### #
#    cases = {}
#    for case in args:
#        assert hasattr(case, '__len__') and len(case) > 1
#        bsize = case[1]
#        version = 0
#        if len(case) > 2:
#            version = case[2]
#
#        if def_case is None:
#            def_case = (version, bsize)
#
#        cases[(version, bsize)] = case[0]
#
#    if def_case is not None:
#        if isinstance(def_case, int):
#            def_case = (0, def_case)
#        else:
#            assert hasattr(def_case, '__len__') and len(def_case)
#            if len(def_case) == 1:
#                def_case = (0, ) + tuple(def_case)
#
#        def_desc = cases[def_case]
#        kwargs.setdefault(DEFAULT, def_desc)
#
#    return TBFDContainer("%s tbfd" % name,
#        QStruct("header",
#            UInt32("sig", DEFAULT='tbfd'),
#            UInt32("version", DEFAULT=def_case[0]),
#            UInt32("bcount", DEFAULT=def_count),
#            UInt32("bsize", DEFAULT=def_case[1]),
#            VISIBLE=False, EDITABLE=False
#            ),
#        Switch(name,
#            CASES=cases, CASE=lambda *a, parent=None, **kw: (
#                parent.header.version, parent.header.bsize)),
#        **kwargs
#        )


from_to_float = from_to

from_to_sint16 = QStruct('',
    SInt16("from", GUI_NAME=''),
    SInt16("to"),
    ORIENT='h'
    )

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

def h2_meta_reflexive(name, substruct, max_count=MAX_REFLEXIVE_COUNT, *names, **desc):
    '''This function serves to macro the creation of a reflexive'''
    desc.update(
        INCLUDE=h2_meta_reflexive_struct,
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

    return H2MetaReflexive(name, **desc)


def h2_meta_rawtext_ref(name, f_type=StrRawLatin1, max_size=None,
                        widget=TextFrame, **kwargs):
    '''This function serves to macro the creation of a rawdata reference'''
    ref_struct = dict(h2_meta_rawdata_ref_struct)
    kwargs.update(WIDGET=widget)
    ref_struct[0] = dict(ref_struct[0])
    ref_struct[0][VISIBLE] = False
    if max_size is not None:
        ref_struct[0][MAX] = max_size
        kwargs[MAX] = max_size

    return H2MetaRawdataRef(name,
        INCLUDE=ref_struct, ORIENT="v",
        STEPTREE=f_type("data",
            SIZE=".size", GUI_NAME=name.replace('_', ' '), **kwargs)
            )

def h2_meta_rawdata_ref(name, f_type=BytearrayRaw, max_size=None, widget=None):
    '''This function serves to macro the creation of a rawdata reference'''
    ref_struct = dict(h2_meta_rawdata_ref_struct)
    if max_size is not None:
        ref_struct[0] = dict(ref_struct[0])
        ref_struct[0][MAX] = max_size

    kwargs = {}
    if widget is not None:
        kwargs[WIDGET] = widget

    return H2MetaRawdataRef(name,
        INCLUDE=ref_struct,
        STEPTREE=f_type("data", GUI_NAME="", SIZE=".size", **kwargs))


def h2_meta_tag_ref(name='tag ref', valid_ids=None):
    '''This function serves to macro the creation of a tag dependency'''
    if isinstance(valid_ids, tuple):
        valid_ids = h2_tag_class(*valid_ids)
    elif isinstance(valid_ids, str):
        valid_ids = h2_tag_class(valid_ids)
    elif valid_ids is None:
        valid_ids = valid_h2_tags

    return H2MetaTagRef(name,
        valid_ids,
        tag_id_struct
        )

def h2_reflexive(*args, **kwargs):
    '''This function serves to macro the creation of a reflexive'''
    desc = h2_meta_reflexive(*args, **kwargs)
    for i in range(desc['ENTRIES']):
        desc.pop(i, None)
    desc["SIZE"] = 12
    desc["INCLUDE"] = reflexive_struct
    desc["TYPE"] = H2Reflexive
    return desc


def h2_rawdata_ref(*args, **kwargs):
    '''This function serves to macro the creation of a rawdata reference'''
    desc = h2_meta_rawdata_ref(*args, **kwargs)
    for i in range(desc['ENTRIES']):
        desc.pop(i, None)
    desc["SIZE"] = 20
    desc["INCLUDE"] = rawdata_ref_struct
    desc["TYPE"] = H2RawdataRef
    return desc


def h2_tag_ref(*args, **kwargs):
    '''This function serves to macro the creation of a tag dependency'''
    desc = h2_meta_tag_ref(*args, **kwargs)
    for i in range(desc['ENTRIES']):
        desc.pop(i, None)
    desc["SIZE"] = 16
    desc["INCLUDE"] = tag_ref_struct
    desc["TYPE"] = H2TagRef
    return desc


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
    UEnum32("engine id",
        (engine_id_to_name['BLM_'], 'BLM!'),
        (engine_id_to_name['LAMB'], 'LAMB'),
        (engine_id_to_name['MLAB'], 'MLAB'),
        (engine_id_to_name['ambl'], 'ambl'),
        DEFAULT='BLM!', EDITABLE=False
        ),
    VISIBLE=False, SIZE=64
    )


h2_meta_tag_index_ref_struct = H2MetaTagRef('h2 meta dependency',
    valid_h2_tags,
    tag_id_struct,
    ORIENT='h'
    )

h2_meta_reflexive_struct = H2MetaReflexive('h2 meta reflexive',
    SInt32("size", VISIBLE=False),
    UInt32("pointer", VISIBLE=False, DEFAULT=0xFFFFFFFF),
    )

h2_meta_rawdata_ref_struct = H2MetaRawdataRef('h2 meta rawdata ref', 
    SInt32("size", GUI_NAME="", SIDETIP="bytes", EDITABLE=False),
    UInt32("pointer", VISIBLE=False, DEFAULT=0xFFFFFFFF),
    ORIENT='h'
    )

# these structs replace the above ones when used outside a map
h2_tag_index_ref_struct = H2TagRef('dependency',
    valid_h2_tags,
    SInt32("path pointer", VISIBLE=False, EDITABLE=False),
    SInt32("path length", MAX=243, VISIBLE=False, EDITABLE=False),
    tag_id_struct,
    ORIENT='h'
    )

h2_reflexive_struct = H2Reflexive('reflexive',
    SInt32("size", VISIBLE=False),
    UInt32("pointer", VISIBLE=False, DEFAULT=0xFFFFFFFF),
    UInt32("id", VISIBLE=False),
    )

h2_rawdata_ref_struct = H2RawdataRef('rawdata ref', 
    SInt32("size", GUI_NAME="", SIDETIP="bytes", EDITABLE=False),
    Bool32("flags",
        "data in resource map",
        VISIBLE=False,
        ),
    UInt32("raw pointer", VISIBLE=False),
    UInt32("pointer", VISIBLE=False, DEFAULT=0xFFFFFFFF),
    UInt32("id", VISIBLE=False),
    ORIENT='h'
    )
