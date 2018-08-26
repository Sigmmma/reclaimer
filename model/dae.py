import math
try:
    #import collada
    # Null the import to collada since we're not using it
    collada = None
except ImportError:
    collada = None

from .jms import JmsNode, JmsMaterial, JmsMarker, JmsVertex, JmsTriangle,\
     JmsModel
from traceback import format_exc


special_mat_names = (
    "sky", "seamsealer", "portal", "exactportal",
    "weatherpoly", "sound", "unused")

def jms_model_from_dae(filepath, model_name=None):
    if collada is None:
        return

    if model_name is None:
        model_name = "__unnamed"

    collada_model = collada.Collada(filepath)
    print(collada_model.geometries)

    model = JmsModel(model_name)

    regions = model.regions
    mats = model.materials
    nodes = model.nodes
    tris = model.tris
    verts = model.verts

    for collada_mat in collada_model.materials:
        mat_name = collada_mat.name

        # correct DAE not being able to use + in material names
        if mat_name.startswith('_'):
            mat_name = mat_name.lstrip("_")
            if mat_name in special_mat_names:
                mat_name = "+" + mat_name

        mats.append(JmsMaterial(mat_name))

    if not mats:
        mats.append(JmsMaterial("__unnamed"))

    return
    # idk if i'll ever implement this. collada is just too complex

    return model
