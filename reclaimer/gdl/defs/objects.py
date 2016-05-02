from supyr_struct.defs.tag_def import TagDef
from supyr_struct.defs.common_descriptors import *
from ..fields import *
from .objs.objects import ObjectsPs2Tag

def get(): return objects_ps2_def

def get_uv32_size(block=None, parent=None, attr_index=None,
                   rawdata=None, new_value=None, *args, **kwargs):
    if block and parent is None:
        parent = block.PARENT
    if new_value is not None:
        parent.length = new_value//8
    return parent.length*8

def get_uv16_size(block=None, parent=None, attr_index=None,
                   rawdata=None, new_value=None, *args, **kwargs):
    if block and parent is None:
        parent = block.PARENT
    if new_value is not None:
        parent.length = new_value//4
    return parent.length*4

def get_uv8_size(block=None, parent=None, attr_index=None,
                   rawdata=None, new_value=None, *args, **kwargs):
    if block and parent is None:
        parent = block.PARENT
    if new_value is not None:
        parent.length = new_value//2
    return parent.length*2

def get_vert32_size(block=None, parent=None, attr_index=None,
                    rawdata=None, new_value=None, *args, **kwargs):
    if block and parent is None:
        parent = block.PARENT
    if new_value is not None:
        parent.length = new_value//12
    return parent.length*12

def get_vert16_size(block=None, parent=None, attr_index=None,
                    rawdata=None, new_value=None, *args, **kwargs):
    if block and parent is None:
        parent = block.PARENT
    if new_value is not None:
        parent.length = new_value//6
    return parent.length*6

def get_vert8_size(block=None, parent=None, attr_index=None,
                   rawdata=None, new_value=None, *args, **kwargs):
    if block and parent is None:
        parent = block.PARENT
    if new_value is not None:
        parent.length = new_value//3
    return parent.length*3

def get_primitive_type(block=None, parent=None, attr_index=None,
                       rawdata=None, new_value=None, *args, **kwargs):
    if rawdata is not None:
        if rawdata.peek(4)[3] not in (0,20,23,45,96,100,101,102,104,105,106,108,111):
            print(rawdata.peek(4)[3], rawdata.tell())
    
        return rawdata.peek(4)[3]

def has_next_primitive(block=None, parent=None, attr_index=None,
                       rawdata=None, new_value=None, *args, **kwargs):
    if rawdata is not None:
        if parent is None:
            parent = block.PARENT
        terminated = len(parent) != 0 and parent[-1].sentinel == 0
        return rawdata.peek(4)[3] != 96 and not terminated
        return rawdata.peek(4)[3] != 96


get_vnorm16_size = get_uv8_size

#########################################################
'''FOR TEXTURES.PS2, RED AND BLUE CHANNELS ARE SWAPPED'''
#########################################################

primitive_types = (
    ("terminator", 0),
    ("multi_polyinst", 20),
    ("polyinst_link",  23),
    #("float2d",   45),
    ("subobject", 96),
    ("uv32",     100),
    ("uv16",     101),
    ("uv8",      102),
    ("vert32",   104),
    ("vert16",   105),
    ("vert8",    106),
    ("polyinst", 108),
    ("vnorm16",  111),
    )

'''The last vertex is always set to X=0, Y=0, Z=0.
This must be to signal that the strip has ended.'''

#figure out how the normals are compressed
#they are probably either 5,5,5, 5,6,5, 6,5,5, or 5,5,6

unknown_primitive = Container("unknown primitive",
    BytesRaw("unknown", SIZE=3, DEFAULT=b'\x00\x00\x00'),
    UInt8("sentinel"),
    ALIGN=4,
    )

terminator = Struct("terminator",
    Pad(3),
    UInt8("sentinel"),
    ALIGN=4,
    )

multi_polyinst = Struct("multi polyinst",
    Pad(3),
    UInt8("sentinel", DEFAULT=20),
    ALIGN=4,
    )

