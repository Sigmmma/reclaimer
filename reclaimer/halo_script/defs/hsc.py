#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.field_types import *
from reclaimer.constants import *
from reclaimer.common_descs import DynamicArrayFrame,\
     script_object_types as h1_script_object_types,\
     desc_variant
# NOTE: using this desc_variant override to ensure verify is defaulted on
from reclaimer.util import float_to_str
from reclaimer.h2.common_descs import \
     script_object_types as h2_script_object_types
from reclaimer.stubbs.common_descs import \
    script_object_types as stubbs_script_object_types
from reclaimer.shadowrun_prototype.common_descs import\
    script_object_types as sr_script_object_types


from supyr_struct.defs.block_def import BlockDef
from supyr_struct.defs.tag_def import TagDef


HSC_HEADER_LEN = 56
HSC_STUBBS_64BIT_HEADER_LEN = 64
HSC_NODE_SIZE  = 20
HSC_SIG_OFFSET = 40
HSC_IS_PRIMITIVE   = 1 << 0
HSC_IS_SCRIPT_CALL = 1 << 1
HSC_IS_GLOBAL      = 1 << 2
HSC_IS_GARBAGE_COLLECTABLE = 1 << 3
HSC_IS_PARAMETER   = 1 << 4
HSC_IS_STRIPPED    = 1 << 5
HSC_IS_SCRIPT_OR_GLOBAL = HSC_IS_SCRIPT_CALL | HSC_IS_GLOBAL

script_node_ref = BitStruct("node", 
    SBitInt("idx",  SIZE=16), 
    SBitInt("salt", SIZE=16),
    SIZE=4
    )
script_node_data_union = Union("data",
    CASES={
        "boolean": Struct("bool",  UInt8("data")),
        "short":   Struct("int16", SInt16("data")),
        "long":    Struct("int32", SInt32("data")),
        "real":    Struct("real",  Float("data")),
        "node":    script_node_ref,
        },
    CASE=(lambda parent=None, **kw: (
        "node" if not parent else {
            s: s for s in ("boolean", "short", "long", "real")
            }.get(parent.type.enum_name, "node")
        )),
    SIZE=4
    )

# this is a more complete version of the fast_script_node def below
script_node = Struct("script_node",
    UInt16("salt"),
    Union("index_union",
        CASES={
            "constant_type": Struct("value", SInt16("constant_type")),
            "function_name": Struct("value", SInt16("function_index")),
            "script":        Struct("value", SInt16("script_index")),
            },
        COMMENT="""
For most intents and purposes, this value mirrors the 'type' field"""
        ),
    SEnum16("type"),
    Bool16("flags",
        "is_primitive",
        "is_script_call",
        "is_global",
        "is_garbage_collectable",
        "is_parameter",  # MCC only
        "is_stripped",   # MCC only
        ),
    desc_variant(script_node_ref, NAME="next_node"),
    UInt32("string_offset"),
    script_node_data_union,
    SIZE=20
    )

h1_script_node       = desc_variant(script_node,
    SEnum16("type", *h1_script_object_types)
    )
h2_script_node       = desc_variant(script_node, 
    SEnum16("type", *h2_script_object_types)
    )
stubbs_script_node   = desc_variant(script_node, 
    SEnum16("type", *stubbs_script_object_types)
    )
stubbs_64bit_script_node   = desc_variant(script_node, 
    SEnum16("type", *stubbs_script_object_types),
    desc_variant(script_node_data_union,
        SIZE=8, verify=False
        ),
    SIZE=24, verify=False,
    )
sr_script_node = desc_variant(script_node, 
    SEnum16("type", *sr_script_object_types)
    )

script_syntax_data_header = Struct("header",
    StrLatin1('name', DEFAULT="script node", SIZE=30),
    FlUInt16("total_nodes", DEFAULT=0), # always little endian
    SInt16("max_nodes", DEFAULT=19001),  # this is 1 more than expected
    UInt16("node_size", DEFAULT=20),
    UInt8("is_valid",   DEFAULT=1),
    UInt8("identifier_zero_invalid"),   # zero?
    UInt16("unused"),
    UInt32("sig", DEFAULT="d@t@"),
    UInt16("next_node"),  # always zero?
    UInt16("last_node"),
    BytesRaw("next", SIZE=4),  # seems to be garbage?
    Pointer32("first"),
    SIZE=HSC_HEADER_LEN,
    )
