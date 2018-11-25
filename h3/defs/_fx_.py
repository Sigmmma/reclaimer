from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


_fx_additional_sound_input = Struct("additional_sound_inputs",
    string_id_meta("dsp_effect"),
    rawdata_ref("low_frequency_sound_function"),
    Float("time_period"),
    ENDIAN=">", SIZE=28
    )


_fx__meta_def = BlockDef("<fx>",
    Pad(12),
    SInt32("input_effect_name"),
    reflexive("additional_sound_inputs", _fx_additional_sound_input),
    TYPE=Struct, ENDIAN=">", SIZE=28
    )
