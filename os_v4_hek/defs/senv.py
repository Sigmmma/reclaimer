from ...hek.defs.senv import *

os_senv_ext = Struct("shader environment extension",
    BBool16("flags",
        "do not use dlms",
        ),
    Pad(2),
    BFloat("bump amount"),

    Struct("dlm color",
        dependency_os("map", "bitm"),
        BFloat("specular exponent"),
        BFloat("specular coefficient"),
        BBool16("flags",
            "alpha as exponent mask",
            ),
        Pad(2),
        ),

    QStruct("dlm tint and brightness",
        BFloat("perpendicular brightness"),
        BFloat("perpendicular tint color"),
        BFloat("parallel brightness"),
        BFloat("parallel tint color"),
        ),

    QStruct("dlm intensity",
        BFloat("lighting exponent"),
        BFloat("lighting coefficient"),
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
