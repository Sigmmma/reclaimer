#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from traceback import format_exc
from reclaimer.enums import hmt_icon_types
from reclaimer.util import convert_newlines_to_unix

__all__ = ("compile_hud_message_text",
           "compile_unicode_string_list", "compile_string_list")


icon_type_map = {hmt_icon_types[i]: i for i in range(len(hmt_icon_types))}
MAX_ICON_NAME_LENGTH = max(*(len(name) for name in hmt_icon_types))


def compile_hud_message_text(hmt_tag, hmt_string_data):
    message_strings = {}
    message_names = []

    line_num = 0
    for line in hmt_string_data.lstrip('\ufeff').split("\n"):
        line = line.rstrip()
        line_num += 1
        if not line:
            continue
        elif "=" in line:
            name, message = line.split("=", 1)
        else:
            name, message = line, ""

        if name in message_strings:
            print("    ERROR: Duplicate message name on line %s" % line_num)
            continue

        if len(name) > 31:
            print(("    WARNING: Message name on line %s is too long. " +
                   "Truncating name to '%s'" ) % (line_num, name[: 31]))
            name = name[: 31]

        if name and message:
            message_strings[name] = message
            message_names.append(name)
        elif name and not message and "=" in line:
            print("    WARNING: Empty message on line %s" % line_num)
            message_strings[name] = ""
            message_names.append(name)
        elif not name and message:
            print("    ERROR: No message name on line %s" % line_num)
        else:
            print("    ERROR: No name or message on line %s" % line_num)

    if len(message_strings) > 1024:
        print("    ERROR: Too many hud messages. Please remove %s of them." %
              (len(message_strings) - 1024))
        return

    tagdata = hmt_tag.data.tagdata
    elements = tagdata.message_elements.STEPTREE
    messages = tagdata.messages.STEPTREE
    tagdata.string.data = ""
    del elements[:]
    del messages[:]

    error = False
    text_blob = ""
    for name in message_names:
        message_string = message_strings[name]

        messages.append()
        message = messages[-1]
        message.name = name
        message.text_start = len(text_blob)
        message.element_index = len(elements)

        if len(message_string) == 0:
            elements.append()
            element = elements[-1]
            element.data.set_active("text")
            element.data.text.data = 1  # set length to 1
            message.element_count = 1
            text_blob += "\x00"
            continue

        i = 0
        while i < len(message_string):
            elements.append()
            element = elements[-1]
            message.element_count += 1

            element_base = i
            icon_name = ""
            curr_text = ""
            c = message_string[i]
            if c == "%":
                element.type.set_to("icon")
                element.data.set_active("icon")
            else:
                element.type.set_to("text")
                element.data.set_active("text")
                curr_text += c

            i += 1
            element_type = element.type.enum_name
            while (i < len(message_string) and
                   len(curr_text) < 254 and
                   len(icon_name) < MAX_ICON_NAME_LENGTH):
                c = message_string[i]
                if c == "%":
                    break

                i += 1
                if element_type == "text":
                    curr_text += c
                else:
                    icon_name += c
                    if icon_name in icon_type_map:
                        break

            if element_type == "text":
                # add the delimiter
                element.data.text.data = len(curr_text) + 1
                text_blob += curr_text + "\x00"
            elif icon_name in icon_type_map:
                element.data.icon.data = icon_type_map[icon_name]
            else:
                print("    WARNING: Unknown icon type specified in message '%s'" % name)
                i = element_base + 1
                del elements[-1]
                message.element_count -= 1

    if len(elements) > 8192:
        print("    ERROR: Too many message elements. " +
              "Please simplify your messages.")
        error = True

    if len(text_blob) > 32768:
        print(("    ERROR: String data too large by %s characters. " +
              "Please simplify your messages.") %
              (len(text_blob) - 32768))
        error = True

    # replace the string data
    tagdata.string.data = text_blob

    return error


def compile_unicode_string_list(ustr_tag, string_data):
    return compile_strings(ustr_tag, string_data, True)


def compile_string_list(str_tag, string_data):
    return compile_strings(str_tag, string_data, False)


def compile_strings(tag, string_data, unicode=False):
    if unicode:
        tag_ext = "unicode_string_list"
        tag_cls = "ustr"
        max_str_len = 32768
    else:
        tag_ext = "string_list"
        tag_cls = "str#"
        max_str_len = 4096

    string_data = convert_newlines_to_unix(string_data)

    strings = string_data.split("\n###END-STRING###\n")
    if len(strings) > 32767:
        print("    WARNING: Too many strings. Truncating to 32767.")
        del strings[32768: ]

    for i in range(len(strings)):
        string = strings[i]
        if len(strings) > max_str_len:
            print(("    WARNING: String %s is too long." +
                   " Truncating to %s characters") % (i, max_str_len))
            strings[i] = string[max_str_len: ]

    tag_strings = tag.data.tagdata.strings.STEPTREE
    del tag_strings[:]

    for string in strings:
        tag_strings.append()
        tag_string = tag_strings[-1]
        tag_string.data = string
