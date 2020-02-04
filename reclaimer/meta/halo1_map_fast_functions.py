#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

'''
Contains functions for quickly reading/writing certain structs in mapfiles.
This is very unstructured as it needs to be as fast as possible, so
raw offsets and map magic must be provided explicitely.
'''

from types import MethodType
from struct import pack, unpack

from reclaimer.constants import \
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

pack_4_uint32 = MethodType(pack, "<LLLL")
unpack_3_uint32 = MethodType(unpack, "<LLL")
unpack_4_uint32 = MethodType(unpack, "<LLLL")
unpack_5_uint32 = MethodType(unpack, "<LLLLL")


def read_reflexive(map_data, refl_offset, max_count=0xFFffFFff,
                   struct_size=1, tag_magic=None, unpacker=unpack_3_uint32):
    '''
    Reads a reflexive from the given map_data at the given offset.
    Returns the reflexive's offset and pointer.
    '''
    map_data.seek(refl_offset)
    count, start, id = unpacker(map_data.read(12))
    if tag_magic is not None:
        map_data.seek(0, 2)
        max_count = min(max_count,
                        (map_data.tell() - (start - tag_magic)) // struct_size)
    return min(count, max_count), start, id


def read_rawdata_ref(map_data, ref_offset, tag_magic=None,
                     unpacker=unpack_5_uint32):
    map_data.seek(ref_offset)
    size, flags, raw_pointer, pointer, id = unpacker(map_data.read(20))
    if tag_magic is not None:
        map_data.seek(0, 2)
        size = min(size, map_data.tell() - (pointer - tag_magic))
    return size, flags, raw_pointer, pointer, id


def move_rawdata_ref(map_data, raw_ref_offset, magic, engine, diffs_by_offsets,
                     unpacker=unpack_4_uint32, packer=pack_4_uint32):
    map_data.seek(raw_ref_offset - magic)
    size, flags, raw_ptr, ptr = unpacker(map_data.read(16))
    if not size or ((flags & 1) and "xbox" not in engine):
        return

    ptr_diff = 0
    # find the highest pointer that is still at or below this rawdatas pointer
    for off in diffs_by_offsets:
        if off <= raw_ptr:
            ptr_diff = max(diffs_by_offsets[off], ptr_diff)

    if not ptr_diff:
        return

    # TODO: Determine if we need to modify the regular pointer
    # and also determine in what way to modify it

    map_data.seek(0, 2)
    raw_ptr += ptr_diff
    assert raw_ptr + size <= map_data.tell()
    map_data.seek(raw_ref_offset - magic)
    map_data.write(packer(size, flags, raw_ptr, ptr))


def iter_reflexive_offs(map_data, refl_offset, struct_size,
                        max_count=0xFFffFFff, tag_magic=None):
    count, start, _ = read_reflexive(map_data, refl_offset, max_count,
                                     struct_size, tag_magic)
    return range(start, start + count*struct_size, struct_size)


def repair_dependency(index_array, map_data, tag_magic, repair, engine, cls,
                      dep_offset, map_magic=None):
    if map_magic is None:
        map_magic = tag_magic

    dep_offset -= tag_magic

    try:
        map_data.seek(dep_offset + 12)
    except ValueError:
        return

    tag_id = int.from_bytes(map_data.read(4), "little")
    tag_index_id = tag_id & 0xFFff

    if tag_index_id not in range(len(index_array)):
        return

    tag_index_ref = index_array[tag_index_id]
    if tag_index_ref.id != tag_id:
        return

    if cls is None:
        map_data.seek(dep_offset)
        cls = map_data.read(4)

    # if the class is obje or shdr, make sure to get the ACTUAL class
    if cls in (b'ejbo', b'meti', b'ived', b'tinu'):
        map_data.seek(tag_index_ref.meta_offset - map_magic)
        object_type = int.from_bytes(map_data.read(2), 'little')
        if object_type not in range(-1, len(object_class_bytes) - 1):
            return

        cls = object_class_bytes[object_type]
    elif cls == b'rdhs':
        map_data.seek(tag_index_ref.meta_offset - map_magic + 36)
        shader_type = int.from_bytes(map_data.read(2), 'little')
        if shader_type not in range(3, len(shader_class_bytes) - 1):
            return

        cls = shader_class_bytes[shader_type]
    elif cls in (b'2dom', b'edom'):
        if "xbox" in engine:
            cls = b'edom'
        else:
            cls = b'2dom'

    map_data.seek(dep_offset)
    map_data.write(cls)

    if tag_index_id not in repair:
        repair[tag_index_id] = cls[::-1].decode('latin1')
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
