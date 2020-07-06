#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

import os

from copy import deepcopy
from math import pi, log
from pathlib import Path
from struct import unpack, pack_into
from traceback import format_exc
from types import MethodType

from supyr_struct.buffer import BytearrayBuffer
from supyr_struct.field_types import FieldType
from supyr_struct.defs.frozen_dict import FrozenDict

from reclaimer.halo_script.hsc import get_hsc_data_block,\
     HSC_IS_SCRIPT_OR_GLOBAL, SCRIPT_OBJECT_TYPES_TO_SCENARIO_REFLEXIVES
from reclaimer.common_descs import make_dependency_os_block
from reclaimer.hek.defs.snd_ import snd__meta_stub_blockdef
from reclaimer.hek.defs.sbsp import sbsp_meta_header_def
from reclaimer.os_hek.defs.gelc    import gelc_def
from reclaimer.os_v4_hek.defs.coll import fast_coll_def
from reclaimer.os_v4_hek.defs.sbsp import fast_sbsp_def
from reclaimer.os_v4_hek.handler   import OsV4HaloHandler
from reclaimer.meta.wrappers.byteswapping import raw_block_def, byteswap_animation,\
     byteswap_uncomp_verts, byteswap_comp_verts, byteswap_tris,\
     byteswap_coll_bsp, byteswap_sbsp_meta, byteswap_scnr_script_syntax_data,\
     byteswap_pcm16_samples
from reclaimer.meta.wrappers.halo_map import HaloMap
from reclaimer.meta.wrappers.halo1_rsrc_map import Halo1RsrcMap, inject_sound_data, get_is_xbox_map
from reclaimer.meta.wrappers.map_pointer_converter import MapPointerConverter
from reclaimer.meta.wrappers.tag_index_manager import TagIndexManager
from reclaimer import data_extraction
from reclaimer.constants import tag_class_fcc_to_ext
from reclaimer.util.compression import compress_normal32, decompress_normal32
from reclaimer.util import is_overlapping_ranges, is_valid_ascii_name_str,\
     int_to_fourcc

from supyr_struct.util import is_path_empty


__all__ = ("Halo1Map", "Halo1RsrcMap")


def reparse_reflexive(block, new_size, pointer_converter,
                      map_data, tag_index_manager):
    steptree = block.STEPTREE
    file_ptr = pointer_converter.v_ptr_to_f_ptr(block.pointer)

    if (file_ptr + new_size * steptree.get_desc("SIZE", 0) > len(map_data) or
        file_ptr <= 0):
        return

    # read the palette array from the map
    with FieldType.force_little:
        del steptree[:]
        steptree.extend(new_size)
        steptree.TYPE.parser(
            steptree.desc, node=steptree,
            map_pointer_converter=pointer_converter,
            rawdata=map_data, offset=file_ptr,
            safe_mode=False, parsing_resource=False,
            tag_index_manager=tag_index_manager)


