#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

# There is only 8 spaces allocated for these in the object's gamestate.
# If you have more and it updates the state for those it would write into
# unrelated fields.
HALO_1_MAX_REGIONS = 8

HALO_1_NAME_MAX_LEN = 31

HALO_1_MAX_GEOMETRIES_PER_MODEL = 256

HALO_1_MAX_MATERIALS = 256

HALO_1_MAX_NODES = 64

HALO_1_MAX_MARKERS = 256


# If a jms file is prefixed with this token it
# cannot be randomly chosen as a permutation
JMS_PERM_CANNOT_BE_RANDOMLY_CHOSEN_TOKEN = "~"

SCALE_INTERNAL_TO_JMS = 100.0

JMS_VERSION_HALO_1 = "8200"
JMS_VERSION_HALO_2_8210 = "8210"
