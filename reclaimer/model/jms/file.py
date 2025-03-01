#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

__all__ = ( 'read_jms', 'write_jms', )

import io
import itertools
import mmap
import re
import traceback

from copy import deepcopy
from pathlib import Path


from reclaimer.model.constants import (
    JMS_VER_HALO_1_OLDEST_KNOWN,
    JMS_VER_HALO_1_RETAIL,
    JMS_VER_HALO_2_RETAIL,
    JMS_PERM_CANNOT_BE_RANDOMLY_CHOSEN_TOKEN,
    )
from reclaimer.util import (
    float_to_str, float_to_str_truncate, parse_jm_float, parse_jm_int,
    )
from .model import JmsModel
from .node import JmsNode
from .material import JmsMaterial
from .marker import JmsMarker
from .vertex import JmsVertex
from .triangle import JmsTriangle

# Test showing off the regex can be seen here:
# https://regex101.com/r/7PKpWi/2
JMS_V1_REGEX = re.compile(br'([^\s][^\t\r\n]*)')
# https://regex101.com/r/ySgI1Z/2
JMS_V2_REGEX = re.compile(br'(?:\n+|\t+|^)([^;\t\r\n]+)')


def get_jms_data_iter(jms_stream_or_string, regex):
    # to unify everything, we'll work in bytes
    jms_stream = (
        jms_stream_or_string.encode("utf-8")
        if isinstance(jms_stream_or_string, str) else
        jms_stream_or_string
        )

    if isinstance(jms_stream, (bytes, bytearray)):
        jms_data = jms_stream.lstrip("\ufeff".encode())
    elif isinstance(jms_stream, io.IOBase):
        jms_data = mmap.mmap(jms_stream.fileno(), 0, access=mmap.ACCESS_READ)
    else:
        raise ValueError("Unsupported stream type %s" % type(jms_stream))

    jms_iter = (
        map(bytes.decode,
        map(re.Match.group, regex.finditer(jms_data), itertools.repeat(0)
        )))
    return jms_iter


def read_jms(jms_stream, stop_at="", perm_name=None):
    '''
    Converts a jms string into a JmsModel instance.
    '''
    jms_iter = get_jms_data_iter(jms_stream, JMS_V1_REGEX)
    try:
        version = int(next(jms_iter).strip())
    except ValueError:
        version = 0

    if (version < JMS_VER_HALO_1_OLDEST_KNOWN or 
        version > JMS_VER_HALO_2_RETAIL):
        print("Unknown JMS version '%s'" % version)
        return None

    if version <= JMS_VER_HALO_1_RETAIL:
        # Halo 1
        return _read_jms_8200(jms_iter, stop_at, perm_name, version)

    # after 8200, comments are allowed. the comment character
    # is a semicolon, and the line must start with it.
    # filter out any lines that start with a semicolon.

    jms_iter = get_jms_data_iter(jms_stream, JMS_V2_REGEX)

    version = int(next(jms_iter).strip())
    if version <= JMS_VER_HALO_2_RETAIL:
        # Halo 2
        return _read_jms_8210(jms_iter, stop_at, version)


