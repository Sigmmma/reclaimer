from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return AntrDef

object_desc = Struct("object", 
    BSInt16("animation"),
    BUInt16("function"),
    BUInt16("function controls"),
    SIZE=20,
    )

anim_enum_desc = Struct("animation",
    BSInt16("animation")
    )

ik_point_desc = Struct("ik point", 
    StrLatin1("marker", SIZE=32),
    StrLatin1("attach to marker", SIZE=32),
    SIZE=64,
    )

weapon_types_desc = Struct("weapon types",
    StrLatin1("label", SIZE=32),
    Pad(16),
    Reflexive("animations",
        INCLUDE=Reflexive_Struct, MAX=10,
        CHILD=Array("animations array",
            SUB_STRUCT=anim_enum_desc, SIZE=".Count"),
        ),
    SIZE=60,
    )

unit_weapon_desc = Struct("weapon",
    StrLatin1("name", SIZE=32),
    StrLatin1("grip marker", SIZE=32),
    StrLatin1("hand marker", SIZE=32),
    #Aiming screen bounds

    #pitch and yaw are saved in radians.
    BFloat("right yaw per frame"),
    BFloat("left yaw per frame"),
    BSInt16("right frame count"),
    BSInt16("left frame count"),

    BFloat("down pitch per frame"),
    BFloat("up pitch per frame"),
    BSInt16("down frame count"),
    BSInt16("up frame count"),

    Pad(32),
    Reflexive("animations",
        #animations are as follows:
        #0-1   == idle, gesture
        #2-3   == turn-left/right
        #4-7   == dive-front/back/left/right
        #8-11  == move-front/back/left/right
        #12-15 == slide-front/back/left/right
        #16 == airborne
        #17-18 == land-soft/hard
        #19-24 == unused, throw-grenade, disarm, drop, ready, put-away
        #25-26 == aim-still/move
        #27-28 == surprise-front/back
        #29 == berserk
        #30-31 == evade-left/right
        #32-33 == signal-move/attack
        #34 == warn
        #35-38 == stunned-front/back/left/right
        #39-43 == melee, celebrate, panic, melee-airborne, flaming
        #44-45 == resurrect-front/back
        #46 == melee-continuous
        #47 == feeding
        #48-50 == leap-start/airborne/melee
        #51-54 == zapping, unused, unused, unused
        INCLUDE=Reflexive_Struct,
        CHILD=Array("animations array",
            SUB_STRUCT=anim_enum_desc, SIZE=".Count", MAX=55)
        ),
    Reflexive("ik points",
      INCLUDE=Reflexive_Struct,
      CHILD=Array("ik points array",
              SUB_STRUCT=ik_point_desc, SIZE=".Count", MAX=4),
        ),
    Reflexive("weapon types",
      #animations are as follows:
      #0-1 == reload-1, reload-2
      #2-3 == chamber-1, chamber-2
      #4-5 == fire-1, fire-2
      #6-7 == charged-1, charged-2
      #8-9 == melee, overheat
      INCLUDE=Reflexive_Struct,
      CHILD=Array("weapon types array",
          SUB_STRUCT=weapon_types_desc, SIZE=".Count", MAX=10),
      ),
    SIZE=188,
    )

unit_desc = Struct("unit", 
    StrLatin1("label", SIZE=32),
    #pitch and yaw are saved in radians.
                   
    #Looking screen bounds
    BFloat("right yaw per frame"),
    BFloat("left yaw per frame"),
    BSInt16("right frame count"),
    BSInt16("left frame count"),

    BFloat("down pitch per frame"),
    BFloat("up pitch per frame"),
    BSInt16("down frame count"),
    BSInt16("up frame count"),

    Pad(8),
    Reflexive("animations",
        #animations are as follows:
        #0  == airborne-dead
        #1  == landing-dead
        #2  == acc-front-back
        #3  == acc-left-right
        #4  == acc-up-down
        #5-10 == push, twist, enter, exit, look, talk
        #11 == emotions
        #12 == unused
        #13-22 == user0 - user9
        #23 == flying-front
        #24 == flying-back
        #25 == flying-left
        #26 == flying-right
        #27-29 == opening, closing, hovering
        INCLUDE=Reflexive_Struct,
        CHILD=Array("animations array",
            SUB_STRUCT=anim_enum_desc, SIZE=".Count", MAX=30),
        ),
    Reflexive("ik points",
        INCLUDE=Reflexive_Struct,
        CHILD=Array("ik points array",
            SUB_STRUCT=ik_point_desc, SIZE=".Count", MAX=4),
        ),
    Reflexive("weapons",
        INCLUDE=Reflexive_Struct,
        CHILD=Array("weapons array",
            SUB_STRUCT=unit_weapon_desc, SIZE=".Count", MAX=16)
        ),
    SIZE=100,
    )

