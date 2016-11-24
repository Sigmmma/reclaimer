import os
from traceback import format_exc

try:
    from supyr_struct.apps.binilla.app_window import Binilla
    from supyr_struct.apps.handler import Handler

    if __name__ == "__main__":
        main_window = Binilla(
            curr_dir=os.path.abspath(os.curdir).replace('/', '\\'),
            handler=Handler( defs_path='reclaimer.misc.defs'))
        main_window.mainloop()

except Exception:
    print(format_exc())
    input()