def _read_jms_8200(jms_iter, stop_at="", perm_name=None, version=None):
    if perm_name is None:
        perm_name = "__unnamed"

    jms_model = JmsModel(perm_name, version=version)
    perm_name = jms_model.name

    # Halo 1
    try:
        jms_model.node_list_checksum = parse_jm_int(next(jms_iter))
    except Exception:
        print(traceback.format_exc())
        print("Could not read node list checksum.")
        return jms_model

    if jms_model.node_list_checksum >= 0x80000000:
        # jms gave us an unsigned checksum.... sign it
        jms_model.node_list_checksum -= 0x100000000

    stop = (stop_at == "nodes")
    if not stop:
        # read the nodes
        try:
            count = parse_jm_int(next(jms_iter))
            jms_model.nodes = []
            for i in range(count):
                name        = next(jms_iter)
                first_child = parse_jm_int(next(jms_iter))
                sibling     = parse_jm_int(next(jms_iter))
                quat_ijkw   = [parse_jm_float(next(jms_iter)) for _ in range(4)]
                pos_xyz     = [parse_jm_float(next(jms_iter)) for _ in range(3)]
                jms_model.nodes.append(JmsNode(
                    name, first_child, sibling, *quat_ijkw, *pos_xyz
                    ))

            JmsNode.setup_node_hierarchy(jms_model.nodes)
        except Exception:
            print(traceback.format_exc())
            print("Failed to read nodes.")
            stop = True

    stop |= (stop_at == "materials")
    if not stop:
        # read the materials
        try:
            count = parse_jm_int(next(jms_iter))
            jms_model.materials = []
            for i in range(count):
                jms_model.materials.append(
                    JmsMaterial(next(jms_iter), next(jms_iter))
                    )

        except Exception:
            print(traceback.format_exc())
            print("Failed to read materials.")
            stop = True

    stop |= (stop_at == "markers")
    if not stop:
        # read the markers
        try:
            count = parse_jm_int(next(jms_iter))
            jms_model.markers = []
            for i in range(count):
                name        = next(jms_iter)
                region      = (parse_jm_int(next(jms_iter))
                               if jms_model.has_marker_regions else 0)
                parent      = parse_jm_int(next(jms_iter))
                quat_ijkw   = [parse_jm_float(next(jms_iter)) for _ in range(4)]
                pos_xyz     = [parse_jm_float(next(jms_iter)) for _ in range(3)]
                radius      = (parse_jm_float(next(jms_iter))
                               if jms_model.has_marker_radius else 1)

                jms_model.markers.append(JmsMarker(
                    name, perm_name, region, parent,
                    *quat_ijkw, *pos_xyz, radius
                    ))
        except Exception:
            print(traceback.format_exc())
            print("Failed to read markers.")
            stop = True

    stop |= (stop_at == "regions")
    if not stop:
        # read the regions
        try:
            count = parse_jm_int(next(jms_iter))
            jms_model.regions = [next(jms_iter) for i in range(count)]
        except Exception:
            print(traceback.format_exc())
            print("Failed to read regions.")
            stop = True

    stop |= (stop_at == "vertices")
    if not stop:
        # read the vertices
        try:
            count = parse_jm_int(next(jms_iter))
            jms_model.verts = [None] * count
            i = 0 # make sure i is defined in case of exception
            for i in range(count):
                region      = (parse_jm_int(next(jms_iter))
                               if jms_model.has_vert_regions else 0)
                node_0      = parse_jm_int(next(jms_iter))
                px, py, pz  = [parse_jm_float(next(jms_iter)) for _ in range(3)]
                ni, nj, nk  = [parse_jm_float(next(jms_iter)) for _ in range(3)]
                node_1      = parse_jm_int(next(jms_iter))
                node_weight = parse_jm_float(next(jms_iter))
                tu, tv      = [parse_jm_float(next(jms_iter)) for _ in range(2)]
                tw          = parse_jm_float(next(jms_iter)) if jms_model.has_3d_uvws else 0

                jms_model.verts[i] = JmsVertex(
                    node_0, px, py, pz,
                    # tool normalizes imported jms normals by clamping, so we have to clamp as well
                    (1.0 if ni >= 1.0 else -1.0 if ni <= -1.0 else ni),
                    (1.0 if nj >= 1.0 else -1.0 if nj <= -1.0 else nj),
                    (1.0 if nk >= 1.0 else -1.0 if nk <= -1.0 else nk),
                    node_1, node_weight, tu, tv, tw, region=region
                    )
        except Exception:
            print(traceback.format_exc())
            print("Failed to read vertices.")
            del jms_model.verts[i: ]
            stop = True

    stop |= (stop_at == "triangles")
    if not stop:
        # read the triangles
        try:
            count = parse_jm_int(next(jms_iter))
            jms_model.tris = [None] * count
            i = 0 # make sure i is defined in case of exception
            for i in range(count):
                region = (parse_jm_int(next(jms_iter))
                          if jms_model.has_face_regions else 0)
                shader = parse_jm_int(next(jms_iter))
                v0, v1, v2 = [parse_jm_int(next(jms_iter)) for _ in range(3)]

                jms_model.tris[i] = JmsTriangle(region, shader, v0, v1, v2)

        except Exception:
            print(traceback.format_exc())
            print("Failed to read triangles.")
            del jms_model.tris[i: ]
            stop = True

    # copy the region from the verts into triangles, or
    # from the triangles into the verts
    try:
        verts = jms_model.verts
        if jms_model.has_vert_regions:
            for tri in jms_model.tris:
                tri.region = verts[tri.v0].region
        else:
            for tri in jms_model.tris:
                verts[tri.v0].region = tri.region
                verts[tri.v1].region = tri.region
                verts[tri.v2].region = tri.region
    except Exception:
        print(traceback.format_exc())
        print("Failed to copy regions between vertices and triangles.")

    # return (jms_models[name], )
    return jms_model


