#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#
from reclaimer.meta.wrappers.halo1_map  import Halo1Map, int_to_fourcc
from reclaimer.os_hek.defs.gelc         import gelc_def
from reclaimer.os_v4_hek.defs.coll      import fast_coll_def
from reclaimer.os_v4_hek.defs.sbsp      import fast_sbsp_def
from reclaimer.os_v4_hek.handler        import OsV4HaloHandler
from supyr_struct.defs.frozen_dict      import FrozenDict


class Halo1YeloMap(Halo1Map):
    '''Generation 1 Yelo map'''
    resource_map_prefix = "~"

    # Module path printed when loading the tag defs
    tag_defs_module = "reclaimer.os_v4_hek.defs"
    # Handler that controls how to load tags, eg tag definitions
    handler_class = OsV4HaloHandler
    # NOTE: setting defs to None so setup_defs doesn't think the
    #       defs are setup cause of class property inheritance.
    defs = None

    @property
    def is_fully_yelo(self):
        # since it's possible to compile open sauce maps without the hard
        # requirement that they be yelo maps, this wrapper is able to be
        # used with the engine still set to halo1ce. to determine if the
        # map is truely a .yelo map, we need to check the engine.
        yelo_header = self.map_header.yelo_header
        return "<INVALID>" not in (
            yelo_header.yelo.enum_name, 
            yelo_header.version_type.enum_name
            )

    @property
    def uses_mod_data_files(self):
        if not self.is_fully_yelo:
            return False

        try:
            return self.map_header.yelo_header.flags.uses_mod_data_files
        except AttributeError:
            return False
    @property
    def resource_map_prefix(self):
        return "~" if self.uses_mod_data_files else ""
    @property
    def resource_maps_folder(self):
        return self.filepath.parent.joinpath(
            "data_files" if self.uses_mod_data_files else ""
            )
    @property
    def decomp_file_ext(self):
        return ".yelo" if self.is_fully_yelo else self._decomp_file_ext

    @property
    def project_yellow_tag_id(self):
        if not(self.is_fully_yelo and self.tag_index):
            return None

        for b in self.tag_index.tag_index:
            if int_to_fourcc(b.class_1.data) == "yelo":
                return b.id & 0xFFff

    @property
    def globals_tag_id(self):
        matg_tag_id = None
        if self.is_fully_yelo:
            yelo_meta = self.get_meta(self.project_yellow_tag_id)
            if yelo_meta:
                matg_tag_id = yelo_meta.globals_override.id & 0xFFff

        for b in self.tag_index.tag_index:
            if matg_tag_id in range(len(self.tag_index.tag_index)):
                break

            if int_to_fourcc(b.class_1.data) == "matg":
                matg_tag_id = b.id & 0xFFff

        if matg_tag_id in range(len(self.tag_index.tag_index)):
            return self.tag_index.tag_index[matg_tag_id].id & 0xFFff

    def setup_defs(self):
        this_class = type(self)
        if this_class.defs is None:
            this_class.defs = defs = {}
            print("    Loading definitions in '%s'" % self.tag_defs_module)
            this_class.handler = self.handler_class(
                build_reflexive_cache=False, build_raw_data_cache=False,
                debug=2)

            this_class.defs = dict(this_class.handler.defs)
            this_class.defs["coll"] = fast_coll_def
            this_class.defs["sbsp"] = fast_sbsp_def
            this_class.defs["gelc"] = gelc_def
            this_class.defs = FrozenDict(this_class.defs)

        # make a shallow copy for this instance to manipulate
        self.defs = dict(self.defs)

    def generate_map_info_string(self):
        string = super().generate_map_info_string()
        if self.is_fully_yelo:
            string += self.generate_yelo_info_string()
        return string

    def generate_yelo_info_string(self):
        yelo    = self.map_header.yelo_header
        flags   = yelo.flags
        info    = yelo.build_info
        version = yelo.tag_versioning
        cheape  = yelo.cheape_definitions
        rsrc    = yelo.resources
        min_os  = info.minimum_os_build

        return """
Yelo information:
    Mod name              == %s
    Memory upgrade amount == %sx

    Flags:
        uses memory upgrades       == %s
        uses mod data files        == %s
        is protected               == %s
        uses game state upgrades   == %s
        has compression parameters == %s

    Build info:
        build string  == %s
        timestamp     == %s
        stage         == %s
        revision      == %s

    Cheape:
        build string      == %s
        version           == %s.%s.%s
        size              == %s
        offset            == %s
        decompressed size == %s

    Versioning:
        minimum open sauce     == %s.%s.%s
        project yellow         == %s
        project yellow globals == %s

    Resources:
        compression parameters header offset   == %s
        tag symbol storage header offset       == %s
        string id storage header offset        == %s
        tag string to id storage header offset == %s\n""" % (
            yelo.mod_name, yelo.memory_upgrade_multiplier,
            bool(flags.uses_memory_upgrades),
            bool(flags.uses_mod_data_files),
            bool(flags.is_protected),
            bool(flags.uses_game_state_upgrades),
            bool(flags.has_compression_params),
            info.build_string, info.timestamp, info.stage.enum_name,
            info.revision, cheape.build_string,
            info.cheape.maj, info.cheape.min, info.cheape.build,
            cheape.size, cheape.offset, cheape.decompressed_size,
            min_os.maj, min_os.min, min_os.build,
            version.project_yellow, version.project_yellow_globals,
            rsrc.compression_params_header_offset,
            rsrc.tag_symbol_storage_header_offset,
            rsrc.string_id_storage_header_offset,
            rsrc.tag_string_to_id_storage_header_offset)