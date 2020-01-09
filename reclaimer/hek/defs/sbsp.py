#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from .coll import *
from .objs.sbsp import SbspTag
from supyr_struct.defs.block_def import BlockDef

cluster_fog_tooltip = (
    "Unknown flag is set if negative.\n"
    "Add 0x8000 to get fog index."
    )


# the order is an array of vertices first, then an array of lightmap vertices.
#
uncompressed_vertex = QStruct("uncompressed_vertex",
    Float('position_x'), Float('position_y'), Float('position_z'),
    Float('normal_i'),   Float('normal_j'),   Float('normal_k'),
    Float('binormal_i'), Float('binormal_j'), Float('binormal_k'),
    Float('tangent_i'),  Float('tangent_j'),  Float('tangent_k'),

    Float('tex_coord_u'), Float('tex_coord_v'),
    SIZE=56
    )

compressed_vertex = QStruct("compressed_vertex",
    Float('position_x'), Float('position_y'), Float('position_z'),
    UInt32('normal'),
    UInt32('binormal'),
    UInt32('tangent'),

    Float('tex_coord_u'), Float('tex_coord_v'),
    SIZE=32
    )

uncompressed_lightmap_vertex = QStruct("uncompressed_lightmap_vertex",
    # this normal is the direction the light is hitting from, and
    # is used for calculating dynamic shadows on dynamic objects
    Float('normal_i'), Float('normal_j'), Float('normal_k'),
    Float('u'), Float('v'),
    SIZE=20
    )

compressed_lightmap_vertex = QStruct("compressed_lightmap_vertex",
    # this normal is the direction the light is hitting from, and
    # is used for calculating dynamic shadows on dynamic objects
    UInt32('normal'),
    SInt16('u', UNIT_SCALE=1/32767, MIN=-32767, WIDGET_WIDTH=10),
    SInt16('v', UNIT_SCALE=1/32767, MIN=-32767, WIDGET_WIDTH=10),
    SIZE=8
    )

plane = QStruct("plane",
    Float("i", MIN=-1.0, MAX=1.0),
    Float("j", MIN=-1.0, MAX=1.0),
    Float("k", MIN=-1.0, MAX=1.0),
    Float("d"),
    SIZE=16, ORIENT='h'
    )

vertex = QStruct("vertex", INCLUDE=xyz_float, SIZE=12)

collision_material = Struct("collision_material",
    dependency("shader", valid_shaders),
    FlUInt32("unknown", VISIBLE=False),
    SIZE=20
    )

collision_bsp = Struct("collision_bsp", INCLUDE=permutation_bsp)
fast_collision_bsp = Struct("collision_bsp", INCLUDE=fast_permutation_bsp)

node = Struct("node",
    # these dont get byteswapped going from meta to tag
    BytesRaw("unknown", SIZE=6),
    #QStruct("unknown_0", UInt8("val0"), SInt8("val1"), ORIENT="h"),
    #QStruct("unknown_1", UInt8("val0"), SInt8("val1"), ORIENT="h"),
    #QStruct("unknown_2", UInt8("val0"), SInt8("val1"), ORIENT="h"),
    SIZE=6
    )

leaf = QStruct("leaf",
    # these unknowns are in the tag and are preserved in the meta
    FlSInt16("unknown0", VISIBLE=False),
    FlSInt16("unknown1", VISIBLE=False),
    FlSInt16("unknown2", VISIBLE=False),
    FlSInt16("unknown3", VISIBLE=False),

    SInt16("cluster"),
    SInt16("surface_reference_count"),
    SInt32("surface_references"),
    SIZE=16,
    )

leaf_surface = QStruct("leaf_surface",
    SInt32("surface"),
    SInt32("node"),
    SIZE=8, ORIENT='h'
    )

surface = QStruct("surface",
    SInt16("a"),
    SInt16("b"),
    SInt16("c"),
    SIZE=6, ORIENT='h', COMMENT="""
This is a renderable surface(visible geometry and lightmap geometry)"""
    )

