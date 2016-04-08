from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

string_data_struct = RawDataRef("string",
    INCLUDE=Raw_Data_Ref_Struct,
    CHILD=StrLatin1("raw_string_data", SIZE=".Count"),
    SIZE=20
    )

str__body = Struct("Data",
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
    return str__def

str__def = TagDef(
    com( {1:{DEFAULT:"str#" }}, Tag_Header),
    str__body,
    
    NAME="string_list",
    
    ext=".string_list", def_id="str#", endian=">"
    )
