from os.path import splitext
from traceback import format_exc

try:
    from reclaimer.halo.hek.handler import HaloHandler
    from supyr_struct import handler, buffer

    #used for loading all meter tags that can be found
    metr_loader = HaloHandler(valid_def_ids="metr", print_test=False)

    metrdef = metr_loader.defs['metr']

    #replace the raw data struct of the meter image with the organized one
    Meter_Image_Struct = metrdef.subdefs['Meter_Image'].descriptor
    #override the immutability of the frozendict
    dict.__setitem__(metrdef.descriptor[1][14], 'CHILD', Meter_Image_Struct)
    
    tagsdir = metr_loader.datadir
    #handler to build tga images
    tga_maker = handler.Handler(valid_def_ids='tga', tagsdir=tagsdir,
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

            tgaout         = tga_maker.build_tag(def_id='tga')
            tgaout.tagpath = tagsdir+splitext(Meter_Path)[0]+'.tga'

            meterdata = meter.tagdata.Data
            
            head = tgaout.tagdata.header

            head.image_type.format.set_data("unmapped_rgb")
            head.width  = meterdata.Meter_Width
            head.height = meterdata.Meter_Height
            head.bpp = 32
            head.image_descriptor.alpha_bit_count    = 8
            head.image_descriptor.screen_origin.set_data("upper_left")

            tgaout.tagdata.pixel_data = tga_buffer
            #write a solid red color to the image for the background
            tga_buffer.write(b'\x00\x00\xff\x00'*head.width*head.height)

            lines = meterdata.Meter_Data.Data

            #write each of the lines to the appropriate location
            for line in lines:
                tga_buffer.seek( (line.X_Pos + line.Y_Pos*head.width )*4 )
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
