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


def tag_class_stubbs(*args, **kwargs):
    '''
    A macro for creating a tag_class enum desc with the
    enumerations set to the provided tag_class fcc's.
    '''
    classes = []
    default = 0xffffffff
    for four_cc in args:
        classes.append((tag_class_fcc_to_ext_stubbs[four_cc], four_cc))

    if len(classes) == 1:
        default = classes[0][1]

    return UEnum32(
        'tag_class',
        *(tuple(sorted(classes)) + (("NONE", 0xffffffff),) ),
        DEFAULT=default, GUI_NAME='', WIDGET_WIDTH=20, **kwargs
        )


def dependency_stubbs(name='tag ref', valid_ids=None, **kwargs):
    '''This function serves to macro the creation of a tag dependency'''
    if isinstance(valid_ids, tuple):
        valid_ids = tag_class_stubbs(*valid_ids)
    elif isinstance(valid_ids, str):
        valid_ids = tag_class_stubbs(valid_ids)
    elif valid_ids is None:
        valid_ids = valid_tags

    return TagRef(name,
        valid_ids,
        INCLUDE=tag_ref_struct,
        STEPTREE=StrTagRef(
            "filepath", SIZE=tag_ref_str_size, GUI_NAME="", MAX=234),
        **kwargs
        )


def blam_header_stubbs(tagid, version=1):
    '''This function serves to macro the creation of a tag header'''
    header_desc= dict(tag_header_stubbs)
    header_desc[1] = dict(header_desc[1])
    header_desc[5] = dict(header_desc[5])
    header_desc[1][DEFAULT] = tagid
    header_desc[5][DEFAULT] = version
    return header_desc


valid_tags = tag_class_stubbs(*tag_class_fcc_to_ext_stubbs.keys())


# Descriptors
tag_header_stubbs = Struct("blam header",
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
