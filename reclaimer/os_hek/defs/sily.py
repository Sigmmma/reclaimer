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

text_value_pair = Struct("text_value_pair",
    Bool8("flags",
        "default_setting",
        "unchanged_setting",
        ),
    Pad(3),

    SInt32("integer"),
    Float("real"),
    dependency_os("string_id", "sidy"),
    Pad(4),
    dependency_os("label_string_id", "sidy"),
    Pad(4),
    dependency_os("description_string_id", "sidy"),

    SIZE=72
    )

sily_body = Struct("tagdata",
    dependency_os("parameter", "sidy"),
    Pad(4),
    dependency_os("title_text", "sidy"),
    Pad(4),
    dependency_os("description_text", "sidy"),

    Pad(4),
    SEnum16("type",
        "integer",
        "string_id",
        "unused",
        "real",
        ),

    Pad(2),
    reflexive("text_value_pairs", text_value_pair, 32),
    SIZE=76
    )

def get():
    return sily_def

sily_def = TagDef("sily",
    blam_header_os('sily', 0),
    sily_body,

    ext=".text_value_pair_definition", endian=">", tag_cls=HekTag
    )
