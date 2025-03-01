import math

# converting to a normalized "unit" range of -1 to 1
# one "unit" is a half-revolution around the circle
DEG_TO_UNIT   = 1/180
RAD_TO_UNIT   = 1/math.pi
DEG_TO_RAD    = math.pi/180
RAD_TO_DEG    = 180/math.pi

SCALE_INTERNAL_TO_JMA = 100.0

ANIMATION_COMPILE_MODE_NEW        = 0
ANIMATION_COMPILE_MODE_PRESERVE   = 1
ANIMATION_COMPILE_MODE_ADDITIVE   = 2

ANIMATION_COMPRESS_MODE_USE_FLAG  = 0
ANIMATION_COMPRESS_MODE_NEVER     = 1
ANIMATION_COMPRESS_MODE_IF_BETTER = 2

PHYSICS_CALC_MODE_GUESS  = 0
PHYSICS_CALC_MODE_ALWAYS = 1
PHYSICS_CALC_MODE_NEVER  = 2

JMA_ANIMATION_EXTENSIONS = (
    ".jma", ".jmm", ".jmo", ".jmr", ".jmt", ".jmw", ".jmz",
    )

JMA_VER_HALO_1_OLDEST_KNOWN   = 16390
JMA_VER_HALO_1_NODE_NAMES     = 16391
JMA_VER_HALO_1_NODE_HIERARCHY = 16392
JMA_VER_HALO_1_RETAIL         = JMA_VER_HALO_1_NODE_HIERARCHY

# quats in halo are stored using sint16's, so any change
# in the components less than this should round to zero.
QUAT_EPSILON  = 1/32767
# minimum amounts the position/rotation must
# change for the node to be considered animated
# NOTE: these values were derived by comparing transform flags from
#       tool-compiled tags to ones compiled with mozzarilla
TRANS_EPSILON = 0.005
SCALE_EPSILON = 0.000001
DYAW_EPSILON  = 0.00000001

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

SHARED_UNIT_ANIMATION_NAMES = frozenset((
    'airborne-dead', 'landing-dead', 'push', 'twist',
    'look', 'talk', 'emotions'
    ))
SHARED_UNIT_WEAPON_ANIMATION_NAMES = frozenset((
    'dive-front', 'dive-back', 'dive-left', 'dive-right', 'airborne',
    'land-soft', 'land-hard', 'throw-grenade', 'berserk',
    'surprise-front', 'surprise-back', 'evade-left', 'evade-right',
    'signal-move', 'signal-attack', 'warn', 'melee', 'celebrate', 'panic',
    'melee-airborne', 'flaming', 'resurrect-front', 'resurrect-back',
    'melee-continuous', 'feeding', 'leap-start', 'leap-airborne', 'leap-melee'
    ))



JMA_VER_ALL = frozenset((
    JMA_VER_HALO_1_OLDEST_KNOWN,
    JMA_VER_HALO_1_NODE_NAMES,
    JMA_VER_HALO_1_NODE_HIERARCHY,
    JMA_VER_HALO_1_RETAIL,
    ))

