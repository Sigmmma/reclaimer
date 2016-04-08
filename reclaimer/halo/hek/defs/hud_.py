from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

hud__body = Struct("Data",
    #I didnt feel like adding offsets since there is no
    #padding until AFTER all entries. it's all sequential
    TagIndexRef("digits bitmap", INCLUDE=Tag_Index_Ref_Struct),
    SInt8("bitmap digit width"),
    SInt8("screen digit width"),
    SInt8("x offset"),
    SInt8("y offset"),
    SInt8("decimal point width"),
    SInt8("colon width"),
    SIZE=100,
    )


def get():
    return hud__def

hud__def = TagDef(
    com( {1:{DEFAULT:"hud#" }}, Tag_Header),
    hud__body,
    
    NAME="hud_number",
    
    ext=".hud_number", def_id="hud#", endian=">"
    )
