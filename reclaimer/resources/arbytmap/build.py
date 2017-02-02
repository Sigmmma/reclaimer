from distutils.core import setup, Extension

setup(name="arbytmap", version="1.0",
    packages=['arbytmap'],
    ext_modules = [
        Extension("arbytmap.ext.arbytmap_ext", ["arbytmap\\ext\\arbytmap_ext.c"]),
        Extension("arbytmap.ext.raw_packer_ext", ["arbytmap\\ext\\raw_packer_ext.c"]), 
        Extension("arbytmap.ext.raw_unpacker_ext", ["arbytmap\\ext\\raw_unpacker_ext.c"]), 
        Extension("arbytmap.ext.swizzler_ext", ["arbytmap\\ext\\swizzler_ext.c"])
        ]
    )
