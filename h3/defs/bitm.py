#Written by gbMichelle with help from the adjutant and assembly plugin files
from ..common_descs import *
from .objs.tag import *
from reclaimer.hek.defs.bitm import sequence
from supyr_struct.defs.tag_def import TagDef


sequence_related = Struct("sequence thing",
    ascii_str32("sequence name"),
    UInt16("idx"),
    SIZE=40,
    )


bitmap = Struct("bitmap",
    UEnum32('bitm id', ('bitm', 'bitm'), DEFAULT='bitm', EDITABLE=False),
    UInt16("width", SIDETIP="pixels", EDITABLE=False),
    UInt16("height", SIDETIP="pixels", EDITABLE=False),
    UInt8("depth", SIDETIP="pixels", EDITABLE=False),
    Bool8("format flags",
        "delete from cache file",
        "bitmap create attempted",
        "unknown",
        "tiled",
        ),
    SEnum16("type",
        "texture 2d",
        "texture 3d",
        "cubemap",
        "multipage 2d",
        EDITABLE=False
        ),
    SEnum16("format",
        "a8",
        "y8",
        "ay8",
        "a8y8",
        "unused4",
        "unused5",
        ("r5g6b5", 6),
        "unused7",
        ("a1r5g5b5", 8),
        ("a4r4g4b4", 9),
        ("x8r8g8b8", 10),
        ("a8r8g8b8", 11),
        "unused12",
        "unused13",
        ("dxt1", 14),
        ("dxt3", 15),
        ("dxt5", 16),
        ("p8 bump", 17),
        ("p8", 18),
        ("argbfp32", 19),
        ("rgbfp32", 20),
        ("rgbfp16", 21),
        ("v8u8", 22),
        "unused23",
        "unused24",
        "unused25",  # ui\halox\main_menu.bkd.bitmap is set to this
        #              and is palettized with dimensions 231 x 1 x 1
        "unused26",
        "unused27",
        "unused28",
        "unused29",
        "unused30",
        "unused31",
        "unused32",
        ("dxn", 33),
        ("ctx1", 34),
        ("dxt3a", 35),
        ("dxt3y", 36),
        ("dxt5a", 37),
        ("dxt5y", 38),
        ("dxt5ay", 39),
        "unused40",
        "unused41",
        "unused42",
        "unused43",
        "unused44",
        ),
    Bool16("flags",
        "power of 2 dim",
        "compressed",
        "palletized",
        "swizzled",
        "linear",
        "v16u16",
        "mip map debug level",
        "prefer low detail",
        ("always on", 1<<9),
        ("interlaced", 1<<12),
        ),
    UInt16("registration point x"),
    UInt16("registration point y"),
    UInt8("mipmaps"),
    UInt8("unknown0"),
    SInt8("interleaved asset index"),
    SInt8("interleaved index"),

    SInt32("pixels offset"),     # only valid in tag form and more than 1 bitmap
    SInt32("pixels data size"),  # only valid in tag form and more than 1 bitmap
    SInt32("unknown1"),  # always 0?
    SInt32("mipmap data off"),  # size of main image if mipmaps > 0, else 0
    SInt32("unknown2"),  # always -1?
    SInt32("unknown3"),  # always 0?
    SIZE=48,
    )


bitm_body = Struct("tagdata",
    SInt16("unknown1"),
    SInt16("unknown2"),
    SInt16("unknown3"),
    SInt16("unknown4"),
    Float("blur filter size", MIN=0.0, MAX=10.0, SIDETIP="[0,10] pixels"),
    float_neg_one_to_one("alpha bias"),
    SInt16("unknown5"),
    Bool16("flags",
        "enable diffusion dithering",
        "disable height map compression",
        "uniform sprite sequences",
        "sprite bug fix",
        "use sharp bump filter",
        "unused", # Used for decal bumps
        "use clamped bump filter",
        "invert detail fade",
        "swap x y vector components",
        "convert from signed",
        "convert to signed",
        "import mipmap chains",
        "intentionally true color"
        ),
    reflexive("sequence related", sequence_related, 256, DYN_NAME_PATH='.sequence_name'), #0x14
    reflexive("unknown sequences", sequence, 256, DYN_NAME_PATH='.sequence_name'), #0x20
    rawdata_ref("compressed color plate data"),
    rawdata_ref("processed pixel data"),
    reflexive("sequences", sequence, 256, DYN_NAME_PATH='.sequence_name'),
    reflexive("bitmaps", bitmap, 2048),

    rawdata_ref("unknown6"),
    Pad(12),
    reflexive("zone assets normal", zone_asset_struct),
    reflexive("zone assets interleaved", zone_asset_struct),

    ENDIAN=">", SIZE=164, WIDGET=Halo3BitmapTagFrame,
    )


def get():
    return bitm_def

bitm_def = TagDef("bitm",
    h3_blam_header('bitm'),
    bitm_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["bitm"], endian=">", tag_cls=H3Tag
    )
