from copy import copy, deepcopy

try:
    from mozzarilla.field_widgets import *
except Exception:
    ReflexiveFrame = HaloRawdataFrame = TextFrame = ColorPickerFrame =\
                     EntryFrame = SoundSampleFrame = DynamicArrayFrame = None
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


def ascii_str_varlen(name):
    # encoding used is latin1 to take care of cases
    # where the string has invalid characters in it
    return Struct(name,
        UInt24('offset', VISIBLE=False, EDITABLE=False),
        UInt8('length', VISIBLE=False, EDITABLE=False),
        STEPTREE=StrRawLatin1("data",
            SIZE='.length', GUI_NAME=str(name), MAX=255
            ),
        GUI_NAME="%s struct" % name
        )


def h3_tag_class(*args, **kwargs):
    '''
    A macro for creating a tag_class enum desc with the
    enumerations set to the provided tag_class fcc's.
    '''
    classes = []
    for four_cc in args:
        classes.append((h3_tag_class_fcc_to_ext[four_cc], four_cc))

    return UEnum32(
        'tag_class',
        *(tuple(sorted(classes)) + (("NONE", 0xffffffff),) ),
        DEFAULT=0xffffffff, GUI_NAME='', WIDGET_WIDTH=20, **kwargs
        )

def h3_meta_reflexive(name, substruct, max_count=MAX_REFLEXIVE_COUNT, *names, **desc):
    '''This function serves to macro the creation of a reflexive'''
    desc.update(
        INCLUDE=h3_meta_reflexive_struct,
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

    return H3MetaReflexive(name, **desc)


def h3_meta_rawdata_ref(name, f_type=BytearrayRaw, max_size=None, widget=None):
    '''This function serves to macro the creation of a rawdata reference'''
    ref_struct = dict(h3_meta_rawdata_ref_struct)
    if max_size is not None:
        ref_struct[0] = dict(ref_struct[0])
        ref_struct[0][MAX] = max_size

    kwargs = {}
    if widget is not None:
        kwargs[WIDGET] = widget

    return H3MetaRawdataRef(name,
        INCLUDE=ref_struct,
        STEPTREE=f_type("data", GUI_NAME="", SIZE=".size", **kwargs))


def h3_meta_dependency(name='tag ref', valid_ids=None):
    '''This function serves to macro the creation of a tag dependency'''
    if isinstance(valid_ids, tuple):
        valid_ids = h3_tag_class(*valid_ids)
    elif isinstance(valid_ids, str):
        valid_ids = h3_tag_class(valid_ids)
    elif valid_ids is None:
        valid_ids = valid_h3_tags

    return H3MetaTagIndexRef(name,
        valid_ids,
        STEPTREE=StrTagRef(
            "filepath", SIZE=tag_ref_str_size, GUI_NAME="", MAX=234),  # 10 < Halo1
        )

def h3_reflexive(*args, **kwargs):
    '''This function serves to macro the creation of a reflexive'''
    desc = h3_meta_reflexive(*args, **kwargs)
    desc["SIZE"] = 12
    desc["INCLUDE"] = reflexive_struct
    desc["TYPE"] = H3Reflexive


def h3_rawdata_ref(*args, **kwargs):
    '''This function serves to macro the creation of a rawdata reference'''
    desc = h3_meta_rawdata_ref(*args, **kwargs)
    desc["SIZE"] = 20
    desc["INCLUDE"] = rawdata_ref_struct
    desc["TYPE"] = H3RawdataRef


def h3_dependency(*args, **kwargs):
    '''This function serves to macro the creation of a tag dependency'''
    desc = h3_meta_dependency(*args, **kwargs)
    desc["SIZE"] = 16
    desc["INCLUDE"] = tag_ref_struct
    desc["TYPE"] = H3TagIndexRef


def h3_blam_header(tagid, version=1):
    '''This function serves to macro the creation of a tag header'''
    header_desc = dict(h3_tag_header)
    header_desc[1] = dict(header_desc[1])
    header_desc[5] = dict(header_desc[5])
    header_desc[1][DEFAULT] = tagid
    header_desc[5][DEFAULT] = version
    return header_desc

# Because halo 3 maps are big endian, these are swapped around.
# I guess it actually is a UInt32 masked off as 2 UInt16's
h3_tag_id_struct = QStruct("id",
    UInt16("table index", DEFAULT=0xFFFF),
    UInt16("tag table index", DEFAULT=0xFFFF),
    VISIBLE=False, EDITABLE=False
    )


valid_h3_tags = h3_tag_class(*h3_tag_class_fcc_to_ext.keys())


# ###########################################################################
# The order of element in all the enumerators is important(DONT SHUFFLE THEM)
# ###########################################################################

#Shared Enumerator options
old_materials_list = materials_list
# old materials list that is referenced in tags, but seems to be unused
del materials_list


# Descriptors
h3_tag_header = Struct("blam_header",
    Pad(36),
    UEnum32("tag class",
        GUI_NAME="tag class", INCLUDE=valid_h3_tags, EDITABLE=False
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
        ("halo3", 'BLM!'),
        DEFAULT='BLM!', EDITABLE=False
        ),
    VISIBLE=False, SIZE=64
    )


h3_meta_tag_index_ref_struct = H3MetaTagIndexRef('h3 meta dependency',
    valid_h3_tags,
    h3_tag_id_struct,
    ORIENT='h'
    )

h3_meta_reflexive_struct = H3MetaReflexive('h3 meta reflexive',
    SInt32("size", VISIBLE=False),
    UInt32("pointer", VISIBLE=False, DEFAULT=0xFFFFFFFF),
    )

h3_meta_rawdata_ref_struct = H3MetaRawdataRef('h3 meta rawdata ref', 
    SInt32("size", GUI_NAME="", SIDETIP="bytes", EDITABLE=False),
    UInt32("pointer", VISIBLE=False, DEFAULT=0xFFFFFFFF),
    ORIENT='h'
    )

# these structs replace the above ones when used outside a map
h3_tag_index_ref_struct = H3TagIndexRef('dependency',
    valid_h3_tags,
    SInt32("path pointer", VISIBLE=False, EDITABLE=False),
    SInt32("path length", MAX=243, VISIBLE=False, EDITABLE=False),
    h3_tag_id_struct,
    ORIENT='h'
    )

h3_reflexive_struct = H3Reflexive('reflexive',
    SInt32("size", VISIBLE=False),
    UInt32("pointer", VISIBLE=False, DEFAULT=0xFFFFFFFF),
    UInt32("id", VISIBLE=False),  # 0 in meta it seems
    )

h3_rawdata_ref_struct = H3RawdataRef('rawdata ref', 
    SInt32("size", GUI_NAME="", SIDETIP="bytes", EDITABLE=False),
    Bool32("flags",
        "data in resource map",
        VISIBLE=False,
        ),
    UInt32("raw pointer", VISIBLE=False),  # doesnt use magic
    UInt32("pointer", VISIBLE=False, DEFAULT=0xFFFFFFFF),
    UInt32("id", VISIBLE=False),
    ORIENT='h'
    )
