import re

from os import makedirs
from os.path import dirname, exists
from .util import float_to_str


class JmsNode:
    __slots__ = (
        "name",
        "first_child", "sibling_index", "parent_index",
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
        self.parent_index = -1

    def __repr__(self):
        return """JmsNode(name=%s,
    first_child=%s, sibling_index=%s,
    i=%s, j=%s, k=%s, w=%s,
    x=%s, y=%s, z=%s
)""" % (self.name, self.first_child, self.sibling_index,
        self.rot_i, self.rot_j, self.rot_k, self.rot_w,
        self.pos_x, self.pos_y, self.pos_z)

    def __eq__(self, other):
        if not isinstance(other, JmsNode):
            return False
        elif self.name != other.name:
            return False
        elif self.first_child != other.first_child:
            return False
        elif self.sibling_index != other.sibling_index:
            return False
        elif (abs(self.rot_i - other.rot_i) > 0.00001 or
              abs(self.rot_j - other.rot_j) > 0.00001 or
              abs(self.rot_k - other.rot_k) > 0.00001 or
              abs(self.rot_w - other.rot_w) > 0.00001):
            return False
        elif (abs(self.pos_x - other.pos_x) > 0.000001 or
              abs(self.pos_y - other.pos_y) > 0.000001 or
              abs(self.pos_z - other.pos_z) > 0.000001):
            return False
        return True


class JmsMaterial:
    __slots__ = (
        "name", "tiff_path",
        "shader_path", "shader_type"
        )
    def __init__(self, name="__unnamed", tiff_path="<none>"):
        self.name = name
        self.tiff_path = tiff_path
        self.shader_path = name
        self.shader_type = "shader"

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
    def __init__(self, name="", permutation="", region=0, parent=0,
                 rot_i=0.0, rot_j=0.0, rot_k=0.0, rot_w=1.0,
                 pos_x=0.0, pos_y=0.0, pos_z=0.0, radius=0.0):
        self.name = name
        self.permutation = permutation
        self.parent = parent
        self.region = max(0, region)
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

    def __eq__(self, other):
        if not isinstance(other, JmsMarker):
            return False
        elif self.name != other.name:
            return False
        elif self.permutation != other.permutation:
            return False
        elif self.region != other.region:
            return False
        elif abs(self.radius - other.radius) > 0.00001:
            return False
        elif (abs(self.rot_i - other.rot_i) > 0.00001 or
              abs(self.rot_j - other.rot_j) > 0.00001 or
              abs(self.rot_k - other.rot_k) > 0.00001 or
              abs(self.rot_w - other.rot_w) > 0.00001):
            return False
        elif (abs(self.pos_x - other.pos_x) > 0.000001 or
              abs(self.pos_y - other.pos_y) > 0.000001 or
              abs(self.pos_z - other.pos_z) > 0.000001):
            return False
        return True


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
        if node_1_weight <= 0:
            node_1 = -1
            node_1_weight = 0

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

    def __getitem__(self, index):
        if   index == 0: return self.v0
        elif index == 1: return self.v1
        elif index == 2: return self.v2
        raise IndexError("Triangle indices must be in range(0, 3)")

    def __repr__(self):
        return """JmsTriangle(
    region=%s, shader=%s,
    v0=%s, v1=%s, v2=%s
)""" % (self.region, self.shader,
        self.v0, self.v1, self.v2)


class JmsModel:
    name = ""

    perm_name = "__base"
    lod_level = "superhigh"
    is_random_perm = True

    node_list_checksum = 0
    nodes = ()
    materials = ()
    regions = ()
    markers = ()
    verts   = ()
    tris    = ()

    def __init__(self, name="", node_list_checksum=0, nodes=None,
                 materials=None, markers=None, regions=None,
                 verts=None, tris=None):

        name = name.strip(" ")
        perm_name = name
        if name.startswith("~"):
            self.is_random_perm = False
            perm_name = perm_name.lstrip("~")

        for lod_level in ("superhigh", "high", "medium", "superlow", "low"):
            if perm_name.lower().endswith(lod_level):
                perm_name = perm_name[: -len(lod_level)].strip(" ")
                self.lod_level = lod_level
                break

        node_list_checksum = node_list_checksum & 0xFFffFFff
        if node_list_checksum >= (1<<31):
            node_list_checksum = node_list_checksum - 0x100000000

        self.name = name
        self.perm_name = perm_name
        self.node_list_checksum = node_list_checksum
        self.nodes = nodes if nodes else []
        self.materials = materials if materials else []
        self.regions = regions if regions else []
        self.markers = markers if markers else []
        self.verts   = verts   if verts   else []
        self.tris    = tris    if tris    else []

    def verify_nodes_valid(self):
        errors = []
        if len(self.nodes) == 0:
            errors.append("No nodes. Jms models must contain at least one node.")
        elif len(self.nodes) >= 64:
            errors.append("Too many nodes. Max count is 64.")

        for i in range(len(self.nodes)):
            n = self.nodes[i]
            if n.first_child >= len(self.nodes):
                errors.append("First child of node '%s' is invalid." % n.name)
            elif n.sibling_index >= len(self.nodes):
                errors.append("Sibling node of node '%s' is invalid." % n.name)
            elif len(n.name) >= 32:
                errors.append("Node name node '%s' is too long." % n.name)

        if self.nodes and self.nodes[0].sibling_index != -1:
            errors.append("Root node must not have siblings.")

        seen_hierarchy = set()
        for node in self.nodes:
            sib_idx = node.sibling_index
            child_idx = node.first_child
            if sib_idx in seen_hierarchy or child_idx in seen_hierarchy:
                errors.append("Node hierarchy is janked up. " +
                              "Can't really explain why tho.")

            if sib_idx >= 0:
                seen_hierarchy.add(sib_idx)

            if child_idx >= 0:
                seen_hierarchy.add(child_idx)

        # TODO: Check hierarchy for non-halo sorting
        if not errors:
            # check all nodes to make sure their hierarchy is valid
            all_seen_siblings = set()
            all_seen_children = set()

            for node in self.nodes:
                seen_siblings = set()
                seen_children = set()

                sib_idx = node.sibling_index
                child_idx = node.first_child

                if sib_idx >= 0 and sib_idx in all_seen_siblings:
                    errors.append(("Sibling index in node '%s' is reused " +
                                   "in another node.") % node.name)

                if child_idx >= 0 and child_idx in all_seen_children:
                    errors.append(("Child index in node '%s' is reused " +
                                   "in another node.") % node.name)

                all_seen_siblings.add(sib_idx)
                all_seen_children.add(child_idx)

                while sib_idx >= 0:
                    sib_node = self.nodes[sib_idx]
                    if sib_idx in seen_siblings:
                        errors.append("Circular reference in siblings " +
                                      "of node '%s'." % node.name)

                    seen_siblings.add(sib_idx)
                    sib_idx = sib_node.sibling_index

                while child_idx >= 0:
                    child_node = self.nodes[child_idx]
                    if child_idx in seen_children:
                        errors.append("Circular reference in children " +
                                      "of node '%s'." % node.name)

                    seen_children.add(child_idx)
                    child_idx = child_node.first_child


        return errors

    def verify_models_match(self, other_jms):
        errors = list(verify_jms(other_jms))
        if len(other_jms.nodes) != len(self.nodes):
            errors.append("Node counts do not match.")
            return errors
        elif len(other_jms.materials) != len(self.materials):
            errors.append("Material counts do not match.")
            return errors

        for i in range(len(self.nodes)):
            if self.nodes[i] != other_jms.nodes[i]:
                errors.append("Nodes '%s' do not match." % i)

        for i in range(len(self.materials)):
            mat = self.materials[i]
            other_mat = other_jms.materials[i]
            if mat.name != other_mat.name:
                errors.append("Names of materials '%s' do not match." % i)

        return errors

    def verify_jms(self):
        crc = self.node_list_checksum
        mats  = self.materials
        markers = self.markers
        regions = self.regions

        if isinstance(self, MergedJmsModel):
            perm_meshes = self.perm_meshes
        else:
            perm_meshes = {self.name: self}

        node_error = False

        node_ct = len(self.nodes)
        region_ct = len(regions)
        mat_ct = len(mats)

        errors = self.verify_nodes_valid()

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


class GeometryMesh:
    verts = ()
    tris  = ()
    local_nodes = []
    def __init__(self, verts=(), tris=()):
        self.verts = verts if verts else []
        self.tris  = tris  if tris  else []


class PermutationMesh:
    markers = ()
    lod_meshes = ()
    is_random_perm = True

    def __init__(self):
        self.markers = []
        self.lod_meshes = {}


class MergedJmsRegion:
    name = ""
    perm_meshes = ()
    _split_by_shader = True

    def __init__(self, name, *jms_models, split_by_shader=True):
        self.name = name
        self._split_by_shader = split_by_shader
        self.perm_meshes = {}

        for jms_model in jms_models:
            self.merge_jms_model(jms_model)

    def merge_jms_model(self, jms_model):
        assert isinstance(jms_model, JmsModel)
        try:
            reg_idx = jms_model.regions.index(self.name)
        except ValueError:
            # this region is not in the jms model provided
            return

        lod_level = jms_model.lod_level
        perm_name = jms_model.perm_name

        if perm_name in self.perm_meshes:
            perm_mesh = self.perm_meshes[perm_name] 
        else:
            perm_mesh = self.perm_meshes[perm_name] = PermutationMesh()
            perm_mesh.is_random_perm = jms_model.is_random_perm

            # copy the markers from the first JmsModel
            # we're given for this region
            for marker in jms_model.markers:
                if marker.region == reg_idx:
                    perm_mesh.markers.append(marker)

        mesh_data = perm_mesh.lod_meshes.setdefault(lod_level, {})

        src_verts = jms_model.verts
        src_tris  = jms_model.tris
        region_verts = []
        region_tris = []

        vert_map = dict()
        v_base = len(region_verts)
        tri_ct = 0
        mat_nums = set()
        for tri in src_tris:
            if tri.region == reg_idx:
                tri.v0 = vert_map.setdefault(tri.v0, v_base + len(vert_map))
                tri.v1 = vert_map.setdefault(tri.v1, v_base + len(vert_map))
                tri.v2 = vert_map.setdefault(tri.v2, v_base + len(vert_map))
                mat_nums.add(tri.shader)
                tri_ct += 1

        if tri_ct == 0:
            return

        # collect all the verts and triangles used by this region
        region_verts.extend([None] * len(vert_map))
        for i, j in vert_map.items():
            region_verts[j] = src_verts[i]

        i = len(region_tris)
        region_tris.extend([None] * tri_ct)
        for tri in src_tris:
            if tri.region == reg_idx:
                region_tris[i] = tri
                i += 1

        if len(mat_nums) == 1 or not self._split_by_shader:
            for mat_num in mat_nums: break
            if not self._split_by_shader:
                mat_num = -1

            mesh_data[mat_num] = GeometryMesh()
            mesh_data[mat_num].verts = region_verts
            mesh_data[mat_num].tris  = region_tris
            return

        # make a mesh for each material
        for mat_num in mat_nums:
            if mat_num not in mesh_data:
                mesh_data[mat_num] = GeometryMesh()

            mat_verts = mesh_data[mat_num].verts
            mat_tris  = mesh_data[mat_num].tris

            vert_map = dict()
            v_base = len(mat_verts)
            tri_ct = 0
            for tri in region_tris:
                if tri.shader == mat_num:
                    tri.v0 = vert_map.setdefault(tri.v0, v_base + len(vert_map))
                    tri.v1 = vert_map.setdefault(tri.v1, v_base + len(vert_map))
                    tri.v2 = vert_map.setdefault(tri.v2, v_base + len(vert_map))
                    tri_ct += 1

            mat_verts.extend([None] * len(vert_map))
            for i, j in vert_map.items():
                mat_verts[j] = region_verts[i]

            i = len(mat_tris)
            mat_tris.extend([None] * tri_ct)
            for tri in region_tris:
                if tri.shader == mat_num:
                    mat_tris[i] = tri
                    i += 1


class MergedJmsModel:
    node_list_checksum = 0
    nodes = ()
    materials = ()
    regions = ()
            
    _u_scale = 1.0
    _v_scale = 1.0

    def __init__(self, *jms_models):
        self.nodes = []
        self.materials = []
        self.regions = {}

        for jms_model in jms_models:
            self.merge_jms_model(jms_model)

    @property
    def u_scale(self):
        return self._u_scale
    @u_scale.setter
    def u_scale(self, new_scale):
        factor = 0 if new_scale == 0 else self._u_scale / new_scale
        for region in self.regions.values():
            for perm_mesh in region.perm_meshes.values():
                for meshes in perm_mesh.lod_meshes.values():
                    for lod_mesh_list in perm_mesh.lod_meshes.values():
                        for mesh in lod_mesh_list.values():
                            for vert in mesh.verts:
                                # nesting from the pits of hell
                                vert.tex_u *= factor

        self._u_scale = new_scale

    @property
    def v_scale(self):
        return self._v_scale
    @v_scale.setter
    def v_scale(self, new_scale):
        factor = 0 if new_scale == 0 else self._v_scale / new_scale
        for region in self.regions.values():
            for perm_mesh in region.perm_meshes.values():
                for meshes in perm_mesh.lod_meshes.values():
                    for lod_mesh_list in perm_mesh.lod_meshes.values():
                        for mesh in lod_mesh_list.values():
                            for vert in mesh.verts:
                                # nesting from the pits of hell
                                vert.tex_v *= factor

        self._v_scale = new_scale

    def calc_uv_scales(self):
        u_scale = self.u_scale
        v_scale = self.v_scale
        calc_u_scale = 0.0
        calc_v_scale = 0.0
        for region in self.regions.values():
            for perm_mesh in region.perm_meshes.values():
                for meshes in perm_mesh.lod_meshes.values():
                    for lod_mesh_list in perm_mesh.lod_meshes.values():
                        for mesh in lod_mesh_list.values():
                            for vert in mesh.verts:
                                scale = abs(vert.tex_u * u_scale)
                                calc_u_scale = max(scale, calc_u_scale)
                                scale = abs(vert.tex_v * v_scale)
                                calc_v_scale = max(scale, calc_v_scale)

        return calc_u_scale, calc_v_scale

    verify_models_match = JmsModel.verify_models_match

    def merge_jms_model(self, other_model):
        all_errors = {}
        first_nodes = None

        if not other_model:
            return

        if not self.nodes:
            self.node_list_checksum = other_model.node_list_checksum
            self.nodes = list(other_model.nodes)
            self.materials = list(other_model.materials)
            self.regions = {}

        errors = self.verify_models_match(other_model)
        if errors:
            return errors

        for region in other_model.regions:
            if region not in self.regions:
                self.regions[region] = MergedJmsRegion(region)

            self.regions[region].merge_jms_model(other_model)

        return all_errors


def read_jms(jms_string, stop_at="", perm_name="__unnamed"):
    jms_data = JmsModel(perm_name)
    perm_name = jms_data.perm_name
    nodes = jms_data.nodes
    materials = jms_data.materials
    markers = jms_data.markers
    regions = jms_data.regions
    verts = jms_data.verts
    tris = jms_data.tris

    jms_string = jms_string.replace("\n", "\t")

    data = tuple(d for d in jms_string.split("\t") if d)

    if data[0] != "8200":
        print("JMS identifier '8200' not found.")
        return jms_data

    try:
        node_list_checksum = int(data[1]) & 0xFFffFFff
        if node_list_checksum >= (1<<31):
            node_list_checksum = node_list_checksum - 0x100000000
        jms_data.node_list_checksum = node_list_checksum
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
            
        parented_nodes = set()
        # setup the parent node hierarchy
        for parent_idx in range(len(nodes)):
            node = nodes[parent_idx]
            if node.first_child > 0:
                sib_idx = node.first_child
                seen_nodes = set()
                while sib_idx >= 0:
                    if (sib_idx in seen_nodes or sib_idx == parent_idx or
                        sib_idx >= len(nodes)):
                        break
                    seen_nodes.add(sib_idx)
                    parented_nodes.add(sib_idx)
                    sib_node = nodes[sib_idx]
                    sib_node.parent_index = parent_idx
                    sib_idx = sib_node.sibling_index
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
