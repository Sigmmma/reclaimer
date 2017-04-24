from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

message_element = QStruct("message element",
    SInt8("type"), SInt8("data"),
    SIZE=2, ORIENT='h',
    )

message = Struct("message",
    ascii_str32("name"),
    SInt16("text start", GUI_NAME="start index into text blob"),
    SInt16("message index", GUI_NAME="start index of message block"),
    SInt8("panel count"),
    SIZE=64,
    )

hmt__body = Struct("tagdata",
    rawtext_ref("string", FlUTF16StrData, max_size=65536),
    reflexive("message elements", message_element, 8192),
    reflexive("messages", message, 1024, DYN_NAME_PATH='.name'),
    SIZE=128,
    )


def get():
    return hmt__def

hmt__def = TagDef("hmt ",
    blam_header('hmt '),
    hmt__body,

    ext=".hud_message_text", endian=">", tag_cls=HekTag
    )
