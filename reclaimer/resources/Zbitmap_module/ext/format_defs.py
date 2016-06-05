
from array import array

"""Qwords are still new so they aren't entirely supported. Try
to use them if possible, but default to unsigned long's if not."""
try:
    powers_of_2 = array("Q",[])
    #used in calculating new dimensions
    for pwr in range(64):
        powers_of_2.append(pow(2, pwr))
except:
    powers_of_2 = array("I",[])
    #used in calculating new dimensions
    for pwr in range(32):
        powers_of_2.append(pow(2, pwr))



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
C_ORDER_ARGB = "ARGB"
C_ORDER_ABGR = "ABGR"
C_ORDER_RGBA = "RGBA"
C_ORDER_BGRA = "BGRA" #<---DEFAULT

#Default pixel storing order for most image formats is little endian BGRA
C_ORDER_DEFAULT = C_ORDER_BGRA


#The Texture_Info is a dictionary which serves the purpose of describing
#the texture in full. The variables it can contain are these:
'''
width - width of the texture in pixels
height - height of the texture in pixels
depth - depth of the texture in pixels
TYPE - the type that the texture is(look above for the different types)
format - the format that the texture is(look above for the different types)
Mipmap_Count - the number of mipmaps in the texture(fullsize image doesnt count as a mipmap)
Sub_Texture_Count - the number of sub-textures in the texture(cubemaps have 6 faces, so 6 sub-bitmaps)
Swizzled - whether or not the texture is swizzled
Swizzler - the type of swizzler method to use to swizzle or deswizzle texture
'''

PIXEL_ENCODING_SIZES = {"B":1, "H":2, "I":4, "Q":8}
INVERSE_PIXEL_ENCODING_SIZES = {0:"B", 1:"B",
                                2:"H",
                                3:"I", 4:"I",
                                5:"Q", 6:"Q", 7:"Q", 8:"Q"}

#HALF FLOAT "f" WILL REQUIRE Numpy
PIXEL_ENCODING_SIZES_F = {"f":2, "F":4}
INVERSE_PIXEL_ENCODING_SIZES_F = {2:"f", 4:"F"}


VALID_FORMATS = [FORMAT_A4, FORMAT_A8,
                 FORMAT_Y4, FORMAT_Y8,
                 FORMAT_AY8,  FORMAT_A8Y8,
                 FORMAT_R3G3B2, FORMAT_R5G6B5,
                 FORMAT_R8G8B8, FORMAT_Y8U8V8,
                 FORMAT_A1R5G5B5, FORMAT_A4R4G4B4,
                 FORMAT_X8R8G8B8, FORMAT_A8R8G8B8,
                 FORMAT_STENCIL,
                 FORMAT_R16G16B16, FORMAT_A16R16G16B16]

RAW_FORMATS = [FORMAT_A4, FORMAT_A8,
               FORMAT_Y4, FORMAT_Y8,
               FORMAT_AY8,  FORMAT_A8Y8,
               FORMAT_R3G3B2, FORMAT_R5G6B5,
               FORMAT_R8G8B8, FORMAT_Y8U8V8,
               FORMAT_A1R5G5B5, FORMAT_A4R4G4B4,
               FORMAT_X8R8G8B8, FORMAT_A8R8G8B8,
               FORMAT_STENCIL,
               FORMAT_R16G16B16, FORMAT_A16R16G16B16]

FORMAT_UNPACKERS = {}

FORMAT_PACKERS = {}

COMPRESSED_FORMATS = []

DDS_FORMATS = []

THREE_CHANNEL_FORMATS = [FORMAT_R3G3B2, FORMAT_R5G6B5, FORMAT_R8G8B8,
                         FORMAT_R16G16B16, FORMAT_Y8U8V8]

SUB_BITMAP_COUNTS = {TYPE_2D:1, TYPE_3D:1, TYPE_CUBEMAP:6}

MINIMUM_W = {FORMAT_A4:1, FORMAT_A8:1,
             FORMAT_Y4:1, FORMAT_Y8:1,
             FORMAT_AY8:1,  FORMAT_A8Y8:1,
             FORMAT_R3G3B2:1, FORMAT_R5G6B5:1,
             FORMAT_R8G8B8:1 ,FORMAT_Y8U8V8:1,
             FORMAT_A1R5G5B5:1, FORMAT_A4R4G4B4:1,
             FORMAT_X8R8G8B8:1, FORMAT_A8R8G8B8:1,
             FORMAT_STENCIL:1,
             FORMAT_R16G16B16:1, FORMAT_A16R16G16B16:1}

