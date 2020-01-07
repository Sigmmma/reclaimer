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

string_reference = Struct("string_reference",
    dependency_os("string_id", "sidy"),
    SInt32("english_offset"),
    SInt32("unused_offset_1"),
    SInt32("unused_offset_2"),
    SInt32("unused_offset_3"),
    SInt32("unused_offset_4"),
    SInt32("unused_offset_5"),
    SInt32("unused_offset_6"),
    SInt32("unused_offset_7"),
    SInt32("unused_offset_8"),
    SIZE=56
    )

unic_body = Struct("tagdata",
    reflexive("string_references", string_reference, 9216,
        DYN_NAME_PATH='.string_id.filepath'),
    Pad(12),
    rawtext_ref("string_data_utf8", StrUtf8, max_size=18874368),

    SIZE=80
    )

def get():
    return unic_def

unic_def = TagDef("unic",
    blam_header_os('unic', 0),
    unic_body,

    ext=".multilingual_unicode_string_list", endian=">", tag_cls=HekTag
    )
