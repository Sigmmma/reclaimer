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
     xyz_float, xy_float, argb_float, rgb_float, rgb_byte, argb_byte,\
     ijkw_float, ijk_float, ij_float, yp_float, ypr_float,\
     compressed_normal_32, materials_list


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


def h2_tagdata_switch(*args, **kwargs):
    '''
    Each arg should conform to (desc, bsize, engine_id='BLM_', version=0)
    '''
    cases = {}
    assert len(args)
    for case in args:
        assert hasattr(case, '__len__') and len(case) in (2, 3, 4)
        engine_id = 'BLM_'
        version = 0
        if len(case) > 2:
            engine_id = case[2]
        if len(case) > 3:
            version = case[3]

        tagdata_desc = tbfd_container(
            "tagdata", (case[0], case[1], version), def_count=1)

        engine_name = engine_id_to_name[engine_id]
        if engine_id == 'BLM_':
            def_desc = tagdata_desc
        cases[engine_name] = tagdata_desc

    kwargs.setdefault(VISIBLE, False)
    kwargs.setdefault(EDITABLE, False)
    kwargs.setdefault(DEFAULT, def_desc)

    assert DEFAULT in kwargs

    return Switch("tagdata",
        CASES=cases, CASE='.blam_header.engine_id.enum_name', **kwargs)


def tbfd_container(name, *args, def_case=None, def_count=0, **kwargs):
    '''
    Each arg should conform to (desc, bsize, version=0)
    '''
    # I'm not 100% certain, but I'm very sure that
    # tbfd is an acronym for tag_block_field_definition

    # ############################################### #
    #               !!!!!WARNING!!!!!                 #
    # When the tag's engine_id is ambl, the FieldType #
    # of the version and bcount is actually UInt16    #
    # ############################################### #
    cases = {}
    for case in args:
        assert hasattr(case, '__len__') and len(case) > 1
        bsize = case[1]
        version = 0
        if len(case) > 2:
            version = case[2]

        if def_case is None:
            def_case = (version, bsize)

        cases[(version, bsize)] = case[0]

    if def_case is not None:
        if isinstance(def_case, int):
            def_case = (0, def_case)
        else:
            assert hasattr(def_case, '__len__') and len(def_case)
            if len(def_case) == 1:
                def_case = (0, ) + tuple(def_case)

        def_desc = cases[def_case]
        kwargs.setdefault(DEFAULT, def_desc)

    return TBFDContainer("%s tbfd" % name,
        QStruct("header",
            UInt32("sig", DEFAULT='tbfd'),
            UInt32("version", DEFAULT=def_case[0]),
            UInt32("bcount", DEFAULT=def_count),
            UInt32("bsize", DEFAULT=def_case[1]),
            VISIBLE=False, EDITABLE=False
            ),
        Switch(name,
            CASES=cases, CASE=lambda *a, parent=None, **kw: (
                parent.header.version, parent.header.bsize)),
        **kwargs
        )


def h2v_tag_class(*args, **kwargs):
    '''
    A macro for creating a tag_class enum desc with the
    enumerations set to the provided tag_class fcc's.
    '''
    classes = []
    for four_cc in args:
        classes.append((h2v_tag_class_fcc_to_ext[four_cc], four_cc))

    return UEnum32(
        'tag_class',
        *(tuple(sorted(classes)) + (("NONE", 0xffffffff),) ),
        DEFAULT=0xffffffff, GUI_NAME='', WIDGET_WIDTH=20, **kwargs
        )


def h2_reflexive(name, *args, def_case=None, names=None,
                 max_count=MAX_REFLEXIVE_COUNT, **desc):
    '''
    This function serves to macro the creation of a reflexive
    Each arg should conform to (desc, bsize, version=0)
    '''

    dyn_name_path = desc.pop(DYN_NAME_PATH, None)
    substruct_name = ''
    cases = []

    if names:
        if isinstance(names, str):
            names = (names, )
        name_map = {}
        for i in range(len(names)):
            e_name = BlockDef.str_to_name(None, names[i])
            name_map[e_name] = i

    for case in args:
        case_desc = case[0]
        if not substruct_name:
            substruct_name = case_desc.get("NAME", '')

        array_desc = Array(substruct_name + " array",
            SIZE="..size", MAX=max_count,
            SUB_STRUCT=case_desc, WIDGET=ReflexiveFrame
            )
        if dyn_name_path is not None:
            array_desc[STEPTREE][DYN_NAME_PATH] = dyn_name_path
        if names is not None:
            array_desc[NAME_MAP] = names

        cases.append((array_desc, ) + case[1:])

    desc.update(
        INCLUDE=h2_reflexive_struct,
        STEPTREE=tbfd_container(substruct_name, *cases, def_case=def_case)
        )

    return H2Reflexive(name, **desc)