stubbs_64bit_script_syntax_data_header = desc_variant(script_syntax_data_header,
    UInt16("node_size", DEFAULT=24),
    BytesRaw("next", SIZE=8),  # seems to be garbage?
    Pointer64("first"),  # seems to be unset
    SIZE=HSC_STUBBS_64BIT_HEADER_LEN, verify=False,
    )

fast_script_node = QStruct("script_node",
    UInt16("salt"),
    UInt16("index_union"),
    UInt16("type"),
    UInt16("flags"),
    UInt32("next_node"),
    UInt32("string_offset"),
    UInt32("data"),
    SIZE=HSC_NODE_SIZE
    )

fast_stubbs_64bit_script_node = desc_variant(fast_script_node,
    UInt64("data"),
    SIZE=24, verify=False,
    )

h1_script_syntax_data = desc_variant(script_syntax_data_header,
    STEPTREE=WhileArray("nodes", SUB_STRUCT=fast_script_node)
    )
h1_script_syntax_data_os = desc_variant(h1_script_syntax_data,
    SInt16("max_nodes", DEFAULT=28501)
    )
h1_script_syntax_data_mcc = desc_variant(h1_script_syntax_data,
    FlSInt16("total_nodes", DEFAULT=32766), # only set in mcc?
    SInt16("max_nodes", DEFAULT=32767)
    )
stubbs_64bit_script_syntax_data = desc_variant(
    stubbs_64bit_script_syntax_data_header,
    STEPTREE=WhileArray("nodes", SUB_STRUCT=fast_stubbs_64bit_script_node)
    )

h1_script_syntax_data_def           = BlockDef(h1_script_syntax_data)
h1_script_syntax_data_os_def        = BlockDef(h1_script_syntax_data_os)
h1_script_syntax_data_mcc_def       = BlockDef(h1_script_syntax_data_mcc)
stubbs_64bit_script_syntax_data_def = BlockDef(stubbs_64bit_script_syntax_data)
# NOTE: update the stubbs and shadowrun script syntax defs if
#       differences are ever discovered between them and halo.
#       for now, these work perfectly since the max_nodes is
#       the same as halo 1, and these defs are fast(no enums)
stubbs_script_syntax_data_def   = h1_script_syntax_data_def
sr_script_syntax_data_def       = h1_script_syntax_data_def