material = Struct("material",
    dependency("shader", valid_shaders),
    SInt16("shader_permutation"),
    Bool16("flags",
        "coplanar",
        "fog_plane",
        ),
    SInt32("surfaces", EDITABLE=False,
        TOOLTIP=("The offset into the surfaces array that this\n"
                 "lightmap materials surfaces are located at.")
        ),
    SInt32("surface_count", EDITABLE=False,
        TOOLTIP=("The number of surfaces in the array belonging\n"
                 "to this lightmap material.")
        ),
    QStruct("centroid", INCLUDE=xyz_float),
    QStruct("ambient_color", INCLUDE=rgb_float),
    SInt16("distant_light_count"),
    Pad(2),

    QStruct("distant_light_0_color", INCLUDE=rgb_float),
    QStruct("distant_light_0_direction", INCLUDE=ijk_float),
    QStruct("distant_light_1_color", INCLUDE=rgb_float),
    QStruct("distant_light_1_direction", INCLUDE=ijk_float),
    Pad(12),

    QStruct("reflection_tint", INCLUDE=argb_float),
    QStruct("shadow_vector", INCLUDE=ijk_float),
    QStruct("shadow_color", INCLUDE=rgb_float),
    QStruct("plane", INCLUDE=plane),
    SInt16("breakable_surface", EDITABLE=False),
    Pad(6),

    SInt32("vertices_count", EDITABLE=False),
    SInt32("vertices_offset", EDITABLE=False, VISIBLE=False),

    FlUInt32("unknown_meta_offset0", VISIBLE=False),
    FlUInt32("vertices_meta_offset",
        TOOLTIP=("In xbox maps this is a bspmagic relative pointer that\n"
                 "points to a reflexive. The reflexive contains only a\n"
                 "bspmagic relative pointer to the vertices."),
        VISIBLE=False
        ),
    FlUEnum16("vertex_type",  # name is a guess
        ("unknown", 0),
        ("uncompressed", 2),
        ("compressed",   3),
        VISIBLE=False,
        ),
    Pad(2),
    SInt32("lightmap_vertices_count", EDITABLE=False),
    SInt32("lightmap_vertices_offset", EDITABLE=False, VISIBLE=False),

    FlUInt32("unknown_meta_offset1", VISIBLE=False),
    FlUInt32("lightmap_vertices_meta_offset",
        TOOLTIP=("In xbox maps this is a bspmagic relative pointer that\n"
                 "points to a reflexive. The reflexive contains only a\n"
                 "bspmagic relative pointer to the lightmap vertices."),
        VISIBLE=False
        ),

    rawdata_ref("uncompressed_vertices", max_size=4864000),
    rawdata_ref("compressed_vertices", max_size=2560000),
    SIZE=256
    )

lightmap = Struct("lightmap",
    SInt16("bitmap_index"),
    Pad(18),
    reflexive("materials", material, 2048,
        DYN_NAME_PATH='.shader.filepath'),
    SIZE=32
    )

lens_flare = Struct("lens_flare",
    dependency("shader", 'lens'),
    SIZE=16
    )

lens_flare_marker = Struct("lens_flare_marker",
    QStruct("position", INCLUDE=xyz_float),
    QStruct("direction",
        SInt8('i'), SInt8('j'), SInt8('k'), ORIENT='h'
        ),
    # While guerilla treats this like a signed int, there is no way that it
    # is gonna be able to reference one of the 256 lens flares if its signed
    UInt8('lens_flare_index'),
    SIZE=16
    )

surface_index = QStruct("surface_index",
    SInt32("surface_index"),
    SIZE=4
    )

mirror = Struct("mirror",
    QStruct("plane", INCLUDE=plane),
    # might be padding, might not be
    BytesRaw("unknown", VISIBLE=False, SIZE=20),
    #Pad(20),
    dependency("shader", valid_shaders),
    reflexive("vertices", vertex, 512),
    SIZE=64
    )

portal = QStruct("portal",
    SInt16("portal"),
    SIZE=2
    )

subcluster = Struct("subcluster",
    QStruct('world_bounds_x', INCLUDE=from_to),
    QStruct('world_bounds_y', INCLUDE=from_to),
    QStruct('world_bounds_z', INCLUDE=from_to),
    reflexive("surface_indices", surface_index, 128),
    SIZE=36, COMMENT="""
Subclusters define areas to render in square chunks. Surfaces indices are
the renderable surfaces(not collision) to render in this subcluster. This is
how Halo's renderer knows what surfaces to render in each cluster."""
    )

