from ...hek.defs.antr import *
from ..common_descs import *

# As meta, it seems MOST arrays of anim_enum_desc have an extra extra on the end

animations_extended_desc = Struct("weapon types",
    Pad(16),
    reflexive("animations", anim_enum_desc),
    SIZE=28,
    )

unit_weapon_desc = Struct("weapon",
    ascii_str32("name"),
    ascii_str32("grip marker"),
    ascii_str32("hand marker"),
    #Aiming screen bounds

    Pad(32),
    #pitch and yaw are saved in radians.
    float_rad("right yaw per frame"),
    float_rad("left yaw per frame"),
    SInt16("right frame count"),
    SInt16("left frame count"),

    float_rad("down pitch per frame"),
    float_rad("up pitch per frame"),
    SInt16("down frame count"),
    SInt16("up frame count"),

    reflexive("animations extended", animations_extended_desc),
    reflexive("ik points", ik_point_desc, 4, DYN_NAME_PATH=".marker"),
    reflexive("weapon types", weapon_types_desc, DYN_NAME_PATH=".label"),
    SIZE=188,
    )

label_desc = Struct("label",
    ascii_str32("label"),
    SIZE=32
    )

unknown_unit_desc = Struct("unknown_unit_desc",
    SInt32("unknown0"),
    SInt32("unknown1"),
    ascii_str32("label"),
    reflexive("labels", label_desc),
    reflexive("animations", anim_enum_desc),
    SIZE=64
    )

unit_desc = Struct("unit",
    ascii_str32("label"),
    #pitch and yaw are saved in radians.
                   
    #Looking screen bounds
    float_rad("right yaw per frame"),
    float_rad("left yaw per frame"),
    SInt16("right frame count"),
    SInt16("left frame count"),

    float_rad("down pitch per frame"),
    float_rad("up pitch per frame"),
    SInt16("down frame count"),
    SInt16("up frame count"),

    Pad(8),
    reflexive("animations", anim_enum_desc),
    reflexive("ik points", ik_point_desc, 4, DYN_NAME_PATH=".marker"),
    reflexive("weapons", unit_weapon_desc, DYN_NAME_PATH=".name"),
    reflexive("unknown", unknown_unit_desc),
    SIZE=128,
    )

seat_desc = Struct("seat",
    ascii_str32("label"),
    Pad(16),
    reflexive("animations", anim_enum_desc),
    SIZE=60
    )

vehicle_desc = Struct("vehicle",
    #pitch and yaw are saved in radians.
                      
    #Steering screen bounds
    float_rad("right yaw per frame"),
    float_rad("left yaw per frame"),
    SInt16("right frame count"),
    SInt16("left frame count"),

    float_rad("down pitch per frame"),
    float_rad("up pitch per frame"),
    SInt16("down frame count"),
    SInt16("up frame count"),

    Pad(56),
    reflexive("seats", seat_desc),
    reflexive("animations", anim_enum_desc, 8,
        'steering','roll','throttle','velocity',
        'braking','ground-speed','occupied','unoccupied'),
    reflexive("suspension animations", suspension_desc, 8),
    SIZE=116,
    )

effect_reference_desc = Struct("effect reference", 
    dependency_stubbs('effect', ("snd!", "effe")),
    SIZE=20,
    )

animation_desc = Struct("animation", 
    ascii_str32("name"),
    SEnum16("type",
        "base",
        "overlay",
        "replacement",
        ),
    SInt16("frame count"),
    SInt16("frame size"),
    SEnum16("frame info type",
        "none",
        "dx,dy",
        "dx,dy,dyaw",
        "dx,dy,dz,dyaw",
        ),
    SInt32("node list checksum"),                       
    SInt16("node count"),
    SInt16("loop frame index"),

    Float("weight"),
    SInt16("key frame index"),
    SInt16("second key frame index"),
    Pad(8),

    dyn_senum16("next animation", DYN_NAME_PATH="..[DYN_I].name"),
    Bool16("flags",
        "compressed data",
        "world relative",
        {NAME:"pal", GUI_NAME:"25Hz(PAL)"},
        ),
    dyn_senum16("sound",
        DYN_NAME_PATH="tagdata.effect_references." +
        "effect_references_array[DYN_I].effect.filepath"),
    SInt16("sound frame_index"),
    SInt8("left foot frame index"),
    SInt8("right foot frame index"),
    LSInt16("unknown sint16", ENDIAN='<'),
    LFloat("unknown float", ENDIAN='<'),

    rawdata_ref("frame info", max_size=32768),
    UInt32("trans flags0", EDITABLE=False),
    UInt32("trans flags1", EDITABLE=False),
    Pad(8),
    UInt32("rot flags0", EDITABLE=False),
    UInt32("rot flags1", EDITABLE=False),
    Pad(8),
    UInt32("scale flags0", EDITABLE=False),
    UInt32("scale flags1", EDITABLE=False),
    Pad(4),
    SInt32("offset to compressed data", EDITABLE=False),
    rawdata_ref("default data", max_size=16384),
    rawdata_ref("frame data", max_size=1048576),
    SIZE=188,
    )

antr_body = Struct("tagdata",
    reflexive("objects",  object_desc),
    reflexive("units",    unit_desc, DYN_NAME_PATH=".label"),
    reflexive("weapons",  weapons_desc),
    reflexive("vehicles", vehicle_desc),
    reflexive("devices",  device_desc),
    reflexive("unit damages", anim_enum_desc),
    reflexive("fp animations", fp_animation_desc),

    reflexive("effect references", effect_reference_desc,
        DYN_NAME_PATH=".effect.filepath"),
    Float("limp body node radius"),
    Bool16("flags",
        "compress all animations",
        "force idle compression",
        ),
    Pad(2),
    reflexive("nodes", nodes_desc, DYN_NAME_PATH=".name"),
    reflexive("animations", animation_desc, DYN_NAME_PATH=".name"),
    SIZE=128,
    )


def get():
    return antr_def

antr_def = TagDef("antr",
    blam_header_stubbs('antr', 5),  # increment to differentiate it from halo antr
    antr_body,

    ext=".model_animations", endian=">", tag_cls=AntrTag
    )
