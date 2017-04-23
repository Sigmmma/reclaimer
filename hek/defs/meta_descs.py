from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef
from . import *

'''-----------------------   Notes   ---------------------------
    If a tag is located in one of the shared resource maps, the
    offset in tag_header will the the index in the resource
    map that the tag is located in and indexed will be 1.
    To determine which resource map the tag is in, it must be
    done based on the tag class.
    bitm- > bitmaps.map
    snd! -> sounds.map
    font, hmt , str#, ustr -> loc.map
'''

# sound tags actually located in the sound cache
# still have part of the tag exist in the map.
indexed_sound = dict(snd_.snd__def.descriptor[1])
indexed_sound[18] = reflexive_struct


meta_cases = {
    'indexed_snd!':indexed_sound,
    }
modules = locals()
fcc_map = dict(ant_="ant!", glw_="glw!", jpt_="jpt!", snd_="snd!",
               hud_="hud#", str_="str#", fog_="fog ", hmt_="hmt ", sky_="sky ")
fccs = set(["actr", "actv", "ant_", "antr", "bipd", "bitm", "boom", "cdmg",
            "coll", "colo", "cont", "ctrl", "deca", "DeLa", "devc", "devi",
            "dobc", "effe", "elec", "eqip", "flag", "fog_", "font", "foot",
            "garb", "glw_", "grhi", "hmt_", "hud_", "hudg", "item", "itmc",
            "jpt_", "lens", "lifi", "ligh", "mach", "matg", "metr", "mgs2",
            "mod2", "mode", "mply", "ngpr", "obje", "part", "pctl", "phys",
            "plac", "pphy", "proj", "rain", "sbsp", "scen", "scex", "schi",
            "scnr", "senv", "sgla", "shdr", "sky_", "smet", "snd_", "snde",
            "sndl", "soso", "sotr", "Soul", "spla", "ssce", "str_", "swat",
            "tagc", "trak", "udlg", "unhi", "unit", "ustr", "vcky", "vehi",
            "weap", "wind", "wphi"])

for fcc in fccs:
    meta_cases[fcc_map.get(fcc, fcc)] = modules[fcc].get().descriptor[1]

# not for export
del modules
