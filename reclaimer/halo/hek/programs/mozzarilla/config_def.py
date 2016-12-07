from supyr_struct.apps.binilla.config_def import *
from supyr_struct.apps.binilla.constants import *
from supyr_struct.field_types import *
from supyr_struct.defs.tag_def import TagDef

config_header = Struct("header",
    UInt32("id", DEFAULT='ezoM'),
    INCLUDE=config_header
    )

tag_dirs = Array("tag_dirs",
    SUB_STRUCT=filepath, SIZE=".mozzarilla.tag_dirs_count", MAX=4,
    NAME_MAP=(
        "halo_1_tags_dir", "halo_1_os_tags_dir",
        "halo_1_map_tags_dir", "halo_1_misc_tags_dir"
        )
    )

mozzarilla = Struct("mozzarilla",
    Bool16("flags",
        ),
    UEnum16("selected_handler",
        "halo_1",
        "halo_1_os",
        "halo_1_map",
        "halo_1_misc",
        ),
    Pad(64 - 2*2),

    UInt32("tag_dirs_count", VISIBLE=False),
    SIZE=128
    )

config_def = TagDef("mozzarilla_config",
    config_header,
    array_counts,
    app_window,
    widgets,
    open_tags,
    recent_tags,
    directory_paths,
    widget_depths,
    colors,
    hotkeys,
    tag_window_hotkeys,

    mozzarilla,
    tag_dirs,
    ENDIAN='<', ext=".cfg",
    )
