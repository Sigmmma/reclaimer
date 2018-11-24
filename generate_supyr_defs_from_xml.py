import os
from collections import OrderedDict
from xml.etree.ElementTree import ElementTree
from traceback import format_exc
from supyr_struct.defs.util import str_to_identifier


block_def_import_str = '''from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef'''

name_only_field_types = set((
    "string_id_meta", "rawdata_ref", "dependency",
    "Float", "float_rad",
    "color_argb_float", "color_argb_uint32",
    "color_rgb_float",  "color_xrgb_uint32", 
    "SInt8", "SInt16", "SInt32", "UInt8", "UInt16", "UInt32",
    ))

do_not_indent_field_types = set(name_only_field_types)
do_not_indent_field_types.add("reflexive")
do_not_indent_field_types.add("BytesRaw")
do_not_indent_field_types.add("StrLatin1")
do_not_indent_field_types.add("StrUTF16")
do_not_indent_field_types.add("Pad")
do_not_indent_field_types.add("string_id_meta")

string_field_types = set((
    "BytesRaw", "StrLatin1", "StrUTF16",
    ))

enum_field_types = set((
    "SEnum8", "SEnum16", "SEnum32", "UEnum8", "UEnum16", "UEnum32"
    ))

bool_field_types = set(("Bool8", "Bool16", "Bool32"))


field_sizes = {
    "reflexive": 12, "rawdata_ref": 20, "dependency": 16,
    "color_argb_float": 16, "color_argb_uint32": 4, 
    "color_rgb_float": 12,  "color_xrgb_uint32": 4,
    "Float": 4, "float_rad": 4, "string_id_meta": 4,
    "SInt8":  1, "SInt16":  2, "SInt32":  4,
    "UInt8":  1, "UInt16":  2, "UInt32":  4,
    "SEnum8": 1, "SEnum16": 2, "SEnum32": 4,
    "UEnum8": 1, "UEnum16": 2, "UEnum32": 4,
    "Bool8":  1, "Bool16":  2, "Bool32":  4,

    # special values
    "bit": 1, "opt": 1, "Pad": 4
    }

type_name_map = {
    "raw": "BytesRaw", "undefined": "Pad",
    "reflexive": "reflexive", "dataref": "rawdata_ref", "tagref": "dependency",
    "float32": "Float", "float": "Float", "degree": "float_rad",
    "int8": "SInt8",  "int16": "SInt16",  "int32": "SInt32",
    "uint8": "UInt8", "uint16": "UInt16", "uint32": "UInt32",
    "enum8": "SEnum8",  "enum16": "SEnum16",  "enum32": "SEnum32",
    "uenum8": "UEnum8", "uenum16": "UEnum16", "uenum32": "UEnum32",
    "bitfield8": "Bool8", "bitfield16": "Bool16", "bitfield32": "Bool32",
    "ascii": "StrLatin1", "utf16": "StrUTF16",
    "stringid": "string_id_meta",
    "colorf": "color_argb_float", "color32": "color_argb_uint32",
    "colorfnoalpha": "color_rgb_float", "color24": "color_xrgb_uint32",

    "shader": "UInt32", "string": "UInt32", "uniclist": "UInt32",

    # special values
    "bit": "bit", "option": "opt", "plugin": "BlockDef"
    }

ignored_names = set(("comment", "revisions", "revision"))

name_fix_replacements = dict(
    index="idx", count="size", insert="ins", 
    )


class StructNode(list):
    typ = ""
    name = "unknown"
    size = 0
    offset = 0
    visible = True
    value = 0


