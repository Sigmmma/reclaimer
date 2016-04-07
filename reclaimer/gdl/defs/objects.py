from supyr_struct.defs.tag_def import TagDef
from supyr_struct.defs.common_descriptors import *
from ..fields import *
from .objs.objects import ObjectsPs2Tag

def get(): return objects_ps2_def

'''
( ("Point_List"),
  ("Line_List"),
  ("Triangle_List"),
  ("Triangle_Strip"),
  ("Triangle_Fan"),
  ("Quad_List"),
  ("Quad_Strip"),
)
( ("Off",               0),
  ("YY",                1),
  ("NN",                2),
  ("See_All",           4),
  ("All_Models",       16),
  ("All_Objs",         32),
  ("All_Subobjs",      64),
  ("All_Tris",        128),
  ("Search_Model",    512),
  ("Search_Obj",     1024),
  ("Wait_Count",     4096),
  ("Show_Sel",       8192),
  ("Search_Q",      16384),
  ("Break_Pt",      32768),
  ("Searching",      1536),
  ("New_Search",     1777),
  ("New_Search_HM",  1761),
  ("New_Select",    45056),
  ("Show_All",      36868),
  ("Select_All",    45296),
  ("Cont_Search",   61440)
  )
'''
vertex_8_block  = Struct("vertex_8",  INCLUDE=X_Y_Z_Byte)
vertex_16_block = Struct("vertex_16", INCLUDE=X_Y_Z_Short)

uv_8_block  = Struct("uv_8",  INCLUDE=U_V_Byte)
uv_16_block = Struct("uv_16", INCLUDE=U_V_Short)

#figure out how the normals are compressed
#they are probably either 5,5,5, 5,6,5, 6,5,5, or 5,5,6
v_normal_16_block = LBitStruct("v_normal_16", INCLUDE=Compressed_Normal_16)

    
'''When the type is Subobject, the Count is how ever many
vertices all its primitives contain(minus the zeroed ones)'''

'''When the type is Vertex, the last vertex is always set to
X=0, Y=0, Z=0. This must be to signal that the strip has ended.'''
primitive = Struct("Primitive",
    UInt8("Unknown_0", DEFAULT=4),
    UInt8("Unknown_1"),
    UInt8("Count"),
    UEnum8("Type",
        ("None",        0),
        ("Unknown",     20),
        ("Point_2D_F",  45),
        ("Subobject",   96),
        ("UV_16",       101),#just a guess
        ("UV_8",        102),
        ("Vertex_16",   105),
        ("Vertex_8",    106),
        ("V_Normal_16", 111),
        ),
    #CHILD=Array("primitive_array", SIZE='.count', SUB_STRUCT={} ),
    ALIGN=4
    )

#sub-objects are for things where you may have multiple textures on one mesh.
#in that case each subobject would have one texture.
sub_object_block = Struct("Sub-Object",
    LUInt16("QWC"),
    LUInt16("Texture Index"),
    LUInt16("LM Index"),
    LSInt16("Lod K")
    ) 

object_block = Struct("Object",
    LFloat("InvRad"),
    LFloat("BndRad"),
    Bool32("Flags",
        ("Non_Lit",   0x0),
        ("Fmt_Basic", 0x0),

        ("Alpha",     0x01),
        ("V_Normals", 0x02),
        ("V_Colors",  0x04),
        ("Mesh",      0x08),
        ("TEX2",      0x10),
        ("Lmap",      0x20),

        ("Sharp",  0x040),
        ("Blur",   0x080),
        ("Chrome", 0x100),

        ("Error",  0x200),
        ("Sort_A", 0x400),
        ("Sort",   0x800),

        ("Fmt_Mask", 0x00F000),
        ("Pre_Lit",  0x010000),
        ("Lit_Mask", 0x0F0000),
        ("Lmap_Lit", 0x020000),
        ("Norm_Lit", 0x030000),
        ("Dyn_Lit",  0x100000)
    ),

    LSInt32('Sub-Objects Count'),
    Struct("Sub-Object 0", INCLUDE=sub_object_block),

    LPointer32('Sub-Objects Pointer'),
    LPointer32('Sub-Object Models Pointer'),

    #the number of unique verts in the object.
    #probably number of verts before compiling
    LSInt32("Vert Count"),
    LSInt32("Tri Count"),
    LSInt32("ID Num"),

    #pointer to the obj def that this model uses
    LPointer32("Obj Def"),
    Pad(16),

    SIZE=64,
    
    CHILD=Container("Data",
        Array("Sub-Objects", SIZE=sub_objects_size,
              SUB_STRUCT=sub_object_block, POINTER="..Sub_Objects_Pointer"),
        Array("Sub-Object_Models", SIZE="..Sub_Objects_Count",
              SUB_STRUCT=primitive, POINTER="..Sub_Object_Models_Pointer")
        )
    )


