from supyr_struct.Constructor import Constructor as TC
from ...Tag_Descriptors.GDL_Descriptors.Objs.Tag_Obj import GDL_Tag_Obj
from supyr_struct.Field_Types import *
from os.path import splitext

class Constructor(TC):
    Default_Defs_Path = "ReclaimerLib\\Tag_Descriptors\\GDL_Descriptors\\"
    Default_Tag_Obj   = GDL_Tag_Obj

    def Get_ID(self, Filepath):
        Filepath = Filepath.replace('/', '\\')
        try:    Cls_ID = Filepath.split('\\')[-1].lower()
        except: Cls_ID = ''
        
        if splitext(Cls_ID)[-1].lower() == '.xbe':
            Cls_ID = 'xbe'
            
        if Cls_ID in self.Definitions:
            return Cls_ID
