from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

def get(): return fmod_list_def


tag_ref = Container("tag_ref",
    UInt32('string_len'),
    StrUtf8('name', SIZE='.string_len', WIDGET_WIDTH=60),
    UInt32('idx'),
    UInt32('perm_count'),
    )

header = Struct("header",
    UInt32('unknown', DEFAULT=1),
    UInt32("tag_count"),
    )


fmod_list_def = TagDef('fmod_list',
    header,
    Array("tag_refs", SUB_STRUCT=tag_ref, SIZE=".header.tag_count"),
    ext='.bin', endian='<'
    )