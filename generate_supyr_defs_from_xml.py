import os
from collections import OrderedDict
from copy import deepcopy
from datetime import datetime
from xml.etree.ElementTree import ElementTree
from traceback import format_exc
from string import ascii_letters
from supyr_struct.defs.util import str_to_identifier


VALID_MODULE_NAME_CHARS = ascii_letters + '_' + '0123456789'


# Need to fix bug with reflexives sometimes sharing names with earlier fields
#     Occurs in lswd, chgd, and sbsp


engine_specific_field_types = set((
    "string_id", "rawdata_ref", "dependency", "reflexive"
    ))

name_only_field_types = set((
    "string_id", "rawdata_ref", "dependency", "dependency_uint32",
    "float_rad", "yp_float_rad", "ypr_float_rad",
    "float_deg", "yp_float_deg", "ypr_float_deg",
    "color_argb_float", "color_argb_uint32",
    "color_rgb_float",  "color_xrgb_uint32",
    "Float", "from_to_rad", "ascii_str32",
    "SInt8", "SInt16", "SInt32", "UInt8", "UInt16", "UInt32",
    ))

do_not_indent_field_types = set(name_only_field_types)
do_not_indent_field_types.add("reflexive")
do_not_indent_field_types.add("BytesRaw")
do_not_indent_field_types.add("StrLatin1")
do_not_indent_field_types.add("StrUTF16")
do_not_indent_field_types.add("Pad")
do_not_indent_field_types.add("string_id")

string_field_types = set((
    "BytesRaw", "StrLatin1", "StrUTF16",
    ))

enum_field_types = set((
    "SEnum8", "SEnum16", "SEnum32", "UEnum8", "UEnum16", "UEnum32"
    ))

bool_field_types = set((
    "Bool8", "Bool16", "Bool32"
    ))


array_allowed_fields = set((
    "color_argb_float", "color_argb_uint32",
    "color_rgb_float",  "color_xrgb_uint32",
    "Float", "float_rad", "string_id",
    "SInt8", "SInt16", "SInt32",
    "UInt8", "UInt16", "UInt32", "Pad",
    "ascii_str32"
    ))


field_sizes = {
    "reflexive": 12, "rawdata_ref": 20, "dependency": 16,
    "color_argb_float": 16, "color_argb_uint32": 4,
    "color_rgb_float": 12,  "color_xrgb_uint32": 4,
    "Float": 4, "float_rad": 4, "string_id": 4,
    "SInt8":  1, "SInt16":  2, "SInt32":  4,
    "UInt8":  1, "UInt16":  2, "UInt32":  4,
    "SEnum8": 1, "SEnum16": 2, "SEnum32": 4,
    "UEnum8": 1, "UEnum16": 2, "UEnum32": 4,
    "Bool8":  1, "Bool16":  2, "Bool32":  4,
    "ascii_str32": 32, "dependency_uint32": 4,

    # special values
    "bit": 1, "opt": 1, "Pad": 4
    }

type_name_map = {
    "raw": "BytesRaw", "undefined": "Pad", "array": "Array",
    "reflexive": "reflexive", "dataref": "rawdata_ref",
    "tagref": "dependency", "tagref_uint32": "dependency_uint32",
    "float32": "Float", "float": "Float", "degree": "float_rad",
    "int8": "SInt8",  "int16": "SInt16",  "int32": "SInt32",
    "uint8": "UInt8", "uint16": "UInt16", "uint32": "UInt32",
    "enum8": "SEnum8",  "enum16": "SEnum16",  "enum32": "SEnum32",
    "uenum8": "UEnum8", "uenum16": "UEnum16", "uenum32": "UEnum32",
    "bitfield8": "Bool8", "bitfield16": "Bool16", "bitfield32": "Bool32",
    "ascii": "StrLatin1", "utf16": "StrUTF16",
    "stringid": "string_id",
    "colorf": "color_argb_float", "color32": "color_argb_uint32",
    "colorfnoalpha": "color_rgb_float", "color24": "color_xrgb_uint32",

    "shader": "UInt32", "string": "UInt32", "uniclist": "UInt32",

    # special values
    "bit": "bit", "option": "opt", "plugin": "BlockDef"
    }

