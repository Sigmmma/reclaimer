#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from struct import pack, unpack
from types import MethodType

from reclaimer.meta.halo1_map_fast_functions import iter_reflexive_offs,\
     move_rawdata_ref


def rawdata_ref_move_antr(tag_id, index_array, map_data, magic, engine,
                          diffs_by_offsets):
    tag_offset = index_array[tag_id].meta_offset
    for moff in iter_reflexive_offs(map_data, tag_offset + 116 - magic, 180):
        # frame info
        move_rawdata_ref(map_data, moff +  72, magic, engine, diffs_by_offsets)
        # default data
        move_rawdata_ref(map_data, moff + 140, magic, engine, diffs_by_offsets)
        # frame data
        move_rawdata_ref(map_data, moff + 160, magic, engine, diffs_by_offsets)


def rawdata_ref_move_bitm(tag_id, index_array, map_data, magic, engine,
                          diffs_by_offsets):
    packer   = MethodType(pack, "<L")
    unpacker = MethodType(unpack, "<H8xL")
    tag_offset = index_array[tag_id].meta_offset
    for moff in iter_reflexive_offs(map_data, tag_offset + 96 - magic, 48):
        ptr_off = moff - magic

        map_data.seek(ptr_off + 14)
        flags, raw_ptr = unpacker(map_data.read(14))
        if flags & (1<<8):
            # data in resource map
            continue

        ptr_diff = 0
        for off, diff in diffs_by_offsets.items():
            if off <= raw_ptr:
                ptr_diff = diff

        if not ptr_diff:
            continue

        # fix bitmap pointers
        map_data.seek(ptr_off + 24)
        map_data.write(packer(raw_ptr + ptr_diff))


def rawdata_ref_move_devc(tag_id, index_array, map_data, magic, engine,
                          diffs_by_offsets):
    tag_offset = index_array[tag_id].meta_offset
    # device id
    move_rawdata_ref(map_data, tag_offset +  4, magic, engine, diffs_by_offsets)
    # profile
    move_rawdata_ref(map_data, tag_offset + 24, magic, engine, diffs_by_offsets)


def rawdata_ref_move_font(tag_id, index_array, map_data, magic, engine,
                          diffs_by_offsets):
    # pixels
    move_rawdata_ref(map_data, index_array[tag_id].meta_offset + 136,
                     magic, engine, diffs_by_offsets)


def rawdata_ref_move_metr(tag_id, index_array, map_data, magic, engine,
                          diffs_by_offsets):
    # meter data
    move_rawdata_ref(map_data, index_array[tag_id].meta_offset + 152,
                     magic, engine, diffs_by_offsets)


def rawdata_ref_move_scnr(tag_id, index_array, map_data, magic, engine,
                          diffs_by_offsets):
    tag_offset = index_array[tag_id].meta_offset
    # scenario editor data
    move_rawdata_ref(map_data, tag_offset +  260, magic, engine, diffs_by_offsets)

    # comments
    for moff in iter_reflexive_offs(map_data, tag_offset + 280 - magic, 64):
        move_rawdata_ref(map_data, moff + 44, magic, engine, diffs_by_offsets)

    # recorded animations
    for moff in iter_reflexive_offs(map_data, tag_offset + 876 - magic, 64):
        move_rawdata_ref(map_data, moff + 44, magic, engine, diffs_by_offsets)

    # script syntax data
    move_rawdata_ref(map_data, tag_offset + 1140, magic, engine, diffs_by_offsets)
    # script string data
    move_rawdata_ref(map_data, tag_offset + 1160, magic, engine, diffs_by_offsets)

    # source files
    for moff in iter_reflexive_offs(map_data, tag_offset + 1216 - magic, 52):
        move_rawdata_ref(map_data, moff + 32, magic, engine, diffs_by_offsets)


def rawdata_ref_move_snd_(tag_id, index_array, map_data, magic, engine,
                          diffs_by_offsets):
    tag_offset = index_array[tag_id].meta_offset
    for moff in iter_reflexive_offs(map_data, tag_offset + 152 - magic, 72):
        for moff2 in iter_reflexive_offs(map_data, moff + 60 - magic, 124):
            # samples
            move_rawdata_ref(map_data, moff2 +  64, magic, engine, diffs_by_offsets)
            # mouth data
            move_rawdata_ref(map_data, moff2 +  84, magic, engine, diffs_by_offsets)
            # subtitle data
            move_rawdata_ref(map_data, moff2 + 104, magic, engine, diffs_by_offsets)


def rawdata_ref_move_shpp(tag_id, index_array, map_data, magic, engine,
                          diffs_by_offsets):
    # shader code binary
    move_rawdata_ref(map_data, index_array[tag_id].meta_offset + 24,
                     magic, engine, diffs_by_offsets)


def rawdata_ref_move_sidy(tag_id, index_array, map_data, magic, engine,
                          diffs_by_offsets):
    # documentation
    move_rawdata_ref(map_data, index_array[tag_id].meta_offset,
                     magic, engine, diffs_by_offsets)


rawdata_ref_move_functions = {
    "antr": rawdata_ref_move_antr,
    "bitm": rawdata_ref_move_bitm,
    "devc": rawdata_ref_move_devc,
    "font": rawdata_ref_move_font,
    "metr": rawdata_ref_move_metr,
    "scnr": rawdata_ref_move_scnr,
    "snd!": rawdata_ref_move_snd_,

    # open sauce
    "magy": rawdata_ref_move_antr,
    "shpg": rawdata_ref_move_shpp,
    "shpp": rawdata_ref_move_shpp,
    "sidy": rawdata_ref_move_sidy,
    }
