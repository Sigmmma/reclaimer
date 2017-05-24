from ...hek.defs.sbsp import *


cluster = Struct("cluster",
    SInt16('sky'),
    SInt16('fog'),
    dyn_senum16('background sound',
        DYN_NAME_PATH="tagdata.background_sounds_palette.STEPTREE[DYN_I].name"),
    dyn_senum16('sound environment',
        DYN_NAME_PATH="tagdata.sound_environments_palette." +
        "STEPTREE[DYN_I].name"),
    dyn_senum32('weather',
        DYN_NAME_PATH="tagdata.weather_palettes.STEPTREE[DYN_I].name"),

    QStruct("unknown0",
        UInt16('uint16_1'),
        UInt16('uint16_2'),
        Float('float_0'),
        Float('float_1'),
        Float('float_2'),
        Float('float_3'),
        Float('float_4'),
        Float('float_5'),
        SIZE=28
        ),

    reflexive("predicted resources", predicted_resource, 1024),
    reflexive("subclusters", subcluster, 4096),
    SInt16("first lens flare marker index"),
    SInt16("lens flare marker count"),

    # stubbs seems to have different data here
    #reflexive("surface indices", surface_index, 32768),
    #reflexive("mirrors", mirror, 16, DYN_NAME_PATH=".shader.filepath"),
    #reflexive("portals", portal, 128),
    SIZE=104
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
