#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...hek.defs.scnr import *
from ..common_descs import *
from .objs.scnr import StubbsScnrTag

reference = desc_variant(reference, dependency_stubbs("reference"))

scnr_body = desc_variant(scnr_body,
    reflexive("references", reference, 256, DYN_NAME_PATH='.reference.filepath'),
    )

def get():
    return scnr_def

# TODO: update dependencies
scnr_def = TagDef("scnr",
    blam_header('scnr', 2),
    scnr_body,

    ext=".scenario", endian=">", tag_cls=StubbsScnrTag
    )