class Halo1Map(HaloMap):
    '''Generation 1 map'''
    ce_rsrc_sound_indexes_by_path = None
    ce_tag_indexs_by_paths = None
    sound_rsrc_id = None
    defs = None

    tag_defs_module = "reclaimer.os_v4_hek.defs"
    tag_classes_to_load = tuple(sorted(tag_class_fcc_to_ext.keys()))

    handler_class = OsV4HaloHandler

    force_checksum = False

    inject_rawdata = Halo1RsrcMap.inject_rawdata

    bsp_magics  = ()
    bsp_sizes   = ()
    bsp_headers = ()
    bsp_header_offsets = ()
    bsp_pointer_converters = ()

    data_extractors = data_extraction.h1_data_extractors

    def __init__(self, maps=None):
        HaloMap.__init__(self, maps)

        self.resource_map_class = Halo1RsrcMap
        self.ce_rsrc_sound_indexes_by_path = {}
        self.ce_tag_indexs_by_paths = {}

        self.bsp_magics = {}
        self.bsp_sizes  = {}
        self.bsp_header_offsets = {}
        self.bsp_headers = {}
        self.bsp_pointer_converters = {}

        self.setup_tag_headers()

    @property
    def decomp_file_ext(self):
        if self.engine == "halo1yelo":
            return ".yelo"
        elif self.engine == "halo1vap":
            return ".vap"
        else:
            return ".map"

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
            this_class.defs["gelc"] = gelc_def
            this_class.defs["sbsp"] = fast_sbsp_def
            this_class.defs = FrozenDict(this_class.defs)

        # make a shallow copy for this instance to manipulate
        self.defs = dict(self.defs)

    def ensure_sound_maps_valid(self):
        sounds = self.maps.get("sounds")
        if not sounds or self.is_resource:
            return

        if id(sounds) == self.sound_rsrc_id and (
                self.ce_rsrc_sound_indexes_by_path and
                self.ce_tag_indexs_by_paths):
            return

        self.sound_rsrc_id = id(sounds)
        if self.engine in ("halo1ce", "halo1yelo", "halo1vap"):
            # ce resource sounds are recognized by tag_path
            # so we must cache their offsets by their paths
            rsrc_snd_map = self.ce_rsrc_sound_indexes_by_path = {}
            inv_snd_map  = self.ce_tag_indexs_by_paths = {}

            if sounds is not None:
                i = 0
                for tag_header in sounds.rsrc_map.data.tags:
                    rsrc_snd_map[tag_header.tag.path] = i
                    i += 1

            i = 0
            for tag_header in self.tag_index.tag_index:
                inv_snd_map[tag_header.path] = i
                i += 1

    def get_dependencies(self, meta, tag_id, tag_cls):
        tag_index_array = self.tag_index.tag_index
        if not self.is_indexed(tag_id):
            # not indexed. get dependencies like normal
            pass
        elif tag_cls != "snd!":
            # among the indexable tags, only sounds can have valid dependencies
            return ()
        elif not hasattr(meta, "pitch_ranges"):
            # tag is indexed AND we were provided with the indexed version
            rsrc_id = meta.promotion_sound.id & 0xFFff
            if rsrc_id == 0xFFFF: return ()

            sounds = self.maps.get("sounds")
            if   sounds is None: return ()
            elif rsrc_id >= len(sounds.tag_index.tag_index): return ()

            tag_path = sounds.tag_index.tag_index[rsrc_id].path
            inv_snd_map = getattr(self, 'ce_tag_indexs_by_paths', {})
            tag_id = inv_snd_map.get(tag_path, 0xFFFF)
            if tag_id >= len(tag_index_array): return ()

            ref = deepcopy(meta.promotion_sound)
            tag_index_ref = tag_index_array[tag_id]
            ref.tag_class.data = tag_index_ref.class_1.data
            ref.id             = tag_index_ref.id
            ref.filepath       = tag_index_ref.path

            return [ref]

        if self.handler is None: return ()

        dependency_cache = self.handler.tag_ref_cache.get(tag_cls)
        if not dependency_cache: return ()

        nodes = self.handler.get_nodes_by_paths(dependency_cache, (None, meta))
        dependencies = []

        for node in nodes:
            if node.id & 0xFFff == 0xFFFF:
                continue
            dependencies.append(node)

        if tag_cls == "scnr":
            # collect the tag references from the scenarios syntax data
            try:
                seen_tag_ids = set()
                syntax_data = get_hsc_data_block(meta.script_syntax_data.data)
                for node in syntax_data.nodes:
                    if (node.flags & HSC_IS_SCRIPT_OR_GLOBAL or
                        node.type not in range(24, 32)):
                        # not a tag index ref
                        continue

                    tag_index_id = node.data & 0xFFff
                    if (tag_index_id in range(len(tag_index_array)) and
                        tag_index_id not in seen_tag_ids):
                        seen_tag_ids.add(tag_index_id)
                        tag_index_ref = tag_index_array[tag_index_id]
                        dependencies.append(make_dependency_os_block(
                            tag_index_ref.class_1.enum_name, tag_index_ref.id,
                            tag_index_ref.path, tag_index_ref.path_offset))
            except Exception:
                pass

        return dependencies

    def setup_sbsp_pointer_converters(self):
        # get the scenario meta
        if self.scnr_meta is None:
            print("Cannot setup sbsp pointer converters without scenario tag.")
            return

        try:
            metadata_range = range(self.map_header.tag_index_header_offset,
                                   self.map_header.tag_index_header_offset +
                                   self.map_header.tag_data_size)
            invalid_bsp_tag_ids = [self.tag_index.scenario_tag_id & 0xFFff]
            i = 0
            for b in self.scnr_meta.structure_bsps.STEPTREE:
                bsp_id = b.structure_bsp.id & 0xFFff

                # these checks are necessary because apparently these structs
                # can be super fucked up, and might not affect anything
                if (bsp_id not in range(len(self.tag_index.tag_index)) or
                    bsp_id in invalid_bsp_tag_ids):
                    print("Scenario structure_bsp %s contains invalid tag_id." % i)
                elif is_overlapping_ranges(
                        metadata_range, range(b.bsp_pointer, b.bsp_size)):
                    print("Scenario structure_bsp %s contains invalid pointer." % i)
                elif self.tag_index.tag_index[bsp_id].id != b.structure_bsp.id:
                    print("Scenario structure_bsp %s contains invalid tag_id." % i)
                else:
                    self.bsp_header_offsets[bsp_id] = b.bsp_pointer
                    self.bsp_magics[bsp_id]         = b.bsp_magic
                    self.bsp_sizes[bsp_id]          = b.bsp_size

                    self.bsp_pointer_converters[bsp_id] = MapPointerConverter(
                        (b.bsp_magic, b.bsp_pointer, b.bsp_size)
                        )

                i += 1

            # read the sbsp headers
            for tag_id, offset in self.bsp_header_offsets.items():
                if self.engine == "halo1anni":
                    with FieldType.force_big:
                        header = sbsp_meta_header_def.build(
                            rawdata=self.map_data, offset=offset)
                else:
                    header = sbsp_meta_header_def.build(
                        rawdata=self.map_data, offset=offset)

                if header.sig != header.get_desc("DEFAULT", "sig"):
                    print("Sbsp header is invalid for '%s'" %
                          self.tag_index.tag_index[tag_id].path)
                self.bsp_headers[tag_id] = header
                self.tag_index.tag_index[tag_id].meta_offset = header.meta_pointer

        except Exception:
            print(format_exc())

    def load_map(self, map_path, **kwargs):
        HaloMap.load_map(self, map_path, **kwargs)

        tag_index = self.tag_index
        tag_index_array = tag_index.tag_index

        # cache the original paths BEFORE running basic deprotection
        self.cache_original_tag_paths()

        # make all contents of the map parseable
        self.basic_deprotection()

        self.tag_index_manager = TagIndexManager(tag_index_array)

        # add the tag data section
        self.map_pointer_converter.add_page_info(
            self.index_magic, self.map_header.tag_index_header_offset,
            self.map_header.tag_data_size
            )

        # cache the scenario meta
        try:
            self.scnr_meta = self.get_meta(self.tag_index.scenario_tag_id)
            if self.scnr_meta is None:
                print("Could not read scenario tag")
        except Exception:
            print(format_exc())
            print("Could not read scenario tag")

        self.setup_sbsp_pointer_converters()

        last_bsp_end = 0
        # calculate the start of the rawdata section
        for tag_id in self.bsp_headers:
            bsp_end = self.bsp_header_offsets[tag_id] + self.bsp_sizes[tag_id]
            if last_bsp_end < bsp_end:
                last_bsp_end = bsp_end

        # add the rawdata section
        self.map_pointer_converter.add_page_info(
            last_bsp_end, last_bsp_end,
            tag_index.model_data_offset - last_bsp_end,
            )

        # add the model data section
        if tag_index.SIZE == 40:
            # PC tag index
            self.map_pointer_converter.add_page_info(
                0, tag_index.model_data_offset,
                tag_index.model_data_size,
                )
        else:
            # XBOX tag index
            self.map_pointer_converter.add_page_info(
                0, tag_index.model_data_offset,
                (self.map_header.tag_index_header_offset -
                 tag_index.model_data_offset),
                )

        # get the globals meta
        try:
            matg_id = None
            for b in tag_index_array:
                if int_to_fourcc(b.class_1.data) == "matg":
                    matg_id = b.id & 0xFFff
                    break

            self.matg_meta = self.get_meta(matg_id)
            if self.matg_meta is None:
                print("Could not read globals tag")
        except Exception:
            print(format_exc())
            print("Could not read globals tag")

        if self.map_name == "sounds":
            for halo_map in self.maps.values():
                if hasattr(halo_map, "ensure_sound_maps_valid"):
                    halo_map.ensure_sound_maps_valid()

        self.clear_map_cache()

    def get_meta(self, tag_id, reextract=False, ignore_rsrc_sounds=False, **kw):
        '''
        Takes a tag reference id as the sole argument.
        Returns that tags meta data as a parsed block.
        '''
        if tag_id is None:
            return

        magic     = self.map_magic
        engine    = self.engine
        map_data  = self.map_data
        tag_index = self.tag_index
        tag_index_array = tag_index.tag_index

        # if we are given a 32bit tag id, mask it off
        tag_id &= 0xFFFF
        tag_index_ref = self.tag_index_manager.get_tag_index_ref(tag_id)
        if tag_index_ref is None:
            return

        tag_cls = None
        if tag_id == (tag_index.scenario_tag_id & 0xFFFF):
            tag_cls = "scnr"
        elif tag_index_ref.class_1.enum_name not in ("<INVALID>", "NONE"):
            tag_cls = int_to_fourcc(tag_index_ref.class_1.data)

        # if we dont have a defintion for this tag_cls, then return nothing
        if self.get_meta_descriptor(tag_cls) is None:
            return

        self.ensure_sound_maps_valid()
        pointer_converter = self.bsp_pointer_converters.get(
            tag_id, self.map_pointer_converter)
        offset = tag_index_ref.meta_offset

        if tag_cls is None:
            # couldn't determine the tag class
            return
        elif self.is_indexed(tag_id) and (
                tag_cls != "snd!" or not ignore_rsrc_sounds):
            # tag exists in a resource cache
            tag_id = offset

            rsrc_map = None
            if tag_cls == "snd!" and "sounds" in self.maps:
                rsrc_map = self.maps["sounds"]
                sound_mapping = self.ce_rsrc_sound_indexes_by_path
                tag_path = tag_index_ref.path
                if sound_mapping is None or tag_path not in sound_mapping:
                    return

                tag_id = sound_mapping[tag_path]//2

            elif tag_cls == "bitm" and "bitmaps" in self.maps:
                rsrc_map = self.maps["bitmaps"]
                tag_id = tag_id//2

            elif "loc" in self.maps:
                rsrc_map = self.maps["loc"]
                # this resource tag COULD be in a yelo loc.map, which
                # means we will need to set its tag class to what this
                # map specifies it as or else the resource map wont
                # know what type of tag to extract it as.
                rsrc_map.tag_index.tag_index[tag_id].class_1.set_to(
                    tag_index_ref.class_1.enum_name)

            if rsrc_map is None:
                return

            meta = rsrc_map.get_meta(tag_id, **kw)
            if tag_cls == "snd!":
                # since we're reading the resource tag from the perspective of
                # the map referencing it, we have more accurate information
                # about which other sound it could be referencing. This is only
                # a concern when dealing with open sauce resource maps, as they
                # could have additional promotion sounds we cant statically map
                try:
                    # read the meta data from the map
                    with FieldType.force_little:
                        snd_stub = snd__meta_stub_blockdef.build(
                            rawdata=map_data,
                            offset=pointer_converter.v_ptr_to_f_ptr(offset),
                            tag_index_manager=self.tag_index_manager)
                    meta.promotion_sound = snd_stub.promotion_sound
                except Exception:
                    print(format_exc())

            return meta
        elif not reextract:
            if tag_id == tag_index.scenario_tag_id & 0xFFff and self.scnr_meta:
                return self.scnr_meta
            elif tag_cls == "matg" and self.matg_meta:
                return self.matg_meta

        force_parsing_rsrc = False
        if tag_cls in ("antr", "magy") and not kw.get("disable_tag_cleaning"):
            force_parsing_rsrc = True

        desc = self.get_meta_descriptor(tag_cls)
        block = [None]
        try:
            # read the meta data from the map
            with FieldType.force_little:
                desc['TYPE'].parser(
                    desc, parent=block, attr_index=0, rawdata=map_data,
                    map_pointer_converter=pointer_converter,
                    offset=pointer_converter.v_ptr_to_f_ptr(offset),
                    tag_index_manager=self.tag_index_manager,
                    safe_mode=not kw.get("disable_safe_mode"),
                    parsing_resource=force_parsing_rsrc)
        except Exception:
            print(format_exc())
            if not kw.get("allow_corrupt"):
                return

        meta = block[0]
        try:
            if tag_cls == "bitm" and get_is_xbox_map(engine):
                for bitmap in meta.bitmaps.STEPTREE:
                    # make sure to set this for all xbox bitmaps
                    # so they can be interpreted properly
                    bitmap.base_address = 1073751810

            self.record_map_cache_read(tag_id, 0)
            if self.map_cache_over_limit():
                self.clear_map_cache()

            if not kw.get("ignore_rawdata", False):
                self.inject_rawdata(meta, tag_cls, tag_index_ref)
        except Exception:
            print(format_exc())
            if not kw.get("allow_corrupt"):
                meta = None

        if not kw.get("disable_tag_cleaning"):
            try:
                self.clean_tag_meta(meta, tag_id, tag_cls)
            except Exception:
                print(format_exc())

        return meta

    def clean_tag_meta(self, meta, tag_id, tag_cls):
        tag_index_array = self.tag_index.tag_index

        if tag_cls in ("antr", "magy"):
            highest_valid = -1
            found_valid = False
            animations = meta.animations.STEPTREE
            main_node_count = animations[0].node_count if animations else 0
            main_node_list_checksum = animations[0].node_list_checksum if animations else 0

            permutation_chains = {}
            for i in range(len(animations)):
                if i in permutation_chains:
                    continue

                permutation_chains[i] = i
                next_anim = animations[i].next_animation
                while (next_anim in range(len(animations)) and
                       next_anim not in permutation_chains):
                    permutation_chains[next_anim] = i
                    next_anim = animations[next_anim].next_animation

            anims_to_remove = []

            for i in range(len(animations)):
                if self.engine != "halo1yelo" and i >= 256:
                    # cap it to the non-OS limit of 256 animations
                    break

                anim = animations[i]
                valid = is_valid_ascii_name_str(anim.name)

                trans_int = anim.trans_flags0 + (anim.trans_flags1 << 32)
                rot_int   = anim.rot_flags0   + (anim.rot_flags1   << 32)
                scale_int = anim.scale_flags0 + (anim.scale_flags1 << 32)

                trans_flags = (bool(trans_int & (1 << i))
                               for i in range(anim.node_count))
                rot_flags   = (bool(rot_int   & (1 << i))
                               for i in range(anim.node_count))
                scale_flags = (bool(scale_int & (1 << i))
                               for i in range(anim.node_count))

                expected_frame_size = (12 * sum(trans_flags) +
                                       8  * sum(rot_flags) +
                                       4  * sum(scale_flags))
                expected_frame_info_size = {1: 8, 2: 12, 3: 16}.get(
                    anim.frame_info_type.data, 0) * anim.frame_count
                expected_frame_data_size = expected_frame_size * anim.frame_count
                expected_default_data_size = (
                    anim.node_count * (12 + 8 + 4) - anim.frame_size)

                if anim.frame_count == 0:
                    expected_default_data_size = 0

                if (anim.type.enum_name == "<INVALID>" or
                    anim.frame_info_type.enum_name == "<INVALID>"):
                    valid = False
                elif (anim.node_count != main_node_count or
                      anim.node_count not in range(1, 65)):
                    valid = False
                elif anim.first_permutation_index != permutation_chains[i]:
                    valid = False
                elif not anim.flags.compressed_data:
                    if anim.default_data.size < expected_default_data_size:
                        valid = False
                    elif anim.frame_info.size < expected_frame_info_size:
                        valid = False
                    elif anim.frame_data.size < expected_frame_data_size:
                        valid = False
                    elif anim.frame_size != expected_frame_size:
                        valid = False
                elif anim.offset_to_compressed_data >= anim.frame_data.size:
                    valid = False

                if valid:
                    highest_valid = i
                    if not found_valid:
                        main_node_count = anim.node_count
                        main_node_list_checksum = anim.node_list_checksum
                        found_valid = True
                else:
                    # delete the animation info
                    anims_to_remove.append(i)

            # make sure all animations have the same node count, checksum, and a name
            for i in anims_to_remove:
                animations.pop(i)
                animations.insert(i)
                animations[i].node_count = main_node_count
                animations[i].node_list_checksum = main_node_list_checksum
                animations[i].name = "REMOVED_%s" % i

            # remove the highest invalid animations
            if highest_valid + 1 < len(animations):
                del animations[highest_valid + 1: ]

            # inject the animation data for all remaining animations since
            # it's not safe to try and read it all at parse time
            for anim in animations:
                for block in (anim.default_data, anim.frame_info, anim.frame_data):
                    if not block.size:
                        continue

                    file_ptr = self.map_pointer_converter.v_ptr_to_f_ptr(
                        block.pointer)
                    if not block.pointer or file_ptr < 0:
                        file_ptr = block.raw_pointer

                    if file_ptr + block.size > len(self.map_data) or file_ptr <= 0:
                        continue

                    try:
                        self.map_data.seek(file_ptr)
                        block.data = bytearray(self.map_data.read(block.size))
                    except Exception:
                        print("Couldn't read animation data.")

        elif tag_cls in ("sbsp", "coll"):
            if tag_cls == "sbsp" :
                bsps = meta.collision_bsp.STEPTREE
            else:
                bsps = []
                for node in meta.nodes.STEPTREE:
                    bsps.extend(node.bsps.STEPTREE)

            for bsp in bsps:
                highest_used_vert = -1
                edge_data = bsp.edges.STEPTREE
                vert_data = bsp.vertices.STEPTREE
                for i in range(0, len(edge_data), 24):
                    v0_i = (edge_data[i] +
                            (edge_data[i + 1] << 8) +
                            (edge_data[i + 2] << 16) +
                            (edge_data[i + 3] << 24))
                    v1_i = (edge_data[i + 4] +
                            (edge_data[i + 5] << 8) +
                            (edge_data[i + 6] << 16) +
                            (edge_data[i + 7] << 24))
                    highest_used_vert = max(highest_used_vert, v0_i, v1_i)

                if highest_used_vert * 16 < len(vert_data):
                    del vert_data[(highest_used_vert + 1) * 16: ]
                    bsp.vertices.size = highest_used_vert + 1

        elif tag_cls in ("mode", "mod2"):
            used_shaders = set()
            shaders = meta.shaders.STEPTREE

            for geom in meta.geometries.STEPTREE:
                for part in geom.parts.STEPTREE:
                    if part.shader_index >= 0:
                        used_shaders.add(part.shader_index)

            # determine the max number of shader indices actually used
            # by all the geometry parts, and reparse them with that many.
            if used_shaders:
                try:
                    reparse_reflexive(
                        meta.shaders, max(used_shaders) + 1,
                        self.map_pointer_converter,
                        self.map_data, self.tag_index_manager)
                except Exception:
                    print(format_exc())
                    print("Couldn't re-parse %s data." % meta.shaders)

            new_i = 0
            rebase_map = {}
            new_shaders = [None] * len(used_shaders)
            for i in sorted(used_shaders):
                new_shaders[new_i] = shaders[i]
                rebase_map[i] = new_i
                new_i += 1

            # rebase the shader indices
            for geom in meta.geometries.STEPTREE:
                for part in geom.parts.STEPTREE:
                    if part.shader_index in range(len(shaders)):
                        part.shader_index = rebase_map[part.shader_index]
                    else:
                        part.shader_index = -1

            shaders[:] = new_shaders

        elif tag_cls == "scnr":
            skies = meta.skies.STEPTREE
            comments = meta.comments.STEPTREE

            highest_valid_sky = -1
            for i in range(len(skies)):
                sky = skies[i].sky
                sky_tag_index_id = sky.id & 0xFFff
                if (sky_tag_index_id not in range(len(tag_index_array)) or
                    tag_index_array[sky_tag_index_id].id != sky.id):
                    # invalid sky
                    sky.id = 0xFFffFFff
                    sky.filepath = ""
                    sky.tag_class.set_to("sky")
                else:
                    highest_valid_sky = i

            # clear the highest invalid skies
            del skies[highest_valid_sky + 1: ]

            # clear the child scenarios since they aren't used
            del meta.child_scenarios.STEPTREE[:]

            # determine if there are any fucked up comments
            comments_to_keep = set()
            for i in range(len(comments)):
                comment = comments[i]
                if max(max(comment.position), abs(min(comment.position))) > 5000:
                    # check if the position is outside halos max world bounds
                    continue

                if not (comment.comment_data.data and
                        is_valid_ascii_name_str(comment.comment_data.data)):
                    comments_to_keep.add(i)

            if len(comments_to_keep) != len(comments):
                # clean up any fucked up comments
                comments[:] = [comments[i] for i in sorted(comments_to_keep)]

            syntax_data = get_hsc_data_block(meta.script_syntax_data.data)
            script_nodes_modified = False

            # clean up any fucked up palettes
            for pal_block, inst_block in (
                    (meta.sceneries_palette, meta.sceneries),
                    (meta.bipeds_palette, meta.bipeds),
                    (meta.vehicles_palette, meta.vehicles),
                    (meta.equipments_palette, meta.equipments),
                    (meta.weapons_palette, meta.weapons),
                    (meta.machines_palette, meta.machines),
                    (meta.controls_palette, meta.controls),
                    (meta.light_fixtures_palette, meta.light_fixtures),
                    (meta.sound_sceneries_palette, meta.sound_sceneries),
                    ):
                palette, instances = pal_block.STEPTREE, inst_block.STEPTREE

                used_pal_indices = set(inst.type for inst in instances
                                       if inst.type >= 0)
                script_nodes_to_modify = set()

                if inst_block.NAME == "bipeds":
                    # determine which palette indices are used by script data
                    for i in range(len(syntax_data.nodes)):
                        node = syntax_data.nodes[i]
                        # 35 == "actor_type"  script type
                        if node.type == 35 and not(node.flags & HSC_IS_SCRIPT_OR_GLOBAL):
                            script_nodes_to_modify.add(i)
                            used_pal_indices.add(node.data & 0xFFff)

                # determine the max number of palette indices actually used by all
                # the object instances, and reparse the palette with that many.
                if used_pal_indices:
                    try:
                        reparse_reflexive(
                            pal_block, max(used_pal_indices) + 1,
                            self.map_pointer_converter,
                            self.map_data, self.tag_index_manager)
                    except Exception:
                        print(format_exc())
                        print("Couldn't re-parse %s data." % pal_block.NAME)

                # figure out what to rebase the palette swatch indices to
                new_i = 0
                rebase_map = {}
                new_palette = [None] * len(used_pal_indices)
                for i in sorted(used_pal_indices):
                    new_palette[new_i] = palette[i]
                    rebase_map[i] = new_i
                    new_i += 1

                # rebase the palette indices of the instances and
                # move the palette swatches into their new indices
                for inst in instances:
                    if inst.type in range(len(instances)):
                        inst.type = rebase_map[inst.type]
                    else:
                        inst.type = -1

                palette[:] = new_palette

                # modify the script syntax nodes that need to be
                for i in script_nodes_to_modify:
                    node = syntax_data.nodes[i]
                    salt = node.data & 0xFFff0000
                    cur_index = node.data & 0xFFff
                    new_index = rebase_map[cur_index]
                    if cur_index != new_index:
                        script_nodes_modified = True
                        node.data = salt + new_index

            # replace the script syntax data
            if script_nodes_modified:
                with FieldType.force_little:
                    new_script_data = syntax_data.serialize()
                    meta.script_syntax_data.data[: len(new_script_data)] = new_script_data
                    meta.script_syntax_data.size = len(meta.script_syntax_data.data)

        elif tag_cls in ("tagc", "Soul"):
            tag_collection = meta[0].STEPTREE
            highest_valid = -1
            for i in range(len(tag_collection)):
                tag_ref = tag_collection[i][0]
                if tag_cls == "Soul" and tag_ref.tag_class.enum_name != "ui_widget_definition":
                    continue
                elif (tag_ref.id & 0xFFff) not in range(len(tag_index_array)):
                    continue
                elif tag_index_array[tag_ref.id & 0xFFff].id != tag_ref.id:
                    continue

                highest_valid = i

            # clear the highest invalid entries
            del tag_collection[highest_valid + 1: ]

    def meta_to_tag_data(self, meta, tag_cls, tag_index_ref, **kwargs):
        magic      = self.map_magic
        engine     = self.engine
        map_data   = self.map_data
        tag_index  = self.tag_index
        byteswap = kwargs.get("byteswap", True)

        predicted_resources = []

        if hasattr(meta, "obje_attrs"):
            predicted_resources.append(meta.obje_attrs.predicted_resources)

            # fix the change colors permutations
            for change_color in meta.obje_attrs.change_colors.STEPTREE:
                cutoff = 0
                for perm in change_color.permutations.STEPTREE:
                    perm.weight, cutoff = perm.weight - cutoff, perm.weight


        if tag_cls == "actv":
            # multiply grenade velocity by 30
            meta.grenades.grenade_velocity *= 30

        elif tag_cls in ("antr", "magy"):
            # byteswap animation data
            for anim in meta.animations.STEPTREE:
                if not byteswap: break
                byteswap_animation(anim)

        elif tag_cls == "bitm":
            # set the size of the compressed plate data to nothing
            meta.compressed_color_plate_data.STEPTREE = BytearrayBuffer()

            # to enable compatibility with my bitmap converter we'll set the
            # base address to a certain constant based on the console platform
            is_xbox = get_is_xbox_map(engine)

            new_pixels_offset = 0

            # uncheck the prefer_low_detail flag and
            # set up the pixels_offset correctly.
            for bitmap in meta.bitmaps.STEPTREE:
                bitmap.flags.prefer_low_detail = is_xbox
                bitmap.pixels_offset = new_pixels_offset
                new_pixels_offset += bitmap.pixels_meta_size

                # clear some meta-only fields
                bitmap.pixels_meta_size = 0
                bitmap.bitmap_id_unknown1 = bitmap.bitmap_id_unknown2 = 0
                bitmap.bitmap_data_pointer = 0

                if is_xbox:
                    bitmap.base_address = 1073751810
                    if "dxt" in bitmap.format.enum_name:
                        # need to correct mipmap count on xbox dxt bitmaps.
                        # the game seems to prune the mipmap texels for any
                        # mipmaps whose dimensions are 2x2 or smaller

                        max_dim = max(bitmap.width, bitmap.height)
                        if 2 ** bitmap.mipmaps > max_dim:
                            # make sure the mipmap level isnt higher than the
                            # number of mipmaps that should be able to exist.
                            bitmap.mipmaps = int(log(max_dim, 2))

                        last_mip_dim = max_dim // (2 ** bitmap.mipmaps)
                        if last_mip_dim == 1:
                            bitmap.mipmaps -= 2
                        elif last_mip_dim == 2:
                            bitmap.mipmaps -= 1

                        if bitmap.mipmaps < 0:
                            bitmap.mipmaps = 0
                else:
                    bitmap.base_address = 0

        elif tag_cls == "cdmg":
            # divide camera shaking wobble period by 30
            meta.camera_shaking.wobble_function_period /= 30

        elif tag_cls == "coll":
            # byteswap the raw bsp collision data
            for node in meta.nodes.STEPTREE:
                for perm_bsp in node.bsps.STEPTREE:
                    if not byteswap: break
                    byteswap_coll_bsp(perm_bsp)

        elif tag_cls == "effe":
            # mask away the meta-only flags
            meta.flags.data &= 3
            for event in meta.events.STEPTREE:
                # tool exceptions if any parts reference a damage effect
                # tag type, but have an empty filepath for the reference
                parts = event.parts.STEPTREE
                for i in range(len(parts) - 1, -1, -1):
                    part = parts[i]
                    if (part.type.tag_class.enum_name == "damage_effect" and
                        not part.type.filepath):
                        parts.pop(i)

        elif tag_cls == "jpt!":
            # camera shaking wobble period by 30
            meta.camera_shaking.wobble_function_period /= 30

        elif tag_cls == "glw!":
            # increment enumerators properly
            for b in (meta.particle_rotational_velocity,
                      meta.effect_rotational_velocity,
                      meta.effect_translational_velocity,
                      meta.particle_distance_to_object,
                      meta.particle_size,
                      meta.particle_color):
                b.attachment.data += 1

        elif tag_cls == "lens":
            # DON'T multiply corona rotation by pi/180
            # reminder that this is not supposed to be changed
            pass # meta.corona_rotation.function_scale *= pi/180

        elif tag_cls == "ligh":
            # divide light time by 30
            meta.effect_parameters.duration /= 30

        elif tag_cls == "matg":
            # tool will fail to compile any maps if the
            # multiplayer_info or falling_damage is blank

            # make sure there is multiplayer info.
            multiplayer_info = meta.multiplayer_informations.STEPTREE
            if not len(multiplayer_info):
                multiplayer_info.append()

            # make sure there is falling damage info.
            falling_damages = meta.falling_damages.STEPTREE
            if not len(falling_damages):
                falling_damages.append()

        elif tag_cls == "metr":
            # The meter bitmaps can literally point to not
            # only the wrong tag, but the wrong TYPE of tag.
            # Since dependencies in meter tags are useless, we null them out.
            meta.stencil_bitmap.filepath = meta.source_bitmap.filepath = ''

        elif tag_cls in ("mode", "mod2"):
            if engine in ("halo1yelo", "halo1ce", "halo1pc", "halo1vap",
                          "halo1anni", "halo1pcdemo", "stubbspc"):
                # model_magic seems to be the same for all pc maps
                verts_start = tag_index.model_data_offset
                tris_start  = verts_start + tag_index.vertex_data_size
                model_magic = None
            else:
                model_magic = magic

            if model_magic is None:
                verts_attr_name = "uncompressed_vertices"
                byteswap_verts = byteswap_uncomp_verts
                vert_size = 68

                if engine != "stubbspc":
                    # need to swap the lod cutoff and nodes values around
                    cutoffs = (meta.superlow_lod_cutoff, meta.low_lod_cutoff,
                               meta.high_lod_cutoff, meta.superhigh_lod_cutoff)
                    meta.superlow_lod_cutoff  = cutoffs[3]
                    meta.low_lod_cutoff       = cutoffs[2]
                    meta.high_lod_cutoff      = cutoffs[1]
                    meta.superhigh_lod_cutoff = cutoffs[0]

            else:
                verts_attr_name = "compressed_vertices"
                byteswap_verts = byteswap_comp_verts
                vert_size = 32

            # If this is a gbxmodel localize the markers.
            # We skip this for xbox models for arsenic.

            if tag_cls == "mod2":
                # ensure all local marker arrays are empty
                for region in meta.regions.STEPTREE:
                    for perm in region.permutations.STEPTREE:
                        del perm.local_markers.STEPTREE[:]

                # localize the global markers
                for g_marker in meta.markers.STEPTREE:
                    for g_marker_inst in g_marker.marker_instances.STEPTREE:
                        try:
                            region = meta.regions.STEPTREE[g_marker_inst.region_index]
                        except IndexError:
                            print("Model marker instance for", g_marker.name, "has invalid region index", g_marker_inst.region_index, "and is skipped.")
                            continue

                        try:
                            perm = region.permutations.STEPTREE[g_marker_inst.permutation_index]
                        except IndexError:
                            print("Model marker instance for", g_marker.name, "has invalid permutation index", g_marker_inst.permutation_index, "and is skipped.")
                            continue

                        # make a new local marker
                        perm.local_markers.STEPTREE.append()
                        l_marker = perm.local_markers.STEPTREE[-1]

                        # copy the global marker into the local
                        l_marker.name           = g_marker.name
                        l_marker.node_index     = g_marker_inst.node_index
                        l_marker.translation[:] = g_marker_inst.translation[:]
                        l_marker.rotation[:]    = g_marker_inst.rotation[:]

                # clear the global markers
                del meta.markers.STEPTREE[:]

            # grab vertices and indices from the map
            for geom in meta.geometries.STEPTREE:
                for part in geom.parts.STEPTREE:
                    verts_block = part[verts_attr_name]
                    tris_block  = part.triangles
                    info  = part.model_meta_info

                    # null out certain things in the part
                    part.previous_part_index = part.next_part_index = 0
                    part.centroid_primary_node = 0
                    part.centroid_secondary_node = 0
                    part.centroid_primary_weight = 0.0
                    part.centroid_secondary_weight = 0.0

                    # make the new blocks to hold the raw data
                    verts_block.STEPTREE = raw_block_def.build()
                    tris_block.STEPTREE  = raw_block_def.build()

                    # read the offsets of the vertices and indices from the map
                    if engine == "stubbspc":
                        verts_off = verts_start + info.vertices_reflexive_offset
                        tris_off  = tris_start  + info.indices_reflexive_offset
                    elif model_magic is None:
                        verts_off = verts_start + info.vertices_offset
                        tris_off  = tris_start  + info.indices_offset
                    else:
                        map_data.seek(
                            info.vertices_reflexive_offset + 4 - model_magic)
                        verts_off = unpack(
                            "<I", map_data.read(4))[0] - model_magic
                        map_data.seek(
                            info.indices_reflexive_offset  + 4 - model_magic)
                        tris_off  = unpack(
                            "<I", map_data.read(4))[0] - model_magic

                    # read the raw data from the map
                    map_data.seek(verts_off)
                    raw_verts = map_data.read(vert_size*info.vertex_count)
                    map_data.seek(tris_off)
                    raw_tris  = map_data.read(2*(info.index_count + 2))

                    # append the padding indices to the triangle strip
                    if len(raw_tris)%6 == 2:
                        raw_tris += b'\xff\xff\xff\xff'
                    elif len(raw_tris)%6 == 4:
                        raw_tris += b'\xff\xff'

                    # put the raw data in the verts and tris blocks
                    verts_block.STEPTREE.data = raw_verts
                    tris_block.STEPTREE.data  = raw_tris

                    # call the byteswappers
                    if byteswap:
                        byteswap_verts(verts_block)
                        byteswap_tris(tris_block)

                    # set the size of the reflexives
                    # this is NOT redundant. anniversary maps wont byteswap,
                    # so the size setting occuring in the byteswap wont happen.
                    verts_block.size = len(verts_block.STEPTREE.data) // vert_size
                    tris_block.size  = len(tris_block.STEPTREE.data) // 6

                    # null out the model_meta_info
                    for i in range(len(info)):
                        if isinstance(info[i], int):
                            info[i] = 0

        elif tag_cls == "pphy":
            # set the meta-only values to 0
            meta.scaled_density = 0
            meta.water_gravity_scale = 0
            meta.air_gravity_scale = 0

            # scale friction values
            meta.air_friction /= 10000
            meta.water_friction /= 10000

        elif tag_cls == "proj":
            # need to scale velocities by 30
            meta.proj_attrs.physics.initial_velocity *= 30
            meta.proj_attrs.physics.final_velocity *= 30

        elif tag_cls == "sbsp":
            if byteswap:
                byteswap_sbsp_meta(meta)

            # null out the runtime decals
            del meta.runtime_decals.STEPTREE[:]

            for cluster in meta.clusters.STEPTREE:
                predicted_resources.append(cluster.predicted_resources)

            compressed = "xbox" in engine or engine in ("stubbs", "shadowrun_proto")

            if compressed:
                generate_verts = kwargs.get("generate_uncomp_verts", False)
            else:
                generate_verts = kwargs.get("generate_comp_verts", False)

            endian = "<"
            if engine == "halo1anni":
                endian = ">"

            comp_norm   = compress_normal32
            decomp_norm = decompress_normal32

            comp_vert_nbt_unpacker = MethodType(unpack, endian + "3I")
            uncomp_vert_nbt_packer = MethodType(pack_into, endian + "12s9f8s")

            comp_vert_nuv_unpacker = MethodType(unpack, endian + "I2h")
            uncomp_vert_nuv_packer = MethodType(pack_into, endian + "5f")

            uncomp_vert_nbt_unpacker = MethodType(unpack, endian + "9f")
            comp_vert_nbt_packer = MethodType(pack_into, endian + "12s3I8s")

            uncomp_vert_nuv_unpacker = MethodType(unpack, endian + "5f")
            comp_vert_nuv_packer = MethodType(pack_into, endian + "I2h")

            for lightmap in meta.lightmaps.STEPTREE:
                for b in lightmap.materials.STEPTREE:
                    # need to null these or switching bsps will crash sapien
                    b.unknown_meta_offset0 = b.unknown_meta_offset1 = 0
                    b.vertices_meta_offset = 0
                    b.lightmap_vertices_meta_offset = 0
                    b.vertex_type.data = 0

                    if not generate_verts:
                        continue

                    vert_count = b.vertices_count
                    lightmap_vert_count = b.lightmap_vertices_count

                    u_verts = b.uncompressed_vertices
                    c_verts = b.compressed_vertices

                    if compressed:
                        # generate uncompressed vertices from the compressed
                        comp_buffer   = c_verts.STEPTREE
                        uncomp_buffer = bytearray(56*vert_count +
                                                  20*lightmap_vert_count)
                        in_off  = 0
                        out_off = 0
                        for i in range(vert_count):
                            n, b, t = comp_vert_nbt_unpacker(
                                comp_buffer[in_off + 12: in_off + 24])

                            # write the uncompressed data
                            uncomp_vert_nbt_packer(
                                uncomp_buffer, out_off,
                                comp_buffer[in_off: in_off + 12],
                                *decomp_norm(n),
                                *decomp_norm(b),
                                *decomp_norm(t),
                                comp_buffer[in_off + 24: in_off + 32])

                            in_off  += 32
                            out_off += 56

                        for i in range(lightmap_vert_count):
                            n, u, v = comp_vert_nuv_unpacker(
                                comp_buffer[in_off: in_off + 8])
                            # write the uncompressed data
                            uncomp_vert_nuv_packer(
                                uncomp_buffer, out_off,
                                *decomp_norm(n), u/32767, v/32767)

                            in_off  += 8
                            out_off += 20
                    else:
                        # generate compressed vertices from uncompressed
                        uncomp_buffer = u_verts.STEPTREE
                        comp_buffer   = bytearray(32*vert_count +
                                                  8*lightmap_vert_count)

                        in_off  = 0
                        out_off = 0
                        # for speed purposes, we'll assume all vectors
                        # are already normalized to a length of ~1.0
                        for i in range(vert_count):
                            ni, nj, nk, bi, bj, bk, ti, tj, tk = \
                                uncomp_vert_nbt_unpacker(
                                    uncomp_buffer[in_off + 12: in_off + 48])

                            # write the compressed data
                            comp_vert_nbt_packer(
                                comp_buffer, out_off,
                                uncomp_buffer[in_off: in_off + 12],
                                comp_norm(ni, nj, nk),
                                comp_norm(bi, bj, bk),
                                comp_norm(ti, tj, tk),
                                uncomp_buffer[in_off + 48: in_off + 56])

                            in_off  += 56
                            out_off += 32

                        for i in range(lightmap_vert_count):
                            ni, nj, nk, u, v = uncomp_vert_nuv_unpacker(
                                uncomp_buffer[in_off: in_off + 20])

                            # write the compressed data
                            comp_vert_nuv_packer(
                                comp_buffer, out_off,
                                comp_norm(ni, nj, nk),
                                int(min(max(u, -1.0), 1.0)*32767),
                                int(min(max(v, -1.0), 1.0)*32767))

                            in_off  += 20
                            out_off += 8

                    # replace the buffers
                    u_verts.STEPTREE = uncomp_buffer
                    c_verts.STEPTREE = comp_buffer

        elif tag_cls == "scnr":
            # need to remove the references to the child scenarios
            del meta.child_scenarios.STEPTREE[:]

            # set the bsp pointers and stuff to 0
            for b in meta.structure_bsps.STEPTREE:
                b.bsp_pointer = b.bsp_size = b.bsp_magic = 0

            predicted_resources.append(meta.predicted_resources)

            # byteswap the script syntax data
            if byteswap:
                byteswap_scnr_script_syntax_data(meta)

            # rename duplicate stuff that causes errors when compiling scripts
            if kwargs.get("rename_scnr_dups", False):
                string_data = meta.script_string_data.data.decode("latin-1")
                syntax_data = get_hsc_data_block(raw_syntax_data=meta.script_syntax_data.data)

                # NOTE: For a list of all the script object types
                # with their corrosponding enum value, check
                #     reclaimer.enums.script_object_types
                keep_these = {i: set() for i in
                              SCRIPT_OBJECT_TYPES_TO_SCENARIO_REFLEXIVES}
                for b in meta.bsp_switch_trigger_volumes.STEPTREE:
                    keep_these[11].add(b.trigger_volume)

                for i in range(min(syntax_data.last_node, len(syntax_data.nodes))):
                    node = syntax_data.nodes[i]
                    if node.type not in keep_these:
                        continue

                    keep_these[node.type].add(node.data & 0xFFff)

                for script_object_type, reflexive_name in \
                        SCRIPT_OBJECT_TYPES_TO_SCENARIO_REFLEXIVES.items():
                    keep = keep_these[script_object_type]
                    reflexive = meta[reflexive_name].STEPTREE
                    counts = {b.name.lower(): 0 for b in reflexive}
                    for b in reflexive:
                        counts[b.name.lower()] += 1

                    for i in range(len(reflexive)):
                        name = reflexive[i].name.lower()
                        if counts[name] > 1 and i not in keep:
                            reflexive[i].name = ("DUP%s~%s" % (i, name))[: 31]

            # divide the cutscene times by 30(they're in ticks) and
            # subtract the fade-in time from the up_time(normally added
            # together as a total up-time in maps, but not in tag form)
            for b in meta.cutscene_titles.STEPTREE:
                b.up_time = max(b.up_time - b.fade_in_time, 0.0)

                b.fade_in_time  /= 30
                b.fade_out_time /= 30
                b.up_time       /= 30

        elif tag_cls == "snd!":
            meta.maximum_bend_per_second = meta.maximum_bend_per_second ** 30
            for pitch_range in meta.pitch_ranges.STEPTREE:
                if not byteswap: break
                for permutation in pitch_range.permutations.STEPTREE:
                    if permutation.compression.enum_name == "none":
                        # byteswap pcm audio
                        byteswap_pcm16_samples(permutation.samples)

        elif tag_cls == "shpp":
            predicted_resources.append(meta.predicted_resources)

        elif tag_cls == "shpg":
            shpg_attrs = meta.shpg_attrs

            # copy all merged values into their respective reflexives
            for b in shpg_attrs.merged_values.STEPTREE:
                typ = b.value_type.enum_name
                cnt = b.value_count
                if   typ == "boolean": array = shpg_attrs.booleans.STEPTREE
                elif typ == "integer": array = shpg_attrs.integers.STEPTREE
                elif typ == "color":   array = shpg_attrs.colors.STEPTREE
                elif typ == "bitmap":  array = shpg_attrs.bitmaps.STEPTREE
                elif typ != "float":   continue  # unknown type
                elif cnt == 1: array = shpg_attrs.floats_1d.STEPTREE
                elif cnt == 2: array = shpg_attrs.floats_2d.STEPTREE
                elif cnt == 3: array = shpg_attrs.floats_3d.STEPTREE
                elif cnt == 4: array = shpg_attrs.floats_4d.STEPTREE
                else:          continue  # unknown float type

                array.append()
                new_b = array[-1]
                new_b.value_name = b.value_name
                values = b.values.u_node

                if typ == "bitmap":
                    new_b.bitmap = b.bitmap
                    new_b.bitmap_index = values.bitmap_index
                    continue

                new_b.runtime_value      = b.runtime_value
                new_b.animation_function = b.animation_function
                new_b.animation_flags    = b.animation_flags
                new_b.animation_duration = b.animation_duration
                new_b.animation_rate     = b.animation_rate

                if typ == "boolean":
                    new_b.flags = b.flags
                    new_b.value = values.value
                else:
                    new_b.value_lower_bound = values.value_lower_bound
                    new_b.value_upper_bound = values.value_upper_bound

            # clear the merged values reflexive
            del shpg_attrs.merged_values.STEPTREE[:]

        elif tag_cls == "weap":
            predicted_resources.append(meta.weap_attrs.predicted_resources)

        # remove any predicted resources
        for pr in predicted_resources:
            del pr.STEPTREE[:]

        return meta

    def get_resource_map_paths(self, maps_dir=""):
        if self.is_resource or self.engine not in ("halo1pc", "halo1pcdemo",
                                                   "halo1ce", "halo1yelo",
                                                   "halo1vap"):
            return {}

        map_paths = {"bitmaps": None, "sounds": None, "loc": None}
        if self.engine not in ("halo1ce", "halo1yelo", "halo1vap"):
            map_paths.pop('loc')

        data_files = False
        if hasattr(self.map_header, "yelo_header"):
            data_files = self.map_header.yelo_header.flags.uses_mod_data_files

        if not is_path_empty(maps_dir):
            maps_dir = Path(maps_dir)
        elif data_files:
            maps_dir = self.filepath.parent.joinpath("data_files")
        else:
            maps_dir = self.filepath.parent

        map_name_str = "%s.map"
        if data_files:
            map_name_str = "~" + map_name_str

        # detect the map paths for the resource maps
        for map_name in sorted(map_paths.keys()):
            map_path = maps_dir.joinpath(map_name_str % map_name)
            if self.maps.get(map_name) is not None:
                map_paths[map_name] = self.maps[map_name].filepath
            elif map_path.is_file():
                map_paths[map_name] = map_path

        return map_paths

    def generate_map_info_string(self):
        string = HaloMap.generate_map_info_string(self)
        index, header = self.tag_index, self.map_header

        string += """

Calculated information:
    index magic == %s
    map magic   == %s

Tag index:
    tag count           == %s
    scenario tag id     == %s
    index array pointer == %s   non-magic == %s
    model data pointer  == %s
    meta data length    == %s
    vertex parts count  == %s
    index  parts count  == %s""" % (
        self.index_magic, self.map_magic,
        index.tag_count, index.scenario_tag_id & 0xFFff,
        index.tag_index_offset, index.tag_index_offset - self.map_magic,
        index.model_data_offset, header.tag_data_size,
        index.vertex_parts_count, index.index_parts_count)

        if index.SIZE == 36:
            string += """
    index parts pointer == %s   non-magic == %s""" % (
        index.index_parts_offset, index.index_parts_offset - self.map_magic)
        else:
            string += """
    vertex data size    == %s
    index  data size    == %s
    model  data size    == %s""" % (
        index.vertex_data_size,
        index.model_data_size - index.vertex_data_size,
        index.model_data_size)

        string += "\n\nSbsp magic and headers:\n"
        for tag_id in self.bsp_magics:
            header = self.bsp_headers.get(tag_id)
            if header is None: continue

            magic  = self.bsp_magics[tag_id]
            string += """    %s.structure_scenario_bsp
        bsp base pointer     == %s
        bsp magic            == %s
        bsp size             == %s
        bsp metadata pointer == %s   non-magic == %s\n""" % (
            index.tag_index[tag_id].path, self.bsp_header_offsets[tag_id],
            magic, self.bsp_sizes[tag_id], header.meta_pointer,
            header.meta_pointer - magic)

        if self.engine == "halo1yelo":
            string += self.generate_yelo_info_string()
        elif self.engine == "halo1vap":
            string += self.generate_vap_info_string()

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

    def generate_vap_info_string(self):
        vap = self.map_header.vap_header

        return """
VAP information:
    name        == %s
    build date  == %s
    description == %s

    vap version   == %s
    feature level == %s
    max players   == %s\n""" % (
            vap.name, vap.build_date, vap.description,
            vap.vap_version.enum_name, vap.feature_level.enum_name,
            vap.max_players,
            )
