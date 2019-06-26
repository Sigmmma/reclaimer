import os

from reclaimer.util.matrices import Matrix, matrix_to_quaternion
from reclaimer.model.jms import write_jms, JmsModel, JmsNode, JmsMarker,\
     generate_fake_nodes

__all__ = ("extract_physics", )


def extract_physics(tagdata, tag_path="", **kw):
    do_write_jms = kw.get('write_jms', True)
    filepath = ""
    if do_write_jms:
        filepath = os.path.join(
            kw['out_dir'], os.path.dirname(tag_path), "physics", "physics.jms")
        if not kw.get('overwrite', True) and os.path.isfile(filepath):
            return

    jms_model = JmsModel()
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

        jms_model.markers.append(
            JmsMarker(
                mp.name, "physics", -1, mp.model_node, i, j, k, w,
                mp.position.x * 100, mp.position.y * 100, mp.position.z * 100,
                mp.radius * 100,
                ))

    jms_model.nodes = generate_fake_nodes(child_node_ct)

    if do_write_jms:
        write_jms(filepath, jms_model)
    else:
        return jms_model
