from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

ui_widget_def = dependency("ui widget definition")

soul_body = Struct("Data",
    reflexive("ui widget definitions", ui_widget_def, 32),
    SIZE=12,
    )


def get():
    return soul_def

soul_def = TagDef(
    blam_header('Soul'),
    soul_body,#lol Megaman X4
    
    NAME="ui_widget_collection",
    
    ext=".ui_widget_collection", def_id="Soul", endian=">"
    )
