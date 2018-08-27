import os

from math import sqrt
from struct import Struct as PyStruct

from reclaimer.model.jms import GeometryMesh, JmsVertex
from reclaimer.model.stripify import Stripifier
from reclaimer.hek.defs.scex import scex_def
from reclaimer.hek.defs.schi import schi_def
from reclaimer.hek.defs.senv import senv_def
from reclaimer.hek.defs.sgla import sgla_def
from reclaimer.hek.defs.smet import smet_def
from reclaimer.hek.defs.soso import soso_def
from reclaimer.hek.defs.sotr import sotr_def
from reclaimer.hek.defs.spla import spla_def
from reclaimer.hek.defs.swat import swat_def
from reclaimer.hek.defs.mod2 import mod2_def,\
     triangle as mod2_tri_struct, fast_uncompressed_vertex as mod2_vert_struct
from reclaimer.common_descs import raw_reflexive, BlockDef

mod2_verts_def = BlockDef(
    raw_reflexive("vertices", mod2_vert_struct),
    endian='>'
    )

mod2_tri_strip_def = BlockDef(
    raw_reflexive("triangle", mod2_tri_struct),
    endian='>'
    )

LOD_NAMES = ("superhigh", "high", "medium", "low", "superlow")
MAX_STRIP_LEN = 32763 * 3

EMPTY_GEOM_VERTS = (
    JmsVertex(0, 0.000000001, 0.0, 0.0,
              0.0, 0.0, 1.0,
              -1, 0.0, 0.0, 0.0),
    JmsVertex(0, 0.0, 0.000000001, 0.0,
              0.0, 0.0, 1.0,
              -1, 0.0, 0.0, 1.0),
    JmsVertex(0, 0.0, 0.0, 0.000000001,
              0.0, 0.0, 1.0,
              -1, 0.0, 1.0, 0.0),
    )

def generate_shader(jms_material, tags_dir, data_dir=""):
    shdr_type = jms_material.shader_type
    shdr_path = jms_material.shader_path

    if not shdr_path:
        return

    tag_path = "%s.%s" % (os.path.join(tags_dir, shdr_path), shdr_type)
    if os.path.isfile(tag_path):
        # dont make shaders that already exist
        return

    shdr_blockdef = None
    if shdr_type == "shader_transparent_chicago_extended":
        shdr_blockdef = scex_def
    elif shdr_type == "shader_transparent_chicago":
        shdr_blockdef = schi_def
    elif shdr_type == "shader_environment":
        shdr_blockdef = senv_def
    elif shdr_type == "shader_glass":
        shdr_blockdef = sgla_def
    elif shdr_type == "shader_meter":
        shdr_blockdef = smet_def
    elif shdr_type == "shader_model":
        shdr_blockdef = soso_def
    elif shdr_type == "shader_transparent_generic":
        shdr_blockdef = sotr_def
    elif shdr_type == "shader_plasma":
        shdr_blockdef = spla_def
    elif shdr_type == "shader_water":
        shdr_blockdef = swat_def
    else:
        return

    bitmap_path = ""
    if jms_material.tiff_path not in ('', '<none>') and data_dir:
        try:
            bitmap_path = os.path.relpath(
                jms_material.tiff_path.replace("/", "\\"),
                data_dir.replace("/", "\\")).strip(" ")
        except Exception:
            pass

        if bitmap_path.startswith("."):
            bitmap_path = ""

    shdr_tag = shdr_blockdef.build()
    shdr_tag.filepath = tag_path
    tag_data = shdr_tag.data.tagdata

    if not bitmap_path or bitmap_path.lower() == "<none>":
        pass
    elif "chicago" in shdr_type:
        if shdr_type == "shader_transparent_chicago":
            maps = tag_data.schi_attrs.maps
        else:
            maps = tag_data.scex_attrs.four_stage_maps
        maps.STEPTREE.append()
        map = maps.STEPTREE[-1]
        map.bitmap.map_u_scale = map.bitmap.map_v_scale = 1.0
        map.bitmap.filepath = bitmap_path
    elif "environment" in shdr_type:
        tag_data.senv_attrs.diffuse.base_map.filepath = bitmap_path
    elif "glass" in shdr_type:
        tag_data.sgla_attrs.diffuse_properties.map.filepath = bitmap_path
    elif "meter" in shdr_type:
        tag_data.smet_attrs.meter_shader.map.filepath = bitmap_path
    elif "model" in shdr_type:
        tag_data.soso_attrs.maps.diffuse_map.filepath = bitmap_path
    elif "water" in shdr_type:
        tag_data.swat_attrs.water_shader.base_map.filepath = bitmap_path

    shdr_tag.serialize(temp=False, calc_pointers=False, int_test=False)

    return
        