weapons_desc = Struct("weapons", 
    Pad(16),
    Reflexive("animations",
        #animations are as follows:
        #0-2  == idle, ready, put-away
        #3-4  == reload-1, reload-2
        #5-6  == chamber-1, chamber-2
        #7-8  == charged-1, charged-2
        #9-10 == fire-1, fire-2
        INCLUDE=Reflexive_Struct,
        CHILD=Array("animations array",
            SUB_STRUCT=anim_enum_desc, SIZE=".Count", MAX=11)
        ),
    SIZE=28,
    )

suspension_desc = Struct("suspension animation", 
    BSInt16("mass point index"),
    BSInt16("animation"),
    BFloat("full extension ground depth"),
    BFloat("full compression ground depth"),
    SIZE=20,
    )

vehicle_desc = Struct("vehicle desc",
    #pitch and yaw are saved in radians.
                      
    #Steering screen bounds
    BFloat("right yaw per frame"),
    BFloat("left yaw per frame"),
    BSInt16("right frame count"),
    BSInt16("left frame count"),

    BFloat("down pitch per frame"),
    BFloat("up pitch per frame"),
    BSInt16("down frame count"),
    BSInt16("up frame count"),

    Pad(68),
    Reflexive("animations",
        #animations are as follows:
        #0-1 == steering, roll
        #2-3 == throttle, velocity
        #4-5 == braking,  ground-speed
        #6-7 == occupied, unoccupied
        INCLUDE=Reflexive_Struct,
        CHILD=Array("animations array",
            SUB_STRUCT=anim_enum_desc, SIZE=".Count", MAX=8),
        ),
    Reflexive("suspension animation",
        INCLUDE=Reflexive_Struct,
        CHILD=Array("suspensions array",
            SUB_STRUCT=suspension_desc, SIZE=".Count", MAX=8),
        ),
    SIZE=116,
    )

device_desc = Struct("device", 
    Pad(84),
    Reflexive("animations",
        #animations are as follows:
        #0 == position
        #1 == power
        INCLUDE=Reflexive_Struct,
        CHILD=Array("animations array",
            SUB_STRUCT=anim_enum_desc, SIZE=".Count", MAX=2)
        ),
    SIZE=96,
    )

fp_animation_desc = Struct("fp animation", 
    Pad(16),
    Reflexive("animations",
        #animations are as follows:
        #0-4   == idle, posing, fire-1, moving, overlays
        #5-6   == light-off/on
        #7-8   == reload-empty/full
        #9-11  == overheated, ready, put-away
        #12-14 == overcharged, melee, fire-2
        #15-17 == overcharged-jitter, throw-grenade, ammunition
        #18-19 == misfire-1/2
        #20-22 == throw-overheated, overheating, overheating-again
        #23-27 == enter, exit-empty, exit-full, o-h-exit, o-h-s-enter
        INCLUDE=Reflexive_Struct,
        CHILD=Array("animations array",
            SUB_STRUCT=anim_enum_desc, SIZE=".Count", MAX=28),
        ),
    SIZE=28,
    )

sound_reference_desc = Struct("sound reference", 
    Struct('sound', INCLUDE=Sound_Ref_Struct),
    SIZE=20,
    )

nodes_desc = Struct("node", 
    StrLatin1("name", SIZE=32),
    BSInt16("next sibling node index"),
    BSInt16("first child node index"),
    BSInt16("parent node index"),
    Pad(2),
    BBool32("node joint flags",
        "compress all animations",
        "force idle compression",
        ),
    Struct("base vector", INCLUDE=I_J_K_Float),
    BFloat("vector range"),
    Pad(4),
    SIZE=64,
    )

