from ...hek.defs.antr import *

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

    #pitch and yaw are saved in radians.
    float_rad("right yaw per frame"),
    float_rad("left yaw per frame"),
    BSInt16("right frame count"),
    BSInt16("left frame count"),

    Pad(32),
    float_rad("down pitch per frame"),
    float_rad("up pitch per frame"),
    BSInt16("down frame count"),
    BSInt16("up frame count"),

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
    BytesRaw("unknown0", SIZE=8),
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
    BSInt16("right frame count"),
    BSInt16("left frame count"),

    float_rad("down pitch per frame"),
    float_rad("up pitch per frame"),
    BSInt16("down frame count"),
    BSInt16("up frame count"),

    Pad(8),
    reflexive("animations", anim_enum_desc),
    reflexive("ik points", ik_point_desc, 4, DYN_NAME_PATH=".marker"),
    reflexive("weapon types", unit_weapon_desc, DYN_NAME_PATH=".name"),
    reflexive("unknown", unknown_unit_desc),
    SIZE=128,
    )

seat_desc = Struct("seat",
    ascii_str32("label"),
    Pad(16),
    reflexive("animations", anim_enum_desc),
    SIZE=60
    )

vehicle_desc = Struct("vehicle desc",
    #pitch and yaw are saved in radians.
                      
    #Steering screen bounds
    float_rad("right yaw per frame"),
    float_rad("left yaw per frame"),
    BSInt16("right frame count"),
    BSInt16("left frame count"),

    float_rad("down pitch per frame"),
    float_rad("up pitch per frame"),
    BSInt16("down frame count"),
    BSInt16("up frame count"),

    Pad(56),
    reflexive("seats", seat_desc),
    reflexive("animations", anim_enum_desc, 8,
        'steering','roll','throttle','velocity',
        'braking','ground-speed','occupied','unoccupied'),
    reflexive("suspension animations", suspension_desc, 8),
    SIZE=116,
    )

antr_body = Struct("tagdata",
    reflexive("objects",  object_desc, 4),
    reflexive("units",    unit_desc, 32, DYN_NAME_PATH=".label"),
    reflexive("weapons",  weapons_desc, 1),
    reflexive("vehicles", vehicle_desc, 1),
    reflexive("devices",  device_desc, 1),
    reflexive("unit damages", anim_enum_desc, 176),
    reflexive("fp animations", fp_animation_desc, 1),
    #i have no idea why they decided to cap it at 257 instead of 256....
    reflexive("sound references", sound_reference_desc, 257,
        DYN_NAME_PATH=".sound.filepath"),
    BFloat("limp body node radius"),
    BBool16("flags",
        "compress all animations",
        "force idle compression",
        ),
    Pad(2),
    reflexive("nodes", nodes_desc, 64, DYN_NAME_PATH=".name"),
    reflexive("animations", animation_desc, 256, DYN_NAME_PATH=".name"),
    SIZE=128,
    )


def get():
    return antr_def

antr_def = TagDef("antr",
    blam_header('antr', 4),
    antr_body,

    ext=".model_animations", endian=">", tag_cls=HekTag
    )
