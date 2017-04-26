from ...hek.defs.meta_descs import fccs, fcc_map
from . import *

modules = locals()
meta_cases = {}
fcc_map = dict(tag_="tag+", **fcc_map)
fccs = set(fccs)
fccs.update(["efpc", "efpg", "efpp", "eqhi", "gelc", "gelo", "magy", "shpg",
             "shpp", "sidy", "sily", "sppg", "tag_", "unic", "yelo"])

for fcc in fccs:
    meta_cases[fcc_map.get(fcc, fcc)] = modules[fcc].get().descriptor[1]

# not for export
del modules
