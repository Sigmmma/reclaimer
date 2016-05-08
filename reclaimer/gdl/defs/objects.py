from supyr_struct.defs.tag_def import TagDef
from supyr_struct.defs.common_descriptors import *
from ..fields import *
from .objs.objects import ObjectsPs2Tag

def get(): return objects_ps2_def

def get_qword_size(block=None, parent=None, attr_index=None,
                   rawdata=None, new_value=None, *args, **kwargs):
    if block and parent is None:
        parent = block.PARENT
    if new_value is not None:
        parent.qword_count = (new_value-8)//16
    return parent.qword_count*16+8

#########################################################
'''FOR TEXTURES.PS2, RED AND BLUE CHANNELS ARE SWAPPED'''
#########################################################

'''The last vertex is always set to X=0, Y=0, Z=0.
This must be to signal that the strip has ended.'''

#normals are compressed as 1555 with the most significant bit
#reserved to mean whether or not the face should be created.


sub_object_model = Container("sub-object model",
    LUInt16("qword count"),
    BytesRaw("unknown", SIZE=6, DEFAULT=b'\x00\x60\x00\x00\x00\x00'),

    BytesRaw('data', SIZE=get_qword_size),

    ALIGN=4,
    )

#Multiple sub-objects are for things where you may have multiple
#textures on one mesh. In that case each subobject would have one texture.
sub_object_block = Struct("sub-object",
    LUInt16("qw count", "quadword count"),
    LUInt16("tex index"),
    LUInt16("lm index", GUI_NAME="light map index"),
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
        {NAME:"sort_a", VALUE:0x400, DEFAULT:True},
        ("sort",   0x800),

        ("fmt_mask", 0x00F000),
        {NAME:"pre_lit",  VALUE:0x010000, DEFAULT:True},
        {NAME:"lit_mask", VALUE:0x0F0000, DEFAULT:True},
        {NAME:"lmap_lit", VALUE:0x020000, DEFAULT:True},
        {NAME:"norm_lit", VALUE:0x030000, DEFAULT:True},
        ("dyn_lit",  0x100000)
        ),

    LSInt32('sub-objects count'),
    Struct("sub-object 0", INCLUDE=sub_object_block),

    LPointer32('sub-objects pointer'),
    LPointer32('sub-object models pointer'),

    #the number of unique verts in the object.
    #probably number of verts before compiling
    LSInt32("vert count"),#exactly the number of unique verts
    LSInt32("tri count"),#exactly the number of unique triangles
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

    LUInt16("lm tex first"),
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

######################################################################
'''All these structure defintions are only being kept for illustrating
the hierarchy of the quad-word chunks and what is stored in them.'''
######################################################################
'''
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

def get_stream_type(block=None, parent=None, attr_index=None,
                    rawdata=None, new_value=None, *args, **kwargs):
    if rawdata is not None:
        pad = (STREAM_ALIGN-(rawdata.tell()%STREAM_ALIGN))%STREAM_ALIGN
        if rawdata.peek(4)[3] not in known_streams:
            print('UNKNOWN DATA STREAM')
            try:
                if parent is None:
                    parent = block.PARENT
                print(rawdata.peek(4)[3], rawdata.tell(),
                      parent.get_tag().filepath)
            except:
                print(rawdata.peek(4)[3], rawdata.tell())
            print()
        return rawdata.peek(4+pad)[-1]

def has_next_stream(block=None, parent=None, attr_index=None,
                    rawdata=None, new_value=None, *args, **kwargs):
    if rawdata is not None:
        pad = (STREAM_ALIGN-(rawdata.tell()%STREAM_ALIGN))%STREAM_ALIGN
        return rawdata.peek(4+pad)[-1] not in (0, 96)

def is_pad_stream(block=None, parent=None, attr_index=None,
                  rawdata=None, new_value=None, *args, **kwargs):
    if rawdata is not None:
        pad = (STREAM_ALIGN-(rawdata.tell()%STREAM_ALIGN))%STREAM_ALIGN
        return rawdata.peek(4+pad)[-1] == 0

get_vnorm16_size = get_uv8_size

unknown_stream = Container("unknown stream",
    BytesRaw("unknown", SIZE=3, DEFAULT=b'\x00\x00\x00'),
    UInt8("sentinel"),
    ALIGN=4,
    )

pad_stream = Container("pad stream",
    UInt32("sentinel"),
    ALIGN=4,
    )

link_start = Struct("link start",
    Pad(3),
    UInt8("sentinel", DEFAULT=20),
    ALIGN=4,
    )

strip_link = Struct("strip link",
    Pad(3),
    UInt8("sentinel", DEFAULT=23),
    ALIGN=4,
    )

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

stream_switch = Switch('data stream',
    DEFAULT=unknown_stream,
    CASE=get_stream_type,
    CASES={ 20:link_start,
            23:strip_link,
            100:uv_32bit,
            101:uv_16bit,
            102:uv_8bit,
            104:vert_32bit,
            105:vert_16bit,
            106:vert_8bit,
            #108:tri_strip
            109:vert_color_abgr,
            111:vnorm_16bit,
            },
    ALIGN=4,
    )

tri_strip = Container("tri strip",
    BytesRaw("unknown", SIZE=3, DEFAULT=b'\x00\x80\x01'),
    UInt8("sentinel", DEFAULT=108),
    UInt32('vert count'),
    BytesRaw("unknown", SIZE=4, DEFAULT=b'\x00\x00\x00\x2D'),
    Float("face_dir"),# 1.0 == faces are clockwise
    #                  -1.0 == faces are counter-clockwise
    #                  No solid idea why they decided to use a float for this.
    #                  Maybe they use it for scaling vertex normals.
    Float("uv_scale"),
                   
    #verts, norms, uvs
    Switch('verts',   INCLUDE=stream_switch),
    Switch('norms',   INCLUDE=stream_switch),
    Switch('uvs',     INCLUDE=stream_switch),

    ALIGN=4,
    SIZE=20,
    )

tri_strip_switch = Switch('tri strip',
    DEFAULT=unknown_stream,
    CASE=get_stream_type,
    CASES={ 20:link_start,
            23:strip_link,
            108:tri_strip },
    ALIGN=4,
    )

sub_object_model = Container("sub-object model",
    LUInt16("qword count"),
    BytesRaw("unknown", SIZE=6, DEFAULT=b'\x00\x60\x00\x00\x00\x00'),

    ModelStream('data steams',
        CASE=has_next_stream,
        SUB_STRUCT=tri_strip_switch,
        ALIGN=4),

    WhileArray('pad steams',
        CASE=is_pad_stream,
        SUB_STRUCT=pad_stream,
        ALIGN=4),

    ALIGN=4,
    )

'''