ignored_names = set((
    "comment", "revision"
    ))

name_fix_replacements = dict(
    index="idx", count="size", insert="ins", parent="ancestor"
    )

prefix_chains = [
    (("min_", "minimum_"), ("max_", "maximum_",)),
    (("eular_angle_x_", "x_", ), ("y_", ), ("z_", )),
    ]

suffix_chains = [
    (("_min", "_minimum"), ("_max", "_maximum",)),
    (("_u", "u"), ("_v", "v"), ("_w", "w")),
    (("_y", "y", "yaw"), ("_p", "p", "pitch"), ("_r", "r", "roll")),
    (("_x", "x"), ("_y", "y"), ("_z", "z"), ("_w", "w")),
    (("_i", "i"), ("_j", "j"), ("_k", "k"), ("_w", "w")),
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

    desc_kw = ()


def fix_name_identifier(name):
    orig_name = name
    name = name.replace("don't", "dont")
    if name[: 1] == "-" and name[1: 2] != "-":
        name = "neg_" + name[1: ]

    if name[: 1] in "0123456789":
        name = "_" + name

    name = str_to_identifier(name)
    return name_fix_replacements.get(name, name)


def replace_struct_node_section(struct_node, start, count, typ, size, name,
                                report_optimize=True, desc_kw=None):
    new_node = StructNode()
    new_node.typ = typ
    new_node.size = size
    new_node.name = fix_name_identifier(name).rstrip("_")
    new_node.desc_kw = desc_kw
    new_node.offset = struct_node[start].offset
    new_node.visible = struct_node[start].visible
    if report_optimize:
        print("    Replacing %s '%s' with '%s'" %
              (count, struct_node[start].typ, typ))
    struct_node[start: start + count] = [new_node]


def optimize_common_structs(struct_node, engine_name, report_optimize):
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
        new_desc_kw = OrderedDict()
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
        elif field_names_str == "eular_angle_x_y_z":
            if not node_base_name: node_base_name = "rotation"

            if field_typ == "float_rad":
                new_typ = "ypr_float_rad"
                typ_check = "float_rad"
            else:
                optimize = False
        elif field_names_str == "x_y_z":
            if not node_base_name: node_base_name = "position"

            if field_typ == "Float":
                new_desc_kw["INCLUDE"] = "xyz_float"
                new_size = 12
            else:
                optimize = False
        elif field_names_str == "x_y":
            if not node_base_name: node_base_name = "position"

            if field_typ == "Float":
                new_desc_kw["INCLUDE"] = "xy_float"
                new_size = 8
            else:
                optimize = False
        elif field_names_str in ("i_j_k_w", "x_y_z_w"):
            if not node_base_name: node_base_name = "rotation"

            if field_typ == "Float":
                new_desc_kw["INCLUDE"] = "ijkw_float"
                new_size = 16
            elif field_typ == "SInt16":
                new_desc_kw["INCLUDE"] = "ijkw_sint16"
                typ_check = "SInt16"
                new_size = 8
            else:
                optimize = False
        elif field_names_str == "i_j_k":
            if not node_base_name: node_base_name = "rotation"

            if field_typ == "Float":
                new_desc_kw["INCLUDE"] = "ijk_float"
                new_size = 12
            elif field_typ == "float_rad":
                new_typ = "ypr_float_rad"
                typ_check = "float_rad"
            elif field_typ == "SInt16":
                new_desc_kw["INCLUDE"] = "ijk_sint16"
                typ_check = "SInt16"
                new_size = 6
            else:
                optimize = False
        elif field_names_str == "i_j":
            if not node_base_name: node_base_name = "angle"

            new_size = 8
            if field_typ == "Float":
                new_desc_kw["INCLUDE"] = "ij_float"
            elif field_typ == "float_rad":
                new_typ = "yp_float_rad"
                typ_check = "float_rad"
            elif field_typ == "SInt16":
                new_desc_kw["INCLUDE"] = "ij_sint16"
                typ_check = "SInt16"
                new_size = 4
            else:
                optimize = False
        elif field_names_str == "u_v":
            if not node_base_name: node_base_name = "tex position"

            if field_typ == "Float":
                new_desc_kw["INCLUDE"] = "uv_float"
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
                new_desc_kw["INCLUDE"] = "from_to"
            elif field_typ == "float_rad":
                new_typ = "from_to_rad"
                typ_check = "float_rad"
            elif field_typ[1: ] in ("Int32", "Int16", "Int8"):
                new_desc_kw["INCLUDE"] = "from_to_" + field_typ.lower()
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
                                        new_size, node_base_name, report_optimize,
                                        new_desc_kw)

        start += 1


