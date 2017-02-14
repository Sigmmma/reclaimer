from array import array


"""TEXTURE TYPES"""
TYPE_2D = "2D"
TYPE_3D = "3D"
TYPE_CUBEMAP = "CUBE"

"""TEXTURE FORMATS"""
FORMAT_STENCIL = "STENCIL"#NOT YET IMPLEMENTED
FORMAT_A4 = "Y4"#NOT YET IMPLEMENTED
FORMAT_A8 = "A8"
FORMAT_Y4 = "Y4"#NOT YET IMPLEMENTED
FORMAT_Y8 = "Y8"
FORMAT_AY8 = "AY8"
FORMAT_A8Y8 = "A8Y8"
FORMAT_R3G3B2 = "R3G3B2"
FORMAT_R5G6B5 = "R5G6B5"
FORMAT_R8G8B8 = "R8G8B8"
FORMAT_Y8U8V8 = "Y8U8V8"
FORMAT_A1R5G5B5 = "A1R5G5B5"
FORMAT_A4R4G4B4 = "A4R4G4B4"
FORMAT_X8R8G8B8 = "X8R8G8B8"
FORMAT_A8R8G8B8 = "A8R8G8B8"

#DEEP COLOR SUPPORT
FORMAT_R16G16B16 = "R16G16B16"
FORMAT_A16R16G16B16 = "A16R16G16B16"


#FLOATING POINT SUPPORT
'''NONE OF THESE ARE IMPLEMENTED YET'''
FORMAT_R16F = "R16F"                  #Will require Numpy
FORMAT_R32F = "R32F"
FORMAT_R16G16B16F    = "R16G16B16F"   #Will require Numpy
FORMAT_A16R16G16B16F = "A16R16G16B16F"
FORMAT_R32G32B32F    = "R32G32B32F"
FORMAT_A32R32G32B32F = "A32R32G32B32F"


"""COLOR CHANNEL ORDERS"""
#these are different orders that the color channels can be in.
#rather than make multiple types for each format with 3 or more
#channels, we define the different ways the channels can be ordered
"""channel values are in little endian: least significant byte first.
   So for example, in C_ORDER_BGRA, B is the first byte, and if the
   pixel were read as a 32 bit integer, B's bits would be values 0-255
"""
C_ORDER_ARGB = "ARGB"  # <---THE ORDER Arbytmap UNPACKS TO
C_ORDER_ABGR = "ABGR"
C_ORDER_RGBA = "RGBA"
C_ORDER_BGRA = "BGRA"  # <---DEFAULT FOR MOST IMAGE FORMATS

#Default pixel storing order for most image formats is little endian BGRA
'''The format Arbytmap will store pixels in will ALWAYS be ARGB.
   This does NOT apply to 1 and 2 channel formats though, so they are
   instead always unpacked to AY or A.
   In the future I intend to make it so you can specify which format
   to load from/save to, but the internal format will always be ARGB.
'''
C_ORDER_DEFAULT = C_ORDER_ARGB


#The texture_info is a dictionary which serves the purpose of describing
#the texture in full. The variables it can contain are these:
'''
width - width of the texture in pixels
height - height of the texture in pixels
depth - depth of the texture in pixels
type - the type that the texture is(look above for the different types)
format - the format that the texture is(look above for the different types)
mipmap_count - the number of mipmaps in the texture(fullsize doesnt count)
sub_texture_count - the number of sub-textures in the texture(cubemaps have 6)
swizzled - whether or not the texture is swizzled
swizzler - the type of swizzler method to use to swizzle or deswizzle texture
'''

PIXEL_ENCODING_SIZES = {"B":1, "H":2, "L":4, "Q":8, "b":1, "h":2, "l":4, "q":8}
INVERSE_PIXEL_ENCODING_SIZES = {
    0:"B", 1:"B",
    2:"H",
    3:"L", 4:"L",
    5:"Q", 6:"Q", 7:"Q", 8:"Q"}

#HALF FLOAT "f" WILL REQUIRE Numpy
PIXEL_ENCODING_SIZES_F = {"f":2, "F":4}
INVERSE_PIXEL_ENCODING_SIZES_F = {2:"f", 4:"F"}


