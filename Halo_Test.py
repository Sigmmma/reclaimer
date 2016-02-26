import cProfile
from traceback import format_exc
from time import time

try:
    from reclaimer.halo.hek.handler import HaloHandler

    test = HaloHandler(print_test=True, save_test=False, debug=3,
                        write_as_temp=False, backup=False,
                        allow_corrupt=True,
                        valid_tag_ids="antr",
                        print_options={'indent':4,
                                       'printout':True, 'precision':3,
                                       'show':['name', 'children', 'field',
                                               'value',# 'size', 'offset', 
                                               'index',# 'flags', 'py_id',
                                               'tagpath', #'unique', 'py_type',
                                               'binsize', 'ramsize'] })
    test.run_test()
    #cProfile.run('test.run_test()')
    #input()

except:
    print(format_exc())
    input()
