from ...os_hek.defs.senv import *

dlm_comment = """DIRECTIONAL LIGHTMAP PROPERTIES
Special shader settings for when your map has directional lightmaps rendered for it."""

dlm_specular_map_comment = """DLM SPECULAR (COLOR) MAP
*RGB holds the specular color.
*ALPHA can be used as an exponent mask to provide finer control 
over the size of the specular highlights."""

dlm_tint_comment = """DLM SPECULAR TINT AND BRIGHTNESS"""

dlm_specular_comment = """DLM SPECULAR INTENSITY
Exponent controls the highlight size, the bigger the exponent, the smaller the highlight.
Coefficient controls the brightness of the highlights."""

os_senv_ext = Struct("shader environment extension",
    Bool16("dlm flags",
        "do not use dlms",
        COMMENT=dlm_comment
        ),
    Pad(2),
    Float("bump amount"),

    dependency_os("specular color map", "bitm", COMMENT=dlm_specular_map_comment),
    Float("specular color coefficient"),
    Float("specular color exponent"),
    Bool16("specular flags",
        "alpha as exponent mask",
        ),
    Pad(2),

    float_zero_to_one("perpendicular brightness", COMMENT=dlm_tint_comment),
    QStruct("perpendicular tint color", INCLUDE=rgb_float),
    float_zero_to_one("parallel brightness"),
    QStruct("parallel tint color", INCLUDE=rgb_float),

    Float("specular lighting exponent", COMMENT=dlm_specular_comment),
    Float("specular lighting coefficient"),

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
