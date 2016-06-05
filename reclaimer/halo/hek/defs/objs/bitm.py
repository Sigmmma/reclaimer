from .tag import *

#in a bitmap tag this number designates the type
TYPE_2D = 0
TYPE_3D = 1
TYPE_CUBEMAP = 2
TYPE_WHITE = 3

#in a bitmap tag this number designates the format
FORMAT_NONE = -1#this value is used ONLY in the conversion process

FORMAT_A8 = 0
FORMAT_Y8 = 1
FORMAT_AY8 = 2
FORMAT_A8Y8 = 3
FORMAT_R5G6B5 = 6
FORMAT_A1R5G5B5 = 8
FORMAT_A4R4G4B4 = 9
FORMAT_X8R8G8B8 = 10
FORMAT_A8R8G8B8 = 11
FORMAT_DXT1 = 14
FORMAT_DXT3 = 15
FORMAT_DXT5 = 16
FORMAT_P8 = 17

DXT_FORMATS = [FORMAT_DXT1,FORMAT_DXT3,FORMAT_DXT5]

PALLETIZED_FORMATS = [FORMAT_P8]

#each bitmap's number of bytes must be a multiple of 512
BITMAP_PADDING = 512
#each sub-bitmap(cubemap face) must be a multiple of 128 bytes
CUBEMAP_PADDING = 128

        

