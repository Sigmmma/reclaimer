#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

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

os_senv_ext = Struct("shader_environment_extension",
    Bool16("dlm_flags",
        "do_not_use_dlms",
        COMMENT=dlm_comment
        ),
    Pad(2),
    Float("bump_amount"),

    dependency_os("specular_color_map", "bitm", COMMENT=dlm_specular_map_comment),
    Float("specular_color_coefficient"),
    Float("specular_color_exponent"),
    Bool16("specular_flags",
        "alpha_as_exponent_mask",
        ),
    Pad(2),

    float_zero_to_one("perpendicular_brightness", COMMENT=dlm_tint_comment),
    QStruct("perpendicular_tint_color", INCLUDE=rgb_float),
    float_zero_to_one("parallel_brightness"),
    QStruct("parallel_tint_color", INCLUDE=rgb_float),

    Float("specular_lighting_exponent", COMMENT=dlm_specular_comment),
    Float("specular_lighting_coefficient"),

    SIZE=100,
    )

# replace the padding with an open sauce shader environment extension reflexive
senv_attrs = dict(senv_attrs)
senv_attrs[3] = reflexive("os_shader_environment_ext", os_senv_ext, 1)

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

    ext=".shader_environment", endian=">", tag_cls=ShdrTag
    )
