from .halo1_map import *
from reclaimer.stubbs.defs.antr import antr_def as stubbs_antr_def
from reclaimer.stubbs.defs.coll import coll_def as stubbs_fast_coll_def
from reclaimer.stubbs.defs.mode import mode_def as stubbs_mode_def
from reclaimer.stubbs.defs.mode import pc_mode_def as stubbs_pc_mode_def
from reclaimer.stubbs.defs.sbsp import fast_sbsp_def as stubbs_fast_sbsp_def
from reclaimer.stubbs.defs.soso import soso_def as stubbs_soso_def
from reclaimer.stubbs.handler   import StubbsHandler
from supyr_struct.defs.frozen_dict import FrozenDict
from supyr_struct.buffer import BytearrayBuffer


class StubbsMap(Halo1Map):
    defs = None

    def setup_tag_headers(self):
        if StubbsMap.tag_headers is not None:
            return

        Halo1Map.setup_tag_headers(self)
        tag_headers = StubbsMap.tag_headers = dict(Halo1Map.tag_headers)

        for b_def in (stubbs_antr_def, stubbs_fast_coll_def,
                      stubbs_mode_def, stubbs_soso_def):
            def_id, h_desc, h_block = b_def.def_id, b_def.descriptor[0], [None]
            h_desc['TYPE'].parser(h_desc, parent=h_block, attr_index=0)
            self.tag_headers[def_id] = bytes(
                h_block[0].serialize(buffer=BytearrayBuffer(),
                                     calc_pointers=False))

    def setup_defs(self):
        if not StubbsMap.defs:
            print("Loading Stubbs tag definitions...")
            StubbsMap.handler = StubbsHandler(build_reflexive_cache=False,
                                              build_raw_data_cache=False)
            StubbsMap.defs = dict(StubbsMap.handler.defs)

            if self.engine == "stubbspc":
                StubbsMap.defs["mode"] = stubbs_pc_mode_def
            else:
                StubbsMap.defs["mode"] = stubbs_mode_def
            StubbsMap.defs["antr"] = stubbs_antr_def
            StubbsMap.defs["coll"] = stubbs_fast_coll_def
            StubbsMap.defs["sbsp"] = stubbs_fast_sbsp_def
            StubbsMap.defs = FrozenDict(StubbsMap.handler.defs)
            print("    Finished")

        # make a shallow copy for this instance to manipulate
        self.defs = dict(self.defs)
