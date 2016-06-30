from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

# gotta name this tag_ref cause 'tag' would
# conflict with the tag attribute in Blocks
tag_reference = dependency("tag ref")

tagc_body = Struct("tagdata",
    reflexive("tag references", tag_reference, 200),
    SIZE=12,
    )


def get():
    return tagc_def

tagc_def = TagDef("tagc",
    blam_header('tagc'),
    tagc_body,

    ext=".tag_collection", endian=">"
    )
