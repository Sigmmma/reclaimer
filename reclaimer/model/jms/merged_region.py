#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

__all__ = ( 'MergedJmsRegion', )


from .mesh import ( PermutationMesh, GeometryMesh, )
from .model import JmsModel
from .triangle import JmsTriangle
from .vertex import JmsVertex


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

    def merge_jms_model(self, jms_model, merged_jms_materials):
        assert isinstance(jms_model, JmsModel)
        try:
            src_region_index = jms_model.regions.index(self.name)
        except ValueError:
            # this region is not in the jms model provided
            return

        lod_level = jms_model.lod_level
        perm_name = jms_model.perm_name

        if perm_name not in self.perm_meshes:
            self.perm_meshes[perm_name] = PermutationMesh()
            self.perm_meshes[perm_name].is_random_perm = jms_model.is_random_perm

        perm_mesh = self.perm_meshes[perm_name]
        # copy the markers from the JmsModel we're given for this region,
        # BUT only do so if the lod_level is superhigh(this is what tool
        # does, and it makes sense to do it this way to prevent duplicates).
        if jms_model.lod_level == "superhigh":
            for marker in jms_model.markers:
                if marker.region == src_region_index:
                    perm_mesh.markers.append(marker)

        mesh_data = perm_mesh.lod_meshes.setdefault(lod_level, {})

        src_verts = jms_model.verts
        src_tris  = jms_model.tris
        region_verts = []
        region_tris = [None] * len(src_tris)

        mat_indices_by_name, i = {}, 0
        for mat in merged_jms_materials:
            mat_indices_by_name.setdefault(mat.name, []).append(i)
            i += 1

        mat_map, i = [0] * len(jms_model.materials), 0
        for mat in jms_model.materials:
            mat_map[i] = mat_indices_by_name[mat.name].pop(0)
            i += 1

        vert_map = dict()
        get_add_vert = vert_map.setdefault
        v_base = len(region_verts)
        tri_ct = 0
        mat_nums = set()
        for tri in src_tris:
            if tri.region == src_region_index:
                mat_num = mat_map[tri.shader]
                # region number doesnt matter at this point for triangles
                # since it isnt stored in compiled models, so set it to -1
                tri = JmsTriangle(-1, mat_num, tri.v0, tri.v1, tri.v2)
                tri.v0 = get_add_vert(tri.v0, v_base + len(vert_map))
                tri.v1 = get_add_vert(tri.v1, v_base + len(vert_map))
                tri.v2 = get_add_vert(tri.v2, v_base + len(vert_map))
                mat_nums.add(mat_num)
                region_tris[tri_ct] = tri
                tri_ct += 1

        if tri_ct == 0:
            return

        # collect all the verts and triangles used by this region
        region_verts.extend([None] * len(vert_map))
        for i, j in vert_map.items():
            v = src_verts[i]
            region_verts[j] = JmsVertex(
                v.node_0, v.pos_x, v.pos_y, v.pos_z,
                v.norm_i, v.norm_j, v.norm_k, v.node_1, v.node_1_weight,
                v.tex_u, v.tex_v, v.tex_w,
                v.binorm_i,  v.binorm_j,  v. binorm_k,
                v.tangent_i, v.tangent_j, v.tangent_k)

        del region_tris[tri_ct: ]

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
            get_add_vert = vert_map.setdefault
            v_base = len(mat_verts)
            tri_ct = 0
            for tri in region_tris:
                if tri.shader == mat_num:
                    tri.v0 = get_add_vert(tri.v0, v_base + len(vert_map))
                    tri.v1 = get_add_vert(tri.v1, v_base + len(vert_map))
                    tri.v2 = get_add_vert(tri.v2, v_base + len(vert_map))
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