def _read_jms_8210(jms_iter, stop_at="", version=JMS_VER_HALO_2_RETAIL):
    # Halo 2
    # NOTE: This function is incomplete. It will not fully work
    jms_models = {}

    jms_data = list(jms_iter) # i'm not reworking this to allow streaming
    dat_i = 1

    nodes = []
    markers = []
    regions = []
    all_verts = []
    all_tris = {}

    material_perm_names = []

    perm_regions_and_shaders = {}
    cached_region_shader_indices = []

    stop = (stop_at == "nodes")
    if not stop:
        # read the nodes
        try:
            i = 0 # make sure i is defined in case of exception
            nodes[:] = (None, ) * parse_jm_int(jms_data[dat_i])
            dat_i += 1
            for i in range(len(nodes)):
                # TODO: make the marker positions relative. according to
                #       General_101, the h2 nodes use absolute transforms
                nodes[i] = JmsNode(
                    jms_data[dat_i], -1, -1,  # these will need to be calculated
                    parse_jm_float(jms_data[dat_i+1]), parse_jm_float(jms_data[dat_i+2]),
                    parse_jm_float(jms_data[dat_i+3]), parse_jm_float(jms_data[dat_i+4]),
                    parse_jm_float(jms_data[dat_i+5]), parse_jm_float(jms_data[dat_i+6]),
                    parse_jm_float(jms_data[dat_i+7]), parse_jm_int(jms_data[dat_i+8]),
                    )
                dat_i += 9
            JmsNode.setup_node_hierarchy(nodes, version)
        except Exception:
            print(traceback.format_exc())
            print("Failed to read nodes.")
            del nodes[i: ]
            stop = True

    stop |= (stop_at == "materials")
    if not stop:
        # read the materials
        try:
            i = 0 # make sure i is defined in case of exception
            material_perm_names[:] = (None, ) * parse_jm_int(jms_data[dat_i])
            cached_region_shader_indices[:] = (None, ) * len(material_perm_names)
            dat_i += 1
            for i in range(len(material_perm_names)):
                shader_name = jms_data[dat_i]
                mat_parts = jms_data[dat_i + 1].split()

                perm_name = mat_parts[-2]
                region_name = mat_parts[-1]

                material_perm_names[i] = perm_name

                perm_info = perm_regions_and_shaders.setdefault(perm_name, {})
                perm_regions = perm_info.setdefault("regions", [])
                perm_shaders = perm_info.setdefault("shaders", [])
                if region_name not in perm_regions:
                    perm_regions.append(region_name)

                if shader_name not in perm_shaders:
                    perm_shaders.append(shader_name)

                cached_region_shader_indices[i] = (
                    perm_regions.index(region_name),
                    perm_shaders.index(shader_name)
                    )
                dat_i += 2

        except Exception:
            print(traceback.format_exc())
            print("Failed to read materials.")
            del material_perm_names[i: ]
            del cached_region_shader_indices[i: ]
            stop = True

    stop |= (stop_at == "markers")
    if not stop:
        # read the markers
        try:
            i = 0 # make sure i is defined in case of exception
            markers[:] = (None, ) * parse_jm_int(jms_data[dat_i])
            dat_i += 1
            for i in range(len(markers)):
                markers[i] = JmsMarker(
                    jms_data[dat_i], "", -1, parse_jm_int(jms_data[dat_i+1]),
                    parse_jm_float(jms_data[dat_i+2]), parse_jm_float(jms_data[dat_i+3]),
                    parse_jm_float(jms_data[dat_i+4]), parse_jm_float(jms_data[dat_i+5]),
                    parse_jm_float(jms_data[dat_i+6]), parse_jm_float(jms_data[dat_i+7]), parse_jm_float(jms_data[dat_i+8]),
                    parse_jm_float(jms_data[dat_i+9])
                    )
                dat_i += 10
        except Exception:
            print(traceback.format_exc())
            print("Failed to read markers.")
            del markers[i: ]
            stop = True

    stop |= (stop_at == "instance_xrefs")
    if not stop:
        # read the instance xrefs
        try:
            i = 0 # make sure i is defined in case of exception
            instance_xrefs = (None, ) * parse_jm_int(jms_data[dat_i])
            dat_i += 1
            for i in range(len(instance_xrefs)):
                instance_xrefs[i] = (jms_data[dat_i], jms_data[dat_i+1])
                dat_i += 2
        except Exception:
            print(traceback.format_exc())
            print("Failed to read instance xrefs.")
            del instance_xrefs[i: ]
            stop = True

    stop |= (stop_at == "instance_markers")
    if not stop:
        # read the instance markers
        try:
            i = 0 # make sure i is defined in case of exception
            instance_markers = (None, ) * parse_jm_int(jms_data[dat_i])
            dat_i += 1
            for i in range(len(instance_markers)):
                # TODO: do something about the permutation name for each marker.
                # maybe make one copy of the markers for each permutation
                instance_markers[i] = JmsMarker(
                    jms_data[dat_i], "", -1,
                    parse_jm_float(jms_data[dat_i+3]), parse_jm_float(jms_data[dat_i+4]),
                    parse_jm_float(jms_data[dat_i+5]), parse_jm_float(jms_data[dat_i+6]),
                    parse_jm_float(jms_data[dat_i+7]), parse_jm_float(jms_data[dat_i+8]), parse_jm_float(jms_data[dat_i+9]),
                    )
                dat_i += 10
        except Exception:
            print(traceback.format_exc())
            print("Failed to read instance markers.")
            del instance_markers[i: ]
            stop = True

    stop |= (stop_at == "vertices")
    if not stop:
        # read the vertices
        try:
            i = 0 # make sure i is defined in case of exception
            all_verts[:] = (None, ) * parse_jm_int(jms_data[dat_i])
            dat_i += 1
            for i in range(len(all_verts)):
                x, y, z = parse_jm_float(jms_data[dat_i]),   parse_jm_float(jms_data[dat_i+1]), parse_jm_float(jms_data[dat_i+2])
                #a, b, c = parse_jm_float(jms_data[dat_i+3]), parse_jm_float(jms_data[dat_i+4]), parse_jm_float(jms_data[dat_i+5])

                # tool normalizes imported jms normals in halo 1 by clamping, so I'm going to assume halo 2 does as well
                a = min(1.0, max(-1.0, parse_jm_float(jms_data[dat_i+3])))
                b = min(1.0, max(-1.0, parse_jm_float(jms_data[dat_i+4])))
                c = min(1.0, max(-1.0, parse_jm_float(jms_data[dat_i+5])))
                dat_i += 6

                node_influences = [(-1, 0)] * parse_jm_int(jms_data[dat_i])
                dat_i += 1
                for j in range(len(node_influences)):
                    node_influences[j] = (parse_jm_int(jms_data[dat_i]),
                                          parse_jm_float(jms_data[dat_i+1]))
                    dat_i += 2

                tex_coords = [(0, 0)] * parse_jm_int(jms_data[dat_i])
                dat_i += 1
                for j in range(len(tex_coords)):
                    tex_coords[j] = (parse_jm_float(jms_data[dat_i]),
                                     parse_jm_float(jms_data[dat_i+1]))
                    dat_i += 2

                if len(node_influences) > 1:
                    node_1, node_1_weight = node_influences[1]
                else:
                    node_1, node_1_weight = -1, 0.0

                all_verts[i] = JmsVertex(
                    node_influences[0][0],
                    x, y, z,
                    a, b, c, 0, 1, 0, 1, 0, 0,
                    node_1, node_1_weight,
                    tex_coords[0][0], tex_coords[0][1], 0,
                    list(node[0] for node in node_influences[2: ]),
                    list(node[1] for node in node_influences[2: ]),
                    list(tex_coords[2: ])
                    )
        except Exception:
            print(traceback.format_exc())
            print("Failed to read vertices.")
            del all_verts[i: ]
            stop = True

    stop |= (stop_at == "triangles")
    if not stop:
        # read the triangles
        try:
            i = 0 # make sure i is defined in case of exception
            for perm_name in material_perm_names:
                all_tris[perm_name] = []

            all_tri_count = parse_jm_int(jms_data[dat_i])
            dat_i += 1
            for i in range(all_tri_count):
                mat_index = parse_jm_int(jms_data[dat_i])
                region, shader = cached_region_shader_indices[mat_index]

                all_tris[material_perm_names[mat_index]].append(JmsTriangle(
                    region, shader,
                    parse_jm_int(jms_data[dat_i+1]),
                    parse_jm_int(jms_data[dat_i+2]),
                    parse_jm_int(jms_data[dat_i+3]),
                    ))

                dat_i += 4
        except Exception:
            print(traceback.format_exc())
            print("Failed to read triangles.")
            stop = True

    for perm_name in material_perm_names:
        jms_model = JmsModel()

        jms_model.name = perm_name
        jms_model.perm_name = perm_name
        jms_model.version = version
        jms_model.is_random_perm = False

        jms_model.node_list_checksum = 0
        jms_model.nodes = deepcopy(nodes)
        jms_model.markers = deepcopy(markers)
        jms_model.tris    = all_tris[perm_name]
        jms_model.regions = perm_regions_and_shaders[perm_name]["regions"]
        jms_model.materials = list(
            JmsMaterial(name) for name in
            perm_regions_and_shaders[perm_name]["shaders"]
            )

        for marker in jms_model.markers:
            # set the permutation name for each marker
            marker.permutation = perm_name

        # TODO: address this
        if True or len(material_perm_names) > 1:
            # more than one perm. need to split into multiple and rebase
            vert_rebase_map = {}
            for tri in all_tris[perm_name]:
                tri.v0 = vert_rebase_map.setdefault(tri.v0, len(vert_rebase_map))
                tri.v1 = vert_rebase_map.setdefault(tri.v1, len(vert_rebase_map))
                tri.v2 = vert_rebase_map.setdefault(tri.v2, len(vert_rebase_map))

            jms_model.verts = list(
                all_verts[vert_rebase_map[i]] for i in range(len(vert_rebase_map))
                )
        else:
            # only one perm. no need to split and rebase
            jms_model.verts = all_verts

        jms_models[perm_name] = jms_model


    # TODO: Make this able to read spheres, boxes, capsules,
    #       convex shapes, ragdolls, hinges, car wheels,
    #       point-to-points, prismatics, and bounding spheres

    # TODO: make several jms_models from the parsed data

    jms_models = tuple(jms_models[name] for name in sorted(jms_models))
    # uncomment when pipeline is changed to handle read_jms returning a tuple of JmsModels
    # return jms_models
    return jms_models[0] if jms_models else None


