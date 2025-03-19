#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#
import math

# converting to a normalized "unit" range of -1 to 1
# one "unit" is a half-revolution around the circle
DEG_TO_UNIT   = 1/180
RAD_TO_UNIT   = 1/math.pi
DEG_TO_RAD    = math.pi/180
RAD_TO_DEG    = 180/math.pi

# MODEL CONSTANTS
UV_EPSILON      = 0.0001
POS_EPSILON     = 0.001 # slightly more than a thousandth of an inch
NORM_EPSILON    = 1/5000 #
WEIGHT_EPSILON  = 1/32768 # compressed weight minimum value

# If a jms file is prefixed with this token it
# cannot be randomly chosen as a permutation
JMS_PERM_CANNOT_BE_RANDOMLY_CHOSEN_TOKEN = "~"

SCALE_INTERNAL_TO_JMS = 100.0
SCALE_INTERNAL_TO_JMA = 100.0

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

# ANIMATION CONSTANTS
JMA_EXTENSIONS = (
    ".jma", ".jmm", ".jmo", ".jmr", ".jmt", ".jmw", ".jmz",
    )

# quats in halo are stored using sint16's, so any change
# in the components less than this should round to zero.
QUAT_EPSILON    = 1/32767
# minimum amounts the position/rotation must
# change for the node to be considered animated
# NOTE: these values were derived by comparing transform flags from
#       tool-compiled tags to ones compiled with mozzarilla
TRANS_EPSILON   = 0.005
SCALE_EPSILON   = 0.000001
DYAW_EPSILON    = 0.00000001

JMA_VER_HALO_1_OLDEST_KNOWN   = 16390
JMA_VER_HALO_1_NODE_NAMES     = 16391
JMA_VER_HALO_1_NODE_HIERARCHY = 16392
JMA_VER_HALO_1_RETAIL         = JMA_VER_HALO_1_NODE_HIERARCHY

# not quite sure where this comes from, but it's the
# minimum amount a node must pivot around y or z for
# the axis considered eligible for limp node physics
LIMP_NODE_MIN_RANGE = 10 * DEG_TO_RAD
LIMP_NODE_CROSS_MIN = 0.8113 * DEG_TO_RAD

# NOTE: these constants were determined through trial and error
COMPRESS_AREA_ERR_LOWER     = 0.01
COMPRESS_AREA_ERR_UPPER     = 4.00
# the width of the X axis when calculating
# curve angles(x is time, y is component value)
COMPRESS_FRAME_WIDTH        = 1/30 # number of x units per frame
# the scaled angle range a single point on the
# curve must be considered a critical point
COMPRESS_ANGLE_DIFF_LOWER   =   6 * DEG_TO_UNIT
COMPRESS_ANGLE_DIFF_UPPER   =  12 * DEG_TO_UNIT
# range of total angle difference there must be
# across the curve to create a critical point
COMPRESS_ANGLE_RANGE_LOWER  =  5 * DEG_TO_UNIT
COMPRESS_ANGLE_RANGE_UPPER  = 15 * DEG_TO_UNIT
# range of minimum angles a point must be for it
# to be considered critical when its concavity
# flips to a sign opposite from the previous one
COMPRESS_ANGLE_FLIP_LOWER   = 1.0 * DEG_TO_UNIT
COMPRESS_ANGLE_FLIP_UPPER   = 2.0 * DEG_TO_UNIT

COMPRESS_QUALITY_MIN        = 0.0
COMPRESS_QUALITY_MAX        = 1.0
COMPRESS_RATIO_GOOD_CUTOFF  = 0.7
# the root node has the biggest effect on all other nodes, so
# we need to ensure its compression quality never goes too low
COMPRESS_QUALITY_MIN_NODE_0 = 0.90

JMA_VER_ALL = frozenset((
    JMA_VER_HALO_1_OLDEST_KNOWN,
    JMA_VER_HALO_1_NODE_NAMES,
    JMA_VER_HALO_1_NODE_HIERARCHY,
    JMA_VER_HALO_1_RETAIL,
    ))

del math # not for export
