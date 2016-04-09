from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef
from ...hek.defs import str_, ustr, hmt_, bitm#, snd_, font

com = combine

def get(): return resource_def


def get_resource_tag_type(block=None, parent=None, attr_index=None,
                          rawdata=None, new_value=None, *args, **kwargs):
    if parent is None:
        raise KeyError()
    
    tag = parent.get_tag()
    case = ''
    
    r_type = tag.data.resource_type.data_name

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


raw_meta_data = Container("tag meta", 
    BytesRaw("raw tag meta", SIZE='..size'),
    ALIGN=4
    )

#replace raw data references with padding since they dont exist
bitmap_meta = dict(bitm.bitm_def.descriptor[1])
bitmap_meta[11] = Void(bitmap_meta[11][NAME])
bitmap_meta[12] = Void(bitmap_meta[12][NAME])


tag_meta = Switch("tag meta",
    DEFAULT=raw_meta_data, POINTER='.offset',
    CASE=get_resource_tag_type,
    CASES={'bitmap':Container("meta data",
               bitmap_meta),
           #'sound':Container("meta_data",
           #    sound_meta)
           }
    )

tag_header = Struct("tag header",
    LUInt32("id"),
    LUInt32("size"),
    LUInt32("offset"),
    CHILD=tag_meta
    )

tag_path = CStrLatin1("tag path")


resource_def = TagDef(
    LUEnum32("resource type",
        ('bitmaps', 1),
        ('sounds',  2),
        ('strings', 3)
        ),
    LPointer32("tag paths pointer"),
    LPointer32("tag headers pointer"),
    LUInt32("tag count"),
    Array("tag paths",
        SIZE='.tag_count',
        POINTER='.tag_paths_pointer',
        SUB_STRUCT=tag_path,
        ),
    Array("tag headers",
        SIZE='.tag_count',
        POINTER='.tag_headers_pointer',
        SUB_STRUCT=tag_header,
        ),
    
    NAME="halo map resource",
    ext=".map", def_id="resource", endian="<", align=ALIGN_AUTO
    )
