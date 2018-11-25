from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


snde_meta_def = BlockDef("snde",
    Pad(4),
    SInt16("priority"),
    SInt16("unknown_1"),
    Float("room_intensity"),
    Float("room_intensity_high_frequency"),
    Float("room_rolloff"),
    Float("decay_time"),
    Float("decay_high_frequency_ratio"),
    Float("reflections_intensity"),
    Float("reflections_delay"),
    Float("reverb_intensity"),
    Float("reverb_delay"),
    Float("diffusion"),
    Float("density"),
    Float("high_frequency_refrence"),
    Pad(16),
    TYPE=Struct, ENDIAN=">", SIZE=72
    )