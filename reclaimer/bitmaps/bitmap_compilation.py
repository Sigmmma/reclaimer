#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from pathlib import Path
from traceback import format_exc

from arbytmap.bitmap_io import get_channel_order_by_masks,\
     get_channel_swap_mapping, swap_array_items
from arbytmap.format_defs import clip_dimensions
from arbytmap.dds_defs import clip_dxt_dimensions
from supyr_struct.defs.bitmaps.dds import dds_def
from reclaimer.util import get_block_max

__all__ = ("compile_bitmap_from_dds_files", "add_bitmap_to_bitmap_tag",
           "parse_dds_file", )


def compile_bitmap_from_dds_files(bitm_tag, dds_filepaths=()):
    for fp in dds_filepaths:
        fp = Path(fp)
        try:
            print("    %s" % fp)
            w, h, d, typ, fmt, mips, pixels = parse_dds_file(fp)
        except Exception:
            print(format_exc())
            print("    Could not load dds image")
            continue

        try:
            seq_name = fp.stem
            if "#" in seq_name:
                seq_name, _ = seq_name.split("#", 1)

            add_bitmap_to_bitmap_tag(bitm_tag, w, h, d, typ, fmt,
                                     mips, pixels, seq_name)
        except Exception:
            print(format_exc())
            print("Could not add bitmap data to bitmap tag.")


def add_bitmap_to_bitmap_tag(bitm_tag, width, height, depth, typ, fmt,
                             mip_count, new_pixels, seq_name=""):
    bitm_data = bitm_tag.data.tagdata
    sequences = bitm_data.sequences.STEPTREE
    bitmaps   = bitm_data.bitmaps.STEPTREE
    seq_name  = seq_name[: 31]

    max_bitmaps     = get_block_max(bitm_data.bitmaps)
    max_sequences   = get_block_max(bitm_data.sequences)
    max_pixel_bytes = get_block_max(bitm_data.processed_pixel_data)

    if len(bitmaps) >= max_bitmaps:
        raise ValueError("Cannot add more bitmaps(max of %s per tag)." % max_bitmaps)

    bitmaps.append()
    if not sequences or sequences[-1].sequence_name != seq_name:
        if len(sequences) >= max_sequences:
            print("Cannot add more sequences(max of %s per tag)." % max_sequences)
        else:
            sequences.append()
            sequences[-1].sequence_name = seq_name
            sequences[-1].first_bitmap_index = len(bitmaps) - 1

    seq_block = sequences[-1]
    bitm_block = bitmaps[-1]
    if seq_block.sequence_name == seq_name:
        seq_block.bitmap_count += 1

    if fmt not in bitm_block.format.NAME_MAP:
        raise ValueError("%s does not support the bitmap format '%s'" %
                         (type(bitm_tag), fmt))

    if len(bitmaps) == 1:
        if typ == "texture_2d":
            bitm_data.type.set_to("textures_2d")
        elif typ == "texture_3d":
            bitm_data.type.set_to("textures_3d")
        elif typ == "cubemap":
            bitm_data.type.set_to("cubemaps")

        if fmt == "dxt1":
            bitm_data.format.set_to("color_key_transparency")
        elif fmt == "dxt3":
            bitm_data.format.set_to("explicit_alpha")
        elif fmt == "dxt5":
            bitm_data.format.set_to("interpolated_alpha")
        elif fmt in ("r5g6b5", "a1r5g5b5", "a4r4g4b4"):
            bitm_data.format.set_to("color_16bit")
        elif fmt in ("x8r8g8b8", "a8r8g8b8", "p8_bump"):
            bitm_data.format.set_to("color_32bit")
        elif fmt in ("a8", "y8", "ay8", "a8y8"):
            bitm_data.format.set_to("monochrome")
        elif fmt == "bc7":
            bitm_data.format.set_to("high_quality_compression")

    bitm_block.bitm_id.set_to("bitm")
    if fmt in ("dxt1", "dxt3", "dxt5", "bc7"):
        bitm_block.flags.compressed = True
    bitm_block.flags.power_of_2_dim = True

    bitm_block.width = width
    bitm_block.height = height
    bitm_block.depth = depth
    bitm_block.type.set_to(typ)
    bitm_block.format.set_to(fmt)
    bitm_block.mipmaps = mip_count
    bitm_block.registration_point_x = width // 2
    bitm_block.registration_point_y = height // 2

    bitm_block.pixels_offset = len(bitm_data.processed_pixel_data.data)

    if len(bitm_data.processed_pixel_data.data) + len(new_pixels) >= max_pixel_bytes:
        raise ValueError("Cannot add more pixel data(max of %s bytes per tag)." % max_pixel_bytes)

    # place the pixels from the dds tag into the bitmap tag
    bitm_data.processed_pixel_data.data += new_pixels


