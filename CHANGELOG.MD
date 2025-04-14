# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.22.0]
### Changed
 - fix safe-mode clipping reflexives/rawdata to wrong sizes
 - fix exception when using recursive extraction on resource maps alone
 - fix sound metadata being extracted from resource map instead of primary map(i.e. warthog engine)
 - fix open sauce deprotection possibly corrupting maps due to incorrect offsets being used
 - fix open sauce animation tags not having extra animation slots recognized and being trimmed on extraction
 - fix bug where sometimes script decompilation could fail to sort scripts by dependencies
 - fix incorrect max reflexive sizes model_animations tag(weapon types, animations, oshek/osv3hek/etc)
 - fix typo in field name in font tag
 - fix lod cutoffs ordering when extracting/compiling models
 - fix local markers being globalized on model compile
 - fix incorrect flag being used when determining if part uses local nodes
 - fix incorrect type flags offset in auxilary_meter in unit_hud_interface
 - fix weapon_collection references not being deprotected to item_collection
 - fix incorrect byteswapping on compressed model vertices
 - fix incorrect tag definitions being used in certain cases when extracting from maps
 - fix incorrect resource maps being used in certain cases when loading custom resource maps
 - fix local markers not being generated for xbox models on extraction
 - fix material_response.otential_response impact velocities not being scaled properly on extraction
 - attempt to fix some HEK+ bugs(weapon zoom levels and animation function enum)
 - attempt to fix old reclaimer bug where lens_flare corona rotation was incorrectly multiplied by pi/360
 - fix map information reported by HaloMap.generate_map_info_string having some wrong magic offsets
 - fix yelo maps not having their globals override selected through yelo tag
 - fix shadowrun prototype grenade count in globals being 2 instead of 5
 - fix audio being shortened when compiling and extracting xbadpcm sounds
 - fix audio sample rate being incorrectly set when extracting to wav
 - fix overlay animations extracting without a valid base pose
 - animation compilation pipeline now supports all H1 engine variants and their tag size limits
 - replace all instances of magic numbers in tag definition variants with desc_variant calls
 - xbox bitmaps now extract unswizzled and with mipmap/cubemap faces swapped for pc(breaks arsenic support)
 - tag definition variant verification enabled by default(oc, mcc, stubbs, etc)
 - general reorganization and cleanup(still lots that could be done though)
 - decompile minified haloscript sources to scenario source files on tag extraction
 - faster cleaning of certain tags on extraction
 - faster, more correct sbsp compressed/uncompressed render/lightmap vertex generation
 - unset blend_shared_normals when extracting models
 - xbox maps now always load with original halo definitions(open sauce is not the default)
 - better detection on whether or not tag path in map is protected
 - improved open sauce definitions by looking over open sauce github
 - improve stubbs definitions with some extra research(i.e. differences in hud interface tags)

