import os
from collections import OrderedDict
from xml.etree.ElementTree import ElementTree
from traceback import format_exc
from supyr_struct.defs.util import str_to_identifier


block_def_import_str = '''from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef'''

name_only_field_types = set((
    "string_id_meta", "rawdata_ref", "dependency",
    "float_rad", "yp_float_rad", "ypr_float_rad",
    "float_deg", "yp_float_deg", "ypr_float_deg",
    "color_argb_float", "color_argb_uint32",
    "color_rgb_float",  "color_xrgb_uint32", 
    "Float", "from_to_rad",
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
    index="idx", count="size", insert="ins", parent="ancestor"
    )

prefix_chains = [
    (("min_", "minimum_"), ("max_", "maximum_",)),
    ]

suffix_chains = [
    (("_min", "_minimum"), ("_max", "_maximum",)),
    (("_u",), ("_v",), ("_w",)), (("_y",), ("_p",), ("_r",)),
    (("_x",), ("_y",), ("_z",), ("_w",)),  # some specify xyz instead of ijk
    (("_i",), ("_j",), ("_k",), ("_w",)),
    (("_a", "_alpha", "alpha"), ("_r", "_red", "red"),
     ("_g", "_green", "green"), ("_b", "_blue", "blue")),
    (("_r", "_red", "red"), ("_g", "_green", "green"),
     ("_b", "_blue", "blue")),
    ]


class StructNode(list):
    typ = ""
    name = "unknown"
    size = 0
    offset = 0
    visible = True
    value = 0

    include = ""


def fix_name_identifier(name):
    if name[: 1] == "-" and name[1: 2] != "-":
        name = "neg_" + name[1: ]

    if name[: 1] in "0123456789":
        name = "_" + name

    name = str_to_identifier(name).rstrip("_")
    return name_fix_replacements.get(name, name)


def replace_struct_node_section(struct_node, start, count,
                                typ, size, name, include):
    new_node = StructNode()
    new_node.typ = typ
    new_node.size = size
    new_node.name = name
    new_node.include = include
    new_node.offset = struct_node[start].offset
    new_node.visible = struct_node[start].visible
    print("    Replacing %s '%s' with '%s' including '%s'" %
          (count, struct_node[start].typ, typ, include))
    struct_node[start: start + count] = [new_node]


def optimize_common_structs(struct_node):
    if (struct_node.typ in bool_field_types or
        struct_node.typ in enum_field_types):
        return

    start = 0
    while start < len(struct_node):
        # keep checking fields in the node until it's finished

        field_names_str = node_base_name = new_typ = ""
        field_ct = 0
        check_suffix = check_prefix = True
        while start + field_ct < len(struct_node):
            field = struct_node[start + field_ct]
            name = field.name.lower()
            suffix = prefix = true_suffix = true_prefix = ""
            curr_node_base_name = ""

            for prefix_chain in prefix_chains:
                if not check_prefix: break
                curr_prefix_chain_str = curr_prefix = curr_true_prefix = ""
                for i in range(len(prefix_chain)):
                    curr_prefix = prefix_chain[i][0]
                    # detect the prefix
                    curr_true_prefix = ""
                    for s in prefix_chain[i]:
                        if name.startswith(s):
                            curr_true_prefix = s
                            break

                    if curr_true_prefix:
                        # found the prefix this field ends with
                        break
                    else:
                        # didnt find it. add the current prefix to the chain
                        curr_prefix_chain_str += curr_prefix

                if curr_prefix_chain_str == field_names_str:
                    prefix = curr_prefix
                    true_prefix = curr_true_prefix
                    break

            for suffix_chain in suffix_chains:
                if not check_suffix: break
                curr_suffix_chain_str = curr_suffix = curr_true_suffix = ""
                for i in range(len(suffix_chain)):
                    curr_suffix = suffix_chain[i][0]
                    # detect the suffix
                    curr_true_suffix = ""
                    for s in suffix_chain[i]:
                        if name.endswith(s):
                            curr_true_suffix = s
                            break

                    if curr_true_suffix:
                        # found the suffix this field ends with
                        break
                    else:
                        # didnt find it. add the current suffix to the chain
                        curr_suffix_chain_str += curr_suffix

                if curr_suffix_chain_str == field_names_str:
                    suffix = curr_suffix
                    true_suffix = curr_true_suffix
                    break

            if true_suffix and check_suffix:
                field_ct += 1
                curr_node_base_name = name[: -len(true_suffix)]
                check_prefix = False
            elif true_prefix and check_prefix:
                field_ct += 1
                curr_node_base_name = name[len(true_prefix): ]
                check_suffix = False
            else:
                break

            if field_ct == 1:
                node_base_name = curr_node_base_name

            if curr_node_base_name != node_base_name:
                break
            elif check_prefix:
                field_names_str += prefix
            elif check_suffix:
                field_names_str += suffix

        typ_check = "Float"
        optimize = True
        new_typ = "QStruct"
        new_include = ""
        new_size = 0
        field_names_str = field_names_str.strip("_")
        field_typ = struct_node[start].typ
        if field_names_str == "a_r_g_b":
            if not node_base_name: node_base_name = "color"

            if field_typ == "Float":
                new_typ = "color_argb_float"
                new_size = 16
            elif field_typ == "UInt8":
                new_typ = "color_argb_uint32"
                typ_check = "UInt8"
                new_size = 4
            else:
                optimize = False
        elif field_names_str == "r_g_b":
            if not node_base_name: node_base_name = "color"

            if field_typ == "Float":
                new_typ = "color_rgb_float"
                new_size = 12
            elif field_typ == "UInt8":
                new_typ = "color_xrgb_uint32"
                typ_check = "UInt8"
                new_size = 4
            else:
                optimize = False
        elif field_names_str == "x_y_z":
            if not node_base_name: node_base_name = "position"

            if field_typ == "Float":
                new_include = "xyz_float"
                new_size = 12
            else:
                optimize = False
        elif field_names_str == "x_y":
            if not node_base_name: node_base_name = "position"

            if field_typ == "Float":
                new_include = "xy_float"
                new_size = 8
            else:
                optimize = False
        elif field_names_str in ("i_j_k_w", "x_y_z_w"):
            if not node_base_name: node_base_name = "rotation"

            if field_typ == "Float":
                new_include = "ijkw_float"
                new_size = 16
            elif field_typ == "SInt16":
                new_include = "ijkw_sint16"
                typ_check = "SInt16"
                new_size = 8
            else:
                optimize = False
        elif field_names_str == "i_j_k":
            if not node_base_name: node_base_name = "rotation"

            if field_typ == "Float":
                new_include = "ijk_float"
                new_size = 12
            elif field_typ == "float_rad":
                new_typ = "ypr_float_rad"
                typ_check = "float_rad"
            elif field_typ == "SInt16":
                new_include = "ijk_sint16"
                typ_check = "SInt16"
                new_size = 6
            else:
                optimize = False
        elif field_names_str == "i_j":
            if not node_base_name: node_base_name = "angle"

            new_size = 8
            if field_typ == "Float":
                new_include = "ij_float"
            elif field_typ == "float_rad":
                new_typ = "yp_float_rad"
                typ_check = "float_rad"
            elif field_typ == "SInt16":
                new_include = "ij_sint16"
                typ_check = "SInt16"
                new_size = 4
            else:
                optimize = False
        elif field_names_str == "u_v":
            if not node_base_name: node_base_name = "tex position"

            if field_typ == "Float":
                new_include = "uv_float"
                new_size = 8
            else:
                optimize = False
        elif field_names_str == "y_p_r":
            if not node_base_name: node_base_name = "angle"

            new_size = 12
            if field_typ == "Float":
                new_typ = "ypr_float_deg"
            elif field_typ == "float_rad":
                new_typ = "ypr_float_rad"
                typ_check = "float_rad"
            else:
                optimize = False
        elif field_names_str == "y_p":
            if not node_base_name: node_base_name = "angle"

            new_size = 8
            if field_typ == "Float":
                new_typ = "yp_float_deg"
            elif field_typ == "float_rad":
                new_typ = "yp_float_rad"
                typ_check = "float_rad"
            else:
                optimize = False
        elif field_names_str == "min_max":
            if not node_base_name: node_base_name = "bounds"

            new_size = 8
            if field_typ == "Float":
                new_include = "from_to"
            elif field_typ == "float_rad":
                new_typ = "from_to_rad"
                typ_check = "float_rad"
            elif field_typ[1: ] in ("Int32", "Int16", "Int8"):
                new_include = "from_to_" + field_typ.lower()
                typ_check = field_typ
                if field_typ in ("UInt16", "SInt16"):
                    new_size = 4
                elif field_typ in ("UInt8", "SInt8"):
                    new_size = 2
            else:
                optimize = False
        else:
            optimize = False

        if optimize:
            for i in range(start, start + field_ct):
                if struct_node[i].typ != typ_check:
                    optimize = False
                    break

        if optimize:
            replace_struct_node_section(struct_node, start, field_ct, new_typ,
                                        new_size, node_base_name, new_include)

        start += 1


def optimize_numbered_arrays(struct_node):
    if (struct_node.typ in bool_field_types or
        struct_node.typ in enum_field_types):
        return

    return
    # TODO: MAKE THIS WORK
    # REMINDER: Need to split by  _num  _num_  or  num_  depending
    # on where in the field name the integer is
    start = 0
    while start < len(struct_node):
        # keep checking fields in the node until it's finished
        field_names_str = node_base_name = new_typ = ""
        field_ct = 0

        if optimize:
            for i in range(start, start + field_ct):
                if struct_node[i].typ != typ_check:
                    optimize = False
                    break

        if optimize:
            replace_struct_node_section(struct_node, start, field_ct, new_typ,
                                        new_size, node_base_name, new_include)

        start += 1


def optimize_struct_node(struct_node):
    optimize_common_structs(struct_node)
    optimize_numbered_arrays(struct_node)


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
    optimize_struct_node(struct_node)
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
        desc_str += '"%s", ' % struct_node.name
        if struct_node.typ in name_only_field_types:
            indent_str = ""
        else:
            if struct_node.typ in string_field_types:
                desc_str += "SIZE=%s" % struct_node.size
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

                desc_str += "*%s" % (enum_name)
                indent_str = ""

                #indent_str = ' ' * (4 * (indent + 1))
            elif struct_node.typ in bool_field_types:
                desc_str += '\n'
                i = 0
                j = last_val = -1
                for bit in struct_node:
                    j += 1
                    #if bit.name in ("_%s" % j, "_%s" % (j + 1),
                    #                "bit_%s" % j, "bit_%s" % (j + 1)):
                    #    continue

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
            elif struct_node.typ in ("BlockDef", "reflexive",
                                     "Struct", "QStruct"):

                if len(struct_node):
                    desc_str += '\n'
                elif struct_node.include:
                    desc_str += "INCLUDE=%s, " % struct_node.include
                    indent_str = ""

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
    elif not struct_node.visible:
        desc_str += "VISIBLE=False, "

    desc_str = desc_str.rstrip(", ") + indent_str + ')'

    if struct_node.typ in ("reflexive", "BlockDef"):
        descs_by_name[desc_name] = desc_str
        return desc_name

    return desc_str


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
        new_node.value = eval(xml_attribs.get('value', "0"))

    if new_node.offset is None:
        new_node.offset = new_node.value

    sub_nodes_by_offset = {}
    for xml_subnode in xml_node:
        new_sub_node = parse_xml_node(xml_subnode)
        if new_sub_node is not None:
            sub_nodes_by_offset[new_sub_node.offset] = new_sub_node

    for off in sorted(sub_nodes_by_offset):
        sub_node = sub_nodes_by_offset[off]
        if sub_node.typ == "Pad":
            sub_node.visible = True

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
            pad_node.visible = True
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
        nodes.name = fix_name_identifier(tag_id + (" " * (4 - len(tag_id))))
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
