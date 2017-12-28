from ...common_descs import *
from ...hek.defs.objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

shader_pass = Struct("pass",
    ascii_str32("name"),
    Bool16("flags",
        "clear target",
        "copy scene to target",
        "clear buffer texture",
        ),
    SEnum16("render chain",
        "main chain",
        "buffer chain"
        ),
    SIZE=48,
    )

technique = Struct("entry",
    ascii_str32("name"),
    Bool16("shader model",
        "sm 1.0",
        "sm 2.0",
        "sm 3.0",
        ),

    Pad(18),
    reflexive("shader pass", shader_pass,
        DYN_NAME_PATH='.name'),
    SIZE=64
    )

shpp_attrs = Struct("shpp",
    Pad(24),
    rawdata_ref("shader code binary", max_size=32768),

    Pad(64),
    reflexive("techniques", technique,
        DYN_NAME_PATH='.name'),
    reflexive("predicted resources", predicted_resource, 1024, VISIBLE=False),
    SIZE=164
    )

shpp_body = Struct("tagdata", shpp_attrs)

def get():
    return shpp_def

shpp_def = TagDef("shpp",
    blam_header_os('shpp'),
    shpp_body,

    ext=".shader_postprocess", endian=">", tag_cls=HekTag
    )
