from os.path import splitext

from .tag import *

class MachTag(HekTag):

    def calc_internal_data(self):
        HekTag.calc_internal_data(self)
        mach_attrs = self.data.tagdata.mach_attrs
        mach_attrs.door_open_time_ticks = int(mach_attrs.door_open_time * 30)
