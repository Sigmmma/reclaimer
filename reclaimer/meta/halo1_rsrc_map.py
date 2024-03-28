#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.common_descs import *
from reclaimer.meta.objs.halo1_rsrc_map import Halo1RsrcMapTag
from supyr_struct.defs.tag_def import TagDef


def get():
    return halo1_rsrc_map_def


def tag_path_pointer(parent=None, new_value=None, **kwargs):
    if parent is None:
        raise KeyError()
    t_head = parent.parent
    if new_value is None:
        return t_head.parent.parent.tag_paths_pointer + t_head.path_offset
    t_head.path_offset = new_value - t_head.parent.parent.tag_paths_pointer


rsrc_tag = Container("tag",
    BytesRaw("data", SIZE="..size", POINTER="..offset"),
    CStrTagRef("path", POINTER=tag_path_pointer, MAX=768, WIDGET=EntryFrame),
    )

tag_header = Struct("tag header",
    LUInt32("path offset"),
    LUInt32("size"),
    LUInt32("offset"),
    STEPTREE=rsrc_tag
    )

halo1_rsrc_map_def = TagDef("halo1_rsrc_map",
    LUEnum32("resource type",
        'NONE',
        'bitmaps',
        'sounds',
        'strings'
        ),
    LPointer32("tag paths pointer"),
    LPointer32("tag headers pointer"),
    LUInt32("tag count"),
    Array("tags",
        SIZE='.tag_count', SUB_STRUCT=tag_header,
        POINTER='.tag_headers_pointer',
        ),
    endian="<", ext=".map", tag_cls=Halo1RsrcMapTag
    )

lite_rsrc_tag = Container("tag",
    Void("data"),
    CStrLatin1("path", POINTER=tag_path_pointer),
    )
lite_tag_header = Struct("tag header",
    INCLUDE=tag_header, STEPTREE=lite_rsrc_tag
    )
lite_halo1_rsrc_map_desc = dict(halo1_rsrc_map_def.descriptor)
lite_halo1_rsrc_map_desc[4] = Array("tags",
    SIZE='.tag_count', SUB_STRUCT=lite_tag_header,
    POINTER='.tag_headers_pointer',
    )
lite_halo1_rsrc_map_def = TagDef("lite_halo1_rsrc_map",
    descriptor=lite_halo1_rsrc_map_desc,
    endian="<", ext=".map", tag_cls=Halo1RsrcMapTag
    )
