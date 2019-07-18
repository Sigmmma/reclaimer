import os

from traceback import format_exc

from reclaimer.halo_script.hsc import get_hsc_data_block,\
     hsc_bytecode_to_string

__all__ = ("extract_h1_scripts", )

def extract_h1_scripts(tagdata, tag_path, **kw):
    filepath_base = os.path.join(kw['out_dir'], os.path.dirname(tag_path), "scripts")
    overwrite = kw.get('overwrite', True)
    hsc_node_strings_by_type = kw.get("hsc_node_strings_by_type", ())
    # If the path doesnt exist, create it
    if not os.path.exists(filepath_base):
        os.makedirs(filepath_base)

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
        filepath = os.path.join(filepath_base, "%ss" % typ)
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
                    for src in need_to_sort.keys():
                        print("\t%s" % src)
                        sorted_sources.append(src)
                    break
                need_to_sort = next_need_to_sort

            merged_sources = []
            merged_src = ""
            for src in sorted_sources:
                if not src:
                    continue
                # concatenate sources until they are too large to be compiled
                if len(merged_src) + len(src) > 262100:
                    merged_sources.append(merged_src)
                    merged_src = ""

                merged_src += src + "\n\n\n"

            if merged_src:
                merged_sources.append(merged_src)

            i = 0
            for out_data in merged_sources:
                # write sources to hsc files
                if len(merged_sources) > 1:
                    fp = "%s_%s.hsc" % (filepath, i)
                else:
                    fp = "%s.hsc" % filepath

                if not overwrite and os.path.isfile(fp):
                    continue

                # apparently the scripts use latin1 encoding, who knew....
                with open(fp, "w", encoding='latin1') as f:
                    f.write("; Extracted with Reclaimer\n\n")
                    f.write(out_data)
                    f.write(comments)

                i += 1
        except Exception:
            return format_exc()

    # TEMPORARY CODE
    #from reclaimer.enums import TEST_PRINT_HSC_BUILT_IN_FUNCTIONS
    #TEST_PRINT_HSC_BUILT_IN_FUNCTIONS()
    # TEMPORARY CODE