bitmap_block = Struct("Bitmap",
    #palletized textures are in either 16 or 256 color format
    #   if a texture has a 16 color palette then each byte counts as
    #   2 pixels with the least significant 4 bits being the left pixel
    #portraits used as background on player bar are in ABGR_8888_IDX_4

    #color data is stored in RGBA order
    #8x8 seems to be the smallest a texture is allowed to be

    UEnum8("Format",
        ("ABGR_1555", 0),
        ("XBGR_1555", 1),
        ("ABGR_8888", 2),
        ("XBGR_8888", 3),
        ("ABGR_1555_IDX_4", 16),
        ("XBGR_1555_IDX_4", 17),
        ("ABGR_8888_IDX_4", 34),
        ("XBGR_8888_IDX_4", 35),
        ("ABGR_1555_IDX_8", 48),
        ("XBGR_1555_IDX_8", 49),
        ("IDXA_88",         56),
        ("ABGR_8888_IDX_8", 66),
        ("XBGR_8888_IDX_8", 67),
        ("A_8_IDX_8", 130),
        ("I_8_IDX_8", 131),
        ("A_4_IDX_4", 146),
        ("I_4_IDX_4", 147)
        ),
    SInt8("Lod K"),
    UInt8("Mipmap Count"),

    #Width-64 == int(ceil(width/64))
    UInt8("Width-64"),
    LUInt16("Log2 of Width"),
    LUInt16("Log2 of Height"),

    LBool16("Flags",
        ("Halfres",   0x001),
        ("See Alpha", 0x002),
        ("Clamp U",   0x004),
        ("Clamp V",   0x008),
        ("Animation", 0x010),
        ("External",  0x020),
        ("Tex Shift", 0x040),
        ("Has Alpha", 0x080),
        ("Invalid",   0x100),
        ("Dual Tex",  0x200)
        ),

    LUInt16("Tex Palette Index"),

    #pointer to the texture in the BITMAPS.ps2
    #where the pixel texture data is located
    LPointer32("Tex Base"),

    LUInt16("Tex Palette Count"),
    LUInt16("Tex Shift Index"),

    #the number of bitmaps after the current
    #one that are included in the animation
    #animated textures can have different formats for each frame
    LUInt16("Frame Count"),

    LUInt16("Width"),
    LUInt16("Height"),

    #related to resolution as a texture with half the
    #size of another texture has this int halved as well
    LUInt16("Size"),

    #points to the bitmap def that this bitmap uses
    #this seems to be the same pointer for each texture in
    #an animation, except for ones of a different format
    LPointer32("Bitmap Def"),

    LUInt32Array("Tex 0", SIZE=8),
    LUInt32Array("Mip TBP 1", SIZE=8),
    LUInt32Array("Mip TBP 2", SIZE=8),

    LUInt16Array("VRAM Address", SIZE=4),
    LUInt16Array("CLUT Address", SIZE=4),
    Pad(0),

    SIZE=64
    #To animate a series of bitmaps, take the first bitmap and lets call it "base".
    #    In the chain and make a sequence block aiming to base. Create another bitmap
    #    block to act as the main object (so multiple, different, animations can exist).
    #    In the anim.ps2 create a texture animation aiming to the main sequence
    #    and aim the start of the animation to the base sequence.
    )

objects_header = Struct('Header',
    StrRawLatin1("Dir Name",   SIZE=32),
    StrRawLatin1("Model Name", SIZE=32),
    LUInt32("Version",         DEFAULT=0x0D000BF0),

    LUInt32("Objects Count"),
    LUInt32("Bitmaps Count"),
    LUInt32("Object Defs Count"),
    LUInt32("Bitmap Defs Count"),

    LPointer32("Objects Pointer"),
    LPointer32("Bitmaps Pointer"),
    LPointer32("Object Defs Pointer"),
    LPointer32("Bitmap Defs Pointer"),

    LPointer32("Sub-Objects Pointer"),
    LPointer32("Geometry Pointer"),

    LUInt32("Obj_End"),

    LUInt32("Tex Start"),
    LUInt32("Tex End"),

    LUInt32("Tex Bits"),

    LUInt16("LMTex First"),
    LUInt16("LMTex Num"),
    LUInt32("Tex Info"),
    Pad(28),
    SIZE=160
    )


object_def = Struct("Object Def",
    StrRawLatin1("Name", SIZE=16),
    LFloat("BndRad", GUI_NAME="Bounding Radius"),
    LSInt16("Index"),
    LSInt16("NFrames"),
    SIZE=24
    )
   
bitmap_def = Struct("Bitmap Def",
    StrRawLatin1("Name", SIZE=16),
    Pad(14),
    LUInt16("Index"),
    LUInt16("Width"),
    LUInt16("Height"),
    SIZE=36
    )

objects_ps2_def = TagDef(
    objects_header,
    
    Array("Objects",
        SIZE='.Header.Objects_Count',
        POINTER='.Header.Objects_Pointer',
        SUB_STRUCT=object_block,
        ),
    Array("Bitmaps",
        SIZE='.Header.Bitmaps_Count',
        POINTER='.Header.Bitmaps_Pointer',
        SUB_STRUCT=bitmap_block
        ),
    Array("Object Defs",
        SIZE='.Header.Object_Defs_Count',
        POINTER='.Header.Object_Defs_Pointer',
        SUB_STRUCT=object_def
        ),
    Array("Bitmap Defs",
        SIZE='.Header.Bitmap_Defs_Count',
        POINTER='.Header.Bitmap_Defs_Pointer',
        SUB_STRUCT=bitmap_def
        ),
    
    NAME="GDL Objects Resource",
    ext=".ps2", def_id="objects", tag_cls=ObjectsPs2Tag
    )
