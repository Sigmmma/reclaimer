from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

string_data_struct = RawDataRef("string",
    INCLUDE=Raw_Data_Ref_Struct,
    CHILD=FlStrUTF16("raw_string_data", SIZE=".Count"),
    SIZE=20
    )

ustr_body = Struct("Data",
    Reflexive("strings",
        INCLUDE=Reflexive_Struct,

        CHILD=Array("strings array",
            MAX=32767, SIZE=".Count",
            SUB_STRUCT=string_data_struct
            )
        ),
    SIZE=12,
    )


def get():
    return ustr_def

ustr_def = TagDef(
    com( {1:{DEFAULT:"ustr" }}, Tag_Header),
    ustr_body,
    
    NAME="unicode_string_list",
    
    ext=".unicode_string_list", def_id="ustr", endian=">"
    )
