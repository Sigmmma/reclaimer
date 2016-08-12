from ...common_descs import *
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
    bitm- > bitmaps.map
    snd! -> sounds.map
    font, hmt , str#, ustr -> loc.map

'''
################################################################
################################################################


def get(): return map_def

def tag_path_pointer(block=None, parent=None, attr_index=None,
                     rawdata=None, new_value=None, *args, **kwargs):
    if parent is None: raise KeyError()
    
    t_head = parent.parent
    m_head = t_head.parent.parent.mapfile_header
    magic  = PC_INDEX_MAGIC - m_head.tag_index_offset

    #NEED TO FINISH THIS SO IT CAN SET THE PATH POINTER
    
    if new_value is None:
        return PC_TAG_INDEX_HEADER_SIZE + t_head.tag_path_offset - magic
    

def tag_meta_data_pointer(block=None, parent=None, attr_index=None,
                          rawdata=None, new_value=None, *args, **kwargs):
    if parent is None: raise KeyError()

    t_head = parent.parent
    m_head = t_head.parent.parent.mapfile_header
    magic  = PC_INDEX_MAGIC - m_head.tag_index_offset
    #NEED TO FINISH THIS SO IT CAN SET THE META POINTER
    
    if new_value is None:
        return PC_TAG_INDEX_HEADER_SIZE + t_head.tag_offset - magic
    

def tag_meta_case(block=None, parent=None, attr_index=None,
                  rawdata=None, new_value=None, *args, **kwargs):
    if parent is None: raise KeyError()
    
    t_head = parent.parent
    if t_head.indexed:
        return
    
    m_head = t_head.parent.parent.mapfile_header
    magic  = PC_INDEX_MAGIC - m_head.tag_index_offset
    
    offset = PC_TAG_INDEX_HEADER_SIZE + t_head.tag_offset - magic
    return t_head.tag_class_1.data
    

def tag_index_array_pointer(block=None, parent=None, attr_index=None,
                            rawdata=None, new_value=None, *args, **kwargs):
    if block is None: raise KeyError()
    i_head = block.parent.tag_index_header
    m_head = block.parent.mapfile_header
    
    if new_value is None:
        return (m_head.tag_index_offset + PC_TAG_INDEX_HEADER_SIZE +
                i_head.index_magic - PC_INDEX_MAGIC)
    
def map_fcc(value):
    return fcc(value, 'big')
       

tag_meta = Switch("tag meta",
    CASE=tag_meta_case,
    #THESE WILL NEED TO BE MODIFIED SINCE
    #RAW DATA ISN'T INSIDE IT ANYMORE
    CASES={#map_fcc('bitm'):bitm.bitm_def.descriptor[1],
        map_fcc('boom'):boom.boom_def.descriptor[1],
        map_fcc('colo'):colo.colo_def.descriptor[1],
        map_fcc('devc'):devc.devc_def.descriptor[1],
        map_fcc('devi'):devi.devi_def.descriptor[1],
        map_fcc('flag'):flag.flag_def.descriptor[1],
        map_fcc('fog '):fog_.fog__def.descriptor[1],
        map_fcc('foot'):foot.foot_def.descriptor[1],
        #map_fcc('hmt '):hmt_.hmt__def.descriptor[1],
        map_fcc('hud#'):hud_.hud__def.descriptor[1],
        map_fcc('item'):item.item_def.descriptor[1],
        map_fcc('itmc'):itmc.itmc_def.descriptor[1],
        #map_fcc('metr'):metr.metr_def.descriptor[1],
        map_fcc('mply'):mply.mply_def.descriptor[1],
        map_fcc('ngpr'):ngpr.ngpr_def.descriptor[1],
        map_fcc('pphy'):pphy.pphy_def.descriptor[1],
        map_fcc('scex'):scex.scex_def.descriptor[1],
        map_fcc('schi'):schi.schi_def.descriptor[1],
        map_fcc('senv'):senv.senv_def.descriptor[1],
        map_fcc('sgla'):sgla.sgla_def.descriptor[1],
        map_fcc('shdr'):shdr.shdr_def.descriptor[1],
        map_fcc('smet'):smet.smet_def.descriptor[1],
        map_fcc('snde'):snde.snde_def.descriptor[1],
        map_fcc('soso'):soso.soso_def.descriptor[1],
        map_fcc('Soul'):Soul.soul_def.descriptor[1],
        map_fcc('spla'):spla.spla_def.descriptor[1],
        #map_fcc('str#'):str_.str__def.descriptor[1],
        map_fcc('swat'):swat.swat_def.descriptor[1],
        map_fcc('tagc'):tagc.tagc_def.descriptor[1],
        map_fcc('trak'):trak.trak_def.descriptor[1],
        #map_fcc('ustr'):ustr.ustr_def.descriptor[1],
        map_fcc('wind'):wind.wind_def.descriptor[1],
        },
    POINTER=tag_meta_data_pointer,
    )


tag_data = Container("tag data",
    CStrLatin1("tag path", POINTER=tag_path_pointer),
    tag_meta,
    )

tag_header = Struct("tag header",
    Struct("tag class 1", INCLUDE=valid_tags),
    Struct("tag class 2", INCLUDE=valid_tags),
    Struct("tag class 3", INCLUDE=valid_tags),
    LUInt32("tag id"),
    LSInt32("tag path offset"),
    LSInt32("tag offset"),
    LUInt32("indexed"),
    Pad(4),
    CHILD=tag_data,
    )

map_header = Struct("map_header",
    LUInt32("head", DEFAULT='head'),
    LSEnum32("version",
        ("xbox",    5),
        ("pc_demo", 6),
        ("pc_full", 7),
        ("pc_ce", 609),
        ),
    LSInt32("decompressed len"),
    BytesRaw("unknown1", SIZE=4),
    LUInt32("tag index offset"),
    LUInt32("tag index meta len"),
    Pad(8),
    StrLatin1("map name", SIZE=32),
    StrLatin1Enum("build date",
        ("xbox", "01.10.12.2276"),
        ("demo", "01.00.00.0576"),
        ("pc",   "01.00.00.0564"),
        ("ce",   "01.00.00.0609"),
        SIZE=32,
        ),
    LUEnum32("map type",
        ("sp", 0),
        ("mp", 1),
        ("ui", 2),
        ),
    LUInt32("crc32"),
    Pad(1940),
    LUInt32("foot", DEFAULT='foot'),
    )

#Apparently the Halo Demo maps have a different
#header as there are 704 bytes #before the header
#that appear to be garbage AND garbage filling
#all the headers null padding.
tag_index_header = Struct("tag index header",
    LUInt32("index magic"),
    LUInt32("base magic"),
    LUInt32("map id"),
    LUInt32("tag count"),

    LUInt32("vertex object count"),
    LUInt32("model raw data offset"),

    LUInt32("indices object count"),
    LUInt32("indices offset"),

    LUInt32("model raw data size"),
    LUInt32("tag sig", DEFAULT='tags'),

    POINTER='.mapfile_header.tag_index_offset'
    )

tag_index = TagIndex("tag index",
    SIZE=".tag_index_header.tag_count",
    SUB_STRUCT=tag_header,
    POINTER=tag_index_array_pointer
    ),

subdefs = {}
for key in tag_meta[CASES]:
    #need to make a copy of this, or it screws up the original
    subdefs[key] = dict(tag_meta[CASES][key])
    subdefs[key][POINTER] = tag_meta[POINTER]
        
map_def = TagDef("map",
    map_header,
    tag_index_header,
    tag_index,

    ext=".map", endian="<"
    )