MINIMUM_H = {FORMAT_A4:1, FORMAT_A8:1,
             FORMAT_Y4:1, FORMAT_Y8:1,
             FORMAT_AY8:1,  FORMAT_A8Y8:1,
             FORMAT_R3G3B2:1, FORMAT_R5G6B5:1,
             FORMAT_R8G8B8:1 ,FORMAT_Y8U8V8:1,
             FORMAT_A1R5G5B5:1, FORMAT_A4R4G4B4:1,
             FORMAT_X8R8G8B8:1, FORMAT_A8R8G8B8:1,
             FORMAT_STENCIL:1,
             FORMAT_R16G16B16:1, FORMAT_A16R16G16B16:1}

MINIMUM_D = {FORMAT_A4:1, FORMAT_A8:1,
             FORMAT_Y4:1, FORMAT_Y8:1,
             FORMAT_AY8:1,  FORMAT_A8Y8:1,
             FORMAT_R3G3B2:1, FORMAT_R5G6B5:1,
             FORMAT_R8G8B8:1 ,FORMAT_Y8U8V8:1,
             FORMAT_A1R5G5B5:1, FORMAT_A4R4G4B4:1,
             FORMAT_X8R8G8B8:1, FORMAT_A8R8G8B8:1,
             FORMAT_STENCIL:1,
             FORMAT_R16G16B16:1, FORMAT_A16R16G16B16:1}

#this is how many BITS(NOT BYTES) each format's pixels take up
BITS_PER_PIXEL = {FORMAT_A4:4, FORMAT_A8:8,
                  FORMAT_Y4:4, FORMAT_Y8:8,
                  FORMAT_AY8:8,  FORMAT_A8Y8:16,
                  FORMAT_R3G3B2:8, FORMAT_R5G6B5:16,
                  FORMAT_R8G8B8:24, FORMAT_Y8U8V8:24,
                  FORMAT_A1R5G5B5:16, FORMAT_A4R4G4B4:16,
                  FORMAT_X8R8G8B8:32, FORMAT_A8R8G8B8:32,
                  FORMAT_STENCIL:1, 
                  FORMAT_R16G16B16:48, FORMAT_A16R16G16B16:64}

#this is the data type that each format's pixel data array will hold
FORMAT_DATA_SIZES = {FORMAT_A4:"B", FORMAT_A8:"B",
                     FORMAT_Y4:"B", FORMAT_Y8:"B",
                     FORMAT_AY8:"B",  FORMAT_A8Y8:"H",
                     FORMAT_R3G3B2:"B", FORMAT_R5G6B5:"H",
                     FORMAT_R8G8B8:"I", FORMAT_Y8U8V8:"I",
                     FORMAT_A1R5G5B5:"H", FORMAT_A4R4G4B4:"H",
                     FORMAT_X8R8G8B8:"I", FORMAT_A8R8G8B8:"I",
                     FORMAT_STENCIL:"B", 
                     FORMAT_R16G16B16:"Q", FORMAT_A16R16G16B16:"Q"}

#this is the mask of each channel in each format
FORMAT_CHANNEL_MASKS = {FORMAT_A4:(15,), FORMAT_A8:(255,),
                        FORMAT_Y4:(15,), FORMAT_Y8:(255,),
                        FORMAT_AY8:(255,),  FORMAT_A8Y8:(65280,255),
                        FORMAT_R3G3B2:(0,192,56,7),
                        FORMAT_R5G6B5:(0,63488,2016,31),
                        FORMAT_A1R5G5B5:(32768, 31744, 992, 31),
                        FORMAT_R8G8B8:(0, 16711680, 65280, 255),
                        FORMAT_Y8U8V8:(0, 16711680, 65280, 255),
                        FORMAT_A4R4G4B4:(61440, 3840, 240, 15),
                        FORMAT_X8R8G8B8:(4278190080, 16711680, 65280, 255),
                        FORMAT_A8R8G8B8:(4278190080, 16711680, 65280, 255),
                        FORMAT_STENCIL:(1,),
                        FORMAT_R16G16B16:(0, 2**48-2**32, 4294901760, 65535),
                        FORMAT_A16R16G16B16:(2**64-2**48, 2**48-2**32, 4294901760, 65535)}


