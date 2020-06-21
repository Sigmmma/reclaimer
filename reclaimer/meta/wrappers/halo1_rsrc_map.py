#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from struct import unpack
from traceback import format_exc

from reclaimer import data_extraction
from reclaimer.util import get_is_xbox_map
from reclaimer.meta.halo_map import map_header_def, tag_index_pc_def
from reclaimer.meta.halo1_rsrc_map import lite_halo1_rsrc_map_def as halo1_rsrc_map_def
from reclaimer.meta.wrappers.byteswapping import raw_block_def, byteswap_pcm16_samples
from reclaimer.meta.wrappers.map_pointer_converter import MapPointerConverter
from reclaimer.meta.wrappers.tag_index_manager import TagIndexManager
from reclaimer.meta.wrappers.halo_map import HaloMap

from supyr_struct.buffer import BytearrayBuffer, get_rawdata
from supyr_struct.field_types import FieldType

# this is ultra hacky, but it seems to be the only
# way to fix the tagid for the sounds resource map
sound_rsrc_id_map = {
    92: 7,  # sound\sfx\impulse\impacts\smallrock
    93: 8,  # sound\sfx\impulse\impacts\medrocks
    94: 9,  # sound\sfx\impulse\impacts\lrgrocks

    125: 12,  # sound\sfx\impulse\impacts\metal_chips
    126: 13,  # sound\sfx\impulse\impacts\metal_chip_med

    372: 61,  # sound\sfx\impulse\shellcasings\double_shell_dirt
    373: 62,  # sound\sfx\impulse\shellcasings\multi_shell_dirt
    374: 63,  # sound\sfx\impulse\shellcasings\single_shell_metal
    375: 64,  # sound\sfx\impulse\shellcasings\double_shell_metal
    376: 65,  # sound\sfx\impulse\shellcasings\multi_shell_metal

    1545: 264,  # sound\sfx\impulse\glass\glass_medium
    1546: 265,  # sound\sfx\impulse\glass\glass_large
    }

DEFAULT_LOC_TAG_COUNT = 176
DEFAULT_SOUNDS_TAG_COUNT = 376
DEFAULT_BITMAPS_TAG_COUNT = 853


# Tag classes aren't stored in the cache maps, so we need to
# have a cache of them somewhere. Might as well do it manually
loc_exts = {0:'font', 1:'font', 4:'hud_message_text', 56:'font', 58:'font'}

