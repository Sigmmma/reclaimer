#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from pathlib import Path
from traceback import format_exc

from reclaimer.halo_script.hsc import get_hsc_data_block,\
     hsc_bytecode_to_string

__all__ = ("extract_h1_scripts", )


MAX_SCRIPT_SOURCE_SIZE = 1 << 18


def extract_h1_scripts(tagdata, tag_path, **kw):
    dirpath = Path(kw.get("out_dir", "")).joinpath(
        Path(tag_path).parent, "scripts")

    overwrite = kw.get('overwrite', True)
    hsc_node_strings_by_type = kw.get("hsc_node_strings_by_type", ())

    dirpath.mkdir(exist_ok=True, parents=True)

    engine = kw.get('engine')
    if not engine and 'halo_map' in kw:
        engine = kw['halo_map'].engine

    syntax_data = get_hsc_data_block(tagdata.script_syntax_data.data)
    string_data = tagdata.script_string_data.data.decode("latin-1")
    if not syntax_data or not string_data:
        return "No script data to extract."

    already_sorted = set()
    for typ, arr in (("global", tagdata.globals.STEPTREE),
                     ("script", tagdata.scripts.STEPTREE)):
        filename_base = "%ss" % typ

        header = "; Extracted with Reclaimer\n\n"
        comments = ""
        src_file_i = 0
        global_uses  = {}
        static_calls = {}
        if typ == "global":
            sort_by = global_uses
            try:
                comments += "; scenario names(each sorted alphabetically)\n"
                comments += "\n;   object names:\n"
                for name in sorted(set(obj.name for obj in
                                       tagdata.object_names.STEPTREE)):
                    comments += ";     %s\n" % name

                comments += "\n;   trigger volumes:\n"
                for name in sorted(set(tv.name for tv in
                                       tagdata.trigger_volumes.STEPTREE)):
                    comments += ";     %s\n" % name

                comments += "\n;   device groups:\n"
                for name in sorted(set(dg.name for dg in
                                       tagdata.device_groups.STEPTREE)):
                    comments += ";     %s\n" % name

            except Exception:
                pass
        else:
            sort_by = static_calls

        try:
            sources = {}
            for i in range(len(arr)):
                # assemble source code for each function/global
                name = arr[i].name
                global_uses[name]  = set()
                static_calls[name] = set()
                sources[name] = hsc_bytecode_to_string(
                    syntax_data, string_data, i, tagdata.scripts.STEPTREE,
                    tagdata.globals.STEPTREE, typ, engine,
                    global_uses=global_uses[name],
                    hsc_node_strings_by_type=hsc_node_strings_by_type,
                    static_calls=static_calls[name])

            sorted_sources = []
            need_to_sort = sources
            while need_to_sort:
                # sort the functions/globals so dependencies come first
                next_need_to_sort = {}
                for name in sorted(need_to_sort.keys()):
                    source = need_to_sort[name]
                    if sort_by[name].issubset(already_sorted):
                        sorted_sources.append(source)
                        already_sorted.add(name)
                    else:
                        next_need_to_sort[name] = source

                if need_to_sort.keys() == next_need_to_sort.keys():
                    print("Could not sort these %ss so dependencies come first:" % typ)
                    for name in need_to_sort.keys():
                        print("\t%s" % name)
                        print("\t  Requires: ", ", ".join(sorted(sort_by[name])))
                        print()
                        sorted_sources.append(need_to_sort[name])
                    break
                need_to_sort = next_need_to_sort

            merged_sources = []
            merged_src = ""
            merged_src_len = 0
            # figure out how much data we can fit in the source file
            max_size = MAX_SCRIPT_SOURCE_SIZE - len(header) - len(comments)

            for src in sorted_sources:
                if not src:
                    continue

                src += "\n\n\n"
                # \n will be translated to \r\n, so the actual serialized string
                # length will be incremented by the number of newline characters
                src_len = len(src) + src.count("\n")

                # concatenate sources until they are too large to be compiled
                if merged_src_len + src_len >= max_size:
                    merged_sources.append(merged_src)
                    merged_src = ""
                    merged_src_len = 0

                merged_src += src
                merged_src_len += src_len

            if merged_src:
                merged_sources.append(merged_src)

            i = 0
            for out_data in merged_sources:
                # write sources to hsc files
                if len(merged_sources) > 1:
                    filename = "%s_%s.hsc" % (filename_base, i)
                else:
                    filename = "%s.hsc" % filename_base

                filepath = dirpath.joinpath(filename)
                if not overwrite and filepath.is_file():
                    continue

                # apparently the scripts use latin1 encoding, who knew....
                with filepath.open("w", encoding='latin1', newline="\r\n") as f:
                    f.write(header)
                    f.write(out_data)
                    f.write(comments)

                i += 1
        except Exception:
            return format_exc()

    # TEMPORARY CODE
    #from reclaimer.enums import TEST_PRINT_HSC_BUILT_IN_FUNCTIONS
    #TEST_PRINT_HSC_BUILT_IN_FUNCTIONS()
    # TEMPORARY CODE
