import os
from traceback import format_exc

try:
    from reclaimer.halo.hek.programs.mozzarilla.app_window import Mozzarilla

    if __name__ == "__main__":
        main_window = Mozzarilla()
        main_window.mainloop()

except Exception:
    print(format_exc())
    input()
