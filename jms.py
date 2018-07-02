import re

from os import makedirs
from os.path import dirname, exists
from .util import float_to_str


class JmsNode:
    __slots__ = (
        "name",
        "first_child", "sibling_index",
        "rot_i", "rot_j", "rot_k", "rot_w",
        "pos_x", "pos_y", "pos_z",
        )
    def __init__(self, name="", first_child=-1, sibling_index=-1,
                 rot_i=0.0, rot_j=0.0, rot_k=0.0, rot_w=1.0,
                 pos_x=0.0, pos_y=0.0, pos_z=0.0):
        self.name = name
        self.sibling_index = sibling_index
        self.first_child = first_child
        self.rot_i = rot_i
        self.rot_j = rot_j
        self.rot_k = rot_k
        self.rot_w = rot_w
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z

    def __repr__(self):
        return """JmsNode(%s,
    first_child=%s, sibling_index=%s,
    i=%s, j=%s, k=%s, w=%s,
    x=%s, y=%s, z=%s
)""" % (self.name, self.first_child, self.sibling_index,
        self.rot_i, self.rot_j, self.rot_k, self.rot_w,
        self.pos_x, self.pos_y, self.pos_z)


class JmsMaterial:
    __slots__ = (
        "name",
        "tiff_path",
        )
    def __init__(self, name="__unnamed", tiff_path="<none>"):
        self.name = name
        self.tiff_path = tiff_path

    def __repr__(self):
        return """JmsMaterial(name=%s,
    tiff_path=%s
)""" % (self.name, self.tiff_path)


class JmsMarker:
    __slots__ = (
        "name",
        "region", "parent",
        "rot_i", "rot_j", "rot_k", "rot_w",
        "pos_x", "pos_y", "pos_z",
        "radius",
        )
    def __init__(self, name="", region=-1, parent=0,
                 rot_i=0.0, rot_j=0.0, rot_k=0.0, rot_w=1.0,
                 pos_x=0.0, pos_y=0.0, pos_z=0.0, radius=0.0):
        self.name = name
        self.parent = parent
        self.region = region
        self.rot_i = rot_i
        self.rot_j = rot_j
        self.rot_k = rot_k
        self.rot_w = rot_w
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.radius = radius

    def __repr__(self):
        return """JmsMarker(name=%s,
    region=%s,  parent=%s,
    i=%s, j=%s, k=%s, w=%s,
    x=%s, y=%s, z=%s,
    radius=%s
)""" % (self.name, self.region, self.parent,
        self.rot_i, self.rot_j, self.rot_k, self.rot_w,
        self.pos_x, self.pos_y, self.pos_z, self.radius)


class JmsVertex:
    __slots__ = (
        "node_0",
        "pos_x", "pos_y", "pos_z",
        "norm_i", "norm_j", "norm_k",
        "node_1", "node_1_weight", 
        "tex_u", "tex_v", "tex_w",
        )
    def __init__(self, node_0=0,
                 pos_x=0.0, pos_y=0.0, pos_z=0.0,
                 norm_i=0.0, norm_j=0.0, norm_k=0.0,
                 node_1=-1, node_1_weight=0.0,
                 tex_u=0, tex_v=0, tex_w=0):
        self.node_0 = node_0
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.norm_i = norm_i
        self.norm_j = norm_j
        self.norm_k = norm_k
        self.node_1 = node_1
        self.node_1_weight = node_1_weight
        self.tex_u = tex_u
        self.tex_v = tex_v
        self.tex_w = tex_w

    def __repr__(self):
        return """JmsVertex(node_0=%s,
    x=%s, y=%s, z=%s,
    i=%s, j=%s, k=%s,
    node_1=%s, node_1_weight=%s,
    u=%s, v=%s, w=%s
)""" % (self.node_0,
        self.pos_x, self.pos_y, self.pos_z,
        self.norm_i, self.norm_j, self.norm_k,
        self.node_1, self.node_1_weight,
        self.tex_u, self.tex_v, self.tex_w)


class JmsTriangle:
    __slots__ = (
        "region", "shader",
        "v0", "v1", "v2"
        )
    def __init__(self, region=0, shader=0,
                 v0=0, v1=0, v2=0):
        self.region = region
        self.shader = shader
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2

    def __repr__(self):
        return """JmsTriangle(
    region=%s, shader=%s,
    v0=%s, v1=%s, v2=%s
)""" % (self.region, self.shader,
        self.v0, self.v1, self.v2)