def struct_node_to_supyr_desc(struct_node, descs_by_name, enum_names_by_desc,
                              parent_name="", indent=0):
    desc_name = struct_node.name
    if parent_name and struct_node.typ == "reflexive":
        if desc_name.endswith("s"):
            desc_name = desc_name[: -1]
        desc_name = "%s_%s" % (parent_name, desc_name)

    if struct_node.typ == "BlockDef":
        indent = 1

    indent_str = ' ' * (4 * indent)

    desc_name = fix_name_identifier(desc_name)

    if struct_node.typ == "reflexive":
        desc_str = 'Struct('
    elif struct_node.typ == "BlockDef":
        desc_str = 'BlockDef('
    else:
        desc_str = '%s%s(' % (indent_str, struct_node.typ)

    if struct_node.typ == "Pad":
        desc_str += str(struct_node.size)
        indent_str = ""
    else:
        desc_str += '"%s"' % struct_node.name
        if struct_node.typ in name_only_field_types:
            indent_str = ""
        else:
            desc_str += ','

            if struct_node.typ in string_field_types:
                desc_str += " SIZE=%s" % struct_node.size
                indent_str = ""

            if struct_node.typ in enum_field_types:
                i = 0
                last_val = -1
                enum_str = ""
                for enum in struct_node:
                    if enum.value == i or (enum.value - last_val == 1):
                        enum_str += '%s"%s",\n' % (
                            indent_str, enum.name)
                    else:
                        enum_str += '%s("%s", %s),\n' % (
                            indent_str, enum.name, enum.value)
                    i += 1
                    last_val = enum.value

                enum_str = "(\n%s%s)" % (enum_str, indent_str)
                enum_name = "%s_%s" % (parent_name, desc_name)
                if enum_str in enum_names_by_desc:
                    enum_name = enum_names_by_desc[enum_str]
                else:
                    enum_names_by_desc[enum_str] = enum_name

                desc_str += " *%s" % (enum_name)
                indent_str = ""

                #indent_str = ' ' * (4 * (indent + 1))
            elif struct_node.typ in bool_field_types:
                desc_str += '\n'
                i = 0
                j = last_val = -1
                for bit in struct_node:
                    j += 1
                    if bit.name in ("_%s" % j, "_%s" % (j + 1),
                                    "bit_%s" % j, "bit_%s" % (j + 1)):
                        continue

                    if bit.value == i or (bit.value - last_val == 1):
                        desc_str += '%s%s"%s",\n' % (
                            indent_str, indent_str, bit.name)
                    else:
                        desc_str += '%s%s("%s", 1 << %s),\n' % (
                            indent_str, indent_str,
                            bit.name, bit.value)
                    last_val = bit.value
                    i += 1
                indent_str = ' ' * (4 * (indent + 1))
            elif struct_node.typ in ("BlockDef", "reflexive"):
                desc_str += '\n'
                for field in struct_node:
                    subdesc_str = struct_node_to_supyr_desc(
                        field, descs_by_name, enum_names_by_desc, desc_name, 1)

                    if field.typ == "reflexive":
                        desc_str += '    reflexive("%s", %s)' % (
                            field.name, subdesc_str)
                    else:
                        desc_str += subdesc_str

                    desc_str += ",\n"

    if struct_node.typ in ("reflexive", "BlockDef"):
        desc_str += indent_str
        if struct_node.typ == "BlockDef":
            desc_name += "_meta_def"
            desc_str += "TYPE=Struct, "

        desc_str += 'ENDIAN=">", SIZE=%s\n' % struct_node.size

    desc_str += indent_str + ')'

    if struct_node.typ in ("reflexive", "BlockDef"):
        descs_by_name[desc_name] = desc_str
        return desc_name

    return desc_str


def fix_name_identifier(name):
    if name[: 1] in "0123456789":
        name = "_" + name

    name = str_to_identifier(name).rstrip("_")
    return name_fix_replacements.get(name, name)


