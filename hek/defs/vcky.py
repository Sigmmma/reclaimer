from ...common_descs import *
from .objs.tag import HekTag
from supyr_struct.defs.tag_def import TagDef

def get(): return vcky_def

virtual_key = Struct("virtual key",
    SEnum16("keyboard key",
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
    SInt16("lowercase character"),
    SInt16("shift character"),
    SInt16("caps character"),
    SInt16("symbols character"),
    SInt16("shift+caps character"),
    SInt16("shift+symbols character"),
    SInt16("caps+symbols character"),
    dependency("unselected background bitmap", "bitm"),
    dependency("selected background bitmap", "bitm"),
    dependency("active background bitmap", "bitm"),
    dependency("sticky background bitmap", "bitm"),
    SIZE=80
    )

vcky_body = Struct("tagdata",
    dependency("display font", "font"),
    dependency("background bitmap", "bitm"),
    dependency("special key labels string list", "ustr"),
    reflexive("virtual keys", virtual_key, 44,
        DYN_NAME_PATH='.keyboard_key.enum_name'),
    SIZE=60,
    )

vcky_def = TagDef("vcky",
    blam_header('vcky', 2),
    vcky_body,

    ext=".virtual_keyboard", endian=">", tag_cls=HekTag
    )
