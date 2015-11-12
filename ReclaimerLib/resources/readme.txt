This is where things that can operate independently of ReclaimerLib, 
yet are still used by some of the programs, are placed. It is also
where things that don't quite fit in anywhere else are placed.

Example: the bitmap converter is capable of being used in another
program for converting textures as long as it is integrated properly.
The bitmap headers has a series of functions for constructing the
header of different texture file formats when given the proper
arguments.

The "tags" folder located here is where special tags are placed 
which are used by the program for special reasons.