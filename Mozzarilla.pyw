import os

from datetime import datetime
from traceback import format_exc

try:
    from reclaimer.halo.hek.programs.mozzarilla.app_window import Mozzarilla
    if __name__ == "__main__":
        main_window = Mozzarilla(debug=3)
        main_window.mainloop()
    
except Exception:
    exception = format_exc()
    try:
        main_window.log_file.write('\n' + exception)
    except Exception:
        try:
            with open('startup_crash.log', 'a+') as cfile:
                time = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
                cfile.write("\n%s%s%s\n" % ("-"*30, time, "-"*(50-len(time))))
                cfile.write(time + format_exc())
        except Exception:
            pass
    print(format_exc())
    input()