VALID_FORMATS = set([
    FORMAT_A4, FORMAT_A8,
    FORMAT_Y4, FORMAT_Y8,
    FORMAT_AY8,  FORMAT_A8Y8,
    FORMAT_R3G3B2, FORMAT_R5G6B5,
    FORMAT_R8G8B8, FORMAT_Y8U8V8,
    FORMAT_A1R5G5B5, FORMAT_A4R4G4B4,
    FORMAT_X8R8G8B8, FORMAT_A8R8G8B8,
    FORMAT_STENCIL,
    FORMAT_R16G16B16, FORMAT_A16R16G16B16])

RAW_FORMATS = set([
    FORMAT_A4, FORMAT_A8,
    FORMAT_Y4, FORMAT_Y8,
    FORMAT_AY8,  FORMAT_A8Y8,
    FORMAT_R3G3B2, FORMAT_R5G6B5,
    FORMAT_R8G8B8, FORMAT_Y8U8V8,
    FORMAT_A1R5G5B5, FORMAT_A4R4G4B4,
    FORMAT_X8R8G8B8, FORMAT_A8R8G8B8,
    FORMAT_STENCIL,
    FORMAT_R16G16B16, FORMAT_A16R16G16B16])

COMPRESSED_FORMATS = set()

DDS_FORMATS = set()

THREE_CHANNEL_FORMATS = set([
    FORMAT_R3G3B2, FORMAT_R5G6B5, FORMAT_R8G8B8,
    FORMAT_R16G16B16, FORMAT_Y8U8V8])

FORMAT_UNPACKERS = {}

FORMAT_PACKERS = {}

SUB_BITMAP_COUNTS = {TYPE_2D:1, TYPE_3D:1, TYPE_CUBEMAP:6}

MINIMUM_W = {
    FORMAT_A4:1, FORMAT_A8:1,
    FORMAT_Y4:1, FORMAT_Y8:1,
    FORMAT_AY8:1,  FORMAT_A8Y8:1,
    FORMAT_R3G3B2:1, FORMAT_R5G6B5:1,
    FORMAT_R8G8B8:1, FORMAT_Y8U8V8:1,
    FORMAT_A1R5G5B5:1, FORMAT_A4R4G4B4:1,
    FORMAT_X8R8G8B8:1, FORMAT_A8R8G8B8:1,
    FORMAT_STENCIL:1,
    FORMAT_R16G16B16:1, FORMAT_A16R16G16B16:1}

MINIMUM_H = {
    FORMAT_A4:1, FORMAT_A8:1,
    FORMAT_Y4:1, FORMAT_Y8:1,
    FORMAT_AY8:1,  FORMAT_A8Y8:1,
    FORMAT_R3G3B2:1, FORMAT_R5G6B5:1,
    FORMAT_R8G8B8:1, FORMAT_Y8U8V8:1,
    FORMAT_A1R5G5B5:1, FORMAT_A4R4G4B4:1,
    FORMAT_X8R8G8B8:1, FORMAT_A8R8G8B8:1,
    FORMAT_STENCIL:1,
    FORMAT_R16G16B16:1, FORMAT_A16R16G16B16:1}

MINIMUM_D = {
    FORMAT_A4:1, FORMAT_A8:1,
    FORMAT_Y4:1, FORMAT_Y8:1,
    FORMAT_AY8:1,  FORMAT_A8Y8:1,
    FORMAT_R3G3B2:1, FORMAT_R5G6B5:1,
    FORMAT_R8G8B8:1, FORMAT_Y8U8V8:1,
    FORMAT_A1R5G5B5:1, FORMAT_A4R4G4B4:1,
    FORMAT_X8R8G8B8:1, FORMAT_A8R8G8B8:1,
    FORMAT_STENCIL:1,
    FORMAT_R16G16B16:1, FORMAT_A16R16G16B16:1}

# this is how many BITS(NOT BYTES) each format's pixels take up
BITS_PER_PIXEL = {
    FORMAT_A4:4, FORMAT_A8:8,
    FORMAT_Y4:4, FORMAT_Y8:8,
    FORMAT_AY8:8,  FORMAT_A8Y8:16,
    FORMAT_R3G3B2:8, FORMAT_R5G6B5:16,
    FORMAT_R8G8B8:24, FORMAT_Y8U8V8:24,
    FORMAT_A1R5G5B5:16, FORMAT_A4R4G4B4:16,
    FORMAT_X8R8G8B8:32, FORMAT_A8R8G8B8:32,
    FORMAT_STENCIL:1, 
    FORMAT_R16G16B16:48, FORMAT_A16R16G16B16:64}

