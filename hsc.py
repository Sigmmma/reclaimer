import struct

from reclaimer.field_types import *
from reclaimer.constants import *
from reclaimer.common_descs import ascii_str32,\
     script_types as h1_script_types,\
     script_object_types as h1_script_object_types
from reclaimer.util import float_to_str
from reclaimer.h2.common_descs import script_types as h2_script_types,\
     script_object_types as h2_script_object_types
from supyr_struct.defs.block_def import BlockDef
from supyr_struct.field_types import FieldType


# in a list that begins with the keyed expression, this
# is the number of nodes required before we will indent them.
INDENT_LIST_MIN = {
    "begin": 2, "begin_random": 2, "cond": 2, "if": 3,
    "+": 4, "*": 4, "and": 4, "or": 4, "min": 4, "max": 4,
    "ai_debug_communication_suppress": 4,
    "ai_debug_communication_ignore": 4,
    "ai_debug_communication_focus": 4,
    }

# in a list that begins with the keyed expression, this
# is the node index we will start applying indentation at.
START_INDENTING_AFTER = {
    "begin": 1, "begin_random": 1, "cond": 1, "if": 2,
    "+": 1, "*": 1, "and": 1, "or": 1, "min": 1, "max": 1,
    "ai_debug_communication_suppress": 1,
    "ai_debug_communication_ignore": 1,
    "ai_debug_communication_focus": 1,
    }


h1_script_type = SEnum16("type", *h1_script_types)
h1_return_type = SEnum16("return_type", *h1_script_object_types)


# this is a more complete version of the faster script_node def below
script_node = Struct("script_node",
    UInt16("salt"),
    Union("index_union",
        CASES={
            "constant_type":  SInt16("constant_type"),
            "function_index": SInt16("function_index"),
            "script_index":   SInt16("script_index"),
            }
        ),
    SEnum16("type", *h1_script_object_types),
    Bool16("flags",
        "is_primitive",
        "is_script_call",
        "is_global",
        "is_garbage_collectable",
        ),
    UInt32("next_node"),
    UInt32("string_offset"),
    Union("data",
        CASES={
            "bool":  UInt8("bool"),
            "int16": SInt16("int16"),
            "int32": SInt32("int32"),
            "real":  Float("real"),
            "node":  UInt32("node"),
            }
        ),
    SIZE=20
    )

fast_script_node = QStruct("script_node",
    UInt16("salt"),
    UInt16("index_union"),
    UInt16("type"),
    UInt16("flags"),
    UInt32("next_node"),
    UInt32("string_offset"),
    UInt32("data"),
    SIZE=20
    )

h1_script_syntax_data = Struct("script syntax data header",
    ascii_str32('name', DEFAULT="script node"),
    UInt16("max_nodes", DEFAULT=19001),  # this is 1 more than expected
    UInt16("node_size", DEFAULT=20),
    UInt8("is_valid", DEFAULT=1),
    UInt8("identifier_zero_invalid"),   # zero?
    UInt16("unused"),
    UInt32("sig", DEFAULT="d@t@"),
    UInt16("next_node"),  # zero?
    UInt16("last_node"),
    BytesRaw("next", SIZE=4),
    Pointer32("first"),
    STEPTREE=WhileArray("nodes", SUB_STRUCT=fast_script_node)
    )

h1_script_syntax_data_os = dict(h1_script_syntax_data)
h1_script_syntax_data_os[1] = UInt16("max_nodes", DEFAULT=28501)

h1_script_syntax_data_def    = BlockDef(h1_script_syntax_data)
h1_script_syntax_data_os_def = BlockDef(h1_script_syntax_data_os)


def cast_uint32_to_float(uint32, packer=struct.Struct("<I"),
                         unpacker=struct.Struct("<f")):
    return unpacker.unpack(packer.pack(uint32))[0]


def cast_uint32_to_sint16(uint32):
    if uint32&0x8000:
        return (uint32&0xFFFF)-0x10000
    return uint32&0xFFFF