polyinst_link = Struct("polyinst link",
    Pad(3),
    UInt8("sentinel", DEFAULT=23),
    ALIGN=4,
    )

#float_2d = Container("float 2d",
#    Pad(3),#BytesRaw("unknown0", SIZE=3, DEFAULT=b'\x00\x00\x00'),
#    UInt8("sentinel", DEFAULT=45),
#    Float("x"),
#    Float("y"),
#    ALIGN=4,
#    )

uv_32bit = Container("uv 32bit",
    BytesRaw("unknown", SIZE=2, DEFAULT=b'\x04\x80'),
    UInt8("length"),
    UInt8("sentinel", DEFAULT=100),
    UInt32Array('data', SIZE=get_uv32_size),
    ALIGN=4,
    )

uv_16bit = Container("uv 16bit",
    BytesRaw("unknown", SIZE=2, DEFAULT=b'\x04\x80'),
    UInt8("length"),
    UInt8("sentinel", DEFAULT=101),
    UInt16Array('data', SIZE=get_uv16_size),
    ALIGN=4,
    )

uv_8bit = Container("uv 8bit",
    BytesRaw("unknown", SIZE=2, DEFAULT=b'\x04\x80'),
    UInt8("length"),
    UInt8("sentinel", DEFAULT=102),
    UInt8Array('data', SIZE=get_uv8_size),
    ALIGN=4,
    )

vert_32bit = Container("vert 32bit",
    BytesRaw("unknown", SIZE=2, DEFAULT=b'\x01\x80'),
    UInt8("length"),
    UInt8("sentinel", DEFAULT=104),
    SInt32Array('data', SIZE=get_vert32_size),
    ALIGN=4,
    )

vert_16bit = Container("vert 16bit",
    BytesRaw("unknown", SIZE=2, DEFAULT=b'\x01\x80'),
    UInt8("length"),
    UInt8("sentinel", DEFAULT=105),
    SInt16Array('data', SIZE=get_vert16_size),
    ALIGN=4,
    )

vert_8bit = Container("vert 8bit",
    BytesRaw("unknown", SIZE=2, DEFAULT=b'\x01\x80'),
    UInt8("length"),
    UInt8("sentinel", DEFAULT=106),
    SInt8Array('data', SIZE=get_vert8_size),
    ALIGN=4,
    )

vnorm_16bit = Container("vnorm 16bit",
    BytesRaw("unknown", SIZE=2, DEFAULT=b'\x02\x80'),
    UInt8("length"),
    UInt8("sentinel", DEFAULT=111),
    UInt16Array('data', SIZE=get_vnorm16_size),
    ALIGN=4,
    )

#polyinstance = Container("polyinstance",
#    BytesRaw("unknown", SIZE=3, DEFAULT=b'\x00\x80\x01'),
#    UInt8("sentinel", DEFAULT=108),
#    UInt32('vert count'),
#    ALIGN=4,
#    )

polyinstance = Struct("polyinstance",
    BytesRaw("unknown", SIZE=12,
        DEFAULT=(b'\x00\x80\x01\x6C'+
            b'\x00\x00\x00\x00'+
            b'\x00\x00\x00\x2D')
            ),
    UInt8("sentinel", OFFSET=3, DEFAULT=108),
    UInt32('vert count', OFFSET=4),
    Pad(4),
    Float("vert_scale"),
    Float("uv_scale"),
    ALIGN=4,
    )

primitive_switch = Switch('primitive',
    DEFAULT=unknown_primitive,
    CASE=get_primitive_type,
    CASES={ 0:terminator,
            20:multi_polyinst,
            23:polyinst_link,
            #45:float_2d,
            100:uv_32bit,
            101:uv_16bit,
            102:uv_8bit,
            104:vert_32bit,
            105:vert_16bit,
            106:vert_8bit,
            108:polyinstance,
            111:vnorm_16bit,
            },
    ALIGN=4,
    )

primitives = WhileArray('primitives',
    CASE=has_next_primitive,
    SUB_STRUCT=primitive_switch,
    ALIGN=4,
    )

