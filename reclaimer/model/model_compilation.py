#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#
import array
import sys

from math import sqrt
from struct import Struct as PyStruct

from reclaimer.jm.constants import SCALE_INTERNAL_TO_JMS
from reclaimer.model.constants import (
    HALO_1_MAX_MATERIALS, HALO_1_MAX_REGIONS,
    HALO_1_MAX_GEOMETRIES_PER_MODEL, HALO_1_MAX_PARTS_PER_GEOMETRY,
    HALO_1_MAX_MARKERS_PER_PERM, HALO_1_NAME_MAX_LEN
    )
from reclaimer.jm.jms import GeometryMesh
from reclaimer.model.stripify import Stripifier
from reclaimer.model import util


def compile_gbxmodel(mod2_tag, merged_jms, ignore_errors=False, pos_scale=1.0):
    tagdata = mod2_tag.data.tagdata
    tagdata.flags.parts_have_local_nodes = False
    pos_scale /= SCALE_INTERNAL_TO_JMS

    u_scale, v_scale = merged_jms.calc_uv_scales()
    if u_scale < 1:
        u_scale = 1
    if v_scale < 1:
        v_scale = 1
    tagdata.base_map_u_scale = merged_jms.u_scale = u_scale
    tagdata.base_map_v_scale = merged_jms.v_scale = v_scale

    tagdata.node_list_checksum = merged_jms.node_list_checksum

    errors = []
    if len(merged_jms.materials) > HALO_1_MAX_MATERIALS:
        errors.append("Too many materials. Max count is %s." % (HALO_1_MAX_MATERIALS))

    if len(merged_jms.regions) > HALO_1_MAX_REGIONS:
        errors.append("Too many regions. Max count is %s." % (HALO_1_MAX_REGIONS))

    if errors and not ignore_errors:
        return errors

    # make nodes
    mod2_nodes = tagdata.nodes.STEPTREE
    del mod2_nodes[:]
    for node in merged_jms.nodes:
        mod2_nodes.append()
        mod2_node = mod2_nodes[-1]

        mod2_node.name = node.name[: HALO_1_NAME_MAX_LEN]
        mod2_node.next_sibling_node = node.sibling_index
        mod2_node.first_child_node = node.first_child
        mod2_node.parent_node = node.parent_index
        mod2_node.translation[:] = node.pos_x * pos_scale,\
                                   node.pos_y * pos_scale,\
                                   node.pos_z * pos_scale
        mod2_node.rotation[:] = node.rot_i, node.rot_j,\
                                node.rot_k, node.rot_w

        if node.parent_index >= 0:
            mod2_node.distance_from_parent = sqrt(
                node.pos_x**2 + node.pos_y**2 + node.pos_z**2) * pos_scale


    # make shader references
    mod2_shaders = tagdata.shaders.STEPTREE
    del mod2_shaders[:]
    for mat in merged_jms.materials:
        mod2_shaders.append()
        mod2_shader = mod2_shaders[-1]

        mod2_shader.shader.filepath   = mat.shader_path
        mod2_shader.permutation_index = mat.permutation_index

        if mat.shader_type:
            mod2_shader.shader.tag_class.set_to(mat.shader_type)
        else:
            mod2_shader.shader.tag_class.set_to("shader")

        shdr_name = mod2_shader.shader.filepath.split("\\")[-1].lower()

    # make regions
    mod2_regions = tagdata.regions.STEPTREE
    del mod2_regions[:]

    global_markers = {}
    geom_meshes = []
    for region_name in sorted(merged_jms.regions):
        region = merged_jms.regions[region_name]

        mod2_regions.append()
        mod2_region = mod2_regions[-1]
        mod2_region.name = region_name[: HALO_1_NAME_MAX_LEN]

        mod2_perms = mod2_region.permutations.STEPTREE
        for perm_name in sorted(region.perm_meshes):
            perm = region.perm_meshes[perm_name]

            mod2_perms.append()
            mod2_perm = mod2_perms[-1]
            mod2_perm.name = perm_name[: HALO_1_NAME_MAX_LEN]

            mod2_perm.flags.cannot_be_chosen_randomly = not perm.is_random_perm

            perm_added = False
            skipped_lods = []
            for i in range(len(util.LOD_NAMES)):
                lod_name = util.LOD_NAMES[i]
                if not perm.lod_meshes.get(lod_name):
                    if skipped_lods is not None:
                        skipped_lods.append(i)
                    continue

                geom_index = len(geom_meshes)
                lod_mesh = perm.lod_meshes[lod_name]
                geom_meshes.append(lod_mesh)

                lods_to_set = list(range(i, 5))
                if skipped_lods:
                    lods_to_set.extend(skipped_lods)
                    skipped_lods = None

                for name in (util.LOD_NAMES[i] for i in lods_to_set):
                    setattr(mod2_perm, "%s_geometry_block" % name, geom_index)

                perm_added = True

            if len(perm.markers) > HALO_1_MAX_MARKERS_PER_PERM and not ignore_errors:
                return ("Cannot add more than %s markers to a permutation. "
                        "This model would contain %s markers." % (
                            HALO_1_MAX_MARKERS_PER_PERM, len(perm.markers)), )

            perm_added |= bool(perm.markers)
            mod2_markers = mod2_perm.local_markers.STEPTREE
            for marker in perm.markers:
                mod2_markers.append()
                mod2_marker = mod2_markers[-1]

                mod2_marker.name = marker.name[: HALO_1_NAME_MAX_LEN]
                mod2_marker.node_index = marker.parent
                mod2_marker.translation[:] = marker.pos_x * pos_scale,\
                                             marker.pos_y * pos_scale,\
                                             marker.pos_z * pos_scale
                mod2_marker.rotation[:] = marker.rot_i, marker.rot_j,\
                                          marker.rot_k, marker.rot_w


            if not(perm_added or ignore_errors):
                del mod2_perms[-1]
                continue

    if len(geom_meshes) > HALO_1_MAX_GEOMETRIES_PER_MODEL and not ignore_errors:
        return ("Cannot add more than %s geometries to a model.\n"
                "Each permutation in each region in each LOD is counted as "
                "one geometry.\nThis model would contain %s geometries." % (
                    HALO_1_MAX_GEOMETRIES_PER_MODEL, len(geom_meshes)), )

    # make the markers
    mod2_marker_headers = tagdata.markers.STEPTREE
    del mod2_marker_headers[:]
    for marker_name in sorted(global_markers):
        marker_list = global_markers[marker_name]
        mod2_marker_headers.append()
        mod2_marker_header = mod2_marker_headers[-1]

        mod2_marker_header.name = marker_name[: HALO_1_NAME_MAX_LEN]
        mod2_marker_list = mod2_marker_header.marker_instances.STEPTREE

        for marker in marker_list:
            mod2_marker_list.append()
            mod2_marker = mod2_marker_list[-1]

            # figure out which permutation index this marker
            # matches for all the permutations in its region
            i = perm_index = 0
            for perm in mod2_regions[marker.region].permutations.STEPTREE:
                if perm.name == marker.permutation:
                    perm_index = i
                    break
                i += 1

            mod2_marker.region_index = marker.region
            mod2_marker.permutation_index = perm_index
            mod2_marker.node_index = marker.parent
            mod2_marker.translation[:] = marker.pos_x * pos_scale,\
                                         marker.pos_y * pos_scale,\
                                         marker.pos_z * pos_scale
            mod2_marker.rotation[:] = marker.rot_i, marker.rot_j,\
                                      marker.rot_k, marker.rot_w


    # calculate triangle strips
    stripped_geom_meshes = []
    for geom_idx in range(len(geom_meshes)):
        material_meshes = {}
        stripped_geom_meshes.append(material_meshes)
        for mat_idx in sorted(geom_meshes[geom_idx]):
            material_meshes[mat_idx] = mesh_list = []
            geom_mesh = geom_meshes[geom_idx][mat_idx]
            all_verts = geom_mesh.verts

            strp = Stripifier()
            strp.max_strip_len  = util.MAX_STRIP_LEN
            strp.max_vert_count = util.MAX_VERT_COUNT
            strp.load_mesh(geom_mesh.tris, True)
            strp.make_strips()
            strp.link_strips()

            strips_verts   = [all_verts]
            strips_indices = [strp.translate_strip(strp.get_strip(i))
                              for i in range(strp.get_strip_count())]

            if len(strips_indices) > 1:
                # multiple strips due to model being huge.
                # reindex verts to localize them for each strip
                strips_verts = []
                for i, indices in enumerate(strips_indices):
                    # this'll map the existing vert indices
                    # in the strip to the new, localized ones
                    index_map      = sorted(set(indices))
                    inv_index_map  = {vi: j for j, vi in enumerate(index_map)}
                    strips_indices[i] = list(map(inv_index_map.__getitem__, indices))
                    strips_verts.append([all_verts[vi] for vi in index_map])

            elif not strips_indices:
                # no strips. add a degen tri one so things render properly
                strips_verts = [util.EMPTY_GEOM_VERTS]
                strips_indices  = [(0, 1, 2)]
                
            for verts, strip in zip(strips_verts, strips_indices):
                mesh_list.append((verts, strip))


    # make the geometries
    mod2_geoms = tagdata.geometries.STEPTREE
    del mod2_geoms[:]
    vert_packer = PyStruct(">14f2h2f").pack_into
    for geom_idx in range(len(stripped_geom_meshes)):
        mod2_geoms.append()
        mod2_parts = mod2_geoms[-1].parts.STEPTREE

        part_cts = [len(m) for m in stripped_geom_meshes[geom_idx].values()]
        if sum(part_cts) > HALO_1_MAX_PARTS_PER_GEOMETRY and not ignore_errors:
            return (
                "Cannot add more than %s parts to a geometry. "
                "Each permutation in each region in each LOD is counted "
                "as one geometry.\nEach geometry is split into single-"
                "material parts containing less than %s triangles.\n"
                "Geometry %s would contain %s materials split into "
                "this many parts each:\n%s" % (
                    HALO_1_MAX_PARTS_PER_GEOMETRY, util.MAX_STRIP_LEN,
                    geom_idx, len(part_cts), part_cts
                    ),
                )

        for mat_idx in sorted(stripped_geom_meshes[geom_idx]):
            geom_mesh_list = stripped_geom_meshes[geom_idx][mat_idx]

            for verts, strip in geom_mesh_list:
                mod2_parts.append()
                mod2_part = mod2_parts[-1]
                mod2_verts = mod2_part.uncompressed_vertices.STEPTREE

                vert_ct = len(verts)
                mod2_verts.extend(len(verts))
                mod2_part.shader_index = mat_idx

                # TODO: Modify this to take into account local nodes....
                # honestly though, who the fuck is going to care? fuck it.

                # make raw vert/tri reflexives and replace the ones in the part
                mod2_part.uncompressed_vertices = util.mod2_verts_def.build()
                mod2_part.triangles             = util.mod2_tri_strip_def.build()

                mod2_verts = bytearray(68 * len(verts))
                mod2_tris  = array.array("H")

                mod2_tris.extend(strip)
                mod2_tris.extend([0xFFff] * ((3-len(strip)%3)%3))

                sys.byteorder == "big" or mod2_tris.byteswap()

                cent_x = cent_y = cent_z = 0
                cent_scale = 1 / vert_ct
                for i, vert in enumerate(verts):
                    x, y, z = (vert.pos_x * pos_scale,
                               vert.pos_y * pos_scale,
                               vert.pos_z * pos_scale)
                    vert_packer(
                        mod2_verts, i*68, x, y, z,
                        vert.norm_i, vert.norm_j, vert.norm_k,
                        vert.binorm_i, vert.binorm_j, vert.binorm_k,
                        vert.tangent_i, vert.tangent_j, vert.tangent_k,
                        vert.tex_u / u_scale, (1.0 - vert.tex_v) / v_scale,
                        vert.node_0, vert.node_1,
                        1 - vert.node_1_weight, vert.node_1_weight)

                    cent_x += x * cent_scale
                    cent_y += y * cent_scale
                    cent_z += z * cent_scale

                mod2_part.centroid_translation[:] = [cent_x, cent_y, cent_z]

                # replace the rawdata in the reflexives now that we've packed it
                mod2_part.triangles.STEPTREE             = mod2_tris.tobytes()
                mod2_part.uncompressed_vertices.STEPTREE = mod2_verts


    # calculate final bits of data before saving
    mod2_tag.calc_internal_data()