#this is how many bits the depth of each channel is for each raw format
FORMAT_CHANNEL_DEPTHS = {FORMAT_A4:(4,), FORMAT_A8:(8,),
                         FORMAT_Y4:(4,), FORMAT_Y8:(8,),
                         FORMAT_AY8:(8,), FORMAT_A8Y8:(8,8),
                         FORMAT_R3G3B2:(0,2,3,3), FORMAT_R5G6B5:(0,5,6,5),
                         FORMAT_R8G8B8:(0,8,8,8), FORMAT_Y8U8V8:(0,8,8,8),
                         FORMAT_A1R5G5B5:(1,5,5,5), FORMAT_A4R4G4B4:(4,4,4,4),
                         FORMAT_X8R8G8B8:(8,8,8,8), FORMAT_A8R8G8B8:(8,8,8,8),
                         FORMAT_STENCIL:(1,),
                         FORMAT_R16G16B16:(0,16,16,16),
                         FORMAT_A16R16G16B16:(16,16,16,16)}

#the number of channels possible in each format, regardless of whether or not they are raw formats
FORMAT_CHANNEL_COUNTS = {FORMAT_A4:1, FORMAT_A8:1,
                         FORMAT_Y4:1, FORMAT_Y8:1,
                         FORMAT_AY8:1,  FORMAT_A8Y8:2,
                         FORMAT_R3G3B2:4, FORMAT_R5G6B5:4,
                         FORMAT_R8G8B8:4, FORMAT_Y8U8V8:4,
                         FORMAT_A1R5G5B5:4, FORMAT_A4R4G4B4:4,
                         FORMAT_X8R8G8B8:4, FORMAT_A8R8G8B8:4,
                         FORMAT_STENCIL:1,
                         FORMAT_R16G16B16:4, FORMAT_A16R16G16B16:4}

#this is how far right the channel is shifted when unpacked and left when repacked
FORMAT_CHANNEL_OFFSETS = {FORMAT_A4:(0,), FORMAT_A8:(0,),
                          FORMAT_Y4:(0,), FORMAT_Y8:(0,),
                          FORMAT_AY8:(0,), FORMAT_A8Y8:(8,0),
                          FORMAT_R3G3B2:(0,6,3,0), FORMAT_R5G6B5:(0,11,5,0),
                          FORMAT_R8G8B8:(0,16,8,0), FORMAT_Y8U8V8:(0,16,8,0),
                          FORMAT_A1R5G5B5:(15,10,5,0), FORMAT_A4R4G4B4:(12,8,4,0),
                          FORMAT_X8R8G8B8:(24,16,8,0), FORMAT_A8R8G8B8:(24,16,8,0),
                          FORMAT_STENCIL:(0,),
                          FORMAT_R16G16B16:(0,32,16,0), FORMAT_A16R16G16B16:(48,32,16,0)}

#if a channel has this in it's divisor it will be erased when the bitmap is repacked
CHANNEL_ERASE_DIVISOR = 2**63-1

#this is the default amount of bits per pixel for palettized bitmaps
DEFAULT_INDEXING_SIZE = 8

DEFAULT_UNPACK_FORMAT = FORMAT_A8R8G8B8

ALL_FORMAT_COLLECTIONS = {"VALID_FORMAT":VALID_FORMATS, "BITS_PER_PIXEL":BITS_PER_PIXEL,
                          "RAW_FORMAT":RAW_FORMATS, "THREE_CHANNEL_FORMAT":THREE_CHANNEL_FORMATS,
                          "COMPRESSED_FORMAT":COMPRESSED_FORMATS, "DDS_FORMAT":DDS_FORMATS,
                          "MINIMUM_W":MINIMUM_W, "MINIMUM_H":MINIMUM_H, "MINIMUM_D":MINIMUM_D,
                          "DATA_SIZE":FORMAT_DATA_SIZES, "UNPACKER":FORMAT_UNPACKERS,
                          "CHANNEL_COUNT":FORMAT_CHANNEL_COUNTS, "PACKER":FORMAT_PACKERS,
                          "CHANNEL_OFFSETS":FORMAT_CHANNEL_OFFSETS,
                          "CHANNEL_MASKS":FORMAT_CHANNEL_MASKS,
                          "CHANNEL_DEPTHS":FORMAT_CHANNEL_DEPTHS}


"""##################"""
### CHANNEL MAPPINGS ###
"""##################"""

#the way channel mappings work is that each index is one channel. in their standard
#form the value of each index should be the number of that index. Ex:(0, 1, 2, 3)

#to remove channels you should create a mapping with exactly how many channels you want
#to have and have the value of each index be the channel that you want to place there.
#Ex: (A, R, G, B) to (G, B) would use the mapping (2, 3)

