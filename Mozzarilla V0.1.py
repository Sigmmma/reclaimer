import os
from traceback import format_exc

from supyr_struct.apps.binilla import Binilla

try:
    if __name__ == "__main__":
        main_window = Binilla(curr_dir = os.path.abspath(os.curdir))
        main_window.mainloop()

except Exception:
    print(format_exc())
    input()
