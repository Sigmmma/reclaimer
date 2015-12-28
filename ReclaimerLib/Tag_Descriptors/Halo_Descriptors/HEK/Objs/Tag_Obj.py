from supyr_struct.Defs.Tag_Obj import *
from .....Tag_Constructors.Halo_Constructors.HEK.Field_Types import *


class Halo_Tag_Obj(Tag_Obj):
    __slots__ = ('Tag_Conversion_Settings',
                 'Library', 'Constructor', 'Definition',
                 'Root_Offset', 'Calc_Pointers',
                 'Tag_Source_Path', 'Tag_Path', 'Tag_Data')
    
    def __init__(self, **kwargs):
        Calc_Pointers = False
        
        #this is used by various things to store variables
        #per tag which specify how it is to be changed.
        self.Tag_Conversion_Settings = []
        Tag_Obj.__init__(self, **kwargs)
