#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.h2.common_descs import *
from supyr_struct.defs.tag_def import TagDef

hsc__body = Struct("tagdata",
    ascii_str32("name"),
    h2_rawtext_ref("source"),
    ENDIAN="<", SIZE=40
    )


def get():
    return hsc__def

hsc__def = TagDef("hsc*",
    h2_blam_header('hsc*'),
    hsc__body,

    ext=".%s" % h2_tag_class_fcc_to_ext["hsc*"], endian="<"
    )
