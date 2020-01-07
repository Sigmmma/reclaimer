#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

try:
    import arbytmap
    if not hasattr(arbytmap, "FORMAT_P8"):
        arbytmap.FORMAT_P8 = "P8"

        """ADD THE P8 FORMAT TO THE BITMAP CONVERTER"""
        arbytmap.register_format(format_id=arbytmap.FORMAT_P8,
                                 depths=(8,8,8,8))

    if not hasattr(arbytmap, "FORMAT_P8_BUMP"):
        arbytmap.FORMAT_P8_BUMP = "P8-BUMP"

        """ADD THE P8 FORMAT TO THE BITMAP CONVERTER"""
        arbytmap.register_format(format_id=arbytmap.FORMAT_P8_BUMP,
                                 depths=(8,8,8,8))

    from arbytmap import Arbytmap, bitmap_io, TYPE_2D, TYPE_3D, TYPE_CUBEMAP,\
         FORMAT_A8, FORMAT_L8, FORMAT_AL8, FORMAT_A8L8,\
         FORMAT_R5G6B5, FORMAT_A1R5G5B5, FORMAT_A4R4G4B4,\
         FORMAT_X8R8G8B8, FORMAT_A8R8G8B8,\
         FORMAT_DXT1, FORMAT_DXT3, FORMAT_DXT5, FORMAT_CTX1, FORMAT_DXN,\
         FORMAT_DXT3Y, FORMAT_DXT3A, FORMAT_DXT3AY,\
         FORMAT_DXT5Y, FORMAT_DXT5A, FORMAT_DXT5AY,\
         FORMAT_P8_BUMP, FORMAT_P8, FORMAT_V8U8, FORMAT_R8G8,\
         FORMAT_R16G16B16F, FORMAT_A16R16G16B16F,\
         FORMAT_R32G32B32F, FORMAT_A32R32G32B32F
except ImportError:
    arbytmap = Arbytmap = None

import zlib

from array import array
from pathlib import Path
from struct import unpack

from reclaimer.util import get_is_xbox_map
from reclaimer.h3.util import get_virtual_dimension,\
     get_pixel_bytes_size, get_h3_pixel_bytes_size
from reclaimer.bitmaps.p8_palette import HALO_P8_PALETTE, STUBBS_P8_PALETTE

__all__ = ("extract_bitmap_tiff_data", "extract_bitmaps", )


#each sub-bitmap(cubemap face) must be a multiple of 128 bytes
CUBEMAP_PADDING = 128


def extract_bitmap_tiff_data(tag_path):
    tag_path = Path(tag_path)
    try:
        with tag_path.open('rb') as f:
            tag_header_data = f.read(256)  # 256 is enough to read all the
            #                                pertinent header information

        tag_id = tag_header_data[36: 40]
        engine_id = tag_header_data[60: 64]

        # make sure this is a bitmap tag
        if tag_id == b'bitm' and engine_id == b'blam':
            # halo 1
            dims_off = 64+24
            size_off = 64+28
            data_off = 64+108
            endian = ">"
        elif tag_id == b'mtib' and engine_id == b'!MLB':
            # halo 2
            dims_off = 64+16+24
            size_off = 64+16+28
            data_off = 64+16
            # get the size of the bitmap body from the tbfd structure
            data_off += unpack("<i", tag_header_data[data_off-4: data_off])[0]
            endian = "<"
        else:
            print('    This file doesnt appear to be a bitmap tag.')
            return 0, 0, bytearray()

        width, height = unpack(endian + "HH", tag_header_data[dims_off: dims_off+4])
        comp_size = unpack(endian + "i", tag_header_data[size_off: size_off+4])[0]
    except Exception:
        print('    Could not load bitmap tag.')
        return 0, 0, bytearray()


    with tag_path.open('rb') as f:
        f.seek(data_off)
        comp_data = f.read(comp_size)

    if not comp_data:
        print('    No source image to extract.')
        return width, height, bytearray()

    try:
        data_size = unpack(endian + "I", comp_data[:4])[0]
        if not data_size:
            print('    Source data is blank.')
            return width, height, bytearray()

        return width, height, bytearray(zlib.decompress(comp_data[4:]))
    except Exception:
        print('    Could not decompress data.')
        return width, height, bytearray()


