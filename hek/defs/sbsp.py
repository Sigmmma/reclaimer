from .coll import *
from .objs.tag import HekTag
from supyr_struct.defs.block_def import BlockDef

# the order is an array of vertices first, then an array of lightmap vertices.
# 
uncompressed_vertex = QStruct("uncompressed vertex",
    Float('position x'), Float('position y'), Float('position z'),
    Float('normal i'),   Float('normal j'),   Float('normal k'),
    Float('binormal i'), Float('binormal j'), Float('binormal k'),
    Float('tangent i'),  Float('tangent j'),  Float('tangent k'),

    Float('tex coord u'), Float('tex coord v'),
    SIZE=56
    )

compressed_vertex = QStruct("compressed vertex",
    Float('position x'), Float('position y'), Float('position z'),
    UInt32('normal'),
    UInt32('binormal'),
    UInt32('tangent'),

    Float('tex coord u'), Float('tex coord v'),
    SIZE=32
    )

uncompressed_lightmap_vertex = QStruct("uncompressed lightmap vertex",
    Float('normal i'),   Float('normal j'),   Float('normal k'),
    Float('u'), Float('v'),
    SIZE=20
    )

compressed_lightmap_vertex = QStruct("compressed lightmap vertex",
    UInt32('normal'),
    SInt16('u', UNIT_SCALE=1/32767, MIN=-32767, WIDGET_WIDTH=10),
    SInt16('v', UNIT_SCALE=1/32767, MIN=-32767, WIDGET_WIDTH=10),
    SIZE=8
    )

plane = QStruct("plane",
    Float("i", MIN=0.0, MAX=1.0),
    Float("j", MIN=0.0, MAX=1.0),
    Float("k", MIN=0.0, MAX=1.0),
    Float("d"),
    SIZE=16, ORIENT='h'
    )

vertex = QStruct("vertex", INCLUDE=xyz_float, SIZE=12)

collision_material = Struct("collision material",
    dependency("shader", valid_shaders),
    FlUInt32("unknown", VISIBLE=False),
    SIZE=20
    )

collision_bsp = Struct("collision bsp", INCLUDE=permutation_bsp)

node = Struct("node",
    # these dont get byteswapped going from meta to tag
    BytesRaw("unknown", SIZE=6),
    SIZE=6
    )

leaf = QStruct("leaf",
    # these unknowns are in the tag and are preserved in the meta
    FlSInt16("unknown0", VISIBLE=False),
    FlSInt16("unknown1", VISIBLE=False),
    FlSInt16("unknown2", VISIBLE=False),
    FlSInt16("unknown3", VISIBLE=False),

    SInt16("cluster"),
    SInt16("surface reference count"),
    SInt32("surface references"),
    SIZE=16,
    )

leaf_surface = QStruct("leaf surface",
    SInt32("surface"),
    SInt32("node"),
    SIZE=8, ORIENT='h'
    )

surface = QStruct("surface",
    SInt16("a"),
    SInt16("b"),
    SInt16("c"),
    SIZE=6, ORIENT='h'
    )

material = Struct("material",
    dependency("shader", valid_shaders),
    SInt16("shader permutation"),
    Bool16("flags",
        "coplanar",
        "fog plane",
        ),
    SInt32("surfaces", EDITABLE=False),
    SInt32("surface count", EDITABLE=False),
    QStruct("centroid", INCLUDE=xyz_float),
    QStruct("ambient color", INCLUDE=rgb_float),
    SInt16("distant light count"),
    Pad(2),

    QStruct("distant light 0 color", INCLUDE=rgb_float),
    QStruct("distant light 0 direction", INCLUDE=ijk_float),
    QStruct("distant light 1 color", INCLUDE=rgb_float),
    QStruct("distant light 1 direction", INCLUDE=ijk_float),
    Pad(12),

    QStruct("reflection tint", INCLUDE=argb_float),
    QStruct("shadow vector", INCLUDE=ijk_float),
    QStruct("shadow color", INCLUDE=rgb_float),
    QStruct("plane", INCLUDE=plane),
    SInt16("breakable surface", EDITABLE=False),
    Pad(6),

    SInt32("vertices count", EDITABLE=False),
    SInt32("vertices offset", VISIBLE=False),

    FlUInt32("unknown meta offset0", VISIBLE=False),
    FlUInt32("vertices meta offset",
        TOOLTIP=("In xbox maps this is a bspmagic relative pointer that\n"
                 "points to a reflexive. The reflexive contains only a\n"
                 "bspmagic relative pointer to the vertices."),
        VISIBLE=False
        ),
    FlUEnum32("vertex type",  # name is a guess
        ("unknown", 0),
        ("uncompressed", 2),
        ("compressed",   3),
        VISIBLE=False,
        ),
    SInt32("lightmap vertices count", VISIBLE=False),
    SInt32("lightmap vertices offset", VISIBLE=False),

    FlUInt32("unknown meta offset1", VISIBLE=False),
    FlUInt32("lightmap vertices meta offset",
        TOOLTIP=("In xbox maps this is a bspmagic relative pointer that\n"
                 "points to a reflexive. The reflexive contains only a\n"
                 "bspmagic relative pointer to the lightmap vertices."),
        VISIBLE=False
        ),

    rawdata_ref("uncompressed vertices", max_size=4864000),
    rawdata_ref("compressed vertices", max_size=2560000),
    SIZE=256
    )

