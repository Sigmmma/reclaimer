from os.path import splitext

from supyr_struct.Test import Tag_Test_Library
from .Field_Types import *
from .Defs.Objs.Tag_Obj import GDL_Tag_Obj

class GDL_Library(Tag_Test_Library):
    Default_Tag_Obj   = GDL_Tag_Obj
    Default_Defs_Path = "ReclaimerLib\\GDL\\Defs\\"

    def Get_Cls_ID(self, Filepath):
        Filepath = Filepath.replace('/', '\\')
        try:
            Cls_ID = Filepath.split('\\')[-1].lower()
        except:
            Cls_ID = ''
        
        if splitext(Cls_ID)[-1].lower() == '.xbe':
            Cls_ID = 'xbe'
            
        if Cls_ID in self.Defs:
            return Cls_ID
