#!/usr/bin/env python
import sys
from traceback import format_exc
try:
    from setuptools import setup, Extension, Command
except ImportError:
    from distutils.core import setup, Extension, Command
from distutils.command.build_ext import build_ext
from distutils.errors import CCompilerError, DistutilsExecError, \
     DistutilsPlatformError

import reclaimer

is_pypy = hasattr(sys, 'pypy_translation_info')
ext_errors = None
if sys.platform == 'win32':
   ext_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError,
                 IOError, ValueError)

class BuildFailed(Exception):
    pass

class ve_build_ext(build_ext):
    # This class allows C extension building to fail.

    def run(self):
        try:
            build_ext.run(self)
        except DistutilsPlatformError:
            raise BuildFailed()

    def build_extension(self, ext):
        if ext_errors:
            try:
                build_ext.build_extension(self, ext)
            except ext_errors:
                raise BuildFailed()
        else:
            build_ext.build_extension(self, ext)

long_desc = open("README.MD").read()


setup_kwargs = dict(
    name='reclaimer',
    description='A libray of SupyrStruct structures and objects for '
                'games built with the Blam engine',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    version='%s.%s.%s' % reclaimer.__version__,
    url=reclaimer.__website__,
    project_urls={
        #"Documentation": <Need a string entry here>,
        "Source": reclaimer.__website__,
        "Funding": "https://liberapay.com/MEK/",
    },
    author=reclaimer.__author__,
    author_email='MosesBobadilla@gmail.com',
    license='GPLv3',
    packages=[
        'reclaimer',
        'reclaimer.animation',
        'reclaimer.bitmaps',
        'reclaimer.h2',
        'reclaimer.h2.defs',
        'reclaimer.h2.defs.objs',
        'reclaimer.h3',
        'reclaimer.h3.defs',
        'reclaimer.h3.defs.objs',
        'reclaimer.halo_script',
        'reclaimer.hek',
        'reclaimer.hek.defs',
        'reclaimer.hek.defs.objs',
        'reclaimer.meta',
        'reclaimer.meta.gen3_resources',
        'reclaimer.meta.objs',
        'reclaimer.meta.wrappers',
        'reclaimer.meta.wrappers.ext',
        'reclaimer.model',
        'reclaimer.misc',
        'reclaimer.misc.defs',
        'reclaimer.misc.defs.objs',
        'reclaimer.os_hek',
        'reclaimer.os_hek.defs',
        'reclaimer.os_hek.defs.objs',
        'reclaimer.os_v3_hek',
        'reclaimer.os_v3_hek.defs',
        'reclaimer.os_v4_hek',
        'reclaimer.os_v4_hek.defs',
        'reclaimer.physics',
        'reclaimer.sounds',
        'reclaimer.sounds.ext',
        'reclaimer.shadowrun_prototype',
        'reclaimer.shadowrun_prototype.defs',
        'reclaimer.strings',
        'reclaimer.stubbs',
        'reclaimer.stubbs.defs',
        'reclaimer.stubbs.defs.objs',
        'reclaimer.util',
        ],
    ext_modules = [
        Extension("reclaimer.sounds.ext.adpcm_ext",
            sources=["reclaimer/sounds/src/adpcm_ext.c",
                     "reclaimer/sounds/src/adpcm-xq/adpcm-lib.c",]),
        Extension("reclaimer.meta.wrappers.ext.byteswapping_ext",
            sources=["reclaimer/meta/wrappers/src/byteswapping_ext.c"]),
        ],
    package_data={
        'reclaimer': [
            "src/*", "meta/wrappers/src/*",
            "sounds/src/*", "sounds/src/adpcm-xq/*",
            '*.[Tt][Xx][Tt]', '*.MD', '*.h',
            '**/p8_palette_halo',   '**/p8_palette_halo_diff_map',
            '**/p8_palette_stubbs', '**/p8_palette_stubbs_diff_map',
            ]
        },
    platforms=["POSIX", "Windows"],
    keywords=["reclaimer", "halo"],
    install_requires=['supyr_struct', 'binilla', 'arbytmap'],
    requires=['supyr_struct', 'binilla', 'arbytmap'],
    provides=['reclaimer'],
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: C",
        ],
    zip_safe=False,
    cmdclass=dict(build_ext=ve_build_ext)
    )


success = False
kwargs = dict(setup_kwargs)
try:
    setup(**kwargs)
    success = True
except BuildFailed:
    print(format_exc())
    print('*' * 80)
    print("WARNING: The C accelerator modules could not be compiled.\n"
          "Attempting to install without accelerators now.\n"
          "Any errors that occurred are printed above.")
    print('*' * 80)

if not success:
    kwargs.pop('ext_modules')
    setup(**kwargs)
    print("Installation successful, but skipped C modules.")
