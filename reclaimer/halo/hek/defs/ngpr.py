from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

def get():
    return NgprDef

class NgprDef(TagDef):

    ext = ".preferences_network_game"

    tag_id = "ngpr"

    endian = ">"

    descriptor = {TYPE:Container, GUI_NAME:"preferences_network_game",
                     0:com( { 1:{ DEFAULT:"ngpr" },
                                  5:{ DEFAULT:"2" }
                                  }, Tag_Header),
                     1:{ TYPE:Struct, SIZE:896, GUI_NAME:"Data",
                         #I didnt feel like adding offsets since
                         #there is only padding in one spot
                         0:{ TYPE:StrLatin1, GUI_NAME:"Name", SIZE:32 },
                         1:com({NAME:"Primary Color"}, R_G_B_Float),
                         2:com({NAME:"Secondary Color"}, R_G_B_Float),
                         
                         3:{ TYPE:TagIndexRef, GUI_NAME:"Pattern",
                             INCLUDE:Tag_Index_Ref_Struct,
                             },
                         4:{ TYPE:SInt16, GUI_NAME:"Pattern Bitmap Index" },
                         
                         5:{ TYPE:Pad, SIZE:2 },
                         
                         6:{ TYPE:TagIndexRef, GUI_NAME:"Decal",
                             INCLUDE:Tag_Index_Ref_Struct,
                             },
                         7:{ TYPE:SInt16, GUI_NAME:"Decal Bitmap Index" },
                         }
                     }
