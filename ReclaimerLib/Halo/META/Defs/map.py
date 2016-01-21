from ...Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def
from ...HEK.Defs import bitm, boom, colo, devc, devi, flag, fog, foot, hmt,\
     hud_, item, itmc, metr, mply, ngpr, pphy, scex, schi, senv, sgla, shdr,\
     smet, snde, soso, Soul, spla, str_, swat, tagc, trak, ustr, wind

Com = Combine

#Halo map constants
PC_TAG_INDEX_HEADER_SIZE   = 40
XBOX_TAG_INDEX_HEADER_SIZE = 36

XBOX_BSP_MAGIC = 2174377984

XBOX_INDEX_MAGIC = 2151309348
PC_INDEX_MAGIC   = 1078198312

def Construct():
    return Map_Def

class Map_Def(Tag_Def):

    Ext = ".map"
    
    Cls_ID = "map"
    
    Endian = "<"

    Sani_Warn = False

    def Tag_Path_Pointer(*args, **kwargs):
        Parent = kwargs.get('Parent')
        
        if Parent is None:
            raise KeyError
        
        New_Value = kwargs.get('New_Value')
        T_Head = Parent.PARENT
        Magic  = kwargs.get('Map_Magic')
        
        if Magic is None:
            I_Head = T_Head.PARENT.PARENT
            Magic  = (I_Head.Index_Magic -
                      I_Head.PARENT.Mapfile_Header.Tag_Index_Offset)

        #NEED TO FINISH THIS SO IT CAN SET THE PATH DATA POINTER
        
        if New_Value is None:
            return PC_TAG_INDEX_HEADER_SIZE + T_Head.Tag_Path_Offset - Magic
        

    def Tag_Meta_Data_Pointer(*args, **kwargs):
        Parent = kwargs.get('Parent')
        
        if Parent is None:
            raise KeyError

        New_Value = kwargs.get('New_Value')
        T_Head = Parent.PARENT
        Magic = kwargs.get('Map_Magic')
        
        if Magic is None:
            I_Head = T_Head.PARENT.PARENT
            Magic  = (I_Head.Index_Magic -
                      I_Head.PARENT.Mapfile_Header.Tag_Index_Offset)
        
        if New_Value is None:
            return PC_TAG_INDEX_HEADER_SIZE + T_Head.Tag_Offset - Magic
        

    def Tag_Meta_Case(*args, **kwargs):
        Parent = kwargs.get('Parent')
        
        if Parent is None:
            raise KeyError

        New_Value = kwargs.get('New_Value')
        T_Head = Parent.PARENT
        I_Head = T_Head.PARENT.PARENT
        M_Head = I_Head.PARENT.Mapfile_Header
        Magic = kwargs.get('Map_Magic')
        
        if Magic is None:
            Magic = I_Head.Index_Magic - M_Head.Tag_Index_Offset

        Offset = PC_TAG_INDEX_HEADER_SIZE + T_Head.Tag_Offset - Magic
        
        if Offset <= 0 or Offset >= M_Head.Decompressed_Len:
            return
        else:
            return T_Head.Tag_Class_1.Data

        
    def FCC(Value):
        return int.from_bytes(bytes(Value, encoding='latin1'), byteorder='big')
        

    Tag_Meta = { TYPE:Switch, NAME:"Tag_Meta",
                 CASE:Tag_Meta_Case,
                 #THESE WILL NEED TO BE MODIFIED SINCE
                 #RAW DATA ISN'T INSIDE IT ANYMORE
                 CASES:{#FCC('bitm'):bitm.BITM_Def.Tag_Structure[1],
                        FCC('boom'):boom.BOOM_Def.Tag_Structure[1],
                        FCC('colo'):colo.COLO_Def.Tag_Structure[1],
                        FCC('devc'):devc.DEVC_Def.Tag_Structure[1],
                        FCC('devi'):devi.DEVI_Def.Tag_Structure[1],
                        FCC('flag'):flag.FLAG_Def.Tag_Structure[1],
                        FCC('fog '):fog.FOG_Def.Tag_Structure[1],
                        FCC('foot'):foot.FOOT_Def.Tag_Structure[1],
                        #FCC('hmt '):hmt.HMT_Def.Tag_Structure[1],
                        FCC('hud#'):hud_.HUD_Def.Tag_Structure[1],
                        FCC('item'):item.ITEM_Def.Tag_Structure[1],
                        FCC('itmc'):itmc.ITMC_Def.Tag_Structure[1],
                        #FCC('metr'):metr.METR_Def.Tag_Structure[1],
                        FCC('mply'):mply.MPLY_Def.Tag_Structure[1],
                        FCC('ngpr'):ngpr.NGPR_Def.Tag_Structure[1],
                        FCC('pphy'):pphy.PPHY_Def.Tag_Structure[1],
                        FCC('scex'):scex.SCEX_Def.Tag_Structure[1],
                        FCC('schi'):schi.SCHI_Def.Tag_Structure[1],
                        FCC('senv'):senv.SENV_Def.Tag_Structure[1],
                        FCC('sgla'):sgla.SGLA_Def.Tag_Structure[1],
                        FCC('shdr'):shdr.SHDR_Def.Tag_Structure[1],
                        FCC('smet'):smet.SMET_Def.Tag_Structure[1],
                        FCC('snde'):snde.SNDE_Def.Tag_Structure[1],
                        FCC('soso'):soso.SOSO_Def.Tag_Structure[1],
                        FCC('Soul'):Soul.SOUL_Def.Tag_Structure[1],
                        FCC('spla'):spla.SPLA_Def.Tag_Structure[1],
                        #FCC('str#'):str_.STR_Def.Tag_Structure[1],
                        FCC('swat'):swat.SWAT_Def.Tag_Structure[1],
                        FCC('tagc'):tagc.TAGC_Def.Tag_Structure[1],
                        FCC('trak'):trak.TRAK_Def.Tag_Structure[1],
                        #FCC('ustr'):ustr.USTR_Def.Tag_Structure[1],
                        FCC('wind'):wind.WIND_Def.Tag_Structure[1],
                        },
                 POINTER:Tag_Meta_Data_Pointer }


    Tag_Data = { TYPE:Container, NAME:"Tag_Data",
                 0:{ TYPE:CStr_Latin1, NAME:"Tag_Path",
                     POINTER:Tag_Path_Pointer },
                 1:Tag_Meta,
                 }

    Tag_Header = { TYPE:Struct, NAME:"Tag_Header",
                   0:Com({ NAME:"Tag_Class_1" }, Tag_4CC_ID),
                   1:Com({ NAME:"Tag_Class_2" }, Tag_4CC_ID),
                   2:Com({ NAME:"Tag_Class_3" }, Tag_4CC_ID),
                   3:{ TYPE:UInt32, NAME:"Tag_ID" },
                   4:{ TYPE:UInt32, NAME:"Tag_Path_Offset" },
                   5:{ TYPE:UInt32, NAME:"Tag_Offset" },
                   6:{ TYPE:UInt32, NAME:"Indexed" },
                   7:{ TYPE:Pad, SIZE:4 },
                   CHILD:Tag_Data
                   }
    
    Tag_Structure = { TYPE:Container, NAME:"Halo_Mapfile",
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
                          3:{ TYPE:Bytes_Raw, NAME:"Unknown1", SIZE:4 },
                          4:{ TYPE:UInt32,    NAME:"Tag_Index_Offset" },
                          5:{ TYPE:UInt32,    NAME:"Tag_Index_Meta_Len" },
                          6:{ TYPE:Pad, SIZE:8 },
                          7:{ TYPE:Str_Latin1, NAME:"Map_Name",   SIZE:32 },
                          8:{ TYPE:Str_Latin1_Enum, NAME:"Build_Date", SIZE:32,
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
                          10:{ TYPE:Bytes_Raw, NAME:"Unknown2", SIZE:4 },
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
                          9:{ TYPE:UInt32, NAME:"Tag_Index_Header_Sig", DEFAULT:'tags' },
                          CHILD:{ TYPE:Tag_Index,  NAME:"Tag_Index",
                                  SIZE:".Tag_Count", SUB_STRUCT:Tag_Header
                              }
                          }
                      }


    Structures = {}
    
    for key in Tag_Meta[CASES]:
        Structures[key] = Tag_Meta[CASES][key]
        Structures[key][POINTER] = Tag_Meta[POINTER]
