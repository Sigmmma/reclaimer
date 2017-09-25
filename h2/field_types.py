from ..field_types import *
from .field_type_methods import *


StringID = FieldType(base=QStruct, name="StringID")

H2MetaTagIndexRef = FieldType(base=TagIndexRef, name="H2MetaIndexRef")
H2MetaReflexive   = FieldType(base=Reflexive,   name="H2MetaReflexive")
H2MetaRawdataRef  = FieldType(base=RawdataRef,  name="H2MetaRawdataRef",
                              parser=h2_rawdata_ref_parser)
H2TagIndexRef = FieldType(base=H2MetaTagIndexRef, name="H2IndexRef")
H2Reflexive   = FieldType(base=H2MetaReflexive,   name="H2Reflexive")
H2RawdataRef  = FieldType(base=H2MetaRawdataRef,  name="H2RawdataRef")