def write_jms(filepath, jms_model, use_blitzkrieg_rounding=False):
    '''
    Writes a JmsModel to filepath.
    '''
    to_str = (
        float_to_str if not use_blitzkrieg_rounding else
        (lambda f: float_to_str_truncate(f, 6))
        )

    materials = jms_model.materials
    regions = jms_model.regions

    # If the path doesnt exist, create it
    filepath = Path(filepath)
    filepath.parent.mkdir(exist_ok=True, parents=True)

    if not regions:
        regions = ("__unnamed", )

    if not materials:
        materials = (JmsMaterial("__unnamed", "<none>"), )

    with filepath.open("w", encoding='latin1', newline="\r\n") as f:
        f.write("%s\n" % jms_model.version)
        f.write("%s\n" % int(jms_model.node_list_checksum))

        f.write("%s\n" % len(jms_model.nodes))
        for node in jms_model.nodes:
            f.write("%s\n%s\n%s\n%s\t%s\t%s\t%s\n%s\t%s\t%s\n" % (
                node.name[: 31], node.first_child, node.sibling_index,
                to_str(node.rot_i), to_str(node.rot_j),
                to_str(node.rot_k), to_str(node.rot_w),
                to_str(node.pos_x), to_str(node.pos_y), to_str(node.pos_z),
                )
            )

        f.write("%s\n" % len(materials))
        for mat in materials:
            f.write("%s%s%d\n%s\n" % (
                mat.name, mat.properties, mat.permutation_index,
                mat.tiff_path
                ))

        f.write("%s\n" % len(jms_model.markers))
        for marker in jms_model.markers:
            f.write("%s\n" % marker.name[: 31])
            if jms_model.has_marker_regions:
                f.write("%s\n" % marker.region)

            f.write("%s\n%s\t%s\t%s\t%s\n%s\t%s\t%s\n" % (
                marker.parent,
                to_str(marker.rot_i), to_str(marker.rot_j),
                to_str(marker.rot_k), to_str(marker.rot_w),
                to_str(marker.pos_x), to_str(marker.pos_y), to_str(marker.pos_z)
                ))

            if jms_model.has_marker_radius:
                f.write("%s\n" % to_str(marker.radius))

        f.write("%s\n" % len(regions))
        for region in regions:
            f.write("%s\n" % region[: 31])

        f.write("%s\n" % len(jms_model.verts))
        for vert in jms_model.verts:
            if jms_model.has_vert_regions:
                f.write("%s\n" % vert.region)

            f.write("%s\n%s\t%s\t%s\n%s\t%s\t%s\n%s\n%s\n%s\n%s\n%s\n" % (
                vert.node_0,
                to_str(vert.pos_x),  to_str(vert.pos_y),  to_str(vert.pos_z),
                to_str(vert.norm_i), to_str(vert.norm_j), to_str(vert.norm_k),
                vert.node_1,
                to_str(vert.node_1_weight),
                to_str(vert.tex_u), to_str(vert.tex_v), to_str(vert.tex_w),
                )
            )

        f.write("%s\n" % len(jms_model.tris))
        for tri in jms_model.tris:
            if jms_model.has_marker_regions:
                f.write("%s\n" % tri.region)
                
            f.write("%s\n%s\t%s\t%s\n" % (
                tri.shader, tri.v0, tri.v1, tri.v2
                )
            )
