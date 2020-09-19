#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from array import array
from reclaimer.constants import TYPE_CUBEMAP, CUBEMAP_PADDING, BITMAP_PADDING,\
     FORMAT_NAME_MAP, TYPE_NAME_MAP, FORMAT_P8_BUMP
from reclaimer.bitmaps.p8_palette import HALO_P8_PALETTE
from reclaimer.hek.defs.objs.tag import HekTag

try:
    import arbytmap as ab

    if not hasattr(ab, "FORMAT_P8_BUMP"):
        ab.FORMAT_P8_BUMP = "P8-BUMP"

        """ADD THE P8 FORMAT TO THE BITMAP CONVERTER"""
        ab.register_format(format_id=ab.FORMAT_P8_BUMP, depths=(8,8,8,8))
except (ImportError, AttributeError):
    ab = None


class BitmTag(HekTag):
    tex_infos = ()
    p8_palette = None

    def __init__(self, *args, **kwargs):
        HekTag.__init__(self, *args, **kwargs)
        self.p8_palette = HALO_P8_PALETTE

    def bitmap_count(self, new_value=None):
        if new_value is None:
            return self.data.tagdata.bitmaps.size
        self.data.tagdata.bitmaps.size = new_value

    def bitmap_width(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.tagdata.bitmaps.bitmaps_array[b_index].width
        self.data.tagdata.bitmaps.bitmaps_array[b_index].width = new_value

    def bitmap_height(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.tagdata.bitmaps.bitmaps_array[b_index].height
        self.data.tagdata.bitmaps.bitmaps_array[b_index].height = new_value

    def bitmap_depth(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.tagdata.bitmaps.bitmaps_array[b_index].depth
        self.data.tagdata.bitmaps.bitmaps_array[b_index].depth = new_value

    def bitmap_mipmaps_count(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.tagdata.bitmaps.bitmaps_array[b_index].mipmaps
        self.data.tagdata.bitmaps.bitmaps_array[b_index].mipmaps = new_value

    def bitmap_type(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.tagdata.bitmaps.bitmaps_array[b_index].type.data
        self.data.tagdata.bitmaps.bitmaps_array[b_index].type.data = new_value

    def bitmap_format(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.tagdata.bitmaps.bitmaps_array[b_index].format.data
        self.data.tagdata.bitmaps.bitmaps_array[b_index].format.data = new_value

    def fix_top_format(self):
        if len(self.data.tagdata.bitmaps.bitmaps_array) <= 0:
            self.data.tagdata.format.data = "color_key_transparency"

        # Why can't get_name get the name of the current option?
        pixel_format = self.data.tagdata.bitmaps.bitmaps_array[0].format.get_name(
            self.data.tagdata.bitmaps.bitmaps_array[0].format.data)

        top_format = "color_key_transparency"
        if pixel_format in ("a8", "y8", "ay8", "a8y8"):
            top_format = "monochrome"
        elif pixel_format in ("r5g6b5", "a1r5g5b5", "a4r4g4b4"):
            top_format = "color_16bit"
        elif pixel_format in ("x8r8g8b8", "a8r8g8b8", "p8_bump"):
            top_format = "color_32bit"
        elif pixel_format == "dxt1":
            top_format = "color_key_transparency"
        elif pixel_format == "dxt3":
            top_format = "explicit_alpha"
        elif pixel_format == "dxt5":
            top_format = "interpolated_alpha"

        self.data.tagdata.format.set_to(top_format)

    def bitmap_width_height_depth(self, b_index=0, new_value=None):
        bitmap = self.data.tagdata.bitmaps.bitmaps_array[b_index]
        if new_value is None:
            return(bitmap.width, bitmap.height, bitmap.depth)
        bitmap.width, bitmap.height, bitmap.depth = (
            new_value[0], new_value[1], new_value[2])

    def bitmap_flags(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.tagdata.bitmaps.bitmaps_array[b_index].flags
        self.data.tagdata.bitmaps.bitmaps_array[b_index].flags = new_value

    def bitmap_base_address(self, b_index=0, new_value=None):
        bitm = self.data.tagdata.bitmaps.bitmaps_array[b_index]
        if new_value is None:
            return(bitm.base_address)
        bitm.base_address=new_value

    def bitmap_data_offset(self, b_index=0, new_value=None):
        bitm = self.data.tagdata.bitmaps.bitmaps_array[b_index]
        if new_value is None:
            return(bitm.pixels_offset)
        bitm.pixels_offset=new_value

    def registration_point_x(self, b_index=0, new_value=None):
        bitm = self.data.tagdata.bitmaps.bitmaps_array[b_index]
        if new_value is None:
            return bitm.registration_point_x
        bitm.registration_point_x = new_value

    def registration_point_y(self, b_index=0, new_value=None):
        bitm = self.data.tagdata.bitmaps.bitmaps_array[b_index]
        if new_value is None:
            return bitm.registration_point_y
        bitm.registration_point_y = new_value

    def registration_point_xy(self, b_index=0, new_value=None):
        bitm = self.data.tagdata.bitmaps.bitmaps_array[b_index]
        if new_value is None:
            return(bitm.registration_point_x,
                   bitm.registration_point_y)
        bitm.registration_point_x, bitm.registration_point_y = new_value[0],\
                                                               new_value[1]

    @property
    def is_xbox_bitmap(self):
        # we only need to check the first bitmap
        if not self.bitmap_count(): return False
        return self.bitmap_base_address() == 1073751810

    def is_power_of_2_bitmap(self, b_index=0):
        if not self.bitmap_count(): return False
        return self.bitmap_flags(b_index).power_of_2_dim

    def is_compressed_bitmap(self, b_index=0):
        if not self.bitmap_count(): return False
        return self.bitmap_flags(b_index).compressed

    def swizzled(self, b_index=0, new_flag=None):
        if new_flag is None:
            if not self.bitmap_count(): return False
            return self.bitmap_flags(b_index).swizzled
        if not self.bitmap_count(): return
        self.bitmap_flags(b_index).swizzled = new_flag

    def color_plate_data_bytes_size(self, new_value=None):
        if new_value is None:
            return(self.data.tagdata.compressed_color_plate_data.size)
        self.data.tagdata.compressed_color_plate_data.size = new_value

    def pixel_data_bytes_size(self, new_value=None):
        if new_value is None:
            return self.data.tagdata.processed_pixel_data.size
        self.data.tagdata.processed_pixel_data.size = new_value

    def set_platform(self, saveasxbox):
        '''changes different things to set the platform to either PC or Xbox'''
        # read each of the bitmap blocks
        for b_index in range(self.bitmap_count()):
            bitmap = self.data.tagdata.bitmaps.bitmaps_array[b_index]

            bitmap.flags.prefer_low_detail = saveasxbox

            '''base_address is the ONLY discernable difference
            between a bitmap made by arsenic from a PC map, and
            a bitmap made by arsenic from an original XBOX map'''
            if saveasxbox:
                # change some miscellaneous variables
                bitmap.pixels = 18
                bitmap.bitmap_data_pointer = 0xFFFFFFFF
                bitmap.base_address = 1073751810
            else:
                bitmap.base_address = 0

        if not saveasxbox:
            return

        # if Xbox, reset these structure variable's all to 0
        # since xbox doesn't like them being non-zero
        tagdata = self.data.tagdata
        tagdata.compressed_color_plate_data.flags.data = 0
        tagdata.processed_pixel_data.flags.data = 0
        for i in (2,3):
            tagdata.compressed_color_plate_data[i] = 0
            tagdata.processed_pixel_data[i] = 0

        for i in (1,2):
            tagdata.sequences[i] = 0
            tagdata.bitmaps[i] = 0

        # swap the order of the cubemap faces
        # and mipmaps if saving to xbox format
        self.change_sub_bitmap_ordering(saveasxbox)

    def change_sub_bitmap_ordering(self, saveasxbox):
        '''Used to change the mipmap and cube face ordering.
        On pc all highest resolution faces are first, then
        the next highest resolution mipmap set. On xbox it's
        all of a face's mipmaps before any of the other faces.

        DO NOT UNDER ANY CIRCUMSTANCES CALL THIS FUNCTION
        IF PADDING HAS ALREADY BEEN ADDED TO A BITMAP'''

        raw_bitmap_data = self.data.tagdata.processed_pixel_data.data

        # loop over each of the bitmap blocks
        for b_index in range(self.bitmap_count()):
            if self.bitmap_type(b_index) == TYPE_CUBEMAP:
                mipmap_count = self.bitmap_mipmaps_count(b_index) + 1
                tex_block = raw_bitmap_data[b_index]

                # this will be used to copy values from
                template = tex_block.__copy__()

                # this is used to keep track of which index
                # we're placing the new pixel array into
                i = 0

                '''since we also want to swap the second and third
                cubemap faces we can do that easily like this.
                xbox has the second and third cubemap faces swapped
                with each other compared to pc. IDFKY'''
                for face in (0, 2, 1, 3, 4, 5):
                    for mip in range(0, mipmap_count*6, 6):
                        '''get the block we want from the original
                        layout and place it in its new position'''
                        if saveasxbox:
                            tex_block[i] = template[mip + face]
                        else:
                            tex_block[mip + face] = template[i]
                        i += 1

    def add_bitmap_padding(self, save_as_xbox):
        '''This function will create and apply padding to each of the
        bitmaps in the tag to make it XBOX compatible. This function will
        also add the number of bytes of padding to the internal offsets'''

        """The offset of each bitmap's pixel data needs to be increased by
        the padding of all the bitmaps before it. This variable will be
        used for knowing the total amount of padding before each bitmap.

        DO NOT RUN IF A BITMAP ALREADY HAS PADDING."""
        total_data_size = 0
        if ab is None:
            raise NotImplementedError(
                "Arbytmap is not loaded. Cannot add padding.")

        for i in range(self.bitmap_count()):
            sub_bitmap_count = 1
            if self.bitmap_type(i) == TYPE_CUBEMAP:
                sub_bitmap_count = 6

            pixel_data_block = self.data.tagdata.processed_pixel_data.data[i]

            # apply the offset to the tag
            self.bitmap_data_offset(i, total_data_size)

            if save_as_xbox or self.bitmap_format(i) == FORMAT_P8_BUMP:
                # calculate how much padding to add to the xbox bitmaps
                bitmap_pad, cubemap_pad = self.get_padding_size(i)

                # if this bitmap has padding on each of the sub-bitmaps
                if cubemap_pad:
                    mipmap_count = self.bitmap_mipmaps_count(i) + 1
                    for j in range(0, 6*(mipmap_count + 1), mipmap_count + 1):
                        pad = bytearray(cubemap_pad)
                        if isinstance(pixel_data_block[0], array):
                            pad = array('B', pad)
                        pixel_data_block.insert(j + mipmap_count, pad)

                # add the main padding to the end of the bitmap block
                pad = bytearray(bitmap_pad)
                if isinstance(pixel_data_block[0], array):
                    pad = array('B', pad)
                pixel_data_block.append(pad)

            # add the number of bytes this bitmap is to the
            # total bytes so far(multiple by sub-bitmap count)
            for pixel_data in pixel_data_block:
                if isinstance(pixel_data, array):
                    total_data_size += len(pixel_data) * pixel_data.itemsize
                else:
                    total_data_size += len(pixel_data)

        # update the total number of bytes of pixel data
        # in the tag by all the padding that was added
        self.pixel_data_bytes_size(total_data_size)

    def get_bitmap_size(self, b_index):
        '''Given a bitmap index, this function will
        calculate how many bytes the data takes up.
        THIS FUNCTION WILL NOT TAKE INTO ACCOUNT THE NUMBER OF SUB-BITMAPS'''
        if ab is None:
            raise NotImplementedError(
                "Arbytmap is not loaded. Cannot get bitmap size.")

        w, h, d, = self.bitmap_width_height_depth(b_index)
        fmt = FORMAT_NAME_MAP[self.bitmap_format(b_index)]

        bytes_count = 0
        for mipmap in range(self.bitmap_mipmaps_count(b_index) + 1):
            mw, mh, md = ab.get_mipmap_dimensions(w, h, d, mipmap)
            if fmt == ab.FORMAT_P8_BUMP:
                bytes_count += mw*mh*md
            else:
                bytes_count += ab.bitmap_io.get_pixel_bytes_size(fmt, mw, mh, md)

        return bytes_count

    def get_padding_size(self, b_index):
        bytes_count = self.get_bitmap_size(b_index)
        cubemap_pad = 0

        if self.bitmap_type(b_index) == TYPE_CUBEMAP:
            cubemap_pad = ((CUBEMAP_PADDING - (bytes_count % CUBEMAP_PADDING))
                           % CUBEMAP_PADDING)
            bytes_count = (bytes_count + cubemap_pad) * 6

        bitmap_pad = (BITMAP_PADDING -
                      (bytes_count%BITMAP_PADDING)) % BITMAP_PADDING

        return bitmap_pad, cubemap_pad

    def sanitize_mipmap_counts(self):
        '''Some original xbox bitmaps have fudged up mipmap counts
        and cause issues. This function will scan through all a
        bitmap's bitmaps and check that they fit within their
        calculated pixel data bounds. This is done by checking if a
        bitmap's calculated size is both within the side of the total
        pixel data and less than the next bitmap's pixel data start'''

        bad_bitmap_index_list = []
        bitmap_count = self.bitmap_count()

        for i in range(bitmap_count):
            # if this is the last bitmap
            if i + 1 == bitmap_count:
                # this is how many bytes of texture data there is total
                max_size = self.pixel_data_bytes_size()
            else:
                # this is the start of the next bitmap's pixel data
                max_size = self.bitmap_data_offset(i+1)

            while True:
                mipmap_count = self.bitmap_mipmaps_count(i)
                curr_size = self.get_bitmap_size(i) + self.bitmap_data_offset(i)

                if curr_size <= max_size:
                    break

                self.bitmap_mipmaps_count(i, mipmap_count - 1)

                # the mipmap count is zero and the bitmap still will
                # not fit within the space provided. Something's wrong
                if mipmap_count == 0:
                    bad_bitmap_index_list.append(i)
                    break

        return bad_bitmap_index_list

    def sanitize_bitmaps(self):
        if ab is None:
            raise NotImplementedError(
                "Arbytmap is not loaded. Cannot sanitize bitmaps.")
        tex_infos = self.tex_infos

        for i in range(self.bitmap_count()):
            format = FORMAT_NAME_MAP[self.bitmap_format(i)]
            flags = self.bitmap_flags(i)
            old_w, old_h, _ = self.bitmap_width_height_depth(i)

            reg_point_x, reg_point_y = self.registration_point_xy(i)
            texinfo = tex_infos[i]

            # set the flags to the new value
            flags.palletized = (format == ab.FORMAT_P8_BUMP)
            flags.compressed = (format in ab.COMPRESSED_FORMATS)

            self.bitmap_width_height_depth(
                i, (texinfo["width"], texinfo["height"], texinfo["depth"]))
            self.bitmap_mipmaps_count(i, texinfo["mipmap_count"])
            self.registration_point_xy(i, (texinfo["width"]*reg_point_x//old_w,
                                           texinfo["height"]*reg_point_y//old_h))

    def parse_bitmap_blocks(self):
        '''converts the raw pixel data into arrays of pixel
        data and replaces the raw data in the tag with them'''
        if ab is None:
            raise NotImplementedError(
                "Arbytmap is not loaded. Cannot parse bitmaps.")

        pixel_data = self.data.tagdata.processed_pixel_data
        rawdata = pixel_data.data

        tex_infos = self.tex_infos = []

        # this is the block that will hold all of the bitmap blocks
        root_tex_block = self.definition.subdefs['pixel_root'].build()

        is_xbox = self.is_xbox_bitmap
        get_mip_dims = ab.get_mipmap_dimensions
        bytes_to_array = ab.bitmap_io.bitmap_bytes_to_array

        # read the pixel data blocks for each bitmap
        for i in range(self.bitmap_count()):
            # since we need this information to read the bitmap we extract it
            mw, mh, md, = self.bitmap_width_height_depth(i)
            type         = self.bitmap_type(i)
            format       = FORMAT_NAME_MAP[self.bitmap_format(i)]
            mipmap_count = self.bitmap_mipmaps_count(i) + 1
            sub_bitmap_count = ab.SUB_BITMAP_COUNTS[TYPE_NAME_MAP[type]]

            # Get the offset of the pixel data for
            # this bitmap within the raw pixel data
            off = self.bitmap_data_offset(i)

            # this texture info is used in manipulating the texture data
            tex_infos.append(dict(
                width=mw, height=mh, depth=md, format=format,
                mipmap_count=mipmap_count-1, sub_bitmap_count=sub_bitmap_count,
                swizzled=self.swizzled(), texture_type=TYPE_NAME_MAP[type]))

            if format == ab.FORMAT_P8_BUMP:
                tex_infos[-1]["palette"] = [
                    self.p8_palette.p8_palette_32bit_packed]*mipmap_count

                # set it to packed since if we need to drop channels
                # then it needs to be unpacked with channels dropped
                tex_infos[-1]["palette_packed"] = True
                tex_infos[-1]["indexing_size"] = 8

            # this is the block that will hold each mipmap,
            # texture slice, and cube face of the bitmap
            root_tex_block.append()
            tex_block = root_tex_block[-1]

            # xbox bitmaps are stored all mip level faces first, then
            # the next mip level, whereas pc is the other way. Xbox
            # bitmaps also have padding between each mipmap and bitmap.
            dim0 = sub_bitmap_count if is_xbox else mipmap_count
            dim1 = mipmap_count if is_xbox else sub_bitmap_count
            for j in range(dim0):
                if not is_xbox: w, h, d = get_mip_dims(mw, mh, md, j)

                for k in range(dim1):
                    if is_xbox: w, h, d = get_mip_dims(mw, mh, md, k)

                    if format == ab.FORMAT_P8_BUMP:
                        pixel_count = w*h
                        tex_block.append(array('B', rawdata[off: off+pixel_count]))
                        off += pixel_count
                        continue

                    off = bytes_to_array(rawdata, off, tex_block, format, w, h, d)

                # skip the xbox alignment padding to get to the next texture
                if is_xbox:
                    tex_pad, sub_tex_pad = self.get_padding_size(i)
                    off += sub_tex_pad
                    if j + 1 == dim0:
                        off += tex_pad

        pixel_data.data = root_tex_block
        # now that we've successfully built the bitmap
        # blocks from the raw data we replace the raw data
        if is_xbox:
            # it's easier to work with bitmaps in one format so
            # we'll switch the mipmaps from XBOX to PC ordering
            self.change_sub_bitmap_ordering(False)
