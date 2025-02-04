#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

'''
Used for extracting tag definitions to a format that can be easily read.
'''
from reclaimer.field_types import Reflexive
from reclaimer.h2.field_types import H2Reflexive
from traceback import format_exc
from supyr_struct.tag import Tag
from supyr_struct.field_types import Union


def find_enums(block, next_blocks):
    typ = block.TYPE
    if "enum" in typ.name.lower():
        next_blocks.append(block)
        return

    if typ.is_array:
        if block.get_desc('TYPE', 'SUB_STRUCT').is_block:
            if len(block) == 0:
                block.append()
            find_enums(block[0], next_blocks)
    elif typ == Union:
        for case in block.CASE_MAP:
            block.set_active(case)
            find_enums(block.u_node, next_blocks)
        block.set_active()
    elif typ.is_container or typ.is_struct:
        for i in range(len(block)):
            if block.get_desc('TYPE', i).is_block:
                if hasattr(block[i], "TYPE"):
                    find_enums(block[i], next_blocks)

    if (hasattr(block, "STEPTREE") and
            block.get_desc('TYPE', 'STEPTREE').is_block):
        find_enums(block.STEPTREE, next_blocks)


def find_next_blocks(block, next_blocks):
    typ = block.TYPE
    if typ in (Reflexive, H2Reflexive):
        block.STEPTREE.append()
        next_blocks.append(block.STEPTREE[-1])
        return

    if typ.is_array:
        if block.get_desc('TYPE', 'SUB_STRUCT').is_block:
            if len(block) == 0:
                block.append()
            find_next_blocks(block[0], next_blocks)
    elif typ == Union:
        for case in block.CASE_MAP:
            block.set_active(case)
            find_next_blocks(block.u_node, next_blocks)
        block.set_active()
    elif typ.is_container or typ.is_struct:
        for i in range(len(block)):
            if block.get_desc('TYPE', i).is_block:
                if hasattr(block[i], "TYPE"):
                    find_next_blocks(block[i], next_blocks)

    if (hasattr(block, "STEPTREE") and
            block.get_desc('TYPE', 'STEPTREE').is_block):
        find_next_blocks(block.STEPTREE, next_blocks)


def print_tag_def(tag_def):
    # make an empty tag to do w/e with
    new_tag = tag_def.build()

    # write the tag definition to a file
    with open("%s_def.txt" % tag_def.def_id, "w") as f:
        tagdata = new_tag
        def_id = tag_def.def_id
        if isinstance(new_tag, Tag):
            tagdata = new_tag.data.tagdata
            blocks = [new_tag.data.blam_header, tagdata]
            f.write("%s (%s)\n\n" % (def_id, tag_def.ext[1:]))
        else:
            blocks = [tagdata]
            f.write("%s\n\n" % def_id)

        f.write("#"*60 + "\n")
        f.write("#" + (" "*20) + "STRUCTURES\n")
        f.write("\n\n")

        # loop over each block until they are exhausted
        while blocks:
            new_blocks = []

            for block in blocks:
                if not hasattr(block, "NAME"):
                    continue

                f.write("\n")
                f.write("\n")
                f.write("#"*60 + "\n")
                f.write("#" + (" "*20) + block.NAME + "\n")
                f.write("\n")
                f.write(block.pprint(show=("name", "type", "offset",
                                           "flags", "size")).\
                        replace("[", "{").replace("]", "}"))

                find_next_blocks(block, new_blocks)

            blocks = new_blocks

        f.write("\n\n")
        f.write("#"*60 + "\n")
        f.write("#" + (" "*20) + "ENUMERATORS\n")
        f.write("\n\n")

        # loop over each block until they are exhausted
        enums = []
        find_enums(tagdata, enums)
        i = j = 0
        enum_strs = []
        enum_strs_map = {}
        enum_names = []
        for enum in enums:
            name = ""
            b = enum
            while hasattr(b, 'NAME') and hasattr(b, 'parent'):
                if not (b.TYPE.is_array or b.NAME in ("tagdata", def_id) or
                        b.TYPE in (Reflexive, H2Reflexive)):
                    name = "%s.%s" % (b.NAME, name)
                b = b.parent
            name = name.rstrip(".")

            if not name:
                name = "UNNAMED_ENUM_%s" % i
                i += 1

            desc = enum.desc
            enum_str = "%s" + ("%s {\n" % enum.TYPE.name)
            for k in range(enum.ENTRIES):
                enum_str += "    %s = %s,\n" % (desc[k]['NAME'],
                                                desc[k]['VALUE'])
            enum_str += "    }\n\n"

            if enum_str in enum_strs_map:
                enum_names[enum_strs_map[enum_str]].append(name)
                continue

            enum_strs_map[enum_str] = j
            enum_strs.append(enum_str)
            enum_names.append([name])
            j += 1

        for i in range(len(enum_names)):
            name = ""
            names = enum_names[i]
            for j in range(len(names)):
                name = "%s = %s" % (names[j], name)
            f.write(enum_strs[i] % name)


def load_tag_defs(engine, classes):
    tag_defs = {}
    if "****" in classes:
        exec("from reclaimer.%s.defs import __all__ as classes" % engine)

    for cls in classes:
        cls_id = cls.replace("!", "_").replace("#", "_").replace("+", "_").\
                 replace(" ", '')
        cls_id += " " * (4 - len(cls_id))

        try:
            def_name = cls_id
            if "_meta" in def_name:
                def_name = def_name.replace("_meta", "")

            def_id = "%s_def" % def_name
            exec("from reclaimer.%s.defs.%s import %s" %
                 (engine, def_name, def_id), globals(), locals())
            tag_defs[cls] = locals()[def_id]
        except Exception:
            print("Could not load the %s definition" % cls)
            print(format_exc())

    return tag_defs


def run():
    defs = {}

    #import the tag definition so it can be used for making a blank tag
    while not defs:
        engine = input("Type in the definition set to use.\n"
                       "Valid values are hek, os_hek, os_v3_hek, and os_v4_hek.\n"
                       ">>> ")
        engine = engine.strip(" ").lower()
        print()
        classes = input("Type in the four character codes of the tag classes to write.\n"
                        "Use commas to separate each one. Spaces are ignored.\n"
                        "Examples include jpt!, vehi, DeLa, snd!, and bitm.\n"
                        "Type **** if you want to write every available tag class.\n"
                        ">>> ")
        defs = load_tag_defs(engine, [s.strip() for s in classes.split(",")])

    for cls in defs:
        try:
            print_tag_def(defs[cls])
        except Exception:
            print("Could not print the %s definition" % cls)
            print(format_exc())

    input("Finished. Hit enter to exit. . .")

if __name__ == "__main__":
    run()
