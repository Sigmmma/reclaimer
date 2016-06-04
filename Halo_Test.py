import cProfile
from traceback import format_exc
from time import time

try:
    from reclaimer.halo.hek.handler import HaloHandler

    test = HaloHandler( print_test=True, save_test=False, debug=3,
                        write_as_temp=True, backup=False,
                        allow_corrupt=True,
                        #valid_def_ids="antr",
                        print_options={'indent':4,
                                       'printout':True, 'precision':3,
                                       'show':['name', 'children', 'field',
                                               'value', 'offset',# 'size', 
                                               'index', 'flags',# 'py_id',
                                               'filepath', #'unique', 'py_type',
                                               'binsize', 'ramsize'] })
    test.prompt_test()
    #cProfile.run('test.prompt_test()')
    #input()

except:
    print(format_exc())
    input()
