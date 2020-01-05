#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from ...hek.defs.objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

script_variable = Struct("script_variable",
    ascii_str32("script_variable_name"),
    ascii_str32("exposed_parameter_name"),
    SIZE=80
    )

effect = Struct("effect",
    dependency_os("effect", "efpg"),
    ascii_str32("name"),
    reflexive("script_variables", script_variable, 32,
        DYN_NAME_PATH='.script_variable_name'),
    SIZE=72
    )

activation_control = Struct("activation_control",
    SEnum16("state",
        "initially_active",
        "is_in_cutscene",
        "player_is_zoomed",
        "player_is_using_a_vehicle"
        ),
    Bool16("flags",
        "invert"
        ),
    SIZE=4
    )

effect_instance = Struct("effect_instance",
    ascii_str32("name"),
    dyn_senum16("effect",
        DYN_NAME_PATH="tagdata.effects.STEPTREE[DYN_I].effect.filepath"),
    SEnum16("render_stage",
        "after_bsp_and_before_blur",
        "after_blur_and_before_alphad_faces",
        "after_alphad_faces_and_before_hud",
        "after_hud_and_before_menu",
        "after_menu",
        ),
    QStruct("quad_tesselation",
        SInt16("x"), SInt16("y"), ORIENT="h"
        ),
    from_to_zero_to_one("x_screen_bounds"),
    from_to_zero_to_one("y_screen_bounds"),

    Pad(12),
    SEnum16("activation_operation",
        "all",
        "any"
        ),

    Pad(6),
    reflexive("activation_controls", activation_control, 8),

    SIZE=116
    )

efpc_body = Struct("tagdata",
    Pad(12),
    # since there APPEARS to be a reflexive in the tag, but it
    # doesnt show up in Guerilla, I'm gonna turn it into padding
    # and leave this as a reminder that a reflexive might exist.
    #reflexive("unknown", void_desc, 0),
    Pad(12),
    reflexive("effects", effect, 32,
        DYN_NAME_PATH='.name'),
    reflexive("effect_instances", effect_instance, 32,
        DYN_NAME_PATH='.name'),
    SIZE=48
    )

def get():
    return efpc_def

efpc_def = TagDef("efpc",
    blam_header_os('efpc'),
    efpc_body,

    ext=".effect_postprocess_collection", endian=">", tag_cls=HekTag
    )
