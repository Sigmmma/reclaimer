from math import ceil, log
from os.path import exists, join
from tkinter.filedialog import askopenfilename


from reclaimer import data_extraction
from reclaimer.h3.constants import h3_tag_class_fcc_to_ext, FORMAT_NAME_MAP
from reclaimer.h3.util import HALO3_SHARED_MAP_TYPES, get_h3_pixel_bytes_size
from reclaimer.h3.handler import Halo3Handler
from reclaimer.h3.constants import h3_tag_class_fcc_to_ext
from reclaimer.meta.wrappers.halo_map import *
from reclaimer.meta.gen3_resources.bitmap import s_tag_d3d_texture_def,\
     s_tag_d3d_texture_interleaved_def

from arbytmap.format_defs import VALID_FORMATS

__all__ = ("Halo3Map", )


def get_bitmap_pixel_data(halo_map, bitm_meta, bitmap_index):
    n_assets = bitm_meta.zone_assets_normal.STEPTREE
    i_assets = bitm_meta.zone_assets_interleaved.STEPTREE
    bitmap = bitm_meta.bitmaps.STEPTREE[bitmap_index]
    rawdata_manager = halo_map.rawdata_manager

    tag_rsrc_idx = tag_rsrc_info = d3d_texture = None
    pixel_data = ()
    if bitmap.interleaved_asset_index in range(len(i_assets)):
        tag_rsrc_idx = i_assets[bitmap.interleaved_asset_index].idx
        d3d_def = s_tag_d3d_texture_interleaved_def
    else:
        tag_rsrc_idx = n_assets[bitmap_index].idx
        d3d_def = s_tag_d3d_texture_def

    if tag_rsrc_idx is not None:
        fixup_data, _, __ = rawdata_manager.get_tag_resource_fixup(tag_rsrc_idx)
        tag_rsrc_info = rawdata_manager.get_tag_resource(tag_rsrc_idx)

        if fixup_data and tag_rsrc_info:
            d3d_texture = d3d_def.build(rawdata=fixup_data)
            pixel_data = rawdata_manager.get_tag_resource_data(
                tag_rsrc_idx,
                d3d_texture.primary_page_data.size,
                d3d_texture.secondary_page_data.size)

    return d3d_texture, pixel_data


