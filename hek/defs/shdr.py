from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

shdr_attrs = Struct("shdr attrs",
    Bool16("radiosity flags",
        "simple parameterization",
        "ignore normals",
        "transparent lit",
        ),
    SEnum16("radiosity detail level" ,
        "high",
        "medium",
        "low",
        "turd",
        ),
    Float("radiosity light power"),
    QStruct("radiosity light color", INCLUDE=rgb_float),
    QStruct("radiosity tint color",  INCLUDE=rgb_float),

    Pad(2),
    SEnum16("material type", *materials_list),
    # THIS FIELD IS OFTEN INCORRECT ON STOCK TAGS.
    # This seems to be a Guerilla-only optimization value
    FlSEnum16("shader type",
        ("shdr", -1),  # Shader
        ("senv", 3),   # Environment
        ("soso", 4),   # Model
        ("sotr", 5),   # Transparent Generic
        ("schi", 6),   # Transparent Chicago
        ("scex", 7),   # Transparent Chicago Extended
        ("swat", 8),   # Water
        ("sgla", 9),   # Glass
        ("smet", 10),  # Meter
        ("spla", 11),  # Plasma
        DEFAULT=-1, EDITABLE=False,
        ),
    Pad(2),
    SIZE=40
    )

shader_body = Struct("tagdata",
    shdr_attrs,
    SIZE=40
    )

def get():
    return shdr_def

shdr_def = TagDef("shdr",
    blam_header('shdr'),
    shader_body,

    ext=".shader", endian=">", tag_cls=HekTag
    )
