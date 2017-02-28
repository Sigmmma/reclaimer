#!/usr/bin/env python
from os.path import dirname, join
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

curr_dir = dirname(__file__)

#               YYYY.MM.DD
release_date = "2017.02.28"
version = (1, 0, 5)

try:
    try:
        long_desc = open(join(curr_dir, "readme.rst")).read()
    except Exception:
        long_desc = open(join(curr_dir, "readme.md")).read()
except Exception:
    long_desc = 'Could not read long description from readme.'

setup(
    name='reclaimer',
    description='A libray of SupyrStruct structures and objects for \
games built with the Blam engine',
    long_description=long_desc,
    version='%s.%s.%s' % version,
    url='https://bitbucket.org/Moses_of_Egypt/reclaimer',
    author='Devin Bobadilla',
    author_email='MosesBobadilla@gmail.com',
    license='MIT',
    packages=[
        'reclaimer',
        'reclaimer.h2ek',
        'reclaimer.h2ek.defs',
        'reclaimer.h2ek.defs.objs',
        'reclaimer.hek',
        'reclaimer.hek.defs',
        'reclaimer.hek.defs.objs',
        'reclaimer.meta',
        'reclaimer.meta.defs',
        'reclaimer.meta.defs.objs',
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
        'reclaimer.stubbs',
        'reclaimer.stubbs.defs',
        'reclaimer.stubbs.defs.objs',
        ],
    package_data={
        '': ['*.txt', '*.md', '*.rst'],
        'reclaimer': [
            'hek/defs/objs/p8.act',
            ]
        },
    platforms=["POSIX", "Windows"],
    keywords="reclaimer, halo",
    install_requires=['supyr_struct'],#, 'arbytmap'],
    requires=['supyr_struct'],#, 'arbytmap'],
    provides=['reclaimer'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        ],
    zip_safe=False,
    )
