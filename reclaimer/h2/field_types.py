#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.field_types import *
from reclaimer.h2.field_type_methods import h2_rawdata_ref_parser,\
     h2_tag_ref_parser

H2TagRef = FieldType(base=TagRef, name="H2TagRef", parser=h2_tag_ref_parser)
H2Reflexive  = FieldType(base=Reflexive,   name="H2Reflexive")
H2RawdataRef = FieldType(base=RawdataRef,  name="H2RawdataRef",
                         parser=h2_rawdata_ref_parser)
