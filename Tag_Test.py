from traceback import format_exc
try:
    from supyr_struct.test import TagTestHandler
    
    test = TagTestHandler(debug=3, print_test=True, save_test=False,
                          write_as_temp=True, backup=False,
                          valid_def_ids="sote_eep_save",
                          defs_path="reclaimer.misc.defs",
                          
                          print_options={'indent':4,
                                         'printout':True, 'precision':3,
                                         'show':['name', 'children', 'field',
                                                 'value', 'offset',# 'size',
                                                 'index', 'flags',
                                                 'filepath', #'unique', 
                                                 'binsize', 'ramsize',
                                                 #'all'
                                                 ] })
    test.run_test()
except Exception:
    print(format_exc())
    input()

TT = test.tags['tga']['test32.tga']
TD = TT.tagdata