def parse_dds_file(filepath):
    dds_tag = dds_def.build(filepath=Path(filepath))
    dds_head = dds_tag.data.header
    caps  = dds_head.caps
    caps2 = dds_head.caps2
    pf = dds_head.dds_pixelformat
    dds_pixels = dds_tag.data.pixel_data
    if caps2.cubemap and not(caps2.pos_x and caps2.neg_x and
                             caps2.pos_y and caps2.neg_y and
                             caps2.pos_z and caps2.neg_z):
        raise ValueError(
            "    DDS image is malformed and does not " +
            "    contain all six necessary cubemap faces.")

    elif not dds_head.flags.pixelformat:
        raise TypeError(
            "    DDS image is malformed and does not " +
            "    contain a pixelformat structure.")

    # get the dimensions
    width  = dds_head.width
    height = dds_head.height
    depth  = dds_head.depth
    mip_count = max(dds_head.mipmap_count - 1, 0)
    if not caps2.volume:
        depth = 1

    # set up the flags
    fcc = pf.four_cc.enum_name if pf.flags.four_cc else None
    bpp = 8  # bits per pixel
    bitm_format = ""
    channel_map = None

    # choose bitmap format
    if fcc == "DXT1":
        bitm_format = "dxt1"
        bpp = 4
    elif fcc in ("DXT2", "DXT3"):
        bitm_format = "dxt3"
    elif fcc in ("DXT4", "DXT5"):
        bitm_format = "dxt5"
    elif fcc == "DX10":
        dx10_head = dds_tag.data.dxt10_header
        dx10_fmt  = dx10_head.format.enum_name[:3]
        # NOTE: we don't really care about if the alpha is premultiplied
        #       or not since we don't intend to do anything about it
        if dx10_fmt == "BC1":
            bitm_format = "dxt1"
            bpp = 4
        elif dx10_fmt in ("BC2", "BC3"):
            bitm_format = "dxt3"
        elif dx10_fmt in ("BC4", "BC5"):
            bitm_format = "dxt5"
        elif dx10_fmt in "BC7":
            bitm_format = "bc7"

    elif pf.flags.rgb_space:
        bitcount = pf.rgb_bitcount
        bpp = 32

        if bitcount == 32:
            channel_order = get_channel_order_by_masks(
                pf.a_bitmask, pf.r_bitmask,
                pf.g_bitmask, pf.b_bitmask)

            channel_map = get_channel_swap_mapping("BGRA", channel_order)
            if pf.flags.has_alpha:
                bitm_format = "a8r8g8b8"
            elif bitcount == 32:
                bitm_format = "x8r8g8b8"

        elif bitcount in (15, 16):
            bpp = 16
            a_mask = pf.a_bitmask
            r_mask = pf.r_bitmask
            g_mask = pf.g_bitmask
            b_mask = pf.b_bitmask
            # shift the masks right until they're all the same scale
            while a_mask and not(a_mask&1): a_mask = a_mask >> 1
            while r_mask and not(r_mask&1): r_mask = r_mask >> 1
            while g_mask and not(g_mask&1): g_mask = g_mask >> 1
            while b_mask and not(b_mask&1): b_mask = b_mask >> 1

            mask_set = set((a_mask, r_mask, g_mask, b_mask))
            if mask_set == set((31, 63, 0)):
                bitm_format = "r5g6b5"
            elif mask_set == set((1, 31)):
                bitm_format = "a1r5g5b5"
            elif mask_set == set((15, )):
                bitm_format = "a4r4g4b4"

    elif pf.flags.alpha_only:
        bitm_format = "a8"

    elif pf.flags.luminance:
        if pf.flags.has_alpha:
            bitm_format = "a8y8"
        else:
            bitm_format = "y8"

    if not bitm_format:
        raise TypeError("Unknown dds image format.")

    # make sure the number of mipmaps is accurate
    face_count = 6 if caps2.cubemap else 1
    w, h, d = width, height, depth
    pixel_counts = []

    # make a list of all the pixel counts of all the mipmaps.
    for mip in range(mip_count + 1):
        mw, mh, md = clip_dimensions(w>>mip, h>>mip, d>>mip)
        if bitm_format in ("dxt1", "dxt3", "dxt5", "bc7"):
            mw, mh = clip_dxt_dimensions(mw, mh)

        pixel_counts.append(mw*mh*md)

    # see how many mipmaps can fit in the number of pixels in the dds file.
    while True:
        if (sum(pixel_counts)*bpp*face_count)//8 <= len(dds_pixels):
            break

        pixel_counts.pop(-1)

        #the mipmap count is zero and the bitmap still will
        #not fit within the space provided. Something's wrong
        if len(pixel_counts) == 0:
            raise ValueError(
                "Size of the pixel data is too small to read even " +
                "the fullsize image from. This dds file is malformed.")

    if len(pixel_counts) != mip_count+1:
        raise ValueError(
            "Mipmap count is too high for the number of pixels stored " +
            "in the dds file. The mipmap count has been reduced from " +
            "%s to %s." % (mip_count, len(pixel_counts)))

    # the mip_count in the tag always excludes the toplevel image
    mip_count = len(pixel_counts) - 1

    # choose the texture type
    if caps2.volume:
        bitm_type = "texture_3d"
        pixels = dds_pixels

    elif caps2.cubemap:
        # gotta rearrange the mipmaps and cubemap faces
        images = [None]*6*len(pixel_counts)
        pos = 0

        # dds images store all mips for one face next to each
        # other, and then the next set of mips for the next face.
        for face in range(6):
            for mip, pixel_count in enumerate(pixel_counts):
                i = mip*6 + face

                image_size = (bpp*pixel_count)//8
                images[i]  = dds_pixels[pos: pos + image_size]
                pos += image_size

        bitm_type = "cubemap"
        pixels = b''
        for image in images:
            pixels += image

    else:
        bitm_type = "texture_2d"
        pixels = dds_pixels

    if channel_map:
        # swap 32bit channels around to the format expected of bitmap tags
        pixels = bytearray(pixels)
        swap_array_items(pixels, channel_map)

    return width, height, depth, bitm_type, bitm_format, mip_count, pixels
