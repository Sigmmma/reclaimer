import cProfile
from traceback import format_exc
from copy import copy
try:
    from reclaimer.gdl.handler import GdlHandler

    valid_id='rom'
   
    test = GdlHandler(debug=3, allow_corrupt=True,
                       print_test=True, save_test=False, int_test=False,
                       write_as_temp=True, backup=False,
                       #valid_def_ids=valid_id,
                       print_options={'indent':4,
                                      'printout':True, 'precision':3,
                                      'show':['name', 'children', 'field',
                                              'value',#'offset',# 'py_id',
                                              'index', 'size',#'flags', # 'unique',
                                              'filepath', 'binsize','ramsize',
                                              'trueonly', 'raw'
                                              #'all'
                                              ] })
    test.prompt_test()
    #cProfile.run('test.prompt_test()')
    #objs = test.tags.get(valid_id)
    input()
except Exception:
    print(format_exc())
    input()
