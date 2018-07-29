from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

icon_types = (
    "a-button",
    "b-button",
    "x-button",
    "y-button",
    "black-button",
    "white-button",
    "left-trigger",
    "right-trigger",
    "dpad-up",
    "dpad-down",
    "dpad-left",
    "dpad-right",
    "start-button",
    "back-button",
    "left-thumb",
    "right-thumb",
    "left-stick",
    "right-stick",
    "action",
    "throw-grenade",
    "primary-trigger",
    "integrated-light",
    "jump",
    "use-equipment",
    "rotate-weapons",
    "rotate-grenades",
    "zoom",
    "crouch",
    "accept",
    "back",
    "move",
    "look",
    "custom-1",
    "custom-2",
    "custom-3",
    "custom-4",
    "custom-5",
    "custom-6",
    "custom-7",
    "custom-8",
    )

message_element = Struct("message element",
    UEnum8("type",
        "text",
        "icon",
        EDITABLE=False
        ),
    Union("data",
        CASE=".type.enum_name",
        CASES=dict(
            text=UEnum8("length",
                *({GUI_NAME: str(i), NAME: "_%s" % i} for i in range(256))),
            icon=UEnum8("icon_type",
                *({GUI_NAME: name, NAME: name} for name in icon_types)
                ),
            ),
        EDITABLE=False
        ),
    SIZE=2,
    )

message = Struct("message",
    ascii_str32("name"),
    SInt16("text start", GUI_NAME="start index into text blob"),
    SInt16("element index", GUI_NAME="start index of message block"),
    SInt8("element count"),
    SIZE=64,
    )

hmt__body = Struct("tagdata",
    rawtext_ref("string", FlStrUTF16Data, max_size=65536, EDITABLE=False),
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
