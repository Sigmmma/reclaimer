from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef
from .grhi import messaging_information, multitex_overlay, hud_background

attached_state = BSEnum16("state attached to",
    "total ammo",
    "loaded ammo",
    "heat",
    "age",
    "secondary weapon total ammo",
    "secondary weapon loaded ammo",
    "distance to target",
    "elevation to target",
    )

use_on_map_type = BSEnum16("can use on map type",
    "any",
    "solo",
    "multiplayer",
    )

static_element = Struct("static element",
    attached_state,
    Pad(2),
    use_on_map_type,

    Pad(30),
    QStruct("anchor offset",
        BSInt16("x"), BSInt16("y"), ORIENT='h',
        ),
    BFloat("width scale"),
    BFloat("height scale"),
    BBool16("scaling flags", *hud_scaling_flags),

    Pad(22),
    dependency("interface bitmap", "bitm"),
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

    Pad(4),
    BSInt16("sequence index"),

    Pad(2),
    reflexive("multitex overlays", multitex_overlay, 30),
    SIZE=180
    )

meter_element = Struct("meter element",
    attached_state,
    Pad(2),
    use_on_map_type,

    Pad(30),
    QStruct("anchor offset",
        BSInt16("x"), BSInt16("y"), ORIENT='h',
        ),
    BFloat("width scale"),
    BFloat("height scale"),
    BBool16("scaling flags", *hud_scaling_flags),

    Pad(22),
    dependency("meter bitmap", "bitm"),
    #QStruct("color at meter minimum", INCLUDE=xrgb_byte),
    #QStruct("color at meter maximum", INCLUDE=xrgb_byte),
    #QStruct("flash color", INCLUDE=xrgb_byte),
    #QStruct("empty color", INCLUDE=argb_byte),
    UInt32("color at meter minimum", INCLUDE=xrgb_uint32),
    UInt32("color at meter maximum", INCLUDE=xrgb_uint32),
    UInt32("flash color", INCLUDE=xrgb_uint32),
    UInt32("empty color", INCLUDE=argb_uint32),
    Bool8("flags", *hud_panel_meter_flags),
    SInt8("minimum meter value"),
    BSInt16("sequence index"),
    SInt8("alpha multiplier"),
    SInt8("alpha bias"),
    BSInt16("value scale"),
    BFloat("opacity"),
    BFloat("translucency"),
    #QStruct("disabled color", INCLUDE=argb_byte),
    UInt32("disabled color", INCLUDE=argb_uint32),
    SIZE=180
    )

number_element = Struct("number element",
    attached_state,
    Pad(2),
    use_on_map_type,

    Pad(30),
    QStruct("anchor offset",
        BSInt16("x"), BSInt16("y"), ORIENT='h',
        ),
    BFloat("width scale"),
    BFloat("height scale"),
    BBool16("scaling flags", *hud_scaling_flags),

    Pad(22),
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

    Pad(4),
    SInt8("maximum number of digits"),
    Bool8("flags",
        "show leading zeros",
        "only show when zoomed",
        "draw a trailing m",
        ),
    SInt8("number of fractional digits"),
    Pad(1),

    Pad(12),
    BBool16("weapon specific flags",
        "divide number by magazine size"
        ),
    SIZE=160
    )

crosshair_overlay = Struct("crosshair overlay",
    QStruct("anchor offset",
        BSInt16("x"), BSInt16("y"), ORIENT='h',
        ),
    BFloat("width scale"),
    BFloat("height scale"),
    BBool16("scaling flags", *hud_scaling_flags),

    Pad(22),
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

    Pad(4),
    BSInt16("frame rate", UNIT_SCALE=per_sec_unit_scale),
    BSInt16("sequence index"),
    BBool32("type",
        "flashes when active",
        "not a sprite",
        "show only when zoomed",
        "show sniper data",
        "hide area outside reticle",
        "one zoom level",
        "dont show when zoomed",
        ),
    SIZE=108
    )

