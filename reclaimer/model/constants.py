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

HALO_1_MAX_MARKERS_PER_PERM = 32


# If a jms file is prefixed with this token it
# cannot be randomly chosen as a permutation
JMS_PERM_CANNOT_BE_RANDOMLY_CHOSEN_TOKEN = "~"

SCALE_INTERNAL_TO_JMS = 100.0

JMS_VER_HALO_1_OLDEST_KNOWN  = 8197
JMS_VER_HALO_1_TRI_REGIONS   = 8198
JMS_VER_HALO_1_3D_UVWS       = 8199
JMS_VER_HALO_1_MARKER_RADIUS = 8200
JMS_VER_HALO_1_RETAIL        = JMS_VER_HALO_1_MARKER_RADIUS
JMS_VER_HALO_2_RETAIL        = 8210

JMS_VER_ALL = frozenset((
    JMS_VER_HALO_1_OLDEST_KNOWN,
    JMS_VER_HALO_1_TRI_REGIONS,
    JMS_VER_HALO_1_3D_UVWS,
    JMS_VER_HALO_1_MARKER_RADIUS,
    JMS_VER_HALO_1_RETAIL,
    JMS_VER_HALO_2_RETAIL,
    ))