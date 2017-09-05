from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

button_icon = Struct("button icon",
    SInt16("sequence index"),
    SInt16("width offset"),
    QStruct("offset from reference corner",
        SInt16("x"), SInt16("y"), ORIENT='h'
        ),
    #QStruct("override icon color", INCLUDE=argb_byte),
    UInt32("override icon color", INCLUDE=argb_uint32),
    SInt8("frame rate", MIN=0, MAX=30, UNIT_SCALE=per_sec_unit_scale),
    Bool8("flags",
        "use text from string_list instead",
        "override default color",
        "width offset is absolute icon width",
        ),
    SInt16("text index"),
    SIZE=16
    )

waypoint_arrow = Struct("waypoint arrow",
    ascii_str32("name"),

    Pad(8),
    #QStruct("color", INCLUDE=xrgb_byte),
    UInt32("color", INCLUDE=xrgb_uint32),
    Float("opacity"),
    Float("translucency"),
    SInt16("on screen sequence index"),
    SInt16("off screen sequence index"),
    SInt16("occluded sequence index"),

    Pad(18),
    Bool32("flags",
        "dont rotate when pointing offscreen"
        ),
    SIZE=104
    )


messaging_parameters = Struct("messaging parameters",
    SEnum16("anchor", *hud_anchors),

    Pad(34),
    QStruct("anchor offset",
        SInt16("x"), SInt16("y"), ORIENT='h'
        ),
    Float("width scale"),
    Float("height scale"),
    Bool16("scaling flags", *hud_scaling_flags),

    Pad(22),
    dependency("single player font", "font"),
    dependency("multi player font", "font"),
    float_sec("up time"),
    float_sec("fade time"),
    QStruct("icon color", INCLUDE=argb_float),
    QStruct("text color", INCLUDE=argb_float),
    Float("text spacing"),
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
    SInt16("number of flashes"),
    Bool16("flash flags", *hud_flash_flags),
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
    SInt16("number of flashes"),
    Bool16("flash flags", *hud_flash_flags),
    float_sec("flash length"),
    #QStruct("disabled color", INCLUDE=argb_byte),
    UInt32("disabled color", INCLUDE=argb_uint32),
    SInt16("uptime ticks", UNIT_SCALE=sec_unit_scale),
    SInt16("fade ticks", UNIT_SCALE=sec_unit_scale),
    SIZE=32
    )

waypoint_parameters = Struct("waypoint parameters",
    Float("top offset"),
    Float("bottom offset"),
    Float("left offset"),
    Float("right offset"),

    Pad(32),
    dependency("arrow bitmaps", "bitm"),
    SIZE=64
    )

hud_globals = Struct("hud globals",
    Float("hud scale in multiplayer"),

    Pad(256),
    dependency("default weapon hud", "wphi"),
    Float("motion sensor range"),
    Float("motion sensor velocity sensitivity"),
    Float("motion sensor scale", DEFAULT=32.0),  # DONT TOUCH(why?)
    QStruct("default chapter title bounds",
        SInt16("t"), SInt16("l"), SInt16("b"), SInt16("r"), ORIENT='h'
        ),
    SIZE=340
    )

hud_damage_indicators = Struct("hud damage indicators",
    SInt16("top offset"),
    SInt16("bottom offset"),
    SInt16("left offset"),
    SInt16("right offset"),

    Pad(32),
    dependency("indicator bitmap", "bitm"),
    SInt16("sequence index"),
    SInt16("multiplayer sequence index"),
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
    SInt16("number of flashes"),
    Bool16("flash flags", *hud_flash_flags),
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
    SInt16("number of flashes"),
    Bool16("flash flags", *hud_flash_flags),
    float_sec("flash length"),
    #QStruct("disabled color", INCLUDE=argb_byte),
    UInt32("disabled color", INCLUDE=argb_uint32),
    SIZE=32
    )

misc_hud_crap = Struct("misc hud crap",
    SInt16("loading begin text"),
    SInt16("loading end text"),
    SInt16("checkpoint begin text"),
    SInt16("checkpoint end text"),
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
