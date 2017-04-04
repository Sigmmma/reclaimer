from math import sqrt

from .tag import *
from .matrices import quaternion_to_matrix, Matrix

class ModeTag(HekTag):

    def calc_internal_data(self):
        HekTag.calc_internal_data()

        # THIS SHIT DONT WORK YET
        return
        nodes = self.data.tagdata.nodes.STEPTREE
        for node in nodes:
            '''
            For each node, this method rcalculates the rotation matrix
            from the quaternion, and the translation to the root bone.
            '''
            qr = node.rotation
            rotation = quaternion_to_matrix(qr.i, qr.j, qr.k, qr.w)

            # recalculate the translation to root
            seen = set()  # make sure we dont infinitely recurse
            curr_node = node

            trans_to_root = Matrix([(0,0,0)])

            # add up all the translations from this node to the root
            while curr_node:
                if id(curr_node) in seen:
                    # infinitely recursing...... something is wrong with that
                    break
                seen.add(id(curr_node))
                trans = curr_node.translation

                trans_to_root[0][0] -= trans[0]
                trans_to_root[0][1] -= trans[1]
                trans_to_root[0][2] -= trans[2]

                if curr_node.parent_node < 0:
                    # reached the root
                    break
                curr_node = nodes[curr_node.parent_node]

            # combine this nodes rotation with its parents rotation
            if curr_node is not node:
                parent = nodes[node.parent_node]
                trans = node.translation
                p_trans = parent.translation
                node.distance_from_parent = sqrt((trans.x - p_trans.x)**2 +
                                                 (trans.y - p_trans.y)**2 +
                                                 (trans.z - p_trans.z)**2)

                parent_rot = Matrix([parent.rot_jj_kk,
                                     parent.rot_kk_ii,
                                     parent.rot_ii_jj])
                rotation *= parent_rot

            # rotate the trans_to_root by this node's rotation
            trans_to_root *= rotation

            # apply the changes to the node
            node.translation_to_root[:] = trans_to_root[0][:]
            node.rot_jj_kk[:] = rotation[0]
            node.rot_kk_ii[:] = rotation[1]
            node.rot_ii_jj[:] = rotation[2]