def parse_xml_node(xml_node):
    new_node = StructNode()
    xml_tag = xml_node.tag.lower()
    if xml_tag in ignored_names:
        return None

    xml_attribs = {key.lower(): xml_node.attrib[key]
                   for key in xml_node.attrib}

    xml_tag = xml_tag.replace("colour", "color")

    if xml_tag == "tagref" and not eval(xml_attribs.get(
            'withclass', "true").capitalize()):
        xml_tag = "uint32"
    elif xml_tag.startswith("colorf") and xml_attribs.get(
            'format', "rgb") == "rgb":
        xml_tag = "colorfnoalpha"


    if xml_tag in type_name_map:
        new_node.typ = type_name_map[xml_tag]
    else:
        raise TypeError("Unknown field type '%s'" % xml_node.tag)

    new_node.name = fix_name_identifier(
        xml_attribs.get('name', "unnamed").lower())
    new_node.offset = eval(xml_attribs.get('offset', "None"))
    new_node.visible = eval(xml_attribs.get('visible', "true").capitalize())

    if "basesize" in xml_attribs:
        new_node.size = eval(xml_attribs['basesize'])
    elif "size" in xml_attribs:
        new_node.size = eval(xml_attribs['size'])
    elif "entrysize" in xml_attribs:
        new_node.size = eval(xml_attribs['entrysize'])
    elif "length" in xml_attribs:
        new_node.size = eval(xml_attribs['length'])
    else:
        new_node.size = field_sizes.get(new_node.typ, 0)

    if "index" in xml_attribs:
        new_node.value = eval(xml_attribs['index'])
    else:
        new_node.value = eval(xml_attribs.get('value', "None"))

    if new_node.offset is None:
        new_node.offset = new_node.value

    sub_nodes_by_offset = {}
    for xml_subnode in xml_node:
        new_sub_node = parse_xml_node(xml_subnode)
        if new_sub_node is not None:
            sub_nodes_by_offset[new_sub_node.offset] = new_sub_node

    for off in sorted(sub_nodes_by_offset):
        sub_node = sub_nodes_by_offset[off]
        if sub_node.typ == "color_xrgb_uint32":
            # adjust for 4 byte based colors
            sub_node.offset -= 1
            sub_nodes_by_offset.pop(off)
            if sub_node.offset in sub_nodes_by_offset:
                # change it to an alpha based color
                sub_node.typ = "color_argb_uint32"
            sub_nodes_by_offset[sub_node.offset] = sub_node

    last_off = 0
    last_node = None
    added_names = dict()
    for off in sorted(sub_nodes_by_offset):
        sub_node = sub_nodes_by_offset[off]
        sub_node_size = sub_node.size
        if sub_node.typ == "reflexive":
            sub_node_size = 12

        if "Enum" in new_node.typ or "Bool" in new_node.typ:
            pass
        elif last_node is not None and (sub_node.typ == "Pad" and
                                        last_node.typ == "Pad"):
            # consolidate consecutive padding
            last_node.size += sub_node_size
            last_off = off + sub_node_size
            #print("PADDED")
            continue
        elif off - last_off:
            # add missing padding
            pad_node = StructNode()
            pad_node.typ = "Pad"
            pad_node.name = "unknown"
            pad_node.size = off - last_off
            pad_node.offset = pad_node.value = last_off
            new_node.append(pad_node)
            
            added_names[pad_node.name] = added_names.get(
                pad_node.name, 0) + 1
            if added_names[pad_node.name] > 1:
                pad_node.name += "_%s" % (added_names[pad_node.name] - 1)

            if pad_node.size < 0:
                raise ValueError(
                    ("Negative padding size in '%s' at field "
                     "'%s' of type '%s' at offset '%s'") %
                    (new_node.name, sub_node.name,
                     sub_node.typ, sub_node.offset))
            #print("PADDED")

        # take care of fields with the same name
        added_names[sub_node.name] = added_names.get(
            sub_node.name, 0) + 1
        if added_names[sub_node.name] > 1:
            sub_node.name += "_%s" % (added_names[sub_node.name] - 1)

        new_node.append(sub_node)
        last_off = off + sub_node_size
        last_node = sub_node

    return new_node


def parse_xml(xml_path):
    try:
        xml_root = ElementTree().parse(xml_path)
        tag_id = os.path.splitext(os.path.basename(xml_path))[0].strip(".")
        nodes = parse_xml_node(xml_root)
        nodes.name = tag_id + (" " * (4 - len(tag_id)))
    except:
        print(format_exc())
        nodes = None

    return nodes


for root, dirs, files in os.walk("."):
    for fname in files:
        xml_name, ext = os.path.splitext(fname)
        if ext.lower() != ".xml":
            continue

        xml_path = os.path.join(root, fname)
        print(xml_path)
        tag_struct_nodes = parse_xml(xml_path)
        if tag_struct_nodes is None:
            continue

        descs_by_name = OrderedDict()
        enum_names_by_desc = dict()
        struct_node_to_supyr_desc(tag_struct_nodes, descs_by_name,
                                  enum_names_by_desc)

        with open(os.path.join(root, xml_name) + ".py", "w+") as pyf:
            pyf.write(block_def_import_str)
            enum_descs_by_name = {enum_names_by_desc[desc]: desc for
                                  desc in enum_names_by_desc}

            for desc_name in sorted(enum_descs_by_name):
                pyf.write("\n\n")
                desc_str = enum_descs_by_name[desc_name]
                pyf.write("%s = %s" % (desc_name, desc_str.strip(",")))

            for desc_name in descs_by_name:
                pyf.write("\n\n\n")
                desc_str = descs_by_name[desc_name]
                pyf.write("%s = %s" % (desc_name, desc_str.strip(",")))


print("Finished")
