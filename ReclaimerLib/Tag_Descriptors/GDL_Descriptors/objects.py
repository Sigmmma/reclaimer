from supyr_struct.Defs.Tag_Def import Tag_Def
from supyr_struct.Defs.Common_Structures import *
from ...Tag_Constructors.GDL_Constructors.Field_Types import *
from .Objs.objects import Objects_PS2_Tag

def Construct():
    return OBJECTS_PS2_Definition

class OBJECTS_PS2_Definition(Tag_Def):
    
    Tag_Ext = ".ps2"
    
    Cls_ID = "objects.ps2"

    #The constructor used to build this definitions Tag_Obj
    Tag_Obj = Objects_PS2_Tag

    Endianness = "<"

    #ELEMENTS: { 0:{NAME:"Point_List"},
    #            1:{NAME:"Line_List"},
    #            2:{NAME:"Triangle_List"},
    #            3:{NAME:"Triangle_Strip"},
    #            4:{NAME:"Triangle_Fan"},
    #            5:{NAME:"Quad_List"},
    #            6:{NAME:"Quad_Strip"},
    #            }
    #ELEMENTS: { 0:{NAME:"Off", VALUE:0},
    #            1:{NAME:"YY", VALUE:1},
    #            2:{NAME:"NN", VALUE:2},
    #            3:{NAME:"See_All", VALUE:4},
    #            4:{NAME:"All_Models", VALUE:16},
    #            5:{NAME:"All_Objs", VALUE:32},
    #            6:{NAME:"All_Subobjs", VALUE:64},
    #            7:{NAME:"All_Tris", VALUE:128},
    #            8:{NAME:"Search_Model", VALUE:512},
    #            9:{NAME:"Search_Obj", VALUE:1024},
    #            10:{NAME:"Wait_Count", VALUE:4096},
    #            11:{NAME:"Show_Sel", VALUE:8192},
    #            12:{NAME:"Search_Q", VALUE:16384},
    #            13:{NAME:"Break_Pt", VALUE:32768},
    #            14:{NAME:"Searching", VALUE:1536},
    #            15:{NAME:"New_Search", VALUE:1777},
    #            16:{NAME:"New_Search_HM", VALUE:1761},
    #            17:{NAME:"New_Select", VALUE:45056},
    #            18:{NAME:"Show_All", VALUE:36868},
    #            19:{NAME:"Select_All", VALUE:45296},
    #            20:{NAME:"Cont_Search", VALUE:61440}
    #            }
    
    Vertex_8_Block = { TYPE:Struct, SIZE:3, NAME:"Vertex_8",
                       ATTRIBUTES:X_Y_Z_Byte
                       }
    
    Vertex_16_Block = { TYPE:Struct, SIZE:6, NAME:"Vertex_16",
                        ATTRIBUTES:X_Y_Z_Short
                        }
    
    UV_8_Block = { TYPE:Struct, SIZE:2, NAME:"UV_8",
                   ATTRIBUTES:U_V_Byte
                   }
    
    UV_16_Block = { TYPE:Struct, SIZE:4, NAME:"UV_16",
                    ATTRIBUTES:U_V_Short
                    }

    #figure out how the normals are compressed
    #they are probably either 5,5,5, 5,6,5, 6,5,5, or 5,5,6
    V_Normal_16_Block = { TYPE:Bit_Struct, NAME:"V_Normal_16",
                          ATTRIBUTES:Compressed_Normal_16
                          }
    
    
    '''When the type is Subobject, the Count is how ever many
    vertices all its primitives contain(minus the zeroed ones)'''

    '''When the type is Vertex, the last vertex is
    always X=0, Y=0, Z=0. not sure why, but it is.'''
    Primitive = { TYPE:Struct, NAME:"Primitive", ALIGN:4,
                  0:{ TYPE:UInt8, NAME:"Unknown_0", DEFAULT:4 },
                  1:{ TYPE:UInt8, NAME:"Unknown_1" },
                  2:{ TYPE:UInt8, NAME:"Count" },
                  3:{ TYPE:UInt8, NAME:"Type",
                      ELEMENTS: { 0:{NAME:"None",        VALUE:0},
                                  1:{NAME:"Unknown",     VALUE:20},
                                  2:{NAME:"Point_2D_F",  VALUE:45},
                                  3:{NAME:"Subobject",   VALUE:96},
                                  4:{NAME:"UV_16",       VALUE:101},#just a guess
                                  5:{NAME:"UV_8",        VALUE:102},
                                  6:{NAME:"Vertex_16",   VALUE:105},
                                  7:{NAME:"Vertex_8",    VALUE:106},
                                  8:{NAME:"V_Normal_16", VALUE:111},
                                 }
                      },
                  #CHILD:{ TYPE:Array, NAME:"Primitive_Array",
                  #        SIZE:'.Count', ARRAY_ELEMENT:{ }
                  #        }
                  }
    Pointer32
    #sub-objects are for things where you may have multiple textures on one mesh.
    #in that case each subobject would have one texture.
    Sub_Object_Block = { TYPE:Struct, GUI_NAME:"Sub-Object",
                         0:{ TYPE:UInt16, OFFSET:0, GUI_NAME:"QWC"},
                         1:{ TYPE:UInt16, OFFSET:2, GUI_NAME:"Texture Index"},
                         2:{ TYPE:UInt16, OFFSET:4, GUI_NAME:"LM Index"},
                         3:{ TYPE:SInt16, OFFSET:6, GUI_NAME:"Lod K"},
                         }

    Object_Block = { TYPE:Struct, SIZE:64, GUI_NAME:"Object",
                     0:{ TYPE:Float,  OFFSET:0, GUI_NAME:"InvRad"},
                     1:{ TYPE:Float,  OFFSET:4, GUI_NAME:"BndRad"},
                     2:{ TYPE:UInt32, OFFSET:8, GUI_NAME:"Flags",
                         FLAGS: { 0:{ NAME:"Non_Lit",   VALUE:0x0 },
                                  1:{ NAME:"Fmt_Basic", VALUE:0x0 },
                                  
                                  2:{ NAME:"Alpha",     VALUE:0x1 },
                                  3:{ NAME:"V_Normals", VALUE:0x2 },
                                  4:{ NAME:"V_Colors",  VALUE:0x4 },
                                  5:{ NAME:"Mesh",      VALUE:0x8 },
                                  6:{ NAME:"TEX2",      VALUE:0x10 },
                                  7:{ NAME:"Lmap",      VALUE:0x20 },
                                 
                                  8:{ NAME:"Sharp",   VALUE:0x40 },
                                  9:{ NAME:"Blur",    VALUE:0x80 },
                                  10:{ NAME:"Chrome", VALUE:0x100 },
                                 
                                  11:{ NAME:"Error",  VALUE:0x200 },
                                  12:{ NAME:"Sort_A", VALUE:0x400 },
                                  13:{ NAME:"Sort",   VALUE:0x800 },
                                 
                                  14:{ NAME:"Fmt_Mask", VALUE:0xF000 },
                                  15:{ NAME:"Pre_Lit",  VALUE:0x10000 },
                                  16:{ NAME:"Lit_Mask", VALUE:0xF0000 },
                                  17:{ NAME:"Lmap_Lit", VALUE:0x20000 },
                                  18:{ NAME:"Norm_Lit", VALUE:0x30000 },
                                  19:{ NAME:"Dyn_Lit",  VALUE:0x100000 },
                                  }
                         },
                    
                     3:{ TYPE:SInt32, OFFSET:12, GUI_NAME:'Sub-Objects Count' },
                     4:{ TYPE:Struct, OFFSET:16, GUI_NAME:"Sub-Object 0",
                         ATTRIBUTES:Sub_Object_Block },
               
                     5:{ TYPE:Pointer32, OFFSET:24, GUI_NAME:'Sub-Objects Pointer' },
                     6:{ TYPE:Pointer32, OFFSET:28, GUI_NAME:'Sub-Object Models Pointer' },

                     #the number of unique verts in the object.
                     #probably number of verts before compiling
                     7:{ TYPE:SInt32, OFFSET:32, GUI_NAME:"Vert Count" },
                     8:{ TYPE:SInt32, OFFSET:36, GUI_NAME:"Tri Count" },
                     9:{ TYPE:SInt32, OFFSET:40, GUI_NAME:"ID Num"},
                     
                     #pointer to the obj def that this model uses
                     10:{ TYPE:Pointer32, OFFSET:44, GUI_NAME:"Obj Def"},
                    
                     CHILD:{ TYPE:Container, NAME:"Data",
                             0:{ TYPE:Array, GUI_NAME:"Sub-Objects",
                                 POINTER:"..Sub_Objects_Pointer",
                                 CARRY_OFF:False, SIZE:Sub_Objects_Size,
                                 ARRAY_ELEMENT:Sub_Object_Block
                                 },
                             1:{ TYPE:Array, GUI_NAME:"Sub-Object_Models",
                                 POINTER:"..Sub_Object_Models_Pointer",
                                 CARRY_OFF:False, SIZE:"..Sub_Objects_Count",
                                 ARRAY_ELEMENT:Primitive
                                 }
                             }
                     }


    Bitmap_Block = { TYPE:Struct, SIZE:64, GUI_NAME:"Bitmap",
                     #palletized textures are in either 16 or 256 color format
                     #   if a texture has a 16 color palette then each byte counts as
                     #   2 pixels with the least significant 4 bits being the left pixel
                     #portraits used as background on player bar are in ABGR_8888_IDX_4

                     #color data is stored in RGBA order
                     #8x8 seems to be the smallest a texture is allowed to be
                     
                     0:{ TYPE:UInt8,  OFFSET:0, GUI_NAME:"Bitmap Format",
                         ELEMENTS:{ 0:{NAME:"ABGR_1555", VALUE:0 },
                                    1:{NAME:"XBGR_1555", VALUE:1 },
                                    2:{NAME:"ABGR_8888", VALUE:2 },
                                    3:{NAME:"XBGR_8888", VALUE:3 },
                                    4:{NAME:"ABGR_1555_IDX_4", VALUE:16 },
                                    5:{NAME:"XBGR_1555_IDX_4", VALUE:17 },
                                    6:{NAME:"ABGR_8888_IDX_4", VALUE:34 },
                                    7:{NAME:"XBGR_8888_IDX_4", VALUE:35 },
                                    8:{NAME:"ABGR_1555_IDX_8", VALUE:48 },
                                    9:{NAME:"XBGR_1555_IDX_8", VALUE:49 },
                                    10:{NAME:"IDXA_88",        VALUE:56 },
                                    11:{NAME:"ABGR_8888_IDX_8",VALUE:66 },
                                    12:{NAME:"XBGR_8888_IDX_8",VALUE:67 },
                                    13:{NAME:"A_8_IDX_8", VALUE:130 },
                                    14:{NAME:"I_8_IDX_8", VALUE:131 },
                                    15:{NAME:"A_4_IDX_4", VALUE:146 },
                                    16:{NAME:"I_4_IDX_4", VALUE:147 },
                                    }
                         },
                     1:{ TYPE:SInt8,  OFFSET:1, GUI_NAME:"Lod K"},
                     2:{ TYPE:UInt8,  OFFSET:2, GUI_NAME:"Mipmap Count"},
                     
                     #Width-64 == int(ceil(width/64))
                     3:{ TYPE:UInt8,  OFFSET:3, GUI_NAME:"Width-64"},
                     4:{ TYPE:UInt16, OFFSET:4, GUI_NAME:"Log2 of Width"},
                     5:{ TYPE:UInt16, OFFSET:6, GUI_NAME:"Log2 of Height"},
                    
                     6:{ TYPE:UInt16, OFFSET:8, GUI_NAME:"Flags",
                         FLAGS: { 0:{NAME:"Halfres",   VALUE:0x1},
                                  1:{NAME:"See Alpha", VALUE:0x2},
                                  2:{NAME:"Clamp U",   VALUE:0x4},
                                  3:{NAME:"Clamp V",   VALUE:0x8},
                                  4:{NAME:"Animation", VALUE:0x10},
                                  5:{NAME:"Eternal",   VALUE:0x20},
                                  6:{NAME:"Tex Shift", VALUE:0x40},
                                  7:{NAME:"Has Alpha", VALUE:0x80},
                                  8:{NAME:"INVALID",   VALUE:0x100},
                                  9:{NAME:"Dual Tex",  VALUE:0x200},
                                  }
                         },
                        
                     7:{ TYPE:UInt16,  OFFSET:10, GUI_NAME:"Tex Palette Index"},
                     
                     #pointer to the texture in the BITMAPS.ps2
                     #where the pixel texture data is located
                     8:{ TYPE:Pointer32,  OFFSET:12, GUI_NAME:"Tex Base"},
                     
                     9:{ TYPE:UInt16,  OFFSET:16, GUI_NAME:"Tex Palette Count"},
                     10:{ TYPE:UInt16, OFFSET:18, GUI_NAME:"Tex Shift Index"},
                    
                     #the number of bitmaps after the current
                     #one that are included in the animation
                     #animated textures can have different formats for each frame
                     11:{ TYPE:UInt16, OFFSET:20, GUI_NAME:"Frame Count"},
                    
                     12:{ TYPE:UInt16, OFFSET:22, GUI_NAME:"Width"},
                     13:{ TYPE:UInt16, OFFSET:24, GUI_NAME:"Height"},
                     
                     #related to resolution as a texture with half the
                     #size of another texture has this int halved as well
                     14:{ TYPE:UInt16, OFFSET:26, GUI_NAME:"Size"},

                     #points to the bitmap def that this bitmap uses
                     #this seems to be the same pointer for each texture in
                     #an animation, except for ones of a different format
                     15:{ TYPE:Pointer32, OFFSET:28, GUI_NAME:"Bitmap Def"},
                    
                     16:{ TYPE:UInt32_Array, OFFSET:32, GUI_NAME:"Tex 0", SIZE:8},
                     17:{ TYPE:UInt32_Array, OFFSET:40, GUI_NAME:"Mip TBP 1", SIZE:8},
                     18:{ TYPE:UInt32_Array, OFFSET:48, GUI_NAME:"Mip TBP 2", SIZE:8},
                     
                     19:{ TYPE:UInt16_Array, OFFSET:56, GUI_NAME:"VRAM Address", SIZE:4},
                     20:{ TYPE:UInt16_Array, OFFSET:60, GUI_NAME:"CLUT Address", SIZE:4}

                     
                     #To animate a series of bitmaps, take the first bitmap and lets call it "base".
                     #    In the chain and make a sequence block aiming to base. Create another bitmap
                     #    block to act as the main object (so multiple, different, animations can exist).
                     #    In the anim.ps2 create a texture animation aiming to the main sequence
                     #    and aim the start of the animation to the base sequence.
                     }


    Tag_Structure = {TYPE:Struct, SIZE:160, GUI_NAME:"GDL Objects Resource",
                     0:{ TYPE:Str_Latin1, OFFSET:0, GUI_NAME:"Dir Name", SIZE:32},
                     1:{ TYPE:Str_Latin1, OFFSET:32, GUI_NAME:"Model Name", SIZE:32},
                     2:{ TYPE:UInt32, OFFSET:64, GUI_NAME:"Version", DEFAULT:4027252749},
                     
                     3:{ TYPE:UInt32, OFFSET:68, GUI_NAME:"Object Count" },
                     4:{ TYPE:UInt32, OFFSET:72, GUI_NAME:"Bitmap Count" },
                     5:{ TYPE:UInt32, OFFSET:76, GUI_NAME:"Object Def Count" },
                     6:{ TYPE:UInt32, OFFSET:80, GUI_NAME:"Bitmap Def Count" },
                     
                     7:{ TYPE:Pointer32, OFFSET:84, GUI_NAME:"Object Pointer" },
                     8:{ TYPE:Pointer32, OFFSET:88, GUI_NAME:"Bitmap Pointer" },
                     9:{ TYPE:Pointer32, OFFSET:92, GUI_NAME:"Object Def Pointer" },
                     10:{ TYPE:Pointer32, OFFSET:96, GUI_NAME:"Bitmap Def Pointer" },
                     
                     11:{ TYPE:Pointer32, OFFSET:100, GUI_NAME:"Sub-Objects Pointer"},
                     12:{ TYPE:Pointer32, OFFSET:104, GUI_NAME:"Geometry Pointer"},
                     
                     13:{ TYPE:UInt32, OFFSET:108, GUI_NAME:"Filesize", NAME:"Obj End"},
                   
                     14:{ TYPE:UInt32, OFFSET:112, GUI_NAME:"Tex Start"},
                     15:{ TYPE:UInt32, OFFSET:116, GUI_NAME:"Tex End"},

                     16:{ TYPE:UInt32, OFFSET:120, GUI_NAME:"Tex Bits"},
                     
                     17:{ TYPE:UInt16, OFFSET:124, NAME:"LMTex First"},
                     18:{ TYPE:UInt16, OFFSET:126, NAME:"LMTex Num"},
                     19:{ TYPE:UInt32, OFFSET:128, NAME:"Tex Info"},

                     CHILD:{TYPE:Container, GUI_NAME:"Data",
                            0:{TYPE:Array, GUI_NAME:"Objects",
                               SIZE:'..Object_Count', POINTER:'..Object_Pointer',
                               ARRAY_ELEMENT:Object_Block,
                               },
                            1:{TYPE:Array, GUI_NAME:"Bitmaps",
                               SIZE:'..Bitmap_Count', POINTER:'..Bitmap_Pointer',
                               ARRAY_ELEMENT:Bitmap_Block
                               },
                            2:{TYPE:Array, GUI_NAME:"Object Defs",
                               SIZE:'..Object_Def_Count', POINTER:'..Object_Def_Pointer',
                               ARRAY_ELEMENT:{ TYPE:Struct, SIZE:24, GUI_NAME:"Object Def",
                                               0:{ TYPE:Str_Latin1, NAME:"Name", SIZE:16},
                                               1:{ TYPE:Float, NAME:"BndRad", GUI_NAME:"Bounding Radius"},
                                               2:{ TYPE:SInt16, NAME:"Index"},
                                               3:{ TYPE:SInt16, NAME:"NFrames"},
                                               }
                               },
                            3:{TYPE:Array, GUI_NAME:"Bitmap Defs",
                               SIZE:'..Bitmap_Def_Count', POINTER:'..Bitmap_Def_Pointer',
                               ARRAY_ELEMENT:{ TYPE:Struct, SIZE:36, GUI_NAME:"Bitmap Def",
                                               0:{ TYPE:Str_Latin1, OFFSET:0, NAME:"Name", SIZE:16},
                                               1:{ TYPE:UInt16, OFFSET:30, NAME:"Index"},
                                               2:{ TYPE:UInt16, OFFSET:32, NAME:"Width"},
                                               3:{ TYPE:UInt16, OFFSET:34, NAME:"Height"},
                                               }
                               }
                            }
                     }
