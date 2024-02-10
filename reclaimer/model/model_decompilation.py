#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from pathlib import Path
from struct import Struct as PyStruct
from traceback import format_exc

from reclaimer.model.constants import (
    JMS_PERM_CANNOT_BE_RANDOMLY_CHOSEN_TOKEN, SCALE_INTERNAL_TO_JMS )
from reclaimer.model.jms import write_jms, JmsModel, JmsNode,\
     JmsMaterial, JmsMarker, JmsVertex, JmsTriangle
from reclaimer.util.compression import decompress_normal32


__all__ = ("extract_model", )


def extract_model(tagdata, tag_path="", **kw):
    do_write_jms = kw.get('write_jms', True)
    if do_write_jms:
        jms_models = None
        filepath_base = Path(kw.get("out_dir", "")).joinpath(
            Path(tag_path).parent, "models")
    else:
        jms_models = []
        filepath_base = Path("")

    global_markers = {}
    materials = []
    regions = []
    nodes = []

    for b in tagdata.markers.STEPTREE:
        marker_name = b.name

        for inst in b.marker_instances.STEPTREE:
            try:
                region = tagdata.regions.STEPTREE[inst.region_index]
            except Exception:
                print("Invalid region index in marker '%s'" % marker_name)
                continue

            try:
                perm = region.permutations.STEPTREE[inst.permutation_index]
                perm_name = perm.name
                if (perm.flags.cannot_be_chosen_randomly and
                    not perm_name.startswith(JMS_PERM_CANNOT_BE_RANDOMLY_CHOSEN_TOKEN)):
                    perm_name = JMS_PERM_CANNOT_BE_RANDOMLY_CHOSEN_TOKEN + perm_name
            except Exception:
                print("Invalid permutation index in marker '%s'" % marker_name)
                continue

            perm_markers = global_markers.setdefault(perm_name, [])

            trans = inst.translation
            rot = inst.rotation
            perm_markers.append(JmsMarker(
                marker_name, perm_name, inst.region_index, inst.node_index,
                rot.i, rot.j, rot.k, rot.w,
                trans.x * SCALE_INTERNAL_TO_JMS,
                trans.y * SCALE_INTERNAL_TO_JMS,
                trans.z * SCALE_INTERNAL_TO_JMS,
                1.0
                ))

    for b in tagdata.nodes.STEPTREE:
        trans = b.translation
        rot = b.rotation
        nodes.append(JmsNode(
            b.name, b.first_child_node, b.next_sibling_node,
            rot.i, rot.j, rot.k, rot.w,
            trans.x * SCALE_INTERNAL_TO_JMS,
            trans.y * SCALE_INTERNAL_TO_JMS,
            trans.z * SCALE_INTERNAL_TO_JMS,
            b.parent_node
            ))

    for b in tagdata.shaders.STEPTREE:
        shader_name = b.shader.filepath.replace("/", "\\").split("\\")[-1]
        if b.permutation_index != 0:
            shader_name += str(b.permutation_index)

        materials.append(JmsMaterial(shader_name))

    markers_by_perm = {}
    geoms_by_perm_lod_region = {}

    # When scale is 0 it really should be 1.

    u_scale = 1 if tagdata.base_map_u_scale == 0 else tagdata.base_map_u_scale 
    v_scale = 1 if tagdata.base_map_v_scale == 0 else tagdata.base_map_v_scale 

    for region in tagdata.regions.STEPTREE:
        region_index = len(regions)
        regions.append(region.name)
        for perm in region.permutations.STEPTREE:
            perm_name = perm.name
            if (perm.flags.cannot_be_chosen_randomly and
                not perm_name.startswith(JMS_PERM_CANNOT_BE_RANDOMLY_CHOSEN_TOKEN)):
                perm_name = JMS_PERM_CANNOT_BE_RANDOMLY_CHOSEN_TOKEN + perm_name

            geoms_by_lod_region = geoms_by_perm_lod_region.setdefault(perm_name, {})

            perm_markers = markers_by_perm.setdefault(perm_name, [])
            if hasattr(perm, "local_markers"):
                for m in perm.local_markers.STEPTREE:
                    trans = m.translation
                    rot = m.rotation
                    perm_markers.append(JmsMarker(
                        m.name, perm_name, region_index, m.node_index,
                        rot.i, rot.j, rot.k, rot.w,
                        trans.x * SCALE_INTERNAL_TO_JMS,
                        trans.y * SCALE_INTERNAL_TO_JMS,
                        trans.z * SCALE_INTERNAL_TO_JMS,
                        1.0
                        ))

            last_geom_index = -1
            for lod in range(5):
                geoms_by_region = geoms_by_lod_region.get(lod, {})
                region_geoms = geoms_by_region.get(region.name, [])

                geom_index = perm[
                    perm.NAME_MAP["superlow_geometry_block"] + (4 - lod)]

                if (geom_index in region_geoms or
                    geom_index == last_geom_index):
                    continue

                geoms_by_lod_region[lod] = geoms_by_region
                geoms_by_region[region.name] = region_geoms
                region_geoms.append(geom_index)
                last_geom_index = geom_index

    can_have_local_nodes = hasattr(tagdata.flags, "parts_have_local_nodes")
    def_node_map = [*range(128), -1]

    # use big endian since it will have been byteswapped
    comp_vert_unpacker = PyStruct(">3f3I2h2bh").unpack_from
    uncomp_vert_unpacker = PyStruct(">14f2h2f").unpack_from

    for perm_name in sorted(geoms_by_perm_lod_region):
        geoms_by_lod_region = geoms_by_perm_lod_region[perm_name]
        perm_markers = markers_by_perm.get(perm_name)

        for lod in sorted(geoms_by_lod_region):
            if lod == -1:
                continue

            jms_name = perm_name + {4: " superlow", 3: " low", 2: " medium",
                                    1: " high", 0: " superhigh"}.get(lod, "")

            filepath = filepath_base.joinpath(jms_name + ".jms")

            markers = list(perm_markers)
            markers.extend(global_markers.get(perm_name, ()))
            verts = []
            tris = []

            geoms_by_region = geoms_by_lod_region[lod]
            for region_name in sorted(geoms_by_region):
                region_index = regions.index(region_name)
                geoms = geoms_by_region[region_name]

                for geom_index in geoms:
                    try:
                        geom_block = tagdata.geometries.STEPTREE[geom_index]
                    except Exception:
                        print("Invalid geometry index '%s'" % geom_index)
                        continue

                    for part in geom_block.parts.STEPTREE:
                        v_origin = len(verts)
                        shader_index = part.shader_index

                        node_map = (
                            [*part.local_nodes, -1]
                            if can_have_local_nodes and part.flags.ZONER else
                            def_node_map
                            )

                        tris_steptree    = part.triangles.STEPTREE
                        cverts_steptree  = part.compressed_vertices.STEPTREE
                        ucverts_steptree = part.uncompressed_vertices.STEPTREE
                        unparsed = isinstance(
                            getattr(tris_steptree, "data", None), 
                            (bytearray, bytes)
                            )
                        compressed = (
                            bool(unparsed and getattr(cverts_steptree, "data", None)) or 
                            bool(not unparsed and cverts_steptree)
                            )
                        uncompressed = (
                            bool(unparsed and getattr(ucverts_steptree, "data", None)) or 
                            bool(not unparsed and ucverts_steptree)
                            )
                        # prefer uncompressed vertices if both exist
                        compressed = compressed and not uncompressed

                        try:
                            vert_data = cverts_steptree if compressed else ucverts_steptree
                            if unparsed:
                                # if verts are unparsed, parse them
                                unpack, v_size = (
                                    (comp_vert_unpacker,   32) if compressed else 
                                    (uncomp_vert_unpacker, 68)
                                    )
                                data = vert_data.data
                                vert_data = [
                                    unpack(data, i) for i in range(0, len(data), v_size)
                                    ]

                            if compressed:
                                verts.extend(
                                    JmsVertex(
                                        v[8]//3,
                                        v[0] * 100, v[1] * 100, v[2] * 100,
                                        *decompress_normal32(v[3]),
                                        v[9]//3, 1.0 - (v[10]/32767),
                                        u_scale * v[6]/32767, 1.0 - v_scale * v[7]/32767
                                        )
                                    for v in vert_data
                                    )
                            else:
                                verts.extend(
                                    JmsVertex(
                                        node_map[v[14]],
                                        v[0] * 100, v[1] * 100, v[2] * 100,
                                        v[3], v[4], v[5],
                                        node_map[v[15]], max(0, min(1, v[17])),
                                        u_scale * v[12], 1.0 - v_scale * v[13]
                                        )
                                    for v in vert_data
                                    )
                        except Exception:
                            print(format_exc())
                            print("If you see this, tell Moses to stop "
                                  "fucking with the vertex definition.")

                        try:
                            if unparsed:
                                tri_block = tris_steptree.data
                                tri_list = [-1] * (len(tri_block) // 2)
                                for i in range(len(tri_list)):
                                    # assuming big endian
                                    tri_list[i] = (
                                        tri_block[i * 2 + 1] +
                                        (tri_block[i * 2] << 8))
                                    if tri_list[i] > 32767:
                                        tri_list[i] = -1
                            else:
                                tri_list = []
                                for triangle in tris_steptree:
                                    tri_list.extend(triangle)

                            swap = True
                            for i in range(len(tri_list) - 2):
                                v0 = tri_list[i]
                                v1 = tri_list[i + 1 + swap]
                                v2 = tri_list[i + 2 - swap]
                                if v0 != -1 and v1 != -1 and v2 != -1:
                                    # remove degens
                                    if v0 != v1 and v0 != v2 and v1 != v2:
                                        tris.append(JmsTriangle(
                                            region_index, shader_index,
                                            v0 + v_origin,
                                            v1 + v_origin,
                                            v2 + v_origin))
                                swap = not swap
                        except Exception:
                            print(format_exc())
                            print("Could not parse triangle blocks.")

            jms_model = JmsModel(
                jms_name, tagdata.node_list_checksum, nodes,
                materials, markers, regions, verts, tris)
            if do_write_jms:
                write_jms(filepath, jms_model)
            else:
                jms_models.append(jms_model)

    return jms_models
