from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef
from ..hek.defs import str_, ustr, hmt_, bitm, snd_, font

def get(): return resource_def

def get_resource_tag_type(node=None, parent=None, attr_index=None,
                          rawdata=None, new_value=None, *args, **kwargs):
    if parent is None:
        raise KeyError()
    
    tag = parent.get_root()
    case = ''
    
    r_type = tag.data.resource_type.enum_name

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
            tag.sub_r_type = case = ''
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
bitmap_meta = dict(bitm.bitm_def.descriptor[1], NAME='meta_data')
sound_meta = dict(snd_.snd__def.descriptor[1], NAME='meta_data')

bitmap_meta[11] = Void(bitmap_meta[11][NAME])
bitmap_meta[12] = Void(bitmap_meta[12][NAME])

pitch_range = sound_meta[18] = dict(sound_meta[18])
pitch_range[STEPTREE] = Void(pitch_range[STEPTREE][NAME])
# delete just the above one line and uncomment the below lines
# when I figure out how the pointers and shit work for the reflexives
#pitch_range_child = pitch_range[STEPTREE] = dict(pitch_range[STEPTREE])
#pitch_range_substruct = pitch_range_child[SUB_STRUCT] =\
#                        dict(pitch_range_child[SUB_STRUCT])

#permutations = pitch_range_substruct[4] = dict(pitch_range_substruct[4])
#perms_child = permutations[STEPTREE] = dict(permutations[STEPTREE])
#perms_substruct = perms_child[SUB_STRUCT] = dict(perms_child[SUB_STRUCT])
#rawdata1 = perms_substruct[5] = dict(perms_substruct[5])
#rawdata2 = perms_substruct[6] = dict(perms_substruct[6])
#rawdata3 = perms_substruct[7] = dict(perms_substruct[7])

#rawdata1[STEPTREE] = Void(rawdata1[STEPTREE][NAME])
#rawdata2[STEPTREE] = Void(rawdata2[STEPTREE][NAME])
#rawdata3[STEPTREE] = Void(rawdata3[STEPTREE][NAME])

tag_meta = Switch("tag meta",
    DEFAULT=raw_meta_data, POINTER='.offset',
    CASE=get_resource_tag_type,
    CASES={'bitmap':bitmap_meta,
           'sound':sound_meta
           }
    )

tag_header = QuickStruct("tag header",
    LUInt32("id"),
    LUInt32("size"),
    LUInt32("offset"),
    STEPTREE=tag_meta
    )

tag_path = Container("tag path",
    CStrLatin1("tag path"),
    )


resource_def = TagDef("resource",
    LUEnum32("resource type",
        'NONE',
        'bitmaps',
        'sounds',
        'strings'
        ),
    LPointer32("tag paths pointer"),
    LPointer32("tag headers pointer"),
    LUInt32("tag count"),
    Array("tag paths",
        SIZE='.tag_count',
        SUB_STRUCT=tag_path, POINTER='.tag_paths_pointer',
        WIDGET=DynamicArrayFrame, DYN_NAME_PATH=".tag_path",
        ),
    Array("tag headers",
        SIZE='.tag_count', SUB_STRUCT=tag_header,
        POINTER='.tag_headers_pointer',
        ),

    ext=".map", endian="<"
    )
