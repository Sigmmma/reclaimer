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
        "name", "permutation",
        "region", "parent",
        "rot_i", "rot_j", "rot_k", "rot_w",
        "pos_x", "pos_y", "pos_z",
        "radius",
        )
    def __init__(self, name="", permutation="", region=-1, parent=0,
                 rot_i=0.0, rot_j=0.0, rot_k=0.0, rot_w=1.0,
                 pos_x=0.0, pos_y=0.0, pos_z=0.0, radius=0.0):
        self.name = name
        self.permutation = permutation
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
    permutation=%s,
    region=%s,  parent=%s,
    i=%s, j=%s, k=%s, w=%s,
    x=%s, y=%s, z=%s,
    radius=%s
)""" % (self.name, self.permutation, self.region, self.parent,
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


class JmsMeshData:
    verts = ()
    tris = ()

    def __init__(self, verts=None, tris=None):
        self.verts = verts if verts else []
        self.tris  = tris  if tris  else []


class JmsModel(JmsMeshData):
    name = ""

    node_list_checksum = 0
    nodes = ()
    materials = ()
    markers = ()
    regions = ()

    def __init__(self, name="", node_list_checksum=0, nodes=None,
                 materials=None, markers=None, regions=None,
                 verts=None, tris=None):
        self.name = name
        self.node_list_checksum = node_list_checksum
        self.nodes = nodes if nodes else []
        self.materials = materials if materials else []
        self.regions = regions if regions else []
        self.markers = markers if markers else []

        JmsMeshData.__init__(self, verts, tris)

    def verify_nodes_match(self, other_jms):
        errors = list(verify_jms(other_jms))
        if len(other_jms.nodes) != len(self.nodes):
            errors.append("Node counts do not match.")
            return

        for i in range(len(self.nodes)):
            fn = self.nodes[i]
            n = other_jms.nodes[i]
            if fn.name != n.name:
                errors.append("Names of nodes '%s' do not match." % i)
            elif fn.first_child != n.first_child:
                errors.append("First children of node '%s' do not match." % n.name)
            elif fn.sibling_index != n.sibling_index:
                errors.append("Sibling index of node '%s' do not match." % n.name)
            elif (abs(fn.rot_i - n.rot_i) > 0.00001 or
                  abs(fn.rot_j - n.rot_j) > 0.00001 or
                  abs(fn.rot_k - n.rot_k) > 0.00001 or
                  abs(fn.rot_w - n.rot_w) > 0.00001):
                errors.append("Rotations of node '%s' do not match." % n.name)
            elif (abs(fn.pos_x - n.pos_x) > 0.000001 or
                  abs(fn.pos_y - n.pos_y) > 0.000001 or
                  abs(fn.pos_z - n.pos_z) > 0.000001):
                errors.append("Positions of node '%s' do not match." % n.name)

        return errors

    def verify_jms(self):
        errors = []

        crc = self.node_list_checksum
        nodes = self.nodes
        mats  = self.materials
        markers = self.markers
        regions = self.regions

        if isinstance(self, MergedJmsModel):
            perm_meshes = self.perm_meshes
        else:
            perm_meshes = {self.name: JmsMeshData(self.verts, self.tris)}

        node_error = False

        node_ct = len(nodes)
        region_ct = len(regions)
        mat_ct = len(mats)

        if node_ct == 0:
            errors.append("No nodes. Jms models must contain at least one node.")
        elif node_ct >= 64:
            errors.append("Too many nodes. Max count is 64.")

        if mat_ct > 256:
            errors.append("Too many materials. Max count is 256.")

        if region_ct > 32:
            errors.append("Too many regions. Max count is 32.")

        marker_name_cts = {}
        for marker in markers:
            marker_name_cts[marker.name] = marker_name_cts.get(marker.name, 0) + 1

        if len(marker_name_cts) > 256:
            errors.append("Too many unique marker names. Max count is 256.")

        for name in sorted(marker_name_cts):
            if not name.strip(" "):
                errors.append("Detected unnamed markers.")
            if marker_name_cts[name] > 32:
                errors.append("Too many '%s' marker instances. Max count is 32.")

        for i in range(node_ct):
            n = nodes[i]
            if n.first_child >= len(nodes):
                errors.append("First child of node '%s' is invalid." % n.name)
            elif n.sibling_index >= len(nodes):
                errors.append("Sibling node of node '%s' is invalid." % n.name)
            elif len(n.name) >= 32:
                errors.append("Node name node '%s' is too long." % n.name)

        if errors:
            return errors

        err_str = "Invalid %s index in %s(s)."
        for region_name in regions:
            if len(region_name) >= 32:
                errors.append("Region name '%s' is too long." % region_name)

        for marker in markers:
            if marker.parent >= node_ct:
                errors.append(err_str % ("parent", "marker"))
            elif marker.region >= region_ct:
                errors.append(err_str % ("region", "marker"))
            elif len(marker.name) >= 32:
                errors.append("Marker name '%s' is too long." % marker.name)
            else:
                continue
            break

        for perm_name in sorted(perm_meshes):
            verts = perm_meshes[perm_name].verts
            tris  = perm_meshes[perm_name].tris
            vert_ct = len(verts)
            for tri in tris:
                if (tri.v0 < 0 or tri.v1 < 0 or tri.v2 < 0 or
                    tri.v0 >= vert_ct or tri.v1 >= vert_ct or tri.v2 >= vert_ct):
                    errors.append(err_str % ("vertex", "triangle"))
                elif tri.region >= region_ct:
                    errors.append(err_str % ("region", "triangle"))
                elif tri.shader >= mat_ct:
                    errors.append(err_str % ("shader", "triangle"))
                else:
                    continue
                break

            for vert in verts:
                if vert.node_0 >= node_ct:
                    errors.append(err_str % ("node_0", "vertex"))
                elif vert.node_1 >= node_ct:
                    errors.append(err_str % ("node_1", "vertex"))
                else:
                    continue
                break

        return errors


class MergedJmsModel(JmsModel):
    perm_meshes = ()

    def __init__(self, perm_meshes=None, *args):
        JmsModel.__init__(self, *args)
        self.perm_meshes = perm_meshes if perm_meshes else {}

    def merge_jms_models(self, *jms_models):
        all_errors = {}
        first_nodes = None
        self.__init__()

        if not jms_models:
            return

        jms_data = jms_models[0]
        for other_jms_data in jms_models[1: ]:
            errors = jms_data.verify_nodes_match(other_jms_data)
            if errors:
                all_errors[other_jms_data.name] = errors

        if all_errors:
            return all_errors


        # TODO: Merge jms models into self


        return all_errors


def read_jms(jms_string, stop_at="", perm_name="__unnamed"):
    jms_data = JmsModel(perm_name)
    nodes = jms_data.nodes
    materials = jms_data.materials
    markers = jms_data.markers
    regions = jms_data.regions
    verts = jms_data.verts
    tris = jms_data.tris

    jms_string = jms_string.replace("\n", "\t")

    data = tuple(d for d in jms_string.split("\t") if d)

    if data[0] != "8200":
        print("JMS identifier not found.")
        return jms_data

    try:
        jms_data.node_list_checksum = int(data[1])
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
                data[dat_i], perm_name, int(data[dat_i+1]), int(data[dat_i+2]),
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
        verts.extend((None, ) * int(data[dat_i]))
        dat_i += 1
        for i in range(len(verts)):
            verts[i] = JmsVertex(
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
        del verts[i: ]
        return jms_data

    if stop_at == "triangles": return jms_data

    # read the triangles
    try:
        i = 0
        tris.extend((None, ) * int(data[dat_i]))
        dat_i += 1
        for i in range(len(tris)):
            tris[i] = JmsTriangle(
                int(data[dat_i]), int(data[dat_i+1]),
                int(data[dat_i+2]), int(data[dat_i+3]), int(data[dat_i+4]),
                )
            dat_i += 5
            i += 1
    except Exception:
        print("Failed to read triangles.")
        del tris[i: ]
        return jms_data

    return jms_data


def write_jms(filepath, jms_data):
    checksum = jms_data.node_list_checksum
    materials = jms_data.materials
    regions = jms_data.regions
    nodes = jms_data.nodes
    markers = jms_data.markers
    verts = jms_data.verts
    tris = jms_data.tris

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

        f.write("%s\n" % len(verts))
        for vert in verts:
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

        f.write("%s\n" % len(tris))
        for tri in tris:
            f.write("%s\t%s\n%s\t%s\t%s\n" % (
                tri.region, tri.shader,
                tri.v0, tri.v1, tri.v2
                )
            )

# PLACEHOLDER ALIAS
verify_jms = JmsModel.verify_jms
