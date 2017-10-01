from ..common_descs import *
from supyr_struct.defs.block_def import BlockDef


control_point = Struct("control point",
    QStruct("position", INCLUDE=ijk_float),
    QStruct("orientation", INCLUDE=ijkw_float),
    SIZE=28,
    )

trak_meta_def = BlockDef("trak",
    Pad(4),
    h2_meta_reflexive("control points", control_point, 16),
    ENDIAN="<", TYPE=Struct,
    )