def _generate_script_syntax_tagdef(
        prefix, script_node_desc, header_desc=script_syntax_data_header
        ):
    def get_script_data_endianness(parent=None, rawdata=None, **kw):
        try:
            rawdata.seek(parent.header_pointer + HSC_SIG_OFFSET)
            sig = bytes(rawdata.read(4))
            return ">" if sig == b'd@t@' else "<"
        except Exception:
            asdf
            pass

    def header_pointer(parent=None, rawdata=None, offset=0, root_offset=0, **kw):
        if parent is None:
            return

        base = offset + root_offset
        ptr  = -1
        try:
            while ptr < base:
                ptr = rawdata.find(b"script node\x00", base)
                if ptr < 0: 
                    break

                rawdata.seek(ptr + HSC_SIG_OFFSET)
                if bytes(rawdata.read(4)) in (b'd@t@', b'@t@d'):
                    break

                base = ptr + 12 # 12 is size of "script node" string
                ptr  = -1

        except Exception:
            ptr = parent.base_pointer

        parent.header_pointer = ptr

    def strings_pointer(parent=None, header_size=header_desc["SIZE"], **kw):
        if parent is None:
            return
        header = parent.header
        parent.strings_pointer = (
            parent.parent.header_pointer + header_size + 
            header.max_nodes * header.node_size
            )

    def get_script_string_data_size(parent=None, **kw):
        try:
            return parent.header.max_nodes * parent.header.node_size
        except Exception:
            return 0

    def get_node_string(parent=None, rawdata=None, **kw):
        if parent is None:
            return

        node    = parent.parent
        node_type           = node.type.enum_name
        flags               = node.flags.data
        data                = node.data
        is_global           = flags & HSC_IS_GLOBAL
        is_script           = flags & HSC_IS_SCRIPT_CALL
        is_primitive        = flags & HSC_IS_PRIMITIVE
        is_script_or_global = is_global or is_script
        is_list             = not is_primitive
        is_unused           = node.salt == 0 or node_type in("special_form", "unparsed")
        prefixes            = []
        string              = None

        if node.next_node.salt != -1 and node.next_node.idx != -1:
            prefixes.append(f"NEXT={node.next_node.idx}")

        if is_unused:
            prefixes = ["UNUSED", *prefixes]
        elif is_list:
            prefixes = [f"FIRST={data.node.idx}", *prefixes]
        else:
            if not is_global and node_type in ("boolean", "real", "short", "long"):
                string = (
                    bool(data.boolean.data&1)   if node_type == "boolean" else
                    data.real.data              if node_type == "real" else
                    data.short.data             if node_type == "short" else
                    data.long.data              if node_type == "long" else
                    None
                    )
            else:
                start  = node.parent.parent.strings_pointer + node.string_offset
                end    = rawdata.find(b"\x00", start)
                try:
                    rawdata.seek(start-1)
                    if rawdata.read(1) == b"\x00" or node.string_offset == 0:
                        string = rawdata.read(max(0, end-start)).decode(encoding="latin-1")
                except Exception:
                    pass

            if string is None:
                node_type, string = "undef", ""

        if is_global or is_script:
            prefixes = ["GLOBAL" if is_global else "SCRIPT", *prefixes]

        if not is_unused and not is_list:
            prefixes.append(f"TYPE={node_type}")

        parent.string = string
        parent.description = '<%s> %s' % (
            " ".join(prefixes),
            "" if string is None else f'"{string}"'
            )

    script_node_desc = desc_variant(script_node_desc,
        STEPTREE=Container("computed",
            Computed("description", COMPUTE_READ=get_node_string, WIDGET_WIDTH=120),
            Computed("string",      WIDGET_WIDTH=120),
            ),
        )
    script_data = Container("script_data",
        desc_variant(header_desc, POINTER="..header_pointer"),
        Computed("strings_pointer", COMPUTE_READ=strings_pointer, WIDGET_WIDTH=20),
        Array("nodes",
            SUB_STRUCT=script_node_desc, SIZE=".header.last_node",
            DYN_NAME_PATH=".computed.description", WIDGET=DynamicArrayFrame
            ),
        )

    return (
        TagDef('%s_%s_scripts' % (prefix, extension),
            Computed("header_pointer",  COMPUTE_READ=header_pointer,  WIDGET_WIDTH=20),
            Switch("script_data",
                CASES={
                    ">": desc_variant(script_data, ENDIAN=">"),
                    "<": desc_variant(script_data, ENDIAN="<"),
                    },
                CASE=get_script_data_endianness, DEFAULT=script_data
                ),
            ext="." + extension
            )
        for extension in ("scenario", "map")
        )

# for loading in binilla for debugging script data issues
def get():
    return (
        *h1_script_syntax_data_tagdefs,
        *h2_script_syntax_data_tagdefs, 
        *stubbs_script_syntax_data_tagdefs,
        *stubbs_64bit_script_syntax_data_tagdefs,
        *sr_script_syntax_data_tagdefs
        )

h1_script_syntax_data_tagdefs           = _generate_script_syntax_tagdef(
    "h1", h1_script_node
    )
h2_script_syntax_data_tagdefs           = _generate_script_syntax_tagdef(
    "h2", h2_script_node
    )
stubbs_script_syntax_data_tagdefs       = _generate_script_syntax_tagdef(
    "stubbs", stubbs_script_node
    )
stubbs_64bit_script_syntax_data_tagdefs = _generate_script_syntax_tagdef(
    "stubbs_64bit", stubbs_64bit_script_node,
    stubbs_64bit_script_syntax_data_header
    )
sr_script_syntax_data_tagdefs           = _generate_script_syntax_tagdef(
    "sr", sr_script_node
    )

del _generate_script_syntax_tagdef  # just for quick generation