def optimize_numbered_arrays(struct_node, engine_name, report_optimize):
    if (struct_node.typ in bool_field_types or
        struct_node.typ in enum_field_types):
        return

    start = 0
    while start < len(struct_node):
        base_field_num = field_num = field_num_index = -1
        base_field_name = field_name = first_field_name = ""
        base_field_typ = ""
        field_ct = 0
        while start + field_ct < len(struct_node):
            field = struct_node[start + field_ct]
            if field.typ not in array_allowed_fields:
                break

            name = field.name.lower()
            name_pieces = field.name.split("_")
            if field_ct == 0:
                while field_num_index != len(name_pieces):
                    try:
                        int(name_pieces[field_num_index])
                        break
                    except Exception:
                        field_num_index += 1

            if field_num_index == len(name_pieces):
                # handle cases where the fields are the same name
                if not first_field_name:
                    first_field_name = base_field_name = name
                    base_field_typ = field.typ

                if first_field_name == name and base_field_typ == field.typ:
                    field_ct += 1
                else:
                    break
                continue

            try:
                field_num = int(name_pieces.pop(field_num_index))
                field_name = "_".join(s for s in name_pieces)
                if not field_name:
                    pass
                elif field_num_index == 0:
                    field_name = "_" + field_name
                elif field_num_index == -1:
                    field_name = field_name + "_"

                if field_ct == 0:
                    base_field_num = field_num
                    base_field_name = field_name
                    base_field_typ = field.typ

                if (field_num  != base_field_num + field_ct or
                    field.typ  != base_field_typ or
                    field_name != base_field_name):
                    break
            except:
                break

            field_ct += 1

        base_field_name = base_field_name.strip("_")
        if field_ct > 3 and base_field_typ in array_allowed_fields:
            new_desc_kw = OrderedDict()
            sub_struct_string = '%s("%s")' % (base_field_typ, base_field_name)
            if base_field_typ in engine_specific_field_types:
                sub_struct_string = "%s_%s" % (engine_name, sub_struct_string)

            new_desc_kw.update(SIZE=field_ct, SUB_STRUCT=sub_struct_string)
            replace_struct_node_section(struct_node, start, field_ct, "Array",
                                        field_ct, base_field_name + "_array",
                                        report_optimize, new_desc_kw)

        start += 1


def optimize_struct_node(struct_node, engine_name, report_optimize):
    optimize_common_structs(struct_node, engine_name, report_optimize)
    optimize_numbered_arrays(struct_node, engine_name, report_optimize)


