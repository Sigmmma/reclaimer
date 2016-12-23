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
    ascii_str32("sequence name"),
    BUInt16("first bitmap index"),
    BUInt16("bitmap count"),
    Pad(16),
    reflexive("sprites", sprite, 64),
    SIZE=64,
    )

bitmap = Struct("bitmap",
    BUEnum32('bitm id', ('bitm', 'bitm'), EDITABLE=False),
    BUInt16("width", SIDETIP="pixels"),
    BUInt16("height", SIDETIP="pixels"),
    BUInt16("depth", SIDETIP="pixels"),
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
    BBool16("flags",
        "power of 2 dim",
        "compressed",
        "palletized",
        "swizzled",
        "linear",
        "v16u16",
        ("made by arsenic", 1<<7)
        ),
    BUInt16("registration point x"),
    BUInt16("registration point y"),
    BUInt16("mipmaps"),
    BUInt16("pixels", VISIBLE=False, EDITABLE=False),
    BUInt32("pixels offset", VISIBLE=False, EDITABLE=False),
    BUInt32("bitmap id unknown1", VISIBLE=False, EDITABLE=False),
    BUInt32("bitmap id unknown2", VISIBLE=False, EDITABLE=False),
    BSInt32("bitmap data pointer", VISIBLE=False, EDITABLE=False),
    BUInt32("bitmap id unknown3", VISIBLE=False, EDITABLE=False),
    BUInt32("base address", VISIBLE=False, EDITABLE=False),
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
    float_zero_to_one("detail fade factor"),
    float_zero_to_one("sharpen amount"),
    BFloat("bump height", SIDETIP="repeats"),  # repeats
    BSEnum16("sprite budget size",
      {NAME: "x32",  VALUE: 0, GUI_NAME: "32x32"},
      {NAME: "x64",  VALUE: 1, GUI_NAME: "64x64"},
      {NAME: "x128", VALUE: 2, GUI_NAME: "128x128"},
      {NAME: "x256", VALUE: 3, GUI_NAME: "256x256"},
      {NAME: "x512", VALUE: 4, GUI_NAME: "512x512"},
      ),
    BUInt16("sprite budget count"),
    BUInt16("color plate width", SIDETIP="pixels"),
    BUInt16("color plate height", SIDETIP="pixels"),

    rawdata_ref("compressed color plate data", max_size=16777216),
    rawdata_ref("processed pixel data", max_size=16777216),

    BFloat("blur filter size", MIN=0.0, MAX=10.0, SIDETIP="[0,10] pixels"),
    float_neg_one_to_one("alpha bias"),
    BUInt16("mipmap levels", MIN=0, SIDETIP="levels"),
    BSEnum16("sprite usage",
       "blend/add/subtract/max",
       "multiply/min",
       "double multiply",
       ),
    BUInt16("sprite spacing", SIDETIP="pixels"),
    Pad(2),
    reflexive("sequences", sequence, 256, DYN_NAME_PATH='.sequence_name'),
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
