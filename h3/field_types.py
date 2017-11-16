from ..field_types import *

H3MetaTagIndexRef = FieldType(base=TagRef, name="H3MetaIndexRef")
H3MetaReflexive   = FieldType(base=Reflexive,   name="H3MetaReflexive")
H3MetaRawdataRef  = FieldType(base=RawdataRef,  name="H3MetaRawdataRef")
H3TagIndexRef = FieldType(base=H3MetaTagIndexRef, name="H3IndexRef")
H3Reflexive   = FieldType(base=H3MetaReflexive,   name="H3Reflexive")
H3RawdataRef  = FieldType(base=H3MetaRawdataRef,  name="H3RawdataRef")