cluster = Struct("cluster",
    SInt16('sky'),
    SInt16('fog', TOOLTIP=cluster_fog_tooltip),
    dyn_senum16('background_sound',
        DYN_NAME_PATH="tagdata.background_sounds_palette.STEPTREE[DYN_I].name"),
    dyn_senum16('sound_environment',
        DYN_NAME_PATH="tagdata.sound_environments_palette." +
        "STEPTREE[DYN_I].name"),
    dyn_senum16('weather',
        DYN_NAME_PATH="tagdata.weather_palettes.STEPTREE[DYN_I].name"),

    UInt16("transition_structure_bsp", VISIBLE=False),
    UInt16("first_decal_index", VISIBLE=False),
    UInt16("decal_count", VISIBLE=False),

    # almost certain this is padding, though a value in the third
    # and fourth bytes is non-zero in meta, but not in a tag, so idk.
    Pad(24),

    reflexive("predicted_resources", predicted_resource, 1024, VISIBLE=False),
    reflexive("subclusters", subcluster, 4096),
    SInt16("first_lens_flare_marker_index"),
    SInt16("lens_flare_marker_count"),
    reflexive("surface_indices", surface_index, 32768),
    reflexive("mirrors", mirror, 16, DYN_NAME_PATH=".shader.filepath"),
    reflexive("portals", portal, 128),
    SIZE=104
    )

cluster_portal = Struct("cluster_portal",
    SInt16("front_cluster"),
    SInt16("back_cluster"),
    SInt32("plane_index"),
    QStruct("centroid", INCLUDE=xyz_float),
    Float("bounding_radius"),
    Bool32("flags",
        "ai_cant_hear_through_this",
        ),

    # might be padding, might not be
    BytesRaw("unknown", VISIBLE=False, SIZE=24),
    #Pad(24),
    reflexive("vertices", vertex, 128),
    SIZE=64
    )

breakable_surface = Struct("breakable_surface",
    QStruct("centroid", INCLUDE=xyz_float),
    Float("radius"),
    SInt32("collision_surface_index"),
    Pad(28),
    SIZE=48
    )

fog_plane = Struct("fog_plane",
    SInt16("front_region"),
    FlSEnum16("material_type",
        *(tuple((materials_list[i], i) for i in
           range(len(materials_list))) + (("NONE", -1), )),
        VISIBLE=False),  # calculated when compiled into map
    QStruct("plane", INCLUDE=plane),
    reflexive("vertices", vertex, 4096),
    SIZE=32
    )

fog_region = Struct("fog_region",
    Pad(36),
    dyn_senum16("fog_palette",
        DYN_NAME_PATH="tagdata.fog_palettes.STEPTREE[DYN_I].name"),
    dyn_senum16("weather_palette",
        DYN_NAME_PATH="tagdata.weather_palettes.STEPTREE[DYN_I].name"),
    SIZE=40
    )

fog_palette = Struct("fog_palette",
    ascii_str32("name"),
    dependency("fog", "fog "),
    Pad(4),
    ascii_str32("fog_scale_function"),
    SIZE=136
    )

weather_palette = Struct("weather_palette",
    ascii_str32("name"),
    dependency("particle_system", "rain"),
    Pad(4),
    ascii_str32("particle_system_scale_function"),

    Pad(44),
    dependency("wind", "wind"),
    QStruct("wind_direction", INCLUDE=ijk_float),
    Float("wind_magnitude"),
    Pad(4),
    ascii_str32("wind_scale_function"),
    SIZE=240
    )

weather_polyhedra = Struct("weather_polyhedra",
    QStruct("bounding_sphere_center", INCLUDE=xyz_float),
    Float("bounding_sphere_radius"),
    Pad(4),
    reflexive("planes", plane, 16),
    SIZE=32
    )

pathfinding_surface = QStruct("pathfinding_surface",
    # this is actually a 3bit width index, 3bit height
    # index, and 2 flags(is_walkable and is_breakable/is_broken)
    # stored in a single byte(in that order)
    UInt8("data"),
    SIZE=1
    )

pathfinding_edge = QStruct("pathfinding_edge", UInt8("midpoint"), SIZE=1)