def read_jms(jms_string, stop_at=""):
    nodes = []
    materials = []
    markers = []
    regions = []
    vertices = []
    triangles = []

    jms_data = [0, materials, regions,
                nodes, markers, vertices, triangles]

    jms_string = jms_string.replace("\n", "\t")

    data = tuple(d for d in jms_string.split("\t") if d)

    if data[0] != "8200":
        print("JMS identifier not found.")
        return jms_data

    try:
        jms_data[0] = int(data[1])
    except Exception:
        print("Could not read node list checksum.")
        return jms_data

    if stop_at == "nodes": return jms_data

    dat_i = 2

    # read the nodes
    try:
        i = 0
        nodes.extend((None, ) * int(data[dat_i]))
        dat_i += 1
        for i in range(len(nodes)):
            nodes[i] = JmsNode(
                data[dat_i], int(data[dat_i+1]), int(data[dat_i+2]),
                float(data[dat_i+3]), float(data[dat_i+4]),
                float(data[dat_i+5]), float(data[dat_i+6]),
                float(data[dat_i+7]), float(data[dat_i+8]), float(data[dat_i+9]),
                )
            dat_i += 10
            i += 1
    except Exception:
        print("Failed to read nodes.")
        del nodes[i: ]
        return jms_data

    if stop_at == "materials": return jms_data

    # read the materials
    try:
        i = 0
        materials.extend((None, ) * int(data[dat_i]))
        dat_i += 1
        for i in range(len(materials)):
            materials[i] = JmsMaterial(data[dat_i], data[dat_i+1])
            dat_i += 2
            i += 1
    except Exception:
        print("Failed to read materials.")
        del materials[i: ]
        return jms_data

    if stop_at == "markers": return jms_data

    # read the markers
    try:
        i = 0
        markers.extend((None, ) * int(data[dat_i]))
        dat_i += 1
        for i in range(len(markers)):
            markers[i] = JmsMarker(
                data[dat_i], int(data[dat_i+1]), int(data[dat_i+2]),
                float(data[dat_i+3]), float(data[dat_i+4]),
                float(data[dat_i+5]), float(data[dat_i+6]),
                float(data[dat_i+7]), float(data[dat_i+8]), float(data[dat_i+9]),
                float(data[dat_i+10])
                )
            dat_i += 11
            i += 1
    except Exception:
        print("Failed to read markers.")
        del markers[i: ]
        return jms_data

    if stop_at == "regions": return jms_data

    # read the regions
    try:
        i = 0
        regions.extend((None, ) * int(data[dat_i]))
        dat_i += 1
        for i in range(len(regions)):
            regions[i] = data[dat_i]
            dat_i += 1
            i += 1
    except Exception:
        print("Failed to read regions.")
        del regions[i: ]
        return jms_data

    if stop_at == "vertices": return jms_data

    # read the vertices
    try:
        i = 0
        vertices.extend((None, ) * int(data[dat_i]))
        dat_i += 1
        for i in range(len(vertices)):
            vertices[i] = JmsVertex(
                int(data[dat_i]),
                float(data[dat_i+1]), float(data[dat_i+2]), float(data[dat_i+3]),
                float(data[dat_i+4]), float(data[dat_i+5]), float(data[dat_i+6]),
                int(data[dat_i+7]), float(data[dat_i+8]),
                float(data[dat_i+9]), float(data[dat_i+10]), float(data[dat_i+11])
                )
            dat_i += 12
            i += 1
    except Exception:
        print("Failed to read vertices.")
        del vertices[i: ]
        return jms_data

    if stop_at == "triangles": return jms_data

    # read the triangles
    try:
        i = 0
        triangles.extend((None, ) * int(data[dat_i]))
        dat_i += 1
        for i in range(len(triangles)):
            triangles[i] = JmsTriangle(
                int(data[dat_i]), int(data[dat_i+1]),
                int(data[dat_i+2]), int(data[dat_i+3]), int(data[dat_i+4]),
                )
            dat_i += 5
            i += 1
    except Exception:
        print("Failed to read triangles.")
        del triangles[i: ]
        return jms_data

    return jms_data


def write_jms(filepath, *, checksum=3251, materials=(), regions=(),
              nodes=(), markers=(), vertices=(), triangles=()):
    # If the path doesnt exist, create it
    if not exists(dirname(filepath)):
        makedirs(dirname(filepath))

    if not regions:
        regions = ("__unnamed", )

    if not materials:
        materials = (JmsMaterial("__unnamed", "<none>"), )

    with open(filepath, "w", encoding='latin1') as f:
        f.write("8200\n")
        f.write("%s\n" % (int(checksum) & 0xFFffFFff))

        f.write("%s\n" % len(nodes))
        for node in nodes:
            f.write("%s\n%s\n%s\n%s\t%s\t%s\t%s\n%s\t%s\t%s\n" % (
                node.name[: 31], node.first_child, node.sibling_index,
                float_to_str(node.rot_i),
                float_to_str(node.rot_j),
                float_to_str(node.rot_k),
                float_to_str(node.rot_w),
                float_to_str(node.pos_x),
                float_to_str(node.pos_y),
                float_to_str(node.pos_z),
                )
            )

        f.write("%s\n" % len(materials))
        for mat in materials:
            f.write("%s\n%s\n" % (mat.name, mat.tiff_path))

        f.write("%s\n" % len(markers))
        for marker in markers:
            f.write("%s\n%s\n%s\n%s\t%s\t%s\t%s\n%s\t%s\t%s\n%s\n" % (
                marker.name[: 31], marker.region, marker.parent,
                float_to_str(marker.rot_i),
                float_to_str(marker.rot_j),
                float_to_str(marker.rot_k),
                float_to_str(marker.rot_w),
                float_to_str(marker.pos_x),
                float_to_str(marker.pos_y),
                float_to_str(marker.pos_z),
                float_to_str(marker.radius)
                )
            )

        f.write("%s\n" % len(regions))
        for region in regions:
            f.write("%s\n" % region[: 31])

        f.write("%s\n" % len(vertices))
        for vert in vertices:
            f.write("%s\n%s\t%s\t%s\n%s\t%s\t%s\n%s\n%s\n%s\t%s\t%s\n" % (
                vert.node_0,
                float_to_str(vert.pos_x),
                float_to_str(vert.pos_y),
                float_to_str(vert.pos_z),
                float_to_str(vert.norm_i),
                float_to_str(vert.norm_j),
                float_to_str(vert.norm_k),
                vert.node_1,
                float_to_str(vert.node_1_weight),
                float_to_str(vert.tex_u),
                float_to_str(vert.tex_v),
                float_to_str(vert.tex_w),
                )
            )

        f.write("%s\n" % len(triangles))
        for tri in triangles:
            f.write("%s\t%s\n%s\t%s\t%s\n" % (
                tri.region, tri.shader,
                tri.v0, tri.v1, tri.v2
                )
            )
