from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

tag_reference = dependency("tag")

tagc_body = Struct("Data",
    reflexive("tag references", tag_reference, 200),
    SIZE=12,
    )


def get():
    return tagc_def

tagc_def = TagDef(
    blam_header('tagc'),
    tagc_body,
    
    NAME="tag_collection",
    
    ext=".tag_collection", def_id="tagc", endian=">"
    )
