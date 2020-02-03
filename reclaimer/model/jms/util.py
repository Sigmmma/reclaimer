#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

__all__ = (
    'generate_fake_nodes',
    'edge_loop_to_strippable_tris',
    'edge_loop_to_fannable_tris',
    'edge_loop_to_tris',
    )

from .node import JmsNode
from .triangle import JmsTriangle


def generate_fake_nodes(node_count):
    nodes = []
    if node_count <= 0:
        return nodes

    nodes.append(JmsNode("fake_node0", 1, -1))
    for i in range(1, node_count):
        nodes.append(JmsNode("fake_node%s" % i, -1, i + 1))

    nodes[-1].first_child = -1
    nodes[-1].sibling_index = -1
    JmsNode.setup_node_hierarchy(nodes)
    return nodes


def edge_loop_to_strippable_tris(edge_loop, region=0, mat_id=0):
    tris = [None] * (len(edge_loop) - 2)
    vert_ct = len(edge_loop)

    even_face_ct = (vert_ct - 1) // 2
    odd_face_ct = (vert_ct - 2) // 2

    # make the even faces
    v0 = edge_loop[0]
    for i in range(even_face_ct):
        v1 = edge_loop[i + 1]
        v2 = edge_loop[vert_ct - 1 - i]
        tris[i << 1] = JmsTriangle(region, mat_id, v0, v1, v2)

        v0 = v2

    # make the odd faces
    v0 = edge_loop[1]
    for i in range(odd_face_ct):
        v1 = edge_loop[i + 2]
        v2 = edge_loop[vert_ct - 1 - i]
        tris[(i << 1) + 1] = JmsTriangle(region, mat_id, v0, v1, v2)

        v0 = v1

    return tris


def edge_loop_to_fannable_tris(edge_loop, region=0, mat_id=0):
    vert_index_count = len(edge_loop)
    v0 = edge_loop[0]
    return [JmsTriangle(region, mat_id, v0,
                        edge_loop[((i + 1) % vert_index_count)],
                        edge_loop[((i + 2) % vert_index_count)])
            for i in range(len(edge_loop) - 2)]


def edge_loop_to_tris(edge_loop_or_vert_index_count, region=0, mat_id=0,
                      base=0, make_fan=False):
    if isinstance(edge_loop_or_vert_index_count, int):
        edge_loop = list(range(base, base + edge_loop_or_vert_index_count))
    else:
        edge_loop = edge_loop_or_vert_index_count

    if make_fan:
        return edge_loop_to_fannable_tris(edge_loop, region, mat_id)

    return edge_loop_to_strippable_tris(edge_loop, region, mat_id)
