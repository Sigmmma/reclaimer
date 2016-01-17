from ...Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def

def Construct():
    return NGPR_Def

class NGPR_Def(Tag_Def):

    Ext = ".preferences_network_game"

    Cls_ID = "ngpr"

    Endian = ">"

    Tag_Structure = {TYPE:Container, GUI_NAME:"preferences_network_game",
                     0:Combine( { 1:{ DEFAULT:"ngpr" },
                                  5:{ DEFAULT:"2" }
                                  }, Tag_Header),
                     1:{ TYPE:Struct, SIZE:896, GUI_NAME:"Data",
                         #I didnt feel like adding offsets since
                         #there is only padding in one spot
                         0:{ TYPE:Str_Latin1, GUI_NAME:"Name", SIZE:32 },
                         1:Com({NAME:"Primary Color"}, R_G_B_Float),
                         2:Com({NAME:"Secondary Color"}, R_G_B_Float),
                         
                         3:{ TYPE:Tag_Index_Ref, GUI_NAME:"Pattern",
                             INCLUDE:Tag_Index_Ref_Struct,
                             },
                         4:{ TYPE:SInt16, GUI_NAME:"Pattern Bitmap Index" },
                         
                         5:{ TYPE:Pad, SIZE:2 },
                         
                         6:{ TYPE:Tag_Index_Ref, GUI_NAME:"Decal",
                             INCLUDE:Tag_Index_Ref_Struct,
                             },
                         7:{ TYPE:SInt16, GUI_NAME:"Decal Bitmap Index" },
                         }
                     }
