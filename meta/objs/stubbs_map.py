from .halo1_map import *
from reclaimer.stubbs.defs.mode import mode_def as stubbs_mode_def
from reclaimer.stubbs.defs.mode import pc_mode_def as stubbs_pc_mode_def
from reclaimer.stubbs.defs.sbsp import fast_sbsp_def as stubbs_fast_sbsp_def
from reclaimer.stubbs.defs.coll import fast_coll_def as stubbs_fast_coll_def
from reclaimer.stubbs.handler   import StubbsHandler


class StubbsMap(Halo1Map):

    def setup_tag_headers(self):
        if StubbsMap.tag_headers is not None:
            return

        Halo1Map.setup_tag_headers(self)
        tag_headers = StubbsMap.tag_headers = dict(Halo1Map.tag_headers)

        for b_def in (stubbs_antr_def, stubbs_coll_def, stubbs_mode_def,
                      stubbs_soso_def):
            def_id, h_desc, h_block = b_def.def_id, b_def.descriptor[0], [None]
            h_desc['TYPE'].parser(h_desc, parent=h_block, attr_index=0)
            self.tag_headers[def_id] = bytes(
                h_block[0].serialize(buffer=BytearrayBuffer(),
                                     calc_pointers=False))

    def setup_defs(self):
        Halo1Map.setup_defs(self)
        if StubbsMap.defs is None:
            print("Loading Stubbs tag definitions...")
            StubbsMap.handler = StubbsHandler(build_reflexive_cache=False,
                                              build_raw_data_cache=False)
            StubbsMap.defs = FrozenDict(StubbsMap.handler.defs)
            print("    Finished")

        if self.engine == "stubbspc":
            self.defs["mode"] = stubbs_pc_mode_def
        else:
            self.defs["mode"] = stubbs_mode_def
        self.defs["sbsp"] = stubbs_fast_sbsp_def
        self.defs["coll"] = stubbs_fast_coll_def
