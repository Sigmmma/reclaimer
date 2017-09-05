from ..common_descs import *

# ###########################################################################
# The order of element in all the enumerators is important(DONT SHUFFLE THEM)
# ###########################################################################

#Shared Enumerator options
materials_list = (
    "unknown1",
    "unknown2",
    "unknown3",
    "unknown4",
    "unknown5",
    "unknown6",
    "unknown7",
    "unknown8",
    "unknown9",
    "unknown10",
    "unknown11",
    "unknown12",
    "unknown13",
    "unknown14",
    "unknown15",
    "unknown16",
    "unknown17",
    "unknown18",
    "unknown19",
    "unknown20",
    "unknown21",
    "unknown22",
    "unknown23",
    "unknown24",
    "unknown25",
    "unknown26",
    "unknown27",
    "unknown28",
    "unknown29",
    "unknown30",
    "unknown31",
    "unknown32",
    "unknown33",
    "unknown34",
    "unknown35",
    )
actor_types = (
    "unknown1",
    "unknown2",
    "unknown3",
    "unknown4",
    "unknown5",
    "unknown6",
    "unknown7",
    "unknown8",
    "unknown9",
    "unknown10",
    "unknown11",
    "unknown12",
    "unknown13",
    "unknown14",
    "unknown15",
    "unknown16",
    )
damage_category = (
    "unknown1",
    "unknown2",
    "unknown3",
    "unknown4",
    "unknown5",
    "unknown6",
    "unknown7",
    "unknown8",
    "unknown9",
    "unknown10",
    "unknown11",
    "unknown12",
    "unknown13",
    )
grenade_types = (
    'unknown1',
    'unknown2',
    'unknown3',
    'unknown4',
    )

#Tag class specific enumerators
unit_teams = (
    "none",
    "player",
    "unknown1",
    "unknown2",
    "unknown3",
    "unknown4",
    "unknown5",
    "unknown6",
    "unknown7",
    "unknown8",
    )
vehicle_types = (
    "unknown1",
    "unknown2",
    "unknown3",
    "unknown4",
    "unknown5",
    "unknown6",
    "unknown7",
    )
weapon_types = (
    "unknown1",
    "unknown2",
    "unknown3",
    "unknown4",
    "unknown5",
    )

damage_modifiers = QStruct("damage modifiers",
    *(float_zero_to_inf(material_name) for material_name in materials_list)
    )


def tag_class_stubbs(*args):
    classes = []
    for four_cc in args:
        classes.append((tag_class_fcc_to_ext_stubbs[four_cc], four_cc))

    return UEnum32(
        'tag_class',
        *(tuple(classes) + (("NONE", 0xffffffff),) ),
        DEFAULT=0xffffffff, GUI_NAME=''
        )


def dependency_stubbs(name='tag ref', valid_ids=None):
    '''This function serves to macro the creation of a tag dependency'''
    if isinstance(valid_ids, tuple):
        valid_ids = tag_class_stubbs(*valid_ids)
    elif isinstance(valid_ids, str):
        valid_ids = tag_class_stubbs(valid_ids)
    elif valid_ids is None:
        valid_ids = valid_tags_stubbs

    return TagIndexRef(name,
        valid_ids,
        UInt32("path pointer", VISIBLE=False, EDITABLE=False),
        UInt32("path length", MAX=243, VISIBLE=False, EDITABLE=False),
        tag_id_struct,

        STEPTREE=HaloRefStr(
            "filepath", SIZE=tag_ref_size, GUI_NAME="", MAX=244),
        ORIENT='h'
        )


def blam_header_stubbs(tagid, version=1):
    '''This function serves to macro the creation of a tag header'''
    header_desc= dict(tag_header_stubbs)
    header_desc[1] = dict(header_desc[1])
    header_desc[5] = dict(header_desc[5])
    header_desc[1][DEFAULT] = tagid
    header_desc[5][DEFAULT] = version
    return header_desc


valid_tags_os = tag_class_stubbs(*tag_class_fcc_to_ext_stubbs.keys())
