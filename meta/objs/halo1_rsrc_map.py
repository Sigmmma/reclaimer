import os

from collections import OrderedDict
from traceback import format_exc

from array import array
from reclaimer.common_descs import rawdata_ref_struct
from reclaimer.field_types import FieldType, RawdataRef, Reflexive, TagRef
from supyr_struct.defs.block_def import BlockDef
from supyr_struct.tag import Tag
from ..wrappers.map_pointer_converter import MapPointerConverter

empty_rawdata_def = BlockDef("samples_stub", INCLUDE=rawdata_ref_struct)

REMOVED_RSRC_TAG_DIR = "!rem\\"


def set_tag_meta_pointers(block, meta_pointer, raw_pointer_base=0):
    if not (hasattr(block, "desc") and hasattr(block, "__iter__")):
        return meta_pointer, raw_pointer_base

    item_indices = list(range(len(block)))
    if hasattr(block, "STEPTREE"):
        item_indices.append("STEPTREE")

    for i in item_indices:
        typ = block.get_desc("TYPE", i)
        sub_block = block[i]
        if typ == RawdataRef:
            if getattr(sub_block, "data", None):
                orig_size = sub_block.size
                # pad data streams to multiples of 4 bytes for alignment
                sub_block.data += b'\x00' * ((4 - (sub_block.size % 4)) % 4)
                sub_block.size = orig_size

            sub_block.id = sub_block.pointer = 0
            if not sub_block.flags.data_in_resource_map:
                sub_block.pointer = meta_pointer
                sub_block.raw_pointer = meta_pointer + raw_pointer_base
                meta_pointer += len(getattr(sub_block, "data", ()))
            else:
                raw_pointer_base += sub_block.size

        elif typ == TagRef:
            sub_block.filepath = ""
            sub_block.id = 0xFFffFFff
        elif typ == Reflexive:
            sub_block.pointer = meta_pointer
            sub_block.id = 0
            if sub_block.STEPTREE:
                meta_pointer += sub_block.size * sub_block.STEPTREE[0].SIZE

        meta_pointer, raw_pointer_base = set_tag_meta_pointers(
            sub_block, meta_pointer, raw_pointer_base)

    meta_pointer += (4 - (meta_pointer % 4)) % 4
    return meta_pointer, raw_pointer_base


