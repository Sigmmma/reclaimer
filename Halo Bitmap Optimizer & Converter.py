from traceback import format_exc
try:
    from reclaimer.halo.hek.programs.bitmap_optimizer_and_converter import *

    converter = BitmapConverter(debug = 5)

except:
    print(format_exc())
    input()
