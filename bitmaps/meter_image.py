from reclaimer.field_types import *
from supyr_struct.defs.tag_def import BlockDef


def linesize(parent=None, new_value=None, *args, **kwargs):
    if parent is None:
        raise KeyError
    if new_value is None:
        return 4*parent.width
    
    parent.width = new_value//4


def has_next_line(rawdata=None, *args, **kwargs):
    try:
        return len(rawdata.peek(6)) >= 6
    except Exception:
        return False

meter_line = Container("meter_line",
    FlUInt16("x_pos"),
    FlUInt16("y_pos"),
    FlUInt16("width"),
    BytesRaw("line_data", SIZE=linesize)
    )

meter_image = WhileArray("meter_image",
    CASE=has_next_line,
    SUB_STRUCT=meter_line
    )

meter_image_def = BlockDef(meter_image)