# this is the typecode that each format's pixel data array will use
FORMAT_PACKED_TYPECODES = {
    FORMAT_A4:"B", FORMAT_A8:"B",
    FORMAT_Y4:"B", FORMAT_Y8:"B",
    FORMAT_AY8:"B",  FORMAT_A8Y8:"H",
    FORMAT_R3G3B2:"B", FORMAT_R5G6B5:"H",
    FORMAT_R8G8B8:"L", FORMAT_Y8U8V8:"L",
    FORMAT_A1R5G5B5:"H", FORMAT_A4R4G4B4:"H",
    FORMAT_X8R8G8B8:"L", FORMAT_A8R8G8B8:"L",
    FORMAT_STENCIL:"B", 
    FORMAT_R16G16B16:"Q", FORMAT_A16R16G16B16:"Q"}

# the number of channels possible in each format,
# regardless of whether or not they are raw formats
FORMAT_CHANNEL_COUNTS = {
    FORMAT_A4:1, FORMAT_A8:1,
    FORMAT_Y4:1, FORMAT_Y8:1,
    FORMAT_AY8:1,  FORMAT_A8Y8:2,
    FORMAT_R3G3B2:4, FORMAT_R5G6B5:4,
    FORMAT_R8G8B8:4, FORMAT_Y8U8V8:4,
    FORMAT_A1R5G5B5:4, FORMAT_A4R4G4B4:4,
    FORMAT_X8R8G8B8:4, FORMAT_A8R8G8B8:4,
    FORMAT_STENCIL:1,
    FORMAT_R16G16B16:4, FORMAT_A16R16G16B16:4}

# this is how many bits the depth of each channel is for each raw format
FORMAT_CHANNEL_DEPTHS = {
    FORMAT_A4:(4,), FORMAT_A8:(8,),
    FORMAT_Y4:(4,), FORMAT_Y8:(8,),
    FORMAT_AY8:(8,), FORMAT_A8Y8:(8,8),
    FORMAT_R3G3B2:(0,2,3,3), FORMAT_R5G6B5:(0,5,6,5),
    FORMAT_R8G8B8:(0,8,8,8), FORMAT_Y8U8V8:(0,8,8,8),
    FORMAT_A1R5G5B5:(1,5,5,5), FORMAT_A4R4G4B4:(4,4,4,4),
    FORMAT_X8R8G8B8:(0,8,8,8), FORMAT_A8R8G8B8:(8,8,8,8),
    FORMAT_STENCIL:(1,),
    FORMAT_R16G16B16:(0,16,16,16),
    FORMAT_A16R16G16B16:(16,16,16,16)}

# this is the mask of each channel in each format
FORMAT_CHANNEL_MASKS = {
    FORMAT_A4:(15,), FORMAT_A8:(255,),
    FORMAT_Y4:(15,), FORMAT_Y8:(255,),
    FORMAT_AY8:(255,),  FORMAT_A8Y8:(65280,255),
    FORMAT_R3G3B2:(0,192,56,7),
    FORMAT_R5G6B5:(0,63488,2016,31),
    FORMAT_A1R5G5B5:(32768, 31744, 992, 31),
    FORMAT_R8G8B8:(0, 16711680, 65280, 255),
    FORMAT_Y8U8V8:(0, 16711680, 65280, 255),
    FORMAT_A4R4G4B4:(61440, 3840, 240, 15),
    FORMAT_X8R8G8B8:(0, 16711680, 65280, 255),
    FORMAT_A8R8G8B8:(4278190080, 16711680, 65280, 255),
    FORMAT_STENCIL:(1,),
    FORMAT_R16G16B16:(0, 2**48-2**32, 4294901760, 65535),
    FORMAT_A16R16G16B16:(2**64-2**48, 2**48-2**32, 4294901760, 65535)}

# this is how far right the channel is shifted when
# unpacked and left when repacked
FORMAT_CHANNEL_OFFSETS = {
    FORMAT_A4:(0,), FORMAT_A8:(0,),
    FORMAT_Y4:(0,), FORMAT_Y8:(0,),
    FORMAT_AY8:(0,), FORMAT_A8Y8:(8,0),
    FORMAT_R3G3B2:(0,6,3,0), FORMAT_R5G6B5:(0,11,5,0),
    FORMAT_R8G8B8:(0,16,8,0), FORMAT_Y8U8V8:(0,16,8,0),
    FORMAT_A1R5G5B5:(15,10,5,0), FORMAT_A4R4G4B4:(12,8,4,0),
    FORMAT_X8R8G8B8:(0,16,8,0), FORMAT_A8R8G8B8:(24,16,8,0),
    FORMAT_STENCIL:(0,),
    FORMAT_R16G16B16:(0,32,16,0), FORMAT_A16R16G16B16:(48,32,16,0)}

