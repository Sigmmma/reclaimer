#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from struct import unpack

from supyr_struct.defs.constants import *
from supyr_struct.util import fourcc_to_int
from binilla.constants import *

# some reflexives are so massive that it's significantly faster to treat them
# as raw data and just byteswap them using precalculated offsets and sizes
RAW_REFLEXIVE_INFO = "RAW_REFLEXIVE_INFO"
STRINGID_IDX_BITS = "STRINGID_IDX_BITS"
STRINGID_SET_BITS = "STRINGID_SET_BITS"
STRINGID_LEN_BITS = "STRINGID_LEN_BITS"
COLOR_CHANNELS = "COLOR_CHANNELS"
IGNORE_SAFE_MODE = "IGNORE_SAFE_MODE"

def inject_halo_constants():
    # add the new descriptor keywords to the sets
    add_desc_keywords(RAW_REFLEXIVE_INFO, COLOR_CHANNELS,
                      MAX, MIN, IGNORE_SAFE_MODE,
                      STRINGID_IDX_BITS, STRINGID_SET_BITS, STRINGID_LEN_BITS)


PCDEMO_INDEX_MAGIC          = 0x4BF10000
PC_INDEX_MAGIC              = 0x40440000
CE_INDEX_MAGIC              = 0x40440000
ANNIVERSARY_INDEX_MAGIC     = 0x004B8000
XBOX_INDEX_MAGIC            = 0x803A6000
STUBBS_INDEX_MAGIC          = 0x8038B000
SHADOWRUN_PROTO_INDEX_MAGIC = 0x8069E000
H2_XBOX_INDEX_MAGIC         = 0x80061000


map_build_dates = {
    "stubbs":          "400",
    "stubbspc":        "",
    "shadowrun_proto": "01.12.07.0132",
    "halo1xboxdemo":   "",
    "halo1xbox":       "01.10.12.2276",
    "halo1pcdemo":     "01.00.00.0576",
    "halo1anni":       "01.00.01.0563",
    "halo1ce":         "01.00.00.0609",
    "halo1yelo":       "01.00.00.0609",
    "halo1vap":        "01.00.00.0609",
    "halo1pc":         "01.00.00.0564",
    "halo2alpha":      "02.01.07.4998",
    "halo2beta":       "02.06.28.07902",
    "halo2epsilon":    "02.08.28.09214",
    "halo2xbox":       "02.09.27.09809",
    "halo2vista":      "11081.07.04.30.0934.main",
    "halo3beta":       "",  # SET THIS
    "halo3":           "11855.07.08.20.2317.halo3_ship",
    "halo3odst":       "13895.09.04.27.2201.atlas_relea",
    "haloreachbeta":   "11860.10.07.24.0147.omaha_relea",
    "haloreach":       "",  # SET THIS
    "halo4":           "20810.12.09.22.1647.main",
    "halo4nettest":    "",  # SET THIS
    "halo5":           "",  # SET THIS
    }

map_versions = {
    "stubbs":          5,
    "stubbspc":        5,
    "shadowrun_proto": 5,
    "halo1xboxdemo":   5,
    "halo1xbox":       5,
    "halo1pcdemo":     6,
    "halo1pc":         7,
    "halo1anni":       7,
    "halo1ce":         609,
    "halo1yelo":       609,
    "halo1vap":        134,
    "halo2alpha":      7,
    "halo2beta":       8,
    "halo2epsilon":    8,
    "halo2xbox":       8,
    "halo2vista":      8,
    "halo3beta":       9,
    "halo3":           11,
    "halo3odst":       11,
    "haloreachbeta":   12,
    "haloreach":       12,
    "halo4":           12,
    #"halo4nettest":    ????,
    #"halo5":           ????,
    }

GEN_1_HALO_ENGINES = ("halo1xboxdemo", "halo1xbox",
                      "halo1ce", "halo1vap", "halo1yelo",
                      "halo1pcdemo", "halo1pc", "halo1anni", )

GEN_1_ENGINES = GEN_1_HALO_ENGINES + (
    "stubbs", "stubbspc", "shadowrun_proto", )