def struct_node_to_supyr_desc(struct_node, descs_by_name,
                              enum_bool_names_by_desc,
                              shared_enum_bool_names_by_desc,
                              engine_name, parent_name="", indent=0,
                              report_optimize=True):
    optimize_struct_node(struct_node, engine_name, report_optimize)

    added_names = dict()
    add_num_to = set()
    for sub_node in struct_node:
        # take care of fields with the same name
        added_names[sub_node.name] = added_names.get(
            sub_node.name, 0) + 1
        if added_names[sub_node.name] > 1:
            add_num_to.add(sub_node.name)
            sub_node.name += "_%s" % (added_names[sub_node.name] - 1)

    if add_num_to:
        for sub_node in struct_node:
            if sub_node.name not in add_num_to:
                continue
            added = 0
            while "%s_%s" % (sub_node.name, added) in add_num_to:
                added += 1
            sub_node.name = "%s_%s" % (sub_node.name, added)


    desc_name = struct_node_name = struct_node.name
    if struct_node.typ == "reflexive":
        if desc_name.endswith("s"):
            desc_name = struct_node_name = desc_name[: -1]
        if parent_name:
            desc_name = "%s_%s" % (parent_name, desc_name)

    if struct_node.typ == "BlockDef":
        indent = 1

    indent_str = ' ' * (4 * indent)
    if struct_node.typ in ("reflexive", "BlockDef"):
        desc_str = 'Struct('
    else:
        if struct_node.typ in engine_specific_field_types:
            desc_str = "%s%s_%s(" % (indent_str, engine_name, struct_node.typ)
        else:
            desc_str = '%s%s(' % (indent_str, struct_node.typ)

    if struct_node.typ == "Pad":
        desc_str += str(struct_node.size)
        indent_str = ""
    else:
        if struct_node.typ == "BlockDef":
            desc_str += '"tagdata", '
        else:
            desc_str += '"%s", ' % struct_node_name

        if struct_node.typ in name_only_field_types:
            indent_str = ""
        else:
            if struct_node.typ in string_field_types:
                desc_str += "SIZE=%s, " % struct_node.size
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
                if enum_str in enum_bool_names_by_desc:
                    enum_name = enum_bool_names_by_desc[enum_str]
                elif enum_str in shared_enum_bool_names_by_desc:
                    enum_name = shared_enum_bool_names_by_desc[enum_str]
                else:
                    enum_bool_names_by_desc[enum_str] = enum_name

                desc_str += "*%s, " % enum_name
                indent_str = ""

            elif struct_node.typ in bool_field_types:
                has_incremental_flags = True
                base_flag_num = flag_num = -1
                base_flag_name = flag_name = ""
                for bit in struct_node:
                    name_pieces = bit.name.split("_")
                    try:
                        flag_num = int(name_pieces[-1])
                        flag_name = "_".join(s for s in name_pieces[: -1])
                        if flag_name:
                            flag_name += "_"

                        if bit.offset == 0:
                            base_flag_num = flag_num
                            base_flag_name = flag_name

                        if (flag_num != base_flag_num + bit.offset or
                            flag_name != base_flag_name):
                            has_incremental_flags = False
                            break
                    except Exception:
                        has_incremental_flags = False
                        break

                if has_incremental_flags:
                    bits = len(struct_node)
                    if base_flag_name == "":
                        base_name = struct_node.name
                        if base_name.endswith("s"):
                            base_name = base_name[: -1]

                        bools_str = 'tuple("%s_%%s" %% i for i in range(%s))' % (
                            base_name, bits)
                        bools_name = "%s_bits" % desc_name
                        if (bools_str not in enum_bool_names_by_desc and
                            bools_str not in shared_enum_bool_names_by_desc):
                            enum_bool_names_by_desc[bools_str] = bools_name
                    elif base_flag_name == "bit_":
                        bools_str = 'tuple("bit_%%s" %% i for i in range(%s))' % bits
                        bools_name = "unknown_flags_%s" % bits
                        if (bools_str not in enum_bool_names_by_desc and
                            bools_str not in shared_enum_bool_names_by_desc):
                            enum_bool_names_by_desc[bools_str] = bools_name
                    elif base_flag_num == 0:
                        bools_name = '("%s%%s" %% i for i in range(%s))' % (
                            base_flag_name, bits)
                    else:
                        bools_name = '("%s%%s" %% i for i in range(%s, %s))' % (
                            base_flag_name, base_flag_num, base_flag_num + bits)

                    desc_str += "*%s, " % bools_name
                    indent_str = ""
                else:
                    desc_str += '\n'
                    i = 0
                    j = last_val = -1
                    for bit in struct_node:
                        j += 1
                        name_parts = bit.name.split("_")
                        if len(name_parts) == 2 and name_parts[0] == "bit":
                            try:
                                int(name_parts[1])
                                continue
                            except Exception:
                                pass

                        if bit.value == i or (bit.value - last_val == 1):
                            desc_str += '%s%s"%s",\n' % (
                                indent_str, indent_str, bit.name)
                        else:
                            desc_str += '%s%s("%s", 1 << %s),\n' % (
                                indent_str, indent_str,
                                bit.name, bit.value)
                        i += 1
                        last_val = bit.value
                    indent_str = ' ' * (4 * (indent + 1))


            elif struct_node.typ in ("BlockDef", "reflexive",
                                     "Struct", "QStruct", "Array"):

                if len(struct_node):
                    desc_str += '\n'
                elif struct_node.desc_kw:
                    for k, v in struct_node.desc_kw.items():
                        desc_str += "%s=%s, " % (k, v)
                    indent_str = ""

                for field in struct_node:
                    subdesc_str = struct_node_to_supyr_desc(
                        field, descs_by_name, enum_bool_names_by_desc,
                        shared_enum_bool_names_by_desc, engine_name,
                        desc_name, 1, report_optimize)

                    if field.typ == "reflexive":
                        desc_str += '    %s_reflexive("%s", %s)' % (
                            engine_name, field.name, subdesc_str)
                    else:
                        desc_str += subdesc_str

                    desc_str += ",\n"

        if not struct_node.visible:
            add_newline = desc_str.endswith("\n")
            desc_str += indent_str + "VISIBLE=False,"
            if add_newline:
                desc_str += "\n"


    if struct_node.typ in ("reflexive", "BlockDef"):
        desc_str += indent_str
        if struct_node.typ == "BlockDef":
            desc_name += "_meta_def"

        desc_str += 'ENDIAN=">", SIZE=%s\n' % struct_node.size

    desc_str = desc_str.rstrip(", ") + indent_str + ')'

    if struct_node.typ in ("reflexive", "BlockDef"):
        descs_by_name[desc_name] = desc_str
        return desc_name

    return desc_str


