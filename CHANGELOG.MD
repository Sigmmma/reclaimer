# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