# some retail tags don't have nodes due to their
# age, so we'll hardcode them here as a fallback.
# the key is a tuple of the node count and checksum
# maps to a tuple for each nod, looking like:
#   (name, first_child, first_sibling, parent)
JMA_RETAIL_NODES = {
    # digsite\weapons\plasma_rifle\01_gs\fp
    (42, 1525243607): (
        ["frame bone24",        2, -1, -1],
        ["frame l upperarm",    3, -1,  0],
        ["frame r upperarm",    4,  1,  0],
        ["frame l forearm",     5, -1,  1],
        ["frame r forearm",     6, -1,  2],
        ["frame l wriste",     12, -1,  3],
        ["frame r wriste",      7, -1,  4],
        ["frame gun",          29, 15,  6],
        ["frame l index low",  18, -1,  5],
        ["frame l middlelow",  19,  8,  5],
        ["frame l pinky low",  20, 11,  5],
        ["frame l ring low",   21,  9,  5],
        ["frame l thumb low",  22, 10,  5],
        ["frame r index low",  23, 17,  6],
        ["frame r middle low", 24, 13,  6],
        ["frame r pinky low",  25, 16,  6],
        ["frame r ring low",   26, 14,  6],
        ["frame r thumb low",  27, -1,  6],
        ["frame l index mid",  30, -1,  8],
        ["frame l middle mid", 31, -1,  9],
        ["frame l pinky mid",  32, -1, 10],
        ["frame l ring mid",   33, -1, 11],
        ["frame l thumb mid",  34, -1, 12],
        ["frame r index mid",  35, -1, 13],
        ["frame r middle mid", 36, -1, 14],
        ["frame r pinky mid",  37, -1, 15],
        ["frame r ring mid",   38, -1, 16],
        ["frame r thumb mid",  39, -1, 17],
        ["frame rod_left",     40, -1,  7],
        ["frame rod_right",    41, 28,  7],
        ["frame l index tip",  -1, -1, 18],
        ["frame l middle tip", -1, -1, 19],
        ["frame l pinky tip",  -1, -1, 20],
        ["frame l ring tip",   -1, -1, 21],
        ["frame l thumb tip",  -1, -1, 22],
        ["frame r index tip",  -1, -1, 23],
        ["frame r middle tip", -1, -1, 24],
        ["frame r pinky tip",  -1, -1, 25],
        ["frame r ring tip",   -1, -1, 26],
        ["frame r thumb tip",  -1, -1, 27],
        ["frame wing_left",    -1, -1, 28],
        ["frame wing_right",   -1, -1, 29],
        ),
    # characters\engineer\engineer
    (25, -256390784): (
        ('frame root',            7, -1, -1),
        ('frame ltop uparm',     11,  3,  0),
        ('frame neck',            9,  6,  0),
        ('frame rtop uparm',     13,  2,  0),
        ('frame sack01',         -1,  5,  0),
        ('frame sack02',         -1,  1,  0),
        ('frame sack03',         -1, -1,  0),
        ('frame sack06',         -1,  8,  0),
        ('frame tail01',         14,  4,  0),
        ('frame head',           -1, -1,  2),
        ('frame lbottom uparm',  19, 16,  8),
        ('frame ltop forarm',    20, -1,  1),
        ('frame rbottom uparm',  21, 10,  8),
        ('frame rtop forarm',    22, -1,  3),
        ('frame sack04',         17, 15,  8),
        ('frame sack05',         18, 12,  8),
        ('frame tail02',         -1, -1,  8),
        ('frame box01',          -1, -1, 14),
        ('frame box02',          -1, -1, 15),
        ('frame lbottom forarm', 23, -1, 10),
        ('frame ltop hand',      -1, -1, 11),
        ('frame rbottom foarm',  24, -1, 12),
        ('frame rtop hand',      -1, -1, 13),
        ('frame lbottom hand',   -1, -1, 19),
        ('frame rbottom hand',   -1, -1, 21),
        ),
    # levels\a10\devices\doors\door airlock\door airlock
    (4, -921384993): (
        ("frame door airlock", 2, -1, -1),
        ("frame in bottom",   -1, -1,  0),
        ("frame in top",      -1,  3,  0),
        ("frame top",         -1,  1,  0),
        ),
    # levels\a10\devices\doors\door cryo chamber\door cryo chamber
    (3, -2130918511): (
        ("frame door cryo",    1, -1, -1),
        ("frame door cryo l", -1,  2,  0),
        ("frame door cryo r", -1, -1,  0),
        ),
    # levels\a10\devices\doors\door jeff tube\door jeff tube
    (3, 303126628): (
        ("frame door jeff tube", 2, -1, -1),
        ("frame door l",        -1, -1,  0),
        ("frame door r",        -1,  1,  0),
        ),
    # levels\a10\devices\doors\door small\door small
    # levels\a10\devices\doors\door small no glass\door small no glass
    (3, -1054070559): (
        ("frame door small", 2, -1, -1),
        ("frame in bottom", -1, -1,  0),
        ("frame in top",    -1,  1,  0),
        ),
    # levels\a30\devices\beam emitter\beam emitter
    (2, -1073502840): (
        ("frame root",  1, -1, -1),
        ("frame beam", -1, -1,  0),
        ),
    # levels\a30\devices\torpedo_bridge\torpedo_bridge
    (9, 893764757): (
        ("frame root",           1, -1, -1),
        ("frame bridgeaback",    5,  2,  0),
        ("frame bridgeafront",   6,  3,  0),
        ("frame bridgebback",    7,  4,  0),
        ("frame bridgebfront",   8, -1,  0),
        ("frame emitteraback",  -1, -1,  1),
        ("frame emitterafront", -1, -1,  2),
        ("frame emitterbback",  -1, -1,  3),
        ("frame emitterbfront", -1, -1,  4),
        ),
    # levels\a50\devices\mustering_door\mustering_door
    (3, 16992281): (
        ("frame door root",   1, -1, -1),
        ("frame left door",  -1,  2,  0),
        ("frame right door", -1, -1,  0),
        ),
    # levels\b30\devices\interior tech objects\holo control equipment\holo control equipment
    (5, -1411630910): (
        ("frame root",             2, -1, -1),
        ("frame holo circle bot", -1,  3,  0),
        ("frame holo circle top", -1,  1,  0),
        ("frame holo equip bot",  -1,  4,  0),
        ("frame holo equip top",  -1, -1,  0),
        ),
    # levels\b30\devices\interior tech objects\holo control room display\holo control room display
    (21, -1377126976): (
        ("frame root",            1, -1, 0),
        ("frame hologramb30",     5, -1, 0),
        ("frame big marker01",   -1, -1, 1),
        ("frame big marker02",   -1,  2, 1),
        ("frame big marker03",   -1,  3, 1),
        ("frame sentinel01",     -1, 20, 1),
        ("frame small marker01", -1,  4, 1),
        ("frame small marker02", -1,  6, 1),
        ("frame small marker03", -1,  7, 1),
        ("frame small marker04", -1,  8, 1),
        ("frame small marker05", -1,  9, 1),
        ("frame small marker06", -1, 10, 1),
        ("frame small marker07", -1, 11, 1),
        ("frame small marker08", -1, 12, 1),
        ("frame small marker09", -1, 13, 1),
        ("frame small marker10", -1, 14, 1),
        ("frame small marker11", -1, 15, 1),
        ("frame small marker12", -1, 16, 1),
        ("frame small marker13", -1, 17, 1),
        ("frame small marker14", -1, 18, 1),
        ("frame small marker15", -1, 19, 1),
        ),
    # levels\b30\devices\interior tech objects\holo panel\holo panel
    (2, 265626): (
        ("frame root",   1, -1, -1),
        ("frame rotor", -1, -1,  0),
        ),
    # levels\c10\devices\bridge\bridge
    (5, -802003263): (
        ("frame root",      2, -1, -1),
        ("framen_big01",    3, -1,  0),
        ("frames_big01",    4,  1,  0),
        ("framen_small01", -1, -1,  1),
        ("frames_small01", -1, -1,  2),
        ),
    # levels\c20\devices\door_large\door_large
    (3, 743432): (
        ("frame root",    2, -1, -1),
        ("frame door l", -1, -1,  0),
        ("frame door r", -1,  1,  0),
        ),
    # levels\c20\devices\holo control\holo control
    (2, 1074060612): (
        ("frame root",    1, -1, -1),
        ("frame rotate", -1, -1,  0),
        ),
    # levels\c20\devices\holo radial control\holo radial control
    (8, 1141351629): (
        ("frame root",      4, -1, -1),
        ("frame rotate01", -1, -1,  0),
        ("frame rotate02", -1,  1,  0),
        ("frame rotate03", -1,  2,  0),
        ("frame rotate04", -1,  5,  0),
        ("frame rotate05", -1,  6,  0),
        ("frame rotate06", -1,  7,  0),
        ("frame rotate07", -1,  3,  0),
        ),
    # levels\c20\devices\holo tri control\holo tri control
    (6, 16583471): (
        ("frame root",      1, -1, -1),
        ("frame rotate01", -1,  5,  0),
        ("frame rotate02", -1, -1,  0),
        ("frame rotate03", -1,  2,  0),
        ("frame rotate04", -1,  3,  0),
        ("frame rotate05", -1,  4,  0),
        ),
    # levels\test\infinity\devices\beam emitter red\beam emitter red
    (2, -1073502840): (
        ("frame root",  1, -1, -1),
        ("frame beam", -1, -1,  0),
        ),
    # scenery\lightning\lightning
    (8, 830878205): (
        ('frame root',        3, -1, -1),
        ('frame link01',      4,  2,  0),
        ('frame link05',      5, -1,  0),
        ('frame link06',     -1,  1,  0),
        ('frame link02',      7, -1,  1),
        ('frame link04',      6, -1,  2),
        ('frame link end',   -1, -1,  5),
        ('frame link end01', -1, -1,  4),
        ),
    # levels\c10\scenery\c10_bigplant\c10_bigplant
    # scenery\plants\plant_broadleaf_short\plant_broadleaf_short
    (3, 1074195833): (
        ("frame base", 1, -1, -1),
        ("frame mid",  2, -1,  0),
        ("frame end", -1, -1,  1),
        ),
    # scenery\plants\plant_broadleaf_tall\plant_broadleaf_tall
    (7, -1033375598): (
        ("frame trunk",        2, -1, -1),
        ("frame brancha",      4,  3,  0),
        ("frame branchb",      5,  1,  0),
        ("frame branchc",      6, -1,  0),
        ("frame brancha end", -1, -1,  1),
        ("frame branchb end", -1, -1,  2),
        ("frame branchc end", -1, -1,  3),
        ),
    # scenery\trees\tree_leafy_doublewide\tree_leafy_doublewide
    (4, -1849496914): (
        ("frame tree root",     1, -1, -1),
        ("frame tree mid",      2, -1,  0),
        ("frame tree top",      3, -1,  1),
        ("frame tree top end", -1, -1,  2),
        ),
    # scenery\trees\tree_leafy_medium\tree_leafy_medium
    (3, 1089048985): (
        ("frame tree root",    1, -1, -1),
        ("frame tree mid",     2, -1,  0),
        ("frame tree topend", -1, -1,  1),
        ),
    # scenery\trees\tree_pine\tree_pine
    (2, -2147257918): (
        ("frame root", 1, -1, -1),
        ("frame mid", -1, -1,  0),
        ),
    # scenery\trees\tree_pine_snow\tree_pine_snow
    # scenery\trees\tree_pine_tall\tree_pine_tall
    (4, -804395985): (
        ("frame root", 1, -1, -1),
        ("frame mid",  2, -1,  0),
        ("frame top",  3, -1,  1),
        ("frame end", -1, -1,  2),
        ),
    # vehicles\warthog
    (18, -114204588) : (
        ('frame hull',                   1,  -1,  -1),
        ('frame gun mount base',         7,   6,   0),
        ('frame left back suspension',   9,  -1,   0),
        ('frame left front suspension',  10,  4,   0),
        ('frame right back suspension',  11,  2,   0),
        ('frame right front suspension', 12,  3,   0),
        ('frame steering wheel',         -1,  5,   0),
        ('frame chain',                  -1,  8,   1),
        ('frame gun',                    13, -1,   1),
        ('frame left back engine',       14, -1,   2),
        ('frame left front engine',      15, -1,   3),
        ('frame right back engine',      16, -1,   4),
        ('frame right front engine',     17, -1,   5),
        ('frame barrels',                -1, -1,   8),
        ('frame left back tire',         -1, -1,   9),
        ('frame left front tire',        -1, -1,  10),
        ('frame right back tire',        -1, -1,  11),
        ('frame right front tire',       -1, -1,  12),
        ),
    # vehicles\ghost
    (5, -1063303411): (
        ("frame hull",        4, -1, -1),
        ("frame guns",       -1, -1,  0),
        ("frame left flap",  -1,  1,  0),
        ("frame right flap", -1,  2,  0),
        ("frame seat",       -1,  3,  0),
        )
    }

# not for export
del math
