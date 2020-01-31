#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

__all__ = ( 'MergedJmsModel', )


from .model import JmsModel
from .node import JmsNode
from .material import JmsMaterial
from .merged_region import MergedJmsRegion


class MergedJmsModel:
    node_list_checksum = 0
    nodes = ()
    materials = ()
    regions = ()

    u_scale = 1.0
    v_scale = 1.0

    def __init__(self, *jms_models):
        self.nodes = []
        self.materials = []
        self.regions = {}

        for jms_model in jms_models:
            self.merge_jms_model(jms_model)

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
                                calc_u_scale = max(abs(vert.tex_u * u_scale),
                                                   calc_u_scale)
                                calc_v_scale = max(abs(vert.tex_v * v_scale),
                                                   calc_v_scale)

        return calc_u_scale, calc_v_scale

    verify_models_match = JmsModel.verify_models_match

    def merge_jms_model(self, other_model):
        all_errors = {}
        first_nodes = None

        if not other_model:
            return

        if not self.nodes:
            self.node_list_checksum = other_model.node_list_checksum
            self.nodes = []
            self.materials = []
            for node in other_model.nodes:
                self.nodes.append(
                    JmsNode(
                        node.name, node.first_child, node.sibling_index,
                        node.rot_i, node.rot_j, node.rot_k, node.rot_w,
                        node.pos_x, node.pos_y, node.pos_z, node.parent_index)
                    )

            for mat in other_model.materials:
                self.materials.append(
                    JmsMaterial(
                        mat.name, mat.tiff_path, mat.shader_path,
                        mat.shader_type, mat.properties)
                    )

            self.regions = {}

        errors = self.verify_models_match(other_model)
        if errors:
            return errors

        new_mat_counts = {}
        for mat in self.materials:
            new_mat_counts[mat.name] = new_mat_counts.get(mat.name, 0) - 1

        default_mats = {}
        for mat in other_model.materials:
            default_mats.setdefault(mat.name, mat)
            new_mat_counts[mat.name] = new_mat_counts.get(mat.name, 0) + 1

        for mat_name, mat_ct in new_mat_counts.items():
            if mat_ct > 0:
                self.materials.extend((default_mats[mat_name], ) * mat_ct)

        # merge each region from the other model into this ones regions
        for region in other_model.regions:
            if region not in self.regions:
                self.regions[region] = MergedJmsRegion(region)

            self.regions[region].merge_jms_model(other_model, self.materials)

        # correct the region index numbers for each marker in the regions
        i = 0
        for region_name in sorted(self.regions):
            perm_meshes = self.regions[region_name].perm_meshes
            for perm_mesh in perm_meshes.values():
                for marker in perm_mesh.markers:
                    marker.region = i
            i += 1

        return all_errors
