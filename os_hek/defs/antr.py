from ...hek.defs.antr import *

antr_body = desc_variant(
    antr_body,
    ("animations", reflexive(
        "animations", animation_desc, 2048, DYN_NAME_PATH=".name"))
    )

def get():
    return antr_def

antr_def = TagDef("antr",
    blam_header('antr', 4),
    antr_body,

    ext=".model_animations", endian=">", tag_cls=AntrTag
    )
