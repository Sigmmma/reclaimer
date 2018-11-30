############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/11/30  01:44
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef


vtsh_unknown_1_unknown = Struct("unknown", 
    BytesRaw("unknown", SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


vtsh_unknown_1 = Struct("unknown_1", 
    h3_reflexive("unknown", vtsh_unknown_1_unknown),
    VISIBLE=False,
    ENDIAN=">", SIZE=12
    )


vtsh_vertex_shader_unknown_2 = Struct("unknown_2", 
    h3_string_id("unknown_0", VISIBLE=False),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=8
    )


vtsh_vertex_shader = Struct("vertex_shader", 
    h3_rawdata_ref("unknown_0", VISIBLE=False),
    h3_rawdata_ref("unknown_1", VISIBLE=False),
    h3_reflexive("unknown_2", vtsh_vertex_shader_unknown_2),
    BytesRaw("unknown_3", SIZE=24, VISIBLE=False),
    UInt32("vertex_shader"),
    ENDIAN=">", SIZE=80
    )


vtsh_meta_def = BlockDef("vtsh", 
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    h3_reflexive("unknown_1", vtsh_unknown_1),
    BytesRaw("unknown_2", SIZE=4, VISIBLE=False),
    h3_reflexive("vertex_shaders", vtsh_vertex_shader),
    TYPE=Struct, ENDIAN=">", SIZE=32
    )