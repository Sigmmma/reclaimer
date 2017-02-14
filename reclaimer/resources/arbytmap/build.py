from distutils.core import setup, Extension

setup(name="arbytmap", version="1.0",
    packages=[
        'arbytmap',
        'arbytmap.ext',
        ],
    ext_modules = [
        Extension("arbytmap.ext.arbytmap_ext", ["arbytmap\\src\\arbytmap_ext.c"]),
        Extension("arbytmap.ext.bitmap_io_ext", ["arbytmap\\src\\bitmap_io_ext.c"]),
        Extension("arbytmap.ext.dds_defs_ext", ["arbytmap\\src\\dds_defs_ext.c"]),
        Extension("arbytmap.ext.raw_packer_ext", ["arbytmap\\src\\raw_packer_ext.c"]),
        Extension("arbytmap.ext.raw_unpacker_ext", ["arbytmap\\src\\raw_unpacker_ext.c"]),
        Extension("arbytmap.ext.swizzler_ext", ["arbytmap\\src\\swizzler_ext.c"])
        ]
    )
