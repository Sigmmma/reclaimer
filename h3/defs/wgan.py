from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


wgan_meta_def = BlockDef("wgan",
    string_id_meta("unknown"),
    Pad(4),
    dependency("widget_color"),
    dependency("widget_position"),
    dependency("widget_rotation"),
    dependency("widget_scale"),
    dependency("widget_texture_coordinate"),
    dependency("widget_sprite"),
    dependency("widget_font"),
    TYPE=Struct, ENDIAN=">", SIZE=120
    )