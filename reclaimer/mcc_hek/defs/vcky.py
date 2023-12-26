#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

def get(): return vcky_def

virtual_key = Struct("virtual_key",
    SEnum16("keyboard_key",
        {NAME:"one", GUI_NAME:"1"},
        {NAME:"two", GUI_NAME:"2"},
        {NAME:"three", GUI_NAME:"3"},
        {NAME:"four", GUI_NAME:"4"},
        {NAME:"five", GUI_NAME:"5"},
        {NAME:"six", GUI_NAME:"6"},
        {NAME:"seven", GUI_NAME:"7"},
        {NAME:"eight", GUI_NAME:"8"},
        {NAME:"nine", GUI_NAME:"9"},
        {NAME:"zero", GUI_NAME:"0"},
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
        "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
        "done",
        "shift",
        "capslock",
        "symbols",
        "backspace",
        "left",
        "right",
        "space",
        ),
    SInt16("lowercase_character"),
    SInt16("shift_character"),
    SInt16("caps_character"),
    SInt16("symbols_character"),
    SInt16("shift_caps_character", GUI_NAME="shift+caps character"),
    SInt16("shift_symbols_character", GUI_NAME="shift+symbols character"),
    SInt16("caps_symbols_character", GUI_NAME="caps+symbols character"),
    dependency("unselected_background_bitmap", "bitm"),
    dependency("selected_background_bitmap", "bitm"),
    dependency("active_background_bitmap", "bitm"),
    dependency("sticky_background_bitmap", "bitm"),
    SIZE=80
    )

vcky_body = Struct("tagdata",
    dependency("display_font", "font"),
    dependency("background_bitmap", "bitm"),
    dependency("special_key_labels_string_list", "ustr"),
    reflexive("virtual_keys", virtual_key, 44,
        DYN_NAME_PATH='.keyboard_key.enum_name'),
    SIZE=60,
    )

vcky_def = TagDef("vcky",
    blam_header('vcky', 2),
    vcky_body,

    ext=".virtual_keyboard", endian=">", tag_cls=HekTag
    )
