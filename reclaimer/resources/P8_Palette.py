from array import array
from math import sqrt

Hash_Multiplier = 10000

class P8_Palette_Class():

    def __init__(self):
        #caching these values in dictionaries this way will really speed up converting normal maps to p8 bump

        #this is the set of cached colors abailable to the dominant color channel, which is selected by the bias.
        #the keys are 0 - 255 and the values are the closest to that value that is available in the palette
        Cached_Dominant_Colors = dict(zip([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,
                                       34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,
                                       65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,
                                       96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,
                                       120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,
                                       143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,
                                       166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,
                                       189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,
                                       212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,
                                       235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255] ,
                                      [25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25,
                                       25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 47, 47, 47, 47, 47, 47, 47, 47, 47,
                                       47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 66, 66, 66, 66, 66, 66, 66, 66, 66, 66, 66,
                                       66, 66, 66, 66, 66, 66, 82, 82, 82, 82, 82, 82, 82, 82, 82, 82, 82, 82, 82, 82, 82, 96, 96,
                                       96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 96, 107, 107, 107, 107, 107, 107, 107, 107, 107,
                                       107, 116, 116, 116, 116, 116, 116, 116, 122, 122, 122, 122, 126, 126, 126, 126, 128, 129,
                                       129, 129, 133, 133, 133, 133, 139, 139, 139, 139, 139, 139, 139, 139, 148, 148, 148, 148,
                                       148, 148, 148, 148, 148, 148, 159, 159, 159, 159, 159, 159, 159, 159, 159, 159, 159, 159,
                                       173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 189, 189, 189,
                                       189, 189, 189, 189, 189, 189, 189, 189, 189, 189, 189, 189, 189, 189, 189, 208, 208, 208,
                                       208, 208, 208, 208, 208, 208, 208, 208, 208, 208, 208, 208, 208, 208, 208, 208, 208, 229,
                                       229, 229, 229, 229, 229, 229, 229, 229, 229, 229, 229, 229, 229, 229, 229, 229, 229, 229,
                                       229, 229, 229, 229, 229, 229, 229, 229, 229, 229, 229, 229, 229, 229, 229, 229, 229, 229]
                                     )
                                 )


        Cached_Submissive_Colors = []

        #this function is used for building the dictionaries that will be cached in the dictionary below
        #since there are 20 possible red or green values we build 20 lists
        for loop_count in range(20):
            
            if (loop_count == 0):
                Available_Colors = [0]
            elif (loop_count == 1 or loop_count == 19):
                Available_Colors = [122, 126, 128, 129, 133]
            elif (loop_count == 2 or loop_count == 18):
                Available_Colors = [116, 122, 126, 128, 129, 133, 139]
            elif (loop_count == 3 or loop_count == 17):
                Available_Colors = [107, 116, 122, 126, 128, 129, 133, 139, 148]
            elif (loop_count == 4 or loop_count == 16):
                Available_Colors = [96, 107, 116, 122, 126, 128, 129, 133, 139, 148, 159]
            elif (loop_count == 5 or loop_count == 15):
                Available_Colors = [82, 96, 107, 116, 122, 126, 128, 129, 133, 139, 148, 159, 173]
            elif (loop_count == 6 or loop_count == 14):
                Available_Colors = [66, 82, 96, 107, 116, 122, 126, 128, 129, 133, 139, 148, 159, 173, 189]
            elif (loop_count == 7 or loop_count == 13):
                Available_Colors = [47, 66, 82, 96, 107, 116, 122, 126, 128, 129, 133, 139, 148, 159, 173, 189, 208]
            else:
                Available_Colors = [25, 47, 66, 82, 96, 107, 116, 122, 126, 128, 129, 133, 139, 148, 159, 173, 189, 208, 229]


            keys_list = []
            values_list = []
            
            if (len(Available_Colors) > 1):
                Value_Index = 0
                #we need to figure out the difference between the two values so we
                #know when to switch to the other color
                
                for value in range(256):
                    keys_list.append(value)
                    
                    #we check this so we don't try to read past the end of the list
                    if (Value_Index < (len(Available_Colors) - 1)):
                        
                        #check if the value we are at is past the midpoint of the two colors
                        if (value >= (Available_Colors[Value_Index] + (Available_Colors[Value_Index + 1] - Available_Colors[Value_Index]) // 2)):
                            Value_Index += 1
                          
                    values_list.append(Available_Colors[Value_Index])
            else:
                #if the red value is zero all the values are 0
                for value in range(256):
                    keys_list.append(value)
                    values_list.append(0)
                    
            Cached_Submissive_in_Dominant_Set = dict(zip(keys_list, values_list))

            Cached_Submissive_Colors.append(Cached_Submissive_in_Dominant_Set)

        #the keys in this are the red values available in the palette and their values are
        #lists of the closest available green values associated with that red value
        Dominant_Indexed_Submissive_Colors = dict(zip([25, 47, 66, 82, 96, 107, 116, 122, 126, 128, 129, 133, 139, 148, 159, 173, 189, 208, 229],
                                            [Cached_Submissive_Colors[1],Cached_Submissive_Colors[2],
                                             Cached_Submissive_Colors[3],Cached_Submissive_Colors[4],
                                             Cached_Submissive_Colors[5],Cached_Submissive_Colors[6],
                                             Cached_Submissive_Colors[7],Cached_Submissive_Colors[8],
                                             Cached_Submissive_Colors[9],Cached_Submissive_Colors[10],
                                             Cached_Submissive_Colors[11],Cached_Submissive_Colors[12],
                                             Cached_Submissive_Colors[13],Cached_Submissive_Colors[14],
                                             Cached_Submissive_Colors[15],Cached_Submissive_Colors[16],
                                             Cached_Submissive_Colors[17],Cached_Submissive_Colors[18],
                                             Cached_Submissive_Colors[19]
                                             ]
                                            )
                                        )

        
        Cached_Palette_Keys = []
        Cached_Palette_Values = []
        
        Red_Colors = [                                   122, 126, 128, 129, 133,
                                                    116, 122, 126, 128, 129, 133, 139,
                                               107, 116, 122, 126, 128, 129, 133, 139, 148,
                                          96,  107, 116, 122, 126, 128, 129, 133, 139, 148, 159,
                                     82,  96,  107, 116, 122, 126, 128, 129, 133, 139, 148, 159, 173,
                                66,  82,  96,  107, 116, 122, 126, 128, 129, 133, 139, 148, 159, 173, 189,
                           47,  66,  82,  96,  107, 116, 122, 126, 128, 129, 133, 139, 148, 159, 173, 189, 208,
                      25,  47,  66,  82,  96,  107, 116, 122, 126, 128, 129, 133, 139, 148, 159, 173, 189, 208, 229,
                      25,  47,  66,  82,  96,  107, 116, 122, 126, 128, 129, 133, 139, 148, 159, 173, 189, 208, 229,
                      25,  47,  66,  82,  96,  107, 116, 122, 126, 128, 129, 133, 139, 148, 159, 173, 189, 208, 229,
                      25,  47,  66,  82,  96,  107, 116, 122, 126, 128, 129, 133, 139, 148, 159, 173, 189, 208, 229,
                      25,  47,  66,  82,  96,  107, 116, 122, 126, 128, 129, 133, 139, 148, 159, 173, 189, 208, 229,
                           47,  66,  82,  96,  107, 116, 122, 126, 128, 129, 133, 139, 148, 159, 173, 189, 208,
                                66,  82,  96,  107, 116, 122, 126, 128, 129, 133, 139, 148, 159, 173, 189,
                                     82,  96,  107, 116, 122, 126, 128, 129, 133, 139, 148, 159, 173,
                                          96,  107, 116, 122, 126, 128, 129, 133, 139, 148, 159,
                                               107, 116, 122, 126, 128, 129, 133, 139, 148,
                                                    116, 122, 126, 128, 129, 133, 139,
                                                         122, 126, 128, 129, 133,
                      0, -1, -2, -3, -4, -5, -6]

        Green_Colors = [                                    25,  25,  25,  25,  25,
                                                       47,  47,  47,  47,  47,  47,  47,
                                                  66,  66,  66,  66,  66,  66,  66,  66,  66,
                                             82,  82,  82,  82,  82,  82,  82,  82,  82,  82,  82,
                                        96,  96,  96,  96,  96,  96,  96,  96,  96,  96,  96,  96,  96,
                                  107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107,
                             116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116,
                        122, 122, 122, 122, 122, 122, 122, 122, 122, 122, 122, 122, 122, 122, 122, 122, 122, 122, 122,
                        126, 126, 126, 126, 126, 126, 126, 126, 126, 126, 126, 126, 126, 126, 126, 126, 126, 126, 126,
                        128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128,
                        129, 129, 129, 129, 129, 129, 129, 129, 129, 129, 129, 129, 129, 129, 129, 129, 129, 129, 129,
                        133, 133, 133, 133, 133, 133, 133, 133, 133, 133, 133, 133, 133, 133, 133, 133, 133, 133, 133,
                             139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139,
                                  148, 148, 148, 148, 148, 148, 148, 148, 148, 148, 148, 148, 148, 148, 148,
                                       159, 159, 159, 159, 159, 159, 159, 159, 159, 159, 159, 159, 159,
                                            173, 173, 173, 173, 173, 173, 173, 173, 173, 173, 173,
                                                 189, 189, 189, 189, 189, 189, 189, 189, 189,
                                                      208, 208, 208, 208, 208, 208, 208,
                                                           229, 229, 229, 229, 229,
                        0, 0, 0, 0, 0, 0, 0]


        #now we construct the pallet keys
        #these are unique numbers obtained by combining the red and green values
        #in order to get a quick "hash" used to look up which palette index to assign
        for index in range(256):
            #add the new hash to the list of keys
            Cached_Palette_Keys.append((Red_Colors[index]*Hash_Multiplier) + Green_Colors[index])
            Cached_Palette_Values.append(index)

        #the keys in this are a combination of the red and green values and
        #the values are the palette index that that specific combination yields
        Cached_Palette = dict(zip(Cached_Palette_Keys, Cached_Palette_Values))
        
        self.Palette = {0:Cached_Dominant_Colors, 1:Dominant_Indexed_Submissive_Colors, 2:Cached_Palette}
        
        #now lets build the array to convert p8 back to 32 bit
        self.P8_Palette_32Bit = array("B", [])
        self.P8_Palette_32Bit_Packed = array("I", [])
        for Index in range(0, 256):
            if Index <= 248:
                Red = Red_Colors[Index]
                Green = Green_Colors[Index]
                
                Red_abs = abs(Red-128)
                Green_abs = abs(Green-128)
                
                if abs(Red_abs-127) > abs(Green_abs-127):
                    Scaler = 1-((Red_abs/128) * 0.2)
                else:
                    Scaler = 1-((Green_abs/128) * 0.2)
                    
                Blue = int(Scaler*(sqrt(65536-(Red_abs**2 + Green_abs**2) ) ))
                if Blue > 255:
                    self.P8_Palette_32Bit.extend(array("B", [255, Red, Green, 255]))
                    self.P8_Palette_32Bit_Packed.append( (255<<24) + (Red<<16) +
                                                         (Green<<8) + 255)
                else:
                    self.P8_Palette_32Bit.extend(array("B", [255, Red, Green, Blue]))
                    self.P8_Palette_32Bit_Packed.append( (255<<24) + (Red<<16) +
                                                         (Green<<8) + Blue)
                    
            elif Index == 255:
                self.P8_Palette_32Bit.extend(array("B", [0, 128, 128, 255]))
                self.P8_Palette_32Bit_Packed.append( (128<<16) + (128<<8) + 255)
            else:
                self.P8_Palette_32Bit.extend(array("B", [0, 0, 0, 0]))
                self.P8_Palette_32Bit_Packed.append(0)
                

        #stick the palette in a list since that's how it'll
        #need to be referenced by the bitmap convertor
        self.P8_Palette_32Bit = [self.P8_Palette_32Bit]
        self.P8_Palette_32Bit_Packed = [self.P8_Palette_32Bit_Packed]



    ###################################################################################
    """THE BELOW FUNCTIONS ARE FOR CONVERTING AN ENTIRE ARRAY TO OR FROM P8/ARGB/RGB"""
    ###################################################################################


    def ARGB_Array_to_P8_Array_Average_Alpha(self, Unpacked_Pixel_Array):
        Palette_0 = self.Palette[0]
        Palette_1 = self.Palette[1]
        Palette_2 = self.Palette[2]
        Multi = Hash_Multiplier
        
        Indexing_Array = array("B", [0]*(len(Unpacked_Pixel_Array)//4 ))
        
        for i in range(0, len(Indexing_Array)*4, 4):
            if Unpacked_Pixel_Array[i] == 0:
                Indexing_Array[i//4] = 255
            else:
                Source_Red = Unpacked_Pixel_Array[i+1]
                Source_Green = Unpacked_Pixel_Array[i+2]
                
                Green_Color = Palette_0[Source_Green]
                Best_Red_in_Green = Palette_1[Green_Color][Source_Red]
                
                Red_Color = Palette_0[Source_Red]
                Best_Green_in_Red = Palette_1[Red_Color][Source_Green]
                
                Source_Green = Best_Green_in_Red + (Source_Green - Best_Green_in_Red)//2
                Source_Red = Best_Red_in_Green + (Source_Red - Best_Red_in_Green)//2
                
                Red_Color = Palette_0[Source_Red]
                
                Indexing_Array[i] = Palette_2[((Red_Color*Multi) + Palette_1[Red_Color][Source_Green])]

        return(self.P8_Palette_32Bit[0], Indexing_Array)

    

    def ARGB_Array_to_P8_Array_Average(self, Unpacked_Pixel_Array):
        Palette_0 = self.Palette[0]
        Palette_1 = self.Palette[1]
        Palette_2 = self.Palette[2]
        Multi = Hash_Multiplier
        
        Indexing_Array = array("B", [0]*(len(Unpacked_Pixel_Array)//4 ))
        
        for i in range(0, len(Indexing_Array)*4, 4):
            Source_Red = Unpacked_Pixel_Array[i+1]
            Source_Green = Unpacked_Pixel_Array[i+2]
            
            Green_Color = Palette_0[Source_Green]
            Best_Red_in_Green = Palette_1[Green_Color][Source_Red]
            
            Red_Color = Palette_0[Source_Red]
            Best_Green_in_Red = Palette_1[Red_Color][Source_Green]
            
            Source_Green = Best_Green_in_Red + (Source_Green - Best_Green_in_Red)//2
            Source_Red = Best_Red_in_Green + (Source_Red - Best_Red_in_Green)//2
            
            Red_Color = Palette_0[Source_Red]
            
            Indexing_Array[i] = Palette_2[((Red_Color*Multi) + Palette_1[Red_Color][Source_Green])]

        return(self.P8_Palette_32Bit[0], Indexing_Array)

            

    def ARGB_Array_to_P8_Array_Auto_Alpha(self, Unpacked_Pixel_Array):
        Palette_0 = self.Palette[0]
        Palette_1 = self.Palette[1]
        Palette_2 = self.Palette[2]
        Multi = Hash_Multiplier
        
        Indexing_Array = array("B", [0]*(len(Unpacked_Pixel_Array)//4 ))
        
        for i in range(0, len(Unpacked_Pixel_Array), 4):
            if Unpacked_Pixel_Array[i] == 0:
                Indexing_Array[i//4] = 255
            else:
                Red = Unpacked_Pixel_Array[i+1]
                Green = Unpacked_Pixel_Array[i+2]
                
                if abs(Red - 127) > abs(Green - 127):
                    Red = Palette_0[Red]
                    Indexing_Array[i//4] = Palette_2[((Red*Multi) + Palette_1[Red][Green])]
                else:
                    Green = Palette_0[Green]
                    Indexing_Array[i//4] = Palette_2[((Palette_1[Green][Red]*Multi) + Green)]
                    
        return(self.P8_Palette_32Bit[0], Indexing_Array)

            

    def ARGB_Array_to_P8_Array_Auto(self, Unpacked_Pixel_Array):
        Palette_0 = self.Palette[0]
        Palette_1 = self.Palette[1]
        Palette_2 = self.Palette[2]
        Multi = Hash_Multiplier
        
        Indexing_Array = array("B", [0]*(len(Unpacked_Pixel_Array)//4 ))
        
        for i in range(0, len(Unpacked_Pixel_Array), 4):
            Red = Unpacked_Pixel_Array[i+1]
            Green = Unpacked_Pixel_Array[i+2]
            
            if abs(Red - 127) > abs(Green - 127):
                Red = Palette_0[Red]
                Indexing_Array[i//4] = Palette_2[((Red*Multi) + Palette_1[Red][Green])]
            else:
                Green = Palette_0[Green]
                Indexing_Array[i//4] = Palette_2[((Palette_1[Green][Red]*Multi) + Green)]

        return(self.P8_Palette_32Bit[0], Indexing_Array)


def Load_Palette():
    #construct the palette object
    return(P8_Palette_Class())
