from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef
from .grhi import multitex_overlay, hud_background

warning_sound = Struct("warning sound",
    dependency("sound", ('lsnd', 'snd!')),
    Bool32("latched to",
        "shield recharging",
        "shield recharged",
        "shield low",
        "shield empty",
        "health low",
        "health empty",
        "health minor damage",
        "health major damage",
        ),
    Float("scale"),
    SIZE=56
    )

shield_panel_meter = Struct("shield panel meter",
    QStruct("anchor offset",
        SInt16("x"), SInt16("y"), ORIENT='h',
        ),
    Float("width scale"),
    Float("height scale"),
    Bool16("scaling flags", *hud_scaling_flags),

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
    SInt16("sequence index"),
    SInt8("alpha multiplier"),
    SInt8("alpha bias"),
    SInt16("value scale"),
    Float("opacity"),
    Float("translucency"),
    #QStruct("disabled color", INCLUDE=argb_byte),
    UInt32("disabled color", INCLUDE=argb_uint32),
    Pad(16),
    #QStruct("overcharge minimum color", INCLUDE=xrgb_byte),
    #QStruct("overcharge maximum color", INCLUDE=xrgb_byte),
    #QStruct("overcharge flash color", INCLUDE=xrgb_byte),
    #QStruct("overcharge empty color", INCLUDE=xrgb_byte),
    UInt32("overcharge minimum color", INCLUDE=xrgb_uint32),
    UInt32("overcharge maximum color", INCLUDE=xrgb_uint32),
    UInt32("overcharge flash color", INCLUDE=xrgb_uint32),
    UInt32("overcharge empty color", INCLUDE=xrgb_uint32),
    SIZE=136
    )

health_panel_meter = Struct("health panel meter",
    QStruct("anchor offset",
        SInt16("x"), SInt16("y"), ORIENT='h',
        ),
    Float("width scale"),
    Float("height scale"),
    Bool16("scaling flags", *hud_scaling_flags),

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
    SInt16("sequence index"),
    SInt8("alpha multiplier"),
    SInt8("alpha bias"),
    SInt16("value scale"),
    Float("opacity"),
    Float("translucency"),
    #QStruct("disabled color", INCLUDE=argb_byte),
    UInt32("disabled color", INCLUDE=argb_uint32),
    Pad(16),
    #QStruct("medium health left color", INCLUDE=xrgb_byte),
    UInt32("medium health left color", INCLUDE=xrgb_uint32),
    Float("max color health fraction cutoff"),
    Float("min color health fraction cutoff"),
    SIZE=136
    )

motion_sensor_center = Struct("motion sensor center",
    QStruct("anchor offset",
        SInt16("x"), SInt16("y"), ORIENT='h',
        ),
    Float("width scale"),
    Float("height scale"),
    Bool16("scaling flags", *hud_scaling_flags),
    SIZE=16
    )

auxilary_overlay = Struct("auxilary overlay",
    Struct("background", INCLUDE=hud_background),
    SEnum16("type",
        "team icon"
        ),
    Bool16("flags",
        "use team color"
        ),
    SIZE=132
    )

auxilary_meter = Struct("auxilary meter",
    Pad(18),
    SEnum16("type", "integrated light", VISIBLE=False),
    Struct("background", INCLUDE=hud_background),

    QStruct("anchor offset",
        SInt16("x"), SInt16("y"), ORIENT='h',
        ),
    Float("width scale"),
    Float("height scale"),
    Bool16("scaling flags", *hud_scaling_flags),

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
    SInt16("sequence index"),
    SInt8("alpha multiplier"),
    SInt8("alpha bias"),
    SInt16("value scale"),
    Float("opacity"),
    Float("translucency"),
    #QStruct("disabled color", INCLUDE=argb_byte),
    UInt32("disabled color", INCLUDE=argb_uint32),

    Pad(16),
    Float("minimum fraction cutoff"),
    Bool32("overlay flags",
        "show only when active",
        "flash once if activated while disabled",
        ),

    SIZE=324,
    COMMENT="\nThis auxilary meter is meant for the flashlight.\n"
    )

unhi_body = Struct("tagdata",
    SEnum16("anchor", *hud_anchors),

    Pad(34),
    Struct("unit hud background", INCLUDE=hud_background),
    Struct("shield panel background", INCLUDE=hud_background),
    shield_panel_meter,
    Struct("health panel background", INCLUDE=hud_background),
    health_panel_meter,
    Struct("motion sensor background", INCLUDE=hud_background),
    Struct("motion sensor foreground", INCLUDE=hud_background),

    Pad(32),
    motion_sensor_center,

    Pad(20),
    SEnum16("auxilary overlay anchor", *hud_anchors),
    Pad(34),
    reflexive("auxilary overlays", auxilary_overlay, 16),

    Pad(16),
    reflexive("warning sounds", warning_sound, 12,
        DYN_NAME_PATH='.sound.filepath'),
    reflexive("auxilary meters", auxilary_meter, 16),

    SIZE=1388
    )

    
def get():
    return unhi_def

unhi_def = TagDef("unhi",
    blam_header("unhi"),
    unhi_body,

    ext=".unit_hud_interface", endian=">", tag_cls=HekTag,
    )
