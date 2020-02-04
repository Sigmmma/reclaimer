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

from reclaimer.hek.defs.objs.tag import HekTag
from reclaimer.util.compression import compress_normal32, decompress_normal32
from reclaimer.util.matrices import quaternion_to_matrix, Matrix

# TODO: Make calc_internal_data recalculate the lod nodes, and remove that
# same function from model.model_compilation.compile_gbxmodel and replace
# it with a call to calc_internal_data. lod nodes are recalculated when
# tags are compiled into maps, but the functionality should still be here.
class ModeTag(HekTag):

    def calc_internal_data(self):
        '''
        For each node, this method recalculates the rotation matrix
        from the quaternion, and the translation to the root bone.
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
