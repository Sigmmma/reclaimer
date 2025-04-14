#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.tagc import *

tag_reference = desc_variant(tag_reference, dependency_os("tag"))

tagc_body = desc_variant(tagc_body,
    reflexive("tag_references", tag_reference, 200,
        DYN_NAME_PATH='.tag.filepath'
        )
    )


def get():
    return tagc_def

tagc_def = TagDef("tagc",
    blam_header('tagc'),
    tagc_body,

    ext=".tag_collection", endian=">", tag_cls=HekTag
    )
