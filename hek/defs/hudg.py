from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

button_icon = Struct("button icon",
    BSInt16("sequence index"),
    BSInt16("width offset"),
    QStruct("offset from reference corner",
        BSInt16("x"), BSInt16("y"), ORIENT='h'
        ),
    #QStruct("override icon color", INCLUDE=argb_byte),
    UInt32("override icon color", INCLUDE=argb_uint32),
    SInt8("frame rate", MIN=0, MAX=30, UNIT_SCALE=per_sec_unit_scale),
    Bool8("flags",
        "use text from string_list instead",
        "override default color",
        "width offset is absolute icon width",
        ),
    BSInt16("text index"),
    SIZE=16
    )

waypoint_arrow = Struct("waypoint arrow",
    ascii_str32("name"),

    Pad(8),
    #QStruct("color", INCLUDE=xrgb_byte),
    UInt32("color", INCLUDE=xrgb_uint32),
    BFloat("opacity"),
    BFloat("translucency"),
    BSInt16("on screen sequence index"),
    BSInt16("off screen sequence index"),
    BSInt16("occluded sequence index"),

    Pad(18),
    BBool32("flags",
        "dont rotate when pointing offscreen"
        ),
    SIZE=104
    )


messaging_parameters = Struct("messaging parameters",
    BSEnum16("anchor", *hud_anchors),

    Pad(34),
    QStruct("anchor offset",
        BSInt16("x"), BSInt16("y"), ORIENT='h'
        ),
    BFloat("width scale"),
    BFloat("height scale"),
    BBool16("scaling flags", *hud_scaling_flags),

    Pad(22),
    dependency("single player font", "font"),
    dependency("multi player font", "font"),
    float_sec("up time"),
    float_sec("fade time"),
    QStruct("icon color", INCLUDE=argb_float),
    QStruct("text color", INCLUDE=argb_float),
    BFloat("text spacing"),
    dependency("item message text", "ustr"),
    dependency("icon bitmap", "bitm"),
    dependency("alternate icon text", "ustr"),
    SIZE=196
    )

hud_help_text_color = Struct("hud help text color",
    #QStruct("default color", INCLUDE=argb_byte),
    #QStruct("flashing color", INCLUDE=argb_byte),
    UInt32("default color", INCLUDE=argb_uint32),
    UInt32("flashing color", INCLUDE=argb_uint32),
    float_sec("flash period"),
    float_sec("flash delay"),
    BSInt16("number of flashes"),
    BBool16("flash flags", *hud_flash_flags),
    float_sec("flash length"),
    #QStruct("disabled color", INCLUDE=argb_byte),
    UInt32("disabled color", INCLUDE=argb_uint32),
    SIZE=32
    )

objective_colors = Struct("objective colors",
    #QStruct("default color", INCLUDE=argb_byte),
    #QStruct("flashing color", INCLUDE=argb_byte),
    UInt32("default color", INCLUDE=argb_uint32),
    UInt32("flashing color", INCLUDE=argb_uint32),
    float_sec("flash period"),
    float_sec("flash delay"),
    BSInt16("number of flashes"),
    BBool16("flash flags", *hud_flash_flags),
    float_sec("flash length"),
    #QStruct("disabled color", INCLUDE=argb_byte),
    UInt32("disabled color", INCLUDE=argb_uint32),
    BSInt16("uptime ticks", UNIT_SCALE=sec_unit_scale),
    BSInt16("fade ticks", UNIT_SCALE=sec_unit_scale),
    SIZE=32
    )

waypoint_parameters = Struct("waypoint parameters",
    BFloat("top offset"),
    BFloat("bottom offset"),
    BFloat("left offset"),
    BFloat("right offset"),

    Pad(32),
    dependency("arrow bitmaps", "bitm"),
    SIZE=64
    )

hud_globals = Struct("hud globals",
    BFloat("hud scale in multiplayer"),

    Pad(256),
    dependency("default weapon hud", "wphi"),
    BFloat("motion sensor range"),
    BFloat("motion sensor velocity sensitivity"),
    BFloat("motion sensor scale", DEFAULT=32.0),  # DONT TOUCH(why?)
    QStruct("default chapter title bounds",
        BSInt16("t"), BSInt16("l"), BSInt16("b"), BSInt16("r"), ORIENT='h'
        ),
    SIZE=340
    )

hud_damage_indicators = Struct("hud damage indicators",
    BSInt16("top offset"),
    BSInt16("bottom offset"),
    BSInt16("left offset"),
    BSInt16("right offset"),

    Pad(32),
    dependency("indicator bitmap", "bitm"),
    BSInt16("sequence index"),
    BSInt16("multiplayer sequence index"),
    #QStruct("color", INCLUDE=argb_byte),
    UInt32("color", INCLUDE=argb_uint32),
    SIZE=80
    )

time_running_out = Struct("time running out flash color",
    #QStruct("default color", INCLUDE=argb_byte),
    #QStruct("flashing color", INCLUDE=argb_byte),
    UInt32("default color", INCLUDE=argb_uint32),
    UInt32("flashing color", INCLUDE=argb_uint32),
    float_sec("flash period"),
    float_sec("flash delay"),
    BSInt16("number of flashes"),
    BBool16("flash flags", *hud_flash_flags),
    float_sec("flash length"),
    #QStruct("disabled color", INCLUDE=argb_byte),
    UInt32("disabled color", INCLUDE=argb_uint32),
    SIZE=32
    )

time_out = Struct("time out flash color",
    #QStruct("default color", INCLUDE=argb_byte),
    #QStruct("flashing color", INCLUDE=argb_byte),
    UInt32("default color", INCLUDE=argb_uint32),
    UInt32("flashing color", INCLUDE=argb_uint32),
    float_sec("flash period"),
    float_sec("flash delay"),
    BSInt16("number of flashes"),
    BBool16("flash flags", *hud_flash_flags),
    float_sec("flash length"),
    #QStruct("disabled color", INCLUDE=argb_byte),
    UInt32("disabled color", INCLUDE=argb_uint32),
    SIZE=32
    )

misc_hud_crap = Struct("misc hud crap",
    BSInt16("loading begin text"),
    BSInt16("loading end text"),
    BSInt16("checkpoint begin text"),
    BSInt16("checkpoint end text"),
    dependency("checkpoint", "snd!"),
    BytearrayRaw("unknown", SIZE=96, VISIBLE=False),
    SIZE=120
    )

hudg_body = Struct("tagdata",
    messaging_parameters,
    reflexive("button icons", button_icon, 18,
        "a button", "b button", "x button", "y button",
        "black button", "white button", "left trigger", "right trigger",
        "dpad up",  "dpad down", "dpad left", "dpad right", "start", "back",
        "left thumb button", "right thumb button", "left stick", "right stick"
        ),
    hud_help_text_color,
    dependency("hud messages", "hmt "),
    objective_colors,
    waypoint_parameters,
    reflexive("waypoint arrows", waypoint_arrow, 16, DYN_NAME_PATH='.name'),

    Pad(80),
    hud_globals,
    hud_damage_indicators,
    time_running_out,
    time_out,

    Pad(40),
    dependency("carnage report bitmap", "bitm"),
    misc_hud_crap,
    SIZE=1104
    )

    
def get():
    return hudg_def

hudg_def = TagDef("hudg",
    blam_header("hudg"),
    hudg_body,

    ext=".hud_globals", endian=">", tag_cls=HekTag,
    )
