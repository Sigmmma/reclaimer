#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

'''
Most byteswapping is handeled by supyr_struct by changing the endianness,
but certain chunks of raw data are significantly faster to just write
byteswapping routines for, like raw vertex, triangle, and animation data.
'''
import array

from reclaimer.sounds.util import byteswap_pcm16_sample_data
from supyr_struct.field_types import BytearrayRaw
from supyr_struct.defs.block_def import BlockDef

try:
    from .ext import byteswapping_ext
    fast_byteswapping = True
except:
    fast_byteswapping = False


raw_block_def = BlockDef("raw_block",
    BytearrayRaw('data',
        SIZE=lambda node, *a, **kw: 0 if node is None else len(node))
    )

def make_mutable_struct_array_copy(data, struct_size):
    valid_length = struct_size*(len(data)//struct_size)
    if valid_length == len(data):
        return bytearray(data)
    return bytearray(data[:valid_length])


def byteswap_struct_array(original, swapped, size, count=None, start=0,
                          two_byte_offs=(), four_byte_offs=(), eight_byte_offs=()):
    assert start >= 0

    for off in two_byte_offs:
        assert (off + 2) <= size

    for off in four_byte_offs:
        assert (off + 4) <= size

    for off in eight_byte_offs:
        assert (off + 8) <= size

    if size <= 0:
        return

    max_count = (min(len(original), len(swapped)) - start) // size
    if count is None:
        count = max_count
    else:
        count = min(max_count, count)

    if count <= 0:
        return

    end = start + count * size
    if fast_byteswapping:
        byteswapping_ext.byteswap_struct_array(
            original, swapped, start, end, size,
            array.array("I", two_byte_offs),
            array.array("I", four_byte_offs),
            array.array("I", eight_byte_offs),
            )
        return

    for field_off in two_byte_offs:
        for off in range(field_off + start, end, size):
            swapped[off]     = original[off + 1]
            swapped[off + 1] = original[off]

    for field_off in four_byte_offs:
        for off in range(field_off + start, end, size):
            swapped[off]     = original[off + 3]
            swapped[off + 1] = original[off + 2]
            swapped[off + 2] = original[off + 1]
            swapped[off + 3] = original[off]

    for field_off in eight_byte_offs:
        for off in range(field_off + start, end, size):
            swapped[off]     = original[off + 7]
            swapped[off + 1] = original[off + 6]
            swapped[off + 2] = original[off + 5]
            swapped[off + 3] = original[off + 4]
            swapped[off + 4] = original[off + 3]
            swapped[off + 5] = original[off + 2]
            swapped[off + 6] = original[off + 1]
            swapped[off + 7] = original[off]


def byteswap_raw_reflexive(refl):
    desc = refl.desc
    struct_size, two_byte_offs, four_byte_offs = desc.get(
        "RAW_REFLEXIVE_INFO", (0, (), ()))
    if not two_byte_offs and not four_byte_offs:
        return

    original = refl.STEPTREE
    swapped = make_mutable_struct_array_copy(original, struct_size)
    byteswap_struct_array(original, swapped, struct_size, refl.size, 0,
                          two_byte_offs, four_byte_offs)
    refl.STEPTREE = swapped


def byteswap_coll_bsp(bsp):
    for b in bsp:
        byteswap_raw_reflexive(b)


def byteswap_pcm16_samples(pcm_block):
    # replace the verts with the byteswapped ones
    pcm_block.STEPTREE = bytearray(
        byteswap_pcm16_sample_data(pcm_block.STEPTREE))


def byteswap_sbsp_meta(meta):
    if len(meta.collision_bsp.STEPTREE):
        for b in meta.collision_bsp.STEPTREE[0]:
            byteswap_raw_reflexive(b)

    # do NOT need to swap meta.nodes since they are always little endian
    for b in (meta.leaves, meta.leaf_surfaces, meta.surface,
              meta.lens_flare_markers, meta.breakable_surfaces, meta.markers):
        byteswap_raw_reflexive(b)


def byteswap_scnr_script_syntax_data(meta):
    original = meta.script_syntax_data.data
    swapped = original[: ((len(original)-56)//20) * 20 + 56]

    # swap the 56 byte header
    # first 32 bytes are a string
    byteswap_struct_array(
        original, swapped, 56, 1, 0,
        two_byte_offs=(32, 34, 38, 44, 46, 48, 50),
        four_byte_offs=(40, 52))

    # swap the 20 byte blocks
    byteswap_struct_array(
        original, swapped, 20, None, 56,
        two_byte_offs=(0, 2, 4, 6),
        four_byte_offs=(8, 12, 16)
        )

    meta.script_syntax_data.data = swapped


def byteswap_uncomp_verts(verts_block):
    original = verts_block.STEPTREE.data
    swapped = make_mutable_struct_array_copy(original, 68)

    byteswap_struct_array(
        original, swapped, 68, None, 0,
        two_byte_offs=(56, 58),
        four_byte_offs=(0, 4, 8, 12, 16, 20, 24, 28, 32,
                        36, 40, 44, 48, 52, 60, 64)
        )

    verts_block.STEPTREE.data = swapped
    verts_block.size = len(swapped)//68


def byteswap_comp_verts(verts_block):
    original = verts_block.STEPTREE.data
    swapped = make_mutable_struct_array_copy(original, 32)

    byteswap_struct_array(
        original, swapped, 32, None, 0,
        two_byte_offs=(24, 26, 28, 30),
        four_byte_offs=(0, 4, 8, 12, 16, 20)
        )

    verts_block.STEPTREE.data = swapped
    verts_block.size = len(swapped)//32


def byteswap_tris(tris_block):
    original = tris_block.STEPTREE.data
    swapped = make_mutable_struct_array_copy(original, 6)

    byteswap_struct_array(
        original, swapped, 6, None, 0,
        two_byte_offs=(0, 2, 4)
        )

    tris_block.STEPTREE.data = swapped
    tris_block.size = len(swapped)//6


def byteswap_animation(anim):
    frame_info   = anim.frame_info.STEPTREE
    default_data = anim.default_data.STEPTREE
    frame_data   = anim.frame_data.STEPTREE

    comp_data_offset = anim.offset_to_compressed_data
    frame_count = anim.frame_count
    node_count  = anim.node_count
    trans_int = anim.trans_flags0 + (anim.trans_flags1<<32)
    rot_int   = anim.rot_flags0   + (anim.rot_flags1  <<32)
    scale_int = anim.scale_flags0 + (anim.scale_flags1<<32)

    trans_flags = tuple(bool(trans_int & (1 << i)) for i in range(node_count))
    rot_flags   = tuple(bool(rot_int   & (1 << i)) for i in range(node_count))
    scale_flags = tuple(bool(scale_int & (1 << i)) for i in range(node_count))

    frame_info_size = {0: 0, 1: 8, 2: 12, 3: 16}.get(
        anim.frame_info_type.data, 0) * frame_count
    frame_size = (12 * sum(trans_flags) +
                  8  * sum(rot_flags) +
                  4  * sum(scale_flags))
    default_data_size = node_count * (12 + 8 + 4) - frame_size
    uncomp_frame_data_size = frame_size * frame_count

    if len(frame_info) < frame_info_size:
        raise ValueError("Expected %s bytes of frame info in '%s', but got %s" %
                         (frame_info_size, anim.name, len(frame_info)))
    elif default_data and len(default_data) < default_data_size:
        raise ValueError("Expected %s bytes of default data in '%s', but got %s" %
                         (default_data_size, anim.name, len(default_data)))
    elif not anim.flags.compressed_data:
        if len(frame_data) - comp_data_offset < uncomp_frame_data_size:
            raise ValueError(
                "Expected %s bytes of frame data in '%s', but got %s" %
                (uncomp_frame_data_size, anim.name, len(frame_data)))

    new_frame_info   = bytearray(frame_info_size)
    new_default_data = bytearray(default_data_size)

    # some tags actually have the offset as non-zero in meta form
    # and it actually matters, so we need to take this into account
    new_uncomp_frame_data = bytearray(uncomp_frame_data_size)

    # byteswap the frame info
    byteswap_struct_array(
        frame_info, new_frame_info, 4, None, 0,
        four_byte_offs=(0, )
        )

    default_data_two_byte_offsets = ()
    default_data_four_byte_offsets = ()
    frame_data_two_byte_offsets = ()
    frame_data_four_byte_offsets = ()
    i = j = 0
    for n in range(node_count):
        if rot_flags[n]:
            frame_data_two_byte_offsets += tuple(range(i, i + 8, 2))
            i += 8
        else:
            default_data_two_byte_offsets += tuple(range(j, j + 8, 2))
            j += 8

        if trans_flags[n]:
            frame_data_four_byte_offsets += tuple(range(i, i + 12, 4))
            i += 12
        else:
            default_data_four_byte_offsets += tuple(range(j, j + 12, 4))
            j += 12

        if scale_flags[n]:
            frame_data_four_byte_offsets += (i, )
            i += 4
        else:
            default_data_four_byte_offsets += (j, )
            j += 4

    if default_data and default_data_size:
        # byteswap the default_data
        byteswap_struct_array(
            default_data, new_default_data, default_data_size, 1, 0,
            two_byte_offs=default_data_two_byte_offsets,
            four_byte_offs=default_data_four_byte_offsets,
            )

    if not anim.flags.compressed_data or comp_data_offset and frame_size:
        # byteswap the frame_data
        byteswap_struct_array(
            frame_data, new_uncomp_frame_data, frame_size, frame_count, 0,
            two_byte_offs=frame_data_two_byte_offsets,
            four_byte_offs=frame_data_four_byte_offsets,
            )

    anim.frame_info.STEPTREE   = new_frame_info
    anim.default_data.STEPTREE = new_default_data
    anim.frame_data.STEPTREE   = new_uncomp_frame_data
    anim.offset_to_compressed_data = 0

    if anim.flags.compressed_data:
        anim.offset_to_compressed_data = len(new_uncomp_frame_data)
        anim.frame_data.STEPTREE += frame_data[comp_data_offset:]
