from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

dyn_anim_path = "tagdata.animations.STEPTREE[DYN_I].name"

object_desc = Struct("object", 
    dyn_senum16("animation", DYN_NAME_PATH=dyn_anim_path),
    BSEnum16("function",
        "A out",
        "B out",
        "C out",
        "D out"
        ),
    BSEnum16("function controls",
        "frame",
        "scale",
        ),
    SIZE=20,
    )

anim_enum_desc = QStruct("animation",
    dyn_senum16("animation", DYN_NAME_PATH=dyn_anim_path)
    )

ik_point_desc = Struct("ik point", 
    ascii_str32("marker"),
    ascii_str32("attach to marker"),
    SIZE=64,
    )

weapon_types_desc = Struct("weapon types",
    ascii_str32("label"),
    Pad(16),
    reflexive("animations", anim_enum_desc, 10,
        'reload-1','reload-2','chamber-1','chamber-2',
        'fire-1','fire-2','charged-1','charged-2',
        'melee','overheat'),
    SIZE=60,
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

    float_rad("down pitch per frame"),
    float_rad("up pitch per frame"),
    BSInt16("down frame count"),
    BSInt16("up frame count"),

    Pad(32),
    reflexive("animations", anim_enum_desc, 55,
        'idle','gesture','turn-left','turn-right',
        'dive-front','dive-back','dive-left','dive-right',
        'move-front','move-back','move-left','move-right',
        'slide-front','slide-back','slide-left','slide-right',
        'airborne','land-soft','land-hard','unused0','throw-grenade',
        'disarm','drop','ready','put-away','aim-still','aim-move',
        'surprise-front','surprise-back','berserk',
        'evade-left','evade-right','signal-move','signal-attack','warn',
        'stunned-front','stunned-back','stunned-left','stunned-right',
        'melee','celebrate','panic','melee-airborne','flaming',
        'resurrect-front','resurrect-back','melee-continuous',
        'feeding','leap-start','leap-airborne','leap-melee',
        'zapping','unused1','unused2','unused3'),
    reflexive("ik points", ik_point_desc, 4, DYN_NAME_PATH=".marker"),
    reflexive("weapon types", weapon_types_desc, 10, DYN_NAME_PATH=".label"),
    SIZE=188,
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
    reflexive("animations", anim_enum_desc, 30,
        'airborne-dead','landing-dead',
        'acc-front-back','acc-left-right','acc-up-down',
        'push','twist','enter','exit','look','talk','emotions','unused0',
        'user0','user1','user2','user3','user4',
        'user5','user6','user7','user8','user9',
        'flying-front','flying-back','flying-left','flying-right',
        'opening','closing','hovering'),
    reflexive("ik points", ik_point_desc, 4, DYN_NAME_PATH=".marker"),
    reflexive("weapon types", unit_weapon_desc, 16, DYN_NAME_PATH=".name"),
    SIZE=100,
    )

weapons_desc = Struct("weapons", 
    Pad(16),
    reflexive("animations", anim_enum_desc, 11,
        'idle','ready','put-away',
        'reload-1','reload-2','chamber-1','chamber-2',
        'charged-1','charged-2','fire-1','fire-2'),
    SIZE=28,
    )

suspension_desc = QStruct("suspension animation", 
    SInt16("mass point index"),
    dyn_senum16("animation", DYN_NAME_PATH=dyn_anim_path),
    BFloat("full extension ground depth"),
    BFloat("full compression ground depth"),
    SIZE=20,
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

    Pad(68),
    reflexive("animations", anim_enum_desc, 8,
        'steering','roll','throttle','velocity',
        'braking','ground-speed','occupied','unoccupied'),
    reflexive("suspension animations", suspension_desc, 8),
    SIZE=116,
    )

device_desc = Struct("device", 
    Pad(84),
    reflexive("animations", anim_enum_desc, 2,
              'position','power'),
    SIZE=96,
    )

fp_animation_desc = Struct("fp animation", 
    Pad(16),
    reflexive("animations", anim_enum_desc, 28,
        'idle','posing','fire-1',
        'moving','overlays', 'light-off','light-on',
        'reload-empty','reload-full', 'overheated','ready','put-away',
        'overcharged','melee','fire-2','overcharged-jitter',
        'throw-grenade','ammunition', 'misfire-1','misfire-2',
        'throw-overheated','overheating', 'overheating-again',
        'enter','exit-empty','exit-full','o-h-exit','o-h-s-enter'),
    SIZE=28,
    )

sound_reference_desc = Struct("sound reference", 
    dependency('sound', "snd!"),
    SIZE=20,
    )

nodes_desc = Struct("node", 
    ascii_str32("name"),
    dyn_senum16("next sibling node index",
        DYN_NAME_PATH="..[DYN_I].name"),
    dyn_senum16("first child node index",
        DYN_NAME_PATH="..[DYN_I].name"),
    dyn_senum16("parent node index",
        DYN_NAME_PATH="..[DYN_I].name"),
    Pad(2),
    BBool32("node joint flags",
        "compress all animations",
        "force idle compression",
        ),
    QStruct("base vector", INCLUDE=ijk_float),
    float_rad("vector range"),
    Pad(4),
    SIZE=64,
    )

animation_desc = Struct("animation", 
    ascii_str32("name"),
    BSEnum16("type",
        "base",
        "overlay",
        "replacement",
        ),
    BSInt16("frame count"),
    BSInt16("frame size"),
    BSEnum16("frame info type",
        "none",
        "dx,dy",
        "dx,dy,dyaw",
        "dx,dy,dz,dyaw",
        ),
    BSInt32("node list checksum"),                       
    BSInt16("node count"),
    BSInt16("loop frame index"),

    BFloat("weight"),
    BSInt16("key frame index"),
    BSInt16("second key frame index"),

    dyn_senum16("next animation",
        DYN_NAME_PATH="..[DYN_I].name"),
    BBool16("flags",
        "compressed data",
        "world relative",
        { NAME:"pal", GUI_NAME:"25Hz(PAL)" },
        ),
    dyn_senum16("sound",
        DYN_NAME_PATH="tagdata.sound_references." +
        "sound_references_array[DYN_I].sound.filepath"),
    BSInt16("sound frame_index"),
    SInt8("left foot frame index"),
    SInt8("right foot frame index"),
    LSInt16("unknown sint16", ENDIAN='<'),
    LFloat("unknown float", ENDIAN='<'),

    rawdata_ref("frame info", max_size=32768),
    BytesRaw("unknown bytes", SIZE=44),
    BSInt32("offset to compressed data"),
    rawdata_ref("default data", max_size=16384),
    rawdata_ref("frame data", max_size=1048576),
    SIZE=180,
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