animation_desc = Struct("animation", 
    StrLatin1("name", SIZE=32),
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

    BSInt16("next animation"),
    BBool16("flags",
        "compressed data",
        "world relative",
        { NAME:"pal", GUI_NAME:"25Hz(PAL)" },
        ),
    BSInt16("sound"),
    BSInt16("sound frame_index"),
    SInt8("left foot frame index"),
    SInt8("right foot frame index"),
    BSInt16("unknown1", ENDIAN='<'),
    BFloat("unknown2", ENDIAN='<'),

    RawDataRef("frame info",
        EDITABLE=False, INCLUDE=Raw_Data_Ref_Struct,
        CHILD=BytearrayRaw("data", VISIBLE=False, SIZE=".Count"),
        ),
    BytesRaw("unknown3", SIZE=44),
    BSInt32("offset to compressed data"),
    RawDataRef("default data",
        EDITABLE=False, INCLUDE=Raw_Data_Ref_Struct,
        CHILD=BytearrayRaw("data", VISIBLE=False, SIZE=".Count"),
        ),
    RawDataRef("frame data",
        EDITABLE=False, INCLUDE=Raw_Data_Ref_Struct,
        CHILD=BytearrayRaw("data", VISIBLE=False, SIZE=".Count"),
        ),
    SIZE=180,
    )

antr_body = Struct("Data",
    Reflexive("objects",
       INCLUDE=Reflexive_Struct,
       CHILD=Array("objects array", MAX=4,
           SUB_STRUCT=object_desc, SIZE=".Count")
       ),
    Reflexive("units",
       INCLUDE=Reflexive_Struct,
       CHILD=Array("units array", MAX=32,
           SUB_STRUCT=unit_desc, SIZE=".Count")
       ),
    Reflexive("weapons",
       INCLUDE=Reflexive_Struct,
       CHILD=Array("weapons array", MAX=1,
           SUB_STRUCT=weapons_desc, SIZE=".Count")
       ),
    Reflexive("vehicles",
       INCLUDE=Reflexive_Struct,
       CHILD=Array("vehicles array", MAX=1,
           SUB_STRUCT=vehicle_desc, SIZE=".Count")
       ),
    Reflexive("devices",
       INCLUDE=Reflexive_Struct,
       CHILD=Array("devices array", MAX=1,
           SUB_STRUCT=device_desc, SIZE=".Count")
       ),
    Reflexive("unit damage",
       INCLUDE=Reflexive_Struct,
       CHILD=Array("unit damages array", MAX=176,
           SUB_STRUCT=anim_enum_desc, SIZE=".Count")
       ),
    Reflexive("fp animations",
       INCLUDE=Reflexive_Struct,
       CHILD=Array("fp animations array", MAX=1,
           SUB_STRUCT=fp_animation_desc, SIZE=".Count")
       ),
    Reflexive("sound references",
       INCLUDE=Reflexive_Struct,
       #i have no idea why they decided to cap it at 257 instead of 256....
       CHILD=Array("sound references array", MAX=257,
           SUB_STRUCT=sound_reference_desc, SIZE=".Count")
       ),
    BFloat("limp body node radius"),
    BBool16("flags",
        "compress all animations",
        "force idle compression",
        ),
    Pad(2),

    Reflexive("nodes",
       INCLUDE=Reflexive_Struct,
       CHILD=Array("nodes array", MAX=64,
           SUB_STRUCT=nodes_desc, SIZE=".Count")
       ),
    Reflexive("animations",
       INCLUDE=Reflexive_Struct,
       CHILD=Array("animations array", MAX=256,
           SUB_STRUCT=animation_desc, SIZE=".Count")
       ),
    SIZE=128,
    )


def get():
    return antr_def

antr_def = TagDef(
    com( {1:{DEFAULT:"antr" },
          5:{DEFAULT:4}}, Tag_Header),
    antr_body,
    
    NAME="model_animations",
    
    ext=".model_animations", def_id="antr", endian=">"
    )
