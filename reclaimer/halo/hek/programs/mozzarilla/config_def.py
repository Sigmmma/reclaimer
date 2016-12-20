from supyr_struct.apps.binilla.config_def import *
from supyr_struct.apps.binilla.constants import *
from supyr_struct.field_types import *
from supyr_struct.defs.tag_def import TagDef

new_method_enums = (
    {GUI_NAME:"open dependency scanner", NAME:"show_dependency_viewer"},
    {GUI_NAME:"open tag scanner", NAME:"show_tag_scanner"},
    {GUI_NAME:"choose tags directory", NAME:"set_tags_dir"},
    )

method_enums += new_method_enums

hotkey = Struct("hotkey",
    BitStruct("combo",
        BitUEnum("modifier", GUI_NAME="", *modifier_enums, SIZE=4),
        BitUEnum("key", GUI_NAME="and", *hotkey_enums, SIZE=28),
        SIZE=4, ORIENT='h',
        ),
    UEnum32("method", *method_enums)
    )

config_header = Struct("header",
    LUEnum32("id", ('Moze', 'ezoM'), VISIBLE=False, DEFAULT='ezoM'),
    INCLUDE=config_header
    )

hotkeys = Array("hotkeys", SUB_STRUCT=hotkey, SIZE=".array_counts.hotkey_count")

tag_window_hotkeys = Array("tag_window_hotkeys", SUB_STRUCT=hotkey,
                           SIZE=".array_counts.tag_window_hotkey_count")

tag_dirs = Array("tag_dirs",
    SUB_STRUCT=filepath, SIZE=".mozzarilla.tag_dirs_count", MAX=4,
    NAME_MAP=(
        "halo_1_tags_dir", "halo_1_os_tags_dir",
        "halo_1_map_tags_dir", "halo_1_misc_tags_dir"
        ),
    EDITABLE=False, VISIBLE=False
    )

mozzarilla = Struct("mozzarilla",
    Bool16("flags",
        ),
    UEnum16("selected_handler",
        "halo_1",
        "halo_1_os",
        "halo_1_map",
        "halo_1_misc",
        EDITABLE=False, VISIBLE=False
        ),
    Pad(64 - 2*2),

    UInt32("tag_dirs_count", VISIBLE=False, EDITABLE=False),
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
    colors,
    hotkeys,
    tag_window_hotkeys,

    mozzarilla,
    tag_dirs,
    ENDIAN='<', ext=".cfg",
    )


def extra_data_size(parent=None, new_value=None, **kwargs):
    if parent is None:
        raise KeyError()
    if new_value is None:
        return parent.extra_data_size * 4

    parent.extra_data_size = new_value // 4


def has_next_tag(rawdata=None, **kwargs):
    '''Returns whether or not there is another block in the stream.'''
    try:
        offset = kwargs.get('offset')
        try:
            offset += kwargs.get('root_offset')
        except Exception:
            pass
        return rawdata.peek(4, offset) == b'\x01\x00\x00\x00'
    except AttributeError:
        return False

extra_data_sizes = {
    "actv": 1, "tagc": 1, "mgs2": 1, "lens": 1,
    "elec": 2,
    "bitm": 3, "sky ": 3, "phys": 3,
    "obje": 6, "eqip": 6, "garb": 6, "scen": 6,
    "plac": 6, "mach": 6, "lifi": 6, "ctrl": 6,
    "proj": 7,
    "unit": 8,
    "mode": 12, "mod2": 12,
    "antr": 22,
    "coll": 15, "bipd": 15,
    "matg": 19,
    "sbsp": 53,
    "scnr": 61,
    # This dictionary is incomplete since I havent
    # checked all of known tags for their sizes.
    }

window_header = Struct("window_header",
    UInt32("struct_size", DEFAULT=44),
    Pad(24),
    #UInt32("unknown1"),
    #UInt32("unknown2", DEFAULT=1),
    # These raw bytes seem to be some sort of window coordinates, but idc
    #BytesRaw("unknown3", DEFAULT=b'\xff'*16, SIZE=16),

    QStruct("top_left_corner",     UInt32("x"), UInt32("y"), ORIENT="h"),
    QStruct("bottom_right_corner", UInt32("x"), UInt32("y"), ORIENT="h"),
    SIZE=44
    )

open_halo_tag = Container("open_tag",
    UInt32("is_valid_tag", DEFAULT=1),
    window_header,
    UInt8("filepath_len"),
    StrRawAscii("filepath", SIZE='.filepath_len'),
    Pad(8),
    UInt16("extra_data_size"),
    BytesRaw("extra_data", SIZE=extra_data_size),
    )

guerilla_workspace_def = TagDef("guerilla_workspace",
    window_header,
    WhileArray("tags",
        SUB_STRUCT=open_halo_tag,
        CASE=has_next_tag
        ),
    UInt32("eof_marker"),

    ENDIAN='<', ext=".cfg"
    )
