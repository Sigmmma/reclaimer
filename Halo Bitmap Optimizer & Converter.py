from traceback import format_exc
try:
    from ReclaimerLib.Halo.HEK.Programs.Bitmap_Optimizer_and_Converter import *

    Bitmap_Convertor = Bitmap_Converter(Debug = 0)

except:
    print(format_exc())
    input()