def cast_uint32_to_sint32(uint32):
    if uint32&0x80000000:
        return uint32 - 0x100000000
    return uint32


def get_string(string_data, start):
    end = string_data.find("\x00", start)
    string = string_data[start: end]
    return string


def get_hsc_data_block(raw_syntax_data=None, engine="halo1"):
    block_def = None
    header_len = 56
    sig_off = 40

    if "yelo" in engine:
        block_def = h1_script_syntax_data_os_def
    elif "halo1" in engine:
        block_def = h1_script_syntax_data_def

    if block_def is None:
        return

    endianness_force = FieldType.force_little
    if raw_syntax_data[sig_off: sig_off+4] == b"d@t@":
        endianness_force = FieldType.force_big

    with endianness_force:
        syntax_data = block_def.build(rawdata=raw_syntax_data)
        node_size = syntax_data.node_size
        node_ct = min(syntax_data.max_nodes, syntax_data.last_node,
                      (len(raw_syntax_data) - header_len) // node_size)

        nodes = syntax_data.nodes
        for i in range(header_len, header_len + node_ct*node_size, node_size):
            nodes.append(rawdata=raw_syntax_data, root_offset=i)

    return syntax_data


def get_node_sibling_count(node, nodes):
    ct = 0
    seen = set()
    while True:
        sib_index, salt = node.next_node & 0xFFff, node.next_node >> 16
        if salt == 0 or sib_index >= len(nodes):
            return ct
        elif sib_index in seen:
            return 0xFFffFFff

        ct += 1
        seen.add(sib_index)
        node = nodes[sib_index]


def get_first_significant_node(node, nodes, string_data, parent=None,
                               last_begin_parenthese=None, started=False):
    if (not started) or get_node_sibling_count(node, nodes) <= 1:
        # node has one or no siblings, meaning it COULD be a begin block
        if node.flags == 8:
            index, salt = node.data & 0xFFff, node.data >> 16
            if salt and index < len(nodes):
                # node is parenthese. go deeper
                return get_first_significant_node(
                    nodes[index], nodes, string_data, node, node, True)

        func_name = get_string(string_data, node.string_offset)
        if (node.flags & 1) and node.type == 2 and func_name == "begin":
            index, salt = node.next_node & 0xFFff, node.next_node >> 16
            if salt and index < len(nodes):
                return get_first_significant_node(
                    nodes[index], nodes, string_data, parent,
                    last_begin_parenthese, True)

    if last_begin_parenthese is not None:
        return last_begin_parenthese
    elif parent is not None:
        return parent
    return node
        

def decompile_node_bytecode(node_index, nodes, script_blocks, string_data,
                            object_types, indent=1, indent_size=4, **kwargs):
    if node_index < 0 or node_index >= len(nodes):
        return "", False, 0

    has_newlines = False
    node_strs = []
    i = 0
    while node_index > 0:
        # collect unparsed strings of all linked nodes
        if node_index == 0xFFff:
            break

        newl = False
        node = nodes[node_index]
        node_type = node.type
        union_i = node.index_union
        node_str = ""
        if node.flags == 8:
            # check if ONLY is_garbage_collectable is set
            start_node = get_first_significant_node(node, nodes, string_data)

            child_node, salt = start_node.data & 0xFFff, start_node.data >> 16
            if salt != 0:
                node_str, newl, ct = decompile_node_bytecode(
                    child_node, nodes, script_blocks, string_data,
                    object_types, indent + 1, indent_size, **kwargs)

                if ct > 1 or newl or (node_str[:1]  != "(" and
                                      node_str[-1:] != ")"):
                    # only add a start parenthese so the end can be added
                    # on later when we decide how to pad the list elements
                    node_str = "(%s" % node_str[1:]
                else:
                    # reparse the node at a lesser indent
                    node_str, newl, ct = decompile_node_bytecode(
                        child_node, nodes, script_blocks, string_data,
                        object_types, indent, indent_size, **kwargs)

        elif node.flags & 4:
            # is_global is set
            node_str = get_string(string_data, node.string_offset)
            if "global_uses" in kwargs:
                kwargs["global_uses"].add(node_str)

        elif node.flags & 2 and union_i >= 0 and union_i < len(script_blocks):
            # is_script_call is set
            block = script_blocks[union_i]
            node_str = "(%s" % block.name
            if "static_calls" in kwargs:
                kwargs["static_calls"].add(block.name)

        elif node.flags & 1:
            # is_primitive is set
            if node_type in (2, 10):
                # function/script name
                node_str = get_string(string_data, node.string_offset)
                if node_type == 10 and "static_calls" in kwargs:
                    kwargs["static_calls"].add(node_str)
            elif node_type in (3, 4):
                # passthrough/void type
                pass
            elif node_type == 5:
                # bool
                node_str = "true" if node.data&1 else "false"
            elif node_type == 6:
                # float
                node_str = float_to_str(cast_uint32_to_float(node.data))
            elif node_type == 7:
                # short
                node_str = str(cast_uint32_to_sint16(node.data))
            elif node_type == 8:
                # long
                node_str = str(cast_uint32_to_sint32(node.data))
            elif node_type < len(object_types):
                # other
                node_str = '"%s"' % get_string(string_data, node.string_offset)

        node_strs.append((node_str, newl))
        node_index, salt = node.next_node & 0xFFff, node.next_node >> 16
        if salt == 0:
            break

        i += 1

    node_str_ct = len(node_strs)
    if not node_str_ct:
        return "", False, 0

    string = ""
    indent_str = " " * indent_size * indent
    returned = False
    i = 0
    first_node = node_strs[0]
    node_indent_min   = INDENT_LIST_MIN.get(first_node[0], 20)
    node_indent_start = START_INDENTING_AFTER.get(first_node[0], 1)

    for node_str, local_newlines in node_strs:
        if not node_str:
            continue

        i += 1
        cap_end   = node_str[0] == "("
        do_indent = (i > node_indent_start and indent_str and
                     node_str_ct >= node_indent_min)
        has_newlines |= local_newlines

        # might need to indent this node's string
        if do_indent:
            if returned:
                node_str = indent_str + node_str
            else:
                node_str = "\n" + indent_str + node_str
                has_newlines = True
        elif i > 1:
            node_str = " " + node_str

        if cap_end:
            if local_newlines:
                node_str += "\n" + indent_str
            node_str += ")"

        returned = node_str[-1] == "\n"
        string += node_str

    if string:
        # always add a space to the beginning.
        # it can be stripped off by whatever we return to
        string = " " + string

    return string, has_newlines, i


def hsc_bytecode_to_string(syntax_data, string_data, block_index,
                           script_blocks, global_blocks, block_type,
                           engine="halo1", indent_size=4, **kwargs):
    if block_type not in ("script", "global"):
        return ""

    if ("halo1" in engine or "yelo" in engine or
        "stubbs" in engine or "shadowrun" in engine):
        script_types = h1_script_types
        object_types = h1_script_object_types
    elif "halo2" in engine:
        script_types = h2_script_types
        object_types = h2_script_object_types
    else:
        return ""

    if block_type == "global":
        block       = global_blocks[block_index]
        script_type = ""
        node_index  = block.initialization_expression_index & 0xFFFF
        main_type   = object_types[block.type.data]
    else:
        block       = script_blocks[block_index]
        script_type = script_types[block.type.data]
        node_index  = block.root_expression_index & 0xFFFF
        main_type   = object_types[block.return_type.data]
        if script_type in ("dormant", "startup", "continuous"):
            # these types wont compile if a return type is specified
            main_type = ""
        else:
            script_type += " "

    if "INVALID" in main_type:
        return ""

    indent_str  = " " * indent_size
    head = "%s %s%s %s" % (block_type, script_type, main_type, block.name)
    body, _, __ = decompile_node_bytecode(
        node_index, syntax_data.nodes, script_blocks, string_data,
        object_types, 1, indent_size, **kwargs)
    if block_type == "global":
        return "(%s%s)" % (head, body)
    return "(%s\n%s%s\n)" % (head, indent_str, body[1:])
