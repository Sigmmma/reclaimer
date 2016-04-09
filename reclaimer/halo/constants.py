from supyr_struct.defs.constants import *

PC_TAG_INDEX_HEADER_SIZE   = 40
XBOX_TAG_INDEX_HEADER_SIZE = 36

XBOX_BSP_MAGIC = 2174377984

XBOX_INDEX_MAGIC = 2151309348
PC_INDEX_MAGIC   = 1078198312

#I cant imagine Halo allowing any one field even close to this many
#indices, though I have seen some open sauce stuff go over 180,000.
MAX_REFLEXIVE_COUNT = 2**31-1
