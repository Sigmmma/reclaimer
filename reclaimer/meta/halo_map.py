#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

import lzma
import zlib
import os

from copy import deepcopy

from reclaimer.constants import map_build_dates, map_magics, GEN_3_ENGINES
from reclaimer.meta.halo1_map import map_header_def, map_header_vap_def,\
     map_header_anni_def, map_header_demo_def, tag_index_pc_def,\
     tag_index_xbox_def, tag_index_anni_def
from reclaimer.meta.halo2_alpha_map import h2_alpha_map_header_def,\
     h2_alpha_tag_index_def
from reclaimer.meta.halo2_map import h2v_map_header_full_def,\
     h2v_map_header_def, h2x_map_header_full_def, h2x_map_header_def,\
     h2_tag_index_def
from reclaimer.meta.halo3_map import h3_map_header_def, h3_tag_index_def
from reclaimer.meta.shadowrun_map import sr_tag_index_def
from reclaimer.meta.stubbs_map import stubbs_tag_index_def

from supyr_struct.defs.tag_def import TagDef
from supyr_struct.buffer import get_rawdata


def get_map_version(header):
    try:
        version = header.version.enum_name
    except AttributeError:
        return None
    try:
        build_date = header.build_date
    except AttributeError:
        build_date = None

    if version == "halo1pc":
        # apparently the halo pc build and halo 2 alpha
        # use the same version integer of 7
        if build_date == map_build_dates["halo2alpha"]:
            version = "halo2alpha"
        elif build_date == map_build_dates["halo1anni"]:
            version = "halo1anni"
    elif version == "halo1xbox":
        if build_date is None:
            version = None
        elif build_date == map_build_dates["stubbs"]:
            version = "stubbs"
        elif build_date == "":
            if header.unknown in (11, 1033):
                # this is the only discernable difference
                # between xbox demo and stubbs pc maps
                version = "halo1xboxdemo"
            else:
                version = "stubbspc"
        elif build_date == map_build_dates["shadowrun_proto"]:
            version = "shadowrun_proto"
    elif hasattr(header, "yelo_header") and (
            header.yelo_header.yelo.enum_name == "yelo"):
        version = "halo1yelo"
    elif version == "halo2":
        version = None
        if build_date == map_build_dates['halo2beta']:
            version = "halo2beta"
        elif build_date == map_build_dates['halo2xbox']:
            version = "halo2xbox"
        elif build_date == map_build_dates['halo2epsilon']:
            version = "halo2epsilon"
        elif build_date == map_build_dates['halo2vista']:
            version = "halo2vista"
    elif version == "halo3":
        if build_date == map_build_dates['halo3odst']:
            version = "halo3odst"
    elif version == "haloreach":
        if build_date == map_build_dates['haloreachbeta']:
            version = "haloreachbeta"
        elif build_date == map_build_dates['halo4']:
            version = "halo4"

    return version


def get_map_header(map_file, header_only=False):
    if hasattr(map_file, "read"):
        orig_pos = map_file.tell()
        map_file.seek(0)
        header_data = map_file.read(2048)
        map_file.seek(orig_pos)
    else:
        header_data = map_file

    sig   = header_data[:4]
    sig_big    = sig.decode('latin-1').lower()
    sig_little = sig_big[::-1]
    ver_big    = int.from_bytes(header_data[4:8], 'big')
    ver_little = int.from_bytes(header_data[4:8], 'little')
    header_def = None

    if sig_little == "head":
        if ver_little == 8:
            build_date = header_data[300: 324].decode("latin-1")
            if build_date == map_build_dates['halo2vista']:
                header_def = h2v_map_header_full_def
                if header_only:
                    header_def = h2v_map_header_def
            else:
                header_def = h2x_map_header_full_def
                if header_only:
                    header_def = h2x_map_header_def

        elif ver_little in (5, 6, 609):
            header_def = map_header_def

        elif ver_little == 134:
            header_def = map_header_vap_def

        elif ver_little == 7:
            header_def = map_header_def
            build_date = header_data[64: 96].decode("latin-1")
            if build_date == map_build_dates['halo2alpha']:
                header_def = h2_alpha_map_header_def

    elif sig_big == "head":
        if ver_big == 11:
            header_def = h3_map_header_def
        elif ver_big == 7:
            header_def = map_header_anni_def

    elif header_data[704:708] == b'dehE' and header_data[1520:1524] == b'tofG':
        header_def = map_header_demo_def

    elif header_data[:2] == b'\x78\xDA':
        # zlib compressed halo 2 vista map.
        # decompress the 2048 byte header
        header_def = h2v_map_header_full_def
        decomp_len = None
        if header_only:
            header_def = h2v_map_header_def
            decomp_len = 2048

        map_file = zlib.decompressobj().decompress(map_file, decomp_len)

    if header_def is None:
        return None

    return header_def.build(rawdata=map_file)


