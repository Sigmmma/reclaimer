#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

import os
import sys

from array import array as PyArray
from copy import deepcopy
from math import pi, log
from pathlib import Path
from struct import unpack, unpack_from, pack_into
from traceback import format_exc
from types import MethodType

from supyr_struct.buffer import BytearrayBuffer
from supyr_struct.field_types import FieldType
from supyr_struct.defs.frozen_dict import FrozenDict

from reclaimer.halo_script.hsc_decompilation import extract_scripts
from reclaimer.halo_script.hsc import get_hsc_data_block,\
    get_script_syntax_node_tag_refs, clean_script_syntax_nodes,\
    get_script_types, HSC_IS_SCRIPT_OR_GLOBAL,\
    SCRIPT_OBJECT_TYPES_TO_SCENARIO_REFLEXIVES
from reclaimer.common_descs import make_dependency_os_block
from reclaimer.hek.defs.snd_ import snd__meta_stub_blockdef
from reclaimer.hek.defs.sbsp import sbsp_meta_header_def
from reclaimer.hek.handler   import HaloHandler
from reclaimer.os_v4_hek.defs.coll import fast_coll_def
from reclaimer.os_v4_hek.defs.sbsp import fast_sbsp_def
from reclaimer.meta.wrappers.byteswapping import raw_block_def, byteswap_animation,\
     byteswap_uncomp_verts, byteswap_comp_verts, byteswap_tris,\
     byteswap_coll_bsp, byteswap_sbsp_meta, byteswap_scnr_script_syntax_data,\
     byteswap_pcm16_samples
