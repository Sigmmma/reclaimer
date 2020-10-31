try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

import reclaimer

long_desc = ""
try:
    long_desc = open("README.MD").read()
except Exception:
    print("Couldn't read readme.")


setup(
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
        'reclaimer.model.jms',
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
            'LICENSE',
            ]
        },
    platforms=["POSIX", "Windows"],
    keywords=["reclaimer", "halo"],
    install_requires=['supyr_struct>=1.5.0', 'binilla', 'arbytmap'],
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
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: C",
        ],
    zip_safe=False,
    )
