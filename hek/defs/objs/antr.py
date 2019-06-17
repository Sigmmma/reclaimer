from struct import pack_into, pack, unpack
from .tag import *
from reclaimer.animation import animation_compression,\
     animation_compilation, jma
from reclaimer.model import jms
from supyr_struct.field_type_methods import byteorder_char


class AntrTag(HekTag):
    jma_nodes = ()

    def decompress_all_anims(self, jma_nodes=None):
        decompressed_indices = []

        for i in range(self.data.tagdata.animations.size):
            if self.decompress_anim(i, jma_nodes):
                decompressed_indices.append(i)

        return decompressed_indices

    def decompress_anim(self, anim_index, jma_nodes=None):
        anim = self.data.tagdata.animations.STEPTREE[anim_index]
        if not anim.flags.compressed_data:
            return False
        elif anim.anim.frame_count == 0:
            # no animation to decompress
            return False

        # if the provided nodes aren't valid, use any that were precomputed
        if not jma_nodes and self.jma_nodes:
            jma_nodes = self.jma_nodes
        else:
            jma_nodes = animation_compilation.animation_nodes_to_jms_nodes(
                self.data.tagdata.nodes.STEPTREE)

            if len(jma_nodes) < anim.node_count:
                jma_nodes = jms.generate_fake_nodes(anim.node_count)

            self.jma_nodes = jma_nodes

        animation_compression.decompress_animation(anim, jma_nodes[: anim.node_count])
        animation_compilation.compile_animation(anim, jma_animation)

        return True
