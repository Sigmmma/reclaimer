import os

from reclaimer.hek.defs.objs.matrices import Matrix, matrix_to_quaternion
from reclaimer.model.jms import write_jms, JmsModel, JmsNode, JmsMarker

__all__ = ("extract_physics", )


def extract_physics(tagdata, tag_path, **kw):
    filepath = os.path.join(
        kw['out_dir'], os.path.dirname(tag_path), "physics", "physics.jms")
    if not kw.get('overwrite', True) and os.path.isfile(filepath):
        return

    jms_data = JmsModel()
    nodes = jms_data.nodes = [JmsNode("root")]
    markers = jms_data.markers

    child_node_ct = 0
    for mp in tagdata.mass_points.STEPTREE:
        child_node_ct = max(child_node_ct, mp.model_node)
        fi, fj, fk = mp.forward
        ui, uj, uk = mp.up
        si, sj, sk = uj*fk - fj*uk, uk*fi - fk*ui, ui*fj - fi*uj

        matrix = Matrix(
            ((fi, fj, fk),
             (si, sj, sk),
             (ui, uj, uk)))
        i, j, k, w = matrix_to_quaternion(matrix)
        # no idea why I have to invert these
        w = -w
        if w < 0:
            i, j, k, w = -i, -j, -k, -w

        markers.append(
            JmsMarker(
                mp.name, "physics", -1, mp.model_node, i, j, k, w,
                mp.position.x * 100, mp.position.y * 100, mp.position.z * 100,
                mp.radius * 100,
                ))

    if child_node_ct > 0:
        # make some fake nodes
        nodes[0].first_child = 1
        for i in range(child_node_ct):
            nodes.append(JmsNode("node_%s" % (i + 1), -1, i + 2))
        nodes[-1].sibling_index = -1

    write_jms(filepath, jms_data)
