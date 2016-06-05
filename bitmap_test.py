import os, time
curr_dir = os.path.abspath(os.curdir)
start = time.time()

from traceback import format_exc
try:
    from reclaimer.resources.bitmap_module import bitmap_convertor as bc

    bitmap_test = bc.BitmapManipulator()
    #bitmap_test.set_deep_color_mode(True)
    #for f in sorted(bc.VALID_FORMATS):
    #    bc.print_format(f)
    
    bitmap_test.load_from_file(input_path = curr_dir + "\\data\\Test.tga")
    bitmap_test.load_new_conversion_settings(target_format=bc.FORMAT_R8G8B8)
    bitmap_test.print_info(1,1,1,0,0)
    print('Press "Enter" to continue conversion'); input()
    start = time.time()
    bitmap_test.convert_texture()
    bitmap_test.save_to_file(output_path = curr_dir + "\\data\\Test.dds")
except:
    print(format_exc())

print("Completed in", str(time.time()-start).split('.')[0], "seconds.")
input()
