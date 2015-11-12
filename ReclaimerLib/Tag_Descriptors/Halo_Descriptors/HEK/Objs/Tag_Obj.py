from supyr_struct.Defs.Tag_Obj import *
from .....Tag_Constructors.Halo_Constructors.HEK.Field_Types import *


class Halo_Tag_Obj(Tag_Obj):
    Calculate_Pointers = False
    
    def __init__(self, **kwargs):
        #this is used by various things to store variables
        #per tag which specify how it is to be changed.
        self.Tag_Conversion_Settings = {}
        Tag_Obj.__init__(self, **kwargs)