GEN_2_ENGINES = ("halo2alpha", "halo2beta", "halo2epsilon",
                 "halo2xbox", "halo2vista", )

GEN_3_ENGINES = ("halo3", "halo3odst", "halo3beta",
                 "haloreachbeta", "haloreach",
                 "halo4", "halo4nettest", "halo5", )

# magic is actually the virtual address the map is loaded at. Halo 3 and
# beyond instead partition the map into sections with a virtual address for
# each section, meaning there is a "magic" for different parts of each map.
map_magics = {
    "stubbs":          STUBBS_INDEX_MAGIC,
    "stubbspc":        PC_INDEX_MAGIC,
    "shadowrun_proto": SHADOWRUN_PROTO_INDEX_MAGIC,
    "halo1xboxdemo":   XBOX_INDEX_MAGIC,
    "halo1xbox":       XBOX_INDEX_MAGIC,
    "halo1pcdemo":     PCDEMO_INDEX_MAGIC,
    "halo1pc":         PC_INDEX_MAGIC,
    "halo1anni":       ANNIVERSARY_INDEX_MAGIC,
    "halo1ce":         CE_INDEX_MAGIC,
    "halo1yelo":       CE_INDEX_MAGIC,
    "halo1vap":        CE_INDEX_MAGIC,
    "halo2alpha":      H2_XBOX_INDEX_MAGIC,
    "halo2beta":       H2_XBOX_INDEX_MAGIC,
    "halo2epsilon":    H2_XBOX_INDEX_MAGIC,
    "halo2xbox":       H2_XBOX_INDEX_MAGIC,
    }

# bitmap types
TYPE_2D = 0
TYPE_3D = 1
TYPE_CUBEMAP = 2
TYPE_WHITE = 3

# bitmap formats
FORMAT_A8 = 0
FORMAT_Y8 = 1
FORMAT_AY8 = 2
FORMAT_A8Y8 = 3
FORMAT_R5G6B5 = 6
FORMAT_A1R5G5B5 = 8
FORMAT_A4R4G4B4 = 9
FORMAT_X8R8G8B8 = 10
FORMAT_A8R8G8B8 = 11
FORMAT_DXT1 = 14
FORMAT_DXT3 = 15
FORMAT_DXT5 = 16
FORMAT_P8_BUMP = 17
FORMAT_P8 = 18
FORMAT_A32R32G32B32F = 19
FORMAT_R32G32B32F = 20
FORMAT_R16G16B16F = 21
FORMAT_V8U8 = 22
FORMAT_G8B8 = 23
FORMAT_DXN = 33
FORMAT_CTX1 = 34
FORMAT_DXT3A = 35
FORMAT_DXT3Y = 36
FORMAT_DXT5A = 37
FORMAT_DXT5Y = 38
FORMAT_DXT5AY = 39

DXT_FORMATS = (FORMAT_DXT1, FORMAT_DXT3, FORMAT_DXT5)

PALLETIZED_FORMATS = (FORMAT_P8_BUMP, )

# These name maps must match the constants found in arbytmap
TYPE_NAME_MAP = ("2D", "3D", "CUBE", "WHITE")

# this map corrosponds to the bitmap formats
# found in the "format" enum in the bitmap tag
# NOTE: These names must be unique, as they are used to map arbytmap
# formats to halo bitmap format enum values. P8 needs to be its own
# format which is just a variant of A8R8G8B8 so we know its P8.
FORMAT_NAME_MAP = (
    "A8", "L8", "AL8", "A8L8",
    "UNUSED1", "UNUSED2",
    "R5G6B5",  "UNUSED3", "A1R5G5B5", "A4R4G4B4",
    "X8R8G8B8", "A8R8G8B8",
    "UNUSED4", "UNUSED5",
    "DXT1", "DXT3", "DXT5", "P8-BUMP", "P8",
    "A32R32G32B32F", "R32G32B32F", "R16G16B16F",
    "V8U8", "G8B8", "UNUSED6", "UNUSED7", "UNUSED8",
    "UNUSED9", "UNUSED10", "UNUSED11", "UNUSED12", "UNUSED13",
    "UNUSED14", "DXN", "CTX1", "DXT3A", "DXT3Y", "DXT5A", "DXT5Y", "DXT5AY")

