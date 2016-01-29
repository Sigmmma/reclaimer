from hashlib import md5
from os.path import basename, exists, normpath

from supyr_struct.test import TagTestLibrary
from supyr_struct.buffer import BytearrayBuffer
from ..fields import *
from .defs.objs.tag import HekTag


class HaloLibrary(TagTestLibrary):
    default_tag_cls   = HekTag
    default_defs_path = "reclaimer.halo.hek.defs"

    #used whenever we need to know the extension of a tag based
    #on it's FourCC all 83 Halo 1 tag types are defined below
    id_ext_map = {'\x00\x00\x00\x00':'.unknown_tag',
                  '\xff\xff\xff\xff':'.unknown_tag',
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
                  'jpt!':".damage_effect",                      #NEED
                  'effe':".effect",                             #NEED
                  'eqip':".equipment",                          #NEED
                  'flag':".flag",
                  'fog ':".fog",
                  'font':".font",                               #NEED
                  'garb':".garbage",                            #NEED
                  'mod2':".gbxmodel",                           #NEED
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
                  'mode':".model",                              #NEED
                  'antr':".model_animations",                   #NEED
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
                  'snd!':".sound",                              #NEED
                  'snde':".sound_environment",
                  'lsnd':".sound_looping",                      #NEED
                  'ssce':".sound_scenery",                      #NEED
                  'boom':".spheroid",
                  'shdr':".shader",
                  'schi':".shader_transparent_chicago",
                  'scex':".shader_transparent_chicago_extended",
                  'sotr':".shader_transparent_generic",         #NEED
                  'senv':".shader_environment",
                  'sgla':".shader_transparent_glass",
                  'smet':".shader_transparent_meter",
                  'soso':".shader_model",
                  'spla':".shader_transparent_plasma",
                  'swat':".shader_transparent_water",
                  'sky ':".sky",                                #NEED
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
                  }

    ext_id_map = {}

    for key in id_ext_map.keys():
        ext_id_map[id_ext_map[key]] = key

    def __init__(self, *args, **kwargs):
        TagTestLibrary.__init__(self, *args, **kwargs)

        #remove the autogenerated ID_Ext_Map to use the above one
        del self.__dict__['id_ext_map']
            
        if "Default_Conversion_Flags" in kwargs:
            self.Default_Conversion_Flags = kwargs["Default_Conversion_Flags"]
        else:
            self.Default_Conversion_Flags = {}
            for tag_id in self.tags:
                self.Default_Conversion_Flags[tag_id] = {}
        
        if "datadir" in kwargs:
            self.datadir = kwargs["datadir"]
        else:
            self.datadir = basename(normpath(self.tagsdir))
            self.datadir = self.tagsdir.split(self.datadir)[0] + "data\\"

        #call the functions to build the tag_ref_cache,
        #reflexive_cache, and raw_data_cache
        self.tag_ref_cache   = self.build_loc_cache(TagIndexRef)
        self.reflexive_cache = self.build_loc_cache(Reflexive)
        self.raw_data_cache  = self.build_loc_cache(RawDataRef)
    

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
        by caching all possible locations of the Field_Type'''
        cache = {}
        
        for tag_id in self.defs:
            definition = self.defs[tag_id].descriptor

            hasrefs, refs = self._build_loc_cache(f_type, definition)
            
            if hasrefs:
                cache[tag_id] = refs

        return cache


    def get_blocks_by_paths(self, paths, block, cond=None):
        coll = []
        if cond is None:
            cond = lambda x: True
            
        if len(paths):
            self._get_blocks_by_paths(paths, block, coll, cond)

        return coll

        

    def get_tag_id(self, filepath):
        '''It is more reliable to determine a Halo tag
        based on its 4CC tag_id than by file extension'''
        try:            
            with open(filepath, 'r+b') as tagfile:
                tagfile.seek(36)
                tag_id = str(tagfile.read(4), 'latin-1')
                
            if tag_id in self.defs:
                return tag_id
        except:
            return None


    def get_tag_hash(self, tagdata, tag_ref_paths=(),
                     reflexive_paths=(), raw_data_paths=()):
        hash_buffer = BytearrayBuffer()

        #null out the parts of a tag that can screw
        #with the hash when compared to a tag meta                        
        for B in self.get_blocks_by_paths(tag_ref_paths, tagdata):
            B.Tag_Path_Pointer = B.Tag_ID = 0
            
        for B in self.get_blocks_by_paths(reflexive_paths, tagdata):
            B.ID = B.Reflexive_ID = 0
            
        for B in self.get_blocks_by_paths(raw_data_paths, tagdata):
            B.Unknown_1 = B.Unknown_2 = B.Unknown_3 = B.ID = 0

        #write the tag data to the hash buffer
        tagdata.Data.TYPE.writer(tagdata.Data, hash_buffer, None, 0, 0)
        
        return md5(hash_buffer)
        

    def get_tag_not_exist(self, block):
        #if the string is empty, then it doesnt NOT exist, so return False
        if not block.Filepath:
            return False
        tagpath = self.tagsdir
        tagpath += block.Filepath
        
        try:
            tagpath += '.'+block.Tag_Class.data_name
        except Exception:
            pass
        
        return not exists(tagpath)
