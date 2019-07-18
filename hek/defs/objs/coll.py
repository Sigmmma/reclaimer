from reclaimer.hek.defs.objs.tag import HekTag

class CollTag(HekTag):

    def calc_internal_data(self):
        HekTag.calc_internal_data(self)
        
        shield = self.data.tagdata.shield
        shield.shield_recharge_rate = 0
        if shield.recharge_time:
            shield.shield_recharge_rate = 1 / shield.recharge_time
        shield.shield_recharge_rate /= 30
