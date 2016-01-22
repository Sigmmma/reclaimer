from os.path import splitext
from traceback import format_exc

print("Press enter to begin extracting meter images.")
input()

try:
    from ReclaimerLib.Halo.HEK.Library import Halo_Library
    from supyr_struct import Library, Buffer

    #used for loading all meter tags that can be found
    metr_loader = Halo_Library(Valid_Tag_IDs="metr", Print_Test=False)

    #replace the raw data struct of the meter image with the organized one
    Meter_Image_Struct = metr_loader.Defs['metr'].Structures['Meter_Image']
    metr_loader.Defs['metr'].Tag_Structure[1][14]['CHILD'] = Meter_Image_Struct
    
    tags_dir = metr_loader.Data_Dir
    #library to build tga images
    tga_maker = Library.Library(Valid_Tag_IDs='tga', Tags_Dir=tags_dir,
                                Defs_Path='supyr_struct.Defs')
    
    metr_loader.Index_Tags()
    metr_loader.Load_Tags()
    
    for Meter_Path in metr_loader.Tags['metr']:
        try:
            meter = metr_loader.Tags['metr'][Meter_Path]

            tga_buffer = Buffer.BytearrayBuffer()
            tgaout     = tga_maker.Build_Tag(Cls_ID='tga')
            tgaout.Tag_Path = tags_dir+splitext(Meter_Path)[0]+'.tga'

            meterdata = meter.Tag_Data.Data
            
            head = tgaout.Tag_Data.Header

            head.Image_Type.Format.Data = 2
            head.Width  = meterdata.Meter_Width
            head.Height = meterdata.Meter_Height
            head.BPP = 32
            head.Image_Descriptor.Alpha_Bit_Count    = 8
            head.Image_Descriptor.Screen_Origin.Data = 1

            tgaout.Tag_Data.Pixel_Data = tga_buffer
            tga_buffer.seek(4*head.Width*head.Height)
            tga_buffer.write(b'\x00')

            lines = meterdata.Meter_Data.Data

            for line in lines:
                tga_buffer.seek( (line.X_Pos + line.Y_Pos*head.Width )*4 )
                tga_buffer.write(line.Line_Data)

            tgaout.Write(Temp=False, Int_Test=False, Backup=False)
        except Exception:
            print(format_exc())
            print("Above exception occurred while trying to extract "+
                  "meter image for:\n    %s\n\n"%Meter_Path)

    print("Extraction finished. Hit enter to exit.")
    input()

except Exception:
    print(format_exc())
    input()