#The gdl model parser seems like it may be 8-byte aligned.
#The only GOOD reason I can think of for them to do this
#is so it can always expect a sub_object_model struct to
#be aligned to the current position of the parser.

sub_object_model = Container("sub-object model",
    LUInt16("vert count"),
    UInt8("unknown0"),
    UEnum8("type", *primitive_types),
    UInt32('unknown1'),
    ALIGN=8,
    CHILD=primitives,
    )

#sub-objects are for things where you may have multiple textures on one mesh.
#in that case each subobject would have one texture.
sub_object_block = Struct("sub-object",
    LUInt16("qwc"),
    LUInt16("tex index"),
    LUInt16("lm index"),#seems to always be 0
    LSInt16("lod k")
    )

object_block = Struct("object",
    LFloat("inv rad"),
    LFloat("bnd rad"),
    Bool32("flags",
        ("non_lit",   0x0),
        ("fmt_basic", 0x0),

        ("alpha",     0x01),
        ("v_normals", 0x02),
        ("v_colors",  0x04),
        ("mesh",      0x08),
        ("tex2",      0x10),
        ("lmap",      0x20),

        ("sharp",  0x040),
        ("blur",   0x080),
        ("chrome", 0x100),

        ("error",  0x200),
        ("sort_a", 0x400),
        ("sort",   0x800),

        ("fmt_mask", 0x00F000),
        ("pre_lit",  0x010000),
        ("lit_mask", 0x0F0000),
        ("lmap_lit", 0x020000),
        ("norm_lit", 0x030000),
        ("dyn_lit",  0x100000)
        ),

    LSInt32('sub-objects count'),
    Struct("sub-object 0", INCLUDE=sub_object_block),

    LPointer32('sub-objects pointer'),
    LPointer32('sub-object models pointer'),

    #the number of unique verts in the object.
    #probably number of verts before compiling
    LSInt32("vert count"),
    LSInt32("tri count"),
    LSInt32("id num"),

    #pointer to the obj def that this model uses
    LPointer32("obj def"),
    Pad(16),

    SIZE=64,
    
    CHILD=Container("data",
        Array("sub-objects",
              SIZE=sub_objects_size, SUB_STRUCT=sub_object_block,
              POINTER="..sub_objects_pointer"),
        Array("sub-object models",
              SIZE="..sub_objects_count", SUB_STRUCT=sub_object_model,
              POINTER="..sub_object_models_pointer"),
        )
    )


