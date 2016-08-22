from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef


def linesize(block=None, parent=None, attr_index=None,
             rawdata=None, new_value=None, *args, **kwargs):
    if parent is None:
        raise KeyError
    if new_value is None:
        return 4*parent.width
    
    parent.width = new_value//4


def has_next_line(block=None, parent=None, attr_index=None,
                 rawdata=None, new_value=None, *args, **kwargs):
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
    dependency("stencil bitmap", valid_bitmaps),
    dependency("source bitmap",  valid_bitmaps),

    BSInt16("stencil sequence index"),
    BSInt16("source sequence index"),
    Pad(20),
    BSEnum16("interpolate colors",
        "linearly",
        "faster near empty",
        "faster near full",
        "through random noise"
        ),
    BSEnum16("anchor colors" ,
        "at both ends",
        "at empty",
        "at full"
        ),
    Pad(8),
    QuickStruct("empty color", INCLUDE=argb_float),
    QuickStruct("full color",  INCLUDE=argb_float),
    Pad(20),
    BFloat("unmask distance"),
    BFloat("mask distance"),
    Pad(12),
    FlUInt16("screen_x_pos"),
    FlUInt16("screen_y_pos"),
    FlUInt16("width"),
    FlUInt16("height"),

    rawdata_ref("meter data"),
    SIZE=172,
    )

def get():
    return metr_def

metr_def = TagDef("metr",
    blam_header('metr'),
    meter_body,

    subdefs={"meter_image":meter_image},
    ext=".meter", endian=">"
    )
