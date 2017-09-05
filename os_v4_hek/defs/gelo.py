from .yelo import *

gelo_body = Struct("tagdata",
    SInt16("version", DEFAULT=2),
    Bool16("flags",
        "hide health when zoomed",
        "hide shield when zoomed",
        "hide motion sensor when zoomed",
        "force game to use stun jumping penalty"
        ),
    SInt32("base address"),
    ascii_str32("mod name"),
    dependency_os("global explicit references", "tagc"),
    #dependency_os("chokin victim globals", "gelc"),
    Pad(16),  # removed chokin victim globals

    Pad(16),
    Pad(12), #reflexive("unknown1", void_desc),
    Pad(52),
    reflexive("scripted ui widgets", scripted_ui_widget, 128),

    Pad(12), #reflexive("unknown2", void_desc),
    Pad(20),
    reflexive("yelo scripting", yelo_scripting, 1),

    SIZE=288
    )

def get():
    return gelo_def

gelo_def = TagDef("gelo",
    blam_header_os('gelo', 2),
    gelo_body,

    ext=".project_yellow_globals", endian=">", tag_cls=HekTag
    )
