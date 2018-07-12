from array import array
from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef
from .objs.bitm import BitmTag

type_comment = """Type controls bitmap 'geometry'.
All dimensions must be a power-of-two except for SPRITES and INTERFACE:

*2D TEXTURES: Ordinary, 2D textures will be generated.

*3D TEXTURES: Volume textures will be generated from each
    sequence of 2D texture 'slices'.

*CUBE MAPS: Cube maps will be generated from each consecutive
    set of six 2D textures in each sequence. All faces
    of a cubemap must be square and have the same dimensions.

*SPRITES: Sprite texture pages will be generated.

*INTERFACE BITMAPS: Similar to 2D TEXTURES, but without mipmaps or
    the power-of-two restriction on their dimensions."""

format_comment = """Format controls how pixels will be stored internally.

*COMPRESSED WITH COLOR-KEY TRANSPARENCY: DXT1 compression(4-bits per pixel).
    For each 4x4 blocks of pixels, two colors are chosen that best represent
    the range of the colors in that block(c0 and c1). The colors are reduced
    to 16-bit and each of the 16 pixels is given a blending code(0 to 3).
    0 means the pixels color is c0 and 1 means its color is c1, with
    2 meaning to use 1/3(c1) + 2/3(c2), and 3 meaning 2/3(c1) + 1/3(c2).

    If an alpha exists, it is reduced to 1-bit(black or white).
    If a 4x4 block contains transparency, the blending codes are changed so
    that 2 means to use 1/2(c1) + 1/2(c2) and 3 means solid black(a=r=g=b=0).

*COMPRESSED WITH EXPLICIT ALPHA: DXT3 compression(8-bits per pixel).
    Same method as DXT1, but without the color-key transparency stuff.
    Alpha channel is quantized down to 4 bits per pixel(16 shades of gray).
    This format is best used where smooth gradients are not required in the
    alpha channel, and consistancy in shades between 4x4 chunks is important.

*COMPRESSED WITH INTERPOLATED ALPHA: DXT5 compression(8-bits per pixel).
    Same method as DXT1, but without the color-key transparency stuff.
    Alpha channel uses a method similar to DXT1. For each 4x4 block of
    pixels, two 8-bit shades of gray are chosen that best represent the
    range of values in that block(v0, v1). Each of the 16 pixels is given a
    blending code(0 to 7), with 0 meaning to use v0 and 1 meaning to use v1.
    The rest of the codes blend the v0 and v1 shades as shown:
        2 = (v0*6 + v1)/7      3 = (v0*5 + v1*2)/7
        4 = (v0*4 + v1*3)/7    5 = (v0*3 + v1*4)/7
        6 = (v0*2 + v1*5)/7    7 = (v0   + v1*6)/7
    If 100% white and 100% black are in the 4x4 block, these are used instead.
        2 = (v0*4 + v1)/5      3 = (v0*3 + v1*2)/5
        4 = (v0*2 + v1*3)/5    5 = (v0   + v1*4)/5
        6 = black              7 = white
    This allows very smooth gradients in the alpha, but if two neighboring
    4x4 blocks do not use the same v0 and v1 shades, it can be very noticible.

*16-BIT COLOR: Uses 16 bits per pixel. Depending on the alpha channel
    bitmaps are quantized to one of 3 different formats:
    r5g6b5(no alpha), a1r5g5b5(1-bit alpha), or a4r4g4b4(>1-bit alpha)

*32-BIT COLOR: Uses 32 bits per pixel. Very high quality and can have an alpha
    channel at no added cost. This format takes up the most memory, however.
    Bitmap formats are x8r8g8b8 and a8r8g8b8.

*MONOCHROME: Uses either 8 or 16 bits per pixel. This is an Xbox-only format.
    There are 4 different formats, each using an intensity and alpha channel.
    An intensity channel is essentially a monochrome rgb channel:
        a8: 8-bits per pixel. Intensity channel is solid black, with the
            pixel data being used for the alpha channel.
        y8: 8-bits per pixel. Alpha channel is solid white, with the pixel
            data being used for the intensity channel.
        ay8: 8-bits per pixel. Pixel data is used for both intensity and alpha.
        a8y8: 16-bits per pixel. Intensity and alpha channels each use their
            own separate pixel data, with 8 bits for each channel.

NOTE: Normal maps(a.k.a. bump maps) usually use 32-bit color.
    This is costly, and if there is no alpha you can usually use 16-bit
    r5g6b5 to save space without any noticible drop in quality ingame."""

usage_comment = """Usage controls how mipmaps are generated:

*ALPHA BLEND: Pixels with zero alpha are ignored in mipmaps, to prevent
    bleeding the transparent color.

*DEFAULT: Downsampling works normally, as in Photoshop.

*HEIGHT MAP: The bitmap is a height map, which will get converted to a bump map.
    Uses the 'bump height' below. Alpha is 1-bit. This is an Xbox-only format.

*DETAIL MAP: Mipmap color fades to gray and alpha fades to white.
    Color fading is controlled by the 'detail fade factor' below.

*LIGHT MAP: Generates no mipmaps. Do not use!

*VECTOR MAP: Used mostly for special effects; pixels are treated as XYZ vectors
    and are normalized after downsampling. Alpha is passed though unmodified."""

post_processing_comment = """
These properties control how mipmaps are processed."""

sprite_processing_comment = """
When creating a sprite group, specify the number and size of the textures
that the group is allowed to occupy. During importing, you will recieve
feedback about how well the alloted space was used."""

def get(): return bitm_def

def pixel_block_size(node, *a, **kwa):
    if isinstance(node, array):
        return node.itemsize*len(node)
    return len(node)

