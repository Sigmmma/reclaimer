from ..field_types import *
from .field_type_methods import *

H2TagRef = FieldType(base=TagRef, name="H2TagRef",
                     parser=h2_tag_ref_parser, serializer=h2_tag_ref_serializer)
H2Reflexive  = FieldType(base=Reflexive,   name="H2Reflexive")
H2RawdataRef = FieldType(base=RawdataRef,  name="H2RawdataRef",
                         parser=h2_rawdata_ref_parser)
