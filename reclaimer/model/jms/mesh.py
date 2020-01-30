#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

__all__ = ( 'GeometryMesh', 'PermutationMesh', )


class GeometryMesh:
    verts = ()
    tris  = ()
    local_nodes = []
    def __init__(self, verts=(), tris=()):
        self.verts = verts if verts else []
        self.tris  = tris  if tris  else []


class PermutationMesh:
    markers = ()
    lod_meshes = ()
    is_random_perm = True

    def __init__(self):
        self.markers = []
        self.lod_meshes = {}
