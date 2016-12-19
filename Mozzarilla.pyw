import os
from traceback import format_exc

try:
    from reclaimer.halo.hek.programs.mozzarilla.app_window import Mozzarilla

    if __name__ == "__main__":
        main_window = Mozzarilla(debug=3)
        main_window.mainloop()

except Exception:
    exception = format_exc()
    print(exception)
    try:
        main_window.log_file.write('\n' + exception)
    except Exception:
        pass
    input()