### Added
 - partial h3 odst extraction(bitmap extraction for most formats)
 - full mcc support(tag reading/writing, animation/bitmap compilation, etc) except BC7 bitmap preview/compiling
 - full xbox 360 h1 anniversary extraction(except bitmaps/sounds)
 - partial stubbs 64bit map support(just map header reading; no tag parsing)
 - calculate and insert tag crc32 on extraction from maps
 - animation compilation now supports digsite JMA files(pre-retail formats)
 - model compilation now supports digsite JMS files(pre-retail formats)
 - model compilation now supports shader permutations
 - ability to load reclaimer without loading mozzarilla using RECLAIMER_NO_GUI environment variable
 - ability to load reclaimer without loading arbytmap using RECLAIMER_NO_ARBY environment variable
 - support script parameters when decompiling mcc haloscript
 - support for loading a new previewing script syntax data from maps or tags with reclaimer.haloscript.defs.hsc.h1_script_syntax_data_tagdefs
 - add many hidden/map-only fields to tag definitions
 - add calculating many more hidden fields on tag save(including ogg buffer size)
 - proper mcc scoring definitions added to actor_variant, vehicle, and biped tags
 - calculate distance and gain defaults when saving sound tag
 - support 8 magazines in open sauce definitions instead of 2
 - set mcc flag to use xbox multipurpose map order when extracting xbox shader_models
 - include more useful information in HaloMap.generate_map_info_string(shown in refinery)
 - add definition for recorded animation streams(creates possibility to read/edit/create RA's in the future)
 - add definition for fmod sound bank(creates possiblity to decompile/recompile sound banks in the future)
 - add replacement for most audioop functions in anticipation for it being phased out in python 3.13
 - add control over 16bit pcm playback hack in sound compilation pipeline

## [2.11.2]
### Changed
 - Fix bsp extraction bug

## [2.11.1]
### Changed
 - Fix version

## [2.11.0]
### Added
 - Make Halo1YeloMap its own thing
 - Add MCC scoring type to unit definition

### Changed
 - renamed mcc_Actor_type to mcc_scoring_type

## [2.10.0]
### Changed
 - Made some logic optional to get around a Python 3.9 issue with loading tags.

## [2.9.14]
### Changed
 - Fix actor variant tag being read incorrectly.

## [2.9.13]
### Changed
 - Fix max reflexive size logic for non meta tags.

## [2.9.12]
### Changed
 - Fix max reflexive size logic.

## [2.9.11]
### Changed
 - Change SANE_MAX_REFLEXIVE_COUNT from 0x800000 to 0xFFFE
 - Change code that decides what max size to use from finding the minimum between
   max entries for that reflexive and SANE_MAX_REFLEXIVE_COUNT to finding the maximum.

## [2.9.10]
### Changed
 - Add missing "inhibits weapon attack" field in model_collision definition.
 - Add missing "flying" field in biped.
 - Fix burst_return_length being incorrectly marked as seconds instead of world units.
 - Update build config for Python 3.9.

## [2.9.9]
### Changed
 - Updated xbox model struct for invader

## [2.9.8]
### Added
 - Add fix_top_format() to BitmapTag

## [2.9.7]
### Changed
 - Assume that 0 scale values in models are equal to 1.

## [2.9.6]
### Changed
 - Loosened up one of the safeguards for rawdata fields.

## [2.9.5]
### Added
 - Add safegaurds against loading corrupt tags. Fixes various memory usage explosions.

## [2.9.4]
### Changed
 - Fix actor_variant struct being incorrect for open sauce tag set.
 - Remove magic numbers from os\_hek actor\_variant definition to avoid it breaking in the future.

## [2.9.3]
### Changed
 - Add actor type to actor_variant to support MCC scoring.

## [2.9.2]
### Changed
 - Make GbxModel markers local when extracting. (Does not affect Xbox Models)

## [2.9.1]
### Changed
 - Fix animation decompression failing when there is scale data.

## [2.9.0]
### Added
 - util.convert_newlines_to_windows & util.convert_newlines_to_unix.

### Changed
 - Fix some newline conversions breaking.

## [2.8.0]
### Added
 - CRCs of tags are now properly calculated on save. Use the first bit on offset 48 to determine if a tag is edited by reclaimer. (If not using this library.)

### Changed
 - safe_mode: Fix IGNORE_SAFE_MODE flag being retrieved from an incorrect location.
     - safe_mode: Fix bitmaps with permutation counts over 2048 getting pruned.
     - safe_mode: Fix scenario.bipeds getting pruned at counts over 128.
     - safe_mode: Fix scenario.controls getting pruned at counts over 100.
     - safe_mode: Fix scenario.equipments getting pruned at counts over 256.
     - safe_mode: Fix scenario.light_fixtures getting pruned at counts over 500.
     - safe_mode: Fix scenario.machines getting pruned at counts over 400.
     - safe_mode: Fix scenario.object_names getting pruned at counts over 512.
     - safe_mode: Fix scenario.sceneries getting pruned at counts over 2000.
     - safe_mode: Fix scenario.script_string_data getting pruned at sizes over 262144.
     - safe_mode: Fix scenario.script_syntax_data getting pruned at sizes over 380076.
     - safe_mode: Fix scenario.sound_sceneries getting pruned at counts over 256.
     - safe_mode: Fix scenario.vehicles getting pruned at counts over 80.
     - safe_mode: Fix scenario.weapons getting pruned at counts over 128.
     - safe_mode: Fix sound tags with permutation counts over 256 getting pruned.
 - Fix missing license in distributions.

## [2.7.3]
### Changed
 - (Linux) Fix wrong path separators used in C extensions.

## [2.7.2]
### Changed
 - Fix readme potentially breaking setup.

## [2.7.1]
### Changed
 - Fix modules not being properly listed in setup.py

## [2.7.0]
### Added
 - Add large part of the support for Halo 2 .jms files (.ass)
 - Now calculates change color random roll cutoffs into permutation weights.
 - Windows now has prebuilt wheels for the C extensions.

### Changed
 - Fix extraction of node order for Halo 1 model/gbxmodel tags.
 - Fix incorrect vertex normalization on the loading of JMS files.
 - Fix Jms 8200 sometimes having a type error when being parsed.
 - Sped up JMS parsing using regex magic!
 - The model pipeline has a lot of repeated values moved into constants.
 - Update project structure to be installable from source without edits.

## [2.6.1] Hotfix

### Changed
 - Fix some mistakes in the setup.py that were preventing Reclaimer from building and installing.

## [2.6.0] Into the GPLv3
Something that is very important to us is collaboration and the ability to share knowledge. Since this library is just to help mod some games, we've decided that switching to GPLv3 is the right thing to do for us to avoid any future loss of knowledge.

### Added
 - A sound compilation pipeline for turning wave files into Halo 1 sound tags. (Not ready for use by dependents of this library yet.)
 - Add get_node_depths member to JmaAnimation. Fixes a bug with animation compilation.
 - Add staticmethod to hek's SbspTag for checking if a point is in front of a plane.
 - Michelle as an author!
 - Miscellaneous docstrings.
 - pathlib Path compatibility.
 - Posix compatibility.
 - Reparsing scenario palettes and model shaders based on the highest used index of all palettes/shaders.
    - This fixes safe-mode deleting palette/shader palettes that are higher than the max allowed HEK values.

### Changed
 - Fix animation count limit being too low because of incorrect comparison.
 - Fix edge case where basic_deprotection does not remove trailing or leading backslashes.
 - Fix halo 2 definitions not properly importing their field widgets due to a change in module location.
 - Fix lens_flare corona_rotation not extracting correctly. They were incorrectly converted to degrees from radians but should have stayed radians.
 - Fix script source files not being correctly extracted if unable to resolve dependency order.
 - Fix script source files not being correctly size bounded when extracting.
 - Fix XboxAdpcm data being extracted with wrong size.
 - get_def_id now checks the file contents to see what tag type a file is.
 - h2's snd_'s flags had "split long sounds into permutations" renamed to "split long sound into permutations".
 - HekHandler's get_def_id now supports Path objects.
 - Remove cases where try-except blocks caught control-c.
 - Update setup.py to reference the Github git instead of bitbucket.
 - **THIS PROJECT IS NOW LICENSED UNDER THE GNU General Public License version 3**

### Removed
 - Remove bytes_to_hex from hek_handler.
 - Remove fps_60_related() as it is deprecated and nothing references it.
 - Remove various member functions from HekHandler: get_tag_hash, make_write_log.
 - **REMOVED SUPPORT FOR VERSIONS OF PYTHON BELOW 3.5**
