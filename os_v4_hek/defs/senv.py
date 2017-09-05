from ...hek.defs.senv import *

os_senv_ext = Struct("shader environment extension",
    Bool16("flags",
        "do not use dlms",
        ),
    Pad(2),
    Float("bump amount"),

    Struct("dlm color",
        dependency_os("map", "bitm"),
        Float("specular exponent"),
        Float("specular coefficient"),
        Bool16("flags",
            "alpha as exponent mask",
            ),
        Pad(2),
        ),

    QStruct("dlm tint and brightness",
        Float("perpendicular brightness"),
        Float("perpendicular tint color"),
        Float("parallel brightness"),
        Float("parallel tint color"),
        ),

    QStruct("dlm intensity",
        Float("lighting exponent"),
        Float("lighting coefficient"),
        ),

    SIZE=100,
    )

# replace the padding with an open sauce shader environment extension reflexive
senv_attrs = dict(senv_attrs)
senv_attrs[3] = reflexive("os shader environment ext", os_senv_ext, 1)

senv_body = Struct("tagdata",
    shdr_attrs,
    senv_attrs,
    SIZE=836,
    )

def get():
    return senv_def

senv_def = TagDef("senv",
    blam_header('senv', 2),
    senv_body,

    ext=".shader_environment", endian=">", tag_cls=HekTag
    )
