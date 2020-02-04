#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from copy import deepcopy
from reclaimer.animation import serialization
from reclaimer.animation import jma
from reclaimer.model import jms

__all__ = ("compress_animation", "decompress_animation")


def decompress_animation(anim, keep_compressed=True, endian=">"):
    if not anim.flags.compressed_data:
        return False

    jma_anim = jma.JmaAnimation(
        anim.name, anim.node_list_checksum, anim.type.enum_name,
        anim.frame_info_type.enum_name, anim.flags.world_relative
        )
    jma_anim.trans_flags_int = anim.trans_flags0 | (anim.trans_flags1 << 32)
    jma_anim.rot_flags_int   = anim.rot_flags0   | (anim.rot_flags1   << 32)
    jma_anim.scale_flags_int = anim.scale_flags0 | (anim.scale_flags1 << 32)

    # decompress the frame data
    _, jma_anim.frames = serialization.deserialize_compressed_frame_data(anim)

    # make some fake nodes so the serialization functions work
    jma_anim.nodes = jms.util.generate_fake_nodes(anim.node_count)

    # serialize the animation data
    def_data   = serialization.serialize_default_data(jma_anim, endian)
    frame_data = serialization.serialize_frame_data(jma_anim, endian)

    if keep_compressed:
        anim.offset_to_compressed_data = len(frame_data)
        frame_data += anim.frame_data.STEPTREE[anim.offset_to_compressed_data: ]
    else:
        anim.offset_to_compressed_data = 0
        anim.flags.compressed_data = False

    anim.frame_size = jma_anim.frame_data_frame_size
    anim.default_data.STEPTREE = def_data
    anim.frame_data.STEPTREE = frame_data
    return True


def compress_animation(anim, endian=">", **kw):
    jma_anim = kw.pop("jma_anim", None)
    if jma_anim is None:
        jma_anim = jma.JmaAnimation(
            anim.name, anim.node_list_checksum, anim.type.enum_name,
            anim.frame_info_type.enum_name, anim.flags.world_relative
            )
        jma_anim.trans_flags_int = anim.trans_flags0 | (anim.trans_flags1 << 32)
        jma_anim.rot_flags_int   = anim.rot_flags0   | (anim.rot_flags1   << 32)
        jma_anim.scale_flags_int = anim.scale_flags0 | (anim.scale_flags1 << 32)

        # create the node states from the frame_data and default_data
        jma_anim.frames = serialization.deserialize_frame_data(
            anim, None, True, endian)

        # make some fake nodes so the serialization functions work
        jma_anim.nodes = jms.util.generate_fake_nodes(anim.node_count)

        keyframes = kw.pop("keyframes", None)
        # either use provided keyframes, or generate them
        if keyframes is None:
            jma_anim.compress_animation(**kw)
        else:
            jma_anim.rot_keyframes   = keyframes[0]
            jma_anim.trans_keyframes = keyframes[1]
            jma_anim.scale_keyframes = keyframes[2]

    if jma_anim.root_node_info_applied:
        jma_anim = deepcopy(jma_anim)
        jma_anim.apply_root_node_info_to_states(True)

    # serialize the animation data
    comp_frame_data = serialization.serialize_compressed_frame_data(jma_anim)

    uncomp_frame_data = anim.frame_data.STEPTREE
    if anim.flags.compressed_data:
        del uncomp_frame_data[anim.offset_to_compressed_data: ]

    anim.offset_to_compressed_data = len(uncomp_frame_data)
    anim.flags.compressed_data = True
    anim.frame_data.STEPTREE = uncomp_frame_data + comp_frame_data

    return True
