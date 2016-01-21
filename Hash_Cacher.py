from traceback import format_exc
try:
    from ReclaimerLib.Halo.HEK.Programs.Tag_Ripper.Tag_Hash_Cacher import Hash_Cacher
    
    Cacher = Hash_Cacher()
    Cacher.Load_Tags_and_Run()
except Exception:
    print(format_exc())
    input()
