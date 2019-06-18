import os

from traceback import format_exc
from reclaimer.enums import hmt_icon_types

__all__ = ("parse_hmt_message", "extract_hud_message_text",
           "extract_string_list", "parse_hmt_message")


def parse_hmt_message(hmt_data, message_indices=None):
    string_data  = hmt_data.string.data
    messages = hmt_data.messages.STEPTREE
    elements = hmt_data.message_elements.STEPTREE
    if message_indices is None:
        message_indices = range(len(messages))
    elif not hasattr(message_indices, "__iter__"):
        message_indices = (message_indices, )

    strings = []
    for i in message_indices:
        m = messages[i]
        string = ""
        start = m.text_start
        for j in range(m.element_index, m.element_index + m.element_count):
            elem = elements[j]
            if elem.type.enum_name == "text":
                length  = elem.data.text.data
                string += string_data[start: start + length - 1]
                start  += length
            elif elem.type.enum_name == "icon":
                string += "%%%s" % hmt_icon_types[elem.data.icon.data]
            else:
                raise TypeError("Unknown element type %s" % elem.type.data)

        strings.append(string)

    return strings


def extract_hud_message_text(tagdata, tag_path, **kw):
    filepath = os.path.join(
        kw['out_dir'], os.path.splitext(tag_path)[0] + ".hmt")
    if os.path.isfile(filepath) and not kw.get('overwrite', True):
        return

    out_data = b""
    for i in range(tagdata.messages.size):
        try:
            name = tagdata.messages.STEPTREE[i].name
            string = parse_hmt_message(tagdata, i)[0]
        except Exception:
            print(format_exc())
            continue

        out_data += ("%s=%s" % (name, string)).encode("utf-16-le")
        out_data += b"\x0D\x00\x0A\x00"  # cr + lf

    try:
        folderpath = os.path.dirname(filepath)
        # If the path doesnt exist, create it
        if not os.path.exists(folderpath):
            os.makedirs(folderpath)

        with open(filepath, "wb") as f:
            f.write(b"\xFF\xFE")  # little endian unicode sig
            f.write(out_data)
    except Exception:
        return format_exc()

    return


def extract_string_list(tagdata, tag_path, encoding="latin-1", **kw):
    filepath = os.path.join(
        kw['out_dir'], os.path.splitext(tag_path)[0] + ".txt")
    if os.path.isfile(filepath) and not kw.get('overwrite', True):
        return

    out_data = b""
    for b in tagdata.strings.STEPTREE:
        string = b.data
        string += "\r\n###END-STRING###\r\n"  # cr + lf
        out_data += string.encode(encoding)

    try:
        folderpath = os.path.dirname(filepath)
        # If the path doesnt exist, create it
        if not os.path.exists(folderpath):
            os.makedirs(folderpath)

        with open(filepath, "wb") as f:
            if encoding == "utf-16-le":
                f.write(b"\xFF\xFE")  # little endian unicode sig
            f.write(out_data)
    except Exception:
        return format_exc()


def extract_unicode_string_list(tagdata, tag_path, **kw):
    return extract_string_list(tagdata, tag_path, "utf-16-le", **kw)
