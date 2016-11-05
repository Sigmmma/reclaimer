from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

messaging_information = Struct("messaging information",
    BSInt16("sequence index"),
    BSInt16("width offset"),
    QStruct("offset from reference corner",
        BSInt16("x"),
        BSInt16("y")
        ),
    QStruct("override icon color", INCLUDE=argb_byte),
    SInt8("frame rate", MIN=0, MAX=30),
    Bool8("flags",
        "use text from string_list instead",
        "override default color",
        "width offset is absolute icon width",
        ),
    BSInt16("text index"),
    SIZE=64
    )

effector = Struct("effector",
    Pad(64),
    BSEnum16("destination type",
        "tint 0-1",
        "horizontal offset",
        "vertical offset",
        "fade 0-1",
        ),
    BSEnum16("destination",
        "geometry offset",
        "primary map",
        "secondary map",
        "tertiary map",
        ),
    BSEnum16("source",
        "player pitch",
        "player tangent",
        "player yaw",
        "weapon total ammo",
        "weapon loaded ammo",
        "weapon heat",
        "explicit",  # use low bound
        "weapon zoom level",
        ),

    Pad(2),
    QStruct("in bounds", INCLUDE=from_to),  # source units
    QStruct("out bounds", INCLUDE=from_to),  # pixels

    Pad(64),
    QStruct("tint color lower bound", INCLUDE=rgb_float),
    QStruct("tint color upper bound", INCLUDE=rgb_float),
    Struct("periodic functions", INCLUDE=anim_func_per_pha),
    SIZE=220
    )

multitex_overlay = Struct("multitex overlay",
    Pad(2),
    BSInt16("type"),
    BSEnum16("framebuffer blend func", *framebuffer_blend_functions),

    # Anchors
    Pad(34),
    BSEnum16("primary anchor", *multitex_anchors),
    BSEnum16("secondary anchor", *multitex_anchors),
    BSEnum16("tertiary anchor", *multitex_anchors),
    # Blending function
    BSEnum16("zero to one blend func", *blending_funcs),
    BSEnum16("one to two blend func", *blending_funcs),

    # Map scales
    Pad(2),
    QStruct("primary scale", INCLUDE=from_to),
    QStruct("secondary scale", INCLUDE=from_to),
    QStruct("tertiary scale", INCLUDE=from_to),
    # Map offsets
    QStruct("primary offset", INCLUDE=from_to),
    QStruct("secondary offset", INCLUDE=from_to),
    QStruct("tertiary offset", INCLUDE=from_to),

    # Maps
    dependency("primary map", valid_bitmaps),
    dependency("secondary map", valid_bitmaps),
    dependency("tertiary map", valid_bitmaps),
    BSEnum16("primary wrap mode", *multitex_wrap_modes),
    BSEnum16("secondary wrap mode", *multitex_wrap_modes),
    BSEnum16("tertiary wrap mode", *multitex_wrap_modes),

    Pad(186),
    reflexive("effectors", effector, 30),
    SIZE=480,
    )

total_grenades_numbers = Struct("totat grenades numbers",
    QStruct("anchor offset",
        BSInt16("x"),
        BSInt16("y"),
        ),
    BFloat("width scale"),
    BFloat("height scale"),
    BBool16("scaling flags", *hud_scaling_flags),

    Pad(22),
    QStruct("default color", INCLUDE=argb_byte),
    QStruct("flashing color", INCLUDE=argb_byte),
    BFloat("flash period"),
    BFloat("flash delay"),
    BSInt16("number of flashes"),
    BBool16("flash flags", *hud_flash_flags),
    BFloat("flash length"),
    QStruct("disabled color", INCLUDE=argb_byte),

    Pad(4),
    SInt8("maximum number of digits"),
    Bool8("flags",
        "show leading zeros",
        "only show when zoomed",
        "draw a trailing m",
        ),
    SInt8("number of fractional digits"),

    Pad(13),
    BSInt16("flash cutoff"),
    SIZE=88
    )

overlay = Struct("overlay",
    QStruct("anchor offset",
        BSInt16("x"),
        BSInt16("y"),
        ),
    BFloat("width scale"),
    BFloat("height scale"),
    BBool16("scaling flags", *hud_scaling_flags),

    Pad(22),
    QStruct("default color", INCLUDE=argb_byte),
    QStruct("flashing color", INCLUDE=argb_byte),
    BFloat("flash period"),
    BFloat("flash delay"),
    BSInt16("number of flashes"),
    BBool16("flash flags", *hud_flash_flags),
    BFloat("flash length"),
    QStruct("disabled color", INCLUDE=argb_byte),

    Pad(4),
    BFloat("frame rate"),
    BSInt16("sequence index"),
    BBool16("type",
        "show on flashing",
        "show on empty",
        "show on default",
        "show always",
        ),
    BBool32("flags",
        "flashes when active",
        ),

    SIZE=136
    )

warning_sound = Struct("warning sound",
    dependency("sound", ('lsnd', 'snd!')),
    BBool32("latched to",
        "low grenade sound",
        "no grenades left",
        "throw on no grenades",
        ),
    BFloat("scale"),
    SIZE=56
    )

# Use this with INCLUDE keywords since it will need to be named
hud_background = Struct("",
    QStruct("anchor offset",
        BSInt16("x"),
        BSInt16("y"),
        ),
    BFloat("width scale"),
    BFloat("height scale"),
    BBool16("scaling flags", *hud_scaling_flags),

    Pad(22),
    dependency("interface bitmap", valid_bitmaps),
    QStruct("default color", INCLUDE=argb_byte),
    QStruct("flashing color", INCLUDE=argb_byte),
    BFloat("flash period"),
    BFloat("flash delay"),
    BSInt16("number of flashes"),
    BBool16("flash flags", *hud_flash_flags),
    BFloat("flash length"),
    QStruct("disabled color", INCLUDE=argb_byte),

    Pad(4),
    BSInt16("sequence index"),

    Pad(2),
    reflexive("multitex overlays", multitex_overlay, 30),
    Pad(4),
    SIZE=104
    )

grhi_body = Struct("tagdata",
    BSEnum16("anchor", *hud_anchors),

    Pad(34),
    Struct("grenade hud background", INCLUDE=hud_background),
    Struct("total grenades",
        Struct("background", INCLUDE=hud_background),
        Struct("numbers", INCLUDE=total_grenades_numbers),
        dependency("overlay bitmap", valid_bitmaps),
        reflexive("overlays", overlay, 16),
        ),
    reflexive("warning sounds", warning_sound, 12),

    Pad(68),
    messaging_information,
    SIZE=504,
    )

    
def get():
    return grhi_def

grhi_def = TagDef("grhi",
    blam_header("grhi"),
    grhi_body,

    ext=".grenade_hud_interface", endian=">",
    )
