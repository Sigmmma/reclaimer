from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

devi_body = Struct("Data",
    Pad(2),
    BBool16("flags",
        "position loops",
        "position not interpolated",
        ),

    BFloat("power transition time"),
    BFloat("power acceleration time"),
    BFloat("position transition time"),
    BFloat("position acceleration time"),
    BFloat("depowered position transition time"),
    BFloat("depowered position acceleration time"),
                   
    BSEnum16("A in", *Device_Functions),
    BSEnum16("B in", *Device_Functions),
    BSEnum16("C in", *Device_Functions),
    BSEnum16("D in", *Device_Functions),
                   
    TagIndexRef("open",      INCLUDE=Tag_Index_Ref_Struct),
    TagIndexRef("close",     INCLUDE=Tag_Index_Ref_Struct),
    TagIndexRef("opened",    INCLUDE=Tag_Index_Ref_Struct),
    TagIndexRef("closed",    INCLUDE=Tag_Index_Ref_Struct),
    TagIndexRef("depowered", INCLUDE=Tag_Index_Ref_Struct),
    TagIndexRef("repowered", INCLUDE=Tag_Index_Ref_Struct),
    
    BFloat("delay time"),
    Pad(8),
    TagIndexRef("delay effect", INCLUDE=Tag_Index_Ref_Struct),
    BFloat("automatic activation radius"),
                   
    SIZE=276,
    )


def get():
    return devi_def

devi_def = TagDef(
    com( {1:{DEFAULT:"devi" }}, Tag_Header),
    devi_body,
    
    NAME="device",
    
    ext=".device", def_id="devi", endian=">"
    )
