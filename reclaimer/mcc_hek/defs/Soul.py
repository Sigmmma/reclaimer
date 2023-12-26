#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

ui_widget_def = Struct("ui_widget_definition",
    dependency("ui_widget_definition", 'DeLa'),
    SIZE=16
    )

soul_body = Struct("tagdata",
    reflexive("ui_widget_definitions", ui_widget_def, 32,
        DYN_NAME_PATH='.ui_widget_definition.filepath'),
    SIZE=12,
    )


def get():
    return Soul_def

Soul_def = TagDef("Soul",
    blam_header('Soul'),
    soul_body,#lol Megaman X4

    ext=".ui_widget_collection", endian=">", tag_cls=HekTag
    )
