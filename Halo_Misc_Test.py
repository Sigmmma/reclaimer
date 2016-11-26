from traceback import format_exc
try:
    from reclaimer.halo.misc.handler import MiscHaloLoader
    
    test = MiscHaloLoader(debug=3, print_test=True, save_test=False,
                          write_as_temp=True, backup=False,
                          defs_path="reclaimer.halo.misc.defs",
                          
                          print_options={'indent':4,
                                         'printout':True, 'precision':3,
                                         'show':['name', 'steptrees', 'type',
                                                 'value', 'offset',# 'size',
                                                 'index', 'flags',
                                                 'filepath', #'unique', 
                                                 'binsize', 'ramsize',
                                                 #'all'
                                                 ] })
    test.prompt_test()
except Exception:
    print(format_exc())
    input()

TT = test.tags['tga']['test32.tga']
TD = TT.tagdata
