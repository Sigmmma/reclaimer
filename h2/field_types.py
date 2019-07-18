from reclaimer.field_types import *
from reclaimer.h2.field_type_methods import h2_rawdata_ref_parser,\
     h2_tag_ref_parser

H2TagRef = FieldType(base=TagRef, name="H2TagRef", parser=h2_tag_ref_parser)
H2Reflexive  = FieldType(base=Reflexive,   name="H2Reflexive")
H2RawdataRef = FieldType(base=RawdataRef,  name="H2RawdataRef",
                         parser=h2_rawdata_ref_parser)