lightmap = Struct("lightmap",
    SInt16("bitmap index"),
    Pad(18),
    reflexive("materials", material, 2048,
        DYN_NAME_PATH='.shader.filepath'),
    SIZE=32
    )

lens_flare = Struct("lens flare",
    dependency("shader", 'lens'),
    SIZE=16
    )

lens_flare_marker = Struct("lens flare marker",
    QStruct("position", INCLUDE=xyz_float),
    QStruct("direction",
        SInt8('i'), SInt8('j'), SInt8('k'), ORIENT='h'
        ),
    # While guerilla treats this like a signed int, there is no way that it
    # is gonna be able to reference one of the 256 lens flares if its signed
    UInt8('lens flare index'),
    SIZE=16
    )

surface_index = QStruct("surface index",
    SInt32("index"),
    SIZE=4
    )

mirror = Struct("mirror",
    QStruct("plane", INCLUDE=plane),
    # might be padding, might not be
    BytesRaw("unknown", VISIBLE=False, SIZE=20),
    dependency("shader", valid_shaders),
    reflexive("vertices", vertex, 512),
    SIZE=64
    )

portal = QStruct("portal",
    SInt16("portal"),
    SIZE=2
    )

subcluster = Struct("subcluster",
    QStruct('world bounds x', INCLUDE=from_to),
    QStruct('world bounds y', INCLUDE=from_to),
    QStruct('world bounds z', INCLUDE=from_to),
    reflexive("surface indices", surface_index, 128),
    SIZE=36
    )

cluster = Struct("cluster",
    SInt16('sky'),
    SInt16('fog'),
    dyn_senum16('background sound',
        DYN_NAME_PATH="tagdata.background_sounds_palette.STEPTREE[DYN_I].name"),
    dyn_senum16('sound environment',
        DYN_NAME_PATH="tagdata.sound_environments_palette." +
        "STEPTREE[DYN_I].name"),
    dyn_senum16('weather',
        DYN_NAME_PATH="tagdata.weather_palettes.STEPTREE[DYN_I].name"),

    # almost certain this is padding
    BytesRaw("unknown", SIZE=30, VISIBLE=False),
    #Pad(30),

    reflexive("predicted resources", predicted_resource, 1024, VISIBLE=False),
    reflexive("subclusters", subcluster, 4096),
    SInt16("first lens flare marker index"),
    SInt16("lens flare marker count"),
    reflexive("surface indices", surface_index, 32768),
    reflexive("mirrors", mirror, 16, DYN_NAME_PATH=".shader.filepath"),
    reflexive("portals", portal, 128),
    SIZE=104
    )

cluster_portal = Struct("cluster portal",
    SInt16("front cluster"),
    SInt16("back cluster"),
    SInt32("plane index"),
    QStruct("centroid", INCLUDE=xyz_float),
    Float("bounding radius"),
    Bool32("flags",
        "ai cant hear through this",
        ),

    # might be padding, might not be
    BytesRaw("unknown", VISIBLE=False, SIZE=24),
    reflexive("vertices", vertex, 128),
    SIZE=64
    )

breakable_surface = Struct("breakable surface",
    QStruct("centroid", INCLUDE=xyz_float),
    Float("radius"),
    SInt32("collision surface index"),
    Pad(28),
    SIZE=48
    )

fog_plane = Struct("fog plane",
    SInt16("front region"),
    Pad(2),
    QStruct("plane", INCLUDE=plane),
    reflexive("vertices", vertex, 4096),
    SIZE=32
    )

