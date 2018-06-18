import zlib

from os.path import exists, join
from tkinter.filedialog import askopenfilename

from .halo_map import *
from reclaimer import data_extraction
from reclaimer.h2.util import HALO2_MAP_TYPES, split_raw_pointer


class Halo2Map(HaloMap):
    ugh__meta = None

    def __init__(self, maps=None):
        HaloMap.__init__(self, maps)

    def inject_rawdata(self, meta, tag_cls, tag_index_ref):
        # get some rawdata that would be pretty annoying to do in the parser
        if tag_cls == "bitm":
            # grab bitmap data correctly from map
            new_pixels = BytearrayBuffer()
            pix_off = 0

            for bitmap in meta.bitmaps.STEPTREE:
                # grab the bitmap data from the correct map
                bitmap.pixels_offset = pix_off

                ptr, map_name = split_raw_pointer(bitmap.lod1_offset)
                halo_map = self
                if map_name != "local":
                    halo_map = self.maps.get(map_name)

                if halo_map is None:
                    bitmap.lod1_size = 0
                    continue

                halo_map.map_data.seek(ptr)
                mip_pixels = halo_map.map_data.read(bitmap.lod1_size)
                if self.engine != "halo2alpha":
                    mip_pixels = zlib.decompress(mip_pixels)

                new_pixels += mip_pixels
                bitmap.lod1_size = len(mip_pixels)
                pix_off += bitmap.lod1_size

            meta.processed_pixel_data.STEPTREE = new_pixels

    def meta_to_tag_data(self, meta, tag_cls, tag_index_ref, **kwargs):
        engine     = self.engine
        tag_index  = self.tag_index

        if tag_cls == "bitm":
            # set the size of the compressed plate data to nothing
            meta.compressed_color_plate_data.STEPTREE = BytearrayBuffer()
            new_pixels_offset = 0

            # uncheck the prefer_low_detail flag and
            # set up the lod1_offset correctly.
            for bitmap in meta.bitmaps.STEPTREE:
                bitmap.lod1_offset = new_pixels_offset
                new_pixels_offset += bitmap.lod1_size

                bitmap.lod2_offset = bitmap.lod3_offset = bitmap.lod4_offset =\
                                     bitmap.lod5_offset = bitmap.lod6_offset = 0
                bitmap.lod2_size = bitmap.lod3_size = bitmap.lod4_size =\
                                   bitmap.lod5_size = bitmap.lod6_size = 0

        return meta

    def load_all_resource_maps(self, maps_dir=""):
        map_paths = {name: None for name in HALO2_MAP_TYPES[1:]}
        if self.engine == "halo2alpha":
            map_paths.pop("single_player_shared", None)

        if not maps_dir:
            maps_dir = dirname(self.filepath)

        # detect/ask for the map paths for the resource maps
        for map_name in sorted(map_paths.keys()):
            if self.maps.get(map_name) is not None:
                # map already loaded
                continue

            map_path = join(maps_dir, "%s.map" % map_name)

            if not exists(map_path): map_path += ".dtz"

            while map_path and not exists(map_path):
                map_path = askopenfilename(
                    initialdir=maps_dir,
                    title="Select the %s.map" % map_name,
                    filetypes=((map_name, "*.map"),
                               (map_name, "*.map.dtz"),
                               (map_name, "*.*")))

                if map_path:
                    maps_dir = dirname(map_path)
                else:
                    print("    You wont be able to extract from %s.map" % map_name)

            map_paths[map_name] = map_path

        for map_name in sorted(map_paths.keys()):
            map_path = map_paths[map_name]
            try:
                if self.maps.get(map_name) is None and map_path:
                    print("    Loading %s.map..." % map_name)
                    type(self)(self.maps).load_map(map_path, will_be_active=False)
                    print("        Finished")
            except Exception:
                print(format_exc())

    def setup_defs(self):
        if Halo2Map.defs:
            return

        Halo2Map.defs = defs = {}
        for fcc in ("ant!", "bitm", "hsc*", "pphy", "snd!", "trak", "ugh!"):
            try:
                fcc2 = fcc
                for char in "!#$*<>/ ":
                    fcc2 = fcc2.replace(char, "_")
                exec("from reclaimer.h2.defs.%s import %s_meta_def" %
                     (fcc2, fcc2))
                exec("defs['%s'] = %s_meta_def" % (fcc, fcc2))
            except Exception:
                print(format_exc())

    def get_meta_descriptor(self, tag_cls):
        tagdef = self.defs.get(tag_cls)
        if tagdef is not None:
            return tagdef.descriptor

    def load_map(self, map_path, **kwargs):
        autoload_resources = kwargs.get("autoload_resources", True)
        will_be_active = kwargs.get("will_be_active", True)
        HaloMap.load_map(self, map_path, **kwargs)
        tag_index = self.tag_index
        if self.engine == "halo2alpha":
            self.tag_index = h2_alpha_to_h1_tag_index(self.map_header, tag_index)
        else:
            self.tag_index = h2_to_h1_tag_index(self.map_header, tag_index)

        map_type = self.map_header.map_type.data - 1
        if map_type > 0 and map_type < 4:
            self.is_resource = True
            self.maps[HALO2_MAP_TYPES[map_type]] = self

        # get the sound_cache_file_gestalt meta
        try:
            if self.engine == "halo2vista":
                ugh__id = None
                for b in self.tag_index.tag_index:
                    if fourcc(b.class_1.data) == "ugh!":
                        ugh__id = b.id.tag_table_index
                        break

                self.ugh__meta = self.get_meta(ugh__id)
                if self.ugh__meta is None:
                    print("Could not read sound_cache_file_gestalt tag")
        except Exception:
            print(format_exc())
            print("Could not read sound_cache_file_gestalt tag")

        if autoload_resources and (will_be_active or not self.is_resource):
            self.load_all_resource_maps(dirname(map_path))

        self.map_data.clear_cache()

    def extract_tag_data(self, meta, tag_index_ref, **kw):
        extractor = data_extraction.h2_data_extractors.get(
            fourcc(tag_index_ref.class_1.data))
        if extractor is None:
            return "No extractor for this type of tag."
        kw['halo_map'] = self
        return extractor(meta, tag_index_ref.tag.tag_path, **kw)

    def get_meta(self, tag_id, reextract=False):
        if tag_id is None: return
        scnr_id = self.orig_tag_index.scenario_tag_id[0]
        tag_index_array = self.tag_index.tag_index
        shared_map    = self.maps.get("shared")

        # if we are given a 32bit tag id, mask it off
        tag_id &= 0xFFFF

        if self.engine != "halo2alpha":
            matg_id = self.orig_tag_index.globals_tag_id[0]
            sp_shared_map = self.maps.get("single_player_shared")

            if tag_id >= 10000 and shared_map is not self:
                if shared_map is None: return
                return shared_map.get_meta(tag_id, reextract)
            elif tag_id >= len(tag_index_array) and sp_shared_map is not self:
                if sp_shared_map is None: return
                return sp_shared_map.get_meta(tag_id, reextract)
        else:
            matg_id = None

        tag_index_ref = tag_index_array[tag_id]

        tag_cls = None
        if   tag_id == scnr_id: tag_cls = "scnr"
        elif tag_id == matg_id: tag_cls = "matg"
        elif tag_index_ref.class_1.enum_name not in ("<INVALID>", "NONE"):
            tag_cls = fourcc(tag_index_ref.class_1.data)

        desc = self.get_meta_descriptor(tag_cls)
        if desc is None or tag_cls is None:        return
        elif reextract:                            pass
        elif tag_id == scnr_id and self.scnr_meta: return self.scnr_meta
        elif tag_id == matg_id and self.matg_meta: return self.matg_meta
        elif tag_cls == "ugh!" and self.ugh__meta: return self.ugh__meta

        block = [None]
        offset = tag_index_ref.meta_offset - self.map_magic

        try:
            # read the meta data from the map
            desc['TYPE'].parser(
                desc, parent=block, attr_index=0, magic=self.map_magic,
                tag_index=tag_index_array, rawdata=self.map_data, offset=offset)
        except Exception:
            print(format_exc())
            return

        self.record_map_cache_read(tag_id, 0)  # cant get size quickly enough
        if self.map_cache_over_limit():
            self.clear_map_cache()

        self.inject_rawdata(block[0], tag_cls, tag_index_ref)
        if tag_cls == "ugh!":
            self.ugh__meta = block[0]

        return block[0]
