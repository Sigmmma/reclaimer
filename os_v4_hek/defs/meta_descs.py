from ...os_v3_hek.defs.meta_descs import fccs, fcc_map
from . import *

modules = locals()
meta_cases = {}
fccs = set(fccs)
fccs.remove("gelc")

for fcc in fccs:
    meta_cases[fcc_map.get(fcc, fcc)] = modules[fcc].get().descriptor[1]

# not for export
del modules