bitmap_block = Struct("bitmap",
    #palletized textures are in either 16 or 256 color format
    #   if a texture has a 16 color palette then each byte counts as
    #   2 pixels with the least significant 4 bits being the left pixel
    #portraits used as background on player bar are in ABGR_8888_IDX_4

    #color data is stored in RGBA order
    #8x8 seems to be the smallest a texture is allowed to be

    UEnum8("format",
        ("ABGR_1555", 0),
        ("XBGR_1555", 1),
        ("ABGR_8888", 2),
        ("XBGR_8888", 3),
        #all these below formats are palettized
        ("ABGR_1555_IDX_4", 16),
        ("XBGR_1555_IDX_4", 17),
        ("ABGR_8888_IDX_4", 34),
        ("XBGR_8888_IDX_4", 35),
        ("ABGR_1555_IDX_8", 48),
        ("XBGR_1555_IDX_8", 49),
        #("IDXA_88",         56), #i have no idea how this format works
        ("ABGR_8888_IDX_8", 66),
        ("XBGR_8888_IDX_8", 67),
        ("A_8_IDX_8", 130),
        ("I_8_IDX_8", 131),
        ("A_4_IDX_4", 146),
        ("I_4_IDX_4", 147)
        ),
    SInt8("lod k"),
    #mipmap_count does not include the largest size.
    #this means a texture without mipmaps will have a mipmap_count of 0
    UInt8("mipmap count"),

    #Width-64 == int(ceil(width/64))
    UInt8("width-64"),
    LUInt16("log2 of width"),
    LUInt16("log2 of height"),

    LBool16("flags",
        ("halfres",   0x001),
        ("see alpha", 0x002),
        ("clamp u",   0x004),
        ("clamp v",   0x008),
        ("animation", 0x010),
        ("external",  0x020),
        ("tex shift", 0x040),
        ("has alpha", 0x080),
        ("invalid",   0x100),
        ("dual tex",  0x200)
        ),

    LUInt16("tex palette index"),

    #pointer to the texture in the BITMAPS.ps2
    #where the pixel texture data is located
    LPointer32("tex pointer"),

    LUInt16("tex palette count"),
    LUInt16("tex shift index"),

    #the number of bitmaps after the current
    #one that are included in the animation
    #animated textures can have different formats for each frame
    LUInt16("frame count"),

    LUInt16("width"),
    LUInt16("height"),

    #related to resolution as a texture with half the
    #size of another texture has this int halved as well
    LUInt16("size"),

    #points to the bitmap def that this bitmap uses
    #this seems to be the same pointer for each texture in
    #an animation, except for ones of a different format
    LPointer32("bitmap def"),

    LUInt32Array("tex 0", SIZE=8),
    LUInt32Array("mip tbp 1", SIZE=8),
    LUInt32Array("mip tbp 2", SIZE=8),

    LUInt16Array("vram address", SIZE=4),
    LUInt16Array("clut address", SIZE=4),

    SIZE=64
    #To animate a series of bitmaps, take the first bitmap and lets call it "base".
    #    In the chain and make a sequence block aiming to base. Create another bitmap
    #    block to act as the main object (so multiple, different, animations can exist).
    #    In the anim.ps2 create a texture animation aiming to the main sequence
    #    and aim the start of the animation to the base sequence.
    )

objects_header = Struct('header',
    StrRawLatin1("dir name",   SIZE=32),
    StrRawLatin1("model name", SIZE=32),
    LUInt32("version", DEFAULT=0x0D000BF0),

    LUInt32("objects count"),
    LUInt32("bitmaps count"),
    LUInt32("object defs count"),
    LUInt32("bitmap defs count"),

    LPointer32("objects pointer"),
    LPointer32("bitmaps pointer"),
    LPointer32("object defs pointer"),
    LPointer32("bitmap defs pointer"),

    LPointer32("sub-objects pointer"),
    LPointer32("geometry pointer"),

    LUInt32("obj end"),

    LUInt32("tex start"),
    LUInt32("tex end"),

    LUInt32("tex bits"),

    LUInt16("lm tex First"),
    LUInt16("lm tex num"),
    LUInt32("tex info"),
    Pad(28),
    SIZE=160
    )


object_def = Struct("object def",
    StrRawLatin1("name", SIZE=16),
    LFloat("bnd rad", GUI_NAME="bounding radius"),
    LSInt16("obj index"),
    LSInt16("n frames"),
    SIZE=24
    )
   
bitmap_def = Struct("bitmap def",
    StrRawLatin1("name", SIZE=16),
    Pad(14),
    LUInt16("tex index"),
    LUInt16("width"),
    LUInt16("height"),
    SIZE=36
    )

objects_ps2_def = TagDef(
    objects_header,
    
    Array("objects",
        SIZE='.header.objects_count',
        POINTER='.header.objects_pointer',
        SUB_STRUCT=object_block,
        ),
    Array("bitmaps",
        SIZE='.header.bitmaps_count',
        POINTER='.header.bitmaps_pointer',
        SUB_STRUCT=bitmap_block
        ),
    Array("object defs",
        SIZE='.header.object_defs_count',
        POINTER='.header.object_defs_pointer',
        SUB_STRUCT=object_def
        ),
    Array("bitmap defs",
        SIZE='.header.bitmap_defs_count',
        POINTER='.header.bitmap_defs_pointer',
        SUB_STRUCT=bitmap_def
        ),
    
    NAME="gdl objects resource",
    ext=".ps2", def_id="objects", tag_cls=ObjectsPs2Tag
    )