fog_region = Struct("fog region",
    Pad(36),
    dyn_senum16("fog palette",
        DYN_NAME_PATH="tagdata.fog_palettes.STEPTREE[DYN_I].name"),
    dyn_senum16("weather palette",
        DYN_NAME_PATH="tagdata.weather_palettes.STEPTREE[DYN_I].name"),
    SIZE=40
    )

fog_palette = Struct("fog palette",
    ascii_str32("name"),
    dependency("fog", "fog "),
    Pad(4),
    ascii_str32("fog scale function"),
    SIZE=136
    )

weather_palette = Struct("weather palette",
    ascii_str32("name"),
    dependency("particle system", "rain"),
    Pad(4),
    ascii_str32("particle system scale function"),

    Pad(44),
    dependency("wind", "wind"),
    QStruct("wind direction", INCLUDE=ijk_float),
    Float("wind magnitude"),
    Pad(4),
    ascii_str32("wind scale function"),
    SIZE=240
    )

weather_polyhedra = Struct("weather polyhedra",
    QStruct("bounding sphere center", INCLUDE=xyz_float),
    Float("bounding sphere radius"),
    Pad(4),
    reflexive("planes", plane, 15),
    SIZE=32
    )

pathfinding_surface = QStruct("pathfinding surface", UInt8("data"), SIZE=1)

pathfinding_edge = QStruct("pathfinding edge", UInt8("midpoint"), SIZE=1)

background_sound_palette = Struct("background sound palette",
    ascii_str32("name"),
    dependency("background sound", "lsnd"),
    Pad(4),
    ascii_str32("scale function"),
    SIZE=116
    )

sound_environment_palette = Struct("sound environment palette",
    ascii_str32("name"),
    dependency("sound environment", "snde"),
    SIZE=80
    )

marker = Struct("marker",
    ascii_str32("name"),
    QStruct("rotation", INCLUDE=ijkw_float),
    QStruct("position", INCLUDE=xyz_float),
    SIZE=60
    )


detail_object_cell = QStruct("detail object cell",
    SInt16("unknown1"), SInt16("unknown2"),
    SInt16("unknown3"), SInt16("unknown4"),
    SInt32("unknown5"), SInt32("unknown6"), SInt32("unknown7"),
    SIZE=32
    )

detail_object_instance = QStruct("detail object instance",
    SInt8("unknown1"), SInt8("unknown2"),
    SInt8("unknown3"), SInt8("unknown4"), SInt16("unknown5"),
    SIZE=6
    )

detail_object_count = QStruct("detail object count",
    SInt16("unknown"),
    SIZE=2
    )

detail_object_z_reference_vector = QStruct("detail object z reference vector",
    Float("unknown1"), Float("unknown2"),
    Float("unknown3"), Float("unknown4"),
    SIZE=16
    )

detail_object = Struct("detail object",
    reflexive("cells", detail_object_cell, 262144),
    reflexive("instances", detail_object_instance, 2097152),
    reflexive("counts", detail_object_count, 8388608),
    reflexive("z reference vectors", detail_object_z_reference_vector, 262144),
    SIZE=64
    )

runtime_decal = BytesRaw("unknown", SIZE=16)


face_vertex = QStruct("vertex", Float("x"), Float("y"), SIZE=8)
portal_index = Struct("portal index", SInt32("portal index"), SIZE=4)

face = Struct("face",
    SInt32("node index"),
    reflexive("vertices", face_vertex, 64),
    SIZE=16
    )

leaf_map_leaf = Struct("leaf map leaf",
    reflexive("faces", face, 256),
    reflexive("portal indices", portal_index, 256),
    SIZE=24
    )

leaf_map_portal = Struct("leaf map portal",
    SInt32("plane index"),
    SInt32("back leaf index"),
    SInt32("front leaf index"),
    reflexive("vertices", face_vertex, 64),
    SIZE=24
    )

