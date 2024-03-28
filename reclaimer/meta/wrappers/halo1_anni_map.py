#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from math import pi, sqrt, log
from traceback import format_exc

from reclaimer.meta.wrappers.byteswapping import byteswap_anniversary_sbsp,\
    byteswap_anniversary_antr, byteswap_anniversary_rawdata_ref,\
    byteswap_scnr_script_syntax_data, end_swap_float, end_swap_int32,\
    end_swap_int16, end_swap_uint32, end_swap_uint16
    
from reclaimer.misc.defs.recorded_animations import build_r_a_stream_block
from reclaimer.meta.wrappers.halo_map import HaloMap
from reclaimer.meta.wrappers.halo1_rsrc_map import Halo1RsrcMap
from reclaimer.meta.wrappers.halo1_mcc_map import Halo1MccMap
from reclaimer import data_extraction
from reclaimer.halo_script.hsc import h1_script_syntax_data_def
from reclaimer.hek.defs.coll import fast_coll_def
from reclaimer.hek.defs.sbsp import fast_sbsp_def
from reclaimer.hek.handler import HaloHandler
from reclaimer.util import int_to_fourcc

from supyr_struct.field_types import FieldType

__all__ = ("Halo1AnniMap",)


class Halo1AnniMap(Halo1MccMap):
    tag_headers = None
    # NOTE: setting defs to None so setup_defs doesn't think the
    #       defs are setup cause of class property inheritance.
    defs = None

    handler_class = HaloHandler

    @property
    def uses_bitmaps_map(self): return False
    @property
    def uses_sounds_map(self): return False

    def is_indexed(self, tag_id):
        return False

    def setup_sbsp_headers(self):
        with FieldType.force_big:
            super().setup_sbsp_headers()

    def setup_rawdata_pages(self):
        # NOTE: for some reason, anniversary maps have overlap between the 
        #       sbsp virtual address range and the tag data address range. 
        #       because of this, we don't setup any pages in the default 
        #       pointer converter for sbsp
        # NOTE: we also don't setup pages for the model data section, since
        #       it's  also overlapping with the tag data address range.
        pass

    def get_meta(self, tag_id, reextract=False, ignore_rsrc_sounds=False, **kw):
        '''
        Takes a tag reference id as the sole argument.
        Returns that tags meta data as a parsed block.
        '''
        if tag_id is None:
            return
        magic     = self.map_magic
        map_data  = self.map_data
        tag_index = self.tag_index
        tag_index_array = tag_index.tag_index

        tag_id &= 0xFFFF
        tag_index_ref = self.tag_index_manager.get_tag_index_ref(tag_id)
        if tag_index_ref is None:
            return

        tag_cls = None
        if tag_id == tag_index.scenario_tag_id & 0xFFff:
            tag_cls = "scnr"
        elif tag_index_ref.class_1.enum_name not in ("<INVALID>", "NONE"):
            tag_cls = int_to_fourcc(tag_index_ref.class_1.data)

        # if we dont have a defintion for this tag_cls, then return nothing
        if self.get_meta_descriptor(tag_cls) is None:
            return

        if tag_cls is None:
            # couldn't determine the tag class
            return
        elif reextract:
            pass
        elif tag_id == tag_index.scenario_tag_id & 0xFFff and self.scnr_meta:
            return self.scnr_meta
        elif tag_cls == "matg" and self.matg_meta:
            return self.matg_meta

        desc = self.get_meta_descriptor(tag_cls)
        block = [None]
        pointer_converter = self.bsp_pointer_converters.get(
            tag_id, self.map_pointer_converter)

        offset = pointer_converter.v_ptr_to_f_ptr(tag_index_ref.meta_offset)

        try:
            # read the meta data from the map
            with FieldType.force_big:
                desc['TYPE'].parser(
                    desc, parent=block, attr_index=0, rawdata=map_data,
                    map_pointer_converter=pointer_converter,
                    tag_index_manager=self.tag_index_manager, offset=offset)
        except Exception:
            print(format_exc())
            if kw.get("allow_corrupt"):
                return block[0]
            return

        meta = block[0]
        try:

            self.record_map_cache_read(tag_id, 0)  # cant get size quickly enough
            if self.map_cache_over_limit():
                self.clear_map_cache()

            self.inject_rawdata(meta, tag_cls, tag_index_ref)
            self.byteswap_anniversary_fields(meta, tag_cls)
        except Exception:
            print(format_exc())
            if not kw.get("allow_corrupt"):
                meta = None

        return meta

    def byteswap_anniversary_fields(self, meta, tag_cls):
        # fix all the forced-little-endian fields that are big-endian, but were
        # read as little-endian(that's what FlUInt/FlSInt/FlFloat fields are)

        # TODO: use handler build_loc_caches to locate all forced-little-endian
        #       fields and force them to big-endian without having to write these
        if tag_cls == "antr":
            for b in meta.animations.STEPTREE:
                b.first_permutation_index = end_swap_int16(b.first_permutation_index)
                b.chance_to_play          = end_swap_float(b.chance_to_play)

            byteswap_anniversary_antr(meta)

        elif tag_cls == "bitm":
            for b in meta.bitmaps.STEPTREE:
                b.pixels = end_swap_uint16(b.pixels)

        elif tag_cls == "coll":
            for b in meta.nodes.STEPTREE:
                b.unknown = end_swap_int16(b.unknown)
                b.damage_region = end_swap_int16(b.damage_region)

        elif tag_cls == "effe":
            for event in meta.events.STEPTREE:
                for b in event.particles.STEPTREE:
                    b.unknown0 = end_swap_int16(b.unknown0)
                    b.unknown1 = end_swap_int16(b.unknown1)

        elif tag_cls == "hmt ":
            byteswap_anniversary_rawdata_ref(meta.string, size=2, two_byte_offs=[0])

        elif tag_cls == "lens":
            meta.cosine_falloff_angle = end_swap_float(meta.cosine_falloff_angle)
            meta.cosine_cutoff_angle  = end_swap_float(meta.cosine_cutoff_angle)

        elif tag_cls == "lsnd":
            meta.unknown0 = end_swap_float(meta.unknown0)
            meta.unknown1 = end_swap_float(meta.unknown1)
            meta.unknown2 = end_swap_float(meta.unknown2)
            meta.unknown3 = end_swap_float(meta.unknown3)
            meta.unknown4 = end_swap_int16(meta.unknown4)
            meta.unknown5 = end_swap_int16(meta.unknown5)
            meta.max_distance = end_swap_float(meta.max_distance)

        elif tag_cls == "metr":
            meta.screen_x_pos = end_swap_uint16(meta.screen_x_pos)
            meta.screen_y_pos = end_swap_uint16(meta.screen_y_pos)
            meta.width  = end_swap_uint16(meta.width)
            meta.height = end_swap_uint16(meta.height)

        elif tag_cls in ("mod2", "mode"):
            for node in meta.nodes.STEPTREE:
                node.scale = end_swap_float(node.scale)
                for b in (node.rot_jj_kk, node.rot_kk_ii, node.rot_ii_jj,
                          node.translation_to_root):
                    for i, val in enumerate(b):
                        b[i] = end_swap_float(val)

        elif tag_cls == "part":
            meta.rendering.unknown0 = end_swap_int32(meta.rendering.unknown0)
            meta.rendering.unknown1 = end_swap_float(meta.rendering.unknown1)
            meta.rendering.unknown2 = end_swap_uint32(meta.rendering.unknown2)

        elif tag_cls == "pphy":
            meta.scaled_density      = end_swap_float(meta.scaled_density)
            meta.water_gravity_scale = end_swap_float(meta.water_gravity_scale)
            meta.air_gravity_scale   = end_swap_float(meta.air_gravity_scale)

        elif tag_cls == "sbsp":
            for b in meta.collision_materials.STEPTREE:
                b.material_type.data = end_swap_int16(b.material_type.data)

            for b in meta.fog_planes.STEPTREE:
                b.material_type.data = end_swap_int16(b.material_type.data)

            for lm in meta.lightmaps.STEPTREE:
                for b in lm.materials.STEPTREE:
                    b.unknown_meta_offset0          = end_swap_uint32(b.unknown_meta_offset0)
                    b.unknown_meta_offset1          = end_swap_uint32(b.unknown_meta_offset1)
                    b.vertices_meta_offset          = end_swap_uint32(b.vertices_meta_offset)
                    b.lightmap_vertices_meta_offset = end_swap_uint32(b.lightmap_vertices_meta_offset)

            # byteswap the rawdata
            byteswap_anniversary_sbsp(meta)

            # TODO: Might need to byteswap cluster data and sound_pas data

        elif tag_cls == "scnr":
            for b in meta.object_names.STEPTREE:
                b.object_type.data = end_swap_int16(b.object_type.data)
                b.reflexive_index  = end_swap_int16(b.reflexive_index)

            for b in meta.trigger_volumes.STEPTREE:
                b.unknown0 = end_swap_uint16(b.unknown0)

            for b in meta.encounters.STEPTREE:
                b.unknown = end_swap_uint16(b.unknown)

            for ra in meta.recorded_animations.STEPTREE:
                # parse the recorded animations as big-endian
                # and serialize back as little-endian
                try:
                    with FieldType.force_big:
                        ra_block = build_r_a_stream_block(
                            ra.unit_control_data_version,
                            ra.recorded_animation_event_stream.STEPTREE,
                            simple=True
                            )
                    ra.recorded_animation_event_stream.STEPTREE = ra_block.serialize()
                except Exception:
                    print(format_exc())
                    print("Could not byteswap recorded animation '%s'" % ra.name)

            # NOTE: this is gonna get swapped back when converting to tagdata
            byteswap_scnr_script_syntax_data(meta)

        elif tag_cls == "senv":
            bump_props = meta.senv_attrs.bump_properties
            bump_props.map_scale_x = end_swap_float(bump_props.map_scale_x)
            bump_props.map_scale_y = end_swap_float(bump_props.map_scale_y)

        elif tag_cls == "snd!":
            for pr in meta.pitch_ranges.STEPTREE:
                for b in pr.permutations.STEPTREE:
                    b.buffer_size = end_swap_uint32(b.buffer_size)

        elif tag_cls == "spla":
            for noise_map in (
                    meta.spla_attrs.primary_noise_map,
                    meta.spla_attrs.secondary_noise_map
                    ):
                noise_map.unknown0 = end_swap_uint16(noise_map.unknown0)
                noise_map.unknown1 = end_swap_uint16(noise_map.unknown1)

        elif tag_cls == "ustr":
            # need to serialize the unicode strings reflexive back to the
            # endianness it was read as, and then byteswap the code-points 
            # of each character(NOTE: 12 is the end of the refelxive header)
            for b in meta.strings.STEPTREE:
                byteswap_anniversary_rawdata_ref(b, size=2, two_byte_offs=[0])

        if tag_cls in ("bipd", "vehi", "weap", "eqip", "garb", "proj",
                       "scen", "mach", "ctrl", "lifi", "plac", "ssce", "obje"):
            meta.obje_attrs.object_type.data = end_swap_int16(
                meta.obje_attrs.object_type.data
                )
        elif tag_cls in ("senv", "soso", "sotr", "schi", "scex",
                         "swat", "sgla", "smet", "spla", "shdr"):
            meta.shdr_attrs.shader_type.data = end_swap_int16(
                meta.shdr_attrs.shader_type.data
                )

    def inject_rawdata(self, meta, tag_cls, tag_index_ref):
        # TODO: Update this with extracting from sabre paks if 
        #       bitmap/sound/model extraction is ever implemented
        if tag_cls == "snd!":
            # audio samples are ALWAYS in fmod, so fill the with empty padding
            for pitches in meta.pitch_ranges.STEPTREE:
                for perm in pitches.permutations.STEPTREE:
                    for b in (perm.samples, perm.mouth_data, perm.subtitle_data):
                        b.data = b"\x00"*b.size
        elif tag_cls == "bitm":
            # bitmap pixels are ALWAYS in saber paks, so fill the with empty padding
            meta.compressed_color_plate_data.data = b"\x00"*meta.processed_pixel_data.size
            meta.processed_pixel_data.data = b"\x00"*meta.processed_pixel_data.size
        else:
            meta = super().inject_rawdata(meta, tag_cls, tag_index_ref)

        return meta

    def meta_to_tag_data(self, meta, tag_cls, tag_index_ref, **kwargs):
        # no bitmap pixels or sound samples in map. cant extract.
        # also, we don't know how to properly byteswap recorded
        # animations, so scenarios can't be extracted properly.
        if tag_cls == "bitm":
            raise ValueError("Bitmap pixel data missing.")
        elif tag_cls == "snd!":
            raise ValueError("Sound sample data missing.")

        kwargs["byteswap"] = False
        super().meta_to_tag_data(meta, tag_cls, tag_index_ref, **kwargs)

        return meta
