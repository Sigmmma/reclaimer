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

shader_pass = Struct("pass",
    ascii_str32("name"),
    Bool16("flags",
        "clear_target",
        "copy_scene_to_target",
        "clear_buffer_texture",
        ),
    SEnum16("render_chain",
        "main_chain",
        "buffer_chain"
        ),
    SIZE=48,
    )

technique = Struct("entry",
    ascii_str32("name"),
    Bool16("shader_model",
        {NAME: "sm_1_0", GUI_NAME: "1.0"},
        {NAME: "sm_2_0", GUI_NAME: "2.0"},
        {NAME: "sm_3_0", GUI_NAME: "3.0"},
        ),

    Pad(18),
    reflexive("shader_pass", shader_pass, 32,
        DYN_NAME_PATH='.name'),
    SIZE=64
    )

shpp_attrs = Struct("shpp",
    Pad(24),
    rawdata_ref("shader_code_binary", max_size=32768),

    Pad(64),
    reflexive("techniques", technique, 3,
        DYN_NAME_PATH='.name'),
    reflexive("predicted_resources", predicted_resource, 1024, VISIBLE=False),
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
