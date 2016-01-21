from os.path import basename, normpath

from supyr_struct.Test import Tag_Test_Library
from ..Field_Types import *
from .Defs.Objs.Tag import HEK_Tag


class Halo_Library(Tag_Test_Library):
    Default_Tag_Cls   = HEK_Tag
    Default_Defs_Path = "ReclaimerLib.Halo.HEK.Defs"

    #used whenever we need to know the extension of a tag based
    #on it's FourCC all 83 Halo 1 tag types are defined below
    ID_Ext_Map = {b"\x00\x00\x00\x00":".unknown_tag",
                  "":".unknown_tag",
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

    Ext_ID_Map = {}

    for key in ID_Ext_Map.keys():
        Ext_ID_Map[ID_Ext_Map[key]] = key

    def __init__(self, *args, **kwargs):
        Tag_Test_Library.__init__(self, *args, **kwargs)

        #remove the autogenerated ID_Ext_Map to use the above one
        del self.__dict__['ID_Ext_Map']
            
        if "Default_Conversion_Flags" in kwargs:
            self.Default_Conversion_Flags = kwargs["Default_Conversion_Flags"]
        else:
            self.Default_Conversion_Flags = {}
            for Cls_ID in self.Tags:
                self.Default_Conversion_Flags[Cls_ID] = {}
        
        if "Data_Dir" in kwargs:
            self.Data_Dir = kwargs["Data_Dir"]
        else:
            self.Data_Dir = basename(normpath(self.Tags_Dir))
            self.Data_Dir = self.Tags_Dir.split(self.Data_Dir)[0] + "data\\"
        

    def Get_Cls_ID(self, Filepath):
        '''It is more reliable to determine a Halo tag
        based on its 4CC Cls_ID than by file extension'''
        try:            
            with open(Filepath, 'r+b') as Tag_File:
                Tag_File.seek(36)
                Cls_ID = str(Tag_File.read(4), 'latin-1')
                
            if Cls_ID in self.Defs:
                return Cls_ID
        except:
            return None

    def _Build_Loc_Cache(self, F_Type, Desc={}):
        Has_Refs = False
        Refs = {}

        try:
            Type = Desc['TYPE']
        except Exception:
            Type = None
        
        if Type is F_Type:
            return True, None
        elif Type is not None:
            for key in Desc:
                Has_Sub_Refs, Sub_Refs = self._Build_Loc_Cache(F_Type,Desc[key])
                if Has_Sub_Refs:
                    Has_Refs = True
                    Refs[key] = Sub_Refs
                    
        return Has_Refs, Refs
    

    def _Get_Blocks_By_Paths(self, Paths, Block, Coll, Cond):
        if Paths is None:
            if Cond(Block):
                Coll.append(Block)
            return
        
        elif isinstance(Paths, dict):
            if 'SUB_STRUCT' in Paths:
                Paths = Paths['SUB_STRUCT']
                for i in range(len(Block)):
                    self._Get_Blocks_By_Paths(Paths, Block[i], Coll, Cond)
                return
            
            for key in Paths:
                self._Get_Blocks_By_Paths(Paths[key], Block[key], Coll, Cond)
        else:
            raise TypeError("Expected 'Paths' to be of type %s or %s, not %s."%
                            (type(None), type(dict), type(paths)) )
    

    def Build_Loc_Cache(self, F_Type):
        '''this builds a cache of paths that will be used
        to quickly locate specific field types in structures
        by caching all possible locations of the Field_Type'''
        Cache = {}
        
        for Cls_ID in self.Defs:
            Def = self.Defs[Cls_ID].Tag_Structure

            Has_Refs, Refs = self._Build_Loc_Cache(F_Type, Def)
            
            if Has_Refs:
                Cache[Cls_ID] = Refs

        return Cache


    def Get_Blocks_By_Paths(self, Paths, Block, Cond=None):
        Coll = []
        if Cond is None:
            Cond = lambda x: True
            
        if len(Paths):
            self._Get_Blocks_By_Paths(Paths, Block, Coll, Cond)

        return Coll
