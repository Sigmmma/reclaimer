import threading

from traceback import format_exc

from supyr_struct.Library import *
from ...Tag_Constructors.Halo_Constructors.HEK.Constructor import Constructor

class HEK_Tag_Library(Library):
    
    Close_Program = False #if set to True the program will close
    Main_Delay = 0.03     #determines how often the main loop is run

    def __init__(self, **kwargs):
        kwargs["Constructor"] = Constructor
        
        Library.__init__(self, **kwargs)
            
        if "Default_Conversion_Flags" in kwargs:
            self.Default_Conversion_Flags = kwargs["Default_Conversion_Flags"]
        else:
            self.Default_Conversion_Flags = {}
            for Cls_ID in self.Tags:
                self.Default_Conversion_Flags[Cls_ID] = {}
        
        if "Data_Dir" in kwargs:
            self.Data_Dir = kwargs["Data_Dir"]
        else:
            self.Data_Dir = os.path.basename(os.path.normpath(self.Tags_Dir))
            self.Data_Dir = self.Tags_Dir.split(self.Data_Dir)[0] + "data\\"