#to switch channels around you would create a mapping with one index for each channel in
#the target format. the value of each index will be the index of the channel you want from
#the source format. Ex: (A, R, G, B) to (B, G, R, A) would use the mapping (3, 2, 1, 0)

#if you want a blank channel to be made then set the value at that index to -1
#Ex: converting A8 to A8R8G8B8 = (0, -1, -1, -1)


"""these channel mappings are used to swap ALPHA AND
INTENSITY, but ONLY if the source bitmap is A8Y8"""
#              ( A, Y )
A8Y8_TO_Y8A8 = ( 1, 0 )
AY8_TO_A8Y8 =  ( 0, 0 )
A8_TO_A8Y8 =   ( 0,-1 )
Y8_TO_A8Y8 =   (-1, 0 )

"""these channel mappings are used to convert different formats to Y8 and A8. these are also
used for converting to AY8. just use the one that preserves the channel you want to keep"""
#                (A)
ANYTHING_TO_A8 = (0,)
#            (Y)
A8Y8_TO_Y8 = (1,)
#             (AY)
MONO_TO_AY8 = (0,)

"""these channel mappings are to convert A8, Y8, AY8, and A8Y8 to A8R8G8B8 and X8R8G8B8"""
#              ( A,  R,  G,  B)
A8_TO_ARGB =   ( 0, -1, -1, -1)
Y8_TO_ARGB =   (-1,  0,  0,  0)
AY8_TO_ARGB =  ( 0,  0,  0,  0)

A8Y8_TO_ARGB = ( 0,  1,  1,  1)
Y8A8_TO_ARGB = ( 1,  0,  0,  0)


"""########################"""
### CHANNEL MERGE MAPPINGS ###
"""########################"""

#why merge mappings are used is that if the target format has less channels
#than the source then we either need to remove channels or merge them together.
#we can remove them with the above channel mappings, but for things like
#RGB to monochrome we need to merge the pixels together to get the average intensity.

#merge mapping are the length of the source's channel count. each index is which
#channel in the target format to merge the channel from the source into.
#Ex: merging ARGB's 4 channel into A8Y8 would be (0, 1, 1, 1)

#                ( A,  R,  G,  B )
M_ARGB_TO_A8Y8 = ( 0,  1,  1,  1 )
M_ARGB_TO_Y8A8 = ( 1,  0,  0,  0 )
M_ARGB_TO_Y8 =   ( -1, 0,  0,  0 )
M_ARGB_TO_A8 =   ( 0, -1, -1, -1 )


