from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef
from ...hek.defs import bitm, boom, colo, devc, devi, effe, flag, fog_, foot,\
     jpt_, hmt_, hud_, item, itmc, metr, mply, ngpr, pphy, scex, schi, senv,\
     sgla, shdr, smet, snde, snd_, soso, sotr, Soul, spla, str_, swat, tagc,\
     trak, ustr, wind

################################################################
################################################################
'''-----------------------   Notes   ---------------------------
    If a tag is located in one of the shared resource maps, the
    offset in tag_header will the the index in the resource
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

def map_fcc(value):
    return fcc(value, 'big')

SND__FCC = map_fcc('snd!')

def tag_path_pointer(node=None, parent=None, new_value=None, **kwargs):
    if parent is None:
        raise KeyError()
    t_head = parent.parent
    magic = kwargs.get('magic')
    if magic is None:
        m_head = t_head.parent.parent.map_header
        magic  = PC_INDEX_MAGIC - m_head.tag_index_offset

    #NEED TO FINISH THIS SO IT CAN SET THE PATH POINTER

    if new_value is None:
        return PC_TAG_INDEX_HEADER_SIZE + t_head.path_offset - magic


def tag_meta_data_pointer(node=None, parent=None, new_value=None, **kwargs):
    if parent is None:
        raise KeyError()

    t_head = parent.parent
    magic = kwargs.get('magic')
    if magic is None:
        m_head = t_head.parent.parent.map_header
        magic  = PC_INDEX_MAGIC - m_head.tag_index_offset
    #NEED TO FINISH THIS SO IT CAN SET THE META POINTER

    if new_value is None:
        return PC_TAG_INDEX_HEADER_SIZE + t_head.meta_offset - magic


def tag_meta_case(node=None, parent=None, new_value=None, **kwargs):
    if parent is None:
        raise KeyError()

    t_head = parent.parent
    if t_head.indexed:
        if t_head.class_1.data == SND__FCC:
            return 'indexed_snd!'
        return

    magic = kwargs.get('magic')
    if magic is None:
        m_head = t_head.parent.parent.map_header
        magic  = PC_INDEX_MAGIC - m_head.tag_index_offset

    offset = PC_TAG_INDEX_HEADER_SIZE + t_head.meta_offset - magic
    return t_head.class_1.data
    

def tag_index_array_pointer(node=None, parent=None, new_value=None, **kwargs):
    if node is None:
        raise KeyError()
    b_parent = node.parent

    magic = kwargs.get('magic')
    if magic is None:
        magic = PC_INDEX_MAGIC - b_parent.map_header.tag_index_offset

    if new_value is None:
        return (PC_TAG_INDEX_HEADER_SIZE +
                b_parent.tag_index_header.index_magic - magic)

#sound tags actually located in the sound cache
#still have part of the tag exist in the map.
indexed_sound = dict(snd_.snd__def.descriptor[1])
indexed_sound[18] = reflexive_struct

tag_meta = Switch("tag meta",
    CASE=tag_meta_case,
    CASES={
        map_fcc('bitm'):bitm.bitm_def.descriptor[1],
        map_fcc('boom'):boom.boom_def.descriptor[1],
        map_fcc('colo'):colo.colo_def.descriptor[1],
        map_fcc('devc'):devc.devc_def.descriptor[1],
        map_fcc('devi'):devi.devi_def.descriptor[1],
        map_fcc('effe'):effe.effe_def.descriptor[1],
        map_fcc('flag'):flag.flag_def.descriptor[1],
        map_fcc('fog '):fog_.fog__def.descriptor[1],
        map_fcc('foot'):foot.foot_def.descriptor[1],
        map_fcc('hmt '):hmt_.hmt__def.descriptor[1],
        map_fcc('hud#'):hud_.hud__def.descriptor[1],
        map_fcc('item'):item.item_def.descriptor[1],
        map_fcc('itmc'):itmc.itmc_def.descriptor[1],
        map_fcc('jpt!'):jpt_.jpt__def.descriptor[1],
        map_fcc('metr'):metr.metr_def.descriptor[1],
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
        map_fcc('snd!'):snd_.snd__def.descriptor[1],
        map_fcc('soso'):soso.soso_def.descriptor[1],
        map_fcc('sotr'):sotr.sotr_def.descriptor[1],
        map_fcc('Soul'):Soul.soul_def.descriptor[1],
        map_fcc('spla'):spla.spla_def.descriptor[1],
        map_fcc('str#'):str_.str__def.descriptor[1],
        map_fcc('swat'):swat.swat_def.descriptor[1],
        map_fcc('tagc'):tagc.tagc_def.descriptor[1],
        map_fcc('trak'):trak.trak_def.descriptor[1],
        map_fcc('ustr'):ustr.ustr_def.descriptor[1],
        map_fcc('wind'):wind.wind_def.descriptor[1],
        'indexed_snd!':indexed_sound,
        },
    POINTER=tag_meta_data_pointer,
    )


tag_data = Container("tag data",
    CStrLatin1("tag path", POINTER=tag_path_pointer),
    tag_meta,
    )

tag_header = Struct("tag header",
    LUEnum32("class 1", INCLUDE=valid_tags),
    LUEnum32("class 2", INCLUDE=valid_tags),
    LUEnum32("class 3", INCLUDE=valid_tags),
    LUInt32("id"),
    LSInt32("path offset"),
    LSInt32("meta offset"),
    LUInt32("indexed"),
    # if indexed is 1, the meta_offset is the literal index in the
    # bitmaps, sounds, or loc cache that the meta data is located in.
    Pad(4),
    STEPTREE=tag_data,
    )

map_header = Struct("map header",
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
    ascii_str32("map name"),
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
tag_index_header = QuickStruct("tag index header",
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

    POINTER='.map_header.tag_index_offset'
    )

tag_index = TagIndex("tag index",
    SIZE=".tag_index_header.tag_count",
    SUB_STRUCT=tag_header,
    POINTER=tag_index_array_pointer
    )

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
