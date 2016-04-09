from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef
from ...hek.defs import bitm, boom, colo, devc, devi, flag, fog_, foot, hmt_,\
     hud_, item, itmc, metr, mply, ngpr, pphy, scex, schi, senv, sgla, shdr,\
     smet, snde, soso, Soul, spla, str_, swat, tagc, trak, ustr, wind

################################################################
################################################################
'''-----------------------   Notes   ---------------------------
    If a tag is located in one of the shared resource maps, the
    tag_offset in tag_header will the the index in the resource
    map that the tag is located in and indexed will be 1.
    To determine which resource map the tag is in, it must be
    done based on the tag class.
    bitm->bitmaps.map
    snd!->sounds.map
    font,hmt ,str#,ustr->loc.map

'''
################################################################
################################################################


def get(): return map_def

def tag_path_pointer(block=None, parent=None, attr_index=None,
                     rawdata=None, new_value=None, *args, **kwargs):
    if parent is None: raise KeyError()
    
    t_head = parent.PARENT
    m_head = t_head.PARENT.PARENT.mapfile_header
    magic  = PC_INDEX_MAGIC - m_head.tag_index_offset

    #NEED TO FINISH THIS SO IT CAN SET THE PATH POINTER
    
    if new_value is None:
        return PC_TAG_INDEX_HEADER_SIZE + t_head.tag_path_offset - magic
    

def tag_meta_data_pointer(block=None, parent=None, attr_index=None,
                          rawdata=None, new_value=None, *args, **kwargs):
    if parent is None: raise KeyError()

    t_head = parent.PARENT
    m_head = t_head.PARENT.PARENT.mapfile_header
    magic  = PC_INDEX_MAGIC - m_head.tag_index_offset
    #NEED TO FINISH THIS SO IT CAN SET THE META POINTER
    
    if new_value is None:
        return PC_TAG_INDEX_HEADER_SIZE + t_head.tag_offset - magic
    

def tag_meta_case(block=None, parent=None, attr_index=None,
                  rawdata=None, new_value=None, *args, **kwargs):
    if parent is None: raise KeyError()
    
    t_head = parent.PARENT
    if t_head.indexed:
        return
    
    m_head = t_head.PARENT.PARENT.mapfile_header
    magic  = PC_INDEX_MAGIC - m_head.tag_index_offset
    
    offset = PC_TAG_INDEX_HEADER_SIZE + t_head.tag_offset - magic
    return t_head.tag_class_1.data
    

def tag_index_array_pointer(block=None, parent=None, attr_index=None,
                            rawdata=None, new_value=None, *args, **kwargs):
    if block is None: raise KeyError()
    i_head = block.PARENT.tag_index_header
    m_head = block.PARENT.mapfile_header
    
    if new_value is None:
        return (m_head.tag_index_offset + PC_TAG_INDEX_HEADER_SIZE +
                i_head.index_magic - PC_INDEX_MAGIC)
    
def fcc(value):
    '''Converts a string of 4 characters into an int'''
    #the fcc wont let me be, or let me be me, so let me see.....
    return int.from_bytes(bytes(value, encoding='latin1'), byteorder='big')

       