class BitmTag(HekTag):
    
    def bitmap_count(self, new_value=None):
        if new_value is None:
            return self.data.Data.bitmaps.Count
        self.data.Data.bitmaps.Count = new_value
        
    def bitmap_width(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.Data.bitmaps.bitmaps_array[b_index].width
        self.data.Data.bitmaps.bitmaps_array[b_index].width = new_value

    def bitmap_height(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.Data.bitmaps.bitmaps_array[b_index].height
        self.data.Data.bitmaps.bitmaps_array[b_index].height = new_value

    def bitmap_depth(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.Data.bitmaps.bitmaps_array[b_index].depth
        self.data.Data.bitmaps.bitmaps_array[b_index].depth = new_value

    def bitmap_mipmaps_count(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.Data.bitmaps.bitmaps_array[b_index].mipmaps
        self.data.Data.bitmaps.bitmaps_array[b_index].mipmaps = new_value

    def bitmap_type(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.Data.bitmaps.bitmaps_array[b_index].type.data
        self.data.Data.bitmaps.bitmaps_array[b_index].type.data = new_value

    def bitmap_format(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.Data.bitmaps.bitmaps_array[b_index].format.data
        self.data.Data.bitmaps.bitmaps_array[b_index].format.data = new_value


    def bitmap_width_height_depth(self, b_index=0, new_value=None):
        bitmap = self.data.Data.bitmaps.bitmaps_array[b_index]
        if new_value is None:
            return(bitmap.width, bitmap.height, bitmap.depth)
        bitmap.width, bitmap.height, bitmap.depth = (new_value[0],
                                                     new_value[1],
                                                     new_value[2])

    def bitmap_flags(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.Data.bitmaps.bitmaps_array[b_index].flags
        self.data.Data.bitmaps.bitmaps_array[b_index].flags = new_value
        
    def bitmap_base_address(self, b_index=0, new_value=None):
        if new_value is None:
            return(self.data.Data.bitmaps.bitmaps_array[b_index].base_address)
        self.data.Data.bitmaps.bitmaps_array[b_index].base_address = new_value

    def bitmap_data_offset(self, b_index=0, new_value=None):
        if new_value is None:
            return(self.data.Data.bitmaps.\
                   bitmaps_array[b_index].pixels_offset)
        self.data.Data.bitmaps.bitmaps_array[b_index].pixels_offset = new_value



    def registration_point_x(self, b_index=0, new_value=None):
        reg_point = self.data.Data.bitmaps.\
                    bitmaps_array[b_index].registration_point
        if new_value is None:
            return(reg_point.x)
        reg_point.x = new_value

    def registration_point_y(self, b_index=0, new_value=None):
        reg_point = self.data.Data.bitmaps.\
                    bitmaps_array[b_index].registration_point
        if new_value is None:
            return(reg_point.y)
        reg_point.y = new_value

    def registration_point_xy(self, b_index=0, new_value=None):
        reg_point = self.data.Data.bitmaps.\
                    bitmaps_array[b_index].registration_point
        if new_value is None:
            return(reg_point.x, reg_point.y)
        reg_point.x, reg_point.y = new_value[0], new_value[1]


    @property
    def is_xbox_bitmap(self):
        #we only need to check the first bitmap
        return self.bitmap_base_address() == 1073751810
        
    def processed_by_reclaimer(self, new_flag=None):
        if new_flag is None:
            return self.data.Data.flags.processed_by_reclaimer
        self.data.Data.flags.processed_by_reclaimer = new_flag
        

    def is_power_of_2_bitmap(self, b_index=0):
        return self.bitmap_flags(b_index).power_of_2_dim
            
    def is_compressed_bitmap(self, b_index=0):
        return self.bitmap_flags(b_index).compressed
        
    def swizzled(self, new_flag=None, b_index = 0):
        if new_flag is None:
            return self.bitmap_flags(b_index).swizzled
        self.bitmap_flags(b_index).swizzled = new_flag
    

    def color_plate_data_bytes_size(self, new_value=None):
        if new_value is None:
            return(self.data.Data.compressed_color_plate_data.Count)
        self.data.Data.compressed_color_plate_data.Count = new_value
    

    def pixel_data_bytes_size(self, new_value=None):
        if new_value is None:
            return self.data.Data.processed_pixel_data.Count
        self.data.Data.processed_pixel_data.Count = new_value




    def set_platform(self, saveasxbox):
        '''changes different things to set the platform to either PC or Xbox'''
        #Read each of the bitmap blocks
        for b_index in range(self.bitmap_count()):
            bitmap = self.data.Data.bitmaps.bitmaps_array[b_index]
            
            bitmap.flags.set_to('made_by_arsenic', saveasxbox)

            '''base_address is the ONLY discernable difference
            between a bitmap made by arsenic from a PC map, and
            a bitmap made by arsenic from an original XBOX map'''
            if saveasxbox:
                #change some miscellaneous variables               
                bitmap.pixels = 4608
                bitmap.bitmap_data_pointer = -1
                bitmap.base_address = 1073751810
            else:
                bitmap.base_address = 0


        if saveasxbox:
            #if Xbox, reset these structure variable's all to 0
            #since xbox doesn't like them being non-zero
            Data = self.data.Data
            for block in (Data.compressed_color_plate_data,
                          Data.processed_pixel_data):
                for i in (1,2,3):
                    block[i] = 0
                    
            for block in (Data.sequences, Data.bitmaps):
                for i in (1,2):
                    block[i] = 0
                    
            #swap the order of the cubemap faces
            #and mipmaps if saving to xbox format
            self.change_sub_bitmap_ordering(saveasxbox)


    def change_sub_bitmap_ordering(self, saveasxbox):
        '''Used to change the mipmap and cube face ordering.
        On pc all highest resolution faces are first, then
        the next highest resolution mipmap set. On xbox it's
        all of a face's mipmaps before any of the other faces.
        
        DO NOT UNDER ANY CIRCUMSTANCES CALL THIS FUNCTION
        IF PADDING HAS ALREADY BEEN ADDED TO A BITMAP'''

        raw_bitmap_data = self.data.Data.processed_pixel_data.data

        #Loop over each of the bitmap blocks
        for b_index in range(self.bitmap_count()):
            
            if self.bitmap_type(b_index) == TYPE_CUBEMAP:
                mipmap_count = self.bitmap_mipmaps_count(b_index) + 1
                tex_block = raw_bitmap_data[b_index]
        
                if isinstance(tex_block[0], array):
                    #change the type of data for the bitmap pixels
                    #to ANY array block. All Py_Array Tag_Types use
                    #the same writer, thus any Py_Array Tag_Type will work
                    tex_block.set_desc('TYPE', UInt8Array, 'SUB_STRUCT')

                #this will be used to copy values from
                template = tex_block.__copy__()

                #this is used to keep track of which index
                #we're placing the new pixel array into
                i = 0
                
                '''since we also want to swap the second and third
                cubemap faces we can do that easily like this xbox
                has the second and third cubemap faces transposed
                with each other compared to pc. IDFKY'''
                for face in (0, 2, 1, 3, 4, 5):
                    for mip in range(0, mipmap_count*6, 6):
                        '''get the block we want from the original
                        layout and place it in its new position'''
                        if saveasxbox:#True = Xbox, False = PC
                            tex_block[i] = template[mip + face]
                        else:
                            tex_block[mip + face] = template[i]
                        i += 1
                    
