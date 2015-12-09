import threading

from traceback import format_exc

from supyr_struct.Handler import *
from ...Tag_Constructors.Halo_Constructors.HEK.Constructor import Constructor

class Halo_Tag_Handler(Handler):
    
    Close_Program = False #if set to True the program will close
    Main_Delay = 0.03     #determines how often the main loop is run

    def __init__(self, **kwargs):
        kwargs["Constructor"] = Constructor
        
        Handler.__init__(self, **kwargs)
            
        if "Default_Conversion_Flags" in kwargs:
            self.Default_Conversion_Flags = kwargs["Default_Conversion_Flags"]
        else:
            self.Default_Conversion_Flags = {}
            for Cls_ID in self.Tag_Collection:
                self.Default_Conversion_Flags[Cls_ID] = {}
        
        if "Data_Directory" in kwargs:
            self.Data_Directory = kwargs["Data_Directory"]
        else:
            self.Data_Directory = os.path.basename(os.path.normpath(self.Tags_Directory))
            self.Data_Directory = self.Tags_Directory.split(self.Data_Directory)[0] + "data\\"
