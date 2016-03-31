from supyr_struct.defs.tag_def import *

def get():
    return HashCacheDef

class HashCacheDef(TagDef):

    ext = ".hashcache"
    
    def_id = "hashcache"
    
    endian = "<"

    hash_desc = { TYPE:Container, NAME:"hash",
                  0:{ TYPE:BytesRaw,   NAME:"hash",
                      SIZE:"...header.hashsize" },
                  1:{ TYPE:CStrLatin1, NAME:"value" }
                  }
    
    descriptor = { TYPE:Container, NAME:"hashcache",
                      0:{ TYPE:Struct, NAME:"header", SIZE:128,
                          0:{ TYPE:UInt32, NAME:"id",      DEFAULT:'hsah' },
                          1:{ TYPE:UInt32, NAME:"version", DEFAULT:2 },
                          
                          2:{ TYPE:UInt32, NAME:"hashcount" },
                          3:{ TYPE:UInt16, NAME:"hashsize" },
                          4:{ TYPE:UInt16, NAME:"namelen" },
                          5:{ TYPE:UInt32, NAME:"descriptionlen" },

                          #ROOM FOR ADDITIONAL DATA
                          
                          6:{ TYPE:StrLatin1, NAME:"hashmethod",
                              OFFSET:96, SIZE:32 }
                          },
                      1:{ TYPE:StrUtf8, NAME:"cache_name",
                          SIZE:".header.namelen" },
                      2:{ TYPE:StrUtf8, NAME:"cache_description",
                          SIZE:".header.descriptionlen" },
                      3:{ TYPE:Array, NAME:"cache",
                          SIZE:".header.hashcount",
                          SUB_STRUCT:hash_desc }
                      }
