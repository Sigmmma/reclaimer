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

from struct import Struct as PyStruct
from reclaimer.animation import util as anim_util
from reclaimer.sounds import audioop
from supyr_struct.field_types import BytearrayRaw
from supyr_struct.defs.block_def import BlockDef

try:
    from .ext import byteswapping_ext
    fast_byteswapping = True
except ImportError:
    fast_byteswapping = False

# These end_swap_XXXX functions are for byteswapping the
# endianness of values parsed from tags as the wrong order.
def end_swap_float(v, packer=PyStruct(">f").pack,
                   unpacker=PyStruct("<f").unpack):
    return unpacker(packer(v))[0]

def end_swap_int32(v):
    assert v >= -0x80000000 and v < 0x80000000
    if v < 0:
        v += 0x100000000
    v = ((((v << 24) + (v >> 24)) & 0xFF0000FF) +
         ((v << 8) & 0xFF0000) +
         ((v >> 8) & 0xFF00))
    if v & 0x80000000:
        return v - 0x100000000
    return v

def end_swap_int16(v):
    assert v >= -0x8000 and v < 0x8000
    if v < 0:
        v += 0x10000
    v = ((v << 8)  + (v >> 8)) & 0xFFFF
    if v & 0x8000:
        return v - 0x10000
    return v

def end_swap_uint32(v):
    assert v >= 0 and v <= 0xFFFFFFFF
    return ((((v << 24) + (v >> 24)) & 0xFF0000FF) +
            ((v << 8) & 0xFF0000) +
            ((v >> 8) & 0xFF00))

def end_swap_uint16(v):
    assert v >= 0 and v <= 0xFFFF
    return ((v << 8) + (v >> 8)) & 0xFFFF


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
    for offs, width in ([two_byte_offs,   2],
                        [four_byte_offs,  4],
                        [eight_byte_offs, 8]):
        for i in offs:
            assert i + width <= size, (
                f"byteswap range[{i}:{i+width}] outside struct size {size}"
                )

    if size <= 0:
        return

    orig_len  = len(original)
    swap_len  = len(swapped)
    max_count = (min(orig_len, swap_len) - start) // size
    count     = max_count if count is None else min(max_count, count)
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

    # for each set of offsets, use a slice of X width
    # to byteswap each item of X width at those offsets
    for width, offsets in ([2, two_byte_offs],
                           [4, four_byte_offs],
                           [8, eight_byte_offs]):
        for field_off in offsets:
            for off_s in range(field_off + start, end, size):
                off_o = off_s - (1 + orig_len)
                swapped[off_s: off_s+width] = original[off_o+width: off_o: -1]


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
        audioop.byteswap(pcm_block.STEPTREE, 2)
        )


def byteswap_sbsp_meta(meta):
    if len(meta.collision_bsp.STEPTREE):
        for b in meta.collision_bsp.STEPTREE[0]:
            byteswap_raw_reflexive(b)

    # do NOT need to swap meta.nodes since they are always little endian
    for b in (meta.leaves, meta.leaf_surfaces, meta.surface,
              meta.lens_flare_markers, meta.breakable_surfaces, meta.markers):
        byteswap_raw_reflexive(b)


def byteswap_anniversary_antr(meta):
    # NOTE: don't need to byteswap the uncompresed animation data, as that's
    #       already handled by the non-anniversary antr byteswapping code.

    for b in meta.animations.STEPTREE:
        b.first_permutation_index = end_swap_int16(b.first_permutation_index)
        b.chance_to_play = end_swap_float(b.chance_to_play)
        if not b.flags.compressed_data:
            continue

        # slice out the compressed data and byteswap the 
        # 11 UInt32 that make up the 44 byte header that
        # points to the 
        comp_data = bytearray(b.frame_data.data[b.offset_to_compressed_data: ])
        unswapped = bytes(comp_data)
        byteswap_struct_array(
            unswapped, comp_data, count=11, size=4, four_byte_offs=[0],
            )
        header = PyStruct("<11i").unpack(comp_data[: 44])

        # figure out where each array starts, ends, and the item size
        starts = (0, *header)
        ends   = (*header, len(comp_data))
        widths = (4, 2, 2, 2,  4, 2, 4, 4,  4, 2, 4, 4)

        # byteswap each array
        for start, end, width in zip(starts, ends, widths):
            byteswap_struct_array(
                unswapped, comp_data, size=width, 
                count = (end - start)//width,
                four_byte_offs=([0] if width == 4 else []),
                two_byte_offs=( [0] if width == 2 else []),
                )

        # replace the frame_data with the compressed data and some
        # blank uncompressed default/frame data so tool doesnt cry
        frame_data_size   = b.frame_count * b.frame_size
        default_data_size = b.node_count * (12 + 8 + 4) - b.frame_size

        b.offset_to_compressed_data = frame_data_size

        b.frame_data.data    = bytearray(frame_data_size) + comp_data
        b.default_data.data += bytearray(
            max(0, len(b.default_data.data) - default_data_size)
            )


