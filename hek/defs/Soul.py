from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

ui_widget_def = Struct("ui widget definition",
    dependency("ui widget definition", 'DeLa'),
    SIZE=16
    )

soul_body = Struct("tagdata",
    reflexive("ui widget definitions", ui_widget_def, 32,
        DYN_NAME_PATH='.ui_widget_definition.filepath'),
    SIZE=12,
    )


def get():
    return soul_def

soul_def = TagDef("Soul",
    blam_header('Soul'),
    soul_body,#lol Megaman X4

    ext=".ui_widget_collection", endian=">", tag_cls=HekTag
    )