# if a channel has this in it's divisor it
# will be erased when the bitmap is repacked
CHANNEL_ERASE_DIVISOR = 2**31-1

# this is the default amount of bits per pixel for palettized bitmaps
DEFAULT_INDEXING_SIZE = 8

DEFAULT_UNPACK_FORMAT = FORMAT_A8R8G8B8

ALL_FORMAT_COLLECTIONS = {
    "VALID_FORMAT":VALID_FORMATS, "BITS_PER_PIXEL":BITS_PER_PIXEL,
    "RAW_FORMAT":RAW_FORMATS, "THREE_CHANNEL_FORMAT":THREE_CHANNEL_FORMATS,
    "COMPRESSED_FORMAT":COMPRESSED_FORMATS, "DDS_FORMAT":DDS_FORMATS,
    "MINIMUM_W":MINIMUM_W, "MINIMUM_H":MINIMUM_H, "MINIMUM_D":MINIMUM_D,
    "PACKED_TYPECODES":FORMAT_PACKED_TYPECODES, "UNPACKER":FORMAT_UNPACKERS,
    "CHANNEL_COUNT":FORMAT_CHANNEL_COUNTS, "PACKER":FORMAT_PACKERS,
    "CHANNEL_OFFSETS":FORMAT_CHANNEL_OFFSETS,
    "CHANNEL_MASKS":FORMAT_CHANNEL_MASKS,
    "CHANNEL_DEPTHS":FORMAT_CHANNEL_DEPTHS}


"""##################"""
### CHANNEL MAPPINGS ###
"""##################"""

# the way channel mappings work is that each index is one channel.
# in their standard form the value at each index should be the
# number of that index. Ex:(0, 1, 2, 3)

# to remove channels you should create a mapping with exactly
# how many channels you want to have and have the value of each
# index be the channel that you want to place there.
# Ex: (A, R, G, B) to (G, B) would use the mapping (2, 3)

# to switch channels around you would create a mapping with one
# index for each channel in the target format. the value at each
# index will be the index of the channel you want from the source format.
# Ex: (A, R, G, B) to (B, G, R, A) would use the mapping (3, 2, 1, 0)

# if you want a blank channel to be made then set the value at that index to -1
# Ex: converting A8 to A8R8G8B8 = (0, -1, -1, -1)


"""these channel mappings are used to swap ALPHA AND
INTENSITY, but ONLY if the source bitmap is A8Y8"""
#                ( A, Y )
AY_TO_YA = ( 1, 0 )
A_TO_AY  = ( 0,-1 )
Y_TO_AY  = (-1, 0 )

"""these channel mappings are used to convert different
formats to Y8 and A8. these are also used for converting to AY8.
just use the one that preserves the channel you want to keep"""
#               (A)
ANYTHING_TO_A = (0,)
#         (Y)
AY_TO_Y = (1,)

"""these channel mappings are to convert
A8, Y8, AY, and YA to A8R8G8B8 and X8R8G8B8"""
#                  ( A,  R,  G,  B)
A_TO_ARGB = ( 0, -1, -1, -1)
Y_TO_ARGB = (-1,  0,  0,  0)

AY_TO_ARGB = ( 0,  1,  1,  1)
YA_TO_ARGB = ( 1,  0,  0,  0)


"""########################"""
### CHANNEL MERGE MAPPINGS ###
"""########################"""

# why merge mappings are used is that if the target format has
# less channels than the source then we either need to remove
# channels or merge them together. we can remove them with the
# above channel mappings, but for things like RGB to monochrome
# we need to merge the pixels together to get the average intensity.

#merge mapping are the length of the source's channel count. each index is
#which channel in the target format to merge the channel from the source into.
#Ex: merging ARGB's 4 channel into A8Y8 would be (0, 1, 1, 1)

#              ( A,  R,  G,  B )
M_ARGB_TO_AY = ( 0,  1,  1,  1 )
M_ARGB_TO_YA = ( 1,  0,  0,  0 )
M_ARGB_TO_Y  = ( -1, 0,  0,  0 )
M_ARGB_TO_A  = ( 0, -1, -1, -1 )


