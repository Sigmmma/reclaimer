'''
Contains functions for quickly reading/writing certain structs in mapfiles.
This is very unstructured as it needs to be as fast as possible, so
raw offsets and map magic must be provided explicitely.
'''

from struct import Struct as PyStruct
from supyr_struct.defs.constants import *
from supyr_struct.defs.util import *
from reclaimer.os_v4_hek.handler import \
     tag_class_be_int_to_fcc_os,     tag_class_fcc_to_ext_os,\
     tag_class_be_int_to_fcc_stubbs, tag_class_fcc_to_ext_stubbs

tag_cls_int_to_fcc = dict(tag_class_be_int_to_fcc_os)
tag_cls_int_to_ext = {}

tag_cls_int_to_fcc.update(tag_class_be_int_to_fcc_stubbs)

for key in tag_class_be_int_to_fcc_os:
    tag_cls_int_to_ext[key] = tag_class_fcc_to_ext_os[
        tag_class_be_int_to_fcc_os[key]]

for key in tag_class_be_int_to_fcc_stubbs:
    tag_cls_int_to_ext[key] = tag_class_fcc_to_ext_stubbs[
        tag_class_be_int_to_fcc_stubbs[key]]


NULL_CLASS = b'\xFF\xFF\xFF\xFF'

shader_class_bytes = (
    NULL_CLASS,
    NULL_CLASS,
    NULL_CLASS,
    b'vnes',
    b'osos',
    b'rtos',
    b'ihcs',
    b'xecs',
    b'taws',
    b'algs',
    b'tems',
    b'alps',
    b'rdhs'
    )

object_class_bytes = (
    b'dpib',
    b'ihev',
    b'paew',
    b'piqe',
    b'brag',
    b'jorp',
    b'necs',
    b'hcam',
    b'lrtc',
    b'ifil',
    b'calp',
    b'ecss',
    b'ejbo'
    )

_3_uint32_struct = PyStruct("<LLL")

def move_rawdata_ref(map_data, raw_ref_offset, magic, engine, diffs_by_offsets,
                     unpacker=_3_uint32_struct.unpack,
                     packer=_3_uint32_struct.pack):
    map_data.seek(raw_ref_offset - magic)
    size, flags, raw_ptr = unpacker(map_data.read(12))
    if not size: return
    ptr_diff = 0
    for off, diff in diffs_by_offsets.items():
        if off <= raw_ptr:
            ptr_diff = diff

    if not ptr_diff or ((flags & 1) and "xbox" not in engine):
        return

    map_data.seek(0, 2)
    raw_ptr += ptr_diff
    assert raw_ptr + size <= map_data.tell()
    map_data.seek(raw_ref_offset - magic)
    map_data.write(packer(size, flags, raw_ptr))


def read_reflexive(map_data, refl_offset, unpacker=_3_uint32_struct.unpack):
    '''
    Reads a reflexive from the given map_data at the given offset.
    Returns the reflexive's offset and pointer.
    '''
    map_data.seek(refl_offset)
    return unpacker(map_data.read(12))


def iter_reflexive_offs(map_data, refl_offset, struct_size,
                        unpacker=_3_uint32_struct.unpack):
    map_data.seek(refl_offset)
    count, start, _ = unpacker(map_data.read(12))
    return range(start, start + count*struct_size, struct_size)


def repair_dependency(index_array, map_data, magic, repair, engine, cls,
                      dep_offset, map_magic=None):
    if map_magic is None:
        map_magic = magic

    dep_offset -= magic
    if cls is None:
        map_data.seek(dep_offset)
        cls = map_data.read(4)

    map_data.seek(dep_offset + 12)
    tag_id = int.from_bytes(map_data.read(4), "little") & 0xFFFF

    if tag_id != 0xFFFF:
        # if the class is obje or shdr, make sure to get the ACTUAL class
        if cls in b'ejbo\x00meti\x00ived\x00tinu':
            map_data.seek(index_array[tag_id].meta_offset - map_magic)
            cls = object_class_bytes[
                int.from_bytes(map_data.read(2), 'little')]
        elif cls == b'rdhs':
            map_data.seek(index_array[tag_id].meta_offset - map_magic + 36)
            cls = shader_class_bytes[
                int.from_bytes(map_data.read(2), 'little')]
        elif cls in b'2dom\x00edom':
            if "xbox" in engine:
                cls = b'edom'
            else:
                cls = b'2dom'

        map_data.seek(dep_offset)
        map_data.write(cls)

        if tag_id not in repair:
            repair[tag_id] = cls[::-1].decode('latin1')
            #DEBUG
            # print("        %s %s %s" % (tag_id, cls, dep_offset))


def repair_dependency_array(index_array, map_data, magic, repair, engine,
                            base_class, start, array_size, struct_size=16,
                            map_magic=None):
    '''Macro for deprotecting a contiguous array of dependencies'''
    for offset in range(start, start + array_size*struct_size, struct_size):
        repair_dependency(
            index_array, map_data, magic, repair, engine, base_class, offset,
            map_magic)


class_bytes_by_fcc = {
    "senv": b'vnes' + b'rdhs' + NULL_CLASS,  # 3
    "soso": b'osos' + b'rdhs' + NULL_CLASS,  # 4
    "sotr": b'rtos' + b'rdhs' + NULL_CLASS,  # 5
    "schi": b'ihcs' + b'rdhs' + NULL_CLASS,  # 6
    "scex": b'xecs' + b'rdhs' + NULL_CLASS,  # 7
    "swat": b'taws' + b'rdhs' + NULL_CLASS,  # 8
    "sgla": b'algs' + b'rdhs' + NULL_CLASS,  # 9
    "smet": b'tems' + b'rdhs' + NULL_CLASS,  # 10
    "spla": b'alps' + b'rdhs' + NULL_CLASS,  # 11
    "shdr": b'rdhs' + NULL_CLASS + NULL_CLASS,  # -1

    "bipd": b'dpib' + b'tinu' + b'ejbo',  # 0
    "vehi": b'ihev' + b'tinu' + b'ejbo',  # 1
    "weap": b'paew' + b'meti' + b'ejbo',  # 2
    "eqip": b'piqe' + b'meti' + b'ejbo',  # 3
    "garb": b'brag' + b'meti' + b'ejbo',  # 4
    "proj": b'jorp' + b'ejbo' + NULL_CLASS,  # 5
    "scen": b'necs' + b'ejbo' + NULL_CLASS,  # 6
    "mach": b'hcam' + b'ived' + b'ejbo',  # 7
    "ctrl": b'lrtc' + b'ived' + b'ejbo',  # 8
    "lifi": b'ifil' + b'ived' + b'ejbo',  # 9
    "plac": b'calp' + b'ejbo' + NULL_CLASS,  # 10
    "ssce": b'ecss' + b'ejbo' + NULL_CLASS,  # 11
    "obje": b'ejbo' + NULL_CLASS + NULL_CLASS  # -1
    }

for cls in tag_class_be_int_to_fcc_os.values():
    if cls not in class_bytes_by_fcc:
        cls_1 = bytes(cls[slice(None, None, -1)], "latin1")
        cls_2 = cls_3 = NULL_CLASS
        if cls_1 == b'gpfe':
            cls_2 == b'ppfe'
        elif cls_1 == b'gphs':
            cls_2 == b'pphs'

        class_bytes_by_fcc[cls] = cls_1 + cls_2 + cls_3
