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

def _lf_to_crlf(string): # laziness
    return string.replace("\n", "\r\n")


SCRIPT_HEADER  = _lf_to_crlf("; Extracted with Reclaimer\n\n")
MAX_SCRIPT_SOURCE_SIZE      = 1 << 18
MCC_MAX_SCRIPT_SOURCE_SIZE  = 1 << 20


def generate_scenario_references_comment(tagdata):
    '''
    Generate a string which lists out all scenario references 
    that may be useful to have when editing extracted scripts.
    '''
    comments  = "\n; scenario names(each sorted alphabetically)\n"
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
    
    comments += "\n;   globals:\n"
    return _lf_to_crlf(comments)


def extract_scripts(
        tagdata, engine=None, halo_map=None, add_comments=True,
        minify=False, max_script_size=None, default_engine=None, **kwargs
        # NOTE: accepting arbitrary kwargs cause caller wont know what args we use
        ):
    # this will hold the decompiled script source file strings
    script_sources, global_sources = [], []

    engine = engine or getattr(halo_map, "engine", default_engine)
    if max_script_size is None:
        max_script_size = (
            MCC_MAX_SCRIPT_SOURCE_SIZE if engine == "halo1mcc" else
            MAX_SCRIPT_SOURCE_SIZE
            )

    # unknown currently if original halo allows this, but mcc does
    kwargs.setdefault("bool_as_int", engine == "halo1mcc")

    syntax_data = get_hsc_data_block(tagdata.script_syntax_data.data)
    string_data = tagdata.script_string_data.data.decode("latin-1")
    if not syntax_data or not string_data:
        return script_sources, global_sources

    # generate comments string(unless we want sources as small as possible)
    comments = "" if minify or not add_comments else (
        generate_scenario_references_comment(tagdata)
        )

    already_sorted = set()
    for typ, arr in (("global", tagdata.globals.STEPTREE),
                     ("script", tagdata.scripts.STEPTREE)):
        global_uses  = {}
        static_calls = {}
        sort_by = global_uses    if (typ == "global") else static_calls
        sources = global_sources if (typ == "global") else script_sources

        decompiled_scripts = {}
        for i in range(len(arr)):
            # assemble source code for each function/global
            name = arr[i].name
            global_uses[name]  = set()
            static_calls[name] = set()

            decompiled_scripts[name] = hsc_bytecode_to_string(
                syntax_data, string_data, i,
                tagdata.scripts.STEPTREE,
                tagdata.globals.STEPTREE, typ, engine,
                global_uses=global_uses[name],
                static_calls=static_calls[name], minify=minify, **kwargs
                )

        sorted_sources = []
        need_to_sort = decompiled_scripts
        while need_to_sort:
            # sort the functions/globals so dependencies come first
            next_need_to_sort = {}
            for name in sorted(need_to_sort.keys()):
                source = need_to_sort[name]
                sort_remainder = sort_by[name].difference(already_sorted)
                if sort_remainder:
                    next_need_to_sort[name] = source
                    sort_by[name] = sort_remainder
                else:
                    sorted_sources.append(source)
                    already_sorted.add(name)

            if need_to_sort.keys() == next_need_to_sort.keys():
                print("Could not sort these %ss so dependencies come first:" % typ)
                for name in need_to_sort.keys():
                    print("\t%s" % name)
                    print("\t  Requires: ", ", ".join(sorted(sort_by[name])))
                    print()
                    sorted_sources.append(need_to_sort[name])
                break
            need_to_sort = next_need_to_sort

        # header to put before each extracted source file
        header = "" if minify else SCRIPT_HEADER + (
            comments if (typ == "global") else ""
            )

        # concatenate script sources until they are too large to be compiled
        concat_src = ""
        for i, src in enumerate(sorted_sources):
            if src:
                # translate \n to \r\n since that's what haloscripts uses.
                src = _lf_to_crlf(src + ("\n" if minify else "\n\n"))

            # we're gonna pass the limit on script size if we concatenate
            # this script source, so we need to append it and start anew.
            if len(concat_src) + len(src) >= max_script_size:
                sources.append(header + concat_src)
                concat_src = src
            else:
                concat_src += src

            # ensure the last script source is appended if it's not empty
            if i+1 == len(sorted_sources):
                sources.append(header + concat_src)

    # TEMPORARY CODE
    #from reclaimer.enums import TEST_PRINT_HSC_BUILT_IN_FUNCTIONS
    #TEST_PRINT_HSC_BUILT_IN_FUNCTIONS()
    # TEMPORARY CODE

    return script_sources, global_sources


def extract_scripts_to_file(tagdata, tag_path, **kwargs):
    out_dir     = kwargs.pop("out_dir", "")
    overwrite   = kwargs.pop('overwrite', True)
    script_sources, global_sources = extract_scripts(tagdata, **kwargs)

    if not script_sources or not global_sources:
        return "No scripts to extract."

    dirpath = Path(out_dir).joinpath(Path(tag_path).parent, "scripts")
    dirpath.mkdir(exist_ok=True, parents=True)
    for typ, sources in (
            ("scripts", script_sources),
            ("globals", global_sources),
            ):

        for i in range(len(sources)):
            # write sources to hsc files
            filename = "%s_%s.hsc" % (typ, i)
            filepath = dirpath.joinpath(filename)
            if not overwrite and filepath.is_file():
                continue

            # apparently the scripts use latin1 encoding, who knew....
            with filepath.open("w", encoding='latin1', newline="") as f:
                f.write(sources[i])


def extract_h1_scripts(tagdata, tag_path, **kwargs):
    kwargs.setdefault("default_engine", "halo1yelo")
    return extract_scripts_to_file(tagdata, tag_path, **kwargs)


def extract_h1_mcc_scripts(tagdata, tag_path, **kwargs):
    kwargs.setdefault("default_engine", "halo1mcc")
    return extract_scripts_to_file(tagdata, tag_path, **kwargs)