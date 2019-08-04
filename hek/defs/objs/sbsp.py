from reclaimer import util
from reclaimer.hek.defs.objs.tag import HekTag


class SbspTag(HekTag):

    def get_leaf_index_of_point(self, x, y, z):
        '''
        Returns the leaf node the point is in in the bsp.
        If point is not in the bsp, returns None.
        '''
        if len(self.data.tagdata.collision_bsp.STEPTREE) < 1:
            raise ValueError("No collision_bsp structure found in sbsp tag.")

        collision_bsp = self.data.tagdata.collision_bsp.STEPTREE[0]
        bsp3d_nodes = collision_bsp.bsp3d_nodes.STEPTREE
        bsp_planes  = collision_bsp.planes.STEPTREE
        if not bsp3d_nodes:
            return None

        node_index = 0
        # Go through the tree until we get a negative number (leaf or null)
        get_plane_side = util.geometry.is_point_on_front_side_of_plane
        while node_index >= 0:
            node = bsp3d_nodes[node_index]
            node_index = node.front_child if get_plane_side(
                (x, y, z), bsp_planes[node.plane], 1) else node.back_child

        # -1 = null (not found); otherwise it's a leaf (found)
        return None if node_index == -1 else node_index + 0x80000000

    def get_cluster_index_of_point(self, x, y, z):
        '''
        Returns the cluster the point is in in the bsp.
        If point is not in the bsp, returns None.
        '''
        leaf = self.get_leaf_index_of_point(x, y, z)
        leaves = self.data.tagdata.leaves.STEPTREE
        return None if leaf not in range(len(leaves)) else leaves[leaf].cluster

    def is_point_in_bsp(self, x, y, z):
        return self.get_leaf_index_of_point(x, y, z) is not None
