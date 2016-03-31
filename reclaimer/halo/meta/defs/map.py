from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef
from ...hek.defs import bitm, boom, colo, devc, devi, flag, fog_, foot, hmt_,\
     hud_, item, itmc, metr, mply, ngpr, pphy, scex, schi, senv, sgla, shdr,\
     smet, snde, soso, Soul, spla, str_, swat, tagc, trak, ustr, wind

################################################################
################################################################
'''-----------------------   Notes   ---------------------------
    If a tag is located in one of the shared resource maps, the
    Tag_Offset in Tag_Header will the the index in the resource
    map that the tag is located in and Indexed will be 1.
    To determine which resource map the tag is in, it must be
    done based on the tag class.
    bitm->bitmaps.map
    snd!->sounds.map
    font,hmt ,str#,ustr->loc.map

'''
################################################################
################################################################


def get():
    return MapDef

class MapDef(TagDef):

    ext = ".map"
    
    def_id = "map"
    
    endian = "<"

    sani_warn = False

    def tag_path_pointer(*args, **kwargs):
        parent = kwargs.get('parent')
        
        if parent is None:
            raise KeyError
        
        new_value = kwargs.get('new_value')
        t_head    = parent.PARENT
        
        m_head = t_head.PARENT.PARENT.PARENT.Mapfile_Header
        magic = PC_INDEX_MAGIC - m_head.Tag_Index_Offset

        #NEED TO FINISH THIS SO IT CAN SET THE PATH POINTER
        
        if new_value is None:
            return PC_TAG_INDEX_HEADER_SIZE + t_head.Tag_Path_Offset - magic
        

    def tag_meta_data_pointer(*args, **kwargs):
        parent = kwargs.get('parent')
        
        if parent is None:
            raise KeyError

        new_value = kwargs.get('new_value')
        t_head    = parent.PARENT
        
        m_head = t_head.PARENT.PARENT.PARENT.Mapfile_Header
        magic = PC_INDEX_MAGIC - m_head.Tag_Index_Offset
        #NEED TO FINISH THIS SO IT CAN SET THE META POINTER
        
        if new_value is None:
            return PC_TAG_INDEX_HEADER_SIZE + t_head.Tag_Offset - magic
        

    def tag_meta_case(*args, **kwargs):
        parent = kwargs.get('parent')
        
        if parent is None:
            raise KeyError

        new_value = kwargs.get('new_value')
        t_head    = parent.PARENT
        if t_head.Indexed:
            return
        
        m_head = t_head.PARENT.PARENT.PARENT.Mapfile_Header
        magic = PC_INDEX_MAGIC - m_head.Tag_Index_Offset
        
        offset = PC_TAG_INDEX_HEADER_SIZE + t_head.Tag_Offset - magic
        return t_head.Tag_Class_1.data
        

    def tag_index_array_pointer(*args, **kwargs):
        block = kwargs.get('block')
        
        if block is None:
            raise KeyError

        new_value = kwargs.get('new_value')
        i_head    = block.PARENT
        m_head    = i_head.PARENT.Mapfile_Header
        
        if new_value is None:
            return (m_head.Tag_Index_Offset + PC_TAG_INDEX_HEADER_SIZE +
                    i_head.Index_Magic - PC_INDEX_MAGIC)
        
    def fcc(value):
        return int.from_bytes(bytes(value, encoding='latin1'), byteorder='big')
        

    Tag_Meta = { TYPE:Switch, NAME:"Tag_Meta",
                 CASE:tag_meta_case,
                 #THESE WILL NEED TO BE MODIFIED SINCE
                 #RAW DATA ISN'T INSIDE IT ANYMORE
                 CASES:{#fcc('bitm'):bitm.BitmDef.descriptor[1],
                        fcc('boom'):boom.BoomDef.descriptor[1],
                        fcc('colo'):colo.ColoDef.descriptor[1],
                        fcc('devc'):devc.DevcDef.descriptor[1],
                        fcc('devi'):devi.DeviDef.descriptor[1],
                        fcc('flag'):flag.FlagDef.descriptor[1],
                        fcc('fog '):fog_.Fog_Def.descriptor[1],
                        fcc('foot'):foot.FootDef.descriptor[1],
                        #fcc('hmt '):hmt_.Hmt_Def.descriptor[1],
                        fcc('hud#'):hud_.Hud_Def.descriptor[1],
                        fcc('item'):item.ItemDef.descriptor[1],
                        fcc('itmc'):itmc.ItmcDef.descriptor[1],
                        #fcc('metr'):metr.MetrDef.descriptor[1],
                        fcc('mply'):mply.MplyDef.descriptor[1],
                        fcc('ngpr'):ngpr.NgprDef.descriptor[1],
                        fcc('pphy'):pphy.PphyDef.descriptor[1],
                        fcc('scex'):scex.ScexDef.descriptor[1],
                        fcc('schi'):schi.SchiDef.descriptor[1],
                        fcc('senv'):senv.SenvDef.descriptor[1],
                        fcc('sgla'):sgla.SglaDef.descriptor[1],
                        fcc('shdr'):shdr.ShdrDef.descriptor[1],
                        fcc('smet'):smet.SmetDef.descriptor[1],
                        fcc('snde'):snde.SndeDef.descriptor[1],
                        fcc('soso'):soso.SosoDef.descriptor[1],
                        fcc('Soul'):Soul.SoulDef.descriptor[1],
                        fcc('spla'):spla.SplaDef.descriptor[1],
                        #fcc('str#'):str_.Str_Def.descriptor[1],
                        fcc('swat'):swat.SwatDef.descriptor[1],
                        fcc('tagc'):tagc.TagcDef.descriptor[1],
                        fcc('trak'):trak.TrakDef.descriptor[1],
                        #fcc('ustr'):ustr.UstrDef.descriptor[1],
                        fcc('wind'):wind.WindDef.descriptor[1],
                        },
                 POINTER:tag_meta_data_pointer }


    Tag_Data = { TYPE:Container, NAME:"Tag_Data",
                 0:{ TYPE:CStrLatin1, NAME:"Tag_Path",
                     POINTER:tag_path_pointer },
                 1:Tag_Meta,
                 }

    Tag_Header = { TYPE:Struct, NAME:"Tag_Header",
                   0:com({ NAME:"Tag_Class_1" }, Tag_Class, All_Valid_Tags),
                   1:com({ NAME:"Tag_Class_2" }, Tag_Class, All_Valid_Tags),
                   2:com({ NAME:"Tag_Class_3" }, Tag_Class, All_Valid_Tags),
                   3:{ TYPE:UInt32, NAME:"Tag_ID" },
                   4:{ TYPE:SInt32, NAME:"Tag_Path_Offset" },
                   5:{ TYPE:SInt32, NAME:"Tag_Offset" },
                   6:{ TYPE:UInt32, NAME:"Indexed" },
                   7:{ TYPE:Pad, SIZE:4 },
                   CHILD:Tag_Data
                   }
    
    descriptor = { TYPE:Container, NAME:"Halo_Mapfile",
                      #Apparently the Halo Demo maps have a different
                      #header as there are 704 bytes #before the header
                      #that appear to be garbage AND garbage filling
                      #all the headers null padding.
                      0:{ TYPE:Struct, NAME:"Mapfile_Header",
                          0:{ TYPE:UInt32, NAME:"ID", DEFAULT:'head' },
                          1:{ TYPE:Enum32, NAME:"Version",
                              0:{ NAME:"XBOX", VALUE:5 },
                              1:{ NAME:"Demo", VALUE:6 },
                              2:{ NAME:"PC",   VALUE:7 },
                              3:{ NAME:"CE",   VALUE:609 }
                              },
                          2:{ TYPE:SInt32,    NAME:"Decompressed_Len" },
                          3:{ TYPE:BytesRaw, NAME:"Unknown1", SIZE:4 },
                          4:{ TYPE:UInt32,    NAME:"Tag_Index_Offset" },
                          5:{ TYPE:UInt32,    NAME:"Tag_Index_Meta_Len" },
                          6:{ TYPE:Pad, SIZE:8 },
                          7:{ TYPE:StrLatin1, NAME:"Map_Name",   SIZE:32 },
                          8:{ TYPE:StrLatin1Enum, NAME:"Build_Date", SIZE:32,
                              0:{ NAME:"XBOX", VALUE:"01.10.12.2276" },
                              1:{ NAME:"Demo", VALUE:"01.00.00.0576" },
                              2:{ NAME:"PC",   VALUE:"01.00.00.0564" },
                              3:{ NAME:"CE",   VALUE:"01.00.00.0609" },
                              },
                          9:{ TYPE:Enum32, NAME:"Map_Type",
                              0:{ NAME:"SP", NAME:"Campaign",       VALUE:0 },
                              1:{ NAME:"MP", NAME:"Multiplayer",    VALUE:1 },
                              2:{ NAME:"UI", NAME:"User_Interface", VALUE:2 }
                              },
                          10:{ TYPE:BytesRaw, NAME:"Unknown2", SIZE:4 },
                          11:{ TYPE:Pad, SIZE:1940 },
                          12:{ TYPE:UInt32, NAME:"Footer", DEFAULT:'foot' },
                          },
                      1:{ TYPE:Struct, NAME:"Tag_Index_Header",
                          POINTER:'.Mapfile_Header.Tag_Index_Offset',
                          0:{ TYPE:UInt32, NAME:"Index_Magic" },
                          1:{ TYPE:UInt32, NAME:"Base_Magic" },
                          2:{ TYPE:UInt32, NAME:"Map_ID" },
                          3:{ TYPE:UInt32, NAME:"Tag_Count" },
                          
                          4:{ TYPE:UInt32, NAME:"Vertex_Object_Count" },
                          5:{ TYPE:UInt32, NAME:"Model_Raw_Data_Offset" },
                          
                          6:{ TYPE:UInt32, NAME:"Indices_Object_Count" },
                          7:{ TYPE:UInt32, NAME:"Indices_Offset" },
                          
                          8:{ TYPE:UInt32, NAME:"Model_Raw_Data_Size" },
                          9:{ TYPE:UInt32, NAME:"Tag_Sig", DEFAULT:'tags' },
                          CHILD:{ TYPE:TagIndex,  NAME:"Tag_Index",
                                  SIZE:".Tag_Count", SUB_STRUCT:Tag_Header,
                                  POINTER:tag_index_array_pointer
                              }
                          }
                      }


    subdefs = {}
    
    for key in Tag_Meta[CASES]:
        #need to make a copy of this, or it screws up the original
        subdefs[key] = dict(Tag_Meta[CASES][key])
        subdefs[key][POINTER] = Tag_Meta[POINTER]
