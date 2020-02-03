#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from pathlib import Path
from reclaimer.util.matrices import Matrix, matrix_to_quaternion
from reclaimer.model.jms import write_jms, JmsModel, JmsNode, JmsMarker, util

__all__ = ("extract_physics", )


def extract_physics(tagdata, tag_path="", **kw):
    do_write_jms = kw.get('write_jms', True)
    filepath = Path("")
    if do_write_jms:
        filepath = Path(kw.get("out_dir", "")).joinpath(
            Path(tag_path).parent, "physics", "physics.jms")
        if not kw.get('overwrite', True) and filepath.is_file():
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

    jms_model.nodes = util.generate_fake_nodes(child_node_ct)

    if do_write_jms:
        write_jms(filepath, jms_model)
    else:
        return jms_model
