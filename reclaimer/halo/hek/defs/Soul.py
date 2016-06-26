from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

ui_widget_def = dependency("ui widget definition")

soul_body = Struct("tagdata",
    reflexive("ui widget definitions", ui_widget_def, 32),
    SIZE=12,
    )


def get():
    return soul_def

soul_def = TagDef("Soul",
    blam_header('Soul'),
    soul_body,#lol Megaman X4

    ext=".ui_widget_collection", endian=">"
    )
