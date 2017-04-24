from .coll import *
from .objs.tag import HekTag

plane = QStruct("plane",
    BFloat("i", MIN=0.0, MAX=1.0),
    BFloat("j", MIN=0.0, MAX=1.0),
    BFloat("k", MIN=0.0, MAX=1.0),
    BFloat("d"),
    SIZE=16, ORIENT='h'
    )

vertex = QStruct("vertex", INCLUDE=xyz_float, SIZE=12)

collision_material = Struct("collision material",
    dependency("shader", valid_shaders),
    SIZE=20
    )

collision_bsp = Struct("collision bsp", INCLUDE=permutation_bsp)

node = Struct("node",
    BytesRaw("unknown", SIZE=6),
    )

leaf = Struct("leaf",
    Pad(8),
    BSInt16("cluster"),
    BSInt16("surface reference count"),
    BSInt32("surface references"),
    SIZE=16,
    )

leaf_surface = Struct("leaf surface",
    BSInt32("surface"), BSInt32("node"),
    SIZE=8, ORIENT='h'
    )

surface = Struct("surface",
    BSInt16("a"), BSInt16("b"), BSInt16("c"),
    SIZE=6, ORIENT='h'
    )

material = Struct("material",
    dependency("shader", valid_shaders),
    BSInt16("shader permutation"),
    BBool16("flags",
        "coplanar",
        "fog plane",
        ),
    BSInt32("surfaces"),
    BSInt32("surface count"),
    QStruct("centroid", INCLUDE=xyz_float),
    QStruct("ambient color", INCLUDE=rgb_float),
    BSInt16("distant light count"),

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
    BSInt16("breakable surface"),

    Pad(6),
    BSInt32("uncompressed vertices count"),
    BSInt32("uncompressed vertices offset"),

    Pad(12),
    BSInt32("compressed vertices count"),
    BSInt32("compressed vertices offset"),

    Pad(8),
    rawdata_ref("uncompressed vertices", max_size=4864000),
    rawdata_ref("compressed vertices", max_size=2560000),
    SIZE=256
    )

lightmap = Struct("lightmap",
    BSInt16("bitmap index"),
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
    BSInt32("index"),
    SIZE=4
    )

mirror = Struct("mirror",
    QStruct("plane", INCLUDE=plane),
    Pad(20),
    dependency("shader", valid_shaders),
    reflexive("vertices", vertex, 512),
    SIZE=64
    )

portal = QStruct("portal",
    BSInt16("portal"),
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
    BSInt16('sky'),
    BSInt16('fog'),
    dyn_senum16('background sound',
        DYN_NAME_PATH="tagdata.background_sounds_palette.STEPTREE[DYN_I].name"),
    dyn_senum16('sound environment',
        DYN_NAME_PATH="tagdata.sound_environments_palette." +
        "STEPTREE[DYN_I].name"),
    dyn_senum32('weather',
        DYN_NAME_PATH="tagdata.weather_palettes.STEPTREE[DYN_I].name"),

    Pad(28),
    reflexive("predicted resources", predicted_resource, 1024),
    reflexive("subclusters", subcluster, 4096),
    BSInt16('first lens flare marker index'),
    BSInt16('lens flare marker count'),
    reflexive("surface indices", surface_index, 32768),
    reflexive("mirrors", mirror, 16, DYN_NAME_PATH=".shader.filepath"),
    reflexive("portals", portal, 128),
    SIZE=104
    )

cluster_portal = Struct("cluster portal",
    BSInt16("front cluster"),
    BSInt16("back cluster"),
    BSInt32("plane index"),
    QStruct("centroid", INCLUDE=xyz_float),
    BFloat("bounding radius"),
    BBool32("flags",
        "ai cant hear through this",
        ),

    Pad(24),
    reflexive("vertices", vertex, 128),
    SIZE=64
    )

breakable_surface = Struct("breakable surface",
    QStruct("centroid", INCLUDE=xyz_float),
    BFloat("radius"),
    BSInt32("collision surface index"),
    SIZE=48
    )

fog_plane = Struct("fog plane",
    BSEnum16("front region"),
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
    BFloat("wind magnitude"),
    Pad(4),
    ascii_str32("wind scale function"),
    SIZE=240
    )

weather_polyhedra = Struct("weather polyhedra",
    QStruct("bounding sphere center", INCLUDE=xyz_float),
    BFloat("bounding sphere radius"),
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
    BSInt16("unknown1"), BSInt16("unknown2"),
    BSInt16("unknown3"), BSInt16("unknown4"),
    BSInt32("unknown5"), BSInt32("unknown6"), BSInt32("unknown7"),
    SIZE=32
    )

detail_object_instance = QStruct("detail object instance",
    SInt8("unknown1"), SInt8("unknown2"),
    SInt8("unknown3"), SInt8("unknown4"), BSInt16("unknown5"),
    SIZE=6
    )

detail_object_count = QStruct("detail object count",
    BSInt16("unknown"),
    SIZE=2
    )

detail_object_z_reference_vector = QStruct("detail object z reference vector",
    BFloat("unknown1"), BFloat("unknown2"),
    BFloat("unknown3"), BFloat("unknown4"),
    SIZE=16
    )

detail_object = Struct("detail object",
    reflexive("cells", detail_object_cell, 262144),
    reflexive("instances", detail_object_instance, 2097152),
    reflexive("counts", detail_object_count, 8388608),
    reflexive("z reference vectors", detail_object_z_reference_vector, 262144),
    SIZE=64
    )

runtime_decal = Struct("runtime decal",
    BytesRaw("unknown", SIZE=16),
    SIZE=16
    )


face_vertex = QStruct("vertex", BFloat("x"), BFloat("y"), SIZE=8)
portal_index = Struct("portal index", BSInt32("portal index"), SIZE=4)

face = Struct("face",
    BSInt32("node index"),
    reflexive("vertices", face_vertex, 64),
    SIZE=16
    )

leaf_map_leaf = Struct("leaf map leaf",
    reflexive("faces", face, 256),
    reflexive("portal indices", portal_index, 256),
    SIZE=24
    )

leaf_map_portal = Struct("leaf map portal",
    BSInt32("plane index"),
    BSInt32("back leaf index"),
    BSInt32("front leaf index"),
    reflexive("vertices", face_vertex, 64),
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
    reflexive("nodes", node, 131072),
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
    reflexive("runtime decals", runtime_decal, 6144),

    Pad(12),
    reflexive("leaf map leaves", leaf_map_leaf, 256),
    reflexive("leaf map portals", leaf_map_portal, 524288),
    SIZE=648,
    )


def get():
    return sbsp_def

sbsp_def = TagDef("sbsp",
    blam_header("sbsp", 5),
    sbsp_body,

    ext=".scenario_structure_bsp", endian=">", tag_cls=HekTag,
    )