def extract_bitmaps(tagdata, tag_path, **kw):
    out_dir = Path(kw.get("out_dir", ""))
    filepath_base = out_dir.joinpath(tag_path).parent
    filename_base = Path(tag_path).name

    ext = kw.get("bitmap_ext", "").strip(". ")
    keep_alpha = kw.get("bitmap_keep_alpha", True)
    engine = kw.pop('engine', '')
    pix_data = tagdata.processed_pixel_data.STEPTREE
    if 'halo_map' in kw:
        engine = kw['halo_map'].engine

    p8_palette = STUBBS_P8_PALETTE if "stubbs" in engine else HALO_P8_PALETTE
    if not ext:
        ext = "dds"

    is_xbox = get_is_xbox_map(engine)
    is_gen3 = hasattr(tagdata, "zone_assets_normal")
    if Arbytmap is None:
        # cant extract xbox bitmaps yet
        return "    Arbytmap not loaded. Cannot extract bitmaps."

    arby = Arbytmap()
    bitm_i = 0
    multi_bitmap = len(tagdata.bitmaps.STEPTREE) > 1
    size_calc = get_h3_pixel_bytes_size if is_gen3 else get_pixel_bytes_size
    dim_calc = get_virtual_dimension if is_gen3 else None

    for bitmap in tagdata.bitmaps.STEPTREE:
        typ = bitmap.type.enum_name
        fmt = bitmap.format.enum_name
        w = bitmap.width
        h = bitmap.height
        d = bitmap.depth
        tiled = False
        if hasattr(bitmap, "format_flags"):
            tiled = bitmap.format_flags.tiled

        filename = filename_base
        if multi_bitmap:
            filename += "__%s" % bitm_i
            bitm_i += 1

        tex_block = []
        tex_info = dict(
            width=w, height=h, depth=d, mipmap_count=bitmap.mipmaps,
            swizzled=bitmap.flags.swizzled, big_endian=is_gen3,
            packed=True, tiled=tiled, tile_method="DXGI",
            packed_width_calc=dim_calc, packed_height_calc=dim_calc,
            filepath=str(filepath_base.joinpath(filename + "." + ext))
            )
        tex_info["texture_type"] = {
            "texture_2d": TYPE_2D, "texture_3d": TYPE_3D,
            "cubemap": TYPE_CUBEMAP}.get(typ, TYPE_2D)
        tex_info["sub_bitmap_count"] = {
            "texture_2d": 1, "texture_3d": 1,
            "cubemap": 6, "multipage_2d": d}.get(typ, 1)
        if typ == "multipage_2d":
            tex_info.update(depth=1)
            d = 1


        if fmt == "p8_bump":
            tex_info.update(
                palette=[p8_palette.p8_palette_32bit_packed]*(bitmap.mipmaps + 1),
                palette_packed=True, indexing_size=8, format=FORMAT_P8_BUMP)
        else:
            tex_info["format"] = {
                "a8": FORMAT_A8, "y8": FORMAT_L8, "ay8": FORMAT_AL8,
                "a8y8": FORMAT_A8L8, "p8": FORMAT_A8,
                "v8u8": FORMAT_V8U8, "g8b8": FORMAT_R8G8,
                "x8r8g8b8": FORMAT_A8R8G8B8, "a8r8g8b8": FORMAT_A8R8G8B8,
                "r5g6b5": FORMAT_R5G6B5, "a1r5g5b5": FORMAT_A1R5G5B5,
                "a4r4g4b4": FORMAT_A4R4G4B4,
                "dxt1": FORMAT_DXT1, "dxt3": FORMAT_DXT3, "dxt5": FORMAT_DXT5,
                "ctx1": FORMAT_CTX1, "dxn": FORMAT_DXN, "dxt5ay": FORMAT_DXT5AY,
                "dxt3a": FORMAT_DXT3A, "dxt3y": FORMAT_DXT3Y,
                "dxt5a": FORMAT_DXT5A, "dxt5y": FORMAT_DXT5Y,
                "rgbfp16": FORMAT_R16G16B16F, "argbfp32": FORMAT_A32R32G32B32F,
                "rgbfp32": FORMAT_R32G32B32F}.get(fmt, None)


        arby_fmt = tex_info["format"]
        if arby_fmt is None:
            continue

        i_max = tex_info["sub_bitmap_count"] if is_xbox else bitmap.mipmaps + 1
        j_max = bitmap.mipmaps + 1 if is_xbox else tex_info['sub_bitmap_count']
        off = bitmap.pixels_offset
        for i in range(i_max):
            if not is_xbox:
                mip_size = size_calc(arby_fmt, w, h, d, i, tiled)

            for j in range(j_max):
                if is_xbox:
                    mip_size = size_calc(arby_fmt, w, h, d, j, tiled)

                if fmt == "p8_bump":
                    tex_block.append(
                        array('B', pix_data[off: off + (mip_size // 4)]))
                    off += len(tex_block[-1])
                else:
                    off = bitmap_io.bitmap_bytes_to_array(
                        pix_data, off, tex_block,
                        arby_fmt, 1, 1, 1, mip_size)

            # skip the xbox alignment padding to get to the next texture
            if is_xbox and typ == "cubemap":
                off += ((CUBEMAP_PADDING - (off % CUBEMAP_PADDING)) %
                        CUBEMAP_PADDING)


        if is_xbox and typ == "cubemap":
            template = tuple(tex_block)
            i = 0
            for f in (0, 2, 1, 3, 4, 5):
                for m in range(bitmap.mipmaps + 1):
                    tex_block[m*6 + f] = template[i]
                    i += 1

        if not tex_block:
            # nothing to extract
            continue

        arby.load_new_texture(texture_block=tex_block, texture_info=tex_info,
                              tile_mode=False, swizzle_mode=False)
        arby.save_to_file(keep_alpha=keep_alpha)