def h2_rawdata_ref(name, f_type=Rawdata, max_size=None, widget=None):
    '''This function serves to macro the creation of a rawdata reference'''
    ref_struct = dict(h2_rawdata_ref_struct)
    if max_size is not None:
        ref_struct[0] = dict(ref_struct[0])
        ref_struct[0][MAX] = max_size

    kwargs = {}
    if widget is not None:
        kwargs[WIDGET] = widget

    return H2RawdataRef(name,
        INCLUDE=ref_struct,
        STEPTREE=f_type("data", GUI_NAME="", SIZE=".size", **kwargs))


def h2v_dependency(name='tag ref', valid_ids=None):
    '''This function serves to macro the creation of a tag dependency'''
    if isinstance(valid_ids, tuple):
        valid_ids = h2v_tag_class(*valid_ids)
    elif isinstance(valid_ids, str):
        valid_ids = h2v_tag_class(valid_ids)
    elif valid_ids is None:
        valid_ids = valid_h2v_tags

    return H2TagIndexRef(name,
        valid_ids,
        BSInt32("path pointer", VISIBLE=False, EDITABLE=False),
        BSInt32("path length", MAX=243, VISIBLE=False, EDITABLE=False),
        BUInt32("id", DEFAULT=0xFFFFFFFF, VISIBLE=False, EDITABLE=False),

        STEPTREE=HaloRefStr(
            "filepath", SIZE=tag_ref_size, GUI_NAME="", MAX=234),  # 10 < Halo1
        ORIENT='h'
        )


def h2v_blam_header(tagid, version=1):
    '''This function serves to macro the creation of a tag header'''
    header_desc = dict(h2v_tag_header)
    header_desc[1] = dict(header_desc[1])
    header_desc[5] = dict(header_desc[5])
    header_desc[1][DEFAULT] = tagid
    header_desc[5][DEFAULT] = version
    return header_desc


valid_h2v_tags = h2v_tag_class(*h2v_tag_class_fcc_to_ext.keys())


# ###########################################################################
# The order of element in all the enumerators is important(DONT SHUFFLE THEM)
# ###########################################################################

#Shared Enumerator options
old_materials_list = materials_list
# old materials list that is referenced in tags, but seems to be unused
del materials_list


# Descriptors
h2v_tag_header = Struct("blam_header",
    Pad(36),
    UEnum32("tag class",
        GUI_NAME="tag class", INCLUDE=valid_h2v_tags, EDITABLE=False
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

# This is the descriptor used wherever a tag references a rawdata chunk
h2_rawdata_ref_struct = H2RawdataRef('rawdata ref', 
    SInt32("size", EDITABLE=False, GUI_NAME="", SIDETIP="bytes"),
    SInt32("unknown", EDITABLE=False, VISIBLE=False),
    SInt32("raw pointer", EDITABLE=False, VISIBLE=False),
    SInt32("pointer", EDITABLE=False, VISIBLE=False, DEFAULT=-1),
    SInt32("id", EDITABLE=False, VISIBLE=False),
    ORIENT='h'
    )

# This is the descriptor used wherever a tag reference a reflexive.
# The STEPTREE of a h2_reflexive_struct should be a tbfd_struct.
h2_reflexive_struct = H2Reflexive('reflexive',
    BSInt32("size", EDITABLE=False, VISIBLE=False),
    BSInt32("pointer", EDITABLE=False, VISIBLE=False, DEFAULT=-1),  # random
    BUInt32("id", EDITABLE=False, VISIBLE=False),  # 0 in meta it seems
    )


# This is the descriptor used wherever a tag references another tag
h2v_tag_index_ref_struct = h2v_dependency()
