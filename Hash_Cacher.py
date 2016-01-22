from os.path import dirname
from time import time
from traceback import format_exc

This_Dir = dirname(__file__)

try:
    from ReclaimerLib.Halo.HEK.Programs.Tag_Ripper.Hash_Cacher import Hash_Cacher
    
    Cacher = Hash_Cacher()
    
    Cache_Name = 'Halo_1_Default'
    Tags_Dir   = (This_Dir+"\\ReclaimerLib\\Halo\\HEK\\"+
                           "Programs\\Tag_Ripper\\all_original_tags\\")
    Cache_Description = ('All the tags that are used in the original Halo 1 '+
                         'singleplayer, multiplayer, and ui maps.\n'+
                         'This should always be used, and as the base cache.')
    input('Press Enter to begin scanning in:\n'+
          '    %s\n\n' % Tags_Dir)
        
    start = time()
    Cache = Cacher.Build_Hashcache(Cache_Name, Cache_Description, Tags_Dir)
    
    Cache.Print(Printout=True)
    input('-'*80 + '\n'+
          'Finished scanning tags directory.'+
          'Operation took %s seconds.\n'%(time()-start) +
          '\n'+
          'Press enter to exit.')
except Exception:
    print(format_exc())
    input()

raise SystemExit()