background_sound_palette = Struct("background_sound_palette",
    ascii_str32("name"),
    dependency("background_sound", "lsnd"),
    Pad(4),
    ascii_str32("scale_function"),
    SIZE=116
    )

sound_environment_palette = Struct("sound_environment_palette",
    ascii_str32("name"),
    dependency("sound_environment", "snde"),
    SIZE=80
    )

marker = Struct("marker",
    ascii_str32("name"),
    QStruct("rotation", INCLUDE=ijkw_float),
    QStruct("position", INCLUDE=xyz_float),
    SIZE=60
    )


detail_object_cell = QStruct("detail_object_cell",
    SInt16("unknown1"), SInt16("unknown2"),
    SInt16("unknown3"), SInt16("unknown4"),
    SInt32("unknown5"), SInt32("unknown6"), SInt32("unknown7"),
    SIZE=32
    )

detail_object_instance = QStruct("detail_object_instance",
    SInt8("unknown1"), SInt8("unknown2"),
    SInt8("unknown3"), SInt8("unknown4"), SInt16("unknown5"),
    SIZE=6
    )

detail_object_count = QStruct("detail_object_count",
    SInt16("unknown"),
    SIZE=2
    )

detail_object_z_reference_vector = QStruct("detail_object_z_reference_vector",
    Float("unknown1"), Float("unknown2"),
    Float("unknown3"), Float("unknown4"),
    SIZE=16
    )

detail_object = Struct("detail_object",
    reflexive("cells", detail_object_cell, 262144),
    reflexive("instances", detail_object_instance, 2097152),
    reflexive("counts", detail_object_count, 8388608),
    reflexive("z_reference_vectors", detail_object_z_reference_vector, 262144),
    Bool8("flags",
        "enabled",  # required to be set on map compile.
        #             set to   "parent.instances.size != 0"
        VISIBLE=False
        ),
    SIZE=64
    )

runtime_decal = BytesRaw("unknown", SIZE=16)


face_vertex = QStruct("vertex", Float("x"), Float("y"), SIZE=8)
portal_index = Struct("portal_index", SInt32("portal_index"), SIZE=4)

face = Struct("face",
    SInt32("node_index"),
    reflexive("vertices", face_vertex, 64),
    SIZE=16
    )

leaf_map_leaf = Struct("leaf_map_leaf",
    reflexive("faces", face, 256),
    reflexive("portal_indices", portal_index, 256),
    SIZE=24
    )

leaf_map_portal = Struct("leaf_map_portal",
    SInt32("plane_index"),
    SInt32("back_leaf_index"),
    SInt32("front_leaf_index"),
    reflexive("vertices", face_vertex, 64),
    SIZE=24
    )

raw_cluster_data = QStruct("raw_cluster_data",
    UInt16("unknown0"),
    UInt16("unknown1"),
    UInt16("unknown2"),
    UInt16("unknown3"),
    SIZE=8
    )

