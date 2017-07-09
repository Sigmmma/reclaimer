import zlib
import os
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef
from supyr_struct.buffer import PeekableMmap
from .halo1_map import *
from .halo2_map import *
from .halo3_map import *


def get_map_version(header):
    version = header.version.enum_name
    if version == "halo1xbox":
        if header.build_date == map_build_dates["stubbs"]:
            version = "stubbs"
        elif header.build_date == map_build_dates["stubbspc"]:
            version = "stubbspc"
    elif hasattr(header, "yelo_header") and (
        header.yelo_header.yelo.enum_name == "halo1yelo"):
        return "halo1yelo"
    return version


def get_map_header(map_data):
    header_def = map_header_def
    if map_data[704:708] == b'dehE' and map_data[1520:1524] == b'tofG':
        header_def = map_header_demo_def
    elif map_data[4:8] == b'\x08\x00\x00\x00':
        header_def = halo2_map_header_def
    elif map_data[4:8] == b'\x00\x00\x00\x0b':
        header_def = halo3_map_header_def
    return header_def.build(rawdata=map_data)


def get_tag_index(map_data, header=None):
    if header is None:
        header = get_map_header(map_data)

    map_data = decompress_map(map_data, header)
    magic = 0

    tag_index_def = tag_index_pc_def
    if header.version.data < 6 and get_map_version(header) != "stubbspc":
        tag_index_def = tag_index_xbox_def
    elif header.version.enum_name == "halo2":
        tag_index_def = halo2_tag_index_def
    elif header.version.enum_name == "halo3":
        tag_index_def = halo3_tag_index_def
        magic = HALO3_INDEX_MAGIC

    if header.tag_index_header_offset - magic <= 0:
        tag_index = tag_index_def.build()
    else:
        tag_index = tag_index_def.build(
            rawdata=map_data, magic=get_map_magic(header),
            offset=header.tag_index_header_offset - magic)

    return tag_index


def get_index_magic(header):
    return map_magics.get(get_map_version(header), 0)


def get_map_magic(header):
    magic = get_index_magic(header)
    if header.version.enum_name != "halo3":
        magic -= header.tag_index_header_offset

    return magic


def is_compressed(comp_data, header):
    if header.version.data not in (7, 609):
        decomp_len = header.decomp_len
        if get_map_version(header) == "pcstubbs":
            decomp_len -= 2048

        return decomp_len > len(comp_data)
    return False


def decompress_map(comp_data, header=None, decomp_path=None):
    if header is None:
        header = get_map_header(comp_data)

    if is_compressed(comp_data, header):
        comp_data.seek(0)
        decomp_len = header.decomp_len
        if get_map_version(header) == "pcstubbs":
            decomp_len -= 2048

        if decomp_path is None:
            decomp_path = "decomp.map"
        else:
            temp_dir = os.path.dirname(decomp_path)
            if not os.path.isdir(temp_dir):
                os.makedirs(temp_dir)

        print("Decompressing map to: %s" % decomp_path)
        with open(decomp_path, "wb+") as f:
            f.write(comp_data[:2048])
            comp_data = comp_data[2048:]
            decomp_obj = zlib.decompressobj()

            while comp_data:
                # decompress map 64Mb at a time
                f.write(decomp_obj.decompress(comp_data, 64*1024*1024))
                comp_data = decomp_obj.unconsumed_tail

            # pad the file to its decompressed length
            f.write(b'\xca'*(decomp_len - f.tell()))

        # have to do this separate or seeking will be fucked
        with open(decomp_path, "rb+") as f:
            decomp_data = PeekableMmap(f.fileno(), 0)
    else:
        decomp_data = comp_data

    # not actually compressed
    return decomp_data
