from traceback import format_exc
try:
    from ReclaimerLib.Halo.HEK.Programs.Chicago_Shader_Rectifier import *

    if __name__ == '__main__':
        Shader_Rectifier = Shader_Rectifier(Target_Tag="schi")
        Shader_Rectifier.Load_Tags_and_Run()
except:
    print(format_exc())
    input()
