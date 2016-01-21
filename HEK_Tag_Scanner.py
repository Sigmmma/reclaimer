from traceback import format_exc
try:
    from ReclaimerLib.Halo.HEK.Programs.HEK_Tag_Scanner import *

    if __name__ == '__main__':
        Scanner = HEK_Tag_Scanner()
        Scanner.Load_Tags_and_Run()
except Exception:
    print(format_exc())
    input()
