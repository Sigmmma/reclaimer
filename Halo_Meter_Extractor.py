from os.path import splitext
from traceback import format_exc

try:
    from reclaimer.halo.hek.library import HaloLibrary
    from supyr_struct import library, buffer

    #used for loading all meter tags that can be found
    metr_loader = HaloLibrary(valid_tag_ids="metr", print_test=False)

    #replace the raw data struct of the meter image with the organized one
    Meter_Image_Struct = metr_loader.defs['metr'].descriptors['Meter_Image']
    metr_loader.defs['metr'].descriptor[1][14]['CHILD'] = Meter_Image_Struct
    
    tagsdir = metr_loader.datadir
    #library to build tga images
    tga_maker = library.Library(valid_tag_ids='tga', tagsdir=tagsdir,
                                defs_path='supyr_struct.defs')
    
    print("Press enter to begin extracting meter images.")
    input()

    metr_loader.index_tags()
    metr_loader.load_tags()
    
    tga_buffer = buffer.BytearrayBuffer()
    
    for Meter_Path in metr_loader.tags['metr']:
        try:
            print("Extracting '%s'..."%Meter_Path)
            #clear the buffer
            del tga_buffer[:]
            tga_buffer.seek(0)
            
            meter = metr_loader.tags['metr'][Meter_Path]

            tgaout         = tga_maker.build_tag(tag_id='tga')
            tgaout.tagpath = tagsdir+splitext(Meter_Path)[0]+'.tga'

            meterdata = meter.tagdata.Data
            
            head = tgaout.tagdata.Header

            head.Image_Type.Format.data = 2
            head.Width  = meterdata.Meter_Width
            head.Height = meterdata.Meter_Height
            head.BPP = 32
            head.Image_Descriptor.Alpha_Bit_Count    = 8
            head.Image_Descriptor.Screen_Origin.data = 1

            tgaout.tagdata.Pixel_Data = tga_buffer
            #write a solid red color to the image for the background
            tga_buffer.write(b'\x00\x00\xff\x00'*head.Width*head.Height)

            lines = meterdata.Meter_Data.Data

            #write each of the lines to the appropriate location
            for line in lines:
                tga_buffer.seek( (line.X_Pos + line.Y_Pos*head.Width )*4 )
                tga_buffer.write(line.Line_Data)

            tgaout.write(temp=False, int_test=False, backup=False)
        except Exception:
            print(format_exc())
            print("Above exception occurred while trying to extract "+
                  "meter image for:\n    %s\n\n"%Meter_Path)

    input("\nExtraction finished. Hit enter to exit.")

except Exception:
    print(format_exc())
    input()
