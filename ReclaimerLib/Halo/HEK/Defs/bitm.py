from ...Common_Block_Structures import *
from supyr_struct.Defs.Tag_Def import Tag_Def
from .Objs.bitm import BITM_Tag

def Construct():
    return BITM_Def

class BITM_Def(Tag_Def):
    Ext = ".bitmap"

    Cls_ID = "bitm"

    Tag_Cls = BITM_Tag

    Endian = ">"

    Pixel_Root_Desc = { TYPE:Array, NAME:'Pixel_Root_Desc', SIZE:0,
                        SUB_STRUCT:{ TYPE:Array, NAME:'Bitmap_Pixels', SIZE:0,
                                     SUB_STRUCT:{ TYPE:Bytearray_Raw, NAME:'Pixels' }
                                     }
                        }
    

    Sprites_Desc = { TYPE:Struct, SIZE:32, GUI_NAME:"Sprite",
                     0:{ TYPE:UInt16, OFFSET:0, GUI_NAME:"Bitmap Index" },
                     1:{ TYPE:Float,  OFFSET:8, GUI_NAME:"Left Side" },
                     2:{ TYPE:Float, OFFSET:12, GUI_NAME:"Right Side" },
                     3:{ TYPE:Float, OFFSET:16, GUI_NAME:"Top Side" },
                     4:{ TYPE:Float, OFFSET:20, GUI_NAME:"Bottom Side" },
                     5:{ TYPE:Struct, OFFSET:24, GUI_NAME:"Registration Point",
                         0:{ TYPE:Float, OFFSET:0, GUI_NAME:"x" },
                         1:{ TYPE:Float, OFFSET:4, GUI_NAME:"y" }
                         }
                     }

    Sequences_Desc = { TYPE:Struct, SIZE:64, GUI_NAME:"Sequence",
                       0:{ TYPE:Str_Latin1, OFFSET:0, GUI_NAME:"Sequence Name", SIZE:32 },
                       1:{ TYPE:UInt16, OFFSET:32, GUI_NAME:"First Bitmap Index" },
                       2:{ TYPE:UInt16, OFFSET:34, GUI_NAME:"Bitmap Count" },
                       3:{ TYPE:Reflexive, OFFSET:52, GUI_NAME:"Sprites",
                           INCLUDE:Reflexive_Struct,
                           CHILD:{TYPE:Array,  NAME:"Sprite_Block_Array",
                                  MAX:64, SIZE:".Count",
                                  SUB_STRUCT:Sprites_Desc
                                  }
                           }
                       }

    Bitmaps_Desc = { TYPE:Struct, SIZE:48, GUI_NAME:"Bitmap",
                     0:{ TYPE:UInt32, OFFSET:0,  GUI_NAME:"BITM Cls ID",
                         EDITABLE:False, DEFAULT:"bitm" },
                     1:{ TYPE:UInt16, OFFSET:4, GUI_NAME:"Width"},
                     2:{ TYPE:UInt16, OFFSET:6, GUI_NAME:"Height"},
                     3:{ TYPE:UInt16, OFFSET:8, GUI_NAME:"Depth"},
                     4:{ TYPE:Enum16, OFFSET:10, GUI_NAME:"Type",
                         0:{GUI_NAME:"Texture 2D"},
                         1:{GUI_NAME:"Texture 3D"},
                         2:{GUI_NAME:"Cubemap"},
                         3:{GUI_NAME:"White"}
                         },
                     5:{ TYPE:Enum16, OFFSET:12, GUI_NAME:"Format",
                         0:{GUI_NAME:"A8", VALUE:0},
                         1:{GUI_NAME:"Y8", VALUE:1},
                         2:{GUI_NAME:"AY8", VALUE:2},
                         3:{GUI_NAME:"A8Y8", VALUE:3},
                         #4:{GUI_NAME:"-unused1-"},
                         #5:{GUI_NAME:"-unused2-"},
                         4:{GUI_NAME:"R5G6B5", VALUE:6},
                         #7:{GUI_NAME:"-unused3-"},
                         5:{GUI_NAME:"A1R5G5B5", VALUE:8},
                         6:{GUI_NAME:"A4R4G4B4", VALUE:9},
                         7:{GUI_NAME:"X8R8G8B8", VALUE:10},
                         8:{GUI_NAME:"A8R8G8B8", VALUE:11},
                         #12:{GUI_NAME:"-unused4-"},
                         #13:{GUI_NAME:"-unused5-"},
                         9:{GUI_NAME:"DXT1", VALUE:14},
                         10:{GUI_NAME:"DXT3", VALUE:15},
                         11:{GUI_NAME:"DXT5", VALUE:16},
                         12:{GUI_NAME:"P8-bump", VALUE:17}
                         },
                     6:{ TYPE:Bool16, OFFSET:14, GUI_NAME:"Flags",
                         0:{GUI_NAME:"Power of 2 dim", VALUE:1},
                         1:{GUI_NAME:"Compressed", VALUE:2},
                         2:{GUI_NAME:"Palletized", VALUE:4},
                         3:{GUI_NAME:"Swizzled", VALUE:8},
                         4:{GUI_NAME:"Linear", VALUE:16},
                         5:{GUI_NAME:"V16U16", VALUE:32},
                         6:{GUI_NAME:"Made by arsenic", VALUE:128}
                         },
                     7:{TYPE:Struct, OFFSET:16, GUI_NAME:"Registration Point",
                        0:{ TYPE:UInt16, OFFSET:0, GUI_NAME:"X" },
                        1:{ TYPE:UInt16, OFFSET:2, GUI_NAME:"Y" }
                        },
                     8:{ TYPE:UInt16, OFFSET:20, GUI_NAME:"Mipmaps" },
                     9:{ TYPE:UInt16, OFFSET:22, GUI_NAME:"Pixels"},
                     10:{ TYPE:UInt32, OFFSET:24, GUI_NAME:"Pixels Offset"},
                     11:{ TYPE:UInt32, OFFSET:28, GUI_NAME:"Bitmap_ID_Unknown_1" },
                     12:{ TYPE:UInt32, OFFSET:32, GUI_NAME:"Bitmap_ID_Unknown_2" },
                     13:{ TYPE:SInt32, OFFSET:36, GUI_NAME:"Bitmap_Data_Pointer" },
                     14:{ TYPE:UInt32, OFFSET:40, GUI_NAME:"Bitmap_ID_Unknown_3" },
                     15:{ TYPE:UInt32, OFFSET:44, GUI_NAME:"Base Address" }
                     }
    
    Tag_Structure = {TYPE:Container, GUI_NAME:"bitmap",
                     0:Combine( {1:{ DEFAULT:"bitm" },
                                 5:{ DEFAULT:7 }
                                 }, Tag_Header),
                     
                     1:{ TYPE:Struct, SIZE:108, GUI_NAME:"Data",
                          0:{ TYPE:Enum16, OFFSET:0, GUI_NAME:"Type",
                              0:{GUI_NAME:"Textures 2D"},
                              1:{GUI_NAME:"Textures 3D"},
                              2:{GUI_NAME:"Cubemaps"},
                              3:{GUI_NAME:"Sprites"},
                              4:{GUI_NAME:"Interface bitmaps"}
                              },
                          1:{ TYPE:Enum16, OFFSET:2, GUI_NAME:"Format",
                              0:{GUI_NAME:"Color key transparency"},
                              1:{GUI_NAME:"Explicit alpha"},
                              2:{GUI_NAME:"Interpolated alpha"},
                              3:{GUI_NAME:"Color 16bit"},
                              4:{GUI_NAME:"Color 32bit"},
                              5:{GUI_NAME:"Monochrome"}
                              },
                          2:{ TYPE:Enum16, OFFSET:4, GUI_NAME:"Usage",
                              0:{GUI_NAME:"Alpha-blend"},
                              1:{GUI_NAME:"Default"},
                              2:{GUI_NAME:"Height map"},
                              3:{GUI_NAME:"Detail map"},
                              4:{GUI_NAME:"Light map"},
                              5:{GUI_NAME:"Vector map"}
                              },
                          3:{ TYPE:Bool16, OFFSET:6, GUI_NAME:"Flags",
                              0:{GUI_NAME:"Enable diffusion dithering"},
                              1:{GUI_NAME:"Disable height map compression"},
                              2:{GUI_NAME:"Uniform sprite sequences"},
                              3:{GUI_NAME:"Sprite bug fix"},
                              4:{GUI_NAME:"Processed by reclaimer"}
                              },
                          4:{ TYPE:Float, OFFSET:8, GUI_NAME:"Detail Fade Factor",
                              MIN:0.0 , MAX:1.0},
                          5:{ TYPE:Float, OFFSET:12, GUI_NAME:"Sharpen Amount",
                              MIN:0.0 , MAX:1.0},
                          6:{ TYPE:Float, OFFSET:16, GUI_NAME:"Bump Height"},#repeats
                          7:{ TYPE:Enum16, OFFSET:20, GUI_NAME:"Sprite Budget Size",
                              0:{GUI_NAME:"32x32",   NAME:"x32"},
                              1:{GUI_NAME:"64x64",   NAME:"x64"},
                              2:{GUI_NAME:"128x128", NAME:"x128"},
                              3:{GUI_NAME:"256x256", NAME:"x256"},
                              4:{GUI_NAME:"512x512", NAME:"x512"}
                              },
                          8:{ TYPE:UInt16, OFFSET:22, GUI_NAME:"Sprite Budget Count" },
                          9:{ TYPE:UInt16, OFFSET:24, GUI_NAME:"Color Plate Width"},
                          10:{ TYPE:UInt16, OFFSET:26, GUI_NAME:"Color Plate Height"},
                          11:{ TYPE:Raw_Data_Ref, OFFSET:28, GUI_NAME:"Compressed Color Plate Data",
                               EDITABLE:False,
                               INCLUDE:Raw_Data_Ref_Struct,
                               CHILD:{TYPE:Bytearray_Raw, NAME:"Data",
                                      VISIBLE:False, SIZE:".Count"}
                               },
                          12:{ TYPE:Raw_Data_Ref, OFFSET:48, GUI_NAME:"Processed Pixel Data",
                               EDITABLE:False,
                               INCLUDE:Raw_Data_Ref_Struct,
                               CHILD:{TYPE:Bytearray_Raw, NAME:"Data",
                                      VISIBLE:False, SIZE:".Count"}
                               },
                          13:{ TYPE:Float, OFFSET:68, GUI_NAME:"Blur Filter Size",#[0,10]
                               MIN:0.0 , MAX:10.0},
                          14:{ TYPE:Float, OFFSET:72, GUI_NAME:"Alpha Bias",#[-1,1]
                               MIN:-1.0 , MAX:1.0},
                          15:{ TYPE:UInt16, OFFSET:76, GUI_NAME:"Mipmap Levels", MIN:0},
                          16:{ TYPE:Enum16, OFFSET:78, GUI_NAME:"Sprite Usage",
                               0:{GUI_NAME:"Blend\Add\Subtract\Max"},
                               1:{GUI_NAME:"Multiply\Min"},
                               2:{GUI_NAME:"Double Multiply"}
                               },
                          17:{ TYPE:UInt16, OFFSET:80, GUI_NAME:"Sprite Spacing" },
                         
                          18:{ TYPE:Reflexive, OFFSET:84, GUI_NAME:"Sequences",
                               INCLUDE:Reflexive_Struct,
                               CHILD:{TYPE:Array,   NAME:"Sequence_Block_Array",
                                      MAX:256, SIZE:".Count",
                                      SUB_STRUCT:Sequences_Desc
                                      }
                               },
                          19:{ TYPE:Reflexive, OFFSET:96, GUI_NAME:"Bitmaps",
                               INCLUDE:Reflexive_Struct,
                               CHILD:{TYPE:Array, NAME:"Bitmap_Block_Array",
                                      MAX:32767, SIZE:".Count",
                                      SUB_STRUCT:Bitmaps_Desc
                                      }
                               }
                          }
                     }


    Structures = {'Pixel_Root_Desc':Pixel_Root_Desc}
