from ...Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def
from ...HEK.Defs import hmt, str_, ustr, bitm#, snd_, font

Com = Combine

def Construct():
    return Resource_Def

class Resource_Def(Tag_Def):

    Ext = ".map"
    
    Cls_ID = "resource"
    
    Endian = "<"

    Align = ALIGN_AUTO

    def Get_Resource_Tag_Type(*args, **kwargs):
        Parent = kwargs.get('Parent')
        
        if Parent is None:
            raise KeyError()
        
        Tag = Parent.Get_Tag()
        Case = 'Raw'
        
        Resource_Type = Tag.Tag_Data.Resource_Type.Data_Name

        #This is a really hacky(and easy to break) method of determining
        #whether or not the 
        if Resource_Type == 'Bitmaps':
            if not hasattr(Tag, 'Sub_Resource_Type'):
                Tag.Sub_Resource_Type = Case = 'Raw'
            elif Tag.Sub_Resource_Type == 'Raw':
                Tag.Sub_Resource_Type = Case = 'Bitmap'
            else:
                Tag.Sub_Resource_Type = Case = 'Raw'
        
        elif Resource_Type == 'Sounds':
            if not hasattr(Tag, 'Sub_Resource_Type'):
                Tag.Sub_Resource_Type = Case = 'Sound'
            elif Tag.Sub_Resource_Type == 'Raw':
                Tag.Sub_Resource_Type = Case = 'Sound'
            else:
                Tag.Sub_Resource_Type = Case = 'Raw'
        
        #there is no way to know what type of tag each of the tags in the
        #loc.map is, so rather than guess we just treat them as bytes
        return Case


    Raw_Data = { TYPE:Container, NAME:"Raw_Data", ALIGN:4,
                 0:{ TYPE:Bytes_Raw, NAME:"Raw_Tag_Data", SIZE:'..Tag_Size' }
                 }

    Bitmap_Meta = Com({}, bitm.BITM_Def.Tag_Structure[1])


    #null out the data types of the raw data references since they dont exist
    Bitmap_Meta[11][CHILD][TYPE] = Bitmap_Meta[12][CHILD][TYPE] = Void


    Tag_Data = { TYPE:Switch, NAME:"Tag_Data",
                 DEFAULT:Raw_Data, POINTER:'.Tag_Offset',
                 CASE:Get_Resource_Tag_Type,
                 CASES:{'Raw':Raw_Data,
                        'Bitmap':{ TYPE:Container, NAME:"Tag_Meta",
                                   0:Bitmap_Meta },
                        #'Sound':{ TYPE:Container, NAME:"Tag_Meta",
                        #          0:Sound_Meta }
                        }
                 }

    Tag_Header = { TYPE:Struct, NAME:"Tag_Header",
                   0:{ TYPE:UInt32, NAME:"Tag_ID" },
                   1:{ TYPE:UInt32, NAME:"Tag_Size" },
                   2:{ TYPE:UInt32, NAME:"Tag_Offset" },
                   CHILD:Tag_Data
                   }

    Tag_Path = { TYPE:CStr_Latin1, NAME:"Tag_Path" }
    
    Tag_Structure = { TYPE:Container, NAME:"Halo_map_resource",
                      0:{ TYPE:Enum32,    NAME:"Resource_Type",
                          0:{ NAME:'Bitmaps', VALUE:1 },
                          1:{ NAME:'Sounds',  VALUE:2 },
                          2:{ NAME:'Strings', VALUE:3 },
                          },
                      1:{ TYPE:Pointer32, NAME:"Tag_Paths_Pointer" },
                      2:{ TYPE:Pointer32, NAME:"Tag_Headers_Pointer" },
                      3:{ TYPE:UInt32,    NAME:"Tag_Count" },
                      4:{ TYPE:Array, NAME:"Tag_Paths",
                          SIZE:'.Tag_Count', POINTER:'.Tag_Paths_Pointer',
                          SUB_STRUCT:Tag_Path,
                          },
                      5:{ TYPE:Array, NAME:"Tag_Headers",
                          SIZE:'.Tag_Count', POINTER:'.Tag_Headers_Pointer',
                          SUB_STRUCT:Tag_Header,
                          },
                      }

    Structures = {'Tag_Header':Tag_Header,
                  'Tag_Path':Tag_Path,
                  'Tag_Data':Tag_Data}
