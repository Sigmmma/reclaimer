#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

__all__ = ( 'JmsModel', )


import math

from ..constants import JMS_PERM_CANNOT_BE_RANDOMLY_CHOSEN_TOKEN


class JmsModel:
    name = ""

    version = ""

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
                 verts=None, tris=None, version="8200"):

        name = name.strip(" ")
        perm_name = name
        if name.startswith(JMS_PERM_CANNOT_BE_RANDOMLY_CHOSEN_TOKEN):
            self.is_random_perm = False
            perm_name = perm_name.lstrip(JMS_PERM_CANNOT_BE_RANDOMLY_CHOSEN_TOKEN)

        self.lod_level = "superhigh"
        for lod_level in ("superhigh", "high", "medium", "superlow", "low"):
            if perm_name.lower().endswith(lod_level):
                perm_name = perm_name[: -len(lod_level)].strip(" ")
                self.lod_level = lod_level
                break

        node_list_checksum = node_list_checksum

        self.name = name
        self.version = version
        self.perm_name = perm_name
        self.node_list_checksum = node_list_checksum
        self.nodes = nodes if nodes else []
        self.materials = materials if materials else []
        self.regions = regions if regions else ["__unnamed"]
        self.markers = markers if markers else []
        self.verts   = verts   if verts   else []
        self.tris    = tris    if tris    else []

    def calculate_vertex_normals(self):
        verts = self.verts
        vert_ct = len(verts)
        sqrt = math.sqrt

        v_indices = (0, 1, 2)
        binormals = [[0, 0, 0, 0] for i in range(vert_ct)]
        tangents  = [[0, 0, 0, 0] for i in range(vert_ct)]
        for tri in self.tris:
            for tri_i in v_indices:
                v_i = tri[tri_i]
                if v_i >= vert_ct:
                    continue

                v0 = verts[v_i]
                v1 = verts[tri[(tri_i + 1) % 3]]
                v2 = verts[tri[(tri_i + 2) % 3]]
                b = binormals[v_i]
                t = tangents[v_i]

                x0 = v1.pos_x - v0.pos_x;
                x1 = v2.pos_x - v0.pos_x;
                y0 = v1.pos_y - v0.pos_y;
                y1 = v2.pos_y - v0.pos_y;
                z0 = v1.pos_z - v0.pos_z;
                z1 = v2.pos_z - v0.pos_z;


                s0 = v1.tex_u - v0.tex_u;
                s1 = v2.tex_u - v0.tex_u;
                t0 = v1.tex_v - v0.tex_v;
                t1 = v2.tex_v - v0.tex_v;

                r = s0 * t1 - s1 * t0
                if r == 0:
                    continue

                r = 1 / r

                bi = -(s0 * x1 - s1 * x0) * r
                bj = -(s0 * y1 - s1 * y0) * r
                bk = -(s0 * z1 - s1 * z0) * r
                b_len = sqrt(bi**2 + bj**2 + bk**2)

                ti = (t1 * x0 - t0 * x1) * r
                tj = (t1 * y0 - t0 * y1) * r
                tk = (t1 * z0 - t0 * z1) * r
                t_len = sqrt(ti**2 + tj**2 + tk**2)

                if b_len:
                    b[0] += bi / b_len
                    b[1] += bj / b_len
                    b[2] += bk / b_len
                    b[3] += 1

                if t_len:
                    t[0] += ti / t_len
                    t[1] += tj / t_len
                    t[2] += tk / t_len
                    t[3] += 1

        for i in range(vert_ct):
            vert = verts[i]
            b = binormals[i]
            t = tangents[i]

            if b[3]:
                vert.binorm_i = b[0] / b[3]
                vert.binorm_j = b[1] / b[3]
                vert.binorm_k = b[2] / b[3]

            if t[3]:
                vert.tangent_i = t[0] / t[3]
                vert.tangent_j = t[1] / t[3]
                vert.tangent_k = t[2] / t[3]

    def optimize_geometry(self, exact_compare=True):
        verts = self.verts
        vert_ct = len(verts)

        # this will map the verts to prune to the vert they are identical to
        dup_vert_map = {}
        similar_vert_map = {}

        if exact_compare:
            for i in range(len(verts)):
                v = verts[i]
                similar_vert_map.setdefault(
                    (v.pos_x, v.pos_y, v.pos_z), []).append(i)

            # loop over all verts and figure out which ones to replace with others
            for similar_vert_indices in similar_vert_map.values():
                for i in range(len(similar_vert_indices) - 1):
                    orig_idx = similar_vert_indices[i]
                    if orig_idx in dup_vert_map:
                        continue

                    vert_a = verts[orig_idx]
                    vert_a_i = vert_a.norm_i; vert_a_j = vert_a.norm_j; vert_a_k = vert_a.norm_k
                    vert_a_u = vert_a.tex_u;  vert_a_v = vert_a.tex_v
                    vert_a_n0 = vert_a.node_0; vert_a_n1 = vert_a.node_1
                    vert_a_n1w = vert_a.node_1_weight
                    for j in similar_vert_indices[i + 1: ]:
                        if j in dup_vert_map:
                            continue

                        vert_b = verts[j]
                        if (vert_a_i != vert_b.norm_i or
                            vert_a_j != vert_b.norm_j or
                            vert_a_k != vert_b.norm_k):
                            continue
                        elif vert_a_n1w != vert_b.node_1_weight:
                            continue
                        elif vert_a_n0 != vert_b.node_0 or vert_a_n1 != vert_b.node_1:
                            continue
                        elif vert_a_u != vert_b.tex_u or vert_a_v != vert_b.tex_v:
                            continue

                        dup_vert_map[j] = orig_idx
        else:
            for i in range(len(verts)):
                v = verts[i]
                similar_vert_map.setdefault(
                    (round(v.pos_x + 0.001, 3),
                     round(v.pos_y + 0.001, 3),
                     round(v.pos_z + 0.001, 3)), []).append(i)

            # loop over all verts and figure out which ones to replace with others
            for similar_vert_indices in similar_vert_map.values():
                for i in range(len(similar_vert_indices) - 1):
                    orig_idx = similar_vert_indices[i]
                    if orig_idx in dup_vert_map:
                        continue

                    vert_a = verts[orig_idx]
                    for j in similar_vert_indices[i + 1: ]:
                        if j not in dup_vert_map and verts[j] == vert_a:
                            dup_vert_map[j] = orig_idx

        if not dup_vert_map:
            # nothing to optimize away
            return

        # remap any duplicate triangle vert indices to the original
        get_mapped_vert = dup_vert_map.get
        for tri in self.tris:
            tri.v0 = get_mapped_vert(tri.v0, tri.v0)
            tri.v1 = get_mapped_vert(tri.v1, tri.v1)
            tri.v2 = get_mapped_vert(tri.v2, tri.v2)

        # copy the verts list so we can modify it without side-effects
        new_vert_ct = vert_ct - len(dup_vert_map)
        self.verts = new_verts = self.verts[: new_vert_ct]

        shift_map = {}
        copy_idx = vert_ct - 1
        # loop over all duplicate vert indices and move any vertices
        # on the high end of the vert list down to fill in the empty
        # spaces left by the duplicate verts we're removing.
        for dup_i in sorted(dup_vert_map):
            while copy_idx in dup_vert_map:
                # keep looping until we get to a vert we can move
                # from its high index to overwrite the low index dup
                copy_idx -= 1

            if copy_idx <= dup_i or dup_i >= new_vert_ct:
                # cant copy any lower. all upper index verts are duplicates
                break

            # move the vert from its high index to the low index dup
            new_verts[dup_i] = verts[copy_idx]
            shift_map[copy_idx] = dup_i
            copy_idx -= 1

        # remap any triangle vert indices
        get_mapped_vert = shift_map.get
        for tri in self.tris:
            tri.v0 = get_mapped_vert(tri.v0, tri.v0)
            tri.v1 = get_mapped_vert(tri.v1, tri.v1)
            tri.v2 = get_mapped_vert(tri.v2, tri.v2)

    def get_node_depths(self):
        node_depths = [-1] * len(self.nodes)
        if not self.nodes:
            return node_depths

        node_depths[0] = 0

        seen_hierarchy = set((-1, ))
        # figure out the hierarchy depth of each node
        for i in range(len(self.nodes)):
            child_depth = node_depths[i] + 1
            child_idx = self.nodes[i].first_child
            while (child_idx not in seen_hierarchy and
                   child_idx in range(len(self.nodes))):
                seen_hierarchy.add(child_idx)
                node_depths[child_idx] = child_depth
                child_idx = self.nodes[child_idx].sibling_index

        return node_depths

    def verify_nodes_valid(self):
        errors = []
        if len(self.nodes) == 0:
            errors.append("No nodes. Must contain at least one node.")
            return errors

        if len(self.nodes) >= 64:
            errors.append("Too many nodes. Max count is 64.")

        seen_names = set()
        for i in range(len(self.nodes)):
            n = self.nodes[i]
            if n.first_child >= len(self.nodes):
                errors.append("First child of node '%s' is invalid." % n.name)
            elif n.sibling_index >= len(self.nodes):
                errors.append("Sibling node of node '%s' is invalid." % n.name)
            elif len(n.name) >= 32:
                errors.append("Node name node '%s' is too long." % n.name)
            elif n.name.lower() in seen_names:
                errors.append("Multiple nodes named '%s'." % n.name)

            seen_names.add(n.name.lower())

        if self.nodes and self.nodes[0].sibling_index != -1:
            errors.append("Root node must not have siblings.")

        node_depths = self.get_node_depths()

        # make sure the nodes are sorted in increasing hierarchy depth
        curr_depth = node_depths[0]
        prev_name = ""
        for i in range(len(node_depths)):
            if curr_depth > node_depths[i]:
                errors.append("Nodes are not sorted by hierarchy depth.")
                break

            curr_name = self.nodes[i].name
            if curr_depth != node_depths[i]:
                curr_depth = node_depths[i]
            elif curr_name < prev_name:
                errors.append(("Nodes within depth %s are not sorted "
                               "alphabetically.") % curr_depth)
                break

            prev_name = curr_name

        sib_errors = set()
        child_errors = set()
        seen_hierarchy = set()
        for node in self.nodes:
            sib_idx = node.sibling_index
            child_idx = node.first_child

            if child_idx in child_errors:
                pass
            elif child_idx in seen_hierarchy:
                errors.append(
                    "Node %s is specified as the child of multiple nodes." %
                    self.nodes[child_idx].name)
            elif child_idx >= 0:
                seen_hierarchy.add(child_idx)
                seen_children = set()
                while child_idx >= 0:
                    child_node = self.nodes[child_idx]
                    if child_idx in seen_children:
                        errors.append("Circular reference in children " +
                                      "of node '%s'." % node.name)
                        break

                    seen_children.add(child_idx)
                    child_idx = child_node.first_child

            if sib_idx in sib_errors:
                pass
            elif sib_idx in seen_hierarchy:
                errors.append(
                    "Node %s is specified as the sibling of multiple nodes." %
                    self.nodes[sib_idx].name)
            elif sib_idx >= 0:
                seen_hierarchy.add(sib_idx)
                seen_siblings = set()
                while sib_idx >= 0:
                    sib_node = self.nodes[sib_idx]
                    if sib_idx in seen_siblings:
                        errors.append("Circular reference in siblings " +
                                      "of node '%s'." % node.name)
                        break

                    seen_siblings.add(sib_idx)
                    sib_idx = sib_node.sibling_index


        return errors

    def verify_models_match(self, other_jms):
        errors = list(other_jms.verify_jms())
        if len(other_jms.nodes) != len(self.nodes):
            errors.append("Node counts do not match.")
            return errors

        for i in range(len(self.nodes)):
            if self.nodes[i] != other_jms.nodes[i]:
                errors.append("Nodes '%s' do not match." % i)

        return errors

    def verify_jms(self):
        crc = self.node_list_checksum
        mats  = self.materials
        markers = self.markers
        regions = self.regions

        if isinstance(self, JmsModel):
            perm_meshes = {self.name: self}
        else:
            perm_meshes = self.perm_meshes

        node_error = False

        node_ct = len(self.nodes)
        region_ct = len(regions)
        mat_ct = len(mats)

        errors = self.verify_nodes_valid()
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
