from array import array
from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef
from .objs.bitm import BitmTag

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
    BUInt16("bitmap index"),
    Pad(6),
    BFloat("left side"),
    BFloat("right side"),
    BFloat("top side"),
    BFloat("bottom side"),
    BFloat("registration point x"),
    BFloat("registration point y"),
    SIZE=32,
    )

sequence = Struct("sequence",
    StrLatin1("sequence name", SIZE=32),
    BUInt16("first bitmap index"),
    BUInt16("bitmap count"),
    Pad(16),
    reflexive("sprites", sprite, 64),
    SIZE=64,
    )

bitmap = Struct("bitmap",
    BUInt32("bitm id", EDITABLE=False, DEFAULT="bitm"),
    BUInt16("width"),
    BUInt16("height"),
    BUInt16("depth"),
    BSEnum16("type",
        "texture 2d",
        "texture 3d",
        "cubemap",
        "white",
        ),
    BSEnum16("format",
        "a8",
        "y8",
        "ay8",
        "a8y8",
        "-unused1-",
        "-unused2-",
        "r5g6b5",
        "-unused3-",
        "a1r5g5b5",
        "a4r4g4b4",
        "x8r8g8b8",
        "a8r8g8b8",
        "-unused4-",
        "-unused5-",
        "dxt1",
        "dxt3",
        "dxt5",
        "p8-bump",
        ),
    BBool16("flags",
        "power of 2 dim",
        "compressed",
        "palletized",
        "swizzled",
        "linear",
        "v16u16",
        ("made by arsenic", 128)
        ),
    BUInt16("registration point x"),
    BUInt16("registration point y"),
    BUInt16("mipmaps"),
    BUInt16("pixels"),
    BUInt32("pixels offset"),
    BUInt32("bitmap id unknown1"),
    BUInt32("bitmap id unknown2"),
    BSInt32("bitmap data pointer"),
    BUInt32("bitmap id unknown3"),
    BUInt32("base address"),
    SIZE=48,
    )

bitm_body = Struct("tagdata",
    BSEnum16("type",
        "textures 2d",
        "textures 3d",
        "cubemaps",
        "sprites",
        "interface bitmaps",
        ),
    BSEnum16("format",
        "color key transparency",
        "explicit alpha",
        "interpolated alpha",
        "color 16bit",
        "color 32bit",
        "monochrome",
        ),
    BSEnum16("usage",
        "alpha-blend",
        "default",
        "height map",
        "detail map",
        "light map",
        "vector map",
        ),
    BBool16("flags",
        "enable diffusion dithering",
        "disable height map compression",
        "uniform sprite sequences",
        "sprite bug fix",
        "processed by reclaimer",
        ),
    BFloat("detail fade factor", MIN=0.0 , MAX=1.0),
    BFloat("sharpen amount", MIN=0.0 , MAX=1.0),
    BFloat("bump height"),  # repeats
    BSEnum16("sprite budget size",
      {NAME: "x32",  VALUE: 0, GUI_NAME: "32x32"},
      {NAME: "x64",  VALUE: 1, GUI_NAME: "64x64"},
      {NAME: "x128", VALUE: 2, GUI_NAME: "128x128"},
      {NAME: "x256", VALUE: 3, GUI_NAME: "256x256"},
      {NAME: "x512", VALUE: 4, GUI_NAME: "512x512"},
      ),
    BUInt16("sprite budget count"),
    BUInt16("color plate width"),
    BUInt16("color plate height"),
    rawdata_ref("compressed color plate data"),
    rawdata_ref("processed pixel data"),
    BFloat("blur filter size", MIN=0.0, MAX=10.0),
    BFloat("alpha bias", MIN=-1.0 , MAX=1.0),
    BUInt16("mipmap levels", MIN=0),
    BSEnum16("sprite usage",
       "blend/add/subtract/max",
       "multiply/min",
       "double multiply",
       ),
    BUInt16("sprite spacing"),
    Pad(2),
    reflexive("sequences", sequence, 256),
    reflexive("bitmaps", bitmap),
    SIZE=108,
    )

def get():
    return bitm_def

bitm_def = TagDef("bitm",
    blam_header('bitm', 7),
    bitm_body,

    ext=".bitmap", endian=">", tag_cls=BitmTag,
    subdefs = {'pixel_root':pixel_root}
    )
