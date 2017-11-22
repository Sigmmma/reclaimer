from ..common_descs import *
from .constants import *


def sr_tag_class(*args, **kwargs):
    '''
    A macro for creating a tag_class enum desc with the
    enumerations set to the provided tag_class fcc's.
    '''
    classes = []
    default = 0xffffffff
    for four_cc in args:
        classes.append((sr_tag_class_fcc_to_ext[four_cc], four_cc))

    if len(classes) == 1:
        default = classes[0][1]

    return UEnum32(
        'tag_class',
        *(tuple(sorted(classes)) + (("NONE", 0xffffffff),) ),
        DEFAULT=default, GUI_NAME='', WIDGET_WIDTH=20, **kwargs
        )


def dependency(name='tag ref', valid_ids=None, **kwargs):
    '''This function serves to macro the creation of a tag dependency'''
    if isinstance(valid_ids, tuple):
        valid_ids = sr_tag_class(*valid_ids)
    elif isinstance(valid_ids, str):
        valid_ids = sr_tag_class(valid_ids)
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


sr_valid_tags = sr_tag_class(*sr_tag_class_fcc_to_ext.keys())


# Descriptors
sr_tag_header = Struct("blam header",
    Pad(36),
    UEnum32("tag class",
        GUI_NAME="tag class", INCLUDE=sr_valid_tags, EDITABLE=False
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
        ("shadowrun_xbox", 'sr_x'),
        DEFAULT='sr_x', EDITABLE=False
        ),
    VISIBLE=False, SIZE=64, ENDIAN=">"  # KEEP THE ENDIAN SPECIFICATION
    )
