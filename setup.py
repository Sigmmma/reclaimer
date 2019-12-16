#!/usr/bin/env python
import sys
from os.path import dirname, join
from traceback import format_exc
try:
    from setuptools import setup, Extension, Command
except ImportError:
    from distutils.core import setup, Extension, Command
from distutils.command.build_ext import build_ext
from distutils.errors import CCompilerError, DistutilsExecError, \
     DistutilsPlatformError

curr_dir = dirname(__file__)

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

try:
    try:
        long_desc = open(join(curr_dir, "readme.rst")).read()
    except Exception:
        long_desc = "Since PyPI refuses to let me upload due to my readme being Markdown, I wont be using a readme."
        #long_desc = open(join(curr_dir, "readme.md")).read()
except Exception:
    long_desc = 'Could not read long description from readme.'


setup_kwargs = dict(
    name='reclaimer',
    description='A libray of SupyrStruct structures and objects for '
        'games built with the Blam engine',
    long_description=long_desc,
    version='%s.%s.%s' % reclaimer.__version__,
    url='https://bitbucket.org/Moses_of_Egypt/reclaimer',
    author='Devin Bobadilla',
    author_email='MosesBobadilla@gmail.com',
    license='MIT',
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
        Extension("reclaimer.sounds.ext.adpcm_ext", ["reclaimer/sounds/src/adpcm_ext.c"]),
        ],
    package_data={
        '': ['*.txt', '*.md', '*.rst',
             '**/p8_palette_halo',   '**/p8_palette_halo_diff_map',
             '**/p8_palette_stubbs', '**/p8_palette_stubbs_diff_map',
             '**/sounds/src/*'],
        },
    platforms=["POSIX", "Windows"],
    keywords="reclaimer, halo",
    # arbytmap can be removed from the dependencies if you cannot install
    # it for some reason, though it will prevent certain things from working.
    install_requires=['supyr_struct', 'binilla', 'arbytmap'],
    requires=['supyr_struct', 'binilla', 'arbytmap'],
    provides=['reclaimer'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        ],
    zip_safe=False,
    cmdclass=dict(build_ext=ve_build_ext)
    )


success = False
kwargs = dict(setup_kwargs)
if not is_pypy:
    try:
        setup(**kwargs)
        success = True
    except BuildFailed:
        print(format_exc())
        print('*' * 80)
        print("WARNING: The C accelerator modules could not be compiled.\n" +
              "Attempting to install without accelerators now.\n" +
              "Any errors that occurred are printed above.")
        print('*' * 80)

if not success:
    kwargs.pop('ext_modules')
    setup(**kwargs)
    print("Installation successful.")
