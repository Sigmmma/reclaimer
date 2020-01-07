#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

import math

from reclaimer.model.jms import JmsNode, JmsMaterial, JmsVertex,\
     JmsTriangle, JmsModel
from traceback import format_exc


def jms_model_from_obj(obj_string, model_name=None):
    if not isinstance(obj_string, str):
        raise TypeError(
            "Argument must be of type 'str', not '%s'." % type(obj_string))

    if model_name is None:
        model_name = "__unnamed"

    model = JmsModel(model_name)
    model.nodes = [JmsNode("frame")]
    model.regions = ["__unnamed"]

    mats = model.materials
    tris = model.tris

    f_num = 0
    mat_num = 0
    mat_names = {}
    v_locs = []
    v_uvs = []
    v_norms = []
    v_datas = {}
    v_data_by_idx = []
    norms_to_calc = {}
    sg_error = False
    ngon_error = False

    # Reminder that obj's use 1 based indexing
    i = 0
    for line in obj_string.split("\n"):
        i += 1
        line = line.lstrip(' ')
        if not line or line[0] == "#":
            continue

        line_parts = line.replace('\t', ' ').split(' ', 1)
        if len(line_parts) < 2:
            continue

        token, line = line_parts

        if token == "v":
            loc_data = [d for d in line.split(' ') if d]
            if len(loc_data) != 3:
                raise ValueError("Invalid vertex coord on line %s." % i)
            v_locs.append(loc_data)

        elif token == "vt":
            uv_data = [d for d in line.split(' ') if d]
            if len(uv_data) not in (2, 3):
                raise ValueError("Invalid vertex texture coord on line %s." % i)
            v_uvs.append(uv_data)

        elif token == "vn":
            norm_data = [d for d in line.split(' ') if d]
            if len(norm_data) != 3:
                raise ValueError("Invalid vertex normal on line %s." % i)
            v_norms.append(norm_data)

        elif token == "f":
            tri_data = [d for d in line.split(' ') if d]
            if len(tri_data) != 3:
                ngon_error = True
                continue

            v_indices = [0, 0, 0]
            for j in range(len(tri_data)):
                v_data = tuple(tri_data[j].replace(' ', '').split('/'))
                if not len(v_data[0]):
                    raise ValueError("Invalid triangle vert description.")

                if v_data not in v_datas:
                    v_data_by_idx.append(v_data)
                    v_datas[v_data] = len(v_data_by_idx)

                v_idx = v_datas[v_data] - 1
                v_indices[j] = v_idx
                if len(v_data) < 3 or not v_data[2]:
                    norms_to_calc.setdefault(v_idx, []).append(f_num)

            tris.append(JmsTriangle(0, mat_num, *v_indices))
            f_num += 1

        elif token == "usemtl":
            name = line
            if name in mat_names:
                mat_num = mat_names[name]
            else:
                mat_num = len(mat_names)
                mats.append(JmsMaterial(name))
                mat_names[name] = mat_num

        elif token == "s" and not sg_error:
            sg_error = True

        else:
            # dont care about anything else
            pass

    if sg_error or ngon_error:
        if ngon_error:
            print("Quads and n-gons are not supported.")

        if sg_error:
            print("Smoothing groups not supported! Export with vertex normals.")

        return

    model.verts = verts = [None] * len(v_data_by_idx)
    for i in range(len(v_data_by_idx)):
        v_data = v_data_by_idx[i]

        loc_idx = int(v_data[0]) - 1
        v_loc = v_locs[loc_idx]
        pos_x = float(v_loc[0])
        pos_y = float(v_loc[1])
        pos_z = float(v_loc[2])

        if len(v_data) > 1 and v_data[1]:
            v_uv = v_uvs[int(v_data[1]) - 1]
            tex_u = float(v_uv[0])
            tex_v = float(v_uv[1])
        else:
            tex_u = pos_x
            tex_v = pos_y

        if len(v_data) > 2 and v_data[2]:
            v_norm = v_norms[int(v_data[2]) - 1]
            norm_i = float(v_norm[0])
            norm_j = float(v_norm[1])
            norm_k = float(v_norm[2])
        else:
            norm_i = 1
            norm_j = norm_k = 0

        # We want to rotate the model, so we don't use the vertex coords
        # exactly as they are given(swap y and z and make z negative).
        verts[i] = JmsVertex(0, pos_x, -pos_z, pos_y,
                             norm_i, -norm_k, norm_j,
                             -1, 0.0, tex_u, tex_v)

    sqrt = math.sqrt
    for i in norms_to_calc:
        vert = verts[i]
        i = j = k = 0
        face_ct = 0

        for f_num in norms_to_calc[i]:
            face_ct += 1
            face = tris[f_num]
            v0 = verts[face.v0]
            v1 = verts[face.v1]
            v2 = verts[face.v2]
            vax = v1.pos_x - v0.pos_x
            vay = v1.pos_y - v0.pos_y
            vaz = v1.pos_z - v0.pos_z

            vbx = v2.pos_x - v0.pos_x
            vby = v2.pos_y - v0.pos_y
            vbz = v2.pos_z - v0.pos_z

            fi = vay * vbz - vaz * vby
            fj = vaz * vbx - vax * vbz
            fk = vax * vby - vay * vbx

            mag = fi**2 + fj**2 + fk**2
            if mag > 0:
                mag = sqrt(mag)
                i += fi / mag
                j += fj / mag
                k += fk / mag

        if face_ct:
            vert.norm_i = i / face_ct
            vert.norm_j = j / face_ct
            vert.norm_k = k / face_ct

    if not mats:
        mats.append(JmsMaterial("__unnamed"))

    return model
