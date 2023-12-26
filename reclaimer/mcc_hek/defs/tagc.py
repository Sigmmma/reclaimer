#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

tag_reference = Struct("tag_reference",
    dependency("tag"),
    SIZE=16
    )

tagc_body = Struct("tagdata",
    reflexive("tag_references", tag_reference, 200,
        DYN_NAME_PATH='.tag.filepath'),
    SIZE=12,
    )


def get():
    return tagc_def

tagc_def = TagDef("tagc",
    blam_header('tagc'),
    tagc_body,

    ext=".tag_collection", endian=">", tag_cls=HekTag
    )
