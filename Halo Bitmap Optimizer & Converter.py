from traceback import format_exc
try:
    from reclaimer.halo.hek.programs.hboc.bitmap_optimizer_and_converter import *

    # setting debug to 1 or higher will disable log file creation,
    # and instead make it so it is always printed to the console.
    converter = BitmapConverter(debug = 0)

except:
    print(format_exc())
    input()
