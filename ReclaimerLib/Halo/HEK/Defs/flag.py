from ...Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def

def Construct():
    return FLAG_Def

class FLAG_Def(Tag_Def):

    Ext = ".flag"

    Cls_ID = "flag"

    Endian = ">"

    Attachment_Point = { TYPE:Struct, GUI_NAME:"Attachment Point",
                         0:{ TYPE:SInt16, OFFSET:0,
                             GUI_NAME:"Height to Next Attachment" },
                         1:{ TYPE:Str_Latin1, OFFSET:20, SIZE:32,
                             GUI_NAME:"Marker Name" }
                         }

    Tag_Structure = {TYPE:Container, GUI_NAME:"flag",
                     0:Combine( {1:{ DEFAULT:"flag" } }, Tag_Header),
                     
                     1:{ TYPE:Struct, SIZE:96, GUI_NAME:"Data",
                         0:{ TYPE:Enum16, OFFSET:4, GUI_NAME:"Trailing Edge Shape",
                             0:{ GUI_NAME:"Flat" },
                             1:{ GUI_NAME:"Concave triangular" },
                             2:{ GUI_NAME:"Convex triangular" },
                             3:{ GUI_NAME:"Trapezoid short top" },
                             4:{ GUI_NAME:"Trapezoid short bottom" },
                             },
                         
                         1:{ TYPE:SInt16, OFFSET:6, GUI_NAME:"Trailing Edge Shape Offset" },
                         2:{ TYPE:Enum16, OFFSET:8, GUI_NAME:"Attached Edge Shape",
                             0:{ GUI_NAME:"Flat" },
                             1:{ GUI_NAME:"Concave triangular" },
                             },
                         3:{ TYPE:SInt16, OFFSET:12, GUI_NAME:"Width" },
                         4:{ TYPE:SInt16, OFFSET:14, GUI_NAME:"Height" },
                         
                         5:{ TYPE:Float, OFFSET:16, GUI_NAME:"Cell Width" },
                         6:{ TYPE:Float, OFFSET:20, GUI_NAME:"Cell Height" },
                         
                         7:{ TYPE:Tag_Index_Ref, OFFSET:24, 
                             GUI_NAME:"Red Flag Shader",
                             INCLUDE:Tag_Index_Ref_Struct,
                             },
                         8:{ TYPE:Tag_Index_Ref, OFFSET:40,
                             GUI_NAME:"Physics",
                             INCLUDE:Tag_Index_Ref_Struct,
                             },
                         9:{ TYPE:Float, OFFSET:56, GUI_NAME:"Wind Noise" },
                         10:{ TYPE:Tag_Index_Ref, OFFSET:68,
                              GUI_NAME:"Blue Flag Shader",
                             INCLUDE:Tag_Index_Ref_Struct,
                             },
                         
                         11:{ TYPE:Reflexive, OFFSET:84,
                              GUI_NAME:"Attachment Points",
                              INCLUDE:Reflexive_Struct,
                             
                              CHILD:{ TYPE:Array, SIZE:".Count", MAX:4,
                                      GUI_NAME:"Attachment Points Array",
                                      SUB_STRUCT:Attachment_Point
                                      }
                             }
                         }
                     }
