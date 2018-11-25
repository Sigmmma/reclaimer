from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef


perf_performance = Struct("performance",
    Bool32("flags",
        ("disable_self_shadowing", 1 << 1),
        "disable_player_shadows",
        ),
    Float("water"),
    Float("decorators"),
    Float("effects"),
    Float("instanced_geometry"),
    Float("object_fade"),
    Float("object_lod"),
    Float("decals"),
    SInt32("cpu_light_count"),
    Float("cpu_light_quality"),
    SInt32("gpu_light_count"),
    Float("gpu_light_quality"),
    SInt32("shadow_count"),
    Float("shadow_quality"),
    ENDIAN=">", SIZE=56
    )


perf_meta_def = BlockDef("perf",
    reflexive("performance", perf_performance),
    TYPE=Struct, ENDIAN=">", SIZE=12
    )