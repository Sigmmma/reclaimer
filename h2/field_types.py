from ..field_types import *
from .field_type_methods import *


StringID = FieldType(base=QStruct, name="StringID")

H2MetaTagRef     = FieldType(base=TagRef,      name="H2MetaTagRef")
H2MetaReflexive  = FieldType(base=Reflexive,   name="H2MetaReflexive")
H2MetaRawdataRef = FieldType(base=RawdataRef,  name="H2MetaRawdataRef",
                              parser=h2_rawdata_ref_parser)
H2TagRef     = FieldType(base=H2MetaTagRef,      name="H2TagRef")
H2Reflexive  = FieldType(base=H2MetaReflexive,   name="H2Reflexive")
H2RawdataRef = FieldType(base=H2MetaRawdataRef,  name="H2RawdataRef")
