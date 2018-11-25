from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

jmrq_sandbox_text_value_pair_text_value_pair_expected_value_type = (
    "integer_index",
    "stringid_reference",
    "incremental",
    )


jmrq_sandbox_text_value_pair_text_value_pair = Struct("text_value_pairs",
    Bool8("flags",
        "default",
        "unchanged",
        ),
    SEnum8("expected_value_type", *jmrq_sandbox_text_value_pair_text_value_pair_expected_value_type),
    SInt16("unknown"),
    SInt32("int_value"),
    string_id_meta("ref_name"),
    string_id_meta("name"),
    string_id_meta("description"),
    ENDIAN=">", SIZE=20
    )


jmrq_sandbox_text_value_pair = Struct("sandbox_text_value_pairs",
    string_id_meta("parameter_name"),
    reflexive("text_value_pairs", jmrq_sandbox_text_value_pair_text_value_pair),
    ENDIAN=">", SIZE=16
    )


jmrq_meta_def = BlockDef("jmrq",
    reflexive("sandbox_text_value_pairs", jmrq_sandbox_text_value_pair),
    TYPE=Struct, ENDIAN=">", SIZE=12
    )