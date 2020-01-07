#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from supyr_struct.defs.common_descs import *
from supyr_struct.field_types import *
from supyr_struct.defs.tag_def import TagDef

from binilla.constants import VISIBILITY_METADATA

def get(): return composer_playlist_def


def get_str_len(parent=None, attr_index=None, path=None, new_value=None,
                **kwargs):
    if parent is None:
        raise KeyError()
    elif new_value is not None:
        parent.set_neighbor(path, new_value - 1)
        return
    else:
        return parent.get_neighbor(path) + 1


command = Struct("command",
    UEnum32("sig",
        ("Cmnd", "dnmC"),
        DEFAULT="dnmC", VISIBLE=VISIBILITY_METADATA,
        ),
    UInt16("perm_index"),
    Pad(2),
    BitStruct("play_info",
        UBitInt("loop_count", SIZE=10),
        Bit("endless_loop"),
        Bit("play_any"),
        Bit("play_alt"),
        Bit("play_ordered"),
        Bit("skip"),
        SIZE=4
        ),
    SIZE=16
    )


command_list = Struct("command_list",
    UEnum32("sig",
        ("Clst", "tslC"),
        DEFAULT="tslC", VISIBLE=VISIBILITY_METADATA
        ),
    UInt32("lsnd_path_len", VISIBLE=VISIBILITY_METADATA),
    UInt32("lsnd_path_pointer", VISIBLE=VISIBILITY_METADATA),

    UInt32("command_count", VISIBLE=VISIBILITY_METADATA),
    UInt32("commands_pointer", VISIBLE=VISIBILITY_METADATA),

    UInt32("lsnd_tag_pointer", VISIBLE=VISIBILITY_METADATA),
    UInt32("play_length", DEFAULT=180),

    SIZE=64,
    STEPTREE=Container("data",
        StrLatin1("lsnd_path", SIZE=lambda *a, **k:
            get_str_len(*a, path="..lsnd_path_len", **k)),
        Array("commands", SUB_STRUCT=command, SIZE="..command_count")
        )
    )


header = Struct("header",
    UEnum32("sig",
        ("Play", "yalP"),
        DEFAULT="yalP", VISIBLE=VISIBILITY_METADATA,
        ),

    UInt32("tags_dir_len", VISIBLE=VISIBILITY_METADATA),
    UInt32("tags_dir_pointer", VISIBLE=VISIBILITY_METADATA),

    UInt32("command_list_count", VISIBLE=VISIBILITY_METADATA),
    UInt32("command_list_pointer", VISIBLE=VISIBILITY_METADATA),

    Bool32("flags",
        "shuffle",
        "loop",
        ),
    SIZE=64
    )


composer_playlist_def = TagDef('composer_playlist',
    header,
    StrLatin1("tags_dir", SIZE=lambda *a, **k:
        get_str_len(*a, path=".header.tags_dir_len", **k)),
    Array("command_lists",
        SIZE=".header.command_list_count",
        SUB_STRUCT=command_list
        ),

    ext='.play', endian='<',
    )
