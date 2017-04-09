from ..field_types import *
from .field_type_methods import *

H2Reflexive   = FieldType(base=Reflexive,   name="H2Reflexive")
H2RawdataRef  = FieldType(base=RawdataRef,  name="H2RawdataRef")
H2TagIndexRef = FieldType(base=TagIndexRef, name="H2TagIndexRef")
TBFDContainer = FieldType(
    base=Container, name="TBFDContainer",
    parser=tbfd_parser, serializer=tbfd_serializer)