def get_tag_index(map_data, header=None):
    if header is None:
        header = get_map_header(map_data)

    if header is None:
        return None

    map_data = decompress_map(map_data, header)
    base_address = header.tag_index_header_offset

    tag_index_def = tag_index_pc_def
    version = get_map_version(header)
    if "shadowrun" in version:
        tag_index_def = sr_tag_index_def
    elif "stubbs" in version:
        tag_index_def = stubbs_tag_index_def
    elif header.version.data < 6:
        tag_index_def = tag_index_xbox_def
    elif version == "halo2alpha":
        tag_index_def = h2_alpha_tag_index_def
    elif version == "halo1anni":
        tag_index_def = tag_index_anni_def
    elif header.version.enum_name == "halo2":
        tag_index_def = h2_tag_index_def
    elif header.version.enum_name == "halo3":
        tag_index_def = h3_tag_index_def

        for partition in header.partitions:
            if base_address in range(partition.load_address,
                                     partition.load_address + partition.size):
                base_address -= partition.load_address - partition.file_offset
                break

    if hasattr(header, "sections") and header.sections.tag.size == 0:
        # shared resource map. no tag index, so make a blank one
        return tag_index_def.build(map_header=header)

    tag_index = tag_index_def.build(
        rawdata=map_data, magic=get_map_magic(header),
        offset=base_address, map_header=header)

    return tag_index


def get_index_magic(header):
    version = get_map_version(header)
    if version == "halo2vista":
        return header.virtual_address
    elif version in GEN_3_ENGINES:
        base_address = header.tag_index_header_offset
        for partition in header.partitions:
            if base_address in range(partition.load_address,
                                     partition.load_address + partition.size):
                return partition.load_address - partition.file_offset

    return map_magics.get(version, 0)


def get_map_magic(header):
    magic = get_index_magic(header)
    if header.version.enum_name not in GEN_3_ENGINES:
        magic -= header.tag_index_header_offset

    return magic


def get_is_compressed_map(comp_data, header):
    if header.version.data == 134:
        return header.vap_header.compression_type.data != 0
    elif header.version.data not in (7, 609):
        decomp_len = header.decomp_len
        if get_map_version(header) == "pcstubbs":
            decomp_len -= 2048

        return decomp_len > len(comp_data)
    return False


def decompress_map(comp_data, header=None, decomp_path=None, writable=False):
    if header is None:
        header = get_map_header(comp_data)

    if not get_is_compressed_map(comp_data, header):
        # not actually compressed
        return comp_data
    elif header.version.data == 134:
        if header.vap_header.compression_type.enum_name == "lzma":
            return decompress_map_lzma(comp_data, header, decomp_path, writable)
        else:
            return comp_data
    else:
        return decompress_map_deflate(comp_data, header, decomp_path, writable)


def decompress_map_lzma(comp_data, header, decomp_path="", writable=False):
    vap_header = header.vap_header

    os.makedirs(os.path.dirname(decomp_path), exist_ok=True)
    if not decomp_path:
        decomp_path = "decomp.map"

    # get the info needed to decompress each block
    comp_offs = list(b.file_offset for b in vap_header.blocks)
    comp_sizes = list(b.file_size for b in vap_header.blocks)
    if not comp_offs:
        # if blocks is 0, entire compressed size is assumed to be one stream
        comp_offs.append(header.SIZE)
        comp_sizes.append(vap_header.compressed_size - header.SIZE)

    # copy the header and change the compression fields
    header_copy = deepcopy(header)
    header_copy.vap_header.compression_type.set_to("uncompressed")
    header_copy.vap_header.block_count = 0
    header_copy.vap_header.compressed_size = 0
    del header_copy.vap_header.blocks[:]

    with open(decomp_path, "wb+") as f:
        # size the uncompressed file to the right size
        f.seek(vap_header.decompressed_size - 1)
        f.write(b"\x00")

        # write the copied header to the map
        f.seek(0)
        f.write(header_copy.serialize())

        for in_off, in_size in zip(comp_offs, comp_sizes):
            comp_data.seek(in_off)
            f.write(lzma.decompress(comp_data.read(in_size)))

    # have to do this separate or seeking will be fucked
    return get_rawdata(filepath=decomp_path, writable=writable)


def decompress_map_deflate(comp_data, header, decomp_path="", writable=False):
    comp_data.seek(0)
    decomp_start = 2048
    decomp_len   = header.decomp_len
    version      = get_map_version(header)
    if version == "pcstubbs":
        decomp_len -= 2048
    elif version == "halo2vista":
        decomp_start = 0

    os.makedirs(os.path.dirname(decomp_path), exist_ok=True)
    if not decomp_path:
        decomp_path = "decomp.map"

    with open(decomp_path, "wb+") as f:
        if decomp_start:
            comp_data.seek(0)
            f.write(comp_data.read(decomp_start))
            comp_data.seek(decomp_start)
            comp_data = comp_data.read()

        decomp_obj = zlib.decompressobj()
        last_comp_len = len(comp_data)
        while comp_data:
            # decompress map 64Mb at a time
            f.write(decomp_obj.decompress(comp_data, 64*1024*1024))
            comp_data = decomp_obj.unconsumed_tail
            if len(comp_data) == last_comp_len:
                # need to do this to not get stuck in an infinite
                # loop where the compressed data doesnt actually
                # decode to anything because it is all zeros.
                break
            last_comp_len = len(comp_data)

        # pad the file to its decompressed length
        f.write(b'\xca'*(decomp_len - f.tell()))

    # have to do this separate or seeking will be fucked
    return get_rawdata(filepath=decomp_path, writable=writable)
