from array import array
from ..common_descs import *
from supyr_struct.defs.block_def import BlockDef

hsc__meta_def = BlockDef("hsc*",
    ascii_str32("name"),
    h2_meta_rawtext_ref("source"),
    ENDIAN="<", TYPE=Struct,
    )
