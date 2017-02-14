import os
import time
import mmap

from struct import pack_into, unpack_from, unpack
from array import array
from traceback import format_exc

try:
    try:
        from .ext import bitmap_io_ext
    except Exception:
        from ext import bitmap_io_ext
    fast_bitmap_io = True
except Exception:
    fast_bitmap_io = False


#this will be the reference to the bitmap convertor module.
#once the module loads this will become the reference to it.
ab = None

DXT_FORMAT_STRINGS = {
    "DXT1":"DXT1",
    "DXT2":"DXT2", "DXT3":"DXT3",
    "DXT4":"DXT4", "DXT5":"DXT5",
    "DXN":"ATI2", 
    "DXT5A":"DX5A", "DXT5I":"DX5I",  # these 2 are my own typecodes. remove
    "CTX1":"CTX1",  "DXT5AY":"D5AY"  # them when the dx10 header can be read
    }
DXT_FORMAT_STRINGS_I = {
    "DXT1":"DXT1",
    "DXT2":"DXT2", "DXT3":"DXT3",
    "DXT4":"DXT4", "DXT5":"DXT5",
    "ATI2":"DXN",
    "DX5A":"DXT5A", "DX5I":"DXT5I",  # these 2 are my own typecodes. remove
    "CTX1":"CTX1",  "D5AY":"DXT5AY"  # them when the dx10 header can be read
    }

DXT_TEXTURE_TYPE_MAP = {
    "2D":0, "FLAT":0,
    "3D":1, "VOLUME":1, "VOL":1, "DEPTH":0,
    "CUBE":2, "CUBEMAP":2, "CUBE MAP":2, "CUBE_MAP":2}

DXT_VAR_OFFSETS = {
    0:0, 1:4, 2:8, 3:12, 4:16, 5:20, 6:24, 7:28,
    8:76, 9:80, 10:84, 11:88, 12:92, 13:96, 14:100, 15:104,
    16:108, 17:112, 18:116, 19:120, 20:124}

DXT_VAR_DEFAULTS = {
    0:"DDS ".encode('UTF-8'), 1:124, 2:4103, 3:0, 4:0, 5:0,
    6:0, 7:0, 8:32, 9:0, 10:b'\x00\x00\x00\x00', 11:0,
    12:0, 13:0, 14:0, 15:0, 16:4096, 17:0, 18:0, 19:0, 20:0}

DXT_FORMAT_ID_BLANK = b'\x00\x00\x00\x00'.decode('Latin-1')

DXT_HEADER_VAR_NAMES = {
    0:"dds_format_name", 1:"header_size", 2:"flags",
    3:"height", 4:"width", 5:"pitch_or_linear_size",
    6:"depth", 7:"mipmap_count", 8:"pixel_struct_size",
    9:"pixel_format_flags", 10:"dxt_format_id", 11:"bpp",
    12:"r_mask", 13:"g_mask", 14:"b_mask", 15:"a_mask",
    16:"caps_1", 17:"caps_2",
    18:"reserved_0", 19:"reserved_1", 20:"reserved_2"}

TGA_IMAGE_TYPES = {
    0:"BLANK",
    1:"COLOR_MAPPED", 9:"RLE_COLOR_MAPPED",
    2:"TRUE_COLOR",  10:"RLE_TRUE_COLOR",
    3:"MONOCHROME",  11:"RLE_MONOCHROME"}

        
