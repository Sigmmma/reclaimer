#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from struct import pack, unpack
from types import MethodType

from reclaimer.halo_script.defs.hsc import *

from reclaimer.common_descs import \
     script_types as h1_script_types,\
     script_object_types as h1_script_object_types,\
     script_object_tag_ref_types as h1_script_object_tag_ref_types
from reclaimer.util import float_to_str
from reclaimer.h2.common_descs import script_types as h2_script_types,\
     script_object_types as h2_script_object_types,\
     script_object_tag_ref_types as h2_script_object_tag_ref_types
from reclaimer.stubbs.common_descs import \
    script_types as stubbs_script_types,\
    script_object_types as stubbs_script_object_types,\
    script_object_tag_ref_types as stubbs_script_object_tag_ref_types
from reclaimer.shadowrun_prototype.common_descs import \
    script_types as sr_script_types,\
    script_object_types as sr_script_object_types,\
    script_object_tag_ref_types as sr_script_object_tag_ref_types

from supyr_struct.field_types import FieldType

try:
    from reclaimer.enums import _script_built_in_functions_test
except Exception:
    _script_built_in_functions_test = None


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

_script_objects = ("object", "unit", "vehicle", "weapon", "device", "scenery")
SCRIPT_OBJECT_TYPES_TO_SCENARIO_REFLEXIVES = dict((
    ("script", "scripts"), 
    ("trigger_volume", "trigger_volumes"), 
    ("cutscene_flag", "cutscene_flags"),
    ("cutscene_camera_point", "cutscene_camera_points"), 
    ("cutscene_title", "cutscene_titles"),
    ("cutscene_recording", "recorded_animations"), 
    ("device_group", "device_groups"),
    ("ai", "encounters"),
    ("ai_command_list", "command_lists"),
    ("starting_profile", "player_starting_profiles"), 
    ("conversation", "ai_conversations"),
    *((typ, "object_names") for typ in _script_objects),
    *(("%s_name" % typ, "object_names") for typ in _script_objects),
    ))
del _script_objects


def cast_uint32_to_float(uint32, packer=MethodType(pack, "<I"),
                         unpacker=MethodType(unpack, "<f")):
    return unpacker(packer(uint32))[0]


def cast_uint32_to_sint16(uint32):
    return ((uint32 + 0x8000) % 0x10000) - 0x8000


def cast_uint32_to_sint32(uint32):
    return ((uint32 + 0x80000000) % 0x100000000) - 0x80000000


def get_hsc_node_string(string_data, node, hsc_node_strings_by_type=()):
    # if this is not a script or global, try to get the
    # string from the provided hsc_node_strings_by_type
    #if (not(node.flags & HSC_IS_SCRIPT_OR_GLOBAL) and
    #        node.type in hsc_node_strings_by_type):
    if node.type in hsc_node_strings_by_type:
        hsc_node_strings = hsc_node_strings_by_type[node.type]

        # "ai" script object types(17) use 32 bits of the
        # data field to specify index instead of just 16.
        # TODO: remove hardcoding of 17 as "ai" script object type
        mask = 0xFFffFFff if node.type == 17 else 0xFFff
        if node.data & mask in hsc_node_strings:
            return hsc_node_strings[node.data & mask]

    end = string_data.find("\x00", node.string_offset)
    string = string_data[node.string_offset: end]
    #if _script_built_in_functions_test is not None and node.type == 2:
    #    if node.index_union not in range(len(_script_built_in_functions_test)):
    #        _script_built_in_functions_test.extend(
    #            [None] * (node.index_union + 1 -
    #                      len(_script_built_in_functions_test)))
    #    if _script_built_in_functions_test[node.index_union] is None:
    #        _script_built_in_functions_test[node.index_union] = string

    return string


