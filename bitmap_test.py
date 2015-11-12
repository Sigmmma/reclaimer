import os, time
Curr_Dir = os.path.abspath(os.curdir)
start = time.time()

from traceback import format_exc
try:
    from ReclaimerLib.resources.Bitmap_Module import Bitmap_Convertor as BC

    Bitmap_Test = BC.Bitmap_Manipulator()
    #Bitmap_Test.Set_Deep_Color_Mode(True)
    #for Format in sorted(BC.VALID_FORMATS):
    #    BC.Print_Format(Format)
    
    Bitmap_Test.Load_from_File(Input_Path = Curr_Dir + "\\data\\Test.dds")
    Bitmap_Test.Load_New_Conversion_Settings(Target_Format=BC.FORMAT_R8G8B8)
    Bitmap_Test.Print_Info(1,1,1,0,0)
    print('Press "Enter" to continue conversion'); input()
    Bitmap_Test.Convert_Texture()
    Bitmap_Test.Save_to_File(Output_Path = Curr_Dir + "\\data\\Test.tga")
except:
    print(format_exc())

print("Completed in", str(time.time()-start).split('.')[0], "seconds.")
input()
