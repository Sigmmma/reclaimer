from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef
from ...hek.defs import hmt_, str_, ustr, bitm#, snd_, font

com = combine

def get(): return resource_def


def get_resource_tag_type(block=None, parent=None, attr_index=None,
                          raw_data=None, new_value=None, *args, **kwargs):
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


raw_data = Container("tag_meta", 
    BytesRaw("raw_data", SIZE='..size'),
    ALIGN=4
    )

bitmap_meta = Struct('meta_data', INCLUDE=bitm.BitmDef.descriptor[1])

#null out the data types of the raw data references since they dont exist
bitmap_meta[11][CHILD][TYPE] = bitmap_meta[12][CHILD][TYPE] = Void


tag_meta = Switch("tag_meta",
    DEFAULT=raw_data, POINTER='.offset',
    CASE=get_resource_tag_type,
    CASES={'bitmap':Container("meta_data",
               bitmap_meta),
           #'sound':Container("meta_data",
           #    sound_meta)
           }
    )

tag_header = Struct("tag_header",
    LUInt32("id"),
    LUInt32("size"),
    LUInt32("offset"),
    CHILD=tag_meta
    )

tag_path = CStrLatin1("tag_path")


resource_def = TagDef(
    LUEnum32("resource_type",
        ('bitmaps', 1),
        ('sounds',  2),
        ('strings', 3)
        ),
    LPointer32("tag_paths_pointer"),
    LPointer32("tag_headers_pointer"),
    LUInt32("tag_count"),
    Array("tag_paths",
        SIZE='.tag_count',
        POINTER='.tag_paths_pointer',
        SUB_STRUCT=tag_path,
        ),
    Array("tag_headers",
        SIZE='.tag_count',
        POINTER='.tag_headers_pointer',
        SUB_STRUCT=tag_header,
        ),
    
    NAME="halo_map_resource",
    ext=".map", def_id="resource", endian="<", align=ALIGN_AUTO
    )
