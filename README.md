# Reclaimer

## What is this repository for?

* Reclaimer is a library of [supyr_struct](https://bitbucket.org/moses_of_egypt/supyr_struct) structure descriptors and tag definitions for creating and modifying data files for video games utilizing the Blam engine. These descriptors and definitions are currently limited to Halo 1(xbox, custom edition, and the community made "open sauce" variant) with some support for Stubbs the Zombie. There are plans to branch into Halo 2, though for now the "he2k" sub-module is just a placeholder. Some of the tag definitions have an accompanying object class with methods for manipulating the tag(recalculating inertial matrices in physics tags for example).

## Installing

First install any version of Python 3(The newest version is recommended).

There are two ways to install reclaimer from this point:

*    Open a command prompt and execute ```pip install reclaimer```

or

*    Extract a copy of the repository into a directory titled "reclaimer".
*    Move the file "setup.py" into the directory containing "reclaimer".
*    Open a command prompt, navigate to the directory containing setup.py, and execute:```python setup.py install```
*    During install, python should try to download and install [supyr_struct](https://bitbucket.org/moses_of_egypt/supyr_struct). If it fails to, you must install that as well.

Once the install finishes, reclaimer should be ready to use.

There are currently no test cases, but you should be able to directly import any tag definition from the python interpreter, build it, give it a filepath, and serialize it as shown below:
```
>>> from reclaimer.hek.defs.pphy import pphy_def
>>> asdf = pphy_def.build()
>>> print(asdf)
[ Container, entries:2, pphy
    [ Struct, size:64, entries:6, blam_header
        [ UEnum32, offset:36, size:4, tag_class, 1886414969
             point_physics ]
        [ UInt32, offset:40, size:4, base_address, 1299151482 ]
        [ UInt32, offset:44, size:4, header_size, 64 ]
        [ UInt16, offset:56, size:2, version, 1 ]
        [ UInt16, offset:58, size:2, unknown, 255 ]
        [ UEnum32, offset:60, size:4, engine_id, 1651269997
             halo_1 ]
        ]
    [ Struct, size:64, entries:9, tagdata
        [ Bool32, offset:0, size:4, flags, 0
            ]
        [ FlFloat, offset:4, size:4, wind_coefficient, 0.0 ]
        [ FlFloat, offset:8, size:4, wind_sine_modifier, 0.0 ]
        [ FlFloat, offset:12, size:4, z_translation_rate, 0.0 ]
        [ Float, offset:32, size:4, density, 0.0 ]
        [ Float, offset:36, size:4, air_friction, 0.0 ]
        [ Float, offset:40, size:4, water_friction, 0.0 ]
        [ Float, offset:44, size:4, surface_friction, 0.0 ]
        [ Float, offset:48, size:4, elasticity, 0.0 ]
        ]
    ]
>>> asdf.data.serialize()
bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00pphyMozz\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\xffblam
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00
\x00\x00\x00\x00\x00\x00\x00\x00')
```

## Who do I talk to?

* Devin Bobadilla (Author of reclaimer) mosesbobadilla@gmail.com