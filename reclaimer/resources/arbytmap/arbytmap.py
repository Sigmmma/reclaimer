
import time
import sys

from traceback import format_exc
from array import array
from math import ceil, log
from os import path
from copy import deepcopy
from decimal import Decimal

from .ext.format_defs import *
from .ext import swizzler, bitmap_io, dds_defs

bitmap_io.ab = dds_defs.ab = sys.modules[__name__]
dds_defs.initialize()

try:
    from .ext import raw_packer_ext
    fast_raw_packer = True
except:
    fast_raw_packer = False

try:
    from .ext import raw_unpacker_ext
    fast_raw_unpacker = True
except:
    fast_raw_unpacker = False

try:
    from .ext import arbytmap_ext
    fast_arbytmap = True
except:
    fast_arbytmap = False

try:
    from .ext import bitmap_io_ext
    fast_bitmap_io = True
except:
    fast_bitmap_io = False


#speed things up by caching these so we don't have to
#calculate them on the fly or constantly remake them
range_16 = range(16)


'''when constructing this class you must provide the
nested list containing the textures and a dictionary which
contains the texture's height, width, type, and format.

    Optional parameters include the depth, mipmap count,
sub-texture count(cubemaps are composed of 6 2D subtextures
for example), the format to convert the pixels to, whether to
or how to swap channels around, which channels should be
merged/removed/cloned when converting to a format with a different
number of channels, 0-255 cutoff when compressing a channel to
1-bit, the number of times to cut the resolution in half, and
the power to use for merging pixels with gamma correction.'''
class Arbytmap():
    
    def __init__(self, **kwargs):
        self.default_palette_picker = self._palette_picker
        self.set_deep_color_mode()

        self.texture_block = self.texture_info = None

        '''set this to true to force routines to make
           exported data compatible with Photoshop.'''
        self.photoshop_compatability = True
        
        #initialize the bitmap description variables
        self.sub_bitmap_count = self.mipmap_count = 0
        self.swizzled = self.packed = self.palette_packed = False
        self.filepath = None
        self.indexing_size = 0
        self.width = self.height = self.depth = 0
        self.format = self.texture_type = ""
        self.channel_order = C_ORDER_DEFAULT

        #palette stuff
        self.palette = None
        self.palettized_unpacker = None
        self.palettized_packer = None
        self.palette_unpacker = None
        self.palette_packer = None
        self.indexing_unpacker = None
        self.indexing_packer = None
        
        #initialize the conversion variables
        self.target_format = ""
        self.one_bit_bias = 127
        self.downres_amount = 0
        self.generate_mipmaps = self.swizzler_mode = False
        self.gamma = [1.0]*4  # this is only meant to handle up to 4 channels
        self.color_key_transparency = False
        self.reswizzler = self.deswizzler = None
        self.palette_picker = self.default_palette_picker
        self.palettize = False
        self.channel_mapping = self.channel_merge_mapping = None
        self.repack = True
        self.target_indexing_size = DEFAULT_INDEXING_SIZE
        

        #initialize the variables created in the below functions
        self.source_depths = None
        self.unpacked_depths = None
        self.target_depths = None

        self.source_channel_count = 0
        self.unpacked_channel_count = 0
        self.target_channel_count = 0
        
        self.swapping_channels = False
        self.channel_masks = None
        self.channel_offsets = None
        self.channel_depths = None
        self.channel_merge_divisors = None
        self.channel_upscalers = None
        self.channel_downscalers = None
        
        #if a texture block is provided in the kwargs
        #then we load the texture as we build the class
        if "texture_block" in kwargs:
            #create/set this class's variables to those in the texture block
            self.load_new_texture(**kwargs)

    def set_deep_color_mode(self, deep_state=None):
        """Allows changing the unpacking mode of this module
        from "true color"(32BPP) to "deep color"(64BPP).
        If the argument is None, the mode will be the default
        one set in Format_Defs, if False the unpack format will
        be Format_A8R8G8B8, and if True the format will be
        FORMAT_A16R16G16B16."""
        if deep_state is None:
            self._UNPACK_FORMAT = DEFAULT_UNPACK_FORMAT
            self._UNPACK_ARRAY_CODE = INVERSE_PIXEL_ENCODING_SIZES[
                max(FORMAT_CHANNEL_DEPTHS[self._UNPACK_FORMAT])//8]
        elif deep_state:
            self._UNPACK_FORMAT = FORMAT_A16R16G16B16
            self._UNPACK_ARRAY_CODE = "H"
        else:
            self._UNPACK_FORMAT = FORMAT_A8R8G8B8
            self._UNPACK_ARRAY_CODE = "B"


    #call this when providing the convertor with a new list of pixel arrays
    def load_new_texture(self, **kwargs):
        
        try:
            texture_block = self.texture_block = kwargs.get("texture_block")
            texture_info = self.texture_info = kwargs.get("texture_info")
            
            if texture_block is None:
                raise TypeError(
                    "ERROR: NO BITMAP BLOCK SUPPLIED.\n",
                    "CANNOT LOAD BITMAP WITHOUT A SUPPLIED BITMAP BLOCK")
            
            if texture_info is None:
                raise TypeError(
                    "ERROR: BITMAP BLOCK SUPPLIED HAS NO TEXTURE INFO.\n",
                      "CANNOT LOAD BITMAP WITHOUT A DESCRIPTION OF THE BITMAP")
            
            if "format" not in texture_info:
                self.texture_block = None
                raise TypeError(
                    "ERROR: THE SUPPLIED BITMAP'S INFO BLOCK HAS NO " +
                    "FORMAT ENTRY!\nCAN NOT LOAD BITMAP WITHOUT " +
                    "KNOWING THE BITMAP'S FORMAT.")
            
            if texture_info["format"] not in VALID_FORMATS:
                self.texture_block = None
                raise TypeError(
                    "ERROR: THE SUPPLIED BITMAP IS IN AN UNKNOWN FORMAT!\n",
                    "IF YOU WISH TO USE THIS FORMAT YOU MUST " +
                    "INCOROPRATE IT YOURSELF.")

            #if provided with just a pixel data array
            #we will need to put it inside a list
            if isinstance(texture_block, array):
                texture_block = [texture_block]
            
            #initialize the optional bitmap description variables
            self.palette = None
            self.indexing_size = DEFAULT_INDEXING_SIZE
            
            
            #get the bitmap's info from the texture block's info dictionary
            self.width = texture_info.get("width", 1)
            self.height = texture_info.get("height", 1)
            self.depth = texture_info.get("depth", 1)
            self.format = texture_info["format"]
            
            self.swizzled = texture_info.get("swizzled", False)
            self.mipmap_count = texture_info.get("mipmap_count", 0)
            self.sub_bitmap_count = texture_info.get("sub_bitmap_count", 1)
            self.filepath = texture_info.get("filepath", None)
            
            self.packed = texture_info.get("packed", True)
            self.palette_packed = texture_info.get("palette_packed", True)

            if "deswizzler" not in texture_info:
                self.deswizzler = swizzler.Swizzler(
                    texture_converter=self, mask_type="DEFAULT")
            elif swizzler is not None:
                self.deswizzler = swizzler.Swizzler(
                    texture_converter=self,
                    mask_type=texture_info["deswizzler"])
            else:
                print("ERROR: SWIZZLER MODULE NOT LOADED. "+
                      "CANNOT SWIZZLE/UNSWIZZLE WITHOUT SWIZZLER.")

            self.texture_type = texture_info.get("texture_type", TYPE_2D)
            self.channel_order = texture_info.get(
                "channel_order", C_ORDER_DEFAULT)
                
                
            if texture_info.get("palette") is None:
                pass
            elif texture_info.get("indexing_size") not in (0, None):
                self.palette = texture_info["palette"]
                self.indexing_size = texture_info["indexing_size"]
                self.palettize = True
                
                if "palette_packed" in texture_info:
                    self.palette_packed = texture_info["palette_packed"]
            else:
                print("ERROR: PALETTE WAS SUPPLIED, " +
                      "BUT BIT-SIZE OF INDEXING WAS NOT.")
                return

            self.palettized_packer = texture_info.get(
                "palettized_packer", self._pack_palettized)
            self.palettized_unpacker = texture_info.get(
                "palettized_unpacker", self._unpack_palettized)
            self.palette_packer = texture_info.get(
                "palette_packer", self._pack_palette)
            self.palette_unpacker = texture_info.get(
                "palette_unpacker", self._unpack_palette)
            self.indexing_packer = texture_info.get(
                "indexing_packer", self._pack_indexing)
            self.indexing_unpacker = texture_info.get(
                "indexing_unpacker", self._unpack_indexing)

            #we may have been provided with conversion
            #settings at the same time we were given the texture
            self.load_new_conversion_settings(**kwargs)
                
            self.texture_block = texture_block
            self.texture_info = texture_info
        except:
            print("ERROR OCCURED WHILE TRYING TO LOAD " +
                  "TEXTURE INTO BITMAP CONVERTOR")
            print(format_exc())


    def load_new_conversion_settings(self, **kwargs):
        #only run if there is a valid texture block loaded
        if (self.texture_info is None and
            ("texture_info" not in kwargs or kwargs["texture_info"] is None)):
            print("ERROR: CANNOT LOAD CONVERSION SETTINGS "+
                  "WITHOUT A LOADED TEXTURE.")
            return

        """RESETTING THE CONVERSION VARIABLES EACH TIME IS INTENTIONAL
        TO PREVENT ACCIDENTALLY LEAVING INCOMPATIBLE ONES SET"""
        try:
            #initialize the bitmap CONVERSION variables
            self.target_format = self.format
            self.one_bit_bias = 127
            self.downres_amount = 0
            self.generate_mipmaps = False
            self.swizzler_mode = self.swizzled
            self.gamma = 1.0
            self.color_key_transparency = False
            self.reswizzler = self.deswizzler
            self.palette_picker = self.default_palette_picker
            self.palettize = self.is_palettized()
            self.target_indexing_size = self.indexing_size
            self.channel_mapping = None
            self.channel_merge_mapping = None
            self.repack = True
            
            if kwargs.get("target_format") in VALID_FORMATS:
                self.target_format = kwargs["target_format"]
            
            if self.target_format in DDS_FORMATS and swizzler is None:
                print("ERROR: SWIZZLER MODULE NOT LOADED. CANNOT COMPRESS " +
                      "TO DXT WITHOUT SWIZZLER. SWITCHING TO A8R8G8B8.")
                self.target_format = self._UNPACK_FORMAT
                
            self.one_bit_bias = kwargs.get("one_bit_bias", self.one_bit_bias)

            # The number of times to cut the resolution in half
            self.downres_amount = abs(kwargs.get(
                "downres_amount", self.downres_amount))

            # The number of mipmaps to make
            self.generate_mipmaps = kwargs.get(
                "generate_mipmaps", self.generate_mipmaps)
                
            # Whether to swizzle or deswizzle when the swizzler is run
            # False == Deswizzle    True == Swizzle
            self.swizzler_mode = kwargs.get("swizzler_mode", self.swizzler_mode)

            self.gamma = kwargs.get("gamma", self.gamma)
            self.repack = kwargs.get("repack", self.repack)
            self.color_key_transparency = kwargs.get(
                "color_key_transparency", self.color_key_transparency)

            if "reswizzler" not in kwargs:
                pass
            elif swizzler is not None:
                self.reswizzler = swizzler.Swizzler(
                    texture_converter = self, mask_type=kwargs["reswizzler"])
            else:
                print("ERROR: SWIZZLER MODULE NOT LOADED. " +
                      "CANNOT SWIZZLE/UNSWIZZLE WITHOUT SWIZZLER.")

            self.palettize = kwargs.get("palettize", self.palettize)
            self.palette_picker = kwargs.get(
                "palette_picker", self.palette_picker)
            self.target_indexing_size = kwargs.get(
                "target_indexing_size", self.target_indexing_size)
            
            #set up all the channel mappings and such
            self._set_all_channel_mappings(**kwargs)

        except:
            print("ERROR OCCURED WHILE TRYING TO LOAD CONVERSION SETTINGS " +
                  "INTO BITMAP CONVERTOR.\nDEREFERENCING TEXTURE BLOCK FROM " +
                  "BITMAP CONVERTER TO PREVENT UNSTABLE CONVERSION.")
            print(format_exc())
            self.texture_block = None


    def print_info(self, tex_info=True, conv_settings=False,
                   channel_maps=False, methods=False, scalers=False):
        if tex_info:
            print("Texture info:")
            print("   filepath:", self.filepath)
            print("   type:", self.texture_type)
            print("   format:", self.format)
            print("   width:", self.width)
            print("   height:", self.height)
            print("   depth:", self.depth)
            print()
            print("   sub_bitmap_count:", self.sub_bitmap_count)
            print("   mipmap_count:", self.mipmap_count)
            print("   swizzled:", self.swizzled)
            print()
            print("   currently_packed:", self.packed)
            print("   is_palettized:", self.is_palettized())
            if self.is_palettized():
                print()
                print("   palette_currently_packed:", self.palette_packed)
                print("   indexing_size:", self.indexing_size)
            print()
            
        if conv_settings:
            print("Conversion settings:")
            print("   photoshop_compatability:", self.photoshop_compatability)
            print("   target_format:", self.target_format)
            print("   target_indexing_size:", self.target_indexing_size)
            print()
            print("   one_bit_bias:", self.one_bit_bias)
            print("   gamma:", self.gamma)
            print("   swizzler_mode:", self.swizzler_mode)
            print("   downres_amount:", self.downres_amount)
            print("   generate_mipmaps:", self.generate_mipmaps)
            print()
            print("   color_key_transparency:", self.color_key_transparency)
            print("   make\\keep_palettized:", self.palettize)
            print("   repack:", self.repack)
            print("   channel_mapping:", self.channel_mapping)
            print("   channel_merge_mapping:", self.channel_merge_mapping)
            print()
            print("   unpack_format:", self._UNPACK_FORMAT)
            print("   unpack_array_code:", self._UNPACK_ARRAY_CODE)
            print("   channel_order:", self.channel_order)
            print()
            
        if channel_maps:
            print("Channel mapping variables:")
            print("   source_depths:", self.source_depths)
            print("   unpacked_depths:", self.unpacked_depths)
            print("   target_depths:", self.target_depths)
            print()
            print("   source_channel_count:", self.source_channel_count)
            print("   unpacked_channel_count:", self.unpacked_channel_count)
            print("   target_channel_count:", self.target_channel_count)
            print()
            print("   swapping_channels:", self.swapping_channels)
            print()
            print("   channel_mapping:", self.channel_mapping)
            print("   channel_merge_mapping:", self.channel_merge_mapping)
            print()
            print("   channel_offsets:", self.channel_offsets)
            print("   channel_depths:", self.channel_depths)
            print("   channel_merge_divisors:", self.channel_merge_divisors)
            print()

        if methods:
            print("Bound methods:")
            print("   palettized_unpacker:", self.palettized_unpacker)
            print("   palettized_packer:", self.palettized_packer)
            print()
            print("   palette_unpacker:", self.palette_unpacker)
            print("   palette_packer:", self.palette_packer)
            print()
            print("   indexing_unpacker:", self.indexing_unpacker)
            print("   indexing_packer:", self.indexing_packer)
            print()
            print("   reswizzler:", self.reswizzler)
            print("   deswizzler:", self.deswizzler)
            print("   palette_picker:", self.palette_picker)
            print("   default_palette_picker:", self.default_palette_picker)

        if scalers:
            print("Scaler arrays:")
            print("   channel_upscalers:", self.channel_upscalers)
            print("   channel_downscalers:", self.channel_downscalers)
            print("   gamma_scaler:", self.gamma_scaler)
            print()

    def _set_all_channel_mappings(self, **kwargs):
        """Sets(or defaults) all the different channel mappings"""
        try:
            self.source_channel_count = FORMAT_CHANNEL_COUNTS[self.format]
            self.unpacked_channel_count = FORMAT_CHANNEL_COUNTS[self.format]
            self.target_channel_count = FORMAT_CHANNEL_COUNTS[
                self.target_format]

            #CREATE THE CHANNEL LOAD MAPPING
            self._set_channel_load_mapping(**kwargs)
            
            #If the format is DXT then the merge mapping
            #will have JUST BEEN padded and set
            if self.channel_merge_mapping is not None:
                kwargs["channel_merge_mapping"] = self.channel_merge_mapping

            #CREATE THE CHANNEL MERGE MAPPING
            self._set_channel_merge_mapping(**kwargs)

            #CREATE THE CHANNEL UP AND DOWN SCALER LISTS
            self._set_upscalers_and_downscalers(**kwargs)
            
            #CREATE THE CHANNEL GAMMA SCALER LISTS
            self._set_gamma_scaler(**kwargs)
        except:
            print("Error occurred while trying to create " +
                  "channel mappings and scalars.")
            print(format_exc())
        
    def is_palettized(self, palette_index=0):
        '''returns whether or not there is a valid palette
        for the bitmap at the index provided'''
        return( self.palette is not None and
                ((hasattr(self.palette, '__iter__') and
                  len(self.palette) > palette_index)
                 and self.palette[palette_index] is not None) )

    
    def _set_gamma_scaler(self, **kwargs):
        '''creates the list per channel for the gamma scaling'''
        if isinstance(self.gamma,(int,float)):
            self.gamma = [self.gamma]*self.unpacked_channel_count
        elif len(self.gamma) < self.unpacked_channel_count:
            #if there aren't enough indexes in the gamma scalar we repeat
            #the last element in the scalar list for each missign channel
            old_gamma_len = len(self.gamma)
            for i in range(self.unpacked_channel_count-old_gamma_len):
                self.gamma.append(self.gamma[old_gamma_len-1])
        
        self.gamma_scaler = [0]*self.unpacked_channel_count
        #this array will be used to quickly convert a color
        #channel value from a linear value to a gamma scaled value
        for channel in range(self.unpacked_channel_count):
            self.gamma_scaler[channel] = array(
                "f",[0.0]*self.unpacked_channel_count)
            for val in range(256):
                self.gamma_scaler[channel].append(
                    ((float(val)/255)**self.gamma[channel])*255)


    def _set_upscalers_and_downscalers(self, **kwargs):
        '''NEED TO ADD A DESCRIPTION'''
        
        #specifies what depth we want to unpack each channel from
        self.source_depths = FORMAT_CHANNEL_DEPTHS[self.format][:]
        #specifies what depth we want to unpack each channel to
        self.unpacked_depths = FORMAT_CHANNEL_DEPTHS[
            self._UNPACK_FORMAT][:self.unpacked_channel_count]
        #specifies what depth we want to repack each channel to
        self.target_depths = FORMAT_CHANNEL_DEPTHS[self.target_format][:]
        
        #each index is a list to upscale the source depth to the unpacked depth
        self.channel_upscalers = []
        self.channel_downscalers = []

        if self.channel_merge_mapping is not None:
            self.target_depths = []
            for i in range(len(self.unpacked_depths)):
                self.target_depths.append(
                    FORMAT_CHANNEL_DEPTHS[self.target_format]
                    [self.channel_merge_mapping[i]])

        
        """BUILD THE UPSCALER ARRAYS"""
        #figure out how large the entries in the arrays need to be
        #In order for the fast unpackers to work well with these,
        #we make sure all the upscale arrays use the same encoding.
        array_enc = INVERSE_PIXEL_ENCODING_SIZES[
            int(max(self.unpacked_depths)/8.0)]
        for i in range(len(self.unpacked_depths)):
            #make a new array to map the source values to their upscaled values
            self.channel_upscalers.append(array(array_enc, []))

            #this is the amount the values will be scaled to and from
            if self.source_depths[self.channel_mapping[i]] == 0:
                scale = 0.0000000001
            else:
                scale = ((2**self.unpacked_depths[i]-1) /
                         (2**self.source_depths[self.channel_mapping[i]]-1))
            
            for val in range(2**self.source_depths[self.channel_mapping[i]]):
                self.channel_upscalers[i].append(int(round( val * scale )))


        """BUILD THE DOWNSCALER ARRAYS"""
        #figure out how large the entries in the arrays need to be
        #In order for the fast packers to work well with these, we
        #make sure all the downscale arrays use the same encoding.
        array_enc = INVERSE_PIXEL_ENCODING_SIZES[
            int(max(self.target_depths)/8.0)]
        for i in range(len(self.target_depths)):
            #make a new array to map the target
            #values to their downscaled values
            self.channel_downscalers.append(array(array_enc, []))
            
            if self.target_depths[i] == 1:
                #if the source depth is 1 bit we use a
                #bias to determine what is white and black
                for val in range(2**self.unpacked_depths[i]):
                    self.channel_downscalers[i].append(
                        int(val >= self.one_bit_bias))
            else:
                #this is the amount the values will be scaled to and from
                if self.unpacked_depths[i] == 0:
                    scale = 0.0000000001
                else:
                    scale = ((2**self.target_depths[i]-1) /
                             (2**self.unpacked_depths[i]-1))
                
                for val in range(2**self.unpacked_depths[i]):
                    self.channel_downscalers[i].append(
                        int(round( val * scale )))


    def _set_channel_load_mapping(self, **kwargs):
        """THIS FUNCTION CREATES MAPPINGS THAT ALLOW US TO
        SWAP CHANNELS AROUND PER PIXEL AS THEY ARE UNPACKED"""
        
        if "channel_mapping" in kwargs:
            self.channel_mapping = array("b", kwargs["channel_mapping"])
            self.swapping_channels = True
        else:
            self.channel_mapping = array("b", range(self.source_channel_count))
            self.swapping_channels = False
        
        """ONLY RUN IF WE CAN FIND THE FORMAT
        WE ARE LOADING IN THE CHANNEL MASKS"""
        #it is possible to have a valid format that doesn't
        #have channel masks. if the format is compressed
        #or palettized it wont work with this method
        if self.format not in FORMAT_CHANNEL_MASKS:
            return

        #create the default offset, mask, and depth arrays
        self.channel_masks = array("Q", FORMAT_CHANNEL_MASKS[self.format])
        self.channel_offsets = array("B", FORMAT_CHANNEL_OFFSETS[self.format])
        self.channel_depths = array("B", FORMAT_CHANNEL_DEPTHS[self.format])

        if "channel_mapping" in kwargs:
            #set the number of channels to how many are in the channel mapping
            self.unpacked_channel_count = len(kwargs["channel_mapping"])
            self.channel_masks = array("L", [])
            self.channel_offsets = array("B", [])
            self.channel_depths = array("B", [])

        """THE BELOW CODE WILL SWAP AROUND THE OFFSETS, MASKS, AND
        CHANNEL DEPTHS PER CHANNEL. THIS WILL ALLOW US TO SWITCH
        CHANNELS WITH EACH OTHER BY CHANGING THE ORDER WE UNPACK THEM."""
        for i in range(len(kwargs.get("channel_mapping", ()))):
            channel = self.channel_mapping[i]
            
            if channel < 0 or channel >= self.source_channel_count:
                """if the channel index provided is outside the number
                of channels we have, it means to make a blank channel.
                this will be used for things like A8 to self._UNPACK_FORMAT"""
                self.channel_masks.append(0)
                self.channel_offsets.append(0)
                
                #we preserve the alpha channel depth
                #so we can set it to full white
                if i == 0:
                    self.channel_depths.append(
                        FORMAT_CHANNEL_DEPTHS[self.format][0])
                else:
                    self.channel_depths.append(0)
            else:
                """otherwise build the channel masks/offsets/depths from
                the approporate template arrays for the channel specified"""
                self.channel_masks.append(
                    FORMAT_CHANNEL_MASKS[self.format][channel])
                self.channel_offsets.append(
                    FORMAT_CHANNEL_OFFSETS[self.format][channel])
                self.channel_depths.append(
                    FORMAT_CHANNEL_DEPTHS[self.format][channel])


        '''if this is a DDS format we need to unpack it to 4
        channels no matter what. in order for that to work we
        need to pad the channel mapping and the merge mapping'''
        if self.format in DDS_FORMATS and self.unpacked_channel_count < 4:
            # pad the channel mapping
            for i in range(self.unpacked_channel_count, 4):
                self.channel_mapping.append(i)
                
            # check if there is a merge mapping
            if "channel_merge_mapping" in kwargs:
                # pad the merge mapping
                self.channel_merge_mapping = array(
                    "b", kwargs["channel_merge_mapping"])
                
                for i in range(self.unpacked_channel_count, 4):
                    self.channel_merge_mapping.append(-1)
            else:
                # create a merge mapping if none exists
                self.channel_merge_mapping = array("b", [0,1,2,3])
                for i in range(4):
                    if (self.channel_mapping[i] == -1 or
                        self.channel_mapping[i] >= self.target_channel_count):
                        self.channel_merge_mapping[i] = -1

            self.unpacked_channel_count = 4


    def _set_channel_merge_mapping(self, **kwargs):
        """THIS FUNCTION ALLOWS US TO SPECIFY HOW CHANNELS
        ARE MERGED WHEN CONVERTING TO A DIFFERENT FORMAT"""
        
        """
        channel_merge_mapping:
        THE LENGTH WILL BE THE NUMBER OF CHANNELS IN THE ORIGINAL FORMAT. EACH
        INDEX WILL BE THE CHANNEL OF THE TARGET FORMAT TO ADD THE CHANNEL INTO.

        channel_merge_divisors:
        THE LENGTH WILL BE THE NUMBER OF CHANNELS IN THE TARGET FORMAT.
        EACH INDEX WILL STORE AN INTEGER. THIS INTEGER WILL BE THE NUMBER
        OF CHANNELS THAT HAVE BEEN ADDED TOGETHER FROM THE ORIGINAL FORMAT
        INTO THIS CHANNEL. THE PURPOSE OF THIS ARRAY WILL BE TO QUICKLY
        DIVIDE THE SUMMED CHANNELS TO GET A RANGE WITHIN THE CHANNEL'S DEPTH.
        """
        ucc = self.unpacked_channel_count
        cmm = self.channel_merge_mapping
        cmd = self.channel_merge_divisors

        # if the unpacked number of channels is more than
        # the target format then we need to merge some
        if ucc <= self.target_channel_count:
            self.channel_merge_mapping = cmm = None
        elif "channel_merge_mapping" not in kwargs:
            self.texture_block = None
            raise TypeError((
                "ERROR: CONVERTING FROM FORMAT WITH %s CHANNELS TO " +
                "FORMAT WITH %s CHANNELS.\nA MAPPING IS NEEDED TO " +
                "SPECIFY WHAT SHOULD BE MERGED WITH WHAT.\n",
                "DEREFERENCING TEXTURE BLOCK FROM BITMAP " +
                "CONVERTER TO PREVENT UNSTABLE CONVERSION.") % (
                    self.source_channel_count, self.target_channel_count))
        elif len(kwargs["channel_merge_mapping"]) != ucc:
            self.texture_block = None
            raise TypeError((
                "ERROR: INVALID NUMBER OF CHANNELS IN CHANNEL " +
                "MERGE MAPPING.\nEXPECTED %s CHANNELS BUT GOT %s.\n" +
                "DEREFERENCING TEXTURE BLOCK FROM BITMAP "+
                "CONVERTER TO PREVENT UNSTABLE CONVERSION.") % (
                    ucc, len(kwargs["channel_merge_mapping"])))
        elif cmm is None:
            self.channel_merge_mapping = cmm = array(
                "b", kwargs["channel_merge_mapping"])
            self.channel_merge_divisors = cmd = array(
                "l", [0]*self.target_channel_count)

        if cmm is not None:
            # loop through the length of the convert channel mapping
            for i in cmm:
                """WHAT WE ARE DOING HERE IS ADDING 1 TO EACH
                CHANNEL'S DIVISOR IN THE TARGET FORMAT FOR EVERY
                CHANNEL FROM THE ORIGINAL FORMAT BEING MERGED IN"""
                if i >= 0:
                    cmd[i] += 1

            # because the merge mapping will reference index -1 it will
            # be the last index. because we are appending an additional
            # divisor of 2**31-1 it will be erased when packed
            if -1 in cmm:
                cmd.append(CHANNEL_ERASE_DIVISOR)

    def save_to_file(self, **kwargs):
        try:
            """saves the loaded bitmap to a file"""
            output_path = kwargs.pop('output_path', self.filepath)
            ext = kwargs.pop('ext', None)
            
            if output_path is None:
                raise TypeError("Cannot save bitmap without output path.")
            elif self.texture_block is None:
                raise TypeError("No bitmap loaded to save to file.")
            elif bitmap_io is None:
                raise TypeError(
                    "Bitmap io module isnt loaded. Cant save bitmap to file.")
            
            # if the extension isnt provided in the
            # kwargs we try to get it from the filepath
            if ext is None:
                splitpath = path.splitext(output_path)
                output_path = splitpath[0]
                ext = splitpath[1][1:].lower()

            if ext not in bitmap_io.file_writers:
                raise TypeError(
                    "Unknown bitmap file export format", ext.lower())

            bitmap_io.file_writers[ext](self, output_path, ext.lower(), *kwargs)
        except:
            print("ERROR OCCURRED WHILE TRYING TO SAVE BITMAP TO FILE.")
            print(format_exc())


    def load_from_file(self, **kwargs):
        try:
            """loads the current bitmap from a file"""
            input_path = kwargs.pop('input_path', self.filepath)
            ext = kwargs.pop('ext', None)

            if input_path is None:
                raise TypeError("Cannot save bitmap without input path.")
            elif bitmap_io is None:
                raise TypeError(
                    "Bitmap io module isnt loaded. Cant load bitmap from file.")

            # if the extension isnt provided in the
            # kwargs we try to get it from the filepath
            if ext is None:
                splitpath = path.splitext(input_path)
                input_path = splitpath[0]
                ext = splitpath[1][1:].lower()
            
            if ext not in bitmap_io.file_readers:
                raise TypeError(
                    "Unknown bitmap file import format", ext.lower())
            
            bitmap_io.file_readers[ext](self, input_path, ext.lower(), *kwargs)
        except:
            print("ERROR OCCURRED WHILE TRYING TO LOAD BITMAP FROM FILE.")
            print(format_exc())


    def convert_texture(self):
        """Runs all the conversions routines for the parameters specified"""

        # only run if there is a valid texture block loaded
        if self.texture_block is None:
            raise TypeError(
                "No texture loaded. Cannot preform bitmap " +
                "conversion without a loaded texture.")

        try:
            fmt = self.format
            target_fmt = self.target_format
            tex_info = self.texture_info
            tex_block = self.texture_block
        
            '''if we want to reduce the resolution, but we have
            mipmaps, we can quickly reduce it by removing the
            larger bitmaps and .using the mipmaps instead'''
            while self.mipmap_count > 0 and self.downres_amount > 0:
                pix_count = self.width*self.height*self.depth
                if 2**int(log(pix_count, 2)) != pix_count:
                    raise ValueError("Cannot downscale non-power-of-2 bitmaps.")

                # remove one mipmap level for each sub-bitmap
                for sub_bitmap_index in range(self.sub_bitmap_count):
                    tex_block.pop(0)

                # divide the dimensions in half and make
                # sure they don't go below the minimum
                self.width, self.height, self.depth = clip_dimensions(
                    self.width//2, self.height//2, self.depth//2, fmt)
                self.downres_amount -= 1
                self.mipmap_count -= 1
                tex_info["width"] = self.width
                tex_info["height"] = self.height
                tex_info["depth"] = self.depth
                tex_info["mipmap_count"] = self.mipmap_count


            '''If we arent going to do any of these things,
            just try swizzling the texture and return.'''
            # Converting to a different format
            # Downsampling the bitmap
            # Generating mipmaps
            # Swapping the bitmap's channels.
            if not(fmt != target_fmt or self.downres_amount > 0 or
                self.swapping_channels or self.generate_mipmaps):

                """SWIZZLE THE TEXTURE IF POSSIBLE AND THE TARGET
                SWIZZLE MODE IS NOT THE CURRENT SWIZZLE MODE."""
                if self.target_format in COMPRESSED_FORMATS:
                    pass
                elif swizzler is not None:
                    self.reswizzler.swizzle_texture()
                else:
                    raise TypeError(
                        "Swizzler module not loaded. " +
                        "Cannot unswizzle without swizzler.")
                
                # return that the conversion was successful
                return True


            '''if the texture is swizzled then it needs to be
            unswizzled before we can do certain conversions with it.
            We can't downsample while swizzled nor convert to a
            compressed format(swizzling unsupported)'''
            if not(self.swizzled and (
                self.downres_amount > 0 or self.generate_mipmaps or
                target_fmt in COMPRESSED_FORMATS)):
                pass
            elif swizzler is not None:
                self.deswizzler.swizzle_texture(True)
            else:
                raise TypeError(
                    "Swizzler module not loaded. " +
                    "Cannot unswizzle without swizzler.")

            '''figure out if we need to depalettize. some formats wont
            support palettes, like DXT1-5, and downressing and other
            operations will require pixels to be explicitely defined'''
            if (target_fmt in COMPRESSED_FORMATS or
                self.downres_amount > 0) and self.is_palettized():
                self.palettize = False


            """CONVERT PACKED PIXELS INTO UNPACKED CHANNEL VALUES.
            CHANNEL SWAPPING IS INTEGRATED INTO UNPACKING THE PIXELS"""
            palettized_unpacker = self.palettized_unpacker
            if self.packed:
                # store the dimensions to local variables so we can change them
                w, h, d = self.width, self.height, self.depth
                
                for m in range(self.mipmap_count+1):
                    for sb in range(self.sub_bitmap_count):
                        # get the index of the bitmap we'll be working with
                        i = sb + (m*self.sub_bitmap_count)
                        
                        if self.is_palettized(i):
                            # unpack the bitmap's palette and indexing
                            unpacked_pal, unpacked_pix = palettized_unpacker(
                                self.palette[i], tex_block[i])
                            if not unpacked_pix:
                                return False
                            
                            # replace the packed palette with the unpacked one
                            self.palette[i] = unpacked_pal
                        else:
                            unpacked_pix = self.unpack(i, w, h, d)

                        if unpacked_pix is None:
                            raise TypeError("Unable to unpack bitmap data.")
                            
                        # now that we are done unpacking the pixel data we
                        # replace the packed array with the unpacked one
                        tex_block[i] = unpacked_pix

                    # calculate the dimensions for the next mipmap
                    w, h, d = clip_dimensions(w//2, h//2, d//2)
                    
                self.packed = False
                self.palette_packed = False

            
            '''DOWNRES BITMAP TO A LOWER RESOLUTION IF STILL NEEDING TO'''
            # only run if there aren't any mipmaps and
            # this bitmap still needs to be downressed
            if self.mipmap_count != 0 or self.downres_amount <= 0:
                pass
            elif swizzler is not None:
                for sb in range(self.sub_bitmap_count):
                    downressed_pixels, w, h, d = self._downsample_bitmap(
                        tex_block[sb], self.downres_amount,
                        self.width, self.height, self.depth, True)
                    
                    # now that we are done repacking the pixel data
                    # we replace the old pixel array with the new one
                    tex_block[sb] = downressed_pixels
                    
                self.downres_amount = 0
                tex_info["width"] = self.width = w
                tex_info["height"] = self.height = h
                tex_info["depth"] = self.depth = d
            else:
                raise TypeError(
                    "Swizzler module not loaded. " +
                    "Cannot downres without swizzler.")



            '''GENERATE MIPMAPS'''
            if not self.generate_mipmaps:
                pass
            elif swizzler is not None:
                new_mip_count = int(log(
                    max(self.width, self.height, self.depth), 2))
                mips_to_make = new_mip_count - self.mipmap_count
                
                if mips_to_make:
                    # get the current smallest dimensions so we can change them
                    mw, mh, md = clip_dimensions(
                        self.width//(2**self.mipmap_count),
                        self.height//(2**self.mipmap_count),
                        self.depth//(2**self.mipmap_count))

                    # Loop for each mipmap we need to make
                    for m in range(self.mipmap_count, new_mip_count):
                        for sb in range(self.sub_bitmap_count):
                            if self.is_palettized(sb):
                                ##############################################
                                """ NEED ROUTINE FOR MAKING PALETTIZED MIPS"""
                                ##############################################

                                # FOR NOW WE'LL PREVENT MIPS FROM BEING
                                # CREATED BY RESETTING THE MIPMAP COUNT
                                new_mip_count = self.mipmap_count
                                continue

                            # get the array of packed pixels to work with
                            mip_pixels = tex_block[m*self.sub_bitmap_count + sb]

                            mip_pixels, _, __, ___ = self._downsample_bitmap(
                                mip_pixels, 1, mw, mh, md)
                            tex_block.append(mip_pixels)
                        
                        # calculate the dimensions for the next mipmap
                        mw, mh, md = clip_dimensions(
                            mw//2, mh//2, md//2)
                    # change the mipmap count in the settings
                    tex_info["mipmap_count"] = self.mipmap_count = new_mip_count
            else:
                raise TypeError(
                    "Swizzler module not loaded. " +
                    "Cannot generate mipmaps without swizzler.")



            '''REPACK THE PIXEL DATA TO THE TARGET FORMAT'''
            if self.repack:
                # store the dimensions to local variables
                w, h, d = self.width, self.height, self.depth

                # if we are palettizing a non-palettized
                # bitmap, we need new palette
                if self.palettize and not self.is_palettized():
                    self.palette = [None]*(
                        self.mipmap_count + 1)*self.sub_bitmap_count

                for m in range(self.mipmap_count+1):
                    for sb in range(self.sub_bitmap_count):
                        # get the index of the bitmap we'll be working with
                        i = sb + (m*self.sub_bitmap_count)

                        if not self.palettize:
                            repacked_pixel_array = self.pack(
                                tex_block[i], w, h, d)
                            if repacked_pixel_array is None:
                                raise TypeError("Unable to pack bitmap data.")
                            
                            # now that we are done repacking the pixel data
                            # we replace the old pixel array with the new one
                            tex_block[i] = repacked_pixel_array
                            continue

                        if self.is_palettized(i):
                            # get the unpacked palette and indexing
                            unpacked_pal = self.palette[i]
                            unpacked_idx = tex_block[i]
                        else:
                            # pass the pixels over to the function to
                            # create a color palette and indexing from it
                            unpacked_pal, unpacked_idx = self.palette_picker(
                                tex_block[i])

                        packed_pal, packed_idx = self.palettized_packer(
                            unpacked_pal, unpacked_idx)
                        self.palette[i] = packed_pal
                        tex_block[i] = packed_idx

                    # calculate the dimensions for the next mipmap
                    w, h, d = clip_dimensions(w//2, h//2, d//2)
                    
                self.packed = True
                self.palette_packed = True
                self.indexing_size = self.target_indexing_size

            """SWIZZLE THE TEXTURE IF POSSIBLE AND THE TARGET
            SWIZZLE MODE IS NOT THE CURRENT SWIZZLE MODE."""
            if self.target_format in COMPRESSED_FORMATS:
                pass
            elif swizzler is not None:
                self.reswizzler.swizzle_texture()
            else:
                raise TypeError(
                    "Swizzler module not loaded. " +
                    "Cannot swizzle without swizzler.")

            # now that we have thoroughly messed with the bitmap, we need
            # to change the format and default all the channel mappings
            self.format = target_fmt
            self._set_all_channel_mappings()
            
            # return that the conversion was successful
            return True
        except:
            print("Error occurred while attempting to convert texture.")
            print(format_exc())
            return False

    def depalettize_bitmap(self, unpacked_palette, unpacked_indexing):
        """Converts a palettized bitmap into an 8BPP
        unpalettized version and returns it. palette and
        indexing provided must be in an unpacked format"""
        ucc = self.unpacked_channel_count
        
        depalettized_bitmap = array(self._UNPACK_ARRAY_CODE,
                                    [0]*(ucc*len(unpacked_indexing)))

        if fast_arbytmap:
            arbytmap_ext.depalettize_bitmap(
                depalettized_bitmap, unpacked_indexing, unpacked_palette, ucc)

            return depalettized_bitmap

        i = 0
        
        if ucc == 4:
            for index in unpacked_indexing:
                depalettized_bitmap[i] = unpacked_palette[index*4]
                depalettized_bitmap[i+1] = unpacked_palette[index*4+1]
                depalettized_bitmap[i+2] = unpacked_palette[index*4+2]
                depalettized_bitmap[i+3] = unpacked_palette[index*4+3]
                i += 4
        elif ucc == 2:
            for index in unpacked_indexing:
                depalettized_bitmap[i] = unpacked_palette[index*2]
                depalettized_bitmap[i+1] = unpacked_palette[index*2+1]
                i += 2
        elif ucc == 1:
            for index in unpacked_indexing:
                depalettized_bitmap[i] = unpacked_palette[index]
                i += 1
        
        return depalettized_bitmap

    def _downsample_bitmap(self, unsampled_bitmap, sample_size,
                           width, height, depth, delete_original=False):
        '''This function will halve a bitmap's resolution
        X number of times, where X == self.downres_amount'''
        ucc = self.unpacked_channel_count
        
        gamma = self.gamma
        no_gamma_scale = True

        if max(gamma) != 1.0 or min(gamma) != 1.0:
            no_gamma_scale = False
            
        # calculate the new dimensions of the bitmap
        new_width, new_height, new_depth = clip_dimensions(
            width//2**sample_size,
            height//2**sample_size,
            depth//2**sample_size)

        # These are the log2 of each dimension
        log_w, log_h, log_d = (
            int(log(width, 2)), int(log(height, 2)), int(log(depth, 2)))

        # These are the log2 of each new dimension
        log_new_w, log_new_h, log_new_d = (
            int(log(new_width, 2)),
            int(log(new_height, 2)),
            int(log(new_depth, 2)))

        # These are how many pixels to merge on each axis
        merge_x, merge_y, merge_z = (
            2**(log_w-log_new_w), 2**(log_h-log_new_h), 2**(log_d-log_new_d))

        # The new array to place the downsampled pixels into
        downsamp = array(self._UNPACK_ARRAY_CODE,
                         [0]*(new_width*new_height*new_depth*ucc) )
        
        # The number of pixels from are being merged into one
        pmio = merge_x * merge_y * merge_z

        # under normal circumstances this should be 255, or possibly 65535
        val_scale = 2**(8*PIXEL_ENCODING_SIZES[self._UNPACK_ARRAY_CODE]) - 1

        # This is used in the gamma based merging to
        # scale the 0-255 or 0-65535 value to a 0-1 value
        pmd = pmio * float(val_scale)
        
        """THIS PART IS ABSOLUTELY CRUCIAL. In order to easily merge all
        the pixels together we will swizzle them around so that all the
        pixels that will be merged into one are directly next to each
        other, but separated by color channel. so it will look like this:
        
        px1A|px2A|px3A|px4A
        px1R|px2R|px3R|px4R
        px1G|px2G|px3G|px4G
        px1B|px2B|px3B|px4B
        """
        pixel_merge_swizzler = swizzler.Swizzler(
            texture_converter = self, mask_type = "DOWNSAMPLER",
            new_width=new_width, new_height=new_height, new_depth=new_depth)
        
        swizzled = pixel_merge_swizzler.swizzle_single_array(
            unsampled_bitmap, True, ucc, width, height, depth, delete_original)
        
        
        if no_gamma_scale:
            if fast_arbytmap:
                arbytmap_ext.downsample_bitmap(downsamp, swizzled, pmio, ucc)

                return(downsamp, new_width, new_height, new_depth)

            # merge pixels linearly
            if ucc == 4:
                for i in range(0, len(downsamp), 4):
                    downsamp[i]   = sum(swizzled[i*pmio:pmio*(i+1)])//pmio
                    downsamp[i+1] = sum(swizzled[pmio*(i+1):pmio*(i+2)])//pmio
                    downsamp[i+2] = sum(swizzled[pmio*(i+2):pmio*(i+3)])//pmio
                    downsamp[i+3] = sum(swizzled[pmio*(i+3):pmio*(i+4)])//pmio
            elif ucc == 2:
                for i in range(0, len(downsamp), 2):
                    downsamp[i]   = sum(swizzled[i*pmio:pmio*(i+1)])//pmio
                    downsamp[i+1] = sum(swizzled[pmio*(i+1):pmio*(i+2)])//pmio
            else:
                for i in range(len(downsamp)):
                    downsamp[i] = sum(swizzled[i*pmio:pmio*(i+1)])//pmio
            return(downsamp, new_width, new_height, new_depth)

        """merge pixels with gamma correction"""
        # DONT USE GAMMA BASED MERGING IF THE BITMAP
        # USES LINEAR GRADIENTS, LIKE WITH METERS

        ######################
        '''NEEDS MORE SPEED'''
        ######################

        gamma_0 = gamma[0]
        g_exp_0 = 1.0/gamma_0
        g_scale_0 = self.gamma_scaler[0]
        
        if ucc > 0:
            g_exp_1 = 1.0/gamma[1]
            g_scale_1 = self.gamma_scaler[1]
        if ucc > 1:
            g_exp_2 = 1.0/gamma[2]
            g_scale_2 = self.gamma_scaler[2]
        if ucc > 2:
            g_exp_3 = 1.0/gamma[3]
            g_scale_3 = self.gamma_scaler[3]

        if ucc == 4:
            for i in range(0, len(downsamp), 4):
                downsamp[i] = int(((sum(map(
                    lambda val: g_scale_0[val],
                    swizzled[i*pmio:pmio*(i+1)]))/pmd)**g_exp_0)*val_scale)

                downsamp[i+1] = int(((sum(map(
                    lambda val: g_scale_1[val],
                    swizzled[pmio*(i+1):pmio*(i+2)]))/pmd)**g_exp_1 )*val_scale)

                downsamp[i+2] = int(((sum(map(
                    lambda val: g_scale_2[val],
                    swizzled[pmio*(i+2):pmio*(i+3)]))/pmd)**g_exp_2 )*val_scale)

                downsamp[i+3] = int(((sum(map(
                    lambda val: g_scale_3[val],
                    swizzled[pmio*(i+3):pmio*(i+4)]))/pmd)**g_exp_3 )*val_scale)
        elif ucc == 2:
            for i in range(0, len(downsamp), 2):
                downsamp[i] = int(((sum(map(
                    lambda val: g_scale_0[val],
                    swizzled[i*pmio:pmio*(i+1)]))/pmd)**g_exp_0 )*val_scale)

                downsamp[i+1] = int(((sum(map(
                    lambda val: g_scale_1[val],
                    swizzled[pmio*(i+1):pmio*(i+2)]))/pmd)**g_exp_1 )*val_scale)
        else:
            for i in range(len(downsamp)):
                downsamp[i] = int(((sum(map(
                    lambda val: g_scale_0[val],
                    swizzled[i*pmio:pmio*(i+1)]))/pmd)**g_exp_0 )*val_scale)

        return(downsamp, new_width, new_height, new_depth)

    def _unpack_palettized(self, packed_palette, packed_indexing):
        '''When supplied with a packed palette and indexing,
        this function will return them in an unpacked form'''
        
        unpacked_palette = packed_palette
        unpacked_indexing = packed_indexing

        # UNPACK THE PALETTE
        if self.packed:
            unpacked_palette = self.palette_unpacker(packed_palette)
        
        # UNPACK THE INDEXING
        if self.packed:
            unpacked_indexing = self.indexing_unpacker(packed_indexing)
        
        if self.palettize:
            return(unpacked_palette, unpacked_indexing)
        
        # if the bitmap isn't going to stay palettized, we depalettize it
        return(None, self.depalettize_bitmap(
            unpacked_palette, unpacked_indexing))

    def _unpack_palette(self, packed_palette):
        """Just a redirect to the _Unpack_Raw function"""
        if self.palette_packed:
            return self.unpack_raw(packed_palette)
        return packed_palette

    def _unpack_indexing(self, packed_indexing):
        if self.indexing_size not in (1,2,4,8):
            raise TypeError(
                "Arbytmap cannot unpack indexing from " +
                "sizes other than 1, 2, 4, or 8 bit")
        
        if self.indexing_size == 8:
            # if the indexing is 8 bits then we can 
            # just copy it directly into a new array
            return array("B", packed_indexing)

        pixel_count = (len(packed_indexing)*8) // self.indexing_size
        unpacked_indexing = array('B', [0]*pixel_count)

        if fast_raw_unpacker:
            raw_unpacker_ext.unpack_indexing(
                unpacked_indexing, packed_indexing,
                self.indexing_size)

            return unpacked_indexing
        
        i = 0

        if self.indexing_size == 4:
            for indexing_chunk in packed_indexing:
                unpacked_indexing[i] = indexing_chunk&15
                unpacked_indexing[i+1] = (indexing_chunk&240)>>4
                i += 2
        elif self.indexing_size == 2:
            for indexing_chunk in packed_indexing:
                unpacked_indexing[i] = indexing_chunk&3
                unpacked_indexing[i+1] = (indexing_chunk&12)>>2
                unpacked_indexing[i+2] = (indexing_chunk&48)>>4
                unpacked_indexing[i+3] = (indexing_chunk&192)>>6
                i += 4
        else:
            for indexing_chunk in packed_indexing:
                unpacked_indexing[i] = indexing_chunk&1
                unpacked_indexing[i+1] = (indexing_chunk&2)>>1
                unpacked_indexing[i+2] = (indexing_chunk&4)>>2
                unpacked_indexing[i+3] = (indexing_chunk&8)>>3
                unpacked_indexing[i+4] = (indexing_chunk&16)>>4
                unpacked_indexing[i+5] = (indexing_chunk&32)>>5
                unpacked_indexing[i+6] = (indexing_chunk&64)>>6
                unpacked_indexing[i+7] = (indexing_chunk&128)>>7
                i += 8

        return unpacked_indexing

    def unpack(self, bitmap_index, width, height, depth):
        """Used for unpacking non-palettized formats"""
        if self.format in FORMAT_UNPACKERS:
            unpacked_pixels = FORMAT_UNPACKERS[self.format](
                self, bitmap_index, width, height, depth)
        elif self.format not in RAW_FORMATS:
            raise TypeError("Cannot find target format unpack method")
        elif (self.unpacked_channel_count == 1 and
            self.source_channel_count == 1 and sum(self.unpacked_depths) == 8):
            # if there is only 1 channel in the source file and we
            # are unpacking to only 1 channel then we don't need to
            # unpack the channels and we can use the array as it is
            unpacked_pixels = array("B", self.texture_block[bitmap_index])
        else:
            unpacked_pixels = self.unpack_raw(self.texture_block[bitmap_index])
        
        return unpacked_pixels

    def unpack_raw(self, packed_array):
        '''this function takes the loaded raw
        pixel data texture and unpacks it'''
        offsets = self.channel_offsets
        masks   = self.channel_masks
        upscale = self.channel_upscalers
        fill_value = 0

        if BITS_PER_PIXEL[self.format] in (8, 16, 24, 32, 48, 64):
            # this is a little hack to set the alpha
            # channel value to white if we are erasing it
            if masks[0] == 0:
                fill_value = 2**self.channel_depths[0] - 1

            if self.unpacked_channel_count == 4:
                unpacked_array = self._unpack_raw_4_channel(
                    packed_array, offsets, masks, upscale, fill_value)
            elif self.unpacked_channel_count == 2:
                unpacked_array = self._unpack_raw_2_channel(
                    packed_array, offsets, masks, upscale, fill_value)
            elif self.unpacked_channel_count == 1:
                unpacked_array = self._unpack_raw_1_channel(
                    packed_array, offsets, masks, upscale, fill_value)

            return unpacked_array

        raise TypeError(
            "Arbyemap cannot unpack raw pixels of sizes " +
            "other than 8, 16, 24, 32, 48, or 64 bit.")

    def _unpack_raw_4_channel(self, packed_array, offsets,
                              masks, upscale, fill_value=0):
        a_shift, r_shift, g_shift, b_shift = (offsets[0], offsets[1],
                                              offsets[2], offsets[3])
        a_mask,  r_mask,  g_mask,  b_mask =  (masks[0],   masks[1],
                                              masks[2],   masks[3])
        a_scale, r_scale, g_scale, b_scale = (upscale[0], upscale[1],
                                              upscale[2], upscale[3])
        
        # create a new array to hold the pixels after we unpack them
        unpacked_array = array(self._UNPACK_ARRAY_CODE,
                               [fill_value]*len(packed_array)*
                               self.unpacked_channel_count )
        
        if fast_raw_unpacker:
            raw_unpacker_ext.unpack_raw_4_channel(
                unpacked_array, packed_array,
                a_scale, r_scale, g_scale, b_scale,
                a_mask,  r_mask,  g_mask,  b_mask,
                a_shift, r_shift, g_shift, b_shift)
        else:
            i = 0
            for pixel in packed_array:
                unpacked_array[i]   = a_scale[(pixel&a_mask)>>a_shift]
                unpacked_array[i+1] = r_scale[(pixel&r_mask)>>r_shift]
                unpacked_array[i+2] = g_scale[(pixel&g_mask)>>g_shift]
                unpacked_array[i+3] = b_scale[(pixel&b_mask)>>b_shift]
                i += 4

        return unpacked_array

    def _unpack_raw_2_channel(self, packed_array, offsets,
                              masks, upscale, fill_value=0):
        a_shift, i_shift = offsets[0], offsets[1]
        a_mask,  i_mask  = masks[0],   masks[1]
        a_scale, i_scale = upscale[0], upscale[1]
            
        # create a new array to hold the pixels after we unpack them
        unpacked_array = array(self._UNPACK_ARRAY_CODE,
                               [fill_value]*len(packed_array)*
                               self.unpacked_channel_count )

        if fast_raw_unpacker:
            raw_unpacker_ext.unpack_raw_2_channel(
                unpacked_array, packed_array,
                a_scale, i_scale, a_mask, i_mask, a_shift, i_shift)
        else:
            i = 0
            for pixel in packed_array:
                unpacked_array[i]   = a_scale[(pixel&a_mask)>>a_shift]
                unpacked_array[i+1] = i_scale[(pixel&i_mask)>>i_shift]
                i += 2

        return unpacked_array

    def _unpack_raw_1_channel(self, packed_array, offsets,
                              masks, upscale, fill_value=0):
        shift, mask, scale = offsets[0], masks[0], upscale[0]
            
        # create a new array to hold the pixels after we unpack them
        unpacked_array = array(self._UNPACK_ARRAY_CODE,
                               [fill_value]*len(packed_array)*
                               self.unpacked_channel_count)
        
        if fast_raw_unpacker:
            raw_unpacker_ext.unpack_raw_1_channel(
                unpacked_array, packed_array, scale, mask, shift)
        else:
            i = 0
            for pixel in packed_array:
                unpacked_array[i] = scale[(pixel&mask)>>shift]
                i += 1
                
        return unpacked_array

    def _pack_palettized(self, unpacked_palette, unpacked_indexing):
        """Used for turning a palette and indexing into arrays
        suitable for being written to a file in little endian format"""
        
        # PACK THE PALETTE
        packed_palette = self.palette_packer(unpacked_palette)

        # PACK THE INDEXING
        packed_indexing = self.indexing_packer(unpacked_indexing)
            
        return(packed_palette, packed_indexing)


    def _pack_palette(self, unpacked_palette):
        if BITS_PER_PIXEL[self.target_format] == 24:
            # Because we can't store 3 byte integers in an array, the
            # best we can do is remove the padded alpha channel
            packed_palette = bitmap_io.unpad_24bit_array(unpacked_palette)
        else:
            packed_palette = self.pack_raw(unpacked_palette)

        return packed_palette


    def _pack_indexing(self, unpacked_indexing):
        if self.target_indexing_size not in (1,2,4,8):
            raise TypeError(
                "Arbytmap cannot pack indexing to " +
                "sizes other than 1, 2, 4, or 8 bit")
        
        largest_indexing_value = max(unpacked_indexing)
        
        if largest_indexing_value >= 2**self.target_indexing_size:
            raise TypeError(
                "Palette indexing references a palette color outside " +
                "the palette.\n Palette length is %s, but found %s." % (
                    2**self.target_indexing_size-1, largest_indexing_value))
        
        if self.target_indexing_size == 8:
            # If the indexing is 8 bits then we can
            # just copy it directly into a new array
            return array("B", unpacked_indexing)

        upi = unpacked_indexing
        packed_count = (len(upi) * self.target_indexing_size)//8
        packed_indexing = array("B", [0]*packed_count)
        
        if fast_raw_packer:
            raw_packer_ext.pack_indexing(
                packed_indexing, unpacked_indexing,
                self.target_indexing_size)

            return packed_indexing
        
        # The indexing will be packed in little endian mode
        if self.target_indexing_size == 1:
            for i in range(0, len(packed_indexing)*8, 8):
                packed_indexing[i//8] = (
                    upi[i]+        (upi[i+1]<<1) +
                   (upi[i+2]<<2) + (upi[i+3]<<3) +
                   (upi[i+4]<<4) + (upi[i+5]<<5) +
                   (upi[i+6]<<6) + (upi[i+7]<<7) )                    
        elif self.target_indexing_size == 2:
            for i in range(0, len(packed_indexing)*4, 4):
                packed_indexing[i//4] = (
                    upi[i]       + (upi[i+1]<<2) +
                   (upi[i+2]<<4) + (upi[i+3]<<6)) 
        elif self.target_indexing_size == 4:
            for i in range(0, len(packed_indexing)*2, 2):
                packed_indexing[i//2] = upi[i]+ (upi[i+1]<<4)

        return packed_indexing

    def pack(self, upa, width, height, depth):        
        """Used for packing non-palettized formats"""
        if self.target_format in FORMAT_PACKERS:
            return FORMAT_PACKERS[self.target_format](
                self, upa, width, height, depth)
        elif self.target_format in RAW_FORMATS:
            return self.pack_raw(upa)
        else:
            raise TypeError("Cannot find target format pack method")

    def pack_raw(self, unpacked_array):
        '''this function packs the 8-bit pixel array that's
        been created by the unpacking process.'''
        downscale = self.channel_downscalers
        ucc = self.unpacked_channel_count
        
        if BITS_PER_PIXEL[self.target_format] not in (8, 16, 24, 32, 48, 64):
            raise TypeError(
                "Arbytmap cannot pack raw pixels to sizes " +
                "other than 8, 16, 24, 32, 48, or 64 bit.")

        # If the nubmer of unpacked channels is just 1 it
        # means we can just use the original array as it is
        if ucc != 1 or self.target_channel_count != 1:
            off = FORMAT_CHANNEL_OFFSETS[self.target_format]
            
            if self.channel_merge_mapping is not None:
                cmm = self.channel_merge_mapping
                cmd = self.channel_merge_divisors
                
                if ucc == 4:
                    packed_array = self._pack_raw_4_channel_merge(
                        unpacked_array, downscale, ucc, cmm, off, cmd)
                elif ucc == 2:
                    packed_array = self._pack_raw_2_channel_merge(
                        unpacked_array, downscale, ucc, cmm, off, cmd)
            elif ucc == 4:
                packed_array = self._pack_raw_4_channel(
                    unpacked_array, downscale, ucc, off)
            elif ucc == 2:
                packed_array = self._pack_raw_2_channel(
                    unpacked_array, downscale, ucc, off)
        elif BITS_PER_PIXEL[self.target_format] == 8:
            packed_array = unpacked_array
        else:
            packed_array = self._pack_raw_1_channel(
                unpacked_array, downscale, ucc)

        return packed_array

    def _pack_raw_4_channel(self, upa, downscale, ucc, off):        
        # create the array to hold the pixel data after
        # it's been repacked in the target format
        packed_array = array(FORMAT_DATA_SIZES[self.target_format],
                             [0]*(len(upa)//ucc))
        
        a_shift, r_shift, g_shift, b_shift = (off[0], off[1], off[2], off[3])
        a_scale, r_scale, g_scale, b_scale = (downscale[0], downscale[1],
                                              downscale[2], downscale[3])

        if fast_raw_packer:
            raw_packer_ext.pack_raw_4_channel(
                packed_array, upa,
                a_scale, r_scale, g_scale, b_scale,
                a_shift, r_shift, g_shift, b_shift)
        else:
            for i in range(0, len(packed_array)*4, 4):
                packed_array[i//4] = ((a_scale[upa[i]]<<a_shift) +
                                      (r_scale[upa[i+1]]<<r_shift) +
                                      (g_scale[upa[i+2]]<<g_shift) +
                                      (b_scale[upa[i+3]]<<b_shift) )

        return packed_array


    def _pack_raw_2_channel(self, upa, downscale, ucc, off):
        # create the array to hold the pixel data after
        # it's been repacked in the target format
        packed_array = array(FORMAT_DATA_SIZES[self.target_format],
                             [0]*(len(upa)//ucc))
            
        a_shift, i_shift = off[0], off[1]
        a_scale, i_scale = downscale[0], downscale[1]
        
        if fast_raw_packer:
            raw_packer_ext.pack_raw_2_channel(
                packed_array, upa, a_scale, i_scale, a_shift, i_shift)
        else:
            for i in range(0, len(packed_array)*2, 2):
                packed_array[i//2] = ((a_scale[upa[i]]<<a_shift) +
                                      (i_scale[upa[i+1]]<<i_shift))

        return packed_array


    def _pack_raw_1_channel(self, upa, downscale, ucc, off=None):
        # create the array to hold the pixel data after
        # it's been repacked in the target format
        packed_array = array(FORMAT_DATA_SIZES[self.target_format],
                             [0]*(len(upa)//ucc))
        
        scale = downscale[0]
        
        if fast_raw_packer:
            raw_packer_ext.pack_raw_1_channel(packed_array, upa, scale)
        else:
            for i in range(len(packed_array)):
                packed_array[i] = scale[upa[i]]

        return packed_array


    def _pack_raw_4_channel_merge(self, upa, downscale, ucc, cmm, off, cmd):
        # create the array to hold the pixel data
        # after it's been repacked in the target format
        packed_array = array(FORMAT_DATA_SIZES[self.target_format],
                             [0]*(len(upa)//ucc))
        
        a_t, r_t, g_t, b_t = cmm[0], cmm[1], cmm[2], cmm[3]
        a_shift, r_shift, g_shift, b_shift = (off[a_t], off[r_t],
                                              off[g_t], off[b_t])
        a_div, r_div, g_div, b_div = cmd[a_t], cmd[r_t], cmd[g_t], cmd[b_t]
        a_rnd, r_rnd, g_rnd, b_rnd = a_div//2, r_div//2, g_div//2, b_div//2
        a_scale, r_scale, g_scale, b_scale = (
            downscale[0], downscale[1], downscale[2], downscale[3])
        
        # if the divisor is CHANNEL_ERASE_DIVISOR, it means to remove
        # the channel, so we shouldnt add half the divisor to round.
        a_rnd *= int(a_div != CHANNEL_ERASE_DIVISOR)
        r_rnd *= int(r_div != CHANNEL_ERASE_DIVISOR)
        g_rnd *= int(g_div != CHANNEL_ERASE_DIVISOR)
        b_rnd *= int(b_div != CHANNEL_ERASE_DIVISOR)
        
        if fast_raw_packer:
            raw_packer_ext.pack_raw_4_channel_merge(
                packed_array, upa, a_scale, r_scale, g_scale, b_scale,
                a_div, r_div, g_div, b_div,
                a_shift, r_shift, g_shift, b_shift)
        else:
            for i in range(0, len(packed_array)*4, 4):
                packed_array[i//4] = (
                    (a_scale[((upa[i]+a_rnd)//a_div)]<<a_shift) +
                    (r_scale[((upa[i+1]+r_rnd)//r_div)]<<r_shift) +
                    (g_scale[((upa[i+2]+g_rnd)//g_div)]<<g_shift) +
                    (b_scale[((upa[i+3]+b_rnd)//b_div)]<<b_shift))
        return packed_array


    def _pack_raw_2_channel_merge(self, upa, downscale, ucc, cmm, off, cmd):
        # create the array to hold the pixel data after
        # it's been repacked in the target format
        packed_array = array(FORMAT_DATA_SIZES[self.target_format],
                             [0]*(len(upa)//ucc))
        
        a_target, i_target = cmm[0], cmm[1]
        a_shift, i_shift = off[a_target], off[i_target]
        a_div, i_div = cmd[a_target], cmd[i_target]
        a_rnd, i_rnd = a_div//2, i_div//2
        a_scale, i_scale = downscale[0], downscale[1]

        # if the divisor is CHANNEL_ERASE_DIVISOR, it means to remove
        # the channel, so we shouldnt add half the divisor to round.
        a_rnd *= int(a_div != CHANNEL_ERASE_DIVISOR)
        i_rnd *= int(i_div != CHANNEL_ERASE_DIVISOR)
        
        if fast_raw_packer:
            raw_packer_ext.pack_raw_2_channel_merge(
                packed_array, upa, a_scale, i_scale,
                a_div, i_div, a_shift, i_shift)
        else:
            for i in range(0, len(packed_array)*2, 2):
                packed_array[i//2] = (
                    (a_scale[((upa[i]+a_rnd)//i_div)]<<a_shift) +
                    (i_scale[((upa[i+1]+i_rnd)//i_div)]<<i_shift))

        return packed_array


    def _palette_picker(self, unpacked_pixels):
        """Converts a bitmap into and returns
        an unpacked palette and indexing"""
        raise NotImplementedError
        return(unpacked_palette, unpacked_indexing)