bitmap_exts = ('bitmap', ) * DEFAULT_BITMAPS_TAG_COUNT
sound_exts  = ('sound', ) * DEFAULT_SOUNDS_TAG_COUNT
loc_exts    = tuple(loc_exts.get(i, 'unicode_string_list')
                    for i in range(DEFAULT_LOC_TAG_COUNT))


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
    '''Generation 1 resource map'''

    # the original resource map header
    rsrc_map = None

    tag_classes = None
    tag_headers = None

    tag_defs_module = "reclaimer.hek.defs"
    tag_classes_to_load = ("bitm", "snd!", "font", "hmt ", "ustr")

    data_extractors = data_extraction.h1_data_extractors

    def __init__(self, maps=None):
        HaloMap.__init__(self, maps)
        self.setup_tag_headers()

    def load_map(self, map_path, **kwargs):
        map_data = get_rawdata(filepath=map_path, writable=False)

        resource_type = unpack("<I", map_data.read(4))[0]
        map_data.seek(0)
        rsrc_map = self.rsrc_map = halo1_rsrc_map_def.build(rawdata=map_data)

        self.orig_tag_index = rsrc_map.data.tags

        # check if this is a pc or ce cache. cant rip pc ones
        pth = self.orig_tag_index[0].tag.path if self.orig_tag_index else ""
        self.filepath = map_path

        ce_engine = ""
        for halo_map in self.maps.values():
            ce_engine = getattr(halo_map, "engine")
            if ce_engine:
                break

        rsrc_tag_count = len(rsrc_map.data.tags)
        if resource_type == 3 or (pth.endswith('__pixels') or
                                  pth.endswith('__permutations')):
            if ce_engine:
                self.engine = ce_engine
            else:
                self.engine = "halo1ce"
        elif ((resource_type == 1 and rsrc_tag_count == 1107) or
              (resource_type == 2 and rsrc_tag_count == 7192)):
            self.engine = "halo1pcdemo"
        else:
            self.engine = "halo1pc"

        # so we don't have to redo a lot of code, we'll make a
        # fake tag_index and map_header and just fill in info
        self.map_header = head = map_header_def.build()
        self.tag_index  = tags = tag_index_pc_def.build()
        self.map_magic  = 0
        self.map_data   = map_data
        self.is_resource = True

        self.index_magic = 0

        index_mul = 2
        if self.engine == "halo1pc" or resource_type == 3:
            index_mul = 1

        rsrc_tag_count = rsrc_tag_count // index_mul
        if resource_type == 1:
            head.map_name = "bitmaps"
            tag_classes, def_cls = bitmap_exts, 'bitmap'
        elif resource_type == 2:
            head.map_name = "sounds"
            tag_classes, def_cls = sound_exts, 'sound'
        elif resource_type == 3:
            head.map_name = "loc"
            tag_classes, def_cls = loc_exts, 'NONE'
            if self.engine == "halo1ce" and rsrc_tag_count != 176:
                # this is a custom edition loc.map, but we can't trust it to be accurate
                # if it contains a different number than 176 tags.
                tag_classes = ()
        else:
            raise ValueError("Unknown resource map type.")

        # allow an override to be specified before the map is loaded
        if self.tag_classes is None:
            self.tag_classes = tag_classes

        self.maps[head.map_name] = self
        self.map_name = head.map_name
        self.tag_classes += (def_cls, )*(rsrc_tag_count - len(self.tag_classes))
        tags.tag_index.extend(rsrc_tag_count)

        tags.scenario_tag_id = 0
        tags.tag_count = rsrc_tag_count
        # fill in the fake tag_index
        for i in range(rsrc_tag_count):
            j = i*index_mul
            if index_mul != 1:
                j += 1

            tag_ref = tags.tag_index[i]
            tag_ref.class_1.set_to(self.tag_classes[i])
            tag_ref.id = i

            tag_ref.meta_offset  = rsrc_map.data.tags[j].offset
            tag_ref.path = rsrc_map.data.tags[j].tag.path
            # not necessary to set it as indexed, as it isn't used
            # when extracting the tags, and leaving it as False
            # allows efinery to display pointer information, and
            # change the classes of tags in custom loc maps.
            #tag_ref.indexed      = 1

        # apparently this is needed(thank spv3/open sauce v4/neil
        #                           for fucking up resource maps)
        self.basic_deprotection()

        self.map_pointer_converter = MapPointerConverter((0, 0, 0xFFffFFff))
        self.tag_index_manager = TagIndexManager(tags.tag_index)
        self.snd_rsrc_tag_index_manager = TagIndexManager(
            tags.tag_index, sound_rsrc_id_map)
        self.clear_map_cache()

    def get_dependencies(self, meta, tag_id, tag_cls):
        if tag_cls != "snd!":
            return ()

        tag_id = meta.promotion_sound.id & 0xFFff
        if tag_id not in range(len(self.tag_index.tag_index)):
            return ()

        return [self.tag_index.tag_index[tag_id]]

    def is_indexed(self, tag_id):
        return True

    def get_meta(self, tag_id, reextract=False, **kw):
        '''Returns just the meta of the tag without any raw data.'''
        if tag_id is None:
            return

        # if we are given a 32bit tag id, mask it off
        tag_id &= 0xFFFF
        tag_index_ref = self.tag_index_manager.get_tag_index_ref(tag_id)
        if tag_index_ref is None:
            return
        tag_cls = dict(
            sound="snd!", bitmap="bitm", font="font",
            unicode_string_list="ustr", hud_message_text="hmt ").get(
                tag_index_ref.class_1.enum_name)

        kwargs = dict(parsing_resource=True)
        desc = self.get_meta_descriptor(tag_cls)
        if desc is None or self.engine not in ("halo1ce", "halo1yelo",
                                               "halo1vap"):
            return
        elif tag_cls != 'snd!':
            # the pitch ranges pointer in resource sound tags is invalid, so
            # for sounds we treat it as if we're parsing a tag(pointerless).
            # only provide a pointer converter for bitmap and loc maps.
            kwargs['map_pointer_converter'] = self.map_pointer_converter

        block = [None]

        self.record_map_cache_read(tag_id, 0)  # cant get size quickly enough
        if self.map_cache_over_limit():
            self.clear_map_cache()

        try:
            FieldType.force_little()
            desc['TYPE'].parser(
                desc, parent=block, attr_index=0, rawdata=self.map_data,
                tag_index_manager=self.snd_rsrc_tag_index_manager,
                tag_cls=tag_cls, root_offset=tag_index_ref.meta_offset,
                safe_mode=not kw.get("disable_safe_mode"),
                indexed=True, **kwargs)
            FieldType.force_normal()

            if not kw.get("ignore_rawdata", False):
                self.inject_rawdata(block[0], tag_cls, tag_index_ref)
        except Exception:
            print(format_exc())
            if not kw.get("allow_corrupt"):
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

        is_not_indexed = not self.is_indexed(tag_index_ref.id & 0xFFff)
        might_be_in_rsrc = engine in ("halo1pc", "halo1pcdemo",
                                      "halo1ce", "halo1yelo", "halo1vap")
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
                meta_offset = loc.rsrc_map.data.tags[meta_offset].tag.offset

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
                meta_offset = loc.rsrc_map.data.tags[meta_offset].tag.offset

            b = meta.string
            loc_data.seek(b.pointer + meta_offset)
            meta.string.data = loc_data.read(b.size).decode('utf-16-le')
        elif tag_cls == "snd!":
            # might need to get samples and permutations from the resource map
            is_pc = engine in ("halo1pc", "halo1pcdemo")
            is_ce = engine in ("halo1ce", "halo1yelo", "halo1vap")
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
                meta_offset = loc.rsrc_map.data.tags[meta_offset].tag.offset

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

    def generate_map_info_string(self):
        if hasattr(self.map_data, '__len__'):
            map_size = str(len(self.map_data))
        elif (hasattr(self.map_data, 'seek') and
              hasattr(self.map_data, 'tell')):
            curr_pos = self.map_data.tell()
            self.map_data.seek(0, 2)
            map_size = str(self.map_data.tell())
            self.map_data.seek(curr_pos)
        else:
            map_size = "unknown"

        return """%s
General:
    engine         == %s
    file size      == %s
    resource type  == %s

Header:
    tag count         == %s
    tag paths pointer == %s
    tag index pointer == %s""" % (
        self.filepath, self.engine, map_size, self.map_name,
        self.tag_index.tag_count, self.rsrc_map.data.tag_paths_pointer,
        self.rsrc_map.data.tag_headers_pointer)
