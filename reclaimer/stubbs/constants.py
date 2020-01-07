#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.constants import *
from reclaimer.util import fourcc_to_int

# maps tag class four character codes(fccs) in
# their string encoding to their int encoding.
stubbs_tag_class_fcc_to_be_int = {}
stubbs_tag_class_fcc_to_le_int = {}
# maps tag class four character codes(fccs) in
# their int encoding to their string encoding.
stubbs_tag_class_be_int_to_fcc = {}
stubbs_tag_class_le_int_to_fcc = {}


stubbs_tag_class_fcc_to_ext = dict(
    terr="terrain",
    vege="vegetation",
    imef="image_effect",
    **tag_class_fcc_to_ext
    )

for tag_cls in stubbs_tag_class_fcc_to_ext:
    stubbs_tag_class_fcc_to_be_int[tag_cls] = fourcc_to_int(tag_cls)
    stubbs_tag_class_be_int_to_fcc[fourcc_to_int(tag_cls)] = tag_cls
    stubbs_tag_class_fcc_to_le_int[tag_cls] = fourcc_to_int(tag_cls)
    stubbs_tag_class_le_int_to_fcc[fourcc_to_int(tag_cls)] = tag_cls