tag_meta = Switch("tag_meta",
    CASE=tag_meta_case,
    #THESE WILL NEED TO BE MODIFIED SINCE
    #RAW DATA ISN'T INSIDE IT ANYMORE
    CASES={#fcc('bitm'):bitm.bitm_def.descriptor[1],
        fcc('boom'):boom.boom_def.descriptor[1],
        fcc('colo'):colo.colo_def.descriptor[1],
        fcc('devc'):devc.devc_def.descriptor[1],
        fcc('devi'):devi.devi_def.descriptor[1],
        fcc('flag'):flag.flag_def.descriptor[1],
        fcc('fog '):fog_.fog__def.descriptor[1],
        fcc('foot'):foot.foot_def.descriptor[1],
        #fcc('hmt '):hmt_.hmt__def.descriptor[1],
        fcc('hud#'):hud_.hud__def.descriptor[1],
        fcc('item'):item.item_def.descriptor[1],
        fcc('itmc'):itmc.itmc_def.descriptor[1],
        #fcc('metr'):metr.metr_def.descriptor[1],
        fcc('mply'):mply.mply_def.descriptor[1],
        fcc('ngpr'):ngpr.ngpr_def.descriptor[1],
        fcc('pphy'):pphy.pphy_def.descriptor[1],
        fcc('scex'):scex.scex_def.descriptor[1],
        fcc('schi'):schi.schi_def.descriptor[1],
        fcc('senv'):senv.senv_def.descriptor[1],
        fcc('sgla'):sgla.sgla_def.descriptor[1],
        fcc('shdr'):shdr.shdr_def.descriptor[1],
        fcc('smet'):smet.smet_def.descriptor[1],
        fcc('snde'):snde.snde_def.descriptor[1],
        fcc('soso'):soso.soso_def.descriptor[1],
        fcc('Soul'):Soul.soul_def.descriptor[1],
        fcc('spla'):spla.spla_def.descriptor[1],
        #fcc('str#'):str_.str__def.descriptor[1],
        fcc('swat'):swat.swat_def.descriptor[1],
        fcc('tagc'):tagc.tagc_def.descriptor[1],
        fcc('trak'):trak.trak_def.descriptor[1],
        #fcc('ustr'):ustr.ustr_def.descriptor[1],
        fcc('wind'):wind.wind_def.descriptor[1],
        },
    POINTER=tag_meta_data_pointer,
    )


tag_data = Container("tag_data",
    CStrLatin1("tag_path", POINTER=tag_path_pointer),
    tag_meta,
    )

tag_header = Struct("tag_header",
    Struct("tag_class_1", INCLUDE=All_Valid_Tags),
    Struct("tag_class_2", INCLUDE=All_Valid_Tags),
    Struct("tag_class_3", INCLUDE=All_Valid_Tags),
    LUInt32("tag_id"),
    LSInt32("tag_path_offset"),
    LSInt32("tag_offset"),
    LUInt32("indexed"),
    Pad(4),
    CHILD=tag_data,
    )

map_header = Struct("map_header",
    LUInt32("id", DEFAULT='head'),
    LSEnum32("version",
        ("xbox", 5, 'xbox'),
        ("demo", 6, 'pC demo'),
        ("pc",   7, 'pc full'),
        ("ce", 609, 'custom edition'),
        ),
    LSInt32("decompressed_len"),
    BytesRaw("unknown1", SIZE=4),
    LUInt32("tag_index_offset"),
    LUInt32("tag_index_meta_len"),
    Pad(8),
    StrLatin1("map_name", SIZE=32),
    StrLatin1Enum("Build_Date",
        ("xbox", "01.10.12.2276"),
        ("demo", "01.00.00.0576"),
        ("pc",   "01.00.00.0564"),
        ("ce",   "01.00.00.0609"),
        SIZE=32,
        ),
    LUEnum32("map_type",
        ("sp", 0, "campaign"),
        ("mp", 1, "multiplayer"),
        ("ui", 2, "user interface"),
        ),
    BytesRaw("unknown2", SIZE=4),
    Pad(1940),
    LUInt32("footer", DEFAULT='foot'),
    )

#Apparently the Halo Demo maps have a different
#header as there are 704 bytes #before the header
#that appear to be garbage AND garbage filling
#all the headers null padding.
tag_index_header = Struct("tag_index_header",
    LUInt32("index_magic"),
    LUInt32("base_magic"),
    LUInt32("map_id"),
    LUInt32("tag_count"),

    LUInt32("vertex_object_count"),
    LUInt32("model_raw_data_offset"),

    LUInt32("indices_object_count"),
    LUInt32("indices_offset"),

    LUInt32("model_raw_data_size"),
    LUInt32("tag_sig", DEFAULT='tags'),

    POINTER='.mapfile_header.tag_index_offset'
    )

tag_index = TagIndex("tag_index",
    SIZE=".tag_index_header.tag_count",
    SUB_STRUCT=tag_header,
    POINTER=tag_index_array_pointer
    ),

subdefs = {}
for key in tag_meta[CASES]:
    #need to make a copy of this, or it screws up the original
    subdefs[key] = dict(tag_meta[CASES][key])
    subdefs[key][POINTER] = tag_meta[POINTER]
        
map_def = TagDef(
    map_header,
    tag_index_header,
    tag_index,
    
    NAME="halo_mapfile",
    
    ext=".map", def_id="map", endian="<", sani_warn=False
    )
