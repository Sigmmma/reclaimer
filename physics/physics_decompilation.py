import os

from reclaimer.hek.defs.objs.matrices import Matrix, matrix_to_quaternion
from reclaimer.model.jms import write_jms, JmsModel, JmsNode, JmsMarker,\
     generate_fake_nodes

__all__ = ("extract_physics", )


def extract_physics(tagdata, tag_path, **kw):
    filepath = os.path.join(
        kw['out_dir'], os.path.dirname(tag_path), "physics", "physics.jms")
    if not kw.get('overwrite', True) and os.path.isfile(filepath):
        return

    jms_data = JmsModel()

    child_node_ct = 1
    for mp in tagdata.mass_points.STEPTREE:
        child_node_ct = max(child_node_ct, mp.model_node + 1)
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

        jms_data.markers.append(
            JmsMarker(
                mp.name, "physics", -1, mp.model_node, i, j, k, w,
                mp.position.x * 100, mp.position.y * 100, mp.position.z * 100,
                mp.radius * 100,
                ))

    jms_data.nodes = generate_fake_nodes(child_node_ct)

    write_jms(filepath, jms_data)