def parse_xml_node(xml_node, version_infos=None):
    xml_tag = xml_node.tag.lower()
    if version_infos is None:
        version_infos = []

    if xml_tag == "revisions":
        for xml_subnode in xml_node:
            xml_attribs = {key.lower(): xml_subnode.attrib[key]
                           for key in xml_subnode.attrib}
            author = xml_attribs.get('author', "unspecified")
            version = xml_attribs.get('version', "1")
            comment = ""
            for comment in xml_subnode.itertext(): break
            version_infos.append("revision: %s\t\tauthor: %s" % (version, author))
            version_infos.append("\t%s" % comment)

        version_infos.append("revision: %s\t\tauthor: Moses_of_Egypt" % (int(version) + 1, ))
        version_infos.append("\tCleaned up and converted to SuPyr definition")
        return None
    elif xml_tag in ignored_names:
        return None

    new_node = StructNode()
    xml_attribs = {key.lower(): xml_node.attrib[key]
                   for key in xml_node.attrib}
    xml_tag = xml_tag.replace("colour", "color")

    new_node.name = fix_name_identifier(
        xml_attribs.get('name', "unnamed").lower()).rstrip("_")
    new_node.offset = eval(xml_attribs.get('offset', "None"))
    new_node.visible = eval(xml_attribs.get('visible', "true").capitalize())

    if xml_tag == "tagref" and not eval(xml_attribs.get(
            'withclass', "true").capitalize()):
        xml_tag = "tagref_uint32"
        new_node.visible = False
    elif xml_tag.startswith("colorf") and xml_attribs.get(
            'format', "rgb") == "rgb":
        xml_tag = "colorfnoalpha"


    if xml_tag in type_name_map:
        new_node.typ = type_name_map[xml_tag]
    else:
        raise TypeError("Unknown field type '%s'" % xml_node.tag)

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

    if new_node.size == 32 and xml_tag == "ascii":
        new_node.typ = "ascii_str32"

    if "index" in xml_attribs:
        new_node.value = eval(xml_attribs['index'])
    else:
        new_node.value = eval(xml_attribs.get('value', "0"))

    if new_node.offset is None:
        new_node.offset = new_node.value

    sub_nodes_by_offset = {}
    for xml_subnode in xml_node:
        new_sub_node = parse_xml_node(xml_subnode, version_infos)
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

            if pad_node.size < 0:
                raise ValueError(
                    ("Negative padding size in '%s' at field "
                     "'%s' of type '%s' at offset '%s'") %
                    (new_node.name, sub_node.name,
                     sub_node.typ, sub_node.offset))

        new_node.append(sub_node)
        last_off = off + sub_node_size
        last_node = sub_node

    for sub_node in new_node:
        if sub_node.typ == "Pad" and not sub_node.visible:
            sub_node.typ = "BytesRaw"

    return new_node


