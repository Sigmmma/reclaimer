from traceback import format_exc

from reclaimer.enums import hmt_icon_types


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
