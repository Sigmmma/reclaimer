from ...hek.defs.meta_descs import *
from . import *

modules = locals()
meta_cases = dict(meta_cases)
fcc_map = dict(tag_="tag+", **fcc_map)
fccs.update(["efpc", "efpg", "efpp", "eqhi", "gelc", "gelo", "magy", "shpg",
             "shpp", "sidy", "sily", "sppg", "tag_", "unic", "yelo"])

for fcc in ("actv", "bipd", "ctrl", "eqip", "garb", "lifi", "mach", "matg",
            "obje", "plac", "proj", "scen", "scnr", "senv", "soso", "ssce",
            "tagc", "unit", "vehi", "weap",

            
            "efpc", "efpg", "efpp", "eqhi", "gelc", "gelo", "magy", "shpg",
            "shpp", "sidy", "sily", "sppg", "tag+", "unic", "yelo"):
    identifier_fcc = fcc.replace("+", "_")
    meta_cases[fcc] = modules[identifier_fcc].get().descriptor[1]
