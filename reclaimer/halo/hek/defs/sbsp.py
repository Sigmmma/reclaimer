from .coll import *

collision_material = Struct("collision material",
    )

collision_bsp = Struct("collision bsp", INCLUDE=bsp)

node = Struct("node",
    )

leaf = Struct("lead",
    )

leaf_surface = Struct("leaf surface",
    )

surface = Struct("surface",
    )

lightmap = Struct("lightmap",
    )

lens_flare = Struct("lens flare",
    )

lens_flare_marker = Struct("lens flare marker",
    )

cluster = Struct("cluster",
    )

cluster_portal = Struct("cluster portal",
    )

breakable_surface = Struct("breakable surface",
    )

fog_plane = Struct("fog plane",
    )

fog_region = Struct("fog region",
    )

fog_palette = Struct("fog palette",
    )

weather_palette = Struct("weather palette",
    )

weather_polyhedra = Struct("weather polyhedra",
    )

pathfinding_surface = Struct("pathfinding surface",
    )

pathfinding_edge = Struct("pathfinding edge",
    )

pathfinding_surface = Struct("pathfinding surface",
    )

background_sound_palette = Struct("background sound palette",
    )

sound_environment_palette = Struct("sound environment palette",
    )

pathfinding_surface = Struct("pathfinding surface",
    )

marker = Struct("marker",
    )

detail_object = Struct("detail object",
    )

runtime_decal = Struct("runtime decal",
    )

leaf_map_leaf = Struct("leaf map leaf",
    )

leaf_map_portal = Struct("leaf map portal",
    )

sbsp_body = Struct("tagdata",
    dependency("lightmap bitmaps", 'bitm'),
    BFloat("vehicle floor"),  # world units
    BFloat("vehicle ceiling"),  # world units

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
    reflexive("collision materials", collision_material, 512),
    reflexive("collision bsp", collision_bsp, 1),
    reflexive("nodes", node, 131072),
    QStruct("world bounds x", INCLUDE=from_to),
    QStruct("world bounds y", INCLUDE=from_to),
    QStruct("world bounds z", INCLUDE=from_to),
    reflexive("leaves", leaf, 65536),
    reflexive("leaf surfaces", leaf_surface, 262144),
    reflexive("surface", surface, 131072),
    reflexive("lightmaps", lightmap, 128),

    Pad(12),
    reflexive("lens flares", lens_flare, 256),
    reflexive("lens flare markers", lens_flare_marker, 65536),
    reflexive("clusters", cluster, 8192),
    rawdata_ref("cluster data"),
    reflexive("cluster portals", cluster_portal, 512),

    Pad(12),
    reflexive("breakable surfaces", breakable_surface, 256),
    reflexive("fog planes", fog_plane, 32),
    reflexive("fog regions", fog_region, 32),
    reflexive("fog palettes", fog_palette, 32),

    Pad(24),
    reflexive("weather palettes", weather_palette, 32),
    reflexive("weather polyhedra", weather_polyhedra, 32),

    Pad(24),
    reflexive("pathfinding surfaces", pathfinding_surface, 131072),
    reflexive("pathfinding edge", pathfinding_edge, 262144),
    reflexive("background sound palette", background_sound_palette, 64),
    reflexive("sound environment palette", sound_environment_palette, 64),
    rawdata_ref("sound pas data"),

    Pad(24),
    reflexive("markers", marker, 1024),
    reflexive("detail objects", detail_object, 1),
    reflexive("runtime decal", runtime_decal, 6144),

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

    ext=".scenario_structure_bsp", endian=">",
    )
