from supyr_struct.Defs.Tag_Def import *

def Construct():
    return Hash_Cache_Def

class Hash_Cache_Def(Tag_Def):

    Ext = ".hashcache"
    
    Cls_ID = "hashcache"
    
    Endian = "<"

    Hash = { TYPE:Container, NAME:"Hash",
             0:{ TYPE:Bytes_Raw, NAME:"Hash",
                 SIZE:"...Header.Hash_Size" },
             1:{ TYPE:CStr_Latin1, NAME:"Hash_Name" }
             }
    
    Tag_Structure = { TYPE:Container, NAME:"hashcache",
                      0:{ TYPE:Struct, NAME:"Header", SIZE:128,
                          0:{ TYPE:UInt32, NAME:"ID",      DEFAULT:'hsah' },
                          1:{ TYPE:UInt32, NAME:"Version", DEFAULT:1 },
                          
                          2:{ TYPE:UInt32, NAME:"Hash_Count" },
                          3:{ TYPE:UInt16, NAME:"Hash_Size" },
                          4:{ TYPE:UInt16, NAME:"Name_Length" },

                          #ROOM FOR ADDITIONAL DATA
                          
                          5:{ TYPE:Str_Latin1, NAME:"Method",
                              OFFSET:96, SIZE:32 }
                          },
                      1:{ TYPE:Str_UTF8, NAME:"Cache_Name",
                          SIZE:".Header.Name_Length" },
                      2:{ TYPE:Array, NAME:"Cache",
                          SIZE:".Header.Hash_Count",
                          SUB_STRUCT:Hash }
                      }

    Structures = {}
