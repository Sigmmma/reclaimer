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

hmt__body = Struct("Data",
    RawDataRef("string",
        INCLUDE=Raw_Data_Ref_Struct,
        CHILD=FlUTF16StrData("raw string data", SIZE=".Count")
        ),
    Reflexive("message elements",
        INCLUDE=Reflexive_Struct,
        CHILD=Array("message elements array",
            SIZE=".Count", SUB_STRUCT=message_element
            ),
        ),
    Reflexive("messages" ,
        INCLUDE=Reflexive_Struct,
        CHILD=Array("messages array",
            SIZE=".Count", SUB_STRUCT=message)
        ),
    SIZE=128,
    )


def get():
    return hmt__def

hmt__def = TagDef(
    com( {1:{DEFAULT:"hmt " }}, Tag_Header),
    hmt__body,
    
    NAME="hud_message_text",
    
    ext=".hud_message_text", def_id="hmt ", endian=">"
    )
