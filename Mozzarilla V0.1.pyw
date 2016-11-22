import os
from traceback import format_exc
from reclaimer.halo.hek.handler import HaloHandler

from supyr_struct.apps.binilla.app_window import Binilla

try:
    if __name__ == "__main__":
        main_window = Binilla(
            curr_dir=os.path.abspath(os.curdir),
            app_name='Mozzarilla', version='0.1',
            handler=HaloHandler())
        main_window.mainloop()

except Exception:
    print(format_exc())
    input()