def byteswap_anniversary_sbsp(meta):
    # make a copy of the nodes to byteswap to
    orig    = meta.nodes.STEPTREE
    swapped = meta.nodes.STEPTREE = make_mutable_struct_array_copy(orig, 2)
    byteswap_struct_array(
        orig, swapped, size=2,
        two_byte_offs=[0],
        )

    for lm in meta.lightmaps.STEPTREE:
        for b in lm.materials.STEPTREE:
            # logic is the same, so put comp/uncomp byteswap in a loop
            for v_size, lm_v_size, rawdata_ref, sint16_offs in (
                    [56, 20, b.uncompressed_vertices,   ()], 
                    [32,  8, b.compressed_vertices, (4, 6)]
                    ):
                verts_size    = v_size    * b.vertices_count
                lm_verts_size = lm_v_size * b.lightmap_vertices_count

                # make a copy of the verts to byteswap to
                orig    = rawdata_ref.STEPTREE[: verts_size+lm_verts_size]
                swapped = rawdata_ref.STEPTREE = make_mutable_struct_array_copy(orig, 2)

                # render verts first
                byteswap_struct_array(
                    orig, swapped, size=v_size, 
                    start=0, count=b.vertices_count,
                    four_byte_offs=range(0, v_size, 4),
                    )

                # followed by lightmap verts
                byteswap_struct_array(
                    orig, swapped, size=lm_v_size, 
                    start=verts_size, count=b.lightmap_vertices_count,
                    four_byte_offs=range(0, lm_v_size, 4),
                    two_byte_offs=sint16_offs,
                    )


def byteswap_anniversary_rawdata_ref(rawdata_ref, **kwargs):
    if rawdata_ref.size:
        orig    = rawdata_ref.serialize(attr_index="data")
        swapped = bytearray(orig)
        byteswap_struct_array(orig, swapped, **kwargs)
        rawdata_ref.parse(rawdata=swapped, attr_index="data")


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
        two_byte_offs=(24, 26, 30),
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

    comp_offset = anim.offset_to_compressed_data
    is_comp     = bool(anim.flags.compressed_data)

    rot_flags, trans_flags, scale_flags = anim_util.get_anim_flags(anim)

    frame_size = 12*sum(trans_flags) + 8*sum(rot_flags) + 4*sum(scale_flags)
    finfo_size = anim.frame_count * {
        1: 8, 2: 12, 3: 16
        }.get(anim.frame_info_type.data, 0)

    # NOTE: any nodes not animated by frame_data have a default value in
    #       the default_data. the size of the default data is complimentary
    #       to the size of a frame, such that combined they add to 24 bytes
    default_data_size = anim.node_count * 24 - frame_size
    uncomp_frame_data_size = frame_size * anim.frame_count

    if len(frame_info) < finfo_size:
        raise ValueError("Expected %s bytes of frame info in '%s', but got %s" %
                         (finfo_size, anim.name, len(frame_info)))
    elif default_data and len(default_data) < default_data_size:
        raise ValueError("Expected %s bytes of default data in '%s', but got %s" %
                         (default_data_size, anim.name, len(default_data)))
    elif not is_comp and len(frame_data) - comp_offset < uncomp_frame_data_size:
        raise ValueError(
            "Expected %s bytes of frame data in '%s', but got %s" %
            (uncomp_frame_data_size, anim.name, len(frame_data)))

    new_frame_info   = bytearray(finfo_size)
    new_default_data = bytearray(default_data_size)
    new_frame_data   = bytearray(uncomp_frame_data_size)

    # NOTE: some tags actually have the offset to the compressed data
    #       as non-zero in cache/meta form, so we need to handle it.

    # byteswap the frame info
    byteswap_struct_array(frame_info, new_frame_info, 4, four_byte_offs=(0, ))

    # loop twice, once for byteswapping default data, and once for frame data
    for is_fdata, data, new_data, size, count in (
            [False, default_data, new_default_data, default_data_size, 1],
            [True,  frame_data,   new_frame_data,   frame_size, anim.frame_count],
            ):
        if is_fdata and is_comp and comp_offset:
            # compressed data with no frame_data to byteswap
            continue
        elif not (data and new_data and size):
            # nothing to operate on
            continue

        i  = 0
        kw = dict(two_byte_offs=[], four_byte_offs=[])
        for n in range(anim.node_count):
            for stride, width, key in (
                [2,  8*(is_fdata == rot_flags[n]),    "two_byte_offs"],
                [4, 12*(is_fdata == trans_flags[n]), "four_byte_offs"],
                [4,  4*(is_fdata == scale_flags[n]), "four_byte_offs"],
                ):
                kw[key].extend(range(i, i + width, stride))
                i += width

        # byteswap the default_data
        byteswap_struct_array(data, new_data, size, count, **kw)

    anim.frame_info.STEPTREE   = new_frame_info
    anim.default_data.STEPTREE = new_default_data
    anim.frame_data.STEPTREE   = new_frame_data

    anim.offset_to_compressed_data = len(new_frame_data) if is_comp else 0
    anim.frame_data.STEPTREE += frame_data[comp_offset:] if is_comp else b''
