from os.path import dirname
from traceback import format_exc
from time import time
This_Dir = dirname(__file__)

try:
    from ReclaimerLib.Halo.HEK.Programs.Tag_Ripper.Tag_Ripper import Tag_Ripper

    Map_Path = (This_Dir+"\\tags\\precipice.map")
    Ripper = Tag_Ripper()
    input('Press Enter to begin ripping tags from:\n'+
          '    %s\n\n' % Map_Path)
        
    start = time()
    Ripper.Rip_Tags(Map_Path)
    
    input('-'*80 + '\n'+
          'Finished ripping tags.\n'+
          'Operation took %s seconds.\n'%(time()-start) +
          '\n'+
          'Press enter to exit.')

except Exception:
    print(format_exc())
    input()
