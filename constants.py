from supyr_struct.defs.constants import *
from binilla.constants import *
from supyr_struct.defs.util import fcc
from struct import unpack

# some reflexives are so massive that it's significantly faster to treat them
# as raw data and just byteswap them using precalculated offsets and sizes
RAW_REFLEXIVE_INFO = "RAW_REFLEXIVE_INFO"
COLOR_CHANNELS = "COLOR_CHANNELS"

def inject_halo_constants():
    # add the new descriptor keywords to the sets
    add_desc_keywords(RAW_REFLEXIVE_INFO, COLOR_CHANNELS)


PCDEMO_INDEX_MAGIC         = 0x4BF10000
PC_INDEX_MAGIC             = 0x40440000
CE_INDEX_MAGIC             = 0x40440000
XBOX_INDEX_MAGIC           = 0x803A6000
STUBBS_INDEX_MAGIC         = 0x8038B000
SHADOWRUN_BETA_INDEX_MAGIC = 0x8069E000
H2_ALPHA_INDEX_MAGIC       = 0x80061000
H2_XBOX_INDEX_MAGIC        = 0x80061000  # this at least appears to be the
                                         # case in the singleplayer maps
H2V_MP_INDEX_MAGIC         = 0x01400000  # only applies to multiplayer maps.
#                                          pointers below this index magic
#                                          actually point to resource maps.


map_build_dates = {
    "stubbs":         "400",
    "stubbspc":       "",
    "shadowrun_beta": "01.12.07.0132",
    "halo1xbox":      "01.10.12.2276",
    "halo1xboxbeta":  "",
    "halo1pcdemo":    "01.00.00.0576",
    "halo1pc":        "01.00.00.0564",
    "halo2alpha":     "02.01.07.4998",
    "halo2beta":      "02.06.28.07902",
    "halo2epsilon":   "02.08.28.09214",
    "halo2xbox":      "02.09.27.09809",
    "halo2vista":     "11081.07.04.30.0934.main",
    "halo3":          "11855.07.08.20.2317.halo3_ship",
    "halo1ce":        "01.00.00.0609",
    "halo1yelo":      "01.00.00.0609",
    }

map_versions = {
    "stubbs":         5,
    "stubbspc":       5,
    "shadowrun_beta": 5,
    "halo1xbox":      5,
    "halo1xboxbeta":  5,
    "halo1pcdemo":    6,
    "halo1pc":        7,
    "halo1ce":        609,
    "halo1yelo":      609,
    "halo2alpha":     7,
    "halo2beta":      8,
    "halo2epsilon":   8,
    "halo2xbox":      8,
    "halo2vista":     8,
    "halo3":          11,
    }

# magic is actually the virtual address the map is loaded at. Halo 3 and
# beyond instead partition the map into sections with a virtual address for
# each section, meaning there is a "magic" for different parts of each map.
map_magics = {
    "stubbs":         STUBBS_INDEX_MAGIC,
    "stubbspc":       PC_INDEX_MAGIC,
    "shadowrun_beta": SHADOWRUN_BETA_INDEX_MAGIC,
    "halo1xbox":      XBOX_INDEX_MAGIC,
    "halo1xboxbeta":  XBOX_INDEX_MAGIC,
    "halo1pcdemo":    PCDEMO_INDEX_MAGIC,
    "halo1pc":        PC_INDEX_MAGIC,
    "halo1ce":        CE_INDEX_MAGIC,
    "halo1yelo":      CE_INDEX_MAGIC,
    "halo2alpha":     H2_ALPHA_INDEX_MAGIC,
    "halo2beta":      0,
    "halo2epsilon":   0,
    "halo2xbox":      0,  # Halo 2 and beyond dont use magic
    "halo2vista":     0,
    "halo3":          0,
    "halo4":          0,
    "halo5":          0,
    "halo_reach":     0,
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

DXT_FORMATS = (FORMAT_DXT1, FORMAT_DXT3, FORMAT_DXT5)

PALLETIZED_FORMATS = (FORMAT_P8_BUMP, )

# These name maps must match the constants found in arbytmap
TYPE_NAME_MAP = ("2D", "3D", "CUBE", "WHITE")

FORMAT_NAME_MAP = (
    "A8", "L8", "AL8", "A8L8",
    "UNUSED1", "UNUSED2",
    "R5G6B5",  "UNUSED3", "A1R5G5B5", "A4R4G4B4",
    "X8R8G8B8", "A8R8G8B8",
    "UNUSED4", "UNUSED5",
    "DXT1", "DXT3", "DXT5", "P8-BUMP")

I_FORMAT_NAME_MAP = {FORMAT_NAME_MAP[i]: i for i in range(len(FORMAT_NAME_MAP))}

#each bitmap's number of bytes must be a multiple of 512
BITMAP_PADDING = 512
#each sub-bitmap(cubemap face) must be a multiple of 128 bytes
CUBEMAP_PADDING = 128

#I cant imagine Halo allowing any one field even close to this many
#indices, though I have seen some open sauce stuff go over 180,000.
MAX_REFLEXIVE_COUNT = 2**31-1

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
    tag_class_fcc_to_be_int[tag_cls] = fcc(tag_cls, 'big')
    tag_class_be_int_to_fcc[fcc(tag_cls, 'big')] = tag_cls
    tag_class_fcc_to_le_int[tag_cls] = fcc(tag_cls)
    tag_class_le_int_to_fcc[fcc(tag_cls)] = tag_cls


################################
# Open Sauce related constants #
################################
tag_class_fcc_to_ext_os = {
    'avti': "actor_variant_transform_in",
    'avto': "actor_variant_transform_out",
    'avtc': "actor_variant_transform_collection",
    'efpp': "effect_postprocess",
    'efpc': "effect_postprocess_collection",
    'efpg': "effect_postprocess_generic",
    'eqhi': "equipment_hud_interface",
    'magy': "model_animations_yelo",
    'unic': "multilingual_unicode_string_list",
    'yelo': "project_yellow",
    'gelo': "project_yellow_globals",
    'gelc': "project_yellow_globals_cv",
    'shpp': "shader_postprocess",
    'shpg': "shader_postprocess_generic",
    'sppg': "shader_postprocess_globals",
    'sidy': "string_id_yelo",
    'tag+': "tag_database",
    'sily': "text_value_pair_definition",
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
    tag_class_fcc_to_be_int_os[tag_cls] = fcc(tag_cls, 'big')
    tag_class_be_int_to_fcc_os[fcc(tag_cls, 'big')] = tag_cls
    tag_class_fcc_to_le_int_os[tag_cls] = fcc(tag_cls)
    tag_class_le_int_to_fcc_os[fcc(tag_cls)] = tag_cls



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
    tag_class_fcc_to_be_int_stubbs[tag_cls] = fcc(tag_cls, 'big')
    tag_class_be_int_to_fcc_stubbs[fcc(tag_cls, 'big')] = tag_cls
    tag_class_fcc_to_le_int_stubbs[tag_cls] = fcc(tag_cls)
    tag_class_le_int_to_fcc_stubbs[fcc(tag_cls)] = tag_cls