def inject_bitmap_data(halo_map, bitm_meta):
    processed_pixel_data = bitm_meta.processed_pixel_data
    bitmaps = bitm_meta.bitmaps.STEPTREE
    n_assets = bitm_meta.zone_assets_normal.STEPTREE
    i_assets = bitm_meta.zone_assets_interleaved.STEPTREE

    processed_pixel_data.data = bytearray()
    for i in range(len(bitmaps)):
        bitmap = bitmaps[i]
        bitmap.pixels_offset = len(processed_pixel_data.data)
        try:
            fmt = FORMAT_NAME_MAP[bitmap.format.data]
        except (KeyError, IndexError):
            # unknown bitmap format
            continue

        if fmt not in VALID_FORMATS:
            continue
        d3d_texture, pixel_data_chunks = get_bitmap_pixel_data(
            halo_map, bitm_meta, i)
        if not pixel_data_chunks:
            continue
        elif len(pixel_data_chunks) == 1:
            pixel_data_chunks.append(b'')

        tex_stride = get_h3_pixel_bytes_size(
            fmt, 32, 32, 1, 0, bitmap.format_flags.tiled)

        if hasattr(d3d_texture, "texture1"):
            # slice out the main image and mips for each of the
            # interleaved bitmaps(their storage is very confusing)
            pri_chunk, sec_chunk = pixel_data_chunks[: 2]
            main_chunk, mips_chunk = bytearray(), bytearray()
            tex_num = int(bool(bitmap.interleaved_index))
            tex_page0 = d3d_texture.texture0.tex_page_index
            tex_page1 = d3d_texture.texture1.tex_page_index
            if tex_num:
                tex_page, other_tex_page = tex_page1, tex_page0
            else:
                tex_page, other_tex_page = tex_page0, tex_page1

            if tex_page0 == 0 and tex_page1 == 1:
                # idky this is needed, but without it the second textures
                # mipmaps will end up getting used as the first textures
                # main image, and the first textures main image and mipmaps
                # will end up getting used as the second textures mipmaps.
                tex_num = (tex_num + 1) % 2

            tex_skip_size = tex_num * tex_stride // 2

            mips_start = 0
            if tex_page == 0:
                mips_start = bitmap.mipmap_data_off
                main_chunk += pri_chunk[tex_skip_size: tex_skip_size + mips_start]
            elif not other_tex_page:
                main_chunk += sec_chunk
            elif tex_num:
                main_chunk += sec_chunk[len(sec_chunk) // 2: ]
            else:
                main_chunk += sec_chunk[: len(sec_chunk) // 2]

            mips_chunk += pri_chunk[mips_start + tex_skip_size: ]

            pixel_data_chunks = [mips_chunk, main_chunk]

        bitmap.pixels_data_size = 0
        for pixel_data in reversed(pixel_data_chunks):
            bitmap.pixels_data_size += len(pixel_data)
            processed_pixel_data.data += pixel_data


class Halo3Map(HaloMap):
    '''Generation 3 map'''
    rawdata_manager = None

    shared_map_names = ()

    root_tags = {}

    tag_defs_module = "reclaimer.h3.defs"
    tag_classes_to_load = tuple(sorted(h3_tag_class_fcc_to_ext.keys()))

    handler_class = Halo3Handler

    string_id_set_offsets = (
        (0x4B7, 0xC11), (0x0, 0x4B7), (0x0, 0xA7D),
        (0x0, 0xB0F),   (0x0, 0xBAF), (0x0, 0xB63),
        (0x0, 0xBBF),   (0x0, 0xBF0), (0x0, 0xC04))

    def __init__(self, maps=None):
        self.root_tags = {}
        HaloMap.__init__(self, maps)
        self.setup_tag_headers()

    def basic_deprotection(self):
        found_counts = {}
        for b in self.tag_index.tag_index:
            if b.path: continue

            tag_path = self.map_header.map_name
            tag_cls  = b.class_1.data
            name_id  = (tag_path, tag_cls)
            if name_id in found_counts:
                tag_path = "%s_%s" % (tag_path, found_counts[name_id])
                found_counts[name_id] += 1
            else:
                found_counts[name_id] = 0

            b.path = tag_path

    def get_meta_descriptor(self, tag_cls):
        tagdef = self.defs.get(tag_cls)
        if tagdef is not None:
            return tagdef.descriptor[1]

    def get_root_tag(self, tag_id_or_cls):
        if isinstance(tag_id_or_cls, str):
            for b in self.orig_tag_index.root_tags:
                if b.tag_class.enum_name == tag_id_or_cls:
                    tag_id_or_cls = b.id
                    break

        if isinstance(tag_id_or_cls, int):
            tag_id_or_cls &= 0xFFff
            if tag_id_or_cls not in self.root_tags:
                self.load_root_tags(tag_id_or_cls)

        return self.root_tags.get(tag_id_or_cls)

    def load_root_tags(self, tag_ids_to_load=()):
        tag_classes_to_load_by_ids = {}
        for b in self.orig_tag_index.root_tags:
            tag_classes_to_load_by_ids[b.id] = b.tag_class.enum_name

        if not tag_ids_to_load:
            tag_ids_to_load = set(tag_classes_to_load_by_ids).difference(
                ("scenario", "globals"))

        for tag_id in tag_ids_to_load:
            tag_cls = tag_classes_to_load_by_ids[tag_id]
            meta = self.get_meta(tag_id)
            if meta:
                self.root_tags[tag_id & 0xFFff] = meta
                if tag_cls:
                    self.root_tags[tag_cls] = meta

    def load_map(self, map_path, **kwargs):
        autoload_resources = kwargs.get("autoload_resources", True)
        will_be_active = kwargs.get("will_be_active", True)
        HaloMap.load_map(self, map_path, **kwargs)
        self.tag_index = h3_to_h1_tag_index(self.map_header, self.tag_index)
        self.basic_deprotection()

        tag_index_array = self.tag_index.tag_index
        self.tag_index_manager = TagIndexManager(tag_index_array)
        self.string_id_manager = StringIdManager(
            self.map_header.strings.string_id_table,
            self.string_id_set_offsets,
            )
        for sect in self.map_header.sections:
            self.map_pointer_converter.add_page_info(
                sect.virtual_address, sect.file_offset, sect.size)

        for part in self.map_header.partitions:
            self.map_pointer_converter.add_page_info(
                part.load_address, part.file_offset, part.size)

        self.load_root_tags()

        play_meta = self.root_tags.get("cache_file_resource_layout_table")
        if play_meta:
            self.shared_map_names = list(
                b.map_path.lower().replace('\\', '/').split("/")[-1].split(".")[0]
                for b in play_meta.external_cache_references.STEPTREE)

        self.rawdata_manager = RawdataManager(self)

        map_type = self.map_header.map_type.data
        if map_type >= 2 and map_type < 5:
            self.is_resource = True
            ext_cache_name = HALO3_SHARED_MAP_TYPES[map_type - 2]

            for map_name, halo_map in self.maps.items():
                # update each map's rawdata_manager so each one
                # knows what name the shared caches are named.
                if map_name != "<active>":
                    halo_map.rawdata_manager.add_shared_map_name(
                        ext_cache_name, self.map_header.map_name)

        if autoload_resources and map_type <= 2:
            self.load_all_resource_maps(dirname(map_path))

        self.map_data.clear_cache()

    def load_all_resource_maps(self, maps_dir=""):
        play_meta = self.root_tags.get("cache_file_resource_layout_table")
        if not play_meta:
            print("Could not get cache_file_resource_layout_table meta.\n"
                  "Cannot determine resource maps.")
            return

        map_paths = {name: None for name in self.shared_map_names}
        if not maps_dir:
            maps_dir = dirname(self.filepath)

        # detect/ask for the map paths for the resource maps
        for map_name in sorted(map_paths.keys()):
            map_name = map_name.split(".")[0]
            if self.maps.get(map_name) is not None:
                # map already loaded
                continue

            map_path = join(maps_dir, map_name)
            if exists(map_path + ".map"):
                map_path += ".map"

            while map_path and not exists(map_path):
                map_path = askopenfilename(
                    initialdir=maps_dir,
                    title="Select the %s.map" % map_name,
                    filetypes=((map_name, "*.map"),
                               (map_name, "*.*")))

                if map_path:
                    maps_dir = dirname(map_path)
                else:
                    print("    You wont be able to extract from %s.map" % map_name)
                    break

            map_paths[map_name] = map_path

        for map_name in sorted(map_paths.keys()):
            map_path = map_paths[map_name]
            try:
                if self.maps.get(map_name) is None and map_path:
                    print("    Loading %s..." % map_name)
                    type(self)(self.maps).load_map(map_path, will_be_active=False)
                    print("        Finished")
            except Exception:
                print(format_exc())

    def extract_tag_data(self, meta, tag_index_ref, **kw):
        extractor = data_extraction.h3_data_extractors.get(
            fourcc(tag_index_ref.class_1.data))
        if extractor is None:
            return "No extractor for this type of tag."
        kw['halo_map'] = self
        return extractor(meta, tag_index_ref.path, **kw)

    def get_meta(self, tag_id, reextract=False, **kw):
        if tag_id is None or self.map_header.map_type.data > 2:
            # shared maps don't have a tag index
            return

        # if we are given a 32bit tag id, mask it off
        tag_id &= 0xFFff
        tag_index_ref = self.tag_index_manager.get_tag_index_ref(tag_id)
        if tag_index_ref is None:
            return

        tag_cls = None
        full_tag_cls_name = tag_index_ref.class_1.enum_name
        if full_tag_cls_name not in ("<INVALID>", "NONE"):
            tag_cls = fourcc(tag_index_ref.class_1.data)

        desc = self.get_meta_descriptor(tag_cls)
        if desc is None or tag_cls is None:
            return
        elif not reextract and self.root_tags.get(full_tag_cls_name):
            return self.root_tags[full_tag_cls_name]

        block = [None]
        try:
            # read the meta data from the map
            offset = self.map_pointer_converter.v_ptr_to_f_ptr(
                tag_index_ref.meta_offset)

            desc['TYPE'].parser(
                desc, parent=block, attr_index=0,
                rawdata=self.map_data, offset=offset,
                tag_index_manager=self.tag_index_manager,
                map_string_id_manager=self.string_id_manager,
                map_pointer_converter=self.map_pointer_converter,)
        except Exception:
            print(format_exc())
            if kw.get("allow_corrupt"):
                return block[0]
            return

        try:
            self.record_map_cache_read(tag_id, 0)
            if self.map_cache_over_limit():
                self.clear_map_cache()

            self.inject_rawdata(block[0], tag_cls, tag_index_ref)
        except Exception:
            print(format_exc())
            if not kw.get("allow_corrupt"):
                meta = None

        return block[0]

    def inject_rawdata(self, meta, tag_cls, tag_index_ref):
        # get some rawdata that would be pretty annoying to do in the parser
        if tag_cls == "bitm":
            inject_bitmap_data(self, meta)

        return meta

    def meta_to_tag_data(self, meta, tag_cls, tag_index_ref, **kwargs):
        if tag_cls == "bitm":
            # make sure all bitmaps have data, and if they don't we don't
            # consider this as a valid bitmap, so it shouldnt be a tag.
            if not meta.processed_pixel_data.data:
                return None
            del meta.zone_assets_normal.STEPTREE[:]
            del meta.zone_assets_interleaved.STEPTREE[:]

        elif tag_cls in ("jmad", "mode", "pmdf", "sLdT", "sbsp", "snd!"):
            # cannot extract these until rawdata extraction is implemented
            return None

        return meta
