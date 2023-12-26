#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.hek.defs.objs.mode import ModeTag

class Mod2Tag(ModeTag):

    def globalize_local_markers(self):
        tagdata = self.data.tagdata
        all_global_markers = tagdata.markers.STEPTREE
        all_global_markers_by_name = {b.name: b.marker_instances.STEPTREE
                                      for b in all_global_markers}

        for i in range(len(tagdata.regions.STEPTREE)):
            region = tagdata.regions.STEPTREE[i]
            for j in range(len(region.permutations.STEPTREE)):
                perm = region.permutations.STEPTREE[j]

                for k in range(len(perm.local_markers.STEPTREE)):
                    local_marker = perm.local_markers.STEPTREE[k]
                    global_markers = all_global_markers_by_name.get(
                        local_marker.name, None)

                    if global_markers is None or len(global_markers) >= 32:
                        all_global_markers.append()
                        all_global_markers[-1].name = local_marker.name
                        global_markers = all_global_markers[-1].marker_instances.STEPTREE
                        all_global_markers_by_name[local_marker.name] = global_markers

                    global_markers.append()
                    global_marker = global_markers[-1]

                    global_marker.region_index = i
                    global_marker.permutation_index = j
                    global_marker.node_index = local_marker.node_index
                    global_marker.rotation[:] = local_marker.rotation[:]
                    global_marker.translation[:] = local_marker.translation[:]

                del perm.local_markers.STEPTREE[:]

        # sort the markers how Halo's picky ass wants them
        name_map = {all_global_markers[i].name: i
                    for i in range(len(all_global_markers))}
        all_global_markers[:] = list(all_global_markers[name_map[name]]
                                     for name in sorted(name_map))

    def delocalize_part_nodes(self, geometry_index, part_index):
        part = self.data.tagdata.geometries.STEPTREE\
               [geometry_index].parts.STEPTREE[part_index]
        local_nodes = part.local_nodes[: part.local_node_count]

        delocalize_compressed_verts(part.compressed_vertices.STEPTREE,
                                    local_nodes)
        delocalize_uncompressed_verts(part.uncompressed_vertices.STEPTREE,
                                      local_nodes)

        part.flags.ZONER = False
        part.local_node_count = 0


def delocalize_compressed_verts(comp_verts, local_nodes):
    '''TODO: Update this function to also work on parsed vert data.'''
    local_node_ct = len(local_nodes) * 3
    # 28 is the offset to the first verts first node index
    for i in range(28, len(comp_verts), 32):
        if comp_verts[i] < local_node_ct:
            comp_verts[i] = local_nodes[comp_verts[i] // 3] * 3

        i += 1
        if comp_verts[i] < local_node_ct:
            comp_verts[i] = local_nodes[comp_verts[i] // 3] * 3


def delocalize_uncompressed_verts(uncomp_verts, local_nodes):
    '''TODO: Update this function to also work on parsed vert data.'''
    local_node_ct = len(local_nodes)
    # 57 is the offset to the least-significant half of
    # the first verts first node index(in big endian).
    for i in range(57, len(uncomp_verts), 68):
        # literally no reason to use 2 bytes for the node index since
        # a max of 63 nodes can be used, so we'll only edit the least
        # significant byte of the node indices and make it absolute.
        # if the value is 0xFF, the other byte should be 0xFF as well,
        # meaning the node is -1, which should stay as -1(no node).
        if uncomp_verts[i] < local_node_ct:
            uncomp_verts[i] = local_nodes[uncomp_verts[i]]

        i += 2
        if uncomp_verts[i] < local_node_ct:
            uncomp_verts[i] = local_nodes[uncomp_verts[i]]
