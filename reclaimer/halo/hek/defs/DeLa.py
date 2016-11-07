from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

# TYPING OUT THESE THREE ENUMERATORS WAS THE BIGGEST PAIN
# IN THE ASS PART OF WRITING ANY OF THESE TAG DEFINITIONS
game_data_inputs = ()
event_types = ()
event_functions = ()

widget_bounds = QStruct("",
    BSInt16("t"), BSInt16("l"), BSInt16("b"),  BSInt16("r"),
    )

game_data_input = Struct("game data input",
    BSEnum16("function", *game_data_inputs),
    SIZE=36
    )

event_handler = Struct("event handler",
    BBool32('flags',
        "close current widget",
        "close other widget",
        "close all widgets",
        "open widget",
        "reload self",
        "reload other widget",
        "give focus to widget",
        "run function",
        "replace self with widget",
        "go back to previous widget",
        "run scenario script",
        "try to branch on failure",
        ),
    BSEnum16("event type", *event_types),
    BSEnum16("function", *event_functions),
    dependency("widget tag", "DeLa"),
    dependency("sound effect", "snd!"),
    ascii_str32("script"),
    SIZE=72
    )

s_and_r_reference = Struct("search and replace reference",
    ascii_str32("search string"),
    BSEnum16("replace function",
        "NULL",
        "widgets controller",
        "build number",
        "pid",
        ),
    SIZE=34
    )

conditional_widget = Struct("conditional widget",
    dependency("widget tag", "DeLa"),
    ascii_str32("name"),  # UNUSED
    BBool32("flags",
        "load if event handler function fails",
        ),
    BSInt16("custom controller index"),  # UNUSED
    SIZE=80
    )

child_widget = Struct("child widget",
    dependency("widget tag", "DeLa"),
    ascii_str32("name"),  # UNUSED
    BBool32("flags",
        "use custom controller index",
        ),
    BSInt16("custom controller index"),
    BSInt16("vertical offset"),
    BSInt16("horizontal offset"),
    SIZE=80
    )

DeLa_body = Struct("tagdata",
    BSEnum16("widget type",
        "container",
        "text box",
        "spinner list",
        "column list",
        "game model",  # not implemented
        "movie",  # not implemented
        "custom"  # not implemented
        ),
    BSEnum16("controller index",
        "player 1",
        "player 2",
        "player 3",
        "player 4",
        "any player"
        ),
    ascii_str32("name"),
    QStruct("bounds", INCLUDE=widget_bounds),
    BBool32('flags',
        "pass unhandled events to focused child",
        "pause game time",
        "flash background bitmap",
        "dpad up/down tabs thru children",
        "dpad left/right tabs thru children",
        "dpad up/down tabs thru list items",
        "dpad left/right tabs thru list items",
        "dont focus a specific child widget",
        "pass unhandled events to all children",
        "return to main menu if no history",
        "always use tag controller index",
        "always use nifty render fx",
        "dont push history",
        "force handle mouse"
        ),
    BSInt32("milliseconds to auto close"),
    BSInt32("milliseconds to auto close fade time"),
    dependency("background bitmap", "bitm"),

    reflexive("game data inputs", game_data_input, 64),
    reflexive("event handlers", event_handler, 32),
    reflexive("search and replace references", s_and_r_reference, 32),

    Pad(128),
    Struct("text box",
        dependency("text label unicode strings list", "ustr"),
        dependency("text font", "font"),
        QStruct("text color", INCLUDE=argb_float),
        BSEnum16("justification",
            "left",
            "right",
            "center",
            ),
        BBool32("flags",
            "editable",
            "password",
            "flashing",
            "dont do that weird focus test",
            ),

        Pad(12),
        BSInt16("string list index"),
        BSInt16("horizontal offset"),
        BSInt16("vertical offset")
        ),

    Pad(28),
    Struct("list items",
        BBool32("flags",
            "list items generated in code",
            "list items from string list tag",
            "list items only one tooltip",
            "list single preview no scroll"
            )
        ),

    Struct("spinner list",
        dependency("list header bitmap", "bitm"),
        dependency("list footer bitmap", "bitm"),
        QStruct("header bounds", INCLUDE=widget_bounds),
        QStruct("footer bounds", INCLUDE=widget_bounds)
        ),

    Pad(32),
    Struct("column list",
        dependency("extended description widget", "DeLa")
        ),

    Pad(288),
    reflexive("conditional widgets", conditional_widget, 32),

    Pad(256),
    reflexive("child widgets", child_widget, 32),

    SIZE=1004
    )

def get():
    return DeLa_def

DeLa_def = TagDef("DeLa",
    blam_header('DeLa'),
    DeLa_body,

    ext=".ui_widget_definition", endian=">"
    )
