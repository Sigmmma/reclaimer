import zlib
import os
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef
from supyr_struct.buffer import PeekableMmap
from .halo1_map import *
from .halo2_alpha_map import *
from .halo2_map import *
from .halo3_map import *
from .shadowrun_map import *


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
    elif version == "halo1xbox":
        if build_date is None:
            return
        elif build_date == map_build_dates["stubbs"]:
            version = "stubbs"
        elif build_date == map_build_dates["stubbspc"]:
            if header.unknown in (11, 1033):
                # this is the only discernable difference
                # between xbox beta and stubbs pc maps
                version = "halo1xboxbeta"
            else:
                version = "stubbspc"
        elif build_date == map_build_dates["shadowrun_beta"]:
            version = "shadowrun_beta"
    elif hasattr(header, "yelo_header") and (
            header.yelo_header.yelo.enum_name == "yelo"):
        return "halo1yelo"
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

    return version


def get_map_header(map_file, header_only=False):
    if hasattr(map_file, "read"):
        orig_pos = map_file.tell()
        map_file.seek(0)
        map_data = map_file.read(2048)
        map_file.seek(orig_pos)
    else:
        map_data = map_file

    sig   = map_data[:4]
    sig_b = sig.decode('latin-1').lower()
    sig_l = sig_b[::-1]
    ver_b = int.from_bytes(map_data[4:8], 'big')
    ver_l = int.from_bytes(map_data[4:8], 'little')
    header_def = None

    if sig_l == "head":
        if ver_l == 8:
            build_date = map_data[300: 324].decode("latin-1")
            if build_date == map_build_dates['halo2vista']:
                header_def = h2v_map_header_full_def
                if header_only:
                    header_def = h2v_map_header_def
            else:
                header_def = h2x_map_header_full_def
                if header_only:
                    header_def = h2x_map_header_def

        elif ver_l in (5, 6, 609):
            header_def = map_header_def
        elif ver_l == 7:
            header_def = map_header_def
            build_date = map_data[64: 96].decode("latin-1")
            if build_date == map_build_dates['halo2alpha']:
                h2_alpha_map_header_def

    elif sig_b == "head":
        if ver_b == 11:
            header_def = h3_map_header_def

    elif map_data[704:708] == b'dehE' and map_data[1520:1524] == b'tofG':
        header_def = map_header_demo_def

    elif map_data[:2] == b'\x78\xDA':
        # zlib compressed halo 2 vista map.
        # decompress the 2048 byte header
        header_def = h2v_map_header_full_def
        decomp_len = None
        if header_only:
            header_def = h2v_map_header_def
            decomp_len = 2048

        map_data = zlib.decompressobj().decompress(map_data, decomp_len)

    if header_def is None:
        return None

    return header_def.build(rawdata=map_data)


def get_tag_index(map_data, header=None):
    if header is None:
        header = get_map_header(map_data)

    map_data = decompress_map(map_data, header)
    magic = 0

    tag_index_def = tag_index_pc_def
    version = get_map_version(header)
    if "shadowrun" in version:
        tag_index_def = sr_tag_index_def
    elif header.version.data < 6 and version != "stubbspc":
        tag_index_def = tag_index_xbox_def
    elif version == "halo2alpha":
        tag_index_def = h2_alpha_tag_index_def
    elif header.version.enum_name == "halo2":
        tag_index_def = h2_tag_index_def
    elif header.version.enum_name == "halo3":
        tag_index_def = h3_tag_index_def
        magic = HALO3_INDEX_MAGIC

    if header.tag_index_header_offset - magic <= 0:
        tag_index = tag_index_def.build()
    else:
        tag_index = tag_index_def.build(
            rawdata=map_data, magic=get_map_magic(header),
            offset=header.tag_index_header_offset - magic)

    return tag_index


def get_index_magic(header):
    version = get_map_version(header)
    if version == "halo2vista" and header.map_type.enum_name == "mp":
        return H2V_MP_INDEX_MAGIC

    return map_magics.get(version, 0)


def get_map_magic(header):
    magic = get_index_magic(header)
    if header.version.enum_name != "halo3":
        magic -= header.tag_index_header_offset

    return magic


def get_is_compressed_map(comp_data, header):
    if header.version.data not in (7, 609):
        decomp_len = header.decomp_len
        if get_map_version(header) == "pcstubbs":
            decomp_len -= 2048

        return decomp_len > len(comp_data)
    return False


def decompress_map(comp_data, header=None, decomp_path=None):
    if header is None:
        header = get_map_header(comp_data)

    if get_is_compressed_map(comp_data, header):
        comp_data.seek(0)
        decomp_start = 2048
        decomp_len   = header.decomp_len
        version      = get_map_version(header)
        if version == "pcstubbs":
            decomp_len -= 2048
        elif version == "halo2vista":
            decomp_start = 0

        if decomp_path is None:
            decomp_path = "decomp.map"
        else:
            temp_dir = os.path.dirname(decomp_path)
            if temp_dir and not os.path.isdir(temp_dir):
                os.makedirs(temp_dir)

        with open(decomp_path, "wb+") as f:
            if decomp_start:
                f.write(comp_data[:decomp_start])
                comp_data = comp_data[decomp_start:]

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
        with open(decomp_path, "rb+") as f:
            decomp_data = PeekableMmap(f.fileno(), 0)
    else:
        decomp_data = comp_data

    # not actually compressed
    return decomp_data