pixel_root = WhileArray('pixel root',
    SUB_STRUCT=WhileArray('bitmap pixels',
        SUB_STRUCT=UInt8Array('pixels', SIZE=pixel_block_size)
        )
    )

sprite = QStruct("sprite",
    UInt16("bitmap index"),
    Pad(6),
    Float("left side"),
    Float("right side"),
    Float("top side"),
    Float("bottom side"),
    Float("registration point x"),
    Float("registration point y"),
    SIZE=32,
    )

sequence = Struct("sequence",
    ascii_str32("sequence name"),
    UInt16("first bitmap index"),
    UInt16("bitmap count"),
    Pad(16),
    reflexive("sprites", sprite, 64),
    SIZE=64,
    )

bitmap = Struct("bitmap",
    UEnum32('bitm id', ('bitm', 'bitm'), DEFAULT='bitm', EDITABLE=False),
    UInt16("width", SIDETIP="pixels", EDITABLE=False),
    UInt16("height", SIDETIP="pixels", EDITABLE=False),
    UInt16("depth", SIDETIP="pixels", EDITABLE=False),
    SEnum16("type",
        "texture 2d",
        "texture 3d",
        "cubemap",
        "white",
        EDITABLE=False
        ),
    SEnum16("format",
        "a8",
        "y8",
        "ay8",
        "a8y8",
        #"-unused1-",
        #"-unused2-",
        ("r5g6b5", 6),
        #"-unused3-",
        ("a1r5g5b5", 8),
        ("a4r4g4b4", 9),
        ("x8r8g8b8", 10),
        ("a8r8g8b8", 11),
        #"-unused4-",
        #"-unused5-",
        ("dxt1", 14),
        ("dxt3", 15),
        ("dxt5", 16),
        ("p8-bump", 17),
        ),
    Bool16("flags",
        "power of 2 dim",
        "compressed",
        "palletized",
        "swizzled",
        "linear",
        "v16u16",
        "unknown",
        "prefer low detail",
        "data in resource map",
        ),
    UInt16("registration point x"),
    UInt16("registration point y"),
    UInt16("mipmaps"),
    FlUInt16("pixels", VISIBLE=False, EDITABLE=False),

    # this is the non-magic pointer into the map that the pixel data
    # is located at. if flags.data_in_resource_map is True and the
    # map is halo ce/pc/trial, the offset is into the bitmaps.map
    UInt32("pixels offset", VISIBLE=False, EDITABLE=False),
    UInt32("pixels meta size", VISIBLE=False, EDITABLE=False),
    UInt32("bitmap id unknown1", VISIBLE=False, EDITABLE=False),
    UInt32("bitmap data pointer", VISIBLE=False, EDITABLE=False),
    UInt32("bitmap id unknown2", VISIBLE=False, EDITABLE=False),
    UInt32("base address", VISIBLE=False, EDITABLE=False),
    SIZE=48,
    )

bitm_body = Struct("tagdata",
    SEnum16("type",
        "textures 2d",
        "textures 3d",
        "cubemaps",
        "sprites",
        "interface bitmaps",
        COMMENT=type_comment
        ),
    SEnum16("format",
        "color key transparency",
        "explicit alpha",
        "interpolated alpha",
        "color 16bit",
        "color 32bit",
        "monochrome",
        COMMENT=format_comment
        ),
    SEnum16("usage",
        "alpha-blend",
        "default",
        "height map",
        "detail map",
        "light map",
        "vector map",
        COMMENT=usage_comment, DEFAULT=1
        ),
    Bool16("flags",
        "enable diffusion dithering",
        "disable height map compression",
        "uniform sprite sequences",
        "sprite bug fix",
        ),
    QStruct("post processing",
        float_zero_to_one("detail fade factor"),
        float_zero_to_one("sharpen amount"),
        Float("bump height", SIDETIP="repeats"),
        COMMENT=post_processing_comment
        ),
    Struct("sprite processing",
        SEnum16("sprite budget size",
          {NAME: "x32",  VALUE: 0, GUI_NAME: "32x32"},
          {NAME: "x64",  VALUE: 1, GUI_NAME: "64x64"},
          {NAME: "x128", VALUE: 2, GUI_NAME: "128x128"},
          {NAME: "x256", VALUE: 3, GUI_NAME: "256x256"},
          {NAME: "x512", VALUE: 4, GUI_NAME: "512x512"},
          ),
        UInt16("sprite budget count"),
        COMMENT=sprite_processing_comment
        ),
    UInt16("color plate width",  SIDETIP="pixels", EDITABLE=False),
    UInt16("color plate height", SIDETIP="pixels", EDITABLE=False),

    rawdata_ref("compressed color plate data", max_size=16777216),
    rawdata_ref("processed pixel data", max_size=16777216),

    Float("blur filter size", MIN=0.0, MAX=10.0, SIDETIP="[0,10] pixels"),
    float_neg_one_to_one("alpha bias"),
    UInt16("mipmap levels", MIN=0, SIDETIP="levels"),
    SEnum16("sprite usage",
       "blend/add/subtract/max",
       "multiply/min",
       "double multiply",
       ),
    UInt16("sprite spacing", SIDETIP="pixels"),
    Pad(2),
    reflexive("sequences", sequence, 256, DYN_NAME_PATH='.sequence_name'),
    reflexive("bitmaps", bitmap),
    SIZE=108, WIDGET=HaloBitmapTagFrame
    )

def get():
    return bitm_def

bitm_def = TagDef("bitm",
    blam_header('bitm', 7),
    bitm_body,

    ext=".bitmap", endian=">", tag_cls=BitmTag,
    subdefs = {'pixel_root':pixel_root}
    )
