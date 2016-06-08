from traceback import format_exc
try:
    from reclaimer.halo.hek.programs.hek_tag_scanner import *

    scanner = HekTagScanner(debug=5)
    scanner.run_test()
except Exception:
    print(format_exc())
    input()
