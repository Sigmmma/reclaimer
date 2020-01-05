#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.meta.halo_map import tag_index_pc_def


def h2_alpha_to_h1_tag_index(map_header, tag_index):
    new_index = tag_index_pc_def.build()
    old_index_array = tag_index.tag_index
    new_index_array = new_index.tag_index

    # copy information from the h2 index into the h1 index
    new_index.scenario_tag_id = tag_index.scenario_tag_id
    new_index.tag_index_offset = tag_index.tag_index_offset
    new_index.tag_count = tag_index.tag_count

    for i in range(len(old_index_array)):
        old_index_entry = old_index_array[i]
        new_index_array.append()
        new_index_entry = new_index_array[-1]

        new_index_entry.class_1 = old_index_entry.class_1
        new_index_entry.class_2 = old_index_entry.class_2
        new_index_entry.class_3 = old_index_entry.class_3

        new_index_entry.id  = old_index_entry.id
        new_index_entry.pad = old_index_entry.flags
        new_index_entry.path_offset = old_index_entry.path_offset
        new_index_entry.meta_offset = old_index_entry.meta_offset
        new_index_entry.path = old_index_entry.path

    return new_index


def h2_to_h1_tag_index(map_header, tag_index):
    new_index = tag_index_pc_def.build()
    old_index_array = tag_index.tag_index
    new_index_array = new_index.tag_index

    # copy information from the h2 index into the h1 index
    new_index.scenario_tag_id = tag_index.scenario_tag_id
    new_index.tag_index_offset = tag_index.tag_index_offset
    new_index.tag_count = tag_index.tag_count

    tag_types = {}
    for typ in tag_index.tag_types:
        tag_types[typ.class_1.data] = [typ.class_1, typ.class_2, typ.class_3]

    for i in range(len(old_index_array)):
        old_index_entry = old_index_array[i]
        new_index_array.append()
        new_index_entry = new_index_array[-1]
        if old_index_entry.tag_class.data not in tag_types:
            new_index_entry.path = "reserved"
            new_index_entry.class_1.data = new_index_entry.class_2.data =\
                                           new_index_entry.class_3.data =\
                                           0xFFFFFFFF
            new_index_entry.id = 0xFFFFFFFF
            continue

        types = tag_types[old_index_entry.tag_class.data]
        new_index_entry.class_1 = types[0]
        new_index_entry.class_2 = types[1]
        new_index_entry.class_3 = types[2]

        new_index_entry.path = map_header.strings.\
                               tag_name_table[i].tag_name

        new_index_entry.id = old_index_entry.id
        new_index_entry.meta_offset = old_index_entry.offset
        if new_index_entry.meta_offset == 0:
            # might flag sbsp and ltmp tags as indexed
            new_index_entry.indexed = 1

    return new_index


def h3_to_h1_tag_index(map_header, tag_index):
    new_index = tag_index_pc_def.build()
    old_index_array = tag_index.tag_index
    new_index_array = new_index.tag_index

    # copy information from the h2 index into the h1 index
    #new_index.scenario_tag_id = tag_index.scenario_tag_id
    new_index.tag_index_offset = tag_index.tag_index_offset
    new_index.tag_count = tag_index.tag_count

    tag_types = {}
    for i in range(len(tag_index.tag_types)):
        typ = tag_index.tag_types[i]
        tag_types[i] = [typ.class_1, typ.class_2, typ.class_3]

    for i in range(len(old_index_array)):
        old_index_entry = old_index_array[i]
        new_index_array.append()
        new_index_entry = new_index_array[-1]
        if old_index_entry.tag_type_index not in tag_types:
            new_index_entry.path = "reserved"
            new_index_entry.class_1.data = new_index_entry.class_2.data =\
                                           new_index_entry.class_3.data =\
                                           0xFFFFFFFF
            new_index_entry.id = 0xFFFFFFFF
            continue

        types = tag_types[old_index_entry.tag_type_index]
        new_index_entry.class_1 = types[0]
        new_index_entry.class_2 = types[1]
        new_index_entry.class_3 = types[2]

        new_index_entry.path = map_header.strings.\
                               tag_name_table[i].tag_name

        new_index_entry.id = (old_index_entry.table_index << 16) + i
        new_index_entry.meta_offset = old_index_entry.offset
        if new_index_entry.meta_offset == 0:
            # might flag sbsp and ltmp tags as indexed
            new_index_entry.indexed = 1

    return new_index