I_FORMAT_NAME_MAP = {}
for i in range(len(FORMAT_NAME_MAP)):
    if i not in I_FORMAT_NAME_MAP:
        I_FORMAT_NAME_MAP[FORMAT_NAME_MAP[i]] = i

#each bitmap's number of bytes must be a multiple of 512
BITMAP_PADDING = 512
#each sub-bitmap(cubemap face) must be a multiple of 128 bytes
CUBEMAP_PADDING = 128

# max value a reflexive count is theoretically allowed to be
MAX_REFLEXIVE_COUNT = 2**31-1

# this number was taken by seeing what the highest indexable reflexive number
# is.
SANE_MAX_REFLEXIVE_COUNT = 0xFFFE

MAX_TAG_PATH_LEN = 254

# maps tag class four character codes(fccs) in
# their string encoding to their int encoding.
tag_class_fcc_to_be_int = {}
tag_class_fcc_to_le_int = {}
# maps tag class four character codes(fccs) in
# their int encoding to their string encoding.
tag_class_be_int_to_fcc = {}
tag_class_le_int_to_fcc = {}

# maps tag class four character codes to the tags file extension
tag_class_fcc_to_ext = {
    'actr': "actor",
    'actv': "actor_variant",
    'ant!': "antenna",
    'bipd': "biped",
    'bitm': "bitmap",
    'trak': "camera_track",
    'colo': "color_table",
    'cdmg': "continuous_damage_effect",
    'cont': "contrail",
    'jpt!': "damage_effect",
    'deca': "decal",
    'udlg': "dialogue",
    'dobc': "detail_object_collection",
    'devi': "device",
    'ctrl': "device_control",
    'lifi': "device_light_fixture",
    'mach': "device_machine",
    'effe': "effect",
    'eqip': "equipment",
    'flag': "flag",
    'fog ': "fog",
    'font': "font",
    'garb': "garbage",
    'mod2': "gbxmodel",
    'matg': "globals",
    'glw!': "glow",
    'grhi': "grenade_hud_interface",
    'hudg': "hud_globals",
    'hmt ': "hud_message_text",
    'hud#': "hud_number",
    'devc': "input_device_defaults",
    'item': "item",
    'itmc': "item_collection",
    'lens': "lens_flare",
    'ligh': "light",
    'mgs2': "light_volume",
    'elec': "lightning",
    'foot': "material_effects",
    'metr': "meter",
    'mode': "model",
    'antr': "model_animations",
    'coll': "model_collision_geometry",
    'mply': "multiplayer_scenario_description",
    'obje': "object",
    'part': "particle",
    'pctl': "particle_system",
    'phys': "physics",
    'plac': "placeholder",
    'pphy': "point_physics",
    'ngpr': "preferences_network_game",
    'proj': "projectile",
    'scnr': "scenario",
    'sbsp': "scenario_structure_bsp",
    'scen': "scenery",
    'snd!': "sound",
    'snde': "sound_environment",
    'lsnd': "sound_looping",
    'ssce': "sound_scenery",
    'boom': "spheroid",
    'shdr': "shader",
    'schi': "shader_transparent_chicago",
    'scex': "shader_transparent_chicago_extended",
    'sotr': "shader_transparent_generic",
    'senv': "shader_environment",
    'sgla': "shader_transparent_glass",
    'smet': "shader_transparent_meter",
    'soso': "shader_model",
    'spla': "shader_transparent_plasma",
    'swat': "shader_transparent_water",
    'sky ': "sky",
    'str#': "string_list",
    'tagc': "tag_collection",
    'Soul': "ui_widget_collection",
    'DeLa': "ui_widget_definition",
    'ustr': "unicode_string_list",
    'unit': "unit",
    'unhi': "unit_hud_interface",
    'vehi': "vehicle",
    'vcky': "virtual_keyboard",
    'weap': "weapon",
    'wphi': "weapon_hud_interface",
    'rain': "weather_particle_system",
    'wind': "wind",
    }
tag_class_ext_to_fcc = {}

