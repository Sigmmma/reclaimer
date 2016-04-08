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
    
    def Bitmap_Count(self, new_value=None):
        if new_value is None:
            return self.data.Data.Bitmaps.Count
        self.data.Data.Bitmaps.Count = new_value
        
    def Bitmap_Width(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.Data.Bitmaps.Bitmap_Block_Array[b_index].Width
        self.data.Data.Bitmaps.Bitmap_Block_Array[b_index].Width = new_value

    def Bitmap_Height(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.Data.Bitmaps.Bitmap_Block_Array[b_index].Height
        self.data.Data.Bitmaps.Bitmap_Block_Array[b_index].Height = new_value

    def Bitmap_Depth(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.Data.Bitmaps.Bitmap_Block_Array[b_index].Depth
        self.data.Data.Bitmaps.Bitmap_Block_Array[b_index].Depth = new_value

    def Bitmap_Mipmaps_Count(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.Data.Bitmaps.Bitmap_Block_Array[b_index].Mipmaps
        self.data.Data.Bitmaps.Bitmap_Block_Array[b_index].Mipmaps = new_value

    def Bitmap_Type(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.Data.Bitmaps.Bitmap_Block_Array[b_index].Type.data
        self.data.Data.Bitmaps.Bitmap_Block_Array[b_index].Type.data = new_value

    def Bitmap_Format(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.Data.Bitmaps.Bitmap_Block_Array[b_index].Format.data
        self.data.Data.Bitmaps.Bitmap_Block_Array[b_index].Format.data = new_value


    def Bitmap_Width_Height_Depth(self, b_index=0, new_value=None):
        Bitmap = self.data.Data.Bitmaps.Bitmap_Block_Array[b_index]
        if new_value is None:
            return(Bitmap.Width, Bitmap.Height, Bitmap.Depth)
        Bitmap.Width, Bitmap.Height, Bitmap.Depth = (new_value[0],
                                                     new_value[1],
                                                     new_value[2])

    def Bitmap_Flags(self, b_index=0, new_value=None):
        if new_value is None:
            return self.data.Data.Bitmaps.Bitmap_Block_Array[b_index].Flags
        self.data.Data.Bitmaps.Bitmap_Block_Array[b_index].Flags = new_value
        
    def Bitmap_Base_Address(self, b_index=0, new_value=None):
        if new_value is None:
            return(self.data.Data.Bitmaps.Bitmap_Block_Array[b_index].Base_Address)
        self.data.Data.Bitmaps.Bitmap_Block_Array[b_index].Base_Address = new_value

    def Bitmap_Data_Offset(self, b_index=0, new_value=None):
        if new_value is None:
            return(self.data.Data.Bitmaps.Bitmap_Block_Array[b_index].Pixels_Offset)
        self.data.Data.Bitmaps.Bitmap_Block_Array[b_index].Pixels_Offset = new_value



    def Registration_Point_X(self, b_index=0, new_value=None):
        Reg_Point = self.data.Data.Bitmaps.Bitmap_Block_Array[b_index].Registration_Point
        if new_value is None:
            return(Reg_Point.X)
        Reg_Point.X = new_value

    def Registration_Point_Y(self, b_index=0, new_value=None):
        Reg_Point = self.data.Data.Bitmaps.Bitmap_Block_Array[b_index].Registration_Point
        if new_value is None:
            return(Reg_Point.Y)
        Reg_Point.Y = new_value

    def Registration_Point_XY(self, b_index=0, new_value=None):
        Reg_Point = self.data.Data.Bitmaps.Bitmap_Block_Array[b_index].Registration_Point
        if new_value is None:
            return(Reg_Point.X, Reg_Point.Y)
        Reg_Point.X, Reg_Point.Y = new_value[0], new_value[1]


    @property
    def Is_Xbox_Bitmap(self):
        #we only need to check the first bitmap
        return self.Bitmap_Base_Address() == 1073751810
        
    def Processed_by_Reclaimer(self, new_flag=None):
        if new_flag is None:
            return self.data.Data.Flags.Processed_by_reclaimer
        self.data.Data.Flags.Processed_by_reclaimer = new_flag
        

    def Is_Power_of_2_Bitmap(self, b_index=0):
        return self.Bitmap_Flags(b_index).Power_of_2_dim
            
    def Is_Compressed_Bitmap(self, b_index=0):
        return self.Bitmap_Flags(b_index).Compressed
        
    def Swizzled(self, new_flag=None, b_index = 0):
        if new_flag is None:
            return self.Bitmap_Flags(b_index).Swizzled
        self.Bitmap_Flags(b_index).Swizzled = new_flag
    

    def Color_Plate_Data_Bytes_Size(self, new_value=None):
        if new_value is None:
            return(self.data.Data.Compressed_Color_Plate_Data.Count)
        self.data.Data.Compressed_Color_Plate_Data.Count = new_value
    

    def Pixel_Data_Bytes_Size(self, new_value=None):
        if new_value is None:
            return(self.data.Data.Processed_Pixel_Data.Count)
        self.data.Data.Processed_Pixel_Data.Count = new_value




    def Set_Platform(self, saveasxbox):
        '''changes different things to set the platform to either PC or Xbox'''
        #Read each of the bitmap blocks
        for b_index in range(self.Bitmap_Count()):
            Bitmap = self.data.Data.Bitmaps.Bitmap_Block_Array[b_index]
            
            Bitmap.Flags.set_to('Made_by_arsenic', saveasxbox)

            '''Base_Address is the ONLY discernable difference
            between a bitmap made by arsenic from a PC map, and
            a bitmap made by arsenic from an original XBOX map'''
            if saveasxbox:
                #change some miscellaneous variables               
                Bitmap.Pixels = 4608
                Bitmap.Bitmap_Data_Pointer = -1
                Bitmap.Base_Address = 1073751810
            else:
                Bitmap.Base_Address = 0


        if saveasxbox:
            #if Xbox, reset these structure variable's all to 0
            #since xbox doesn't like them being non-zero
            Data = self.data.Data
            for block in (Data.Compressed_Color_Plate_Data, Data.Processed_Pixel_Data):
                for i in (1,2,3):
                    block[i] = 0
                    
            for block in (Data.Sequences, Data.Bitmaps):
                for i in (1,2):
                    block[i] = 0
                    
            #swap the order of the cubemap faces and mipmaps if saving to xbox format
            self.Change_Sub_Bitmap_Ordering(saveasxbox)


    def Change_Sub_Bitmap_Ordering(self, Save_as_Xbox):
        '''Used to change the mipmap and cube face ordering.
        On pc all highest resolution faces are first, then
        the next highest resolution mipmap set. On xbox it's
        all of a face's mipmaps before any of the other faces.
        
        DO NOT UNDER ANY CIRCUMSTANCES CALL THIS FUNCTION
        IF PADDING HAS ALREADY BEEN ADDED TO A BITMAP'''

        Raw_Bitmap_Data = self.data.Data.Processed_Pixel_Data.Data

        #Loop over each of the bitmap blocks
        for b_index in range(self.Bitmap_Count()):
            
            if self.Bitmap_Type(b_index) == TYPE_CUBEMAP:
                mipmap_count = self.Bitmap_Mipmaps_Count(b_index) + 1
                Tex_Block = Raw_Bitmap_Data[b_index]
        
                if isinstance(Tex_Block[0], array):
                    #change the type of data for the bitmap pixels
                    #to ANY array block. All Py_Array Tag_Types use
                    #the same writer, thus any Py_Array Tag_Type will work
                    Tex_Block.set_desc('TYPE', UInt8Array, 'SUB_STRUCT')

                #this will be used to copy values from
                Template = Tex_Block.__copy__()

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
                        if Save_as_Xbox:#True = Xbox, False = PC
                            Tex_Block[i] = Template[mip + face]
                        else:
                            Tex_Block[mip + face] = Template[i]
                        i += 1
                    