sbsp_body = Struct("tagdata",
    dependency("lightmap_bitmaps", 'bitm'),
    float_wu("vehicle_floor"),  # world units
    float_wu("vehicle_ceiling"),  # world units

    Pad(20),
    QStruct("default_ambient_color", INCLUDE=rgb_float),
    Pad(4),
    QStruct("default_distant_light_0_color", INCLUDE=rgb_float),
    QStruct("default_distant_light_0_direction", INCLUDE=ijk_float),
    QStruct("default_distant_light_1_color", INCLUDE=rgb_float),
    QStruct("default_distant_light_1_direction", INCLUDE=ijk_float),

    Pad(12),
    QStruct("default_reflection_tint", INCLUDE=argb_float),
    QStruct("default_shadow_vector", INCLUDE=ijk_float),
    QStruct("default_shadow_color", INCLUDE=rgb_float),

    Pad(4),
    reflexive("collision_materials", collision_material, 512,
        DYN_NAME_PATH='.shader.filepath'),
    reflexive("collision_bsp", collision_bsp, 1),
    reflexive("nodes", node, 131072, VISIBLE=False),
    QStruct("world_bounds_x", INCLUDE=from_to),
    QStruct("world_bounds_y", INCLUDE=from_to),
    QStruct("world_bounds_z", INCLUDE=from_to),
    reflexive("leaves", leaf, 65535),
    reflexive("leaf_surfaces", leaf_surface, 262144),
    reflexive("surfaces", surface, 131072),
    reflexive("lightmaps", lightmap, 128),

    Pad(12),
    reflexive("lens_flares", lens_flare, 256,
        DYN_NAME_PATH='.shader.filepath'),
    reflexive("lens_flare_markers", lens_flare_marker, 65535),
    reflexive("clusters", cluster, 8192),

    # this is an array of 8 byte structs for each cluster
    rawdata_ref("cluster_data", max_size=65536),
    reflexive("cluster_portals", cluster_portal, 512),

    Pad(12),
    reflexive("breakable_surfaces", breakable_surface, 256),
    reflexive("fog_planes", fog_plane, 32),
    reflexive("fog_regions", fog_region, 32),
    reflexive("fog_palettes", fog_palette, 32,
        DYN_NAME_PATH='.name'),

    Pad(24),
    reflexive("weather_palettes", weather_palette, 32,
        DYN_NAME_PATH='.name'),
    reflexive("weather_polyhedras", weather_polyhedra, 32),

    Pad(24),
    reflexive("pathfinding_surfaces", pathfinding_surface, 131072, VISIBLE=False),
    reflexive("pathfinding_edges", pathfinding_edge, 262144, VISIBLE=False),
    reflexive("background_sounds_palette", background_sound_palette, 64,
        DYN_NAME_PATH='.name'),
    reflexive("sound_environments_palette", sound_environment_palette, 64,
        DYN_NAME_PATH='.name'),
    rawdata_ref("sound_pas_data", max_size=131072),

    UInt32("unknown", VISIBLE=False),
    Pad(20),
    reflexive("markers", marker, 1024, DYN_NAME_PATH='.name'),
    reflexive("detail_objects", detail_object, 1, VISIBLE=False),

    # the runtime decals reflexive is populated ONLY by the
    # engine while it is running(I'm making an educated guess)
    reflexive("runtime_decals", runtime_decal, 6144, VISIBLE=False),

    Pad(12),
    reflexive("leaf_map_leaves", leaf_map_leaf, 65536, VISIBLE=False),
    reflexive("leaf_map_portals", leaf_map_portal, 524288, VISIBLE=False),
    SIZE=648,
    )

fast_sbsp_body = dict(sbsp_body)
fast_sbsp_body[16] = reflexive("collision_bsp", fast_collision_bsp, 1)
fast_sbsp_body[17] = raw_reflexive("nodes", node, 131072)
fast_sbsp_body[21] = raw_reflexive("leaves", leaf, 65535)
fast_sbsp_body[22] = raw_reflexive("leaf_surfaces", leaf_surface, 262144)
fast_sbsp_body[23] = raw_reflexive("surface", surface, 131072)
fast_sbsp_body[27] = raw_reflexive("lens_flare_markers", lens_flare_marker, 65535)
fast_sbsp_body[32] = raw_reflexive("breakable_surfaces", breakable_surface, 256)
fast_sbsp_body[40] = raw_reflexive("pathfinding_surfaces", pathfinding_surface, 131072)
fast_sbsp_body[41] = raw_reflexive("pathfinding_edges", pathfinding_edge, 262144)
fast_sbsp_body[47] = raw_reflexive("markers", marker, 1024, DYN_NAME_PATH='.name')


sbsp_meta_header_def = BlockDef("sbsp_meta_header",
    # to convert these pointers to offsets, do:  pointer - bsp_magic
    UInt32("meta_pointer"),
    UInt32("uncompressed_lightmap_materials_count"),
    UInt32("uncompressed_lightmap_materials_pointer"),  # name is a guess
    UInt32("compressed_lightmap_materials_count"),
    UInt32("compressed_lightmap_materials_pointer"),  # name is a guess
    UInt32("sig", DEFAULT="sbsp"),
    SIZE=24, TYPE=QStruct
    )


def get():
    return sbsp_def

sbsp_def = TagDef("sbsp",
    blam_header("sbsp", 5),
    sbsp_body,

    ext=".scenario_structure_bsp", endian=">", tag_cls=SbspTag,
    )

fast_sbsp_def = TagDef("sbsp",
    blam_header("sbsp", 5),
    fast_sbsp_body,

    ext=".scenario_structure_bsp", endian=">", tag_cls=SbspTag,
    )
