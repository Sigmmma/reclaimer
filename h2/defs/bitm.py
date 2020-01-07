#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from array import array
from reclaimer.h2.common_descs import *
from supyr_struct.defs.tag_def import TagDef

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
    SIZE=32
    )

sequence = Struct("sequence",
    ascii_str32("sequence name"),
    UInt16("first bitmap index"),
    UInt16("bitmap count"),
    Pad(16),
    h2_reflexive("sprites", sprite, 64),
    SIZE=60
    )

bitmap = Struct("bitmap",
    UEnum32('bitm id', ('bitm', 'bitm'), DEFAULT='bitm', EDITABLE=False),
    UInt16("width", SIDETIP="pixels", EDITABLE=False),
    UInt16("height", SIDETIP="pixels", EDITABLE=False),
    UInt8("depth", SIDETIP="pixels", EDITABLE=False),
    Bool8("more flags",
        "delete from cache file",
        "bitmap create attempted",
        "unknown"
        ),
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
        ("p8 bump", 17),
        ("p8", 18),
        ("argbfp32", 19),
        ("rgbfp32", 20),
        ("rgbfp16", 21),
        ("v8u8", 22),
        ("g8b8", 23),
        ),
    Bool16("flags",
        "power of 2 dim",
        "compressed",
        "palletized",
        "swizzled",
        "linear",
        "v16u16",
        "mipmap debug level",
        "prefer low detail",
        ),
    UInt16("registration point x"),
    UInt16("registration point y"),
    UInt16("mipmaps"),
    UInt16("low detail mipmaps"),

    UInt32("pixels offset", EDITABLE=False),
    UInt32("lod1 offset", EDITABLE=False),
    UInt32("lod2 offset", EDITABLE=False),
    UInt32("lod3 offset", EDITABLE=False),
    UInt32("lod4 offset", EDITABLE=False),
    UInt32("lod5 offset", EDITABLE=False),
    UInt32("lod6 offset", EDITABLE=False),
    UInt32("lod1 size", EDITABLE=False),
    UInt32("lod2 size", EDITABLE=False),
    UInt32("lod3 size", EDITABLE=False),
    UInt32("lod4 size", EDITABLE=False),
    UInt32("lod5 size", EDITABLE=False),
    UInt32("lod6 size", EDITABLE=False),
    UInt32("datum",  # points back to this tag
        VISIBLE=False, EDITABLE=False
        ),
    SIZE=116
    )

bitm_body = Struct("tagdata",
    SEnum16("type",
        "textures 2d",
        "textures 3d",
        "cubemaps",
        "sprites",
        "interface bitmaps",
        ),
    SEnum16("format",
        "color key transparency",
        "explicit alpha",
        "interpolated alpha",
        "color 16bit",
        "color 32bit",
        "monochrome",
        ),
    SEnum16("usage",
        "alpha-blend",
        "default",
        "height map",
        "detail map",
        "light map",
        "vector map",
        "height map blue 255",
        "embm",
        "height map a8l8",
        "height map g8b8",
        "height map g8b8 with alpha",
        DEFAULT=1
        ),
    Bool16("flags",
        "enable diffusion dithering",
        "disable height map compression",
        "uniform sprite sequences",
        "sprite bug fix",
        "use sharp bump filter",
        "unused",
        "use clamped bump filter",
        "invert detail fade",
        "swap x y vector components",
        "convert from signed",
        "convert to signed",
        "import mipmap chains",
        "intentionally true color"
        ),
    QStruct("post processing",
        float_zero_to_one("detail fade factor"),
        float_zero_to_one("sharpen amount"),
        Float("bump height", SIDETIP="repeats"),
        ),
    Struct("sprite processing",
        SEnum16("sprite budget size",
          {NAME: "x32",  VALUE: 0, GUI_NAME: "32x32"},
          {NAME: "x64",  VALUE: 1, GUI_NAME: "64x64"},
          {NAME: "x128", VALUE: 2, GUI_NAME: "128x128"},
          {NAME: "x256", VALUE: 3, GUI_NAME: "256x256"},
          {NAME: "x512", VALUE: 4, GUI_NAME: "512x512"},
          {NAME: "x1024", VALUE: 5, GUI_NAME: "1024x1024"},
          ),
        UInt16("sprite budget count"),
        ),
    UInt16("color plate width",  SIDETIP="pixels", EDITABLE=False),
    UInt16("color plate height", SIDETIP="pixels", EDITABLE=False),

    h2_rawdata_ref("compressed color plate data", max_size=16777216),
    h2_rawdata_ref("processed pixel data", max_size=16777216),

    Float("blur filter size", MIN=0.0, MAX=10.0, SIDETIP="[0,10] pixels"),
    float_neg_one_to_one("alpha bias"),
    UInt16("mipmap levels", MIN=0, SIDETIP="levels"),
    SEnum16("sprite usage",
       "blend/add/subtract/max",
       "multiply/min",
       "double multiply",
       ),
    UInt16("sprite spacing", SIDETIP="pixels"),
    SEnum16("force format",
       "default",
       "g8b8",
       "dxt1",
       "dxt3",
       "dxt5",
       "a8l8",
       "a4r4g4b4",
       ),
    h2_reflexive("sequences", sequence, 256, DYN_NAME_PATH='.sequence_name'),
    h2_reflexive("bitmaps", bitmap, 65536),
    Struct("more sprite processing",
        SInt8("color compression quality", SIDETIP="[1, 127]"),
        SInt8("alpha compression quality", SIDETIP="[1, 127]"),
        SInt8("overlap"),
        UEnum8("color subsampling",
            {GUI_NAME:"4:0:0", NAME:"x0x0"},
            {GUI_NAME:"4:2:0", NAME:"x2x0"},
            {GUI_NAME:"4:2:2", NAME:"x2x2"},
            {GUI_NAME:"4:4:4", NAME:"x4x4"},
            )
        ),
    ENDIAN="<", SIZE=76, WIDGET=Halo2BitmapTagFrame,
    )


def get():
    return bitm_def

bitm_def = TagDef("bitm",
    h2_blam_header('bitm'),
    bitm_body,

    ext=".%s" % h2_tag_class_fcc_to_ext["bitm"], endian="<",
    subdefs={'pixel_root':pixel_root}
    )
