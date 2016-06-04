from traceback import format_exc
try:
    from reclaimer.halo.hek.programs.hek_tag_scanner import *

    scanner = HekTagScanner()
    scanner.run_test()
except Exception:
    print(format_exc())
    input()