def define_format(**kwargs):
    """THIS FUNCTION CAN BE CALLED TO DEFINE A NEW FORMAT TYPE"""
    try:
        if "format_id" in kwargs:
            format_id = kwargs["format_id"]
        else:
            print("ERROR: NO IDENTIFIER SUPPLIED FOR FORMAT.\n",
                  "THIS MUST BE A HASHABLE TYPE SUCH AS AN INTEGER OR STRING.")
            return

        
        if "remove_format" in kwargs and kwargs["remove_format"]:
            remove_bitmap_format(format_id)
        else:
            if "format_id" in kwargs and kwargs["format_id"] in VALID_FORMATS:
                print("ERROR: CANNOT ADD NEW FORMAT TO BITMAP CONVERTOR.\n",
                      "THE IDENTIFIER PROVIDED IS ALREADY IN USE.")
                return()

            VALID_FORMATS.append(format_id)

            if "raw_format" in kwargs and kwargs["raw_format"]:
                RAW_FORMATS.append(format_id)
            if "compressed" in kwargs and kwargs["compressed"]:
                COMPRESSED_FORMATS.append(format_id)
            if "dds_format" in kwargs and kwargs["dds_format"]:
                DDS_FORMATS.append(format_id)
            if "three_channels" in kwargs and kwargs["three_channels"]:
                THREE_CHANNEL_FORMATS.append(format_id)


            if "unpacker" in kwargs and kwargs["unpacker"]:
                FORMAT_UNPACKERS[format_id] = kwargs["unpacker"]
            if "packer" in kwargs and kwargs["packer"]:
                FORMAT_PACKERS[format_id] = kwargs["packer"]

                
            if "min_width" in kwargs and kwargs["min_width"]:
                MINIMUM_W[format_id] = kwargs["min_width"]
            else: MINIMUM_W[format_id] = 1
            
            if "min_height" in kwargs and kwargs["min_height"]:
                MINIMUM_H[format_id] = kwargs["min_height"]
            else: MINIMUM_H[format_id] = 1
            
            if "min_depth" in kwargs and kwargs["min_depth"]:
                MINIMUM_D[format_id] = kwargs["min_depth"]
            else: MINIMUM_D[format_id] = 1
            
            if "bpp" in kwargs and kwargs["bpp"]:
                BITS_PER_PIXEL[format_id] = kwargs["bpp"]
            else:
                if "channel_depths" in kwargs:
                    BITS_PER_PIXEL[format_id] = sum(kwargs["channel_depths"])
                else:
                    print("ERROR: CANNOT DEFINE BITMAP FORMAT "+
                          "WITHOUT A KNOWN\nBITS PER PIXEL OR A "+
                          "DESCRIPTION OF EACH CHANNEL'S DEPTHS")
                    remove_bitmap_format(format_id)
            
            if "data_size" in kwargs and kwargs["data_size"]:
                FORMAT_DATA_SIZES[format_id] = kwargs["data_size"]
            else:
                FORMAT_DATA_SIZES[format_id] = INVERSE_PIXEL_ENCODING_SIZES[BITS_PER_PIXEL[format_id]//8]
            
            if "channel_count" in kwargs and kwargs["channel_count"]:
                FORMAT_CHANNEL_COUNTS[format_id] = kwargs["channel_count"]
            else:
                FORMAT_CHANNEL_COUNTS[format_id] = 1
            
            if "channel_masks" in kwargs and kwargs["channel_masks"]:
                FORMAT_CHANNEL_MASKS[format_id] = kwargs["channel_masks"]
            if "channel_depths" in kwargs and kwargs["channel_depths"]:
                FORMAT_CHANNEL_DEPTHS[format_id] = kwargs["channel_depths"]
            if "channel_offsets" in kwargs and kwargs["channel_offsets"]:
                FORMAT_CHANNEL_OFFSETS[format_id] = kwargs["channel_offsets"]

    except:
        print("ERROR OCCURED WHILE TRYING TO DEFINE NEW FORMAT IN BITMAP CONVERTOR")
        print(format_exc())


def print_format(format_id):
    print(format_id, "Format Definition:")
    for key in sorted(ALL_FORMAT_COLLECTIONS.keys()):
        if isinstance(ALL_FORMAT_COLLECTIONS[key], dict):
            if format_id in ALL_FORMAT_COLLECTIONS[key]:
                print('    '+str(key)+':', ALL_FORMAT_COLLECTIONS[key][format_id])
            else:
                print('    '+str(key)+':')
        else:
            print('    '+str(key)+':', format_id in ALL_FORMAT_COLLECTIONS[key])
    print()


def remove_bitmap_format(format_id):
    for key in ALL_FORMAT_COLLECTIONS:
        if format_id in ALL_FORMAT_COLLECTIONS[key]:
            if isinstance(ALL_FORMAT_COLLECTIONS[key], dict):
                del(ALL_FORMAT_COLLECTIONS[key][format_id])
            else:
                ALL_FORMAT_COLLECTIONS[key].pop(ALL_FORMAT_COLLECTIONS[key].index(format_id))


def array_length_to_pixel_count(array_len, pixel_size, format):
    '''used to figure out the number of pixels in an array
    of a certain length, with each pixel of a certain
    integer size per pixel, and a certain texture format'''
    return(array_len*8*pixel_size)//BITS_PER_PIXEL[format]
           
def pixel_count_to_array_length(pixel_count, pixel_size, format):
    '''used to figure out the length of an array that will
    hold a certain number of pixels which will take up a
    certain number of bytes each and are of a certain format'''
    return((pixel_count*BITS_PER_PIXEL[format]) // 8 ) // pixel_size




def get_mipmap_dimensions(width, height, depth, mipmap_level, format):
    '''This function will give the dimensions of the
    specified mipmap level, format, and fullsize dimensions'''
    #since the dimensions change per mipmap we need to calculate them
    return(dimension_lower_bound_check(width//powers_of_2[mipmap_level],
                                       height//powers_of_2[mipmap_level],
                                       depth//powers_of_2[mipmap_level],
                                       format))

def dimension_lower_bound_check(width, height, depth=1, format=FORMAT_A8R8G8B8):
    '''clips the supplied width, height, and depth to
    what the minimum is defined for the format'''
    return(max(width,  MINIMUM_W[format]),
           max(height, MINIMUM_H[format]),
           max(depth,  MINIMUM_D[format]))
