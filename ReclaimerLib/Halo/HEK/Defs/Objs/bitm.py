from .Tag import *

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

        

class BITM_Tag(HEK_Tag):
    
    def Bitmap_Count(self, New_Value=None):
        if New_Value is None:
            return(self.Tag_Data.Data.Bitmaps.Block_Count)
        self.Tag_Data.Data.Bitmaps.Block_Count = New_Value
        
    def Bitmap_Width(self, Bitmap_Index=0, New_Value=None):
        if New_Value is None:
            return(self.Tag_Data.Data.Bitmaps.Bitmap_Block_Array[Bitmap_Index].Width)
        self.Tag_Data.Data.Bitmaps.Bitmap_Block_Array[Bitmap_Index].Width = New_Value

    def Bitmap_Height(self, Bitmap_Index=0, New_Value=None):
        if New_Value is None:
            return(self.Tag_Data.Data.Bitmaps.Bitmap_Block_Array[Bitmap_Index].Height)
        self.Tag_Data.Data.Bitmaps.Bitmap_Block_Array[Bitmap_Index].Height = New_Value

    def Bitmap_Depth(self, Bitmap_Index=0, New_Value=None):
        if New_Value is None:
            return(self.Tag_Data.Data.Bitmaps.Bitmap_Block_Array[Bitmap_Index].Depth)
        self.Tag_Data.Data.Bitmaps.Bitmap_Block_Array[Bitmap_Index].Depth = New_Value

    def Bitmap_Mipmaps_Count(self, Bitmap_Index=0, New_Value=None):
        if New_Value is None:
            return(self.Tag_Data.Data.Bitmaps.Bitmap_Block_Array[Bitmap_Index].Mipmaps)
        self.Tag_Data.Data.Bitmaps.Bitmap_Block_Array[Bitmap_Index].Mipmaps = New_Value

    def Bitmap_Type(self, Bitmap_Index=0, New_Value=None):
        if New_Value is None:
            return self.Tag_Data.Data.Bitmaps.Bitmap_Block_Array[Bitmap_Index].Type.Data
        self.Tag_Data.Data.Bitmaps.Bitmap_Block_Array[Bitmap_Index].Type.Data = New_Value

    def Bitmap_Format(self, Bitmap_Index=0, New_Value=None):
        if New_Value is None:
            return self.Tag_Data.Data.Bitmaps.Bitmap_Block_Array[Bitmap_Index].Format.Data
        self.Tag_Data.Data.Bitmaps.Bitmap_Block_Array[Bitmap_Index].Format.Data = New_Value


    def Bitmap_Width_Height_Depth(self, Bitmap_Index=0, New_Value=None):
        Bitmap = self.Tag_Data.Data.Bitmaps.Bitmap_Block_Array[Bitmap_Index]
        if New_Value is None:
            return(Bitmap.Width, Bitmap.Height, Bitmap.Depth)
        Bitmap.Width, Bitmap.Height, Bitmap.Depth = (New_Value[0],
                                                     New_Value[1],
                                                     New_Value[2])

    def Bitmap_Flags(self, Bitmap_Index=0, New_Value=None):
        if New_Value is None:
            return self.Tag_Data.Data.Bitmaps.Bitmap_Block_Array[Bitmap_Index].Flags
        self.Tag_Data.Data.Bitmaps.Bitmap_Block_Array[Bitmap_Index].Flags.Data = New_Value
        
    def Bitmap_Base_Address(self, Bitmap_Index=0, New_Value=None):
        if New_Value is None:
            return(self.Tag_Data.Data.Bitmaps.Bitmap_Block_Array[Bitmap_Index].Base_Address)
        self.Tag_Data.Data.Bitmaps.Bitmap_Block_Array[Bitmap_Index].Base_Address = New_Value

    def Bitmap_Data_Offset(self, Bitmap_Index=0, New_Value=None):
        if New_Value is None:
            return(self.Tag_Data.Data.Bitmaps.Bitmap_Block_Array[Bitmap_Index].Pixels_Offset)
        self.Tag_Data.Data.Bitmaps.Bitmap_Block_Array[Bitmap_Index].Pixels_Offset = New_Value



    def Registration_Point_X(self, Bitmap_Index=0, New_Value=None):
        Reg_Point = self.Tag_Data.Data.Bitmaps.Bitmap_Block_Array[Bitmap_Index].Registration_Point
        if New_Value is None:
            return(Reg_Point.X)
        Reg_Point.X = New_Value

    def Registration_Point_Y(self, Bitmap_Index=0, New_Value=None):
        Reg_Point = self.Tag_Data.Data.Bitmaps.Bitmap_Block_Array[Bitmap_Index].Registration_Point
        if New_Value is None:
            return(Reg_Point.Y)
        Reg_Point.Y = New_Value

    def Registration_Point_XY(self, Bitmap_Index=0, New_Value=None):
        Reg_Point = self.Tag_Data.Data.Bitmaps.Bitmap_Block_Array[Bitmap_Index].Registration_Point
        if New_Value is None:
            return(Reg_Point.X, Reg_Point.Y)
        Reg_Point.X, Reg_Point.Y = New_Value[0], New_Value[1]


    @property
    def Is_Xbox_Bitmap(self):
        #we only need to check the first bitmap
        return self.Bitmap_Base_Address() == 1073751810
        
    def Processed_by_Reclaimer(self, New_Flag=None):
        if New_Flag is None:
            return self.Tag_Data.Data.Flags.Processed_by_Reclaimer
        self.Tag_Data.Data.Flags.Processed_by_Reclaimer = New_Flag
        

    def Is_Power_of_2_Bitmap(self, Bitmap_Index=0):
        return self.Bitmap_Flags(Bitmap_Index).Power_of_2_Dim
            
    def Is_Compressed_Bitmap(self, Bitmap_Index=0):
        return self.Bitmap_Flags(Bitmap_Index).Compressed
        
    def Swizzled(self, New_Flag=None, Bitmap_Index = 0):
        if New_Flag is None:
            return self.Bitmap_Flags(Bitmap_Index).Swizzled
        self.Bitmap_Flags(Bitmap_Index).Swizzled = New_Flag
    

    def Color_Plate_Data_Bytes_Size(self, New_Value=None):
        if New_Value is None:
            return(self.Tag_Data.Data.Compressed_Color_Plate_Data.Byte_Count)
        self.Tag_Data.Data.Compressed_Color_Plate_Data.Byte_Count = New_Value
    

    def Pixel_Data_Bytes_Size(self, New_Value=None):
        if New_Value is None:
            return(self.Tag_Data.Data.Processed_Pixel_Data.Byte_Count)
        self.Tag_Data.Data.Processed_Pixel_Data.Byte_Count = New_Value




    def Set_Platform(self, Save_As_Xbox):
        '''changes different things to set the platform to either PC or Xbox'''
        #Read each of the bitmap blocks
        for Bitmap_Index in range(self.Bitmap_Count()):
            Bitmap = self.Tag_Data.Data.Bitmaps.Bitmap_Block_Array[Bitmap_Index]
            
            Bitmap.Flags.Set_To('Made_by_Arsenic', Save_As_Xbox)

            '''Base_Address is the ONLY discernable difference
            between a bitmap made by arsenic from a PC map, and
            a bitmap made by arsenic from an original XBOX map'''
            if Save_As_Xbox:
                #change some miscellaneous variables               
                Bitmap.Pixels = 4608
                Bitmap.Bitmap_Data_Pointer = -1
                Bitmap.Base_Address = 1073751810
            else:
                Bitmap.Base_Address = 0


        if Save_As_Xbox:
            #if Xbox, reset these structure variable's all to 0
            #since xbox doesn't like them being non-zero
            Data = self.Tag_Data.Data
            for Block in (Data.Compressed_Color_Plate_Data, Data.Processed_Pixel_Data):
                for i in (1,2,3):
                    Block[i] = 0
                    
            for Block in (Data.Sequences, Data.Bitmaps):
                for i in (1,2):
                    Block[i] = 0
                    
            #swap the order of the cubemap faces and mipmaps if saving to xbox format
            self.Change_Sub_Bitmap_Ordering(Save_As_Xbox)


    def Change_Sub_Bitmap_Ordering(self, Save_as_Xbox):
        '''Used to change the mipmap and cube face ordering.
        On pc all highest resolution faces are first, then
        the next highest resolution mipmap set. On xbox it's
        all of a face's mipmaps before any of the other faces.
        
        DO NOT UNDER ANY CIRCUMSTANCES CALL THIS FUNCTION
        IF PADDING HAS ALREADY BEEN ADDED TO A BITMAP'''

        Raw_Bitmap_Data = self.Tag_Data.Data.Processed_Pixel_Data.Data

        #Loop over each of the bitmap blocks
        for Bitmap_Index in range(self.Bitmap_Count()):
            
            if self.Bitmap_Type(Bitmap_Index) == TYPE_CUBEMAP:
                Mipmap_Count = self.Bitmap_Mipmaps_Count(Bitmap_Index) + 1
                Tex_Block = Raw_Bitmap_Data[Bitmap_Index]
        
                if isinstance(Tex_Block[0], array):
                    #change the type of data for the bitmap pixels
                    #to ANY array block. All Py_Array Tag_Types use
                    #the same writer, thus any Py_Array Tag_Type will work
                    Tex_Block.Set_Desc('TYPE', UInt8_Array, 'SUB_STRUCT')

                #this will be used to copy values from
                Template = Tex_Block.__copy__()

                #this is used to keep track of which index
                #we're placing the new pixel array into
                i = 0
                
                '''since we also want to swap the second and third
                cubemap faces we can do that easily like this xbox
                has the second and third cubemap faces transposed
                with each other compared to pc. IDFKY'''
                for Face in (0, 2, 1, 3, 4, 5):
                    for Mipmap in range(0, Mipmap_Count*6, 6):
                        '''get the block we want from the original
                        layout and place it in its new position'''
                        if Save_as_Xbox:#True = Xbox, False = PC
                            Tex_Block[i] = Template[Mipmap + Face]
                        else:
                            Tex_Block[Mipmap + Face] = Template[i]
                        i += 1
                    
