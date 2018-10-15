from reclaimer import data_extraction

from .byteswapping import raw_block_def, byteswap_pcm16_samples
from .halo_map import *


# Tag classes aren't stored in the cache maps, so we need to
# have a cache of them somewhere. Might as well do it manually
loc_exts = {0:'font', 1:'font', 4:'hud_message_text', 56:'font', 58:'font'}

bitmap_exts = ('bitmap',)*853
sound_exts  = ('sound',)*376
loc_exts    = tuple(loc_exts.get(i, 'unicode_string_list') for i in range(176))

def get_is_xbox_map(engine):
    return "xbox" in engine or engine in ("stubbs", "shadowrun_beta")


def inject_sound_data(map_data, rsrc_data, rawdata_ref, map_magic):
    if not rawdata_ref.size:
        rawdata_ref.data = b''
        return

    if rawdata_ref.flags.data_in_resource_map:
        data, ptr = rsrc_data, rawdata_ref.raw_pointer
    elif rawdata_ref.pointer == 0:
        data, ptr = map_data,  rawdata_ref.raw_pointer
    else:
        data, ptr = map_data,  rawdata_ref.pointer + map_magic

    data.seek(ptr)
    rawdata_ref.data = data.read(rawdata_ref.size)


class Halo1RsrcMap(HaloMap):
    tag_classes = None
    tag_headers = None

    def __init__(self, maps=None):
        HaloMap.__init__(self, maps)
        self.setup_tag_headers()

    def setup_tag_headers(self):
        if Halo1RsrcMap.tag_headers is not None:
            return

        tag_headers = Halo1RsrcMap.tag_headers = {}
        for def_id in ("bitm", "snd!", "font", "hmt ", "ustr"):
            h_desc, h_block = self.defs[def_id].descriptor[0], [None]
            h_desc['TYPE'].parser(h_desc, parent=h_block, attr_index=0)
            tag_headers[def_id] = bytes(
                h_block[0].serialize(buffer=BytearrayBuffer(),
                                     calc_pointers=False))

    def setup_defs(self):
        if Halo1RsrcMap.defs:
            return

        Halo1RsrcMap.defs = defs = {}
        for fcc in ("bitm", "snd!", "font", "hmt ", "ustr"):
            try:
                fcc2 = fcc.replace("!", "_").replace(" ", "_")
                exec("from reclaimer.os_v4_hek.defs.%s import %s_def" %
                     (fcc2, fcc2))
                exec("defs['%s'] = %s_def" % (fcc, fcc2))
            except Exception:
                print(format_exc())

    def extract_tag_data(self, meta, tag_index_ref, **kw):
        extractor = data_extraction.h1_data_extractors.get(
            fourcc(tag_index_ref.class_1.data))
        if extractor is None:
            return "No extractor for this type of tag."
        kw['halo_map'] = self
        return extractor(meta, tag_index_ref.tag.tag_path, **kw)

    def load_map(self, map_path, **kwargs):
        will_be_active = kwargs.get("will_be_active", True)
        with open(map_path, 'rb+') as f:
            map_data = PeekableMmap(f.fileno(), 0)

        resource_type = unpack("<I", map_data.read(4))[0]; map_data.seek(0)
        rsrc_head = resource_def.build(rawdata=map_data)

        # check if this is a pc or ce cache. cant rip pc ones
        pth = rsrc_head.tag_paths[0].tag_path
        self.filepath    = map_path
        self.engine = "halo1ce"
        if resource_type < 3 and not (pth.endswith('__pixels') or
                                      pth.endswith('__permutations')):
            self.engine = "halo1pc"

        # so we don't have to redo a lot of code, we'll make a
        # fake tag_index and map_header and just fill in info
        self.map_header = head = map_header_demo_def.build()
        self.tag_index  = tags = tag_index_pc_def.build()
        self.map_magic  = 0
        self.map_data   = map_data
        self.rsrc_header = rsrc_head
        self.is_resource = True

        head.version.set_to(self.engine)
        self.index_magic = 0

        index_mul = 2
        if self.engine == "halo1pc" or resource_type == 3:
            index_mul = 1

        head.map_name, tag_classes, def_cls = {
            1: ("bitmaps", bitmap_exts, 'bitmap'),
            2: ("sounds",  sound_exts,  'sound'),
            3: ("loc",     loc_exts,    'NONE')
            }[resource_type]

        # allow an override to be specified before the map is loaded
        if self.tag_classes is None:
            self.tag_classes = tag_classes

        self.maps[head.map_name] = self
        if will_be_active:
            self.maps["active"] = self

        rsrc_tag_count = len(rsrc_head.tag_paths)//index_mul
        self.tag_classes += (def_cls,)*(rsrc_tag_count - len(self.tag_classes))
        tags.tag_index.extend(rsrc_tag_count)
        tags.scenario_tag_id[:] = (0, 0)

        tags.tag_count = rsrc_tag_count
        # fill in the fake tag_index
        for i in range(rsrc_tag_count):
            j = i*index_mul
            if index_mul != 1:
                j += 1

            tag_ref = tags.tag_index[i]
            tag_ref.class_1.set_to(self.tag_classes[i])
            tag_ref.id[:] = (i, 0)

            tag_ref.meta_offset  = rsrc_head.tag_headers[j].offset
            tag_ref.indexed      = 1
            tag_ref.tag.tag_path = rsrc_head.tag_paths[j].tag_path
            tagid = (tag_ref.id[0], tag_ref.id[1])

        self.map_data.clear_cache()

    def get_dependencies(self, meta, tag_id, tag_cls):
        if tag_cls != "snd!":
            return ()

        tag_id = meta.promotion_sound.id[0]
        if tag_id == 0xFFFF: return ()

        tag_id = tag_id // 2
        if tag_id >= len(self.tag_index.tag_index): return ()

        return [self.tag_index.tag_index[tag_id]]

    def get_meta(self, tag_id, reextract=False):
        '''Returns just the meta of the tag without any raw data.'''
        if tag_id is None:
            return

        # if we are given a 32bit tag id, mask it off
        tag_id &= 0xFFFF
        if tag_id >= len(self.tag_index.tag_index):
            return
        tag_index_ref = self.tag_index.tag_index[tag_id]
        tag_cls = dict(
            sound="snd!", bitmap="bitm", font="font",
            unicode_string_list="ustr", hud_message_text="hmt ").get(
                tag_index_ref.class_1.enum_name)

        kwargs = dict(parsing_resource=True)
        desc = self.get_meta_descriptor(tag_cls)
        if desc is None or self.engine not in ("halo1ce", "halo1yelo"):
            return
        elif tag_cls != 'snd!':
            kwargs['magic'] = 0

        block = [None]

        self.record_map_cache_read(tag_id, 0)  # cant get size quickly enough
        if self.map_cache_over_limit():
            self.clear_map_cache()

        try:
            FieldType.force_little()
            desc['TYPE'].parser(
                desc, parent=block, attr_index=0, rawdata=self.map_data,
                tag_index=self.rsrc_header.tag_paths, tag_cls=tag_cls,
                root_offset=tag_index_ref.meta_offset, **kwargs)
            FieldType.force_normal()
            self.inject_rawdata(block[0], tag_cls, tag_index_ref)
        except Exception:
            print(format_exc())
            return

        return block[0]

    def meta_to_tag_data(self, meta, tag_cls, tag_index_ref, **kwargs):
        magic      = self.map_magic
        engine     = self.engine
        map_data   = self.map_data
        tag_index  = self.tag_index
        is_xbox = get_is_xbox_map(engine)

        if tag_cls == "bitm":
            # set the size of the compressed plate data to nothing
            meta.compressed_color_plate_data.STEPTREE = BytearrayBuffer()

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
                bitmap.bitmap_data_pointer = bitmap.base_address = 0

        elif tag_cls == "snd!":
            meta.maximum_bend_per_second = meta.maximum_bend_per_second ** 30
            for pitch_range in meta.pitch_ranges.STEPTREE:
                for permutation in pitch_range.permutations.STEPTREE:
                    if permutation.compression.enum_name == "none":
                        # byteswap pcm audio
                        byteswap_pcm16_samples(permutation.samples)

        return meta

    def inject_rawdata(self, meta, tag_cls, tag_index_ref):
        bitmaps = self.maps.get("bitmaps")
        sounds  = self.maps.get("sounds")
        loc     = self.maps.get("loc")

        magic  = self.map_magic
        engine = self.engine

        map_data = self.map_data

        try:   bitmap_data = bitmaps.map_data
        except Exception:    bitmap_data = None
        try:   sound_data = sounds.map_data
        except Exception:   sound_data = None
        try:   loc_data = loc.map_data
        except Exception: loc_data = None

        is_not_indexed = not self.is_indexed(tag_index_ref.id[0])
        might_be_in_rsrc = engine in ("halo1pc", "halo1pcdemo",
                                      "halo1ce", "halo1yelo")
        might_be_in_rsrc &= not self.is_resource

        # get some rawdata that would be pretty annoying to do in the parser
        if tag_cls == "bitm":
            # grab bitmap data from map
            new_pixels = BytearrayBuffer()

            # to enable compatibility with my bitmap converter we'll set the
            # base address to a certain constant based on the console platform
            is_xbox = get_is_xbox_map(engine)
            for bitmap in meta.bitmaps.STEPTREE:
                pixel_data = map_data
                if might_be_in_rsrc and bitmap.flags.data_in_resource_map:
                    pixel_data = bitmap_data

                if pixel_data is None: return

                # grab the bitmap data from this map(no magic used)
                pixel_data.seek(bitmap.pixels_offset)
                new_pixels += pixel_data.read(bitmap.pixels_meta_size)

                bitmap.base_address = 1073751810 * is_xbox

            meta.processed_pixel_data.STEPTREE = new_pixels
        elif tag_cls == "font":
            # might need to grab pixel data from resource map
            meta_offset = tag_index_ref.meta_offset

            if is_not_indexed:
                return meta
            elif not self.is_resource:
                if loc is None or loc.map_header is None: return
                meta_offset = loc.rsrc_header.tag_headers[meta_offset].offset

            if loc_data is None: return

            loc_data.seek(meta.pixels.pointer + meta_offset)
            meta.pixels.data = loc_data.read(meta.pixels.size)
        elif tag_cls == "hmt ":
            # might need to grab string data from resource map
            meta_offset = tag_index_ref.meta_offset

            if is_not_indexed:
                return meta
            elif not self.is_resource:
                if loc is None or loc.map_header is None: return
                meta_offset = loc.rsrc_header.tag_headers[meta_offset].offset

            b = meta.string
            loc_data.seek(b.pointer + meta_offset)
            meta.string.data = loc_data.read(b.size).decode('utf-16-le')
        elif tag_cls == "snd!":
            # might need to get samples and permutations from the resource map
            is_pc = engine in ("halo1pc", "halo1pcdemo")
            is_ce = engine in ("halo1ce", "halo1yelo")
            if not(is_pc or is_ce):
                return meta
            elif sound_data is None:
                return

            # ce tagpaths are in the format:  path__permutations
            #     ex: sound\sfx\impulse\coolant\enter_water__permutations
            #
            # pc tagpaths are in the format:  path__pitchrange__permutation
            #     ex: sound\sfx\impulse\coolant\enter_water__0__0
            other_data = map_data
            sound_magic = 0 - magic
            # DO NOT optimize this section. The logic is like this on purpose
            if is_pc:
                pass
            elif self.is_resource:
                other_data = sound_data
                sound_magic = tag_index_ref.meta_offset + meta.get_size()
            elif sounds is None:
                return

            for pitches in meta.pitch_ranges.STEPTREE:
                for perm in pitches.permutations.STEPTREE:
                    for b in (perm.samples, perm.mouth_data, perm.subtitle_data):
                        inject_sound_data(other_data, sound_data, b, sound_magic)

        elif tag_cls == "ustr":
            # might need to grab string data from resource map
            meta_offset = tag_index_ref.meta_offset

            if is_not_indexed:
                return meta
            elif not self.is_resource:
                if loc is None or loc.map_header is None: return
                meta_offset = loc.rsrc_header.tag_headers[meta_offset].offset

            string_blocks = meta.strings.STEPTREE

            if len(string_blocks):
                desc = string_blocks[0].get_desc('STEPTREE')
                parser = desc['TYPE'].parser

            try:
                FieldType.force_little()
                for b in string_blocks:
                    parser(desc, None, b, 'STEPTREE',
                           loc_data, meta_offset, b.pointer)
                FieldType.force_normal()
            except Exception:
                print(format_exc())
                FieldType.force_normal()
                raise