def parse_xml(xml_path, version_infos):
    try:
        xml_root = ElementTree().parse(xml_path)
        tag_id = os.path.splitext(os.path.basename(xml_path))[0].strip(".")
        nodes = parse_xml_node(xml_root, version_infos)
        nodes.name = fix_name_identifier(tag_id + ("_" * (4 - len(tag_id))))
    except:
        print(format_exc())
        nodes = None

    return nodes


timestamp = datetime.now().strftime("%Y/%m/%d  %H:%M")
for _, dirs, __ in os.walk("xml/"):
    tag_def_dirs = dict.fromkeys(dirs)
    for tag_def_dir in tag_def_dirs:
        for _, __, files in os.walk(os.path.join("xml", tag_def_dir)):
            tag_def_dirs[tag_def_dir] = tuple(f[: -4] for f in files if
                                              f.lower().endswith(".xml"))
    break


for tag_def_dir in sorted(tag_def_dirs):

    # TODO: Make this more versatile
    tag_engine_cls_name = tag_def_dir.upper() + "Tag"

    defs_dir = os.path.join(tag_def_dir, "defs")
    os.makedirs(defs_dir, exist_ok=True)

    common_descs_filepath = os.path.join(tag_def_dir, "common_descs.py")
    enum_descs_filepath = os.path.join(tag_def_dir, "enums.py")
    if not os.path.exists(common_descs_filepath):
        with open(common_descs_filepath, "w+") as pyf:
            pyf.write('''from reclaimer.common_descs import *\n''')

    # make the all import in the __init__
    with open(os.path.join(defs_dir, "__init__.py"), "w+") as pyf:
        pyf.write('__all__ = (')
        i = 0
        for fname in sorted(tag_def_dirs[tag_def_dir]):
            if i % 8 == 0:
                pyf.write('\n    ')
            module_name = "".join(c if c in VALID_MODULE_NAME_CHARS
                                  else "_" for c in fname)
            module_name += "_" * ((4 - (len(module_name) % 4)) % 4)
            pyf.write('"%s", ' % module_name)
            i += 1
        pyf.write('\n    )\n')


    all_enum_bool_names_by_desc = {}
    shared_enum_bool_names_by_desc = {}
    all_version_infos = {}
    all_tag_struct_nodes = {}

    # convert all xml's into struct node trees
    print("Parsing XML's...")
    for fname in tag_def_dirs[tag_def_dir]:
        xml_path = os.path.join("xml", tag_def_dir, fname + ".xml")
        version_infos = []
        tag_struct_nodes = parse_xml(xml_path, version_infos)
        if tag_struct_nodes is None:
            print('Could not parse: %s' % xml_path)
        else:
            all_version_infos[fname] = version_infos
            all_tag_struct_nodes[fname] = tag_struct_nodes


    print("Collecting shared enums...")
    # for the first pass, we collect all shared enums
    for fname in sorted(all_tag_struct_nodes):
        descs_by_name = OrderedDict()
        enum_bool_names_by_desc = {}
        struct_node_to_supyr_desc(deepcopy(all_tag_struct_nodes[fname]),
                                  descs_by_name, enum_bool_names_by_desc,
                                  shared_enum_bool_names_by_desc,
                                  tag_def_dir, report_optimize=False)
        for desc_str, desc_name in enum_bool_names_by_desc.items():
            if desc_str in all_enum_bool_names_by_desc:
                shared_enum_bool_names_by_desc[desc_str] = desc_name

            all_enum_bool_names_by_desc[desc_str] = desc_name


    # write out the shared enums
    with open(enum_descs_filepath, "w+") as pyf:
        pyf.write('''from reclaimer.enums import *\n''')
        shared_enum_bool_descs_by_name = {
            shared_enum_bool_names_by_desc[desc]: desc for
            desc in shared_enum_bool_names_by_desc}
        for desc_name in sorted(shared_enum_bool_descs_by_name):
            desc_str = shared_enum_bool_descs_by_name[desc_name]
            pyf.write("\n%s = %s\n" % (desc_name, desc_str.strip(",")))


    print("Writing definitions...")
    # on the second pass, we actually write the definitions
    for tag_cls in sorted(all_tag_struct_nodes):
        print(tag_cls)
        version_infos = all_version_infos[tag_cls]
        tag_struct_nodes = all_tag_struct_nodes[tag_cls]

        descs_by_name = OrderedDict()
        enum_bool_names_by_desc = {}
        struct_node_to_supyr_desc(tag_struct_nodes, descs_by_name,
                                  enum_bool_names_by_desc,
                                  shared_enum_bool_names_by_desc,
                                  tag_def_dir, report_optimize=True)

        module_name = "".join(c if c in VALID_MODULE_NAME_CHARS
                              else "_" for c in tag_cls)
        module_name += "_" * ((4 - (len(module_name) % 4)) % 4)
        with open(os.path.join(defs_dir, module_name) + ".py", "w+") as pyf:
            pyf.write("############# Credits and version info #############\n"
                      "# Definition generated from Assembly XML tag def\n"
                      "#\t Date generated: %s\n#\n" % timestamp)

            for version_info_str in version_infos:
                pyf.write("# %s\n" % version_info_str)

            pyf.write("#\n"
                      "####################################################\n")

            pyf.write('''
from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef''')
            enum_bool_descs_by_name = {enum_bool_names_by_desc[desc]: desc for
                                       desc in enum_bool_names_by_desc}

            for desc_name in sorted(enum_bool_descs_by_name):
                pyf.write("\n\n")
                desc_str = enum_bool_descs_by_name[desc_name]
                pyf.write("%s = %s" % (desc_name, desc_str.strip(",")))

            for desc_name in descs_by_name:
                pyf.write("\n\n\n")
                desc_str = descs_by_name[desc_name]
                if desc_name == "%s_meta_def" % module_name:
                    desc_name = "%s_body" % module_name
                pyf.write("%s = %s" % (desc_name, desc_str.strip(",")))


            pyf.write('\n\n\ndef get():\n    return %s_def' % module_name)

            if "_" in tag_cls:
                print("    MUST SET THIS TAG CLASS STRING MANUALLY")
                pyf.write("\n\n#  REMINDER: Set this tag class string manually.")

            pyf.write('''\n
%s_def = TagDef("%s",
    %s_blam_header('%s'),
    %s_body,

    ext=".%%s" %% %s_tag_class_fcc_to_ext["%s"], endian=">", tag_cls=%s
    )''' % (module_name, tag_cls, tag_def_dir, tag_cls, module_name,
            tag_def_dir, tag_cls, tag_engine_cls_name))

print("Finished")
