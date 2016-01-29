from traceback import format_exc
try:
    from reclaimer.halo.hek.programs.hek_tag_scanner import *

    scanner = HekTagScanner()
    scanner.load_tags_and_run()
except Exception:
    print(format_exc())
    input()
