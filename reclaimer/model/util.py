#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

import os

from reclaimer.model.jms import JmsVertex
from reclaimer.hek.defs.scex import scex_def
from reclaimer.hek.defs.schi import schi_def
from reclaimer.hek.defs.senv import senv_def
from reclaimer.hek.defs.sgla import sgla_def
from reclaimer.hek.defs.smet import smet_def
from reclaimer.hek.defs.soso import soso_def
from reclaimer.hek.defs.sotr import sotr_def
from reclaimer.hek.defs.spla import spla_def
from reclaimer.hek.defs.swat import swat_def
from reclaimer.hek.defs.mod2 import triangle as mod2_tri_struct, \
     fast_uncompressed_vertex as mod2_vert_struct
from reclaimer.common_descs import raw_reflexive, BlockDef

__all__ = (
    'mod2_verts_def', 'mod2_tri_strip_def',
    'LOD_NAMES', 'MAX_STRIP_LEN', 'EMPTY_GEOM_VERTS',
    'generate_shader',
    )


mod2_verts_def = BlockDef(
    raw_reflexive("vertices", mod2_vert_struct, 65535),
    endian='>'
    )

mod2_tri_strip_def = BlockDef(
    raw_reflexive("triangle", mod2_tri_struct, 65535),
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
            # TODO: Make this posix compat
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
