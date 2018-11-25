from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


wgtz_screen_widget = Struct("screen_widgets",
    dependency("widget"),
    ENDIAN=">", SIZE=16
    )


wgtz_meta_def = BlockDef("wgtz",
    dependency("shared_ui_globals"),
    dependency("editable_settings"),
    dependency("matchmaking_hopper_strings"),
    reflexive("screen_widgets", wgtz_screen_widget),
    TYPE=Struct, ENDIAN=">", SIZE=60
    )