from os.path import dirname
from traceback import format_exc
from time import time
Here = dirname(__file__)

try:
    from ReclaimerLib.Halo.META.Library import Map_Loader

    Path = Here+"\\ReclaimerLib\\Halo\\HEK\\Programs\\Tag_Ripper\\resources\\"
    Loader = Map_Loader(Debug=1, Allow_Corrupt=True)
    
    input('Press Enter to begin the resource maps in:\n'+
          '    %s\n\n' % Path)
    
    start = time()
    
    #Sounds  = Loader.Build_Tag(Filepath=Path+'sounds.map',  Cls_ID="resource")
    Bitmaps = Loader.Build_Tag(Filepath=Path+'bitmaps.map', Cls_ID="resource")
    #Strings = Loader.Build_Tag(Filepath=Path+'loc.map',     Cls_ID="resource")

    #Sounds.Print(Printout=True, Show=['Name','Value','Children','Index','Type'])
    Bitmaps.Print(Printout=True, Show=['Name','Value','Children','Index','Type'])
    #Strings.Print(Printout=True, Show=['Name','Value','Children','Index','Type'])
        
    input('-'*80 + '\n'+
          'Finished.\n'+
          'Operation took %s seconds.\n'%(time()-start) +
          '\n'+
          'Press enter to exit.')

except Exception:
    print(format_exc())
    input()
