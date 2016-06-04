from traceback import format_exc
try:
    from reclaimer.halo.hek.programs.chicago_shader_rectifier import *

    rectifier = ShaderRectifier()#target_id="schi")
    rectifier.run_test()
except Exception:
    print(format_exc())
    input()