def define_format(**kwargs):
    """THIS FUNCTION CAN BE CALLED TO DEFINE A NEW FORMAT TYPE"""
    try:
        f_id = kwargs.get("format_id")
        bpp = kwargs.get("bpp", sum(kwargs.get("depths", ())))

        if f_id is None:
            raise TypeError(
                "No identifier supplied for format.\n" +
                "This must be a hashable type, such as an int or str.")
        elif f_id in VALID_FORMATS:
            raise TypeError((
                "Cannot add '%s' format definition to Arbytmap as " +
                "that format identifier is already in use.") % fid)
        elif not bpp:
            raise TypeError((
                "Cannot define '%s' format without a given bits per " +
                "pixel or specifying each channels bit depths.") % fid)

        VALID_FORMATS.add(f_id)

        if kwargs.get("raw_format"): RAW_FORMATS.add(f_id)
        if kwargs.get("compressed"): COMPRESSED_FORMATS.add(f_id)
        if kwargs.get("dds_format"): DDS_FORMATS.add(f_id)
        if kwargs.get("three_channels"): THREE_CHANNEL_FORMATS.add(f_id)

        FORMAT_UNPACKERS[f_id] = kwargs.get("unpacker")
        FORMAT_PACKERS[f_id] = kwargs.get("packer")

        MINIMUM_W[f_id] = kwargs.get("min_width", 1)
        MINIMUM_H[f_id] = kwargs.get("min_height", 1)
        MINIMUM_D[f_id] = kwargs.get("min_depth", 1)

        BITS_PER_PIXEL[f_id] = bpp
        FORMAT_CHANNEL_COUNTS[f_id] = 1
        packed_typecode = kwargs.get(
            "packed_typecode", INVERSE_PIXEL_ENCODING_SIZES[bpp//8])

        FORMAT_PACKED_TYPECODES[f_id] = packed_typecode
        FORMAT_CHANNEL_COUNTS[f_id] = kwargs.get("channel_count")
        FORMAT_CHANNEL_MASKS[f_id] = kwargs.get("masks")
        FORMAT_CHANNEL_DEPTHS[f_id] = kwargs.get("depths")
        FORMAT_CHANNEL_OFFSETS[f_id] = kwargs.get("offsets")

    except:
        print("Error occurred while trying to define new texture format.")
        print(format_exc())


def print_format(format_id, printout=True):
    out_str = "%s Format Definition:\n" % format_id
    for key in sorted(ALL_FORMAT_COLLECTIONS.keys()):
        val = ALL_FORMAT_COLLECTIONS[key]
        if not isinstance(val, dict):
            out_str += '    %s:\n' % (key, format_id in val)
        elif format_id in val:
            out_str += '    %s:%s\n' % (key, val[format_id])
        else:
            out_str += '    %s:\n' % key
    out_str += '\n'
    if printout:
        print(out_str)
    return out_str


def remove_format(format_id):
    for val in ALL_FORMAT_COLLECTIONS.values():
        if format_id not in val:
            continue
        elif isinstance(val, dict):
            del val[format_id]
        else:
            val.pop(val.index(format_id))


def array_length_to_pixel_count(array_len, pixel_size, format):
    '''used to figure out the number of pixels in an array
    of a certain length, with each pixel of a certain
    integer size per pixel, and a certain texture format'''
    return (array_len*8*pixel_size)//BITS_PER_PIXEL[format]


def pixel_count_to_array_length(pixel_count, pixel_size, format):
    '''used to figure out the length of an array that will
    hold a certain number of pixels which will take up a
    certain number of bytes each and are of a certain format'''
    return ((pixel_count*BITS_PER_PIXEL[format])//8)//pixel_size


def get_mipmap_dimensions(width, height, depth, mipmap_level, format):
    '''This function will give the dimensions of the
    specified mipmap level, format, and fullsize dimensions'''
    #since the dimensions change per mipmap we need to calculate them
    return (clip_dimensions(
        width//2**mipmap_level, height//2**mipmap_level,
        depth//2**mipmap_level, format))


def clip_dimensions(width, height, depth=1, fmt=FORMAT_A8R8G8B8):
    '''clips the supplied width, height, and depth to
    what the minimum is defined for the format'''
    return(max(width,  MINIMUM_W[fmt]),
           max(height, MINIMUM_H[fmt]),
           max(depth,  MINIMUM_D[fmt]))
