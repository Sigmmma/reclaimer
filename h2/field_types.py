from ..field_types import *
from .field_type_methods import *

H2TagRef     = FieldType(base=TagRef,      name="H2TagRef")
H2Reflexive  = FieldType(base=Reflexive,   name="H2Reflexive")
H2RawdataRef = FieldType(base=RawdataRef,  name="H2RawdataRef",
                         parser=h2_rawdata_ref_parser)
