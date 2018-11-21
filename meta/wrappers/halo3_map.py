import zlib

from os.path import exists, join
from tkinter.filedialog import askopenfilename

from .halo_map import *
from reclaimer.h2.util import HALO2_MAP_TYPES, split_raw_pointer


class Halo3Map(HaloMap):
    ugh__meta = None

    def __init__(self, maps=None):
        HaloMap.__init__(self, maps)

    def load_all_resource_maps(self, maps_dir=""):
        map_paths = {name: None for name in HALO3_MAP_TYPES[1:]}
        if not maps_dir:
            maps_dir = dirname(self.filepath)

        # detect/ask for the map paths for the resource maps
        for map_name in sorted(map_paths.keys()):
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
                    print("    Loading %s.map..." % map_name)
                    type(self)(self.maps).load_map(map_path, will_be_active=False)
                    print("        Finished")
            except Exception:
                print(format_exc())

    def setup_defs(self):
        return
        if Halo3Map.defs:
            return

        Halo3Map.defs = defs = {}
        for fcc in ("bitm", ):
            try:
                fcc2 = fcc
                for char in "!#$*<>/ ":
                    fcc2 = fcc2.replace(char, "_")
                exec("from reclaimer.h3.defs.%s import %s_meta_def" %
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
        self.tag_index = h3_to_h1_tag_index(self.map_header, tag_index)

        map_type = self.map_header.map_type.data - 1
        if map_type > 0 and map_type < 4:
            self.is_resource = True
            self.maps[HALO3_MAP_TYPES[map_type]] = self

        if autoload_resources and (will_be_active or not self.is_resource):
            self.load_all_resource_maps(dirname(map_path))

        self.map_data.clear_cache()
