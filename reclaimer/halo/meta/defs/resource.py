from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef
from ...hek.defs import hmt, str_, ustr, bitm#, snd_, font

com = combine

def get():
    return ResourceDef

class ResourceDef(TagDef):

    ext = ".map"
    
    tag_id = "resource"
    
    endian = "<"

    align = ALIGN_AUTO

    def get_resource_tag_type(*args, **kwargs):
        parent = kwargs.get('parent')
        
        if parent is None:
            raise KeyError()
        
        tag = parent.get_tag()
        case = 'Raw'
        
        r_type = tag.tagdata.Type.data_name

        #This is a really hacky(and easy to break) method of determining
        #whether or not the 
        if r_type == 'Bitmaps':
            if not hasattr(tag, 'sub_r_type'):
                tag.sub_r_type = case = 'Raw'
            elif tag.sub_r_type == 'Raw':
                tag.sub_r_type = case = 'Bitmap'
            else:
                tag.sub_r_type = case = 'Raw'
        
        elif r_type == 'Sounds':
            if not hasattr(tag, 'sub_r_type'):
                tag.sub_r_type = case = 'Sound'
            elif tag.sub_r_type == 'Raw':
                tag.sub_r_type = case = 'Sound'
            else:
                tag.sub_r_type = case = 'Raw'
        
        #there is no way to know what type of tag each of the tags in the
        #loc.map is, so rather than guess we just treat them as bytes
        return case


    Raw_Data = { TYPE:Container, NAME:"Raw_Data", ALIGN:4,
                 0:{ TYPE:BytesRaw, NAME:"Raw_Tag_Data", SIZE:'..Size' }
                 }

    Bitmap_Meta = com({}, bitm.BitmDef.descriptor[1])


    #null out the data types of the raw data references since they dont exist
    Bitmap_Meta[11][CHILD][TYPE] = Bitmap_Meta[12][CHILD][TYPE] = Void


    Tag_Data = { TYPE:Switch, NAME:"Tag_Data",
                 DEFAULT:Raw_Data, POINTER:'.Offset',
                 CASE:get_resource_tag_type,
                 CASES:{'Raw':Raw_Data,
                        'Bitmap':{ TYPE:Container, NAME:"Tag_Meta",
                                   0:Bitmap_Meta },
                        #'Sound':{ TYPE:Container, NAME:"Tag_Meta",
                        #          0:Sound_Meta }
                        }
                 }

    Tag_Header = { TYPE:Struct, NAME:"Tag_Header",
                   0:{ TYPE:UInt32, NAME:"ID" },
                   1:{ TYPE:UInt32, NAME:"Size" },
                   2:{ TYPE:UInt32, NAME:"Offset" },
                   CHILD:Tag_Data
                   }

    Tag_Path = { TYPE:CStrLatin1, NAME:"Tag_Path" }
    
    descriptor = { TYPE:Container, NAME:"halo_map_resource",
                      0:{ TYPE:Enum32,    NAME:"Type",
                          0:{ NAME:'Bitmaps', VALUE:1 },
                          1:{ NAME:'Sounds',  VALUE:2 },
                          2:{ NAME:'Strings', VALUE:3 },
                          },
                      1:{ TYPE:Pointer32, NAME:"Tag_Paths_Pointer" },
                      2:{ TYPE:Pointer32, NAME:"Tag_Headers_Pointer" },
                      3:{ TYPE:UInt32,    NAME:"Tag_Count" },
                      4:{ TYPE:Array,     NAME:"Tag_Paths",
                          SIZE:'.Tag_Count', POINTER:'.Tag_Paths_Pointer',
                          SUB_STRUCT:Tag_Path,
                          },
                      5:{ TYPE:Array,     NAME:"Tag_Headers",
                          SIZE:'.Tag_Count', POINTER:'.Tag_Headers_Pointer',
                          SUB_STRUCT:Tag_Header,
                          },
                      }

    descriptors = {'Tag_Header':Tag_Header,
                   'Tag_Path':Tag_Path,
                   'Tag_Data':Tag_Data}
