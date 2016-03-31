from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef
from ...hek.defs import hmt_, str_, ustr, bitm#, snd_, font

com = combine

def get():
    return ResourceDef

class ResourceDef(TagDef):

    ext = ".map"
    
    def_id = "resource"
    
    endian = "<"

    align = ALIGN_AUTO

    def get_resource_tag_type(*args, **kwargs):
        parent = kwargs.get('parent')
        
        if parent is None:
            raise KeyError()
        
        tag = parent.get_tag()
        case = ''
        
        r_type = tag.tagdata.resource_type.data_name

        #This is a really hacky(and easy to break) method of determining
        #whether or not the 
        if r_type == 'bitmaps':
            if not hasattr(tag, 'sub_r_type'):
                tag.sub_r_type = case = ''
            elif tag.sub_r_type == '':
                tag.sub_r_type = case = 'bitmap'
            else:
                tag.sub_r_type = case = ''
        
        elif r_type == 'sounds':
            if not hasattr(tag, 'sub_r_type'):
                tag.sub_r_type = case = 'sound'
            elif tag.sub_r_type == '':
                tag.sub_r_type = case = 'sound'
            else:
                tag.sub_r_type = case = ''
        
        #there is no way to know what type of tag each of the tags in the
        #loc.map is, so rather than guess we just treat them as bytes
        return case


    raw_data = { TYPE:Container, NAME:"tag_meta", ALIGN:4,
                 0:{ TYPE:BytesRaw, NAME:"raw_data", SIZE:'..size' }
                 }

    bitmap_meta = com({}, bitm.BitmDef.descriptor[1])


    #null out the data types of the raw data references since they dont exist
    bitmap_meta[11][CHILD][TYPE] = bitmap_meta[12][CHILD][TYPE] = Void


    tag_meta = { TYPE:Switch, NAME:"tag_meta",
                 DEFAULT:raw_data, POINTER:'.offset',
                 CASE:get_resource_tag_type,
                 CASES:{'bitmap':{ TYPE:Container, NAME:"tag_meta",
                                   0:bitmap_meta },
                        #'sound':{ TYPE:Container, NAME:"tag_meta",
                        #          0:sound_meta }
                        }
                 }

    tag_header = { TYPE:Struct, NAME:"tag_header",
                   0:{ TYPE:UInt32, NAME:"id" },
                   1:{ TYPE:UInt32, NAME:"size" },
                   2:{ TYPE:UInt32, NAME:"offset" },
                   CHILD:tag_meta
                   }

    tag_path = { TYPE:CStrLatin1, NAME:"tag_path" }
    
    descriptor = { TYPE:Container,  NAME:"halo_map_resource",
                   0:{ TYPE:Enum32, NAME:"resource_type",
                       0:{ NAME:'bitmaps', VALUE:1 },
                       1:{ NAME:'sounds',  VALUE:2 },
                       2:{ NAME:'strings', VALUE:3 },
                       },
                   1:{ TYPE:Pointer32, NAME:"tag_paths_pointer" },
                   2:{ TYPE:Pointer32, NAME:"tag_headers_pointer" },
                   3:{ TYPE:UInt32,    NAME:"tag_count" },
                   4:{ TYPE:Array,     NAME:"tag_paths",
                       SIZE:'.tag_count', POINTER:'.tag_paths_pointer',
                       SUB_STRUCT:tag_path,
                       },
                   5:{ TYPE:Array,     NAME:"tag_headers",
                       SIZE:'.tag_count', POINTER:'.tag_headers_pointer',
                       SUB_STRUCT:tag_header,
                       },
                   }

    subdefs = {'tag_header':tag_header,
               'tag_path':tag_path,
               'tag_meta':tag_meta}
