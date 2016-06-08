from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

message_element = Struct("message element",
    SInt8("type"),
    SInt8("data"),
    SIZE=2
    )

message = Struct("message",
    StrLatin1("name", SIZE=32),
    SInt16("text start", GUI_NAME="start index into text blob"),
    SInt16("message index", GUI_NAME="start index of message block"),
    SInt8("panel count"),
    SIZE=64,
    )

hmt__body = Struct("tagdata",
    rawdata_ref("string", FlUTF16StrData),
    reflexive("message elements", message_element),
    reflexive("messages", message),
    SIZE=128,
    )


def get():
    return hmt__def

hmt__def = TagDef(
    blam_header('hmt '),
    hmt__body,
    
    NAME="hud_message_text",
    
    ext=".hud_message_text", def_id="hmt ", endian=">"
    )