def compile_gbxmodel(mod2_tag, merged_jms):
    tagdata = mod2_tag.data.tagdata

    tagdata.flags.parts_have_local_nodes = False

    u_scale, v_scale = merged_jms.calc_uv_scales()
    if u_scale < 1:
        u_scale = 1
    if v_scale < 1:
        v_scale = 1
    tagdata.base_map_u_scale = merged_jms.u_scale = u_scale
    tagdata.base_map_v_scale = merged_jms.v_scale = v_scale

    tagdata.node_list_checksum = merged_jms.node_list_checksum
    

    errors = []
    if len(merged_jms.materials) > 256:
        errors.append("Too many materials. Max count is 256.")

    if len(merged_jms.regions) > 32:
        errors.append("Too many regions. Max count is 32.")

    if errors:
        return errors

    # make nodes
    mod2_nodes = tagdata.nodes.STEPTREE
    del mod2_nodes[:]
    for node in merged_jms.nodes:
        mod2_nodes.append()
        mod2_node = mod2_nodes[-1]

        mod2_node.name = node.name[: 31]
        mod2_node.next_sibling_node = node.sibling_index
        mod2_node.first_child_node = node.first_child
        mod2_node.parent_node = node.parent_index
        mod2_node.translation[:] = node.pos_x / 100,\
                                   node.pos_y / 100,\
                                   node.pos_z / 100
        mod2_node.rotation[:] = node.rot_i, node.rot_j,\
                                node.rot_k, node.rot_w

        if node.parent_index >= 0:
            mod2_node.distance_from_parent = sqrt(
                node.pos_x**2 + node.pos_y**2 + node.pos_z**2) / 100


    # make shader references
    mod2_shaders = tagdata.shaders.STEPTREE
    shdr_perm_indices_by_name = {}
    for mod2_shader in mod2_shaders:
        shdr_name = mod2_shader.shader.filepath.split("\\")[-1]
        shdr_perm_indices = shdr_perm_indices_by_name.setdefault(shdr_name, [])
        shdr_perm_indices.append(mod2_shader.permutation_index)

    del mod2_shaders[:]
    for mat in merged_jms.materials:
        mod2_shaders.append()
        mod2_shader = mod2_shaders[-1]
        mod2_shader.shader.filepath = mat.shader_path
        if mat.shader_type:
            mod2_shader.shader.tag_class.set_to(mat.shader_type)
        else:
            mod2_shader.shader.tag_class.set_to("shader")

        shdr_name = mod2_shader.shader.filepath.split("\\")[-1].lower()
        shdr_perm_indices = shdr_perm_indices_by_name.get(shdr_name)
        if shdr_perm_indices:
            mod2_shader.permutation_index = shdr_perm_indices.pop(0)


    # make regions
    mod2_regions = tagdata.regions.STEPTREE
    del mod2_regions[:]

    global_markers = {}
    geom_meshes = []
    all_lod_nodes = {lod: set([0]) for lod in LOD_NAMES}
    for region_name in sorted(merged_jms.regions):
        region = merged_jms.regions[region_name]

        mod2_regions.append()
        mod2_region = mod2_regions[-1]
        mod2_region.name = region_name[: 31]

        mod2_perms = mod2_region.permutations.STEPTREE
        for perm_name in sorted(region.perm_meshes):
            perm = region.perm_meshes[perm_name]

            mod2_perms.append()
            mod2_perm = mod2_perms[-1]
            mod2_perm.name = perm_name[: 31]

            mod2_perm.flags.cannot_be_chosen_randomly = not perm.is_random_perm

            perm_added = False
            skipped_lods = []
            for i in range(len(LOD_NAMES)):
                lod_name = LOD_NAMES[i]
                if not perm.lod_meshes.get(lod_name):
                    if skipped_lods is not None:
                        skipped_lods.append(i)
                    continue

                geom_index = len(geom_meshes)
                lod_mesh = perm.lod_meshes[lod_name]
                geom_meshes.append(lod_mesh)

                # figure out which nodes this mesh utilizes
                this_meshes_nodes = set()
                for mesh in lod_mesh.values():
                    for vert in mesh.verts:
                        if vert.node_1_weight < 1:
                            this_meshes_nodes.add(vert.node_0)
                        if vert.node_1_weight > 0:
                            this_meshes_nodes.add(vert.node_1)

                all_lod_nodes[lod_name].update(this_meshes_nodes)

                lods_to_set = list(range(i, 5))
                if skipped_lods:
                    lods_to_set.extend(skipped_lods)
                    skipped_lods = None

                for i in lods_to_set:
                    setattr(mod2_perm,
                            "%s_geometry_block" % LOD_NAMES[i],
                            geom_index)

                perm_added = True

            if len(perm.markers) > 32:
                for marker in perm.markers:
                    global_markers.setdefault(
                        marker.name[: 31], []).append(marker)
            else:
                perm_added |= bool(perm.markers)
                mod2_markers = mod2_perm.local_markers.STEPTREE
                for marker in perm.markers:
                    mod2_markers.append()
                    mod2_marker = mod2_markers[-1]

                    mod2_marker.name = marker.name[: 31]
                    mod2_marker.node_index = marker.parent
                    mod2_marker.translation[:] = marker.pos_x / 100,\
                                                 marker.pos_y / 100,\
                                                 marker.pos_z / 100
                    mod2_marker.rotation[:] = marker.rot_i, marker.rot_j,\
                                              marker.rot_k, marker.rot_w


            if not perm_added:
                del mod2_perms[-1]
                continue

    if len(geom_meshes) > 256:
        return ("Cannot add more than 256 geometries to a model. "
                "Each material in each region in each permutation "
                "in each LOD is counted as a single geometry.\n"
                "This model would contain %s geometries." % len(geom_meshes), )

    # make the markers
    mod2_marker_headers = tagdata.markers.STEPTREE
    del mod2_marker_headers[:]
    for marker_name in sorted(global_markers):
        marker_list = global_markers[marker_name]
        mod2_marker_headers.append()
        mod2_marker_header = mod2_marker_headers[-1]

        mod2_marker_header.name = marker_name[: 31]
        mod2_marker_list = mod2_marker_header.marker_instances.STEPTREE

        for marker in marker_list:
            mod2_marker_list.append()
            mod2_marker = mod2_marker_list[-1]

            # figure out which permutation index this marker
            # matches for all the permutations in its region
            i = perm_index = 0
            for perm in mod2_regions[marker.region].permutations.STEPTREE:
                if perm.name == marker.permutation:
                    perm_index = i
                    break
                i += 1

            mod2_marker.region_index = marker.region
            mod2_marker.permutation_index = perm_index
            mod2_marker.node_index = marker.parent
            mod2_marker.translation[:] = marker.pos_x / 100,\
                                         marker.pos_y / 100,\
                                         marker.pos_z / 100
            mod2_marker.rotation[:] = marker.rot_i, marker.rot_j,\
                                      marker.rot_k, marker.rot_w

    # set the node counts per lod
    for lod in LOD_NAMES:
        lod_nodes = all_lod_nodes[lod]
        adding = True
        node_ct = len(mod2_nodes)
        
        for i in range(node_ct - 1, -1, -1):
            if i in lod_nodes:
                break
            node_ct -= 1

        setattr(tagdata, "%s_lod_nodes" % lod, max(0, node_ct - 1))


    # calculate triangle strips
    stripped_geom_meshes = []
    for geom_idx in range(len(geom_meshes)):
        material_meshes = {}
        stripped_geom_meshes.append(material_meshes)
        for mat_idx in sorted(geom_meshes[geom_idx]):
            material_meshes[mat_idx] = mesh_list = []
            geom_mesh = geom_meshes[geom_idx][mat_idx]
            all_verts = geom_mesh.verts

            stripifier = Stripifier()
            stripifier.load_mesh(geom_mesh.tris, True)
            stripifier.make_strips()
            stripifier.link_strips()

            strips = stripifier.all_strips.get(0)
            if not strips:
                all_verts = EMPTY_GEOM_VERTS
                tri_strip = (0, 1, 2)
            else:
                tri_strip = strips[0]

            if len(tri_strip) > MAX_STRIP_LEN:
                return (
                    ("Too many triangles ya fuck. Max triangles per "
                     "geometry is %s.\nThis geometry is %s after linking "
                     "all strips.") % (MAX_STRIP_LEN, len(tri_strip)), )

            mesh_list.append(GeometryMesh(all_verts, tri_strip))


    # make the geometries
    mod2_geoms = tagdata.geometries.STEPTREE
    del mod2_geoms[:]
    vert_packer = PyStruct(">14f2h2f").pack_into
    for geom_idx in range(len(stripped_geom_meshes)):
        mod2_geoms.append()
        mod2_parts = mod2_geoms[-1].parts.STEPTREE

        for mat_idx in sorted(stripped_geom_meshes[geom_idx]):
            geom_mesh_list = stripped_geom_meshes[geom_idx][mat_idx]
            for geom_mesh in geom_mesh_list:
                mod2_parts.append()
                mod2_part = mod2_parts[-1]
                mod2_verts = mod2_part.uncompressed_vertices.STEPTREE

                tris  = geom_mesh.tris
                verts = geom_mesh.verts
                vert_ct = len(verts)
                mod2_verts.extend(len(verts))
                mod2_part.shader_index = mat_idx

                cent_x = cent_y = cent_z = 0

                # TODO: Modify this to take into account local nodes
                # honestly though, who the fuck is going to care? fuck it.

                # make a raw vert reflexive and replace the one in the part
                mod2_part.uncompressed_vertices = mod2_verts_def.build()
                mod2_verts = mod2_part.uncompressed_vertices.STEPTREE = \
                             bytearray(68 * len(verts))
                i = 0
                for vert in verts:
                    vert_packer(
                        mod2_verts, i,
                        vert.pos_x / 100,  vert.pos_y / 100,  vert.pos_z / 100,
                        vert.norm_i, vert.norm_j, vert.norm_k,
                        vert.binorm_i, vert.binorm_j, vert.binorm_k,
                        vert.tangent_i, vert.tangent_j, vert.tangent_k,
                        vert.tex_u / u_scale, (1 - vert.tex_v) / v_scale,
                        vert.node_0, vert.node_1,
                        1 - vert.node_1_weight, vert.node_1_weight)
                    i += 68
                    cent_x += vert.pos_x / (vert_ct * 100)
                    cent_y += vert.pos_y / (vert_ct * 100)
                    cent_z += vert.pos_z / (vert_ct * 100)

                mod2_part.centroid_translation[:] = [cent_x, cent_y, cent_z]

                # make a raw tri reflexive and replace the one in the part
                mod2_part.triangles = mod2_tri_strip_def.build()
                mod2_tris = mod2_part.triangles.STEPTREE = bytearray(
                    [255, 255]) * (3 * ((len(tris) + 2) // 3))
                i = 0
                for tri in tris:
                    mod2_tris[i]     = tri >> 8
                    mod2_tris[i + 1] = tri & 0xFF
                    i += 2
