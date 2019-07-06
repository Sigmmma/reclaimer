from reclaimer.hek.defs.objs.obje import ObjeTag

class MachTag(ObjeTag):

    def calc_internal_data(self):
        ObjeTag.calc_internal_data(self)
        mach_attrs = self.data.tagdata.mach_attrs
        mach_attrs.door_open_time_ticks = int(mach_attrs.door_open_time * 30)
