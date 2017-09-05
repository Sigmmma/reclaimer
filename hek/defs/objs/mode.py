from math import sqrt

from .tag import *
from .matrices import quaternion_to_matrix, Matrix

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