for tag_cls in tag_class_fcc_to_ext:
    tag_class_ext_to_fcc[tag_class_fcc_to_ext[tag_cls]] = tag_cls
    tag_class_fcc_to_be_int[tag_cls] = fourcc_to_int(tag_cls, 'big')
    tag_class_be_int_to_fcc[fourcc_to_int(tag_cls, 'big')] = tag_cls
    tag_class_fcc_to_le_int[tag_cls] = fourcc_to_int(tag_cls)
    tag_class_le_int_to_fcc[fourcc_to_int(tag_cls)] = tag_cls


################################
# Open Sauce related constants #
################################
tag_class_fcc_to_ext_os = {
    'efpp': "effect_postprocess",
    'efpc': "effect_postprocess_collection",
    'efpg': "effect_postprocess_generic",
    'eqhi': "equipment_hud_interface",
    'magy': "model_animations_yelo",
    'unic': "multilingual_unicode_string_list",
    'yelo': "project_yellow",
    'gelo': "project_yellow_globals",
    'gelc': "project_yellow_globals_cv",  # removed in OS v4
    'shpp': "shader_postprocess",
    'shpg': "shader_postprocess_generic",
    'sppg': "shader_postprocess_globals",
    'sidy': "string_id_yelo",
    'tag+': "tag_database",
    'sily': "text_value_pair_definition",

    # added in OS v4
    'avti': "actor_variant_transform_in",
    'avto': "actor_variant_transform_out",
    'avtc': "actor_variant_transform_collection",
    }

tag_class_fcc_to_ext_os.update(tag_class_fcc_to_ext)
tag_class_ext_to_fcc_os = {}

for tag_cls in tag_class_fcc_to_ext_os:
    tag_class_ext_to_fcc_os[tag_class_fcc_to_ext_os[tag_cls]] = tag_cls

# maps open sauce tag class four character codes(fccs)
# in their string encoding to their int encoding.
tag_class_fcc_to_be_int_os = {}
tag_class_fcc_to_le_int_os = {}
# maps open sauce tag class four character codes(fccs)
# in their int encoding to their string encoding.
tag_class_be_int_to_fcc_os = {}
tag_class_le_int_to_fcc_os = {}

for tag_cls in tag_class_fcc_to_ext_os:
    tag_class_fcc_to_be_int_os[tag_cls] = fourcc_to_int(tag_cls, 'big')
    tag_class_be_int_to_fcc_os[fourcc_to_int(tag_cls, 'big')] = tag_cls
    tag_class_fcc_to_le_int_os[tag_cls] = fourcc_to_int(tag_cls)
    tag_class_le_int_to_fcc_os[fourcc_to_int(tag_cls)] = tag_cls



#######################################
# Stubbs the Zombie related constants #
#######################################
tag_class_fcc_to_ext_stubbs = {
    'imef': "image_effect",
    'vege': "vegetation",
    'terr': "terrain",  # as kornman said, i dont fucking know
    }

tag_class_fcc_to_ext_stubbs.update(tag_class_fcc_to_ext)
tag_class_ext_to_fcc_stubbs = {}

for tag_cls in tag_class_fcc_to_ext_stubbs:
    tag_class_ext_to_fcc_stubbs[tag_class_fcc_to_ext_stubbs[tag_cls]] = tag_cls

# maps open sauce tag class four character codes(fccs)
# in their string encoding to their int encoding.
tag_class_fcc_to_be_int_stubbs = {}
tag_class_fcc_to_le_int_stubbs = {}
# maps open sauce tag class four character codes(fccs)
# in their int encoding to their string encoding.
tag_class_be_int_to_fcc_stubbs = {}
tag_class_le_int_to_fcc_stubbs = {}

for tag_cls in tag_class_fcc_to_ext_stubbs:
    tag_class_fcc_to_be_int_stubbs[tag_cls] = fourcc_to_int(tag_cls, 'big')
    tag_class_be_int_to_fcc_stubbs[fourcc_to_int(tag_cls, 'big')] = tag_cls
    tag_class_fcc_to_le_int_stubbs[tag_cls] = fourcc_to_int(tag_cls)
    tag_class_le_int_to_fcc_stubbs[fourcc_to_int(tag_cls)] = tag_cls