def get_hsc_data_block(raw_syntax_data=None, engine="halo1"):
    '''
    Accepts a bytes-like object of the script syntax data, and 
    the engine the data is from.
    Returns a block containing the script node header, and all
    nodes following it in an array.
    '''
    block_def = None
    block_def = (
        h1_script_syntax_data_os_def    if "yelo" in engine else
        h1_script_syntax_data_def       if "halo1" in engine else
        h1_script_syntax_data_mcc       if "halo1mcc" in engine else
        stubbs_script_syntax_data_def   if "stubbs" in engine else
        sr_script_syntax_data_def       if "shadowrun" in engine else
        None
        )

    if block_def is None or len(raw_syntax_data) < HSC_HEADER_LEN:
        return

    endianness_force = FieldType.force_little
    if raw_syntax_data[HSC_SIG_OFFSET: HSC_SIG_OFFSET+4] == b"d@t@":
        endianness_force = FieldType.force_big
    elif raw_syntax_data[HSC_SIG_OFFSET: HSC_SIG_OFFSET+4] != b"@t@d":
        raise ValueError("Data stream does not appear to be script syntax data.")

    with endianness_force:
        syntax_data = block_def.build(rawdata=raw_syntax_data)
        node_size = syntax_data.node_size
        node_ct = min(syntax_data.max_nodes, syntax_data.last_node,
                      (len(raw_syntax_data) - HSC_HEADER_LEN) // node_size)

        nodes = syntax_data.nodes
        for i in range(HSC_HEADER_LEN, HSC_HEADER_LEN + node_ct*node_size, node_size):
            nodes.append(rawdata=raw_syntax_data, root_offset=i)

    return syntax_data


def get_h1_scenario_script_object_type_strings(scnr_data, engine="halo1"):
    '''
    Returns a hash of hashes that contain all identifier strings that
    exist in the scenario. The outer layer hash is keyed by the integer
    enum value of the reference type, and the inner hashes are keyed by
    the index a script node would locate them by(i.e. reflexive index).

    NOTE: This function does not currently handle hud_message refs, as it
          does not accept parsed hud_message tag data. Eventually add this.
    '''
    script_strings_by_type = {}
    _, script_object_types = get_script_types(engine)

    biped_node_enum      = script_object_types.index("actor_type")
    encounters_node_enum = script_object_types.index("ai")

    for script_object_type, reflexive_name in \
            SCRIPT_OBJECT_TYPES_TO_SCENARIO_REFLEXIVES.items():
        script_object_type_enum = script_object_types.index(script_object_type)
        names = {}
        script_strings_by_type[script_object_type_enum] = names

        i = 0
        for b in scnr_data[reflexive_name].STEPTREE:
            names[i] = b.name
            i += 1

    i = 0
    script_strings_by_type[biped_node_enum] = names = {}
    for b in scnr_data.bipeds_palette.STEPTREE:
        names[i] = b.name.filepath.split("/")[-1].split("\\")[-1]
        i += 1

    i = 0
    script_strings_by_type[encounters_node_enum] = names = {}
    for enc in scnr_data.encounters.STEPTREE:
        j = 0
        for squad in enc.squads.STEPTREE:
            names[i + (j << 16) + 0x80000000] = "%s/%s" % (enc.name, squad.name)
            j += 1
        i += 1

    return script_strings_by_type


def get_scenario_script_object_type_strings(scnr_data, engine="halo1"):
    # NOTE: update this if shadowrun or stubbs have differences to account for
    return (
        get_h1_scenario_script_object_type_strings(scnr_data, engine)
        )


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
        if node.flags == HSC_IS_GARBAGE_COLLECTABLE:
            index, salt = node.data & 0xFFff, node.data >> 16
            if salt and index < len(nodes):
                # node is parenthese. go deeper
                return get_first_significant_node(
                    nodes[index], nodes, string_data, node, node, True)

        func_name = get_hsc_node_string(string_data, node)
        if ((node.flags & HSC_IS_PRIMITIVE) and
                node.type == 2 and func_name == "begin"):
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


def decompile_node_bytecode(node_index, nodes, string_data,
                            object_types, script_types, indent=1, indent_size=4, 
                            indent_char=" ", return_char="\n", bool_as_int=False, 
                            build_cond=True, **kwargs):
    if node_index < 0 or node_index >= len(nodes):
        return "", False, 0

    hsc_node_strings_by_type = kwargs.get("hsc_node_strings_by_type", ())
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
        node_str = ""

        if node.flags == HSC_IS_GARBAGE_COLLECTABLE:
            start_node = get_first_significant_node(node, nodes, string_data)

            child_node, salt = start_node.data & 0xFFff, start_node.data >> 16
            if salt != 0:
                node_str, newl, ct = decompile_node_bytecode(
                    child_node, nodes, string_data,
                    object_types, script_types, indent + 1, indent_size,
                    indent_char, return_char, bool_as_int, **kwargs)

                if ct > 1 or newl or (node_str[:1]  != "(" and
                                      node_str[-1:] != ")"):
                    # only add a start parenthese so the end can be added
                    # on later when we decide how to pad the list elements
                    node_str = "(" + node_str
                else:
                    # reparse the node at a lesser indent
                    node_str, newl, ct = decompile_node_bytecode(
                        child_node, nodes, string_data,
                        object_types, script_types, indent, indent_size, 
                        indent_char, return_char, bool_as_int, **kwargs)
                    node_str = (" " + node_str) if node_str else ""

        elif node.flags & HSC_IS_GLOBAL:
            node_str = get_hsc_node_string(string_data, node,
                                           hsc_node_strings_by_type)
            if "global_uses" in kwargs and node_str:
                kwargs["global_uses"].add(node_str)

        elif node.flags & HSC_IS_SCRIPT_CALL:
            # is_script_call is set
            args_node, salt = node.data & 0xFFff, node.data >> 16
            node_str = "("
            script_call_node_str, newl, ct = decompile_node_bytecode(
                args_node, nodes, string_data,
                object_types, script_types, indent + 1, indent_size,
                indent_char, return_char, bool_as_int, **kwargs)

            node_str += script_call_node_str

        elif node.flags & HSC_IS_PRIMITIVE:
            # TODO: remove value hardcoding in these node_type checks
            # is_primitive is set
            if node_type in (2, 10):
                # function/script name
                node_str = get_hsc_node_string(string_data, node,
                                               hsc_node_strings_by_type)
                if node_type == 10 and "static_calls" in kwargs and node_str:
                    kwargs["static_calls"].add(node_str)
            elif node_type in range(5):
                # special form/unparsed/passthrough/void type
                pass
            elif node_type == 5:
                # bool
                val = node.data&1
                node_str = str(val) if bool_as_int else ["false", "true"][val]
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
                node_str = '"%s"' % get_hsc_node_string(
                    string_data, node, hsc_node_strings_by_type)

        node_strs.append((node_str, newl))
        node_index, salt = node.next_node & 0xFFff, node.next_node >> 16
        if salt == -1 and node_index == -1:
            break

        i += 1

    node_str_ct = len(node_strs)
    if not node_str_ct:
        return "", False, 0

    string = ""
    indent_str = indent_char * indent_size * indent
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
                node_str = return_char + indent_str + node_str
                has_newlines = True
        elif i > 1:
            # ensure there's a space to separate parameters
            node_str = " " + node_str

        if cap_end:
            if local_newlines:
                node_str += return_char + indent_str
            node_str += ")"

        returned = node_str[-1] == return_char
        string += node_str

    return string, has_newlines, i


def get_script_types(engine="halo1"):
    '''Returns the script types and script object types for this engine.'''
    return (
        (h1_script_types, h1_script_object_types) if "yelo" in engine else
        (h1_script_types, h1_script_object_types) if "halo1" in engine else
        (h2_script_types, h2_script_object_types) if "halo2" in engine else
        (sr_script_types, sr_script_object_types) if "shadowrun" in engine else
        (stubbs_script_types, stubbs_script_object_types)  if "stubbs" in engine else
        ((), ())
        )


def get_script_tag_ref_type_names(engine="halo1"):
    '''
    Returns a list containing the enum name each script node tag
    ref type for this engine.
    '''
    # these are the names of the script object types that are tag references
    return (
        h1_script_object_tag_ref_types  if "yelo" in engine else
        h1_script_object_tag_ref_types  if "halo1" in engine else
        h2_script_object_tag_ref_types  if "halo2" in engine else
        sr_script_object_tag_ref_types  if "shadowrun" in engine else
        stubbs_script_object_tag_ref_types  if "stubbs" in engine else
        ()
        )


def get_script_tag_ref_types(engine="halo1"):
    '''
    Returns a list containing the enum value of each script node tag
    ref type for this engine.
    '''
    # these are the names of the script object types that are tag references
    tag_ref_script_types = get_script_tag_ref_type_names(engine)

    _, script_object_types = get_script_types(engine)
    return [
        script_object_types.index(typ)
        for typ in tag_ref_script_types
        ]


def get_script_syntax_node_tag_refs(syntax_data, engine="halo1"):
    '''Returns a list of all script nodes that are tag references.'''
    tag_ref_type_enums = set(get_script_tag_ref_types(engine))
    tag_ref_nodes = []

    # null all references to tags
    for node in syntax_data.nodes:
        if (node.flags & HSC_IS_SCRIPT_OR_GLOBAL or
            node.type not in tag_ref_type_enums):
            # not a tag index ref
            continue

        tag_ref_nodes.append(node)

    return tag_ref_nodes


def clean_script_syntax_nodes(syntax_data, engine="halo1"):
    '''
    Scans through script nodes and nulls tag references.
    This is necessary for script syntax data in tag form.
    '''
    # null all references to tags
    for node in get_script_syntax_node_tag_refs(syntax_data, engine):
        # null the reference
        node.data = 0xFFffFFff


def hsc_bytecode_to_string(syntax_data, string_data, block_index,
                           script_blocks, global_blocks, block_type,
                           engine="halo1", indent_size=4, minify=False, 
                           indent_char=" ", return_char="\n", **kwargs):
    is_global = (block_type == "global")
    is_script = (block_type == "script")
    script_types, object_types = get_script_types(engine)
    if not((is_global or is_script) and script_types and object_types):
        return ""

    # figure out which reflexive and type enums to use
    blocks      = script_blocks if is_script else global_blocks
    typ_names   = script_types  if is_script else object_types

    block   = blocks[block_index]
    typ     = block.type.data

    # invalid script/global type
    if typ not in range(len(typ_names)):
        return ""

    if minify:
        indent_size = 0
        indent_char = ""
        return_char = ""

    # get the index of the node in the nodes array
    node_index  = (
        block.root_expression_index if is_script else
        block.initialization_expression_index
        ) & 0xFFff

    # figure out the type of the node
    node_type = typ_names[typ]

    # scripts also have a return type(except the 3 specified below)
    if is_script and node_type not in ("dormant", "startup", "continuous"):
        return_typ    = block.return_type.data
        if return_typ not in range(len(object_types)):
            # invalid return type
            return ""

        node_type += " " + object_types[return_typ]

    # generate the suffix of the header, which includes the function/global
    # name, and any parameters the function accepts(params are MCC only)
    suffix = block.name
    if hasattr(block, "parameters") and block.parameters.STEPTREE:
        for param in block.parameters.STEPTREE:
            return_typ    = param.return_type.data
            if return_typ not in range(len(object_types)):
                # invalid return type
                print("Invalid return type '%s' in script '%s'" %
                    (param.name, block.name)
                    )
                return ""
            suffix += "%s(%s %s)" % (
                indent_char, object_types[return_typ], param.name
                )
        suffix = "(%s)" % suffix

    head   = "%s %s %s" % (block_type, node_type, suffix)
    body, _, __ = decompile_node_bytecode(
        node_index, syntax_data.nodes, string_data,
        object_types=object_types, script_types=script_types,
        indent_size=indent_size, indent_char=indent_char, 
        return_char=return_char, **kwargs
        )

    if is_script:
        body = "".join((return_char, " " * indent_size, body, return_char))
    else:
        # add a space to separate global definition from its value
        body = " " + body

    return "(%s%s)" % (head, body)
