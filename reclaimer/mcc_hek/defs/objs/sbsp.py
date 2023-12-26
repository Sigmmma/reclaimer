#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.hek.defs.objs.tag import HekTag


class SbspTag(HekTag):
    @staticmethod
    def point_in_front_of_plane(plane, x, y, z):
        '''
        Takes a plane ex:
        ```py
        collision_bsp = self.data.tagdata.collision_bsp.STEPTREE[0]
        collision_bsp.planes.STEPTREE[i]
        ```
        And dots the plane and coordinates and compares against d to
        see if the xyz are in front of it.
        '''
        return (x*plane.i + y*plane.j + z*plane.k) >= plane.d

    def get_leaf_index_of_point(self, x, y, z):
        '''
        Returns the leaf node the point is in in the bsp.
        If point is not in the bsp, returns None.
        '''
        if len(self.data.tagdata.collision_bsp.STEPTREE) < 1:
            raise ValueError("No collision_bsp structure found in sbsp tag.")

        collision_bsp = self.data.tagdata.collision_bsp.STEPTREE[0]
        bsp3d_nodes   = collision_bsp.bsp3d_nodes.STEPTREE
        bsp_planes    = collision_bsp.planes.STEPTREE
        if not bsp3d_nodes:
            return None

        node_index = 0
        # Go through the tree until we get a negative number (leaf or null)
        while node_index >= 0:
            node = bsp3d_nodes[node_index]
            if self.point_in_front_of_plane(bsp_planes[node.plane], x, y, z):
                node_index = node.front_child
            else:
                node_index = node.back_child

        # -1 = null (not found); otherwise it's a leaf (found)
        return None if node_index == -1 else node_index + 0x80000000

    def get_cluster_index_of_point(self, x, y, z):
        '''
        Returns the cluster the point is in in the bsp.
        If point is not in the bsp, returns None.
        '''
        leaf = self.get_leaf_index_of_point(x, y, z)
        leaves = self.data.tagdata.leaves.STEPTREE
        return leaves[leaf].cluster if leaf in range(len(leaves)) else None

    def is_point_in_bsp(self, x, y, z):
        '''Returns if given point in 3d space is inside of this BSP'''
        return self.get_leaf_index_of_point(x, y, z) is not None