def save_to_tga_file(convertor, output_path, ext, **kwargs):
    """Saves the currently loaded texture to a TGA file"""
    conv = convertor
    f = conv.format
    
    if (f in (ab.FORMAT_R5G6B5, ab.FORMAT_A4R4G4B4,
              ab.FORMAT_A8Y8, ab.FORMAT_U8V8) or f in ab.COMPRESSED_FORMATS):
        print("CANNOT EXTRACT THIS FORMAT TO TGA. EXTRACTING TO DDS INSTEAD.")
        save_to_dds_file(conv, output_path, "dds", **kwargs)
        return
    
    if ab.BITS_PER_PIXEL[f] > 32:
        print("ERROR: CANNOT SAVE BITMAP OF HIGHER THAN 32 BIT "+
              "COLOR DEPTH TO DDS.\nCANCELLING TGA SAVE.")
        return

    channel_count = ab.FORMAT_CHANNEL_COUNTS[f]
    
    tex_desc = dict(
        width=conv.width, height=conv.height*conv.depth,
        image_type=2, palettized=False, bpp=ab.BITS_PER_PIXEL[f],
        image_desc=ab.FORMAT_CHANNEL_DEPTHS[f][0])

    if channel_count in (1,2):
        tex_desc["image_type"] = 3
    
    if conv.is_palettized():
        tex_desc["palettized"] = True
        tex_desc["color_map_type"] = 1
        tex_desc["image_type"] = 1
        tex_desc["color_map_origin"] = 0
        tex_desc["color_map_length"] = 2**conv.indexing_size
        tex_desc["color_map_depth"] = ab.BITS_PER_PIXEL[f]
        tex_desc["image_desc"] = 0
        tex_desc["bpp"] = 8
            
        if conv.target_indexing_size > 8:
            tex_desc["bpp"] = conv.indexing_size

    final_output_path = output_path
    width = conv.width
    height = conv.height
    pals = conv.palette
    tex_block = conv.texture_block
    mip_count = convertor.mipmap_count+1

    for sb in range(conv.sub_bitmap_count):                
        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path))
            
        if conv.sub_bitmap_count > 1:
            final_output_path = "%s_tex%s" % (output_path, sb)
        
        with open("%s.%s" % (final_output_path, ext), 'w+b') as tga_file:
            #write the header and get the offset
            #to start writing the pixel data
            pix_off = write_tga_header(tga_file, **tex_desc)
            tga_file.seek(pix_off)
            
            if tex_desc["palettized"]:
                pal = packed_pal = pals[sb]
                idx = packed_idx = tex_block[sb]
                
                if not conv.palette_packed:
                    packed_pal = conv.palette_packer(pal)
                    
                temp = conv.target_indexing_size
                '''need to pack the indexing and make sure it's 8-bit
                   since TGA doesn't support less than 8 bit indexing'''
                if conv.indexing_size < 8:
                    conv.target_indexing_size = 8
                    if conv.packed:
                        packed_idx = conv.indexing_packer(
                            conv.indexing_unpacker(packed_idx))
    
                if not conv.packed:
                    packed_idx = conv.indexing_packer(idx)
                    
                conv.target_indexing_size = temp
                        
                tga_file.write(packed_pal)
                tga_file.write(packed_idx)
                continue
            elif conv.packed:
                pixel_array = tex_block[sb]
            else:
                pixel_array = conv.pack(tex_block[sb], width, height, 0)
                width, height, _ = ab.clip_dimensions(width//2, height//2)
                if pixel_array is None:
                    print("ERROR: UNABLE TO PACK IMAGE DATA.\n"+
                          "CANCELLING TGA SAVE.")
                    return

            if ab.BITS_PER_PIXEL[f] == 24:
                pixel_array = unpad_24bit_array(pixel_array)
                
            tga_file.write(pixel_array)


def save_to_dds_file(convertor, output_path, ext, **kwargs):
    """Saves the currently loaded texture to a DDS file"""
    f = convertor.format

    if ab.BITS_PER_PIXEL[f] > 32:
        print("ERROR: CANNOT SAVE BITMAP OF HIGHER THAN 32 BIT "+
              "COLOR DEPTH TO DDS.\nCANCELLING DDS SAVE.")
        return
        
    channel_count = 3
    if f not in ab.THREE_CHANNEL_FORMATS:
        channel_count = ab.FORMAT_CHANNEL_COUNTS[f]

    w, h, d = convertor.width, convertor.height, convertor.depth
    bpp = ab.BITS_PER_PIXEL[f]
    masks = ab.FORMAT_CHANNEL_MASKS
    palettized = convertor.is_palettized()
    pal_packed = convertor.palette_packed
    packed = convertor.packed

    palette_unpacker = convertor.palette_unpacker
    indexing_unpacker = convertor.indexing_unpacker
    depalettize = convertor.depalettize_bitmap

    tex_desc = dict(
        width=w, height=h, depth=d, channel_count=channel_count,
        mipmap_count=convertor.mipmap_count, bpp=bpp,
        palettized=False, compressed=False, format=f,
        texture_type=convertor.texture_type)

    if f in DXT_FORMAT_STRINGS:
        tex_desc["compressed"] = True
        tex_desc["dxt_format_id"] = DXT_FORMAT_STRINGS[f]
        del tex_desc['bpp']
    elif channel_count == 1:
        if tex_desc["format"] == ab.FORMAT_A8:
            tex_desc["a_mask"] = masks[f][0]
        else:
            tex_desc["r_mask"] = masks[f][0]
    elif channel_count == 2:
        tex_desc["a_mask"] = masks[f][0]
        tex_desc["r_mask"] = masks[f][1]
    else:
        tex_desc["a_mask"] = masks[f][0]
        tex_desc["r_mask"] = masks[f][1]
        tex_desc["g_mask"] = masks[f][2]
        tex_desc["b_mask"] = masks[f][3]
    
    final_output_path = output_path

    dirpath = os.path.dirname(output_path)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    with open("%s.%s" % (final_output_path, ext), 'w+b') as dds_file:
        #write the header and get the offset
        #to start writing the pixel data
        off = write_dds_header(dds_file, **tex_desc)
        dds_file.seek(off)
        
        #write each of the pixel arrays into the bitmap
        for sb in range(convertor.sub_bitmap_count):
            #write each of the pixel arrays into the bitmap
            for m in range(convertor.mipmap_count+1):
                # get the index of the bitmap we'll be working with
                i = m*convertor.sub_bitmap_count + sb
                pixels = convertor.texture_block[i]
                
                if palettized:
                    pal = unpacked_pal = convertor.palette[i]
                    idx = unpacked_idx = pixels

                    if pal_packed:
                        unpacked_pal = palette_unpacker(pal)
                    if packed:
                        unpacked_idx = indexing_unpacker(idx)
                        
                    unpacked_pixels = depalettize(unpacked_pal,
                                                  unpacked_idx)
                    pixels = convertor.pack_raw(unpacked_pixels)
                elif not convertor.packed:
                    pixels = convertor.pack(pixels, w, h, d)
                    if pixels is None:
                        print("ERROR: UNABLE TO PACK IMAGE DATA.\n"+
                              "CANCELLING DDS SAVE.")
                        return
                    
                if bpp == 24:
                    pixels = unpad_24bit_array(pixels)
                dds_file.write(pixels)

            w, h, d = ab.clip_dimensions(w//2, h//2, d//2)


def save_to_rawdata_file(convertor, output_path, ext, **kwargs):
    """Saves the currently loaded texture to a raw file.
    The file has no header and in most cases wont be able
    to be directly opened be applications."""

    f = convertor.format

    final_output_path = output_path

    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
        
    for sb in range(convertor.sub_bitmap_count):
        if convertor.sub_bitmap_count > 1:
            final_output_path = output_path+"_tex"+str(sb)
                
        #write each of the pixel arrays into the bitmap
        for m in range(convertor.mipmap_count+1):
            i = m*convertor.sub_bitmap_count + sb
            
            if convertor.mipmap_count:
                final_output_path = output_path+"_mip"+str(m)
        
            with open(final_output_path+".raw", 'w+b') as raw_file:
                if convertor.is_palettized():
                    palette = packed_palette = convertor.palette[i]
                    packed_indexing = convertor.texture_block[i]
                    indexing = packed_indexing
                    
                    if not convertor.palette_packed:
                        packed_palette = convertor.palette_packer(palette)
                    if not convertor.packed:
                        packed_indexing = convertor.indexing_packer(indexing)
                        
                    if ab.BITS_PER_PIXEL[f] == 24:
                        packed_palette = unpad_24bit_array(packed_palette)
                    elif ab.BITS_PER_PIXEL[f] == 48:
                        packed_palette = unpad_48bit_array(packed_palette)
                        
                    raw_file.write(packed_palette)
                    raw_file.write(packed_indexing)
                else:
                    if convertor.packed:
                        pixel_array = convertor.texture_block[i]
                    else:
                        pixel_array = convertor.pack(convertor.texture_block[i],
                                                     width, height, depth)
                        width, height, depth = ab.clip_dimensions(
                            width//2, height//2, depth//2)
                        if pixel_array is None:
                            print("ERROR: UNABLE TO PACK IMAGE DATA.\n"+
                                  "CANCELLING DDS SAVE.")
                            return()
                    
                    if ab.BITS_PER_PIXEL[f] == 24:
                        pixel_array = unpad_24bit_array(pixel_array)
                    elif ab.BITS_PER_PIXEL[f] == 48:
                        pixel_array = unpad_48bit_array(pixel_array)
                    raw_file.write(pixel_array)

                
def load_from_tga_file(convertor, input_path, ext, **kwargs):
    """Loads a TGA file into the convertor. Currently doesn't
    support correcting the upside down nature of Truevision
    images. If an image is Truevision, it will be upside down."""
    final_input_path = "%s.%s" % (input_path, ext)
    unable_to_load = False
    
    try:
        with open(final_input_path, 'r+b') as tga_file:
            
            tga_data = mmap.mmap(tga_file.fileno(), 0, access=mmap.ACCESS_READ)
            
            #General image info
            id_length    = unpack_from("B", tga_data, 0)[0]
            color_mapped = unpack_from("B", tga_data, 1)[0]
            image_type   = TGA_IMAGE_TYPES[unpack_from("B", tga_data, 2)[0]]
            compressed = image_type[:3] == "RLE"

            #Color map info
            color_map_origin = unpack_from("<H", tga_data, 3)[0]
            color_map_length = unpack_from("<H", tga_data, 5)[0]
            color_map_depth  = unpack_from("B", tga_data,  7)[0]

            #Image origin coordinate
            image_origin_x = unpack_from("<H", tga_data,  8)[0]
            image_origin_y = unpack_from("<H", tga_data, 10)[0]

            #Dimensions and color depth
            width  = unpack_from("<H", tga_data, 12)[0]
            height = unpack_from("<H", tga_data, 14)[0]
            bpp    = unpack_from("B", tga_data,  16)[0]
            
            image_desc = unpack_from("B", tga_data, 17)[0]

            #Image descriptor properties
            alpha_depth = image_desc & 15
            image_v_flip = not bool(image_desc & 32)
            
            interleave_order = (image_desc & 192) >> 6

            #do another check to make sure image is color mapped
            color_mapped = bool(color_mapped&int("COLOR_MAPPED" in image_type))

            texture_info = {"width":width, "height":height, "depth":1,
                            "texture_type":"2D", "mipmap_count":0,
                            "sub_bitmap_count":1, "filepath":input_path}

            #figure out what color format we've got
            if color_mapped:
                if color_map_depth == 8:
                    texture_info["format"] = ab.FORMAT_Y8
                elif color_map_depth == 15:
                    texture_info["format"] = ab.FORMAT_R5G6B5
                elif color_map_depth == 16:
                    texture_info["format"] = ab.FORMAT_A1R5G5B5
                elif color_map_depth == 24:
                    texture_info["format"] = ab.FORMAT_R8G8B8
                elif color_map_depth == 32:
                    texture_info["format"] = ab.FORMAT_A8R8G8B8
                else:
                    print("Unable to load Targa images with",
                          color_map_depth,"bit color palette.")
                    unable_to_load = True
            elif bpp == 1:
                texture_info["format"] = ab.FORMAT_STENCIL
                #NOT YET SUPPORTED
                
                print("Not yet able to load black and "+
                      "white 1-bit color Targa images.")
                unable_to_load = True
            elif bpp == 8:
                if alpha_depth == 8:
                    texture_info["format"] = ab.FORMAT_A8
                else:
                    texture_info["format"] = ab.FORMAT_Y8
            elif bpp == 15:
                texture_info["format"] = ab.FORMAT_R5G6B5
            elif bpp == 16:
                if alpha_depth == 0:
                    texture_info["format"] = ab.FORMAT_R5G6B5
                elif alpha_depth == 1:
                    texture_info["format"] = ab.FORMAT_A1R5G5B5
                elif alpha_depth == 4:
                    texture_info["format"] = ab.FORMAT_A4R4G4B4
                else:
                    texture_info["format"] = ab.FORMAT_A8Y8
            elif bpp == 24:
                texture_info["format"] = ab.FORMAT_R8G8B8
            elif bpp == 32:
                if alpha_depth == 0:
                    texture_info["format"] = ab.FORMAT_X8R8G8B8
                else:
                    texture_info["format"] = ab.FORMAT_A8R8G8B8
            else:
                print("Unable to load", bpp, "bit color Targa images.")
                unable_to_load = True

            #fix the bit depths so calculations work properly
            if color_map_depth == 15: color_map_depth = 16
            if bpp == 15: bpp = 16

            palette_start = 18 + id_length
            image_start = 18 + id_length + ((color_map_depth//8)*
                                            color_map_length)

            if interleave_order:
                print("Not yet able to load Targa images "+
                      "with interleaved pixels.")
                unable_to_load = True
            if image_type == "BLANK":
                print("Targa image is specified as blank in "+
                      "the header. Nothing to load.")
                unable_to_load = True
                
            if unable_to_load:
                return
            

            if color_mapped:
                if ab.BITS_PER_PIXEL[texture_info["format"]] == 24:
                    palette = pad_24bit_array(tga_data[palette_start:
                                                       image_start])
                else:
                    palette = array(
                        ab.FORMAT_PACKED_TYPECODES[texture_info["format"]],
                        tga_data[palette_start:image_start])
                
                #if the color map doesn't start at zero
                #then we need to shift around the palette
                if color_map_origin:
                    shifted_palette = palette[color_map_origin:len(palette)]
                    shifted_palette.extend(palette[:color_map_origin])
                    palette = shifted_palette
                    
                    color_map_origin = 0

                indexing = array(
                    "B", tga_data[image_start: image_start+width*height])
                
                texture_info["palette"] = [palette]
                texture_info["palettize"] = True
                texture_info["indexing_size"] = bpp
                texture_block = [indexing]
                
                #load all the bitmap data into the convertor
                convertor.load_new_texture(texture_block=texture_block,
                                           texture_info=texture_info)
            else:
                texture_block = []
                comp = None
                if compressed:
                    comp = "rle"
                bitmap_bytes_to_array(tga_data[image_start:], 0, texture_block,
                                      texture_info["format"], width,
                                      height, compression=comp)
                
                convertor.load_new_texture(texture_block=texture_block,
                                           texture_info=texture_info)

            if image_v_flip:
                stride = width
                pixels = texture_block[0]

                if isinstance(pixels, bytearray):
                    stride *= ab.BITS_PER_PIXEL[texture_info["format"]]//8
                    if convertor._UNPACK_ARRAY_CODE == "H":
                        stride *= 2
                    flipped_pixels = bytearray()
                else:
                    flipped_pixels = array(pixels.typecode)

                # reassemble the image upside down
                for x in range((height-1)*stride, -1, -1*stride):
                    flipped_pixels += pixels[x:x+stride]
                texture_block[0] = flipped_pixels

    except:
        print(format_exc())


def load_from_dds_file(convertor, input_path, ext, **kwargs):
    """Loads a DDS file into the convertor."""
    final_input_path = input_path+"."+ext
    unable_to_load = False
    
    try:
        with open(final_input_path, 'r+b') as dds_file:
            dds_data = mmap.mmap(dds_file.fileno(), 0, access=mmap.ACCESS_READ)
            
            height = unpack_from("<L", dds_data, 12)[0]
            width  = unpack_from("<L", dds_data, 16)[0]
            depth  = unpack_from("<L", dds_data, 24)[0]
            
            depth += int(depth == 0)
            b_type = ab.TYPE_2D
            sub_bitmap_count = 1
            
            linear_size  = unpack_from("<L", dds_data, 20)[0]
            mipmap_count = max(unpack_from("<L", dds_data, 28)[0], 1)
            format_flags = unpack_from("<L", dds_data, 80)[0]
            
            dxt_format_id = dds_data[84:88].decode('Latin-1')

            bpp = unpack_from("<L", dds_data, 88)[0]
            r_mask = unpack_from("<L", dds_data, 92)[0]
            g_mask = unpack_from("<L", dds_data, 96)[0]
            b_mask = unpack_from("<L", dds_data, 100)[0]
            a_mask = unpack_from("<L", dds_data, 104)[0]

            caps_1 = unpack_from("<L", dds_data, 108)[0]
            caps_2 = unpack_from("<L", dds_data, 112)[0]

            if dxt_format_id == "DX10":
                #there is a DDS_HEADER_DXT10 extended header present...... shit
                print("THIS MODULE CANNOT LOAD DX10 DDS FILES.")
                return

            #check if the texture is a cubemap and get how many faces exist
            if caps_2&512:
                b_type = ab.TYPE_CUBEMAP
                sub_bitmap_count = ((caps_2&1024)//1024  +(caps_2&2048)//2048 +
                                    (caps_2&4096)//4096  +(caps_2&8192)//8192 +
                                    (caps_2&16384)//16384+(caps_2&32768)//32768)

            #check if the texture is volumetric
            if caps_2&2097152 and depth > 1:
                if b_type == ab.TYPE_CUBEMAP:
                    print("ERROR: DDS HEADER INVALID. TEXTURE "+
                          "SPECIFIED AS BOTH CUBEMAP AND VOLUMETRIC.")
                    return
                b_type = ab.TYPE_3D
                
            if format_flags&4 or dxt_format_id != DXT_FORMAT_ID_BLANK:
                #if the texture has a compression method
                if dxt_format_id in DXT_FORMAT_STRINGS_I:
                    format = DXT_FORMAT_STRINGS_I[dxt_format_id]
                else:
                    print("UNKNOWN DDS FORMAT.",dxt_format_id,
                          "\nUNABLE TO LOAD DDS TEXTURE.")
                    return
            else:
                if format_flags&2:
                    format = ab.FORMAT_A8
                elif format_flags&64:
                    if format_flags&1:
                        format = ab.FORMAT_A8R8G8B8
                    else:
                        format = ab.FORMAT_R8G8B8
                elif format_flags&512:
                    format = ab.FORMAT_Y8U8V8
                elif format_flags&131072:
                    if format_flags&1:
                        format = ab.FORMAT_A8Y8
                    else:
                        format = ab.FORMAT_Y8
                elif format_flags&524288:
                    format = ab.FORMAT_U8V8
                else:
                    print("UNABLE TO DETERMINE DDS FORMAT."+
                          "\nUNABLE TO LOAD DDS TEXTURE")
                    return


                if ab.FORMAT_CHANNEL_COUNTS[format] > 1:
                    #create a channel mapping to shift around the
                    #channels according to the masks in the header
                    channel_mapping = []
                    channel_count = ab.FORMAT_CHANNEL_COUNTS[format]

            #im not sure if it's photoshop doing this, but it's weird....
            if mipmap_count >= 1: mipmap_count -= 1
            
            tex_info = {"width":width, "height":height, "depth":depth,
                        "texture_type":b_type, "mipmap_count":mipmap_count,
                        "sub_bitmap_count":sub_bitmap_count,
                        "format":format, "filepath":input_path}
            
            tmp_tex_block = []
            data_offset = 128
            bitmap_size = None
            
            #loop over each mipmap and cube face
            #and turn them into pixel arrays
            for sb in range(sub_bitmap_count):
                mip_w = width
                mip_h = height
                mip_d = depth
                for m in range(mipmap_count+1):
                    if format == 'DXN':
                        bitmap_size = max(mip_w*mip_h//8, 1)*8
                    elif format in ('DXT1', 'DXT5A', 'DXT5Y'):
                        bitmap_size = max(mip_w*mip_h//16, 1)*8
                    elif format in ('DXT2', 'DXT3', 'DXT4', 'DXT5', 'DXT5AY'):
                        bitmap_size = max(mip_w*mip_h//16, 1)*16

                    data_offset = bitmap_bytes_to_array(
                        dds_data, data_offset, tmp_tex_block,
                        format, width, height, depth, bitmap_size)

                    mip_w, mip_h, mip_d = ab.clip_dimensions(
                        mip_w//2, mip_h//2, mip_d//2, format)

            # rearrange the images so they are sorted by [mip][bitmap]
            tex_block = [None]*len(tmp_tex_block)
            for m in range(mipmap_count+1):
                for sb in range(sub_bitmap_count):
                    tex_block[m*sub_bitmap_count + sb] = tmp_tex_block[
                        sb*(mipmap_count+1) + m]

            convertor.load_new_texture(texture_block=tex_block,
                                       texture_info=tex_info)
    except:
        print(format_exc())


def get_pixel_bytes_size(format, width, height, depth=1):
    pixel_size = ab.PIXEL_ENCODING_SIZES[ab.FORMAT_PACKED_TYPECODES[format]]

    #make sure the dimensions for the format are correct
    width, height, depth = ab.clip_dimensions(width, height, depth, format)
    
    bitmap_size = ab.pixel_count_to_array_length(
        height*width*depth, pixel_size, format)*pixel_size

    return bitmap_size

def make_array(typecode, size):
    return array(typecode, bytearray(size))


def bitmap_bytes_to_array(rawdata, offset, texture_block, format,
                          width, height, depth=1, bitmap_size=None, **kwargs):
    """This function will create an array of pixels of width*height*depth from
    an iterable, sliceable, object, and append it to the supplied texture_block.
    This function will return the offset of the end of the pixel data so that
    textures following the current one can be found."""
    #get the texture encoding
    encoding = ab.FORMAT_PACKED_TYPECODES[format]

    pixel_size = ab.PIXEL_ENCODING_SIZES[encoding]

    #get how many bytes the texture is going to be if it wasnt provided
    if bitmap_size is None:
        bitmap_size = bitmap_data_end = get_pixel_bytes_size(
            format, width, height, depth)
    bitmap_data_end = bitmap_size

    #if the data is compressed,we need to uncompress it
    comp_type = kwargs.get("compression")
    if comp_type: comp_type = comp_type.lower()
    if comp_type in decompressors:
        rawdata, bitmap_data_end = decompressors[compression_type](
            rawdata, format, width, height, depth)
    elif comp_type:
        raise TypeError(
            "CANNOT FIND SPECIFIED DECOMPRESOR FOR SUPPLIED " +
            "PIXEL DATA. COMPRESSION TYPE SPECIFIED IS: %s" % comp_type)
    
    '''24 bit images are handled a bit differently since lots of
    things work on whole powers of 2. "2" can not be raised to an
    integer power to yield "24", whereas it can be for 8, 16, and 32.
    To fix this, the bitmap will be padded with an alpha channel on
    loading and ignored on saving. This will bring the 24 bit image
    up to 32 bit and make everything work just fine.'''
    if ab.BITS_PER_PIXEL[format] == 24:
        #if R8G8B8, need to unpack each byte
        #individually and shift and add them together
        pixel_array = pad_24bit_array(rawdata[
            offset: offset + (height*width*depth*3)])
    elif ab.BITS_PER_PIXEL[format] == 48:
        #if R16G16B16, need to unpack each short
        #individually and shift and add them together
        pixel_array = pad_48bit_array(rawdata[
            offset: offset + (height*width*depth*3)])
    else:
        #stream the start and end of the pixels
        #from the raw_bitmap_data into an array
        pixel_array = array(encoding, rawdata[
            offset: offset + bitmap_size])

    #if not enough pixel data was supplied, extra will be added
    if len(pixel_array)*pixel_size < bitmap_size:
        print("WARNING: PIXEL DATA SUPPLIED DID NOT MEET "+
              "THE SIZE EXPECTED. PADDING WITH ZEROS.")
        pixel_array.extend(
            make_array(pixel_array.typecode,
                       (bitmap_size//pixel_size) - len(pixel_array)))
    
    #add the pixel array to the current texture block
    texture_block.append(pixel_array)
    return offset + bitmap_data_end


def bitmap_palette_to_array(rawdata, offset, palette_block,
                            format, palette_count):
    return bitmap_bytes_to_array(rawdata, offset, palette_block,
                                 format, palette_count, 1)


def bitmap_indexing_to_array(rawdata, offset, indexing_block,
                             width, height, depth=1):
    """This function will create an array of pixels of width*height*depth from
       an iterable, sliceable, object. Since indexing never seems to be more
       than 8 bit, we won't worry about higher bit counts. Appends indexing
       array to supplied indexing_block and returns the end offset
    """
    indexing_block.append(array("B", rawdata[offset:offset+width*height*depth]))
    return offset + width*height*depth


def pad_24bit_array(unpadded):
    if not hasattr(unpadded, 'typecode'):
        unpadded = array("B", unpadded)
    elif unpadded.typecode != 'B':
        raise TypeError(
            "Bad typecode for unpadded 24bit array. Expected B, got %s" %
            unpadded.typecode)

    if fast_bitmap_io:
        padded = make_array("L", len(unpadded)//3)
        bitmap_io_ext.pad_24bit_array(padded, unpadded)
    else:
        padded = array(
            "L", map(lambda x:(
                unpadded[x] + (unpadded[x+1]<<8)+ (unpadded[x+2]<<16)),
                     range(0, len(unpadded), 3)))
    return padded


def pad_48bit_array(unpadded):
    if not hasattr(unpadded, 'typecode'):
        unpadded = array("B", unpadded)
    elif unpadded.typecode != 'B':
        raise TypeError(
            "Bad typecode for unpadded 24bit array. Expected B, got %s" %
            unpadded.typecode)

    if fast_bitmap_io:
        padded = make_array("Q", len(unpadded)//3)
        bitmap_io_ext.pad_48bit_array(padded, unpadded)
    else:
        padded = array(
            "Q", map(lambda x:(
                unpadded[x] + (unpadded[x+1]<<16)+ (unpadded[x+2]<<32)),
                     range(0, len(unpadded), 3)))
    return padded


def unpad_24bit_array(padded):
    """given a 24BPP pixel data array that has been padded to
    32BPP, this will return an unpadded, unpacked, array copy.
    The endianness of the data will be little."""
    
    if padded.typecode == "L":
        # pixels have been packed
        unpadded = make_array("B", len(padded)*3)
        if fast_bitmap_io:
            bitmap_io_ext.unpad_24bit_array(unpadded, padded)
        else:
            for i in range(len(padded)):
                unpadded[i*3] = padded[i]&255
                unpadded[i*3+1] = (padded[i]&65280)>>8
                unpadded[i*3+2] = (padded[i]&16711680)>>16
    elif padded.typecode == "B":
        # pixels have NOT been packed

        # Because they havent been packed, it should be assumed
        # the channel order is the default one, namely ARGB.
        # Since we are removing the alpha channel, remove
        # the first byte from each pixel
        unpadded = make_array("B", (len(padded)//4)*3)
        if fast_bitmap_io:
            bitmap_io_ext.unpad_24bit_array(unpadded, padded)
        else:
            for i in range(len(padded)//4):
                unpadded[i*3] = padded[i*4+1]
                unpadded[i*3+1] = padded[i*4+2]
                unpadded[i*3+2] = padded[i*4+3]
    else:
        raise TypeError(
            "Bad typecode for padded 24bit array. Expected H or Q, got %s" %
            padded.typecode)
        
    return unpadded


def unpad_48bit_array(padded):
    """given a 48BPP pixel data array that has been padded to
    64BPP, this will return an unpadded, unpacked, array copy.
    The endianness of the data will be little."""
    
    if padded.typecode == "Q":
        # pixels have been packed
        unpadded = make_array("H", len(padded)*6)
        if fast_bitmap_io:
            bitmap_io_ext.unpad_48bit_array(unpadded, padded)
        else:
            for i in range(len(padded)):
                j = i*3
                unpadded[j] = padded[i]&65535
                unpadded[j+1] = (padded[i]&4294901760)>>16
                unpadded[j+2] = (padded[i]&281470681743360)>>32
    elif padded.typecode == "H":
        # pixels have NOT been packed

        # Because they havent been packed, it should be assumed
        # the channel order is the default one, namely ARGB.
        # Since we are removing the alpha channel, remove
        # the first two bytes from each pixel
        unpadded = make_array("H", (len(padded)//4)*6)
        if fast_bitmap_io:
            bitmap_io_ext.unpad_48bit_array(unpadded, padded)
        else:
            for i in range(len(padded)//4):
                j = i*3
                i *= 4
                unpadded[j] = padded[i+1]
                unpadded[j+1] = padded[i+2]
                unpadded[j+2] = padded[i+3]
    else:
        raise TypeError(
            "Bad typecode for padded 48bit array. Expected H or Q, got %s" %
            padded.typecode)
        
    return unpadded


def uncompress_rle(comp_bytes, format, width, height, depth=1):
    """given an array compressed with run length encoding, this
    function will uncompress it and return the uncompressed array"""

    #get the texture encoding
    encoding = ab.FORMAT_PACKED_TYPECODES[format]
    bpp = ab.BITS_PER_PIXEL[format]

    #make sure the dimensions for the format are correct
    w, h, d = ab.clip_dimensions(width, height, depth, format)

    #get how many bytes the texture is going to be
    uncomp = bytearray(get_pixel_bytes_size(format, w, h, d))

    pix_byte_count = w*h*d*(bpp//8)
    i = 0
    pos = 0
    
    ######################
    '''NEEDS MORE SPEED'''
    ######################
    try:
        if bpp == 32:
            while i < pix_byte_count:
                #if this packet is compressed with RLE
                if comp_bytes[pos]&128:
                    for i in range(0, (comp_bytes[pos]-127)*4, 4):
                        j = i*2
                        uncomp[j]   = comp_bytes[pos+1]
                        uncomp[j+1] = comp_bytes[pos+2]
                        uncomp[j+2] = comp_bytes[pos+3]
                        uncomp[j+3] = comp_bytes[pos+4]
                    i += (comp_bytes[pos]-127)*4
                    pos += 5
                else:#if it's a raw packet
                    for i in range(0, (comp_bytes[pos]+1)*4, 4):
                        j = i*2
                        uncomp[j]   = comp_bytes[pos+i+1]
                        uncomp[j+1] = comp_bytes[pos+i+2]
                        uncomp[j+2] = comp_bytes[pos+i+3]
                        uncomp[j+3] = comp_bytes[pos+i+4]
                    i += (comp_bytes[pos]+1)*4
                    pos += (comp_bytes[pos]+1)*4+1
        elif bpp == 24:
            while i < pix_byte_count:
                #if this packet is compressed with RLE
                if comp_bytes[pos]&128:
                    for i in range(0, (comp_bytes[pos]-127)*3, 3):
                        j = i*2
                        uncomp[j]   = comp_bytes[pos+1]
                        uncomp[j+1] = comp_bytes[pos+2]
                        uncomp[j+2] = comp_bytes[pos+3]
                    i += (comp_bytes[pos]-127)*3
                    pos += 4
                else:#if it's a raw packet
                    for i in range(0, (comp_bytes[pos]+1)*3, 3):
                        j = i*2
                        uncomp[j]   = comp_bytes[pos+i+1]
                        uncomp[j+1] = comp_bytes[pos+i+2]
                        uncomp[j+2] = comp_bytes[pos+i+3]
                    i += (comp_bytes[pos]+1)*3
                    pos += (comp_bytes[pos]+1)*3+1
        elif bpp == 16:
            while i < pix_byte_count:
                #if this packet is compressed with RLE
                if comp_bytes[pos]&128:
                    for i in range(0, (comp_bytes[pos]-127)*2, 2):
                        j = i*2
                        uncomp[j]   = comp_bytes[pos+1]
                        uncomp[j+1] = comp_bytes[pos+2]
                    i += (comp_bytes[pos]-127)*2
                    pos += 3
                else:#if it's a raw packet
                    for i in range(0, (comp_bytes[pos]+1)*2, 2):
                        j = i*2
                        uncomp[j]   = comp_bytes[pos+i+1]
                        uncomp[j+1] = comp_bytes[pos+i+2]
                    i += (comp_bytes[pos]+1)*2
                    pos += (comp_bytes[pos]+1)*2+1
        else:
            while i < pix_byte_count:
                #if this packet is compressed with RLE
                if comp_bytes[pos]&128:
                    for i in range(comp_bytes[pos]-127):
                        uncomp[i*2] = comp_bytes[pos+1]
                    i += comp_bytes[pos]-127
                    pos += 2
                else:#if it's a raw packet
                    for i in range(comp_bytes[pos]+1):
                        uncomp[i*2] = comp_bytes[pos+i+1]
                    i += comp_bytes[pos]+1
                    pos += comp_bytes[pos]+2
    except IndexError:
        #index errors can be silently passed since the bytes
        #have been padded to their expected size already
        #just need to fix the final read offset
        if comp_bytes[pos]&128:
            pos += (bpp//8)+1
        else:
            pos += (comp_bytes[pos]+1)*(bpp//8)+1

    return(uncomp, pos)



file_writers = {"tga":save_to_tga_file, "dds":save_to_dds_file,
                "raw":save_to_rawdata_file}
file_readers = {"tga":load_from_tga_file, "dds":load_from_dds_file}
decompressors = {"rle":uncompress_rle}


def write_tga_header(tga_file, **kwargs):
    ''' This function can be used to construct a TGA header. The
        first argument must be the buffer that the TGA file will be
        written to. The keywords that can be supplied are these.

        bpp---(BYTE)
        width---(SHORT)
        height---(SHORT)
        id_length---(BYTE)
        image_type---(BYTE)
        image_origin---[(SHORT),(SHORT)]
        color_map_type---(BYTE)
        color_map_depth---(BYTE)
        color_map_origin---(SHORT)
        color_map_length---(SHORT)
        image_desc---(BYTE)
    '''

    buf = bytearray(18)
        
    pack_into('B',  buf, 0,  kwargs.get("id_length",0))
    pack_into('B',  buf, 1,  kwargs.get("color_map_type",0))
    pack_into('B',  buf, 2,  kwargs.get("image_type",2))
    pack_into('<H', buf, 3,  kwargs.get("color_map_origin",0))
    pack_into('<H', buf, 5,  kwargs.get("color_map_length",0))
    pack_into('B',  buf, 7,  kwargs.get("color_map_depth",0))
    pack_into('<H', buf, 8,  kwargs.get("image_origin", (0,0))[0])
    pack_into('<H', buf, 10, kwargs.get("image_origin", (0,0))[1])
    
    pack_into('<H', buf, 12, kwargs.get("width",0))
    pack_into('<H', buf, 14, kwargs.get("height",0))
    pack_into('B',  buf, 16, kwargs.get("bpp",0))
    pack_into('B',  buf, 17, 32 + (kwargs.get("image_desc",0)&223))

    tga_file.write(buf)
    return 18


def write_dds_header(dds_file, **kwargs):
    ''' This function can be used to construct a DDS header. The first
        argument must be the buffer that the DDS file will be written to.
        The keywords that can be supplied are these.

        compressed---(Boolean)
        width---(LONG)
        height---(LONG)
        depth---(LONG)
        mipmap_count---(LONG)
        dxt_format_id---(4BYTE STRING)*
        channel_count---(LONG 0-4)
        bpp---(LONG)
        r_mask---(LONG)
        g_mask---(LONG)
        b_mask---(LONG)
        a_mask---(LONG)
    '''
    ################################################################
    #
    # WARNING: I hate this function. Its so ugly and poorly written.
    #          I intend to clean it up at some point, but not now.
    #
    ################################################################


    if kwargs is not None:
        buf = bytearray(128)

        for i in range(len(DXT_VAR_OFFSETS)):
            #fill in any missing variables
            if DXT_HEADER_VAR_NAMES[i] not in kwargs:
                kwargs[DXT_HEADER_VAR_NAMES[i]] = DXT_VAR_DEFAULTS[i]
        
        if not "compressed" in kwargs:
            print("ERROR: MUST SPECIFY WHETHER OR NOT TEXTURE IS COMPRESSED.\n")
            return False
        
            
        elif isinstance(kwargs["dxt_format_id"], str):
            kwargs["dxt_format_id"] = kwargs["dxt_format_id"]\
                                      [0:4].encode('Latin-1')


        if kwargs["compressed"]:
            kwargs["channel_count"] = 0
        else:
            if (not "channel_count" in kwargs  or
                (not isinstance(kwargs["channel_count"], int)) or
                (kwargs["channel_count"] > 4 or kwargs["channel_count"] < 0)):
                print("ERROR: CHANNEL COUNT OF EITHER 1, 2, 3, "+
                      "OR 4 REQUIRED FOR UNCOMPRESSED TEXTURES.\n")
                return False

            """I could worry about checking the validity of the
            channel masks here, but what's the point?"""


        #figure out if the texture is 2D, a cubemap, or volumetric
        if "texture_type" in kwargs and (kwargs["texture_type"].upper() in
                                         DXT_TEXTURE_TYPE_MAP):
            kwargs["texture_type"] = DXT_TEXTURE_TYPE_MAP\
                                     [kwargs["texture_type"].upper()]
        else:
            #default to a 2d texture
            kwargs["texture_type"] = 0


        #set the mipmap flag
        if kwargs["mipmap_count"] > 0:
            kwargs["flags"] = (kwargs["flags"] & 8917007) + 131072
            kwargs["caps_1"] = (kwargs["caps_1"] & 4104) + 4194304
            
        #set the cubemap flags
        if kwargs["texture_type"] == 2:
            kwargs["caps_2"] = 65024
            
        #set the volumetric texture flag
        if kwargs["depth"] > 1:
            kwargs["flags"] = (kwargs["flags"] & 659471) + 8388608
            kwargs["caps_2"] = 2097152
            
        #set the complex surface flag
        if kwargs["texture_type"] > 0 or kwargs["mipmap_count"] > 0:
            kwargs["caps_1"] = (kwargs["caps_1"] & 4198400) + 8

            
        #set the pixel format flags
        if kwargs["compressed"]:
            kwargs["pixel_format_flags"] = 4
            kwargs["flags"] = (kwargs["flags"] & 4294443007) + 524288
        elif kwargs["channel_count"] == 1:
            if kwargs["format"] == ab.FORMAT_A8:
                kwargs["pixel_format_flags"] = 2
            else:
                kwargs["pixel_format_flags"] = 131072
        elif kwargs["channel_count"] == 2:
            kwargs["pixel_format_flags"] = 131073
        elif kwargs["channel_count"] == 3:
            if kwargs["format"] == ab.FORMAT_Y8U8V8:
                kwargs["pixel_format_flags"] = 512
            elif kwargs["format"] == ab.FORMAT_U8V8:
                kwargs["pixel_format_flags"] = 524288
            else:
                kwargs["pixel_format_flags"] = 64
        elif kwargs["channel_count"] == 4:
            kwargs["pixel_format_flags"] = 65
                
        if not kwargs["compressed"]:
            kwargs["pitch_or_linear_size"] = kwargs["width"]*(kwargs["bpp"]//8)\
                                             *kwargs["channel_count"]

        #set the required flags
        kwargs["flags"] = (kwargs["flags"] & 9043976) + 4103
        kwargs["caps_1"] = (kwargs["caps_1"] & 4194312) + 4096

        #the mipmap count includes the largest dimension image,
        #so it's always at least 1. I think it's photoshop being
        #an idiot and not knowing how mipmaps actually work.
        kwargs["mipmap_count"] += 1

        for i in range(len(DXT_VAR_OFFSETS)):
            #Write the variable to the header
            if isinstance(kwargs[DXT_HEADER_VAR_NAMES[i]], bytes):
                for b in range(len(kwargs[DXT_HEADER_VAR_NAMES[i]])):
                    pack_into('B', buf,
                              DXT_VAR_OFFSETS[i]+b,
                              kwargs[DXT_HEADER_VAR_NAMES[i]][b] )
            else:
                pack_into('<L', buf, DXT_VAR_OFFSETS[i],
                          kwargs[DXT_HEADER_VAR_NAMES[i]])
            
        dds_file.write(buf)
        #return the offset that we are currently at
        return 128
    else:
        print("CANNOT CONSTRUCT DXT HEADER WITHOUT PROPER INFORMATION")
        return False
