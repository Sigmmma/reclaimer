from traceback import format_exc
try:
    from ReclaimerLib.Halo.HEK.Programs.HEK_Tag_Scanner import *

    Scanner = HEK_Tag_Scanner()
    Scanner.Load_Tags_and_Run()
except Exception:
    print(format_exc())
    input()