sbsp_body = Struct("tagdata",
    dependency("lightmap bitmaps", 'bitm'),
    float_wu("vehicle floor"),  # world units
    float_wu("vehicle ceiling"),  # world units

    Pad(20),
    QStruct("default ambient color", INCLUDE=rgb_float),
    Pad(4),
    QStruct("default distant light 0 color", INCLUDE=rgb_float),
    QStruct("default distant light 0 direction", INCLUDE=ijk_float),
    QStruct("default distant light 1 color", INCLUDE=rgb_float),
    QStruct("default distant light 1 direction", INCLUDE=ijk_float),

    Pad(12),
    QStruct("default reflection tint", INCLUDE=argb_float),
    QStruct("default shadow vector", INCLUDE=ijk_float),
    QStruct("default shadow color", INCLUDE=rgb_float),

    Pad(4),
    reflexive("collision materials", collision_material, 512,
        DYN_NAME_PATH='.shader.filepath'),
    reflexive("collision bsp", collision_bsp, 1),
    reflexive("nodes", node, 131072, VISIBLE=False),
    QStruct("world bounds x", INCLUDE=from_to),
    QStruct("world bounds y", INCLUDE=from_to),
    QStruct("world bounds z", INCLUDE=from_to),
    reflexive("leaves", leaf, 65535),
    reflexive("leaf surfaces", leaf_surface, 262144),
    reflexive("surface", surface, 131072),
    reflexive("lightmaps", lightmap, 128),

    Pad(12),
    reflexive("lens flares", lens_flare, 256,
        DYN_NAME_PATH='.shader.filepath'),
    reflexive("lens flare markers", lens_flare_marker, 65535),
    reflexive("clusters", cluster, 8192),
    rawdata_ref("cluster data", max_size=65536),
    reflexive("cluster portals", cluster_portal, 512),

    Pad(12),
    reflexive("breakable surfaces", breakable_surface, 256),
    reflexive("fog planes", fog_plane, 32),
    reflexive("fog regions", fog_region, 32),
    reflexive("fog palettes", fog_palette, 32,
        DYN_NAME_PATH='.name'),

    Pad(24),
    reflexive("weather palettes", weather_palette, 32,
        DYN_NAME_PATH='.name'),
    reflexive("weather polyhedras", weather_polyhedra, 32),

    Pad(24),
    reflexive("pathfinding surfaces", pathfinding_surface, 131072),
    reflexive("pathfinding edges", pathfinding_edge, 262144),
    reflexive("background sounds palette", background_sound_palette, 64,
        DYN_NAME_PATH='.name'),
    reflexive("sound environments palette", sound_environment_palette, 64,
        DYN_NAME_PATH='.name'),
    rawdata_ref("sound pas data", max_size=131072),

    Pad(24),
    reflexive("markers", marker, 1024,
        DYN_NAME_PATH='.name'),
    reflexive("detail objects", detail_object, 1),

    # the runtime decals reflexive is populated ONLY by the
    # engine while it is running(I'm making an educated guess)
    reflexive("runtime decals", runtime_decal, 6144, VISIBLE=False),

    Pad(12),
    reflexive("leaf map leaves", leaf_map_leaf, 65536),
    reflexive("leaf map portals", leaf_map_portal, 524288),
    SIZE=648,
    )

fast_sbsp_body = dict(sbsp_body)
fast_sbsp_body[16] = reflexive("collision bsp", fast_collision_bsp, 1)
fast_sbsp_body[17] = raw_reflexive("nodes", node, 131072)
fast_sbsp_body[21] = raw_reflexive("leaves", leaf, 65535)
fast_sbsp_body[22] = raw_reflexive("leaf surfaces", leaf_surface, 262144)
fast_sbsp_body[23] = raw_reflexive("surface", surface, 131072)
fast_sbsp_body[27] = raw_reflexive("lens flare markers", lens_flare_marker, 65535)
fast_sbsp_body[32] = raw_reflexive("breakable surfaces", breakable_surface, 256)
fast_sbsp_body[40] = raw_reflexive("pathfinding surfaces", pathfinding_surface, 131072)
fast_sbsp_body[41] = raw_reflexive("pathfinding edges", pathfinding_edge, 262144)
fast_sbsp_body[46] = raw_reflexive("markers", marker, 1024, DYN_NAME_PATH='.name')


sbsp_meta_header_def = BlockDef("sbsp meta header",
    # to convert these pointers to offsets, do:  pointer - bsp_magic
    UInt32("meta pointer"),
    UInt32("uncompressed lightmap materials count"),
    UInt32("uncompressed lightmap materials pointer"),  # name is a guess
    UInt32("compressed lightmap materials count"),
    UInt32("compressed lightmap materials pointer"),  # name is a guess
    UInt32("sig", DEFAULT="sbsp"),
    SIZE=24, TYPE=QStruct
    )


def get():
    return sbsp_def

sbsp_def = TagDef("sbsp",
    blam_header("sbsp", 5),
    sbsp_body,

    ext=".scenario_structure_bsp", endian=">", tag_cls=HekTag,
    )

fast_sbsp_def = TagDef("sbsp",
    blam_header("sbsp", 5),
    fast_sbsp_body,

    ext=".scenario_structure_bsp", endian=">", tag_cls=HekTag,
    )
