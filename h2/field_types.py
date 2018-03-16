from ..field_types import *
from .field_type_methods import *


StringID = FieldType(base=QStruct, name="StringID")

H2TagRef     = FieldType(base=TagRef,      name="H2TagRef")
H2Reflexive  = FieldType(base=Reflexive,   name="H2Reflexive")
H2RawdataRef = FieldType(base=RawdataRef,  name="H2RawdataRef")

H2MetaTagRef     = FieldType(base=H2TagRef,      name="H2MetaTagRef")
H2MetaReflexive  = FieldType(base=H2Reflexive,   name="H2MetaReflexive")
H2MetaRawdataRef = FieldType(base=H2RawdataRef,  name="H2MetaRawdataRef",
                             parser=h2_rawdata_ref_parser)