class Halo1RsrcMapTag(Tag):
    defs = ()
    tag_path_indices = ()

    _orig_tag_count = 0

    def __init__(self, *args, **kwargs):
        Tag.__init__(self, *args, **kwargs)
        self.map_pointer_converter = MapPointerConverter((0, 0, 0xFFffFFff))
        self.setup_defs()

        try:
            rsrc_tags = self.data.tags
        except Exception:
            rsrc_tags = ()
        self.tag_path_indices = {rsrc_tags[i].tag.path.lower(): i
                                 for i in range(len(rsrc_tags))}

    def parse(self, *args, **kwargs):
        Tag.parse(self, *args, **kwargs)
        try:
            self._orig_tag_count = len(self.data.tags)
        except Exception:
            self._orig_tag_count = 0

    @property
    def orig_tag_count(self):
        return self._orig_tag_count

    def setup_defs(self):
        if Halo1RsrcMapTag.defs:
            return

        Halo1RsrcMapTag.defs = defs = {}
        for fcc in ("bitm", "snd!", "font", "hmt ", "ustr"):
            try:
                fcc2 = fcc.replace("!", "_").replace(" ", "_")
                exec("from reclaimer.hek.defs.%s import %s_def" %
                     (fcc2, fcc2))
                exec("defs['%s'] = %s_def" % (fcc, fcc2))
            except Exception:
                print(format_exc())

    def load_resource_tags(self, *tags_dirs, ignored=(),
                           tag_paths_to_load_by_tags_dirs=()):
        tag_paths_to_load_by_tags_dirs = dict(tag_paths_to_load_by_tags_dirs)
        loaded_tags = OrderedDict()
        usable_defs = {}
        rsrc_type = self.data.resource_type.enum_name
        if rsrc_type == "bitmaps":
            usable_defs["bitmap"] = self.defs.get("bitm")
        elif rsrc_type == "sounds":
            usable_defs["sound"] = self.defs.get("snd!")
        elif rsrc_type == "strings":
            usable_defs["font"] = self.defs.get("font")
            usable_defs["hud_message_text"] = self.defs.get("hmt ")
            usable_defs["unicode_string_list"] = self.defs.get("ustr")

        for tags_dir in tags_dirs:
            tags_to_load = []
            tag_paths_to_load_by_tags_dirs[tags_dir] = tags_to_load
            for root, dirs, files in os.walk(tags_dir):
                for filename in sorted(files):
                    filepath = os.path.join(root, filename)
                    tag_path, ext = os.path.splitext(
                        filepath.lower().split(tags_dir.lower())[-1])
                    ext = ext.strip(".")

                    if usable_defs.get(ext) and (tag_path not in ignored and
                                                 tag_path not in loaded_tags):
                        tags_to_load.append(tag_path + "." + ext)

        for tags_dir, tag_paths in tag_paths_to_load_by_tags_dirs.items():
            for tag_path in tag_paths:
                try:
                    filepath = os.path.join(tags_dir, tag_path)
                    tag_path, ext = os.path.splitext(
                        filepath.lower().split(tags_dir.lower())[-1])
                    ext = ext.strip(".")
                    loaded_tags[tag_path] = usable_defs[ext].build(
                        filepath=filepath)
                except Exception:
                    print(format_exc())
                    print("Could not load: '%s'" % tag_path)

        return loaded_tags

    def set_pointers(self, offset=0):  # offset is unused
        resource_tags = self.data.tags
        curr_data_pointer = 16
        curr_path_pointer = 0
        for i in range(len(resource_tags)):
            tag_head = resource_tags[i]
            tag_head.path_offset = curr_path_pointer
            curr_path_pointer += len(tag_head.tag.path) + 1

            # align the data pointer
            curr_data_pointer += ((4 - (curr_data_pointer % 4)) % 4)
            if i >= self.orig_tag_count:
                # only adjust the data offset of new tags
                tag_head.offset = curr_data_pointer

            curr_data_pointer = tag_head.offset + tag_head.size

        curr_data_pointer += (4 - (curr_data_pointer % 4)) % 4
        self.data.tag_paths_pointer   = curr_data_pointer
        self.data.tag_headers_pointer = (curr_data_pointer + curr_path_pointer)

    def update_bitmap(self, tag_path, new_tag):
        if self.data.resource_type.enum_name != "bitmaps":
            raise TypeError("Cannot add bitmap to %s resource map" %
                            self.data.resource_type.enum_name)

        meta_head_i = self.tag_path_indices.get(tag_path)
        pixel_head_i = self.tag_path_indices.get(tag_path + "__pixels")
        if None in (meta_head_i, pixel_head_i):
            raise ValueError("'%s' is not in resource map" % tag_path)
        elif self.defs.get("bitm", None) is None:
            raise TypeError("bitmap tag definition is not loaded.")

        pix_head = self.data.tags[pixel_head_i]
        new_bitmaps = new_tag.data.tagdata.bitmaps.STEPTREE
        new_pixels = new_tag.data.tagdata.processed_pixel_data.data

        desc  = self.defs['bitm'].descriptor[1]
        parent = [None]
        with FieldType.force_little:
            desc['TYPE'].parser(
                desc, parent=parent, attr_index=0, parsing_resource=True,
                rawdata=self.data.tags[meta_head_i].tag.data,
                map_pointer_converter=self.map_pointer_converter)
            orig_bitmaps = parent[0].bitmaps.STEPTREE

        if len(orig_bitmaps) != len(new_bitmaps):
            raise ValueError(
                "%s:\nReplacement bitmap count(%s) does not match original(%s)"
                % (tag_path, len(new_bitmaps), len(orig_bitmaps)))

        for i in range(len(new_bitmaps)):
            new_bitmap = new_bitmaps[i]
            orig_bitmap = orig_bitmaps[i]
            for attr_name in ("width", "height", "depth", "type", "format"):
                new_bitm_attr = new_bitmap[attr_name]
                orig_bitm_attr = orig_bitmap[attr_name]
                if attr_name in ("type", "format"):
                    new_bitm_attr = new_bitm_attr.enum_name
                    orig_bitm_attr = orig_bitm_attr.enum_name

                if new_bitm_attr != orig_bitm_attr:
                    raise ValueError(
                        "%s:\nReplacement bitmap %s(%s) does not match original(%s)"
                        % (tag_path, attr_name, new_bitm_attr, orig_bitm_attr))

        if len(new_bitmaps) == 1 and len(pix_head.tag.data) > len(new_pixels):
            # super hacky, but it'll work for now. copy the end of the mipmap
            # data from the old bitmap to the end of the new pixel data
            new_pixels += pix_head.tag.data[len(new_pixels): ]

        if len(pix_head.tag.data) != len(new_pixels):
            raise ValueError(
                "%s:\nReplacement data length(%s) does not match original(%s)"
                % (tag_path, len(new_pixels), len(pix_head.tag.data)))
        else:
            pix_head.tag.data = new_pixels

    def _add_bitmap(self, tag_path, new_tag, base_pointer, depreciate):
        tag_data = new_tag.data.tagdata
        rsrc_tags = self.data.tags
        src_pixels = tag_data.processed_pixel_data.data

        # add headers for this tag
        curr_idx = len(rsrc_tags)
        rsrc_tags.extend(2)
        meta_head, pix_head = rsrc_tags[-1], rsrc_tags[-2]

        for i in range(len(tag_data.sequences.STEPTREE)):
            seq = tag_data.sequences.STEPTREE[-1]
            if seq.sprites.STEPTREE:
                seq.first_bitmap_index = 0
                seq.bitmap_count = 0
            elif not (seq.first_bitmap_index in range(tag_data.bitmaps.size)):
                tag_data.sequences.STEPTREE.pop(-1)
                continue

            break

        # fill out each bitmap block's flags, unknowns, and sizes
        for bitmap in tag_data.bitmaps.STEPTREE:
            min_dim = 4 if "dxt" in bitmap.format.enum_name else 1
            w, h, d = bitmap.width, bitmap.height, bitmap.depth
            pix_chunk_size = 0
            bpp = 8
            if bitmap.format.data in (3, 6, 8, 9):
                bpp = 16
            elif bitmap.format.data in (10, 11):
                bpp = 32
            elif bitmap.format.data == 14:
                bpp = 4

            for i in range(bitmap.mipmaps + 1):
                pix_chunk_size += (w * h * d * bpp) // 8
                w = max(w >> 1, 1)
                h = max(h >> 1, 1)
                d = max(d >> 1, 1)
                w += (min_dim - (w % min_dim)) % min_dim
                h += (min_dim - (h % min_dim)) % min_dim

            if bitmap.type.enum_name == "cubemap":
                pix_chunk_size *= 6

            bitmap.flags.data_in_resource_map = True
            bitmap.flags.prefer_low_detail = True

            bitmap.pixels_meta_size = pix_chunk_size
            bitmap.bitmap_data_pointer = 0xFFffFFff
            bitmap.bitmap_id_unknown1 = 0  # don't know how to set this
            bitmap.bitmap_id_unknown2 = bitmap.base_address = 0

        # fill out each bitmap block pixel data pointer and copy the pixels
        # from each bitmap out of the src_pixels and piece them together
        pixel_off = 0
        combined_pixels = b''
        for bitmap in tag_data.bitmaps.STEPTREE:
            combined_pixels += src_pixels[
                bitmap.pixels_offset:
                bitmap.pixels_offset + bitmap.pixels_meta_size]

            bitmap.pixels_offset = base_pointer + pixel_off
            pixel_off += bitmap.pixels_meta_size

        if tag_path in self.tag_path_indices:
            old_idx = self.tag_path_indices[tag_path]
            old_meta_head, old_pix_head = rsrc_tags[old_idx], rsrc_tags[old_idx - 1]
            if not depreciate or old_pix_head.tag.data == combined_pixels:
                # same pixel data. optimize away
                del rsrc_tags[-2: ]
                return None, None

            old_pix_head.tag.path = REMOVED_RSRC_TAG_DIR + tag_path + "__pixels"
            old_meta_head.tag.path = REMOVED_RSRC_TAG_DIR + tag_path

        # null these to prevent them from screwing with the size calculations
        tag_data.compressed_color_plate_data.data = b""
        tag_data.processed_pixel_data.data = b""

        pix_head.tag.data = combined_pixels
        return pix_head, meta_head

    def _add_sound(self, tag_path, new_tag, base_pointer, depreciate):
        tag_data = new_tag.data.tagdata
        rsrc_tags = self.data.tags
        if tag_data.promotion_sound.filepath:
            # not gonna bother adding sounds with dependencies
            return None, None
        elif tag_path in self.tag_path_indices:
            return None, None

        max_bend = tag_data.maximum_bend_per_second
        if max_bend != 0:
            tag_data.maximum_bend_per_second = 1 / (max_bend ** 30)

        samples = b''
        # add headers for this tag
        rsrc_tags.extend(2)
        meta_head, samp_head = rsrc_tags[-1], rsrc_tags[-2]

        for pr in tag_data.pitch_ranges.STEPTREE:
            pr.unknown0 = 1.0
            pr.unknown1 = pr.unknown2 = -1
            for perm in pr.permutations.STEPTREE:
                perm.unknown1 = 0
                perm.unknown3 = perm.unknown2 = 0xFFffFFff
                sample_data = perm.samples.data
                if perm.compression.enum_name == "none":
                    sample_data = array(">h", sample_data)
                    sample_data.byteswap()
                    sample_data = sample_data.tobytes()

                perm.samples.flags.data_in_resource_map = True
                perm.mouth_data.flags.data_in_resource_map = False
                perm.subtitle_data.flags.data_in_resource_map = False

                perm.samples.raw_pointer = base_pointer
                base_pointer += len(sample_data)

                samples += sample_data
                perm.samples = empty_rawdata_def.build(initdata=perm.samples)

        samp_head.tag.data = samples

        return samp_head, meta_head

    def add_tag(self, tag_path, new_tag, base_pointer=None, depreciate=False):
        tag_data = new_tag.data.tagdata
        if base_pointer is None:
            base_pointer = self.data.tag_paths_pointer

        # make sure the base pointer is aligned
        base_pointer += ((4 - (base_pointer % 4)) % 4)

        rsrc_type = self.data.resource_type.enum_name
        raw_head = meta_head = None
        
        if rsrc_type == "bitmaps":
            raw_head, meta_head = self._add_bitmap(tag_path, new_tag,
                                                   base_pointer, depreciate)
            if not (raw_head and meta_head):
                return base_pointer
            raw_head.tag.path = tag_path + "__pixels"
            set_tag_meta_pointers(tag_data, tag_data.SIZE)

        elif rsrc_type == "sounds":
            if tag_data.promotion_sound.filepath:
                # not gonna bother adding sounds with dependencies
                raise TypeError("Cannot add sound tag with promotion sound.")

            raw_head, meta_head = self._add_sound(tag_path, new_tag,
                                                  base_pointer, depreciate)
            if not (raw_head and meta_head):
                return base_pointer
            raw_head.tag.path = tag_path + "__permutations"

            set_tag_meta_pointers(tag_data, 0, tag_data.SIZE)
        else:
            set_tag_meta_pointers(tag_data, tag_data.SIZE)

        # fill out the tag headers
        meta_head.tag.path = tag_path
        with FieldType.force_little:
            meta_head.tag.data = tag_data.serialize()

        base_pointer += meta_head.size
        base_pointer += ((4 - (base_pointer % 4)) % 4)
        if raw_head:
            base_pointer += raw_head.size

        return base_pointer + ((4 - (base_pointer % 4)) % 4)
