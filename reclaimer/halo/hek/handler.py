from hashlib import md5
from os.path import basename, exists, normpath, splitext

from supyr_struct.test import TagTestHandler
from supyr_struct.buffer import BytearrayBuffer
from ..fields import *
from .defs.objs.tag import HekTag


class HaloHandler(TagTestHandler):
    default_tag_cls   = HekTag
    default_defs_path = "reclaimer.halo.hek.defs"

    '''
    'actr':".actor",                              #NEED
    'actv':".actor_varient",                      #NEED
    'ant!':".antenna",                            #NEED
    'bipd':".biped",                              #NEED
    'bitm':".bitmap",
    'trak':".camera_track",
    'colo':".color_table",
    'cdmg':".continuous_damage_effect",           #NEED
    'cont':".contrail",                           #NEED
    'deca':".decal",                              #NEED
    'udlg':".dialogue",                           #NEED
    'dobc':".detail_object_collection",           #NEED
    'devi':".device",
    'ctrl':".device_control",                     #NEED
    'lifi':".device_light_fixture",               #NEED
    'mach':".device_machine",                     #NEED
    'jpt!':".damage_effect",
    'effe':".effect",
    'eqip':".equipment",                          #NEED
    'flag':".flag",
    'fog ':".fog",
    'font':".font",                               #NEED
    'garb':".garbage",                            #NEED
    'mod2':".gbxmodel",
    'matg':".globals",                            #NEED
    'glw!':".glow",                               #NEED
    'grhi':".grenade_hud_interface",              #NEED
    'hudg':".hud_globals",                        #NEED
    'hmt ':".hud_message_text",
    'hud#':".hud_number",
    'devc':".input_device_defaults",
    'item':".item",
    'itmc':".item_collection",
    'lens':".lens_flare",                         #NEED
    'ligh':".light",                              #NEED
    'mgs2':".light_volume",                       #NEED
    'elec':".lightning",                          #NEED
    'foot':".material_effects",
    'metr':".meter",
    'mode':".model",
    'antr':".model_animations",
    'coll':".model_collision_geometry",           #NEED
    'mply':".multiplayer_scenario_description",
    'obje':".object",                             #----
    'part':".particle",                           #NEED
    'pctl':".particle_system",                    #NEED
    'phys':".physics",                            #NEED
    'plac':".placeholder",                        #NEED
    'pphy':".point_physics",
    'ngpr':".preferences_network_game",
    'proj':".projectile",                         #NEED
    'scnr':".scenario",                           #NEED
    'sbsp':".scenario_structure_bsp",             #NEED
    'scen':".scenery",                            #NEED
    'snd!':".sound",
    'snde':".sound_environment",
    'lsnd':".sound_looping",                      #NEED
    'ssce':".sound_scenery",                      #NEED
    'boom':".spheroid",
    'shdr':".shader",
    'schi':".shader_transparent_chicago",
    'scex':".shader_transparent_chicago_extended",
    'sotr':".shader_transparent_generic",
    'senv':".shader_environment",
    'sgla':".shader_transparent_glass",
    'smet':".shader_transparent_meter",
    'soso':".shader_model",
    'spla':".shader_transparent_plasma",
    'swat':".shader_transparent_water",
    'sky ':".sky",
    'str#':".string_list",
    'tagc':".tag_collection",
    'Soul':".ui_widget_collection",
    'DeLa':".ui_widget_definition",               #NEED
    'ustr':".unicode_string_list",
    'unit':".unit",                               #----
    'unhi':".unit_hud_interface",                 #NEED
    'vehi':".vehicle",                            #NEED
    'vcky':".virtual_keyboard",                   #NEED
    'weap':".weapon",                             #NEED
    'wphi':".weapon_hud_interface",               #NEED
    'rain':".weather_particle_system",            #NEED
    'wind':".wind"
    '''

    def __init__(self, *args, **kwargs):
        TagTestHandler.__init__(self, *args, **kwargs)

        self.ext_id_map = {}
        for key in self.id_ext_map.keys():
            self.ext_id_map[self.id_ext_map[key]] = key
            
        if "default_conversion_flags" in kwargs:
            self.default_conversion_flags = kwargs["default_conversion_flags"]
        else:
            self.default_conversion_flags = {}
            for def_id in self.tags:
                self.default_conversion_flags[def_id] = {}
        
        if "datadir" in kwargs:
            self.datadir = kwargs["datadir"]
        else:
            self.datadir = basename(normpath(self.tagsdir))
            self.datadir = self.tagsdir.split(self.datadir)[0] + "data\\"

        #call the functions to build the tag_ref_cache,
        #reflexive_cache, and raw_data_cache
        self.tag_ref_cache   = self.build_loc_cache(TagIndexRef)
        self.reflexive_cache = self.build_loc_cache(Reflexive)
        self.raw_data_cache  = self.build_loc_cache(RawdataRef)
    

    def _build_loc_cache(self, f_type, desc={}):
        hasrefs = False
        refs = {}

        try:
            field = desc['TYPE']
        except Exception:
            field = None
        
        if field is f_type:
            return True, None
        elif field is not None:
            for key in desc:
                hassubrefs, subrefs = self._build_loc_cache(f_type,desc[key])
                if hassubrefs:
                    hasrefs = True
                    refs[key] = subrefs
                    
        return hasrefs, refs
    

    def _get_blocks_by_paths(self, paths, block, coll, cond):
        if paths is None:
            if cond(block):
                coll.append(block)
            return
        
        elif isinstance(paths, dict):
            if 'SUB_STRUCT' in paths:
                paths = paths['SUB_STRUCT']
                for i in range(len(block)):
                    self._get_blocks_by_paths(paths, block[i], coll, cond)
                return
            
            for key in paths:
                self._get_blocks_by_paths(paths[key], block[key], coll, cond)
        else:
            raise TypeError("Expected 'paths' to be of type %s or %s, not %s."%
                            (type(None), type(dict), type(paths)) )
    

    def build_loc_cache(self, f_type):
        '''this builds a cache of paths that will be used
        to quickly locate specific field types in structures
        by caching all possible locations of the Field'''
        cache = {}
        
        for def_id in self.defs:
            definition = self.defs[def_id].descriptor

            hasrefs, refs = self._build_loc_cache(f_type, definition)
            
            if hasrefs:
                cache[def_id] = refs

        return cache


    def get_blocks_by_paths(self, paths, block, cond=None):
        coll = []
        if cond is None:
            cond = lambda x: True
            
        if len(paths):
            self._get_blocks_by_paths(paths, block, coll, cond)

        return coll

        

    def get_def_id(self, filepath):
        if not filepath.startswith('.') and '.' in filepath:
            ext = splitext(filepath)[-1].lower()
        else:
            ext = filepath.lower()

        if ext in self.ext_id_map:
            return self.ext_id_map[ext]

        '''It is more reliable to determine a Halo tag
        based on its 4CC def_id than by file extension'''
        try:
            with open(filepath, 'r+b') as tagfile:
                tagfile.seek(36)
                def_id = str(tagfile.read(4), 'latin-1')
            if def_id in self.defs:
                return def_id
        except:
            return None


    def get_tag_hash(self, data, tag_ref_paths=(),
                     reflexive_paths=(), raw_data_paths=()):
        hash_buffer = BytearrayBuffer()

        #null out the parts of a tag that can screw
        #with the hash when compared to a tag meta                        
        for b in self.get_blocks_by_paths(tag_ref_paths, data):
            b.path_pointer = b.id = 0
            
        for b in self.get_blocks_by_paths(reflexive_paths, data):
            b.id = b.pointer = 0
            
        for b in self.get_blocks_by_paths(raw_data_paths, data):
            b.unknown_1 = b.unknown_2 = b.pointer = b.id = 0

        #write the tag data to the hash buffer
        data.TYPE.writer(data, writebuffer=hash_buffer)
        
        return md5(hash_buffer)
        

    def get_tag_not_exist(self, block):
        #if the string is empty, then it doesnt NOT exist, so return False
        if not block.filepath:
            return False
        filepath = self.tagsdir
        filepath += block.filepath
        
        try:
            filepath += '.'+block.tag_class.enum_name
        except Exception:
            pass
        
        return not exists(filepath)
