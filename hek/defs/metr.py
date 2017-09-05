from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef


def linesize(parent=None,new_value=None, *args, **kwargs):
    if parent is None:
        raise KeyError
    if new_value is None:
        return 4*parent.width
    
    parent.width = new_value//4


def has_next_line(rawdata=None, *args, **kwargs):
    try:
        return len(rawdata.peek(6)) >= 6
    except Exception:
        pass
    return False

meter_line = Container("meter_line",
    FlUInt16("x_pos"),
    FlUInt16("y_pos"),
    FlUInt16("width"),
    BytesRaw("line_data", SIZE=linesize)
    )

meter_image = WhileArray("data",
    CASE=has_next_line,
    SUB_STRUCT=meter_line
    )


meter_body = Struct("tagdata",
    Pad(4),
    dependency("stencil bitmap", "bitm"),
    dependency("source bitmap",  "bitm"),

    SInt16("stencil sequence index"),
    SInt16("source sequence index"),
    Pad(20),
    SEnum16("interpolate colors",
        "linearly",
        "faster near empty",
        "faster near full",
        "through random noise"
        ),
    SEnum16("anchor colors" ,
        "at both ends",
        "at empty",
        "at full"
        ),
    Pad(8),
    QStruct("empty color", INCLUDE=argb_float),
    QStruct("full color",  INCLUDE=argb_float),
    Pad(20),
    Float("unmask distance", SIDETIP="meter units"),
    Float("mask distance", SIDETIP="meter units"),
    Pad(12),
    FlUInt16("screen x pos", SIDETIP="pixels"),
    FlUInt16("screen y pos", SIDETIP="pixels"),
    FlUInt16("width", SIDETIP="pixels"),
    FlUInt16("height", SIDETIP="pixels"),

    rawdata_ref("meter data", max_size=65536),
    SIZE=172,
    )

def get():
    return metr_def

metr_def = TagDef("metr",
    blam_header('metr'),
    meter_body,

    subdefs={"meter_image":meter_image},
    ext=".meter", endian=">", tag_cls=HekTag
    )
