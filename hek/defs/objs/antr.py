from struct import pack_into, pack, unpack
from .tag import *
from reclaimer.animation import animation_compression,\
     animation_compilation, jma
from supyr_struct.field_type_methods import byteorder_char


class AntrTag(HekTag):
    model_nodes = ()

    def decompress_all_anims(self):
        decompressed_indices = []

        for i in range(self.data.tagdata.animations.size):
            if self.decompress_anim(i):
                decompressed_indices.append(i)

        return decompressed_indices

    def decompress_anim(self, anim_index):
        anim = self.data.tagdata.animations.STEPTREE[anim_index]

        if not anim.flags.compressed_data:
            return False
        elif anim.anim.frame_count == 0:
            # no animation to decompress
            return False

        trans_flags = anim.trans_flags0 + (anim.trans_flags1 << 32)
        rot_flags   = anim.rot_flags0   + (anim.rot_flags1 << 32)
        scale_flags = anim.scale_flags0 + (anim.scale_flags1 << 32)

        offset = anim.offset_to_compressed_data
        comp_data = anim.keyframe_data.STEPTREE
        if offset > 0:
            comp_data = comp_data[offset:]

        try:
            comp_data = animation_compression.compressed_frames_def.build(
                rawdata=comp_data)
        except Exception:
            print(format_exc())
            return False

        # make a nested list to store all transforms
        jma_animation = jma.JmaAnimation(
            anim.name, anim.node_list_checksum, anim.type.enum_name,
            anim.frame_info_type.enum_name, anim.flags.world_relative,
            [jma.JmaNode() for n in range(anim.node_count)]
            )

        jma_animation.rot_flags   = [bool(rot_flags   & (1 << i))
                                     for i in range(anim.node_count)]
        jma_animation.trans_flags = [bool(trans_flags & (1 << i))
                                     for i in range(anim.node_count)]
        jma_animation.scale_flags = [bool(scale_flags & (1 << i))
                                     for i in range(anim.node_count)]

        for f in range(anim.frame_count):
            jma_animation.add_frame(
                [jma.JmaNodeState() for n in range(anim.node_count)]
                )

        animation_compilation.compile_animation(anim, jma_animation)

        return True
