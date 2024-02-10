#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from math import sqrt
from struct import unpack, pack_into
from types import MethodType

from reclaimer.constants import LOD_NAMES
from reclaimer.hek.defs.objs.tag import HekTag
from reclaimer.util.compression import compress_normal32, decompress_normal32
from reclaimer.util.matrices import quaternion_to_matrix, Matrix


class ModeTag(HekTag):

    def calc_internal_data(self):
        '''
        For each node, this method recalculates the rotation matrix
        from the quaternion, the translation to the root bone, and
        the lod nodes.
        '''
        HekTag.calc_internal_data(self)

        nodes = self.data.tagdata.nodes.STEPTREE
        for node in nodes:
            rotation = quaternion_to_matrix(*node.rotation)
            trans = Matrix([node.translation])*-1
            parent = None

            # add the parents translation to this ones
            if node.parent_node > -1:
                trans += Matrix([nodes[node.parent_node].translation_to_root])

            # rotate the trans_to_root by this node's rotation
            trans *= rotation

            # combine this nodes rotation with its parents rotation
            if parent is not None:
                this_trans = node.translation
                node.distance_from_parent = sqrt(
                    this_trans.x**2 + this_trans.y**2 + this_trans.z**2)

                parent_rot = Matrix([parent.rot_jj_kk,
                                     parent.rot_kk_ii,
                                     parent.rot_ii_jj])
                rotation *= parent_rot

            # apply the changes to the node
            node.translation_to_root[:] = trans[0][:]
            node.rot_jj_kk[:] = rotation[0]
            node.rot_kk_ii[:] = rotation[1]
            node.rot_ii_jj[:] = rotation[2]

        # calculate the highest node used by each geometry
        geom_max_node_indices = []
        node_count = len(nodes)
        for geometry in self.data.tagdata.geometries.STEPTREE:
            geom_node_count = 0
            for part in geometry.parts.STEPTREE:
                if geom_node_count == node_count:
                    break
                elif getattr(part.flags, "ZONER", False):
                    # don't need to check every vert when they're all right here
                    geom_node_count = max((
                        geom_node_count,
                        *(v for v in part.local_nodes[:part.local_node_count])
                        ))
                    continue

                is_comp = not part.uncompressed_vertices.STEPTREE
                verts   = (
                    part.compressed_vertices.STEPTREE if is_comp else 
                    part.uncompressed_vertices.STEPTREE
                    )
                curr_highest = 0
                max_highest = (node_count - 1) * (3 if is_comp else 1)
                if isinstance(verts, (bytes, bytearray)):
                    # verts are packed, so unpack what we need from it
                    vert_size = 32 if is_comp else 68 # vert size in bytes
                    unpack_vert = (
                        MethodType(unpack, ">28x bbh") if is_comp else
                        MethodType(unpack, ">56x hhf 4x")
                        )
                    # lazy unpack JUST the indices and weight
                    verts = [
                        unpack_vert(verts[i: i+vert_size])
                        for i in range(0, len(verts), vert_size)
                        ]
                    node_0_key, node_1_key, weight_key = 0, 1, 2
                else:
                    # verts aren't packed, so use as-is
                    weight_key              = "node_0_weight" 
                    node_0_key, node_1_key  = "node_0_index", "node_1_index"

                for vert in verts:
                    node_0_weight  = vert[weight_key]
                    if node_0_weight > 0 and vert[node_0_key] > curr_highest: 
                        curr_highest = vert[node_0_key]
                        if curr_highest == max_highest: break

                    if node_0_weight < 1 and vert[node_1_key] > curr_highest:
                        curr_highest = vert[node_1_key]
                        if curr_highest == max_highest: break

                if is_comp:
                    # compressed nodes use indices multiplied by 3 for some reason
                    curr_highest //= 3

                geom_node_count = max(geom_node_count, curr_highest)

            geom_max_node_indices.append(max(0, geom_node_count))

        # calculate the highest node for each lod
        max_lod_nodes = {lod: 0 for lod in LOD_NAMES}
        for region in self.data.tagdata.regions.STEPTREE:
            for perm in region.permutations.STEPTREE:
                for lod_name in LOD_NAMES:
                    try:
                        highest_node_count = geom_max_node_indices[
                            perm["%s_geometry_block" % lod_name]
                            ]
                    except IndexError:
                        continue

                    max_lod_nodes[lod_name] = max(
                        max_lod_nodes[lod_name], 
                        highest_node_count
                        )

        # set the node counts per lod
        for lod, highest_node in max_lod_nodes.items():
            self.data.tagdata["%s_lod_nodes" % lod] = max(0, highest_node)

    def compress_part_verts(self, geometry_index, part_index):
        part = self.data.tagdata.geometries.STEPTREE\
               [geometry_index].parts.STEPTREE[part_index]
        uncomp_verts_reflexive = part.uncompressed_vertices
        comp_verts_reflexive = part.compressed_vertices

        comp_norm = compress_normal32
        unpack_vert = MethodType(unpack, ">11f2hf")
        pack_vert_into = MethodType(pack_into, ">12s3I2h2bh")

        comp_verts = bytearray(b'\x00' * 32 * uncomp_verts_reflexive.size)
        uncomp_verts = uncomp_verts_reflexive.STEPTREE
        if not isinstance(uncomp_verts, (bytes, bytearray)):
            raise ValueError("Error: Uncompressed vertices must be in raw, unpacked form.")

        in_off = out_off = 0
        # compress each of the verts and write them to the buffer
        for i in range(uncomp_verts_reflexive.size):
            ni, nj, nk, bi, bj, bk, ti, tj, tk,\
                u, v, ni_0, ni_1, nw = unpack_vert(
                    uncomp_verts[in_off + 12: in_off + 64])

            # write the compressed data
            pack_vert_into(
                comp_verts, out_off,
                uncomp_verts[in_off: in_off + 12],
                comp_norm(ni, nj, nk),
                comp_norm(bi, bj, bk),
                comp_norm(ti, tj, tk),
                int(max(0, min(1, u))*32767.5),
                int(max(0, min(1, v))*32767.5),
                ni_0*3, ni_1*3, int(max(0, min(1, nw))*32767.5))
            in_off  += 68
            out_off += 32

        comp_verts_reflexive.STEPTREE = comp_verts

    def decompress_part_verts(self, geometry_index, part_index):
        part = self.data.tagdata.geometries.STEPTREE\
               [geometry_index].parts.STEPTREE[part_index]
        uncomp_verts_reflexive = part.uncompressed_vertices
        comp_verts_reflexive = part.compressed_vertices

        decomp_norm = decompress_normal32
        unpack_vert = MethodType(unpack, ">3I2h2bh")
        pack_vert_into = MethodType(pack_into, ">12s11f2h2f")

        uncomp_verts = bytearray(b'\x00' * 68 * comp_verts_reflexive.size)
        comp_verts = comp_verts_reflexive.STEPTREE
        if not isinstance(comp_verts, (bytes, bytearray)):
            raise ValueError("Error: Compressed vertices must be in raw, unpacked form.")

        in_off = out_off = 0
        # uncompress each of the verts and write them to the buffer
        for i in range(comp_verts_reflexive.size):
            n, b, t, u, v, ni_0, ni_1, nw = unpack_vert(
                comp_verts[in_off + 12: in_off + 32])
            # write the uncompressed data
            pack_vert_into(
                uncomp_verts, out_off,
                comp_verts[in_off: in_off + 12],
                *decomp_norm(n), *decomp_norm(b), *decomp_norm(t),
                u/32767.5, v/32767.5, ni_0 // 3, ni_1 // 3,
                nw/32767.5, 1.0 - nw/32767.5)
            in_off  += 32
            out_off += 68

        uncomp_verts_reflexive.STEPTREE = uncomp_verts
