#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#
from pathlib import Path
from reclaimer.meta.wrappers.halo1_map import Halo1Map
from reclaimer.mcc_hek.handler         import MCCHaloHandler
from reclaimer.mcc_hek.defs.sbsp       import sbsp_meta_header_def
from reclaimer.meta.wrappers.halo1_rsrc_map import uses_external_sounds

from supyr_struct.util import is_path_empty

class Halo1MccMap(Halo1Map):
    '''Masterchief Collection Halo 1 map'''

    # Module path printed when loading the tag defs
    tag_defs_module = "reclaimer.mcc_hek.defs"
    # Handler that controls how to load tags, eg tag definitions
    handler_class = MCCHaloHandler
    # NOTE: setting defs to None so setup_defs doesn't think the
    #       defs are setup cause of class property inheritance.
    defs = None
    
    sbsp_meta_header_def = sbsp_meta_header_def

    indexable_tag_classes = frozenset(("bitm", "snd!"))

    @property
    def uses_loc_map(self): 
        return False
    @property
    def uses_sounds_map(self):
        try:
            return self.map_header.mcc_flags.use_sounds_map
        except AttributeError:
            return False
    @property
    def uses_fmod_sound_bank(self):
        return not self.uses_sounds_map

    def meta_to_tag_data(self, meta, tag_cls, tag_index_ref, **kwargs):
        # for sounds, ensure we can extract ALL their sample data from either
        # resource map or primary map before potentially overwriting local
        # tag files with them. remastered sounds are stored in fmod, and
        # we can't extract those tags without missing the sample data
        sounds      = self.maps.get("sounds")
        sounds_data = getattr(sounds, "map_data", None)
        if tag_cls == "snd!" and not(self.uses_sounds_map and sounds_data):
            if uses_external_sounds(meta):
                # no sounds.map to read sounds from, and sound
                # data is specified as external. can't extract
                raise ValueError("Sound sample data missing.")

        meta = super().meta_to_tag_data(meta, tag_cls, tag_index_ref, **kwargs)
        if tag_cls == "sbsp":
            for lm in meta.lightmaps.STEPTREE:
                for mat in lm.materials.STEPTREE:
                    mat.lightmap_vertices_offset = 0
                    mat.vertices_offset = 0

        return meta

    def inject_rawdata(self, meta, tag_cls, tag_index_ref):
        if tag_cls == "snd!" and self.uses_fmod_sound_bank and uses_external_sounds(meta):
            # no sounds.map to read sounds from, and sound
            # data is specified as external. can't extract
            return None
        elif tag_cls == "sbsp":
            # mcc render geometry isn't stored the same way as custom edition/xbox.
            # it's stored relative to the pointers in the sbsp meta header, and the
            # size of the verts isn't calculated into the size of the sbsp sector.

            tag_id = tag_index_ref.id & 0xFFFF
            bsp_header = self.bsp_headers.get(tag_id, None)
            if bsp_header is None:
                raise ValueError("No bsp header found for tag %s of type %s" % (
                    tag_id, tag_cls,
                    ))

            uc_sector_start = bsp_header.uncompressed_render_vertices_pointer
            uc_sector_size  = bsp_header.uncompressed_render_vertices_size
            c_sector_start  = bsp_header.compressed_render_vertices_pointer
            c_sector_size   = bsp_header.compressed_render_vertices_size
            uc_sector_end   = uc_sector_start + uc_sector_size
            c_sector_end    = c_sector_start  + c_sector_size
            map_data        = self.map_data

            for lm in meta.lightmaps.STEPTREE:
                for mat in lm.materials.STEPTREE:
                    if mat.vertex_type.enum_name == "compressed":
                        data_block  = mat.compressed_vertices
                        start, end  = c_sector_start, c_sector_end
                        vert_size, lm_vert_size = 32, 8
                    else:
                        data_block  = mat.uncompressed_vertices
                        start, end  = uc_sector_start, uc_sector_end
                        vert_size, lm_vert_size = 56, 20

                    verts_offset    = start + mat.vertices_offset
                    lm_verts_offset = start + mat.lightmap_vertices_offset
                    verts_size      = vert_size * mat.vertices_count
                    lm_verts_size   = lm_vert_size * mat.lightmap_vertices_count
                    vert_data = b''
                    if verts_size and verts_size + verts_offset > end:
                        print("Warning: Render vertices pointed to outside sector.")
                    elif verts_size:
                        map_data.seek(verts_offset)
                        vert_data += map_data.read(verts_size)

                    if lm_verts_size and lm_verts_size + lm_verts_offset > end:
                        print("Warning: Lightmap vertices pointed to outside sector.")
                    elif lm_verts_size:
                        map_data.seek(lm_verts_offset)
                        vert_data += map_data.read(lm_verts_size)

                    data_block.data = bytearray(vert_data)
        else:
            return super().inject_rawdata(meta, tag_cls, tag_index_ref)