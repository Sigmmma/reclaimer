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

child_ids = Struct("child_id",
    dyn_senum32("entry_reference",
        DYN_NAME_PATH="tagdata.entries.STEPTREE[DYN_I].name.data"),
    SIZE=4
    )

referenced_by = Struct("referenced_by", INCLUDE=child_ids)

entry = Struct("entry",
    rawtext_ref("name", StrUtf8, max_size=256, widget=EntryFrame),
    UEnum32("group_tag", INCLUDE=valid_tags_os),
    SInt32("handle_data"),
    SInt32("flags"),
    reflexive("child_ids", child_ids, 65536),
    reflexive("referenced_by", referenced_by, 65536),
    SIZE=68
    )

tag__body = Struct("tagdata",
    reflexive("entries", entry, 65536, DYN_NAME_PATH='.name.data'),
    SIZE=36
    )

def get():
    return tag__def

tag__def = TagDef("tag+",
    blam_header_os('tag+'),
    tag__body,

    ext=".tag_database", endian=">", tag_cls=HekTag
    )