overlay = Struct("overlay",
    QStruct("anchor offset",
        BSInt16("x"), BSInt16("y"), ORIENT='h',
        ),
    BFloat("width scale"),
    BFloat("height scale"),
    BBool16("scaling flags", *hud_scaling_flags),

    Pad(22),
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

    Pad(4),
    BSInt16("frame rate", UNIT_SCALE=per_sec_unit_scale),
    Pad(2),
    BSInt16("sequence index"),
    BBool16("type",
        "show on flashing",
        "show on empty",
        "show on reload/overheating",
        "show on default",
        "show always",
        ),
    BBool32("flags",
        "flashes when active",
        ),
    SIZE=136
    )

crosshair = Struct("crosshair",
    BSEnum16("crosshair type",
        "aim",
        "zoom",
        "charge",
        "should reload",
        "flash heat",
        "flash total ammo",
        "flash battery",
        "reload/overheat",
        "flash when firing and no ammo",
        "flash when throwing grenade and no grenade",
        "low ammo and none left to reload",
        "should reload secondary trigger",
        "flash secondary total ammo",
        "flash secondary reload",
        "flash when firing secondary and no ammo",
        "low secondary ammo and none left to reload",
        "primary trigger ready",
        "secondary trigger ready",
        "flash when firing with depleted battery",
        ),
    Pad(2),
    use_on_map_type,

    Pad(30),
    dependency("crosshair bitmap", "bitm"),
    reflexive("crosshair overlays", crosshair_overlay, 16),
    SIZE=104
    )

overlay_element = Struct("overlay element",
    attached_state,
    Pad(2),
    use_on_map_type,

    Pad(30),
    dependency("overlay bitmap", "bitm"),
    reflexive("overlays", overlay, 16),
    SIZE=104
    )

screen_effect = Struct("screen effect",
    Pad(4),
    Struct("mask",
        Bool16("flags",
            "only when zoomed"
            ),
        Pad(18),
        dependency("fullscreen mask", "bitm"),
        dependency("splitscreen mask", "bitm")
        ),

    Pad(8),
    Struct("convolution",
        Bool16("flags",
            "only when zoomed"
            ),
        Pad(2),
        from_to_rad("fov in bounds"),  # radians
        QStruct("radius out bounds",
            INCLUDE=from_to, SIDETIP="pixels")  # pixels
        ),

    Pad(24),
    Struct("night vision",
        Bool16("flags",
            "only when zoomed",
            "connect to flashlight",
            "masked"
            ),
        BSInt16("script source", MIN=0, MAX=3, SIDETIP="[0,3]"),
        BFloat("intensity", MIN=0.0, MAX=1.0, SIDETIP="[0,1]")
        ),

    Pad(24),
    Struct("desaturation",
        Bool16("flags",
            "only when zoomed",
            "connect to flashlight",
            "additive",
            "masked"
            ),
        BSInt16("script source", MIN=0, MAX=3, SIDETIP="[0,3]"),
        BFloat("intensity", MIN=0.0, MAX=1.0, SIDETIP="[0,1]"),
        QStruct("tint", INCLUDE=rgb_float)
        ),
    SIZE=184
    )

wphi_body = Struct("tagdata",
    dependency("child hud", "wphi"),
    Struct("flash cutoffs",
        BBool16("flags",
            "use parent hud flashing parameters"
            ),
        Pad(2),
        BSInt16("total ammo cutoff"),
        BSInt16("loaded ammo cutoff"),
        BSInt16("heat cutoff"),
        BSInt16("age cutoff"),
        ),

    Pad(32),
    BSEnum16("anchor", *hud_anchors),
    
    Pad(34),
    reflexive("static elements", static_element, 16),
    reflexive("meter elements", meter_element, 16),
    reflexive("number elements", number_element, 16),
    reflexive("crosshairs", crosshair, 19),
    reflexive("overlay elements", overlay_element, 16),

    Pad(16),
    reflexive("screen effect", screen_effect, 1),

    Pad(132),
    messaging_information,
    SIZE=380,
    )

    
def get():
    return wphi_def

wphi_def = TagDef("wphi",
    blam_header("wphi", 2),
    wphi_body,

    ext=".weapon_hud_interface", endian=">", tag_cls=HekTag,
    )