from reclaimer.meta.wrappers.halo_map import HaloMap
from reclaimer.meta.wrappers.halo1_rsrc_map import Halo1RsrcMap, inject_sound_data, get_is_xbox_map
from reclaimer.meta.wrappers.map_pointer_converter import MapPointerConverter
from reclaimer.meta.wrappers.tag_index_manager import TagIndexManager
from reclaimer import data_extraction
from reclaimer.constants import tag_class_fcc_to_ext, GEN_1_HALO_CUSTOM_ENGINES
from reclaimer.util.compression import compress_normal32, decompress_normal32
from reclaimer.util import is_overlapping_ranges, is_valid_ascii_name_str,\
     int_to_fourcc, get_block_max

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

    # Module path printed when loading the tag defs
    tag_defs_module = "reclaimer.hek.defs"
    tag_classes_to_load = tuple(sorted(tag_class_fcc_to_ext.keys()))

    # Handler that controls how to load tags, eg tag definitions
    handler_class = HaloHandler

    force_checksum = False

    inject_rawdata = Halo1RsrcMap.inject_rawdata

    bsp_magics  = ()
    bsp_sizes   = ()
    bsp_headers = ()
    bsp_header_offsets = ()
    bsp_pointer_converters = ()
    
    sbsp_meta_header_def = sbsp_meta_header_def

    data_extractors = data_extraction.h1_data_extractors
    
    indexable_tag_classes = set((
        "bitm", "snd!", "font", "hmt ", "ustr"
        ))

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
    def globals_tag_id(self):
        if not self.tag_index:
            return None

        for b in self.tag_index.tag_index:
            if int_to_fourcc(b.class_1.data) == "matg":
                return b.id & 0xFFff

    @property
    def resource_map_prefix(self): 
        return ""
    @property
    def resource_maps_folder(self):
        return self.filepath.parent
    @property
    def resources_maps_mismatched(self):
        maps_dir = self.resource_maps_folder
        if not maps_dir:
            return False

        for map_name, filepath in self.get_resource_map_paths().items():
            if filepath and filepath.parent != maps_dir:
                return True
        return False
    @property
    def uses_bitmaps_map(self):
        return not self.is_resource
    @property
    def uses_loc_map(self):
        return not self.is_resource and "pc" not in self.engine
    @property
    def uses_sounds_map(self):
        return not self.is_resource

    @property
    def decomp_file_ext(self):
        return (
            ".vap" if self.engine == "halo1vap" else 
            self._decomp_file_ext
            )

    def is_indexed(self, tag_id):
        tag_header = self.tag_index.tag_index[tag_id]
        if not tag_header.indexed:
            return False
        return int_to_fourcc(tag_header.class_1.data) in self.indexable_tag_classes

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
        if self.engine in GEN_1_HALO_CUSTOM_ENGINES:
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
            # need to filter to dependencies that are actually valid
            tag_id = node.id & 0xFFff
            if tag_id not in range(len(tag_index_array)):
                continue

            tag_index_ref = tag_index_array[tag_id]
            if (node.tag_class.enum_name == tag_index_ref.class_1.enum_name and
                node.id == tag_index_ref.id):
                dependencies.append(node)

        if tag_cls == "scnr":
            # collect the tag references from the scenarios syntax data
            try:
                seen_tag_ids = set()
                syntax_data = get_hsc_data_block(meta.script_syntax_data.data)
                for node in get_script_syntax_node_tag_refs(syntax_data):
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

            self.setup_sbsp_headers()

        except Exception:
            print(format_exc())

    def setup_sbsp_headers(self):
        # read the sbsp headers
        for tag_id, offset in self.bsp_header_offsets.items():
            header = self.sbsp_meta_header_def.build(
                rawdata=self.map_data, offset=offset)

            if header.sig != header.get_desc("DEFAULT", "sig"):
                print("Sbsp header is invalid for '%s'" %
                      self.tag_index.tag_index[tag_id].path)
            self.bsp_headers[tag_id] = header
            self.tag_index.tag_index[tag_id].meta_offset = header.meta_pointer

    def setup_rawdata_pages(self):
        tag_index = self.tag_index

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
        if hasattr(tag_index, "model_data_size"):
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
        self.setup_rawdata_pages()

        # get the globals meta
        try:
            self.matg_meta = self.get_meta(self.globals_tag_id)
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

        if self.resources_maps_mismatched and kwargs.get("unlink_mismatched_resources", True):
            # this map reference different resource maps depending on what
            # folder its located in. we need to ignore any resource maps 
            # passed in unless they're in the same folder as this map.
            print("Unlinking potentially incompatible resource maps from %s" %
                self.map_name
                )
            self.maps = {}

    def get_meta(self, tag_id, reextract=False, ignore_rsrc_sounds=False, **kw):
        '''
        Takes a tag reference id as the sole argument.
        Returns that tags meta data as a parsed block.
        '''
        if tag_id is None:
            return

        tag_index_ref = self.tag_index_manager.get_tag_index_ref(tag_id)
        if tag_index_ref is None:
            return

        # if we are given a 32bit tag id, mask it off
        tag_id   &= 0xFFFF
        magic     = self.map_magic
        engine    = self.engine
        map_data  = self.map_data

        tag_cls = None
        is_scenario = (tag_id == (self.tag_index.scenario_tag_id & 0xFFFF))
        if is_scenario:
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
            if tag_cls == "snd!":
                if "sounds" in self.maps:
                    rsrc_map = self.maps["sounds"]
                    sound_mapping = self.ce_rsrc_sound_indexes_by_path
                    tag_path = tag_index_ref.path
                    if sound_mapping is None or tag_path not in sound_mapping:
                        return

                    tag_id = sound_mapping[tag_path]//2

            elif tag_cls == "bitm":
                if "bitmaps" in self.maps:
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
            snd_stub = None
            if tag_cls == "snd!":
                # while the sound samples and complete tag are in the 
                # resource map, the metadata for the body of the sound
                # tag is in the main map. Need to copy its values into
                # the resource map sound tag we extracted.
                try:
                    # read the meta data from the map
                    with FieldType.force_little:
                        snd_stub = snd__meta_stub_blockdef.build(
                            rawdata=map_data,
                            offset=pointer_converter.v_ptr_to_f_ptr(offset),
                            tag_index_manager=self.tag_index_manager)
                except Exception:
                    print(format_exc())

            if snd_stub:
                # copy values over
                for name in (
                        "flags", "sound_class", "sample_rate",
                        "minimum_distance", "maximum_distance", 
                        "skip_fraction", "random_pitch_bounds",
                        "inner_cone_angle", "outer_cone_angle",
                        "outer_cone_gain", "gain_modifier", 
                        "maximum_bend_per_second", 
                        "modifiers_when_scale_is_zero",
                        "modifiers_when_scale_is_one",
                        "encoding", "compression", "promotion_sound",
                        "promotion_count", "max_play_length",
                        ):
                    setattr(meta, name, getattr(snd_stub, name))

            return meta
        elif not reextract:
            if is_scenario and self.scnr_meta:
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
                    safe_mode=(self.safe_mode and not kw.get("disable_safe_mode")),
                    parsing_resource=force_parsing_rsrc)
        except Exception:
            print(format_exc())
            if not kw.get("allow_corrupt"):
                return

        meta = block[0]
        try:
            # TODO: remove this dirty-ass hack
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
            max_anim_count = get_block_max(meta.animations)
            for i in range(len(animations)):
                if i >= max_anim_count:
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

        elif tag_cls == "bitm":
            bitmaps = [b for b in meta.bitmaps.STEPTREE
                       if "dxt" in b.format.enum_name]
            # correct mipmap count on xbox dxt bitmaps. texels for any
            # mipmaps whose dimensions are 2x2 or smaller are pruned
            for bitmap in bitmaps:
                # figure out largest dimension(clip to 1 to avoid log(0, 2))
                max_dim = max(1, bitmap.width, bitmap.height)

                # subtract 2 to account for width/height of 1 or 2 not having mips
                maxmips = int(max(0, math.log(max_dim, 2) - 2))

                # clip mipmap count to max and min number that can exist
                bitmap.mipmaps = max(0, min(maxmips, bitmap.mipmaps))

        elif tag_cls in ("sbsp", "coll"):
            if tag_cls == "sbsp" :
                bsps = meta.collision_bsp.STEPTREE
            else:
                bsps = []
                for node in meta.nodes.STEPTREE:
                    bsps.extend(node.bsps.STEPTREE)

            for bsp in bsps:
                vert_data = bsp.vertices.STEPTREE
                # first 2 ints in each edge are the vert indices, and theres
                # 6 int32s per edge. find the highest vert index being used
                if bsp.edges.STEPTREE:
                    byteorder = 'big' if self.engine == "halo1anni" else 'little'

                    edges = PyArray("i", bsp.edges.STEPTREE)
                    if byteorder != sys.byteorder:
                        edges.byteswap()

                    max_start_vert = max(edges[0: len(edges): 6])
                    max_end_vert   = max(edges[1: len(edges): 6])
                else:
                    max_start_vert = max_end_vert = -1

                if max_start_vert * 16 < len(vert_data):
                    del vert_data[(max_start_vert + 1) * 16: ]
                    bsp.vertices.size = max_start_vert + 1

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

            # lets not use magic numbers here
            _, script_object_types = get_script_types(self.engine)
            biped_node_enum = script_object_types.index("actor_type")

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
                        if node.type == biped_node_enum and not(node.flags & HSC_IS_SCRIPT_OR_GLOBAL):
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
            # try to fix HEK+ extraction bug
            for obj in meta.objects.STEPTREE:
                for enum in (obj.function, obj.function_controls):
                    uint16_data = enum.data & 0xFFff
                    if (uint16_data & 0xFF00 and not uint16_data & 0xFF):
                        # higher bits are set than lower. this is likely
                        # a HEK plus extraction bug and should be fixed
                        uint16_data = ((uint16_data>>8) | (uint16_data<<8)) & 0xFFff
                        enum.data = uint16_data - (
                            0 if uint16_data < 0x8000 else 0x10000
                            )

            # byteswap animation data
            for anim in meta.animations.STEPTREE:
                if not byteswap: break
                byteswap_animation(anim)

        elif tag_cls in ("bitm", "snd!"):
            meta = Halo1RsrcMap.meta_to_tag_data(self, meta, tag_cls, tag_index_ref, **kwargs)

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
            # NOTE: xbox has a cache flag in the 2nd 
            #       bit, so it should be masked out too.
            meta.flags.data &= (1 if "xbox" in engine else 3)

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

            if meta.corona_rotation.function_scale == 360.0:
                # fix a really old bug(i think its the
                # reason the above comment was created)
                meta.corona_rotation.function_scale = 0.0

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
            if engine in ("halo1yelo", "halo1ce", "halo1pc", "halo1vap", "halo1mcc",
                          "halo1anni", "halo1pcdemo", "stubbspc", "stubbspc64bit"):
                # model_magic seems to be the same for all pc maps
                verts_start = tag_index.model_data_offset
                tris_start  = verts_start + tag_index.index_parts_offset
                model_magic = None
            else:
                model_magic = magic
                
            # need to unset this flag, as it forces map-compile-time processing
            # to occur on the model's vertices, which shouldn't be done twice.
            meta.flags.blend_shared_normals = False

            # lod cutoffs are swapped between tag and cache form
            cutoffs = (meta.superlow_lod_cutoff, meta.low_lod_cutoff,
                       meta.high_lod_cutoff, meta.superhigh_lod_cutoff)
            meta.superlow_lod_cutoff  = cutoffs[3]
            meta.low_lod_cutoff       = cutoffs[2]
            meta.high_lod_cutoff      = cutoffs[1]
            meta.superhigh_lod_cutoff = cutoffs[0]

            # localize the global markers
            # ensure all local marker arrays are empty
            for region in meta.regions.STEPTREE:
                for perm in region.permutations.STEPTREE:
                    del perm.local_markers.STEPTREE[:]

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
                    tris_block  = part.triangles
                    info        = part.model_meta_info

                    if info.vertex_type.enum_name == "model_comp_verts":
                        verts_block     = part.compressed_vertices
                        byteswap_verts  = byteswap_comp_verts
                        vert_size       = 32
                    elif info.vertex_type.enum_name == "model_uncomp_verts":
                        verts_block     = part.uncompressed_vertices
                        byteswap_verts  = byteswap_uncomp_verts
                        vert_size       = 68
                    else:
                        print("Error: Unknown vertex type in model: %s" % info.vertex_type.data)
                        continue

                    if info.index_type.enum_name != "triangle_strip":
                        print("Error: Unknown index type in model: %s" % info.index_type.data)
                        continue

                    # null out certain things in the part
                    part.centroid_primary_node = 0
                    part.centroid_secondary_node = 0
                    part.centroid_primary_weight = 0.0
                    part.centroid_secondary_weight = 0.0

                    # make the new blocks to hold the raw data
                    verts_block.STEPTREE = raw_block_def.build()
                    tris_block.STEPTREE  = raw_block_def.build()

                    # read the offsets of the vertices and indices from the map
                    if model_magic is None:
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
            meta.proj_attrs.detonation.minimum_velocity *= 30
            for material_response in meta.proj_attrs.material_responses.STEPTREE:
                material_response.potential_response.impact_velocity[0] *= 30
                material_response.potential_response.impact_velocity[1] *= 30

        elif tag_cls == "sbsp":
            if byteswap:
                byteswap_sbsp_meta(meta)

            # null out the runtime decals
            del meta.runtime_decals.STEPTREE[:]

            for cluster in meta.clusters.STEPTREE:
                predicted_resources.append(cluster.predicted_resources)
            
            for coll_mat in meta.collision_materials.STEPTREE:
                coll_mat.material_type.data = 0  # supposed to be 0 in tag form

            comp_norm   = compress_normal32
            decomp_norm = decompress_normal32

            comp_vert_unpacker      = MethodType(unpack_from, "<12s3I8s")
            comp_vert_packer        = MethodType(pack_into,   "<12s3I8s")
            uncomp_vert_unpacker    = MethodType(unpack_from, "<12s9f8s")
            uncomp_vert_packer      = MethodType(pack_into,   "<12s9f8s")

            comp_lm_vert_unpacker   = MethodType(unpack_from, "<I2h")
            comp_lm_vert_packer     = MethodType(pack_into,   "<I2h")
            uncomp_lm_vert_unpacker = MethodType(unpack_from, "<5f")
            uncomp_lm_vert_packer   = MethodType(pack_into,   "<5f")

            for lightmap in meta.lightmaps.STEPTREE:
                if not (kwargs.get("generate_comp_verts") or
                        kwargs.get("generate_uncomp_verts")):
                    break

                for mat in lightmap.materials.STEPTREE:
                    # this code has been designed to be able to handle vertices
                    # in compressed, uncompressed, or mixed format. no real
                    # chance of them ever getting mixed, but who knows?

                    # how much data WOULD be in the buffers if they were full
                    u_verts_size     = 56*mat.vertices_count
                    c_verts_size     = 32*mat.vertices_count
                    u_lm_verts_size  = 20*mat.lightmap_vertices_count
                    c_lm_verts_size  =  8*mat.lightmap_vertices_count

                    vert_offs    = zip(
                        range(0, u_verts_size, 56),
                        range(0, c_verts_size, 32),
                        )
                    lm_vert_offs = zip(
                        range(u_verts_size, u_lm_verts_size, 20),
                        range(c_verts_size, c_lm_verts_size,  8),
                        )
                    vert_type    = mat.vertex_type.enum_name
                    lm_vert_type = mat.lightmap_vertex_type.enum_name

                    # convert the vertex buffers into bytearrays, and insert 
                    # padding for the vertices we're going to generate below
                    u_buffer = bytearray(mat.uncompressed_vertices.STEPTREE)
                    c_buffer = bytearray(mat.compressed_vertices.STEPTREE)

                    if (kwargs.get("generate_comp_verts") and
                        vert_type == "sbsp_uncomp_material_verts"
                        ):
                        # generate compressed verts from uncompressed
                        c_buffer = bytearray(c_verts_size) + c_buffer
                        for u_off, c_off in vert_offs:
                            xyz, ni, nj, nk, bi, bj, bk, ti, tj, tk, uv = \
                                uncomp_vert_unpacker(u_buffer, u_off)
                            comp_vert_packer(
                                c_buffer, c_off,
                                xyz,
                                comp_norm(ni, nj, nk),
                                comp_norm(bi, bj, bk),
                                comp_norm(ti, tj, tk),
                                uv
                                )
                    elif (kwargs.get("generate_uncomp_verts") and
                        vert_type == "sbsp_comp_material_verts"
                        ):
                        # generate uncompressed verts from compressed
                        u_buffer = bytearray(u_verts_size) + u_buffer
                        for u_off, c_off in vert_offs:
                            xyz, n, b, t, uv = comp_vert_unpacker(c_buffer, c_off)
                            uncomp_vert_packer(
                                u_buffer, u_off,
                                xyz,
                                *decomp_norm(n),
                                *decomp_norm(b),
                                *decomp_norm(t),
                                uv
                                )

                    if (kwargs.get("generate_comp_verts") and
                        lm_vert_type == "sbsp_uncomp_lightmap_verts"
                        ):
                        # generate compressed lightmap verts from uncompressed
                        c_buffer += bytearray(c_lm_verts_size)
                        for u_off, c_off in lm_vert_offs:
                            ni, nj, nk, u, v = uncomp_lm_vert_unpacker(u_buffer, c_off)
                            comp_lm_vert_packer(
                                c_buffer, u_off,
                                comp_norm(ni, nj, nk),
                                int((-1 if u < -1 else 1 if u > 1 else u)*32767),
                                int((-1 if v < -1 else 1 if v > 1 else v)*32767),
                                )
                    elif (kwargs.get("generate_uncomp_verts") and
                        lm_vert_type == "sbsp_comp_lightmap_verts"
                        ):
                        # generate uncompressed lightmap verts from compressed
                        u_buffer += bytearray(u_lm_verts_size)
                        for u_off, c_off in lm_vert_offs:
                            n, u, v = comp_lm_vert_unpacker(c_buffer, c_off)
                            uncomp_lm_vert_packer(
                                u_buffer, u_off,
                                *decomp_norm(n), u/32767, v/32767
                                )

                    # need to null these or original CE sapien could crash
                    mat.unknown_meta_offset0  = mat.vertices_meta_offset          = 0
                    mat.unknown_meta_offset1  = mat.lightmap_vertices_meta_offset = 0

                    # set these to the correct vertex types based on what we have
                    vert_type_str = (
                        "sbsp_comp_%s_verts"
                        if c_verts_size and c_lm_verts_size else 
                        "sbsp_uncomp_%s_verts"
                        )
                    mat.vertex_type.set_to(vert_type_str % "material")
                    mat.lightmap_vertex_type.set_to(vert_type_str % "lightmap")

                    mat.uncompressed_vertices.STEPTREE = u_buffer
                    mat.compressed_vertices.STEPTREE   = c_buffer

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

                # lets not use magic numbers here
                _, script_object_types = get_script_types(engine)
                trigger_volume_enum = script_object_types.index("trigger_volume")

                # NOTE: For a list of all the script object types
                # with their corrosponding enum value, check
                #     reclaimer.halo_script.hsc.get_script_types
                keep_these = {script_object_types.index(typ): set() for typ in
                              SCRIPT_OBJECT_TYPES_TO_SCENARIO_REFLEXIVES}

                # don't de-duplicate trigger volumes
                for b in meta.bsp_switch_trigger_volumes.STEPTREE:
                    keep_these[trigger_volume_enum].add(b.trigger_volume)

                # for everything we're keeping, clear the upper 16bits of the data
                for i in range(min(syntax_data.last_node, len(syntax_data.nodes))):
                    node = syntax_data.nodes[i]
                    if node.type in keep_these:
                        keep_these[node.type].add(node.data & 0xFFff)

                # for everything else, rename duplicates
                for script_object_type, reflexive_name in \
                        SCRIPT_OBJECT_TYPES_TO_SCENARIO_REFLEXIVES.items():

                    script_object_type_enum = script_object_types.index(script_object_type)
                    keep        = keep_these[script_object_type_enum]
                    reflexive   = meta[reflexive_name].STEPTREE
                    counts      = {b.name.lower(): 0 for b in reflexive}
                    for b in reflexive:
                        counts[b.name.lower()] += 1

                    for i in range(len(reflexive)):
                        name = reflexive[i].name.lower()
                        if counts[name] > 1 and i not in keep:
                            reflexive[i].name = ("DUP%s~%s" % (i, name))[: 31]

                # null tag refs after we're done with them
                clean_script_syntax_nodes(syntax_data, engine)
            
            # decompile scripts and put them in the source_files array so
            # sapien can recompile them when it opens an extracted scenario
            source_files = meta.source_files.STEPTREE
            del source_files[:]
            script_sources, global_sources = extract_scripts(
                engine=engine, tagdata=meta, add_comments=False, minify=True
                )
            i = 0
            for source in (*script_sources, *global_sources):
                source_files.append()
                source_files[-1].source_name = "decompiled_%s.hsc" % i
                source_files[-1].source.data = source.encode('latin-1')
                i += 1

            # divide the cutscene times by 30(they're in ticks) and
            # subtract the fade-in time from the up_time(normally added
            # together as a total up-time in maps, but not in tag form)
            for b in meta.cutscene_titles.STEPTREE:
                b.up_time = max(b.up_time - b.fade_in_time, 0.0)

                b.fade_in_time  /= 30
                b.fade_out_time /= 30
                b.up_time       /= 30

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

        elif tag_cls == "soso":
            # set the mcc multipurpose_map_uses_og_xbox_channel_order flag
            if "xbox" in engine or "stubbs" in engine or engine == "shadowrun_proto":
                meta.soso_attrs.model_shader.flags.data |= 1<<6

        elif tag_cls == "weap":
            # try to fix HEK+ extraction bug
            uint16_data = (meta.weap_attrs.aiming.zoom_levels & 0xFFff)
            if (uint16_data & 0xFF00 and not uint16_data & 0xFF):
                # higher bits are set than lower. this is likely
                # a HEK plus extraction bug and should be fixed
                uint16_data = ((uint16_data>>8) | (uint16_data<<8)) & 0xFFff
                meta.weap_attrs.aiming.zoom_levels = uint16_data - (
                    0 if uint16_data < 0x8000 else 0x10000
                    )

            predicted_resources.append(meta.weap_attrs.predicted_resources)

        # remove any predicted resources
        for pr in predicted_resources:
            del pr.STEPTREE[:]

        return meta

    def get_resource_map_paths(self, maps_dir=""):
        if self.is_resource or not self.resource_maps_folder:
            return {}

        map_paths = {
            name: None for name in (
                *(["bitmaps"] if self.uses_bitmaps_map else []),
                *(["sounds"]  if self.uses_sounds_map  else []),
                *(["loc"]     if self.uses_loc_map     else []),
                )
            }

        name_str = self.resource_map_prefix + "%s.map"
        maps_dir = (
            Path(maps_dir) if not is_path_empty(maps_dir) else
            self.resource_maps_folder
            )

        # detect the map paths for the resource maps
        if maps_dir:
            for map_name in sorted(map_paths.keys()):
                map_path = maps_dir.joinpath(name_str % map_name)
                if self.maps.get(map_name) is not None:
                    map_paths[map_name] = self.maps[map_name].filepath
                elif map_path.is_file():
                    map_paths[map_name] = map_path

        return map_paths

    def generate_map_info_string(self):
        string = HaloMap.generate_map_info_string(self)
        index, header = self.tag_index, self.map_header

        if self.engine == "halo1mcc":
            string += """\n    Calculated information:
        use bitmaps map      == %s
        use sounds map       == %s
        no remastered sync   == %s""" % (
            bool(header.mcc_flags.use_bitmaps_map), 
            bool(header.mcc_flags.use_sounds_map), 
            bool(header.mcc_flags.disable_remastered_sync), 
            )

        string += """

Calculated information:
    index magic == %s
    map magic   == %s

Tag index:
    tag count           == %s
    scenario tag id     == %s
    index array pointer == %s   non-magic == %s
    meta data length    == %s
    vertex parts count  == %s
    index  parts count  == %s""" % (
        self.index_magic, self.map_magic,
        index.tag_count, index.scenario_tag_id & 0xFFff,
        index.tag_index_offset, index.tag_index_offset - self.map_magic,
        header.tag_data_size,
        index.vertex_parts_count, index.index_parts_count)

        if hasattr(index, "model_data_size"):
            string += """
    vertex data pointer == %s
    index  data pointer == %s
    index  data size    == %s
    model  data size    == %s""" % (
        index.model_data_offset, 
        index.index_parts_offset,
        index.model_data_size - index.index_parts_offset,
        index.model_data_size
        )
        else:
            string += """
    vertex refs pointer == %s   non-magic == %s
    index  refs pointer == %s   non-magic == %s""" % (
        index.model_data_offset,  index.model_data_offset - self.map_magic,
        index.index_parts_offset, index.index_parts_offset - self.map_magic,
        )

        string += "\n\nSbsp magic and headers:\n"
        for tag_id in self.bsp_magics:
            header = self.bsp_headers.get(tag_id)
            if header is None: continue

            magic  = self.bsp_magics[tag_id]
            offset = self.bsp_header_offsets[tag_id]
            string += """    %s.structure_scenario_bsp
        bsp base pointer     == %s
        bsp magic            == %s
        bsp size             == %s
        bsp metadata pointer == %s   non-magic == %s\n""" % (
            index.tag_index[tag_id].path, offset,
            magic, self.bsp_sizes[tag_id], header.meta_pointer,
            header.meta_pointer + offset - magic
            )
            if self.engine in ("halo1mcc", "halo1anni"):
                string += """\
        render verts size    == %s
        render verts pointer == %s\n""" % (
                header.uncompressed_render_vertices_size,
                header.uncompressed_render_vertices_pointer,
                )
            else:
                string += """\
        uncomp mats count    == %s
        uncomp mats pointer  == %s   non-magic == %s
        comp mats count      == %s
        comp mats pointer    == %s   non-magic == %s\n""" % (
                header.uncompressed_lightmap_materials_count,
                header.uncompressed_lightmap_materials_pointer,
                header.uncompressed_lightmap_materials_pointer + offset - magic,
                header.compressed_lightmap_materials_count,
                header.compressed_lightmap_materials_pointer,
                header.compressed_lightmap_materials_pointer + offset - magic,
                )

        if self.engine == "halo1vap":
            string += self.generate_vap_info_string()

        return string

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
