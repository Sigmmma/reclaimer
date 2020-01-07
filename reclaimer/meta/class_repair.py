#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from reclaimer.meta.halo1_map_fast_functions import shader_class_bytes,\
     object_class_bytes, read_reflexive, read_rawdata_ref, iter_reflexive_offs,\
     repair_dependency, repair_dependency_array
from reclaimer.halo_script.hsc import get_hsc_data_block,\
     HSC_IS_SCRIPT_OR_GLOBAL
#from supyr_struct.util import *

MAX_MATERIAL_COUNT = 33


def get_tagc_refs(meta_offset, map_data, magic, tag_classes_by_id, tag_index_array):
    try:
        ct, moff, _ = read_reflexive(map_data, meta_offset - magic, 200, 16, magic)
    except Exception:
        return [], []

    if ct > 200 or ct <= 0 or moff != meta_offset + 12:
        return [], []

    # might be Soul, but need to check tag classes to make sure
    try:
        reffed_ids = []
        reffed_types = []
        for moff2 in iter_reflexive_offs(
                map_data, meta_offset - magic, 16, 200, magic):
            map_data.seek(moff2 - magic + 12)
            tag_id = int.from_bytes(map_data.read(4), "little")
            if tag_id == 0xFFffFFff:
                continue
            elif ((tag_id & 0xFFff) not in range(len(tag_index_array)) or
                  tag_index_array[tag_id & 0xFFff].id != tag_id):
                # break on the first invalid tag id.
                # the reflexive size might be corrupt
                break

            reffed_ids.append(tag_id & 0xFFff)
            reffed_types.append(tag_classes_by_id.get(tag_id & 0xFFff))

        return reffed_ids, reffed_types
    except Exception:
        pass

    return [], []


def repair_hud_background(index_array, map_data, magic, repair, engine, offset):
    args = (index_array, map_data, magic, repair, engine, b'mtib')
    repair_dependency(*(args + (offset + 36, )))
    # multitex overlays
    for moff in iter_reflexive_offs(map_data, offset + 88 - magic, 480, 30, magic):
        repair_dependency(*(args + (moff + 100, )))
        repair_dependency(*(args + (moff + 116, )))
        repair_dependency(*(args + (moff + 132, )))


def repair_devi_attrs(offset, index_array, map_data, magic, repair, engine):
    # struct size is 276
    args = (index_array, map_data, magic, repair, engine)
    repair_dependency(*(args + (None, offset + 36)))
    repair_dependency(*(args + (None, offset + 52)))
    repair_dependency(*(args + (None, offset + 68)))
    repair_dependency(*(args + (None, offset + 84)))
    repair_dependency(*(args + (None, offset + 100)))
    repair_dependency(*(args + (None, offset + 116)))
    repair_dependency(*(args + (None, offset + 144)))


def repair_item_attrs(offset, index_array, map_data, magic, repair, engine):
    # struct size is 396
    args = (index_array, map_data, magic, repair, engine)
    repair_dependency(*(args + (b'toof', offset + 204)))
    repair_dependency(*(args + (b'!dns', offset + 220)))
    repair_dependency(*(args + (b'effe', offset + 364)))
    repair_dependency(*(args + (b'effe', offset + 380)))


def repair_unit_attrs(offset, index_array, map_data, magic, repair, engine):
    # struct size is 372
    args = (index_array, map_data, magic, repair, engine)
    repair_dependency(*(args + (b'effe', offset + 12)))

    # camera tracks
    ct, moff, _ = read_reflexive(map_data, offset + 120 - magic, 2, 28, magic)
    repair_dependency_array(*(args + (b'kart', moff, ct, 28)))

    repair_dependency(*(args + (b'vtca', offset + 208)))
    repair_dependency(*(args + (b'!tpj', offset + 268)))

    # new hud interfaces
    ct, moff, _ = read_reflexive(map_data, offset + 300 - magic, 2, 48, magic)
    repair_dependency_array(*(args + (b'ihnu', moff, ct, 48)))

    # dialogue variants
    ct, moff, _ = read_reflexive(map_data, offset + 312 - magic, 16, 24, magic)
    repair_dependency_array(*(args + (b'gldu', moff + 8, ct, 24)))

    # weapons
    ct, moff, _ = read_reflexive(map_data, offset + 348 - magic, 4, 36, magic)
    repair_dependency_array(*(args + (b'paew', moff, ct, 36)))

    # seats
    for moff in iter_reflexive_offs(map_data, offset + 360 - magic, 284, 16, magic):
        # camera tracks
        ct, moff2, _ = read_reflexive(map_data, moff + 208 - magic, 2, 28, magic)
        repair_dependency_array(*(args + (b'kart', moff2, ct, 28)))

        # new hud interfaces
        ct, moff2, _ = read_reflexive(map_data, moff + 220 - magic, 2, 48, magic)
        repair_dependency_array(*(args + (b'ihnu', moff2, ct, 48)))

        repair_dependency(*(args + (b'vtca', moff + 248)))

        if "yelo" in engine:
            # seat extension
            for moff2 in iter_reflexive_offs(map_data, moff + 264 - magic, 100, 1, magic):
                # seat boarding
                for moff3 in iter_reflexive_offs(map_data, moff2 + 28 - magic, 112, 1, magic):
                    # seat keyframe action
                    for moff4 in iter_reflexive_offs(map_data, moff3 + 76 - magic, 152, 12, magic):
                        repair_dependency(*(args + (b'!tpj', moff4 + 48)))
                        repair_dependency(*(args + (b'effe', moff4 + 68)))

                # seat damage
                for moff3 in iter_reflexive_offs(map_data, moff2 + 40 - magic, 136, 1, magic):
                    repair_dependency(*(args + (b'!tpj', moff3 + 4)))
                    repair_dependency(*(args + (b'!tpj', moff3 + 96)))

    if "yelo" in engine:
        # unit extension
        for moff in iter_reflexive_offs(map_data, offset + 288 - magic, 60, 1, magic):
            # mounted states
            for moff2 in iter_reflexive_offs(map_data, moff - magic, 128, 1, magic):
                # camera tracks
                ct, moff3, _ = read_reflexive(map_data, moff2 + 80 - magic, 2, 28, magic)
                repair_dependency_array(*(args + (b'kart', moff3, ct, 28)))

                # unit keyframe action
                for moff3 in iter_reflexive_offs(map_data, moff2 + 92, 96, 12, magic):
                    repair_dependency(*(args + (b'!tpj', moff3 + 8)))
                    repair_dependency(*(args + (b'effe', moff3 + 24)))


def repair_actv(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)
    repair_dependency(*(args + (b'rtca', tag_offset + 0x4)))
    repair_dependency(*(args + (b'tinu', tag_offset + 0x14)))
    repair_dependency(*(args + (b'vtca', tag_offset + 0x24)))
    repair_dependency(*(args + (b'paew', tag_offset + 0x64)))
    repair_dependency(*(args + (b'piqe', tag_offset + 0x1C0)))


def repair_ant_(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)
    repair_dependency(*(args + (b'mtib', tag_offset + 0x20)))
    repair_dependency(*(args + (b'yhpp', tag_offset + 0x30)))


def repair_antr(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    ct, moff, _ = read_reflexive(
        map_data, index_array[tag_id].meta_offset + 0x54 - magic, 257, 20, magic)
    repair_dependency_array(index_array, map_data, magic, repair, engine,
                            b'!dns', moff, ct, 20)


def repair_coll(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine, b'effe')
    repair_dependency(*(args + (tag_offset + 0x70, )))
    repair_dependency(*(args + (tag_offset + 0x84, )))
    repair_dependency(*(args + (tag_offset + 0x98, )))
    repair_dependency(*(args + (tag_offset + 0xA8, )))
    repair_dependency(*(args + (tag_offset + 0xBC, )))
    repair_dependency(*(args + (tag_offset + 0x188, )))
    repair_dependency(*(args + (tag_offset + 0x198, )))
    repair_dependency(*(args + (tag_offset + 0x1A8, )))

    # regions
    ct, moff, _ = read_reflexive(map_data, tag_offset + 0x240 - magic, 8, 0x54, magic)
    repair_dependency_array(*(args + (moff + 0x38, ct, 0x54)))


def repair_cont(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)

    repair_dependency(*(args + (b'mtib', tag_offset + 0x30)))
    repair_dependency(*(args + (b'mtib', tag_offset + 0xD0)))

    # point states
    ct, moff, _ = read_reflexive(map_data, tag_offset + 0x138 - magic, 16, 104, magic)
    repair_dependency_array(*(args + (b'yhpp', moff + 16, ct, 104)))


def repair_deca(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    moff = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)
    repair_dependency(*(args + (b'aced', moff + 0x8)))
    repair_dependency(*(args + (b'mtib', moff + 0xD8)))


def repair_DeLa(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)
    repair_dependency(*(args + (b'mtib', tag_offset + 56)))

    # event handlers
    for moff in iter_reflexive_offs(map_data, tag_offset + 84 - magic, 72, 32, magic):
        repair_dependency(*(args + (b'aLeD', moff + 8)))
        repair_dependency(*(args + (b'!dns', moff + 24)))

    # search and replace functions
    # Not needed anymore when tags are parsed in safe-mode
    #ct, _, __ = read_reflexive(map_data, tag_offset + 96 - magic)
    #if ct > 32:
    #    # some people apparently think its cute to set this reflexive
    #    # count so high so that tool just fails to compile the tag
    #    map_data.seek(tag_offset + 96 - magic)
    #    map_data.write(b'\x20\x00\x00\x00')

    repair_dependency(*(args + (b'rtsu', tag_offset + 236)))
    repair_dependency(*(args + (b'tnof', tag_offset + 252)))
    repair_dependency(*(args + (b'mtib', tag_offset + 340)))
    repair_dependency(*(args + (b'mtib', tag_offset + 356)))
    repair_dependency(*(args + (b'aLeD', tag_offset + 420)))

    # conditional widgets
    ct, moff, _ = read_reflexive(map_data, tag_offset + 724 - magic, 32, 80, magic)
    repair_dependency_array(*(args + (b'aLeD', moff, ct, 80)))

    # child widgets
    ct, moff, _ = read_reflexive(map_data, tag_offset + 992 - magic, 32, 80, magic)
    repair_dependency_array(*(args + (b'aLeD', moff, ct, 80)))


def repair_dobc(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    repair_dependency(index_array, map_data, magic, repair, engine,
                      b'mtib', index_array[tag_id].meta_offset + 52)


def repair_effe(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)
    # events
    for moff in iter_reflexive_offs(map_data, tag_offset + 0x34 - magic, 0x44, 32, magic):
        # parts
        for moff2 in iter_reflexive_offs(map_data, moff + 0x2C - magic, 0x68, 32, magic):
            map_data.seek(moff2 - magic + 0x14)
            tag_class = map_data.read(4)
            repair_dependency(*(args + (tag_class, moff2 + 0x18)))

        # particles
        ct, moff2, _ = read_reflexive(map_data, moff + 0x38 - magic, 32, 0xE8, magic)
        repair_dependency_array(*(args + (b'trap', moff2 + 0x54, ct, 0xE8)))


def repair_elec(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    repair_dependency(index_array, map_data, magic, repair, engine,
                      b'mtib', index_array[tag_id].meta_offset + 52)

def repair_flag(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)
    repair_dependency(*(args + (b'rdhs', tag_offset + 0x18)))
    repair_dependency(*(args + (b'yhpp', tag_offset + 0x28)))
    repair_dependency(*(args + (b'rdhs', tag_offset + 0x44)))


def repair_fog(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)
    repair_dependency(*(args + (b'mtib', tag_offset + 0xBC)))
    repair_dependency(*(args + (b'dnsl', tag_offset + 0xF4)))
    repair_dependency(*(args + (b'edns', tag_offset + 0x104)))


def repair_font(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    repair_dependency_array(index_array, map_data, magic, repair, engine,
                            b'mtib', index_array[tag_id].meta_offset + 0x3C, 4)


def repair_foot(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)
    # effects
    for moff in iter_reflexive_offs(map_data, tag_offset - magic, 28, 13, magic):
        # materials
        for moff2 in iter_reflexive_offs(map_data, moff - magic, 48, MAX_MATERIAL_COUNT, magic):
            repair_dependency(*(args + (b'effe', moff2)))
            repair_dependency(*(args + (b'!dns', moff2 + 16)))


def repair_glw_(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    repair_dependency(index_array, map_data, magic, repair, engine,
                      b'mtib', index_array[tag_id].meta_offset + 324)

def repair_grhi(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)

    # grenade hud background
    repair_hud_background(*(args + (tag_offset + 36, )))

    # total grenades background
    repair_hud_background(*(args + (tag_offset + 140, )))

    repair_dependency(*(args + (b'mtib', tag_offset + 332)))

    # warning sounds
    for moff in iter_reflexive_offs(map_data, tag_offset + 360 - magic, 56, 12, magic):
        map_data.seek(moff - magic)
        if map_data.read(4) == b'dnsl':
            repair_dependency(*(args + (b'dnsl', moff)))
        else:
            repair_dependency(*(args + (b'!dns', moff)))


def repair_hud_(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    repair_dependency(index_array, map_data, magic, repair, engine,
                      b'mtib', index_array[tag_id].meta_offset)


def repair_hudg(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)
    repair_dependency(*(args + (b'tnof', tag_offset + 0x48, )))
    repair_dependency(*(args + (b'tnof', tag_offset + 0x58, )))
    repair_dependency(*(args + (b'rtsu', tag_offset + 0x94, )))
    repair_dependency(*(args + (b'mtib', tag_offset + 0xA4, )))
    repair_dependency(*(args + (b'rtsu', tag_offset + 0xB4, )))
    repair_dependency(*(args + (b' tmh', tag_offset + 0xF0, )))
    repair_dependency(*(args + (b'mtib', tag_offset + 0x150, )))
    repair_dependency(*(args + (b'ihpw', tag_offset + 0x2C0, )))
    repair_dependency(*(args + (b'mtib', tag_offset + 0x338, )))
    repair_dependency(*(args + (b'mtib', tag_offset + 0x3C8, )))
    repair_dependency(*(args + (b'!dns', tag_offset + 0x3E0, )))


def repair_itmc(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)

    # item permutations
    ct, moff, _ = read_reflexive(map_data, tag_offset - magic, 32767, 84, magic)
    repair_dependency_array(*(args + (b'meti', moff + 36, ct, 84)))


def repair_jpt_(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    repair_dependency(index_array, map_data, magic, repair, engine,
                      b'!dns', index_array[tag_id].meta_offset + 0x114)


def repair_lens(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    repair_dependency(index_array, map_data, magic, repair, engine,
                      b'mtib', index_array[tag_id].meta_offset + 0x20)


def repair_ligh(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)

    repair_dependency(*(args + (b'mtib', tag_offset + 0x64)))
    repair_dependency(*(args + (b'mtib', tag_offset + 0x7C)))
    repair_dependency(*(args + (b'snel', tag_offset + 0xAC)))


def repair_lsnd(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)
    repair_dependency(*(args + (b'gmdc', tag_offset + 0x2C)))

    # tracks
    for moff in iter_reflexive_offs(map_data, tag_offset + 0x3C - magic, 0xA0, 4, magic):
        repair_dependency(*(args + (b'!dns', moff + 0x30)))
        repair_dependency(*(args + (b'!dns', moff + 0x40)))
        repair_dependency(*(args + (b'!dns', moff + 0x50)))
        repair_dependency(*(args + (b'!dns', moff + 0x80)))
        repair_dependency(*(args + (b'!dns', moff + 0x90)))

    # detail sounds
    ct, moff, _ = read_reflexive(map_data, tag_offset + 0x48 - magic, 32, 104, magic)
    repair_dependency_array(*(args + (b'!dns', moff, ct, 104)))


def repair_matg(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)

    # sounds
    ct, moff, _ = read_reflexive(map_data, tag_offset + 0xF8 - magic, 2, 16, magic)
    repair_dependency_array(*(args + (b'!dns', moff, ct)))

    # camera
    ct, moff, _ = read_reflexive(map_data, tag_offset + 0x104 - magic, 1, 16, magic)
    repair_dependency_array(*(args + (b'kart', moff, ct)))

    # grenades
    for moff in iter_reflexive_offs(map_data, tag_offset + 0x128 - magic, 68, 4, magic):
        repair_dependency(*(args + (b'effe', moff + 4)))
        repair_dependency(*(args + (b'ihrg', moff + 20)))
        repair_dependency(*(args + (b'piqe', moff + 36)))
        repair_dependency(*(args + (b'jorp', moff + 52)))

    # rasterizer data
    for moff in iter_reflexive_offs(map_data, tag_offset + 0x134 - magic, 428, 1, magic):
        # function textures
        repair_dependency_array(*(args + (b'mtib', moff, 7)))
        moff += 7*16 + 60
        # default/experimental/video effect textures
        repair_dependency_array(*(args + (b'mtib', moff, 9)))
        moff += 9*16 + 52 + 4*11
        # pc textures
        repair_dependency(*(args + (b'mtib', moff)))

    # interface bitmaps
    for moff in iter_reflexive_offs(map_data, tag_offset + 0x140 - magic, 304, 1, magic):
        repair_dependency_array(*(args + (b'tnof', moff, 2)))
        repair_dependency_array(*(args + (b'oloc', moff + 32, 4)))
        repair_dependency(*(args + (b'gduh', moff + 96)))
        repair_dependency_array(*(args + (b'mtib', moff + 112, 3)))
        repair_dependency(*(args + (b'#rts', moff + 160)))
        repair_dependency(*(args + (b'#duh', moff + 176)))
        repair_dependency_array(*(args + (b'mtib', moff + 192, 4)))

    # weapons
    ct, moff, _ = read_reflexive(map_data, tag_offset + 0x14C - magic, 20, 16, magic)
    repair_dependency_array(*(args + (b'ejbo', moff, ct)))

    # powerups
    ct, moff, _ = read_reflexive(map_data, tag_offset + 0x158 - magic, 20, 16, magic)
    repair_dependency_array(*(args + (b'ejbo', moff, ct)))

    # multiplayer info
    for moff in iter_reflexive_offs(map_data, tag_offset + 0x164 - magic, 160, 1, magic):
        repair_dependency(*(args + (b'meti', moff)))
        repair_dependency(*(args + (b'tinu', moff + 16)))
        # vehicles
        v_ct, v_moff, _ = read_reflexive(map_data, moff + 32 - magic, 20, 16, magic)
        repair_dependency_array(*(args + (b'ejbo', v_moff, v_ct)))
        # shaders
        repair_dependency_array(*(args + (b'rdhs', moff + 44, 2)))
        repair_dependency(*(args + (b'meti', moff + 76)))
        # sounds
        s_ct, s_moff, _ = read_reflexive(map_data, moff + 92 - magic, 60, 16, magic)
        repair_dependency_array(*(args + (b'!dns', s_moff, s_ct)))

    # player info
    for moff in iter_reflexive_offs(map_data, tag_offset + 0x170 - magic, 244, 1, magic):
        repair_dependency(*(args + (b'tinu', moff)))
        repair_dependency(*(args + (b'effe', moff + 184)))

    # fp interface
    for moff in iter_reflexive_offs(map_data, tag_offset + 0x17C - magic, 192, 1, magic):
        repair_dependency(*(args + (b'2dom', moff)))
        repair_dependency(*(args + (b'mtib', moff + 16)))
        repair_dependency(*(args + (b'rtem', moff + 32)))
        repair_dependency(*(args + (b'rtem', moff + 52)))
        repair_dependency_array(*(args + (b'effe', moff + 72, 2)))

    # falling damage
    for moff in iter_reflexive_offs(map_data, tag_offset + 0x188 - magic, 152, 1, magic):
        repair_dependency(*(args + (b'!tpj', moff + 16)))
        repair_dependency_array(*(args + (b'!tpj', moff + 44, 5)))

    # materials
    for moff in iter_reflexive_offs(map_data, tag_offset + 0x194 - magic, 884, MAX_MATERIAL_COUNT, magic):
        repair_dependency(*(args + (b'effe', moff + 740)))
        repair_dependency(*(args + (b'!dns', moff + 756)))
        repair_dependency(*(args + (b'!dns', moff + 868)))
        # particle effects
        p_ct, p_moff, _ = read_reflexive(map_data, moff + 796 - magic, 8, 128, magic)
        repair_dependency_array(*(args + (b'trap', p_moff, p_ct, 128)))


def repair_mgs2(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    repair_dependency(index_array, map_data, magic, repair, engine,
                      b'mtib', index_array[tag_id].meta_offset + 92)


def repair_mode(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    # shaders
    shader_ct, shader_moff, _ = read_reflexive(
        map_data, tag_offset + 220 - magic, 256, 32, magic)

    if safe_mode:
        used_shader_indices = set()
        # loop over each geometries parts and determine which
        # shader indices are actually used across all of them
        for moff in iter_reflexive_offs(map_data, tag_offset + 208 - magic, 48):
            for moff2 in iter_reflexive_offs(map_data, moff + 36 - magic, 132):
                map_data.seek(moff2 + 4 - magic)
                shader_type = int.from_bytes(
                    map_data.read(2), 'little', signed=True)
                if shader_type in range(shader_ct):
                    used_shader_indices.add(shader_type)
    else:
        used_shader_indices = list(range(shader_ct))

    for i in sorted(used_shader_indices):
        repair_dependency(index_array, map_data, magic, repair, engine,
                          b'rdhs', shader_moff + 32 * i)


def repair_mply(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)

    # scenario descriptions
    for moff in iter_reflexive_offs(map_data, tag_offset - magic, 68, 32, magic):
        repair_dependency(*(args + (b'mtib', moff)))
        repair_dependency(*(args + (b'rtsu', moff + 16)))


def repair_ngpr(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)

    repair_dependency(*(args + (b'mtib', tag_offset + 56)))
    repair_dependency(*(args + (b'mtib', tag_offset + 76)))


def repair_predicted_resources(map_data, offset, magic, repair, max_count=0xFFffFFff):
    for moff in iter_reflexive_offs(map_data, offset - magic, 8, max_count, magic):
        map_data.seek(moff - magic)
        rsrc_type = map_data.read(4)[:2]
        tag_id = int.from_bytes(map_data.read(4), "little") & 0xFFFF

        if tag_id == 0xFFFF:
            continue
        elif rsrc_type == b'\x00\x00':
            # bitmap resource type
            repair[tag_id] = 'bitm'
        elif rsrc_type == b'\x01\x00':
            # sound resource type
            repair[tag_id] = 'snd!'


def repair_object(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    map_data.seek(tag_offset - magic)
    object_type = int.from_bytes(map_data.read(2), 'little')
    if object_type != -1 and object_type not in range(len(object_class_bytes) - 1):
        # not an object
        return

    # obje_attrs struct size is 380
    args = (index_array, map_data, magic, repair, engine)
    repair_dependency(*(args + (b'2dom', tag_offset + 40)))
    repair_dependency(*(args + (b'rtna', tag_offset + 56)))

    repair_dependency(*(args + (b'lloc', tag_offset + 112)))
    repair_dependency(*(args + (b'syhp', tag_offset + 128)))
    repair_dependency(*(args + (b'rdhs', tag_offset + 144)))
    repair_dependency(*(args + (b'effe', tag_offset + 160)))

    # attachments
    ct, moff, _ = read_reflexive(map_data, tag_offset + 320 - magic, 8, 72, magic)
    repair_dependency_array(*(args + (None, moff, ct, 72)))

    # widgets
    ct, moff, _ = read_reflexive(map_data, tag_offset + 332 - magic, 4, 32, magic)
    repair_dependency_array(*(args + (None, moff, ct, 32)))

    # add the predicted resources to the tags to repair
    repair_predicted_resources(map_data, tag_offset + 368, magic, repair, 1024)

    tag_offset += 380
    args2 = (index_array, map_data, magic, repair, engine)
    if object_type <= 1:
        # bipd or vehi
        repair_unit_attrs(tag_offset, *args2)
        tag_offset += 372
        if object_type == 0:
            # bipd
            repair_dependency(*(args + (b'!tpj', tag_offset + 36)))
            repair_dependency(*(args + (b'toof', tag_offset + 156)))
        else:
            # vehi
            repair_dependency(*(args + (b'!dns', tag_offset + 192)))
            repair_dependency(*(args + (b'!dns', tag_offset + 208)))
            repair_dependency(*(args + (b'toof', tag_offset + 224)))
            repair_dependency(*(args + (b'effe', tag_offset + 240)))

    elif object_type <= 4:
        # weap, eqip, or garb
        repair_item_attrs(tag_offset, *args2)
        tag_offset += 396
        if object_type == 2:
            # weap
            repair_dependency(*(args + (None, tag_offset + 52)))
            repair_dependency(*(args + (None, tag_offset + 108)))
            repair_dependency(*(args + (None, tag_offset + 124)))
            repair_dependency(*(args + (b'!tpj', tag_offset + 140)))
            repair_dependency(*(args + (b'!tpj', tag_offset + 156)))
            repair_dependency(*(args + (b'vtca', tag_offset + 180)))
            repair_dependency(*(args + (None, tag_offset + 280)))
            repair_dependency(*(args + (None, tag_offset + 296)))
            repair_dependency(*(args + (b'2dom', tag_offset + 340)))
            repair_dependency(*(args + (b'rtna', tag_offset + 356)))
            repair_dependency(*(args + (b'ihpw', tag_offset + 376)))
            repair_dependency(*(args + (b'!dns', tag_offset + 392)))
            repair_dependency(*(args + (b'!dns', tag_offset + 408)))
            repair_dependency(*(args + (b'!dns', tag_offset + 424)))

            repair_predicted_resources(
                map_data, tag_offset + 476, magic, repair, 1024)

            # magazines
            for moff in iter_reflexive_offs(
                    map_data, tag_offset + 488 - magic, 112, 2, magic):
                repair_dependency(*(args + (None, moff + 56)))
                repair_dependency(*(args + (None, moff + 72)))

                # magazine items
                ct, moff2, _ = read_reflexive(map_data, moff + 100 - magic, 2, 28, magic)
                repair_dependency_array(*(args + (b'piqe', moff2 + 12, ct, 28)))

            # triggers
            for moff in iter_reflexive_offs(
                    map_data, tag_offset + 500 - magic, 276, 2, magic):
                repair_dependency(*(args + (None, moff + 92)))
                repair_dependency(*(args + (b'ejbo', moff + 148)))

                # firing effects
                for moff2 in iter_reflexive_offs(
                        map_data, moff + 264 - magic, 132, 8, magic):
                    repair_dependency(*(args + (None, moff2 + 36)))
                    repair_dependency(*(args + (None, moff2 + 52)))
                    repair_dependency(*(args + (None, moff2 + 68)))
                    repair_dependency(*(args + (b'!tpj', moff2 + 84)))
                    repair_dependency(*(args + (b'!tpj', moff2 + 100)))
                    repair_dependency(*(args + (b'!tpj', moff2 + 116)))

        elif object_type == 3:
            # eqip
            repair_dependency(*(args + (b'!dns', tag_offset + 8)))
        else:
            # garb
            pass  # nothing else to do for this

    elif object_type == 5:
        # proj
        repair_dependency(*(args + (b'effe', tag_offset + 16)))
        repair_dependency(*(args + (b'effe', tag_offset + 48)))
        repair_dependency(*(args + (b'effe', tag_offset + 120)))
        repair_dependency(*(args + (b'!dns', tag_offset + 136)))
        repair_dependency(*(args + (b'!tpj', tag_offset + 152)))
        repair_dependency(*(args + (b'!tpj', tag_offset + 168)))

        # material responses
        for moff in iter_reflexive_offs(
                map_data, tag_offset + 196 - magic, 160, MAX_MATERIAL_COUNT, magic):
            repair_dependency(*(args + (b'effe', moff + 4)))
            repair_dependency(*(args + (b'effe', moff + 60)))
            repair_dependency(*(args + (b'effe', moff + 104)))
    elif object_type == 6:
        # scen
        pass  # nothing else to do for this

    elif object_type <= 9:
        # mach, ctrl, or lifi
        repair_devi_attrs(tag_offset, *args2)
        tag_offset += 276
        if object_type == 8:
            # ctrl
            repair_dependency(*(args + (None, tag_offset + 88)))
            repair_dependency(*(args + (None, tag_offset + 104)))
            repair_dependency(*(args + (None, tag_offset + 120)))
        else:
            # mach, lifi
            pass  # nothing else to do for these

    else:
        # plac, or ssce
        pass  # nothing else to do for these


def repair_part(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)

    repair_dependency(*(args + (b'mtib', tag_offset + 0x4)))
    repair_dependency(*(args + (b'yhpp', tag_offset + 0x14)))
    repair_dependency(*(args + (b'toof', tag_offset + 0x24)))
    repair_dependency(*(args + (None, tag_offset + 0x48)))
    repair_dependency(*(args + (None, tag_offset + 0x58)))
    repair_dependency(*(args + (b'mtib', tag_offset + 0xFC)))


def repair_pctl(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)
    repair_dependency(*(args + (b'yhpp', tag_offset + 56)))

    # particle types
    for moff in iter_reflexive_offs(map_data, tag_offset + 92 - magic, 128, 4, magic):
        # particle states
        for moff2 in iter_reflexive_offs(map_data, moff + 116 - magic, 376, 8, magic):
            repair_dependency(*(args + (b'mtib', moff2 + 48)))
            repair_dependency(*(args + (b'yhpp', moff2 + 132)))
            repair_dependency(*(args + (b'mtib', moff2 + 260)))


def repair_rain(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)

    # particle types
    for moff in iter_reflexive_offs(map_data, tag_offset + 0x24 - magic, 0x25C, 8, magic):
        repair_dependency(*(args + (b'yhpp', moff + 0xAC)))
        repair_dependency(*(args + (b'mtib', moff + 0x194)))
        repair_dependency(*(args + (b'mtib', moff + 0x1F4)))


def repair_sbsp(tag_offset, index_array, map_data, magic, repair, engine,
                map_magic, safe_mode=True):
    # This function requires the first argument is the tag's magic offset
    # relative to the bsp magic, rather than the tag's index id
    args = (index_array, map_data, magic, repair, engine)
    kwargs = dict(map_magic=map_magic)
    repair_dependency(*(args + (b'mtib', tag_offset)), **kwargs)

    # collision materials
    ct, moff, _ = read_reflexive(map_data, tag_offset + 164 - magic, 512, 20, magic)
    repair_dependency_array(*(args + (b'rdhs', moff, ct, 20)), **kwargs)

    # lightmaps
    for moff in iter_reflexive_offs(map_data, tag_offset + 260 - magic, 32, 128, magic):
        ct, moff2, _ = read_reflexive(map_data, moff + 20 - magic, 2048, 256, magic)
        # materials
        repair_dependency_array(*(args + (b'rdhs', moff2, ct, 256)), **kwargs)

    # lens flares
    ct, moff, _ = read_reflexive(map_data, tag_offset + 284 - magic, 256, 16, magic)
    repair_dependency_array(*(args + (b'snel', moff, ct)), **kwargs)

    # fog palettes
    ct, moff, _ = read_reflexive(map_data, tag_offset + 400 - magic, 32, 136, magic)
    repair_dependency_array(*(args + (b' gof', moff + 32, ct, 136)), **kwargs)

    # weather palettes
    for moff in iter_reflexive_offs(map_data, tag_offset + 436 - magic, 240, 32, magic):
        repair_dependency(*(args + (b'niar', moff + 32)), **kwargs)
        repair_dependency(*(args + (b'dniw', moff + 128)), **kwargs)

    # background sounds palette
    ct, moff, _ = read_reflexive(map_data, tag_offset + 508 - magic, 64, 116, magic)
    repair_dependency_array(*(args + (b'dnsl', moff + 32, ct, 116)), **kwargs)

    # sound environments palette
    ct, moff, _ = read_reflexive(map_data, tag_offset + 520 - magic, 64, 80, magic)
    repair_dependency_array(*(args + (b'edns', moff + 32, ct, 80)), **kwargs)


def repair_scnr(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    ### Need to finish this up. not all the limits specified here
    # should be as low as they are because open sauce is a thing
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)

    if "yelo" in engine:
        repair_dependency(*(args + (b'oley', tag_offset)))

        # bsp modifiers
        for moff in iter_reflexive_offs(
                map_data, tag_offset + 1288 - magic, 64, 32, magic):
            # lightmap sets
            for moff2 in iter_reflexive_offs(map_data, moff + 4 - magic,
                                             124, 64, magic):
                repair_dependency_array(*(args + (b'mtib', moff2 + 36, 4)))

            # sky set
            for moff2 in iter_reflexive_offs(map_data, moff + 16 - magic, 44, 64, magic):
                # skies
                for moff3 in iter_reflexive_offs(map_data, moff2 + 32 - magic, 20, 8, magic):
                    repair_dependency(*(args + (b' yks', moff3 + 4)))

    repair_dependency(*(args + (b'rtsu', tag_offset + 1396)))
    repair_dependency(*(args + (b'rtsu', tag_offset + 1412)))
    repair_dependency(*(args + (b' tmh', tag_offset + 1428)))

    # skies
    ct, moff, _ = read_reflexive(map_data, tag_offset + 48 - magic, 8, 16, magic)
    repair_dependency_array(*(args + (b' yks', moff, ct)))

    # player starting profiles
    for moff in iter_reflexive_offs(map_data, tag_offset + 840 - magic, 104, 256, magic):
        repair_dependency(*(args + (b'paew', moff + 40)))
        repair_dependency(*(args + (b'paew', moff + 60)))

    # netgame flags
    ct, moff, _ = read_reflexive(map_data, tag_offset + 888 - magic, 200, 148, magic)
    repair_dependency_array(*(args + (b'cmti', moff + 20, ct, 148)))

    # netgame equipments
    ct, moff, _ = read_reflexive(map_data, tag_offset + 900 - magic, 200, 144, magic)
    repair_dependency_array(*(args + (b'cmti', moff + 80, ct, 144)))

    # starting equipment
    for moff in iter_reflexive_offs(map_data, tag_offset + 912 - magic, 204, 200, magic):
        repair_dependency(*(args + (b'cmti', moff + 60)))
        repair_dependency(*(args + (b'cmti', moff + 76)))
        repair_dependency(*(args + (b'cmti', moff + 92)))
        repair_dependency(*(args + (b'cmti', moff + 108)))
        repair_dependency(*(args + (b'cmti', moff + 124)))
        repair_dependency(*(args + (b'cmti', moff + 140)))

    # ai animation reference
    ct, moff, _ = read_reflexive(map_data, tag_offset + 1092 - magic, 128, 60, magic)
    repair_dependency_array(*(args + (b'rtna', moff + 32, ct, 60)))

    # ai conversations
    for moff in iter_reflexive_offs(map_data, tag_offset + 1128 - magic, 116, 128, magic):
        # lines
        for moff2 in iter_reflexive_offs(map_data, moff + 92 - magic, 124, 32, magic):
            repair_dependency(*(args + (b'!dns', moff2 + 28)))
            repair_dependency(*(args + (b'!dns', moff2 + 44)))
            repair_dependency(*(args + (b'!dns', moff2 + 60)))
            repair_dependency(*(args + (b'!dns', moff2 + 76)))
            repair_dependency(*(args + (b'!dns', moff2 + 92)))
            repair_dependency(*(args + (b'!dns', moff2 + 108)))

    # tag references
    ct, moff, _ = read_reflexive(map_data, tag_offset + 1204 - magic, 256, 40, magic)
    repair_dependency_array(*(args + (None, moff + 24, ct, 40)))

    # structure bsps
    ct, moff, _ = read_reflexive(map_data, tag_offset + 1444 - magic, 32, 32, magic)
    repair_dependency_array(*(args + (b'psbs', moff + 16, ct, 32)))

    # palettes
    # NOTE: Can't trust that these palettes are valid.
    # Need to check what the highest one used by all instances
    for off, inst_size in (
            (540, 72), (564, 120), (588, 120), # scen  bipd  vehi
            (612, 40), (636, 92), (672, 64),   # eqip  weap  mach
            (696, 64), (720, 88), (744, 40)):  # ctrl  lifi  ssce
        pal_ct, pal_moff, _ = read_reflexive(map_data, tag_offset + off - magic)

        if safe_mode:
            used_pal_indices = set()
            # loop over each object instance and determine which
            # palette indices are actually used across all of them
            for moff in iter_reflexive_offs(
                    map_data, tag_offset + off - 12 - magic, inst_size, tag_magic=magic):
                map_data.seek(moff - magic)
                inst_type = int.from_bytes(map_data.read(2), 'little', signed=True)
                if inst_type in range(pal_ct):
                    used_pal_indices.add(inst_type)
        else:
            used_pal_indices = list(range(pal_ct))

        for i in sorted(used_pal_indices):
            repair_dependency(*(args + (b'ejbo', pal_moff + 48 * i)))

    # script syntax data references
    size, _, __, moff, ___ = read_rawdata_ref(map_data, tag_offset + 1140 - magic, magic)
    map_data.seek(moff - magic)
    script_syntax_data_nodes = get_hsc_data_block(map_data.read(size)).nodes
    for node in script_syntax_data_nodes:
        tag_cls = {
            24: 'snd!', 25: 'effe', 26: 'jpt!', 27: 'lsnd',
            28: 'antr', 29: 'actv', 30: 'jpt!', 31: 'obje'
            }.get(node.type)
        if tag_cls is None or (node.flags & HSC_IS_SCRIPT_OR_GLOBAL):
            continue

        sub_tag_id = node.data & 0xFFff
        if sub_tag_id in repair or sub_tag_id not in range(len(index_array)):
            continue

        if tag_cls == "obje":
            try:
                map_data.seek(index_array[sub_tag_id].meta_offset - magic)
                object_type = int.from_bytes(map_data.read(2), 'little')
                if object_type not in range(-1, len(object_class_bytes) - 1):
                    continue
            except Exception:
                continue

            tag_cls = object_class_bytes[object_type]

        repair[sub_tag_id] = tag_cls


    # decals
    ct, moff, _ = read_reflexive(map_data, tag_offset + 948 - magic, 128, 16, magic)
    repair_dependency_array(*(args + (b'aced', moff, ct)))

    # detail objects
    ct, moff, _ = read_reflexive(map_data, tag_offset + 960 - magic, 32, 48, magic)
    repair_dependency_array(*(args + (b'cbod', moff, ct, 48)))

    # actors palette
    ct, moff, _ = read_reflexive(map_data, tag_offset + 1056 - magic, 64, 16, magic)
    repair_dependency_array(*(args + (b'vtca', moff, ct)))


def repair_shader(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    map_data.seek(tag_offset + 36 - magic)
    shader_type = int.from_bytes(map_data.read(2), 'little')

    if shader_type != -1 and shader_type not in range(len(shader_class_bytes) - 1):
        # not a shader
        return

    typ = shader_class_bytes[shader_type]

    tag_offset += 40
    args = (index_array, map_data, magic, repair, engine)

    if typ == b'vnes':
        repair_dependency(*(args + (b'snel', tag_offset + 0x8)))
        repair_dependency(*(args + (b'mtib', tag_offset + 0x60)))
        repair_dependency(*(args + (b'mtib', tag_offset + 0x90)))
        repair_dependency(*(args + (b'mtib', tag_offset + 0xA4)))
        repair_dependency(*(args + (b'mtib', tag_offset + 0xD4)))
        repair_dependency(*(args + (b'mtib', tag_offset + 0x100)))
        repair_dependency(*(args + (b'mtib', tag_offset + 0x22C)))
        repair_dependency(*(args + (b'mtib', tag_offset + 0x2FC)))
        # shader environment os extension
        if "yelo" in engine:
            ct, moff, _ = read_reflexive(map_data, tag_offset + 0xC8 - magic, 1, 100, magic)
            repair_dependency_array(*(args + (b'mtib', moff + 8, ct, 100)))

    elif typ == b'osos':
        repair_dependency(*(args + (b'mtib', tag_offset + 0x7C)))
        repair_dependency(*(args + (b'mtib', tag_offset + 0x94)))
        repair_dependency(*(args + (b'mtib', tag_offset + 0xB4)))
        repair_dependency(*(args + (b'mtib', tag_offset + 0x13C)))
        # shader model os extension
        if "yelo" in engine:
            for moff in iter_reflexive_offs(
                    map_data, tag_offset + 0xC8 - magic, 192, 1, magic):
                repair_dependency(*(args + (b'mtib', moff)))
                repair_dependency(*(args + (b'mtib', moff + 0x20)))
                repair_dependency(*(args + (b'mtib', moff + 0x40)))
                repair_dependency(*(args + (b'mtib', moff + 0x60)))

    elif typ == b'tems':
        repair_dependency(*(args + (b'mtib', tag_offset + 0x24)))

    elif typ == b'algs':
        repair_dependency(*(args + (b'mtib', tag_offset + 0x3C)))
        repair_dependency(*(args + (b'mtib', tag_offset + 0x84)))
        repair_dependency(*(args + (b'mtib', tag_offset + 0x98)))
        repair_dependency(*(args + (b'mtib', tag_offset + 0x130)))
        repair_dependency(*(args + (b'mtib', tag_offset + 0x144)))
        repair_dependency(*(args + (b'mtib', tag_offset + 0x178)))
        repair_dependency(*(args + (b'mtib', tag_offset + 0x18C)))

    elif typ == b'alps':
        repair_dependency(*(args + (b'mtib', tag_offset + 0xAC)))
        repair_dependency(*(args + (b'mtib', tag_offset + 0xF4)))

    elif typ == b'taws':
        repair_dependency(*(args + (b'mtib', tag_offset + 0x24)))
        repair_dependency(*(args + (b'mtib', tag_offset + 0x74)))
        repair_dependency(*(args + (b'mtib', tag_offset + 0xA0)))

    elif typ in b'rtos_ihcs_xecs':
        repair_dependency(*(args + (b'snel', tag_offset + 0x10)))
        # layers
        ct, moff, _ = read_reflexive(map_data, tag_offset + 0x20 - magic, 4, 16, magic)
        repair_dependency_array(*(args + (b'rdhs', moff, ct)))
        # maps
        maps_size = 0x64 if typ == b'rtos' else 0xDC

        ct, moff, _ = read_reflexive(map_data, tag_offset + 0x2C - magic, 4, maps_size, magic)

        moff += 0x1C if typ == b'rtos' else 0x6C

        repair_dependency_array(*(args + (b'mtib', moff, ct, maps_size)))

        if typ == b'xecs':
            # 2 stage maps
            ct, moff, _ = read_reflexive(map_data, tag_offset + 0x38 - magic, 2, 0xDC, magic)
            repair_dependency_array(*(args + (b'mtib', moff + 0x6C, ct, 0xDC)))


def repair_sky(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)

    repair_dependency(*(args + (b'2dom', tag_offset)))
    repair_dependency(*(args + (b'rtna', tag_offset + 0x10)))
    repair_dependency(*(args + (b' gof', tag_offset + 0x98)))
    # lights
    ct, moff, _ = read_reflexive(map_data, tag_offset + 0xC4 - magic, 8, 116, magic)
    repair_dependency_array(*(args + (b'snel', moff, ct, 116)))


def repair_snd_(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    repair_dependency(index_array, map_data, magic, repair, engine,
                      b'!dns', index_array[tag_id].meta_offset + 0x70)


def repair_Soul(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    repair_tagc(tag_id, index_array, map_data, magic, repair, engine, safe_mode, b'aLeD', 32)


def repair_tagc(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True,
                tag_cls=None, max_count=200):
    ct, moff, _ = read_reflexive(
        map_data, index_array[tag_id].meta_offset - magic, max_count, 16, magic)

    for moff2 in range(moff, moff + (ct * 16), 16):
        map_data.seek(moff2 + 12 - magic)
        tag_id = int.from_bytes(map_data.read(4), "little")
        if tag_id == 0xFFffFFff:
            continue
        elif ((tag_id & 0xFFff) not in range(len(index_array)) or
              index_array[tag_id & 0xFFff].id != tag_id):
            # break on the first invalid tag id.
            # the reflexive size might be corrupt
            break

        repair_dependency(index_array, map_data, magic, repair, engine,
                          tag_cls, moff2)


def repair_udlg(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine, b'!dns')
    repair_dependency_array(*(args + (tag_offset + 0x10, 3)))
    repair_dependency_array(*(args + (tag_offset + 0x70, 14)))
    repair_dependency_array(*(args + (tag_offset + 0x160, 4)))
    repair_dependency_array(*(args + (tag_offset + 0x1E0, 17)))
    repair_dependency_array(*(args + (tag_offset + 0x320, 28)))
    repair_dependency_array(*(args + (tag_offset + 0x510, 13)))
    repair_dependency_array(*(args + (tag_offset + 0x610, 10)))
    repair_dependency_array(*(args + (tag_offset + 0x6D0, 13)))
    repair_dependency_array(*(args + (tag_offset + 0x7C0, 21)))
    repair_dependency_array(*(args + (tag_offset + 0x950, 23)))
    repair_dependency_array(*(args + (tag_offset + 0xB20, 7)))
    repair_dependency_array(*(args + (tag_offset + 0xBD0, 5)))
    repair_dependency_array(*(args + (tag_offset + 0xC60, 8)))


def repair_unhi(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)

    # unit hud background
    repair_hud_background(*(args + (tag_offset + 36, )))
    # shield panel background
    repair_hud_background(*(args + (tag_offset + 140, )))
    # shield panel meter
    repair_dependency(*(args + (b'mtib', tag_offset + 280)))
    # health panel background
    repair_hud_background(*(args + (tag_offset + 380, )))
    # health panel meter
    repair_dependency(*(args + (b'mtib', tag_offset + 520)))
    # motion sensor panel background
    repair_hud_background(*(args + (tag_offset + 620, )))
    # motion sensor panel foreground
    repair_hud_background(*(args + (tag_offset + 724, )))

    # auxilary overlay
    for moff in iter_reflexive_offs(map_data, tag_offset + 932 - magic, 132, 16, magic):
        repair_hud_background(*(args + (moff, )))

    # warning sounds
    for moff in iter_reflexive_offs(map_data, tag_offset + 960 - magic, 56, 12, magic):
        map_data.seek(moff - magic)
        if map_data.read(4) == b'dnsl':
            repair_dependency(*(args + (b'dnsl', moff)))
        else:
            repair_dependency(*(args + (b'!dns', moff)))

    # auxilary meter
    for moff in iter_reflexive_offs(map_data, tag_offset + 972 - magic, 324, 16, magic):
        repair_hud_background(*(args + (moff + 20, )))
        repair_dependency(*(args + (b'mtib', moff + 160)))


def repair_vcky(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)
    repair_dependency(*(args + (b'tnof', tag_offset)))
    repair_dependency(*(args + (b'mtib', tag_offset + 16)))
    repair_dependency(*(args + (b'rtsu', tag_offset + 32)))
    # virtual keys
    for moff in iter_reflexive_offs(map_data, tag_offset + 48 - magic, 80, 44, magic):
        repair_dependency_array(*(args + (b'mtib', moff + 16, 4)))


def repair_wphi(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)

    repair_dependency(*(args + (b'ihpw', tag_offset)))

    # static elements
    for moff in iter_reflexive_offs(map_data, tag_offset + 96 - magic, 180, 16, magic):
        repair_dependency(*(args + (b'mtib', moff + 72)))
        # multitex overlays
        for moff2 in iter_reflexive_offs(map_data, moff + 124 - magic, 480, 30, magic):
            repair_dependency(*(args + (b'mtib', moff2 + 100)))
            repair_dependency(*(args + (b'mtib', moff2 + 116)))
            repair_dependency(*(args + (b'mtib', moff2 + 132)))

    # meter elements
    for moff in iter_reflexive_offs(map_data, tag_offset + 108 - magic, 180, 16, magic):
        repair_dependency(*(args + (b'mtib', moff + 72)))

    # crosshairs
    for moff in iter_reflexive_offs(map_data, tag_offset + 132 - magic, 104, 19, magic):
        repair_dependency(*(args + (b'mtib', moff + 36)))

    # overlay elements
    for moff in iter_reflexive_offs(map_data, tag_offset + 144 - magic, 104, 16, magic):
        repair_dependency(*(args + (b'mtib', moff + 36)))

    # screen effects
    for moff in iter_reflexive_offs(map_data, tag_offset + 172 - magic, 184, 1, magic):
        repair_dependency(*(args + (b'mtib', moff + 24)))
        repair_dependency(*(args + (b'mtib', moff + 40)))


# open-sauce repair functions
def repair_avtc(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)

    # actor variant transforms
    for moff in iter_reflexive_offs(map_data, tag_offset - magic, 52, 32, magic):
        repair_dependency(*(args + (b'vtca', moff)))

        # transforms
        for moff2 in iter_reflexive_offs(map_data, moff + 16 - magic, 116, 32, magic):
            repair_dependency(*(args + (b'otva', moff2 + 52)))
            repair_dependency(*(args + (b'itva', moff2 + 72)))


def repair_avti(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)
    # targets
    for moff in iter_reflexive_offs(map_data, tag_offset - magic, 172, 16, magic):
        repair_dependency(*(args + (b'vtca', moff + 52)))

        # keyframe actions
        for moff2 in iter_reflexive_offs(map_data, moff + 120 - magic, 72, 9, magic):
            repair_dependency(*(args + (b'!tpj', moff2 + 8)))
            repair_dependency(*(args + (b'effe', moff2 + 24)))


def repair_avto(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset - magic
    args = (index_array, map_data, magic, repair, engine)

    # instigators
    for moff in iter_reflexive_offs(map_data, tag_offset + 44, 32, 16, magic):
        repair_dependency(*(args + (b'tinu', moff)))

    # keyframe actions
    for moff in iter_reflexive_offs(map_data, tag_offset + 88, 72, 9, magic):
        repair_dependency(*(args + (b'!tpj', moff + 8)))
        repair_dependency(*(args + (b'effe', moff + 24)))

    # attachments
    for moff in iter_reflexive_offs(map_data, tag_offset + 104, 120, 16, magic):
        repair_dependency(*(args + (b'ejbo', moff)))


def repair_efpc(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    # effects
    ct, moff, _ = read_reflexive(
        map_data, index_array[tag_id].meta_offset + 24 - magic, 32, 72, magic)
    repair_dependency_array(
        index_array, map_data, magic, repair, engine, b'gpfe', moff, ct, 72)


def repair_efpg(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    # shaders
    ct, moff, _ = read_reflexive(
        map_data, index_array[tag_id].meta_offset + 60 - magic, 12, 16, magic)
    repair_dependency_array(
        index_array, map_data, magic, repair, engine, b'gphs', moff, ct)


def repair_gelc(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)

    # unit infections
    for moff in iter_reflexive_offs(map_data, tag_offset + 4 - magic, 52, 1, magic):
        ct, moff2, _ = read_reflexive(map_data, moff + 4 - magic, 16, magic)
        repair_dependency_array(*(args + (b'tinu', moff2, ct)))

        # boarding seats
        for moff2 in iter_reflexive_offs(map_data, moff + 16 - magic, 144, 32, magic):
            repair_dependency(*(args + (b'tinu', moff2 + 4)))
            repair_dependency(*(args + (b'tinu', moff2 + 24)))
            repair_dependency(*(args + (b'vtca', moff2 + 40)))
            repair_dependency(*(args + (b'effe', moff2 + 56)))
            repair_dependency(*(args + (b'ejbo', moff2 + 72)))

    # unit external upgrades
    for moff in iter_reflexive_offs(map_data, tag_offset + 16 - magic, 68, 64, magic):
        repair_dependency(*(args + (b'tinu', moff + 4)))

        ct, moff2, _ = read_reflexive(map_data, moff + 20 - magic, 120, magic)
        repair_dependency_array(*(args + (b'!tpj', moff2 + 72, ct, 120)))


def repair_gelo(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)

    repair_dependency(*(args + (b'cgat', tag_offset + 40)))
    repair_dependency(*(args + (b'cleg', tag_offset + 56)))

    # scripted ui widgets
    ct, moff, _ = read_reflexive(map_data, tag_offset + 152 - magic, 128, 76, magic)
    repair_dependency_array(*(args + (b'aLeD', moff + 32, ct, 76)))


def repair_magy(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    repair_antr(tag_id, index_array, map_data, magic, repair, engine)
    repair_dependency(index_array, map_data, magic, repair, engine,
                      b'rtna', index_array[tag_id].meta_offset + 0x80)


def repair_shpg(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    repair_shpp(tag_id, index_array, map_data, magic, repair, engine)

    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)
    repair_dependency(*(args + (b'gphs', tag_offset + 168)))

    # merged values
    for moff in iter_reflexive_offs(map_data, tag_offset + 184 - magic, 116, 16*8, magic):
        repair_dependency(*(args + (b'mtib', moff + 88)))


def repair_shpp(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    repair_predicted_resources(
        map_data, index_array[tag_id].meta_offset + 120, magic, repair, 1024)


def repair_unic(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    ct, moff, _ = read_reflexive(
        map_data, index_array[tag_id].meta_offset - magic, 9216, 56, magic)
    repair_dependency_array(index_array, map_data, magic, repair, engine,
                            b'ydis', moff, ct, 56)


def repair_yelo(tag_id, index_array, map_data, magic, repair, engine, safe_mode=True):
    tag_offset = index_array[tag_id].meta_offset
    args = (index_array, map_data, magic, repair, engine)

    repair_dependency(*(args + (b'oleg', tag_offset + 4)))
    repair_dependency(*(args + (b'gtam', tag_offset + 20)))
    repair_dependency(*(args + (b'cgat', tag_offset + 36)))

    # scripted ui widgets
    ct, moff, _ = read_reflexive(map_data, tag_offset + 104 - magic, 128, 76, magic)
    repair_dependency_array(*(args + (b'aLeD', moff + 32, ct, 76)))


class_repair_functions = {
    "actv": repair_actv, "ant!": repair_ant_, "antr": repair_antr,
    "coll": repair_coll, "cont": repair_cont, "deca": repair_deca,
    "DeLa": repair_DeLa, "dobc": repair_dobc, "effe": repair_effe,
    "elec": repair_elec, "flag": repair_flag, "fog ": repair_fog,
    "font": repair_font, "foot": repair_foot, "glw!": repair_glw_,
    "grhi": repair_grhi, "hud#": repair_hud_, "hudg": repair_hudg,
    "itmc": repair_itmc, "jpt!": repair_jpt_, "lens": repair_lens,
    "ligh": repair_ligh, "lsnd": repair_lsnd, "matg": repair_matg,
    "mgs2": repair_mgs2, "mode": repair_mode, "mod2": repair_mode,
    "mply": repair_mply, "ngpr": repair_ngpr, "part": repair_part,
    "pctl": repair_pctl, "rain": repair_rain, "sbsp": repair_sbsp,
    "scnr": repair_scnr, "sky ": repair_sky,  "snd!": repair_snd_,
    "Soul": repair_Soul, "tagc": repair_tagc, "udlg": repair_udlg,
    "unhi": repair_unhi, "vcky": repair_vcky, "wphi": repair_wphi,

    # open sauce
    "avtc": repair_avtc, "avti": repair_avti, "avto": repair_avto,
    "efpc": repair_efpc, "efpg": repair_efpg, "gelc": repair_gelc,
    "gelo": repair_gelo, "magy": repair_magy, "shpg": repair_shpg,
    "shpp": repair_shpp, "unic": repair_unic, "yelo": repair_yelo
    }

# object subclasses
for name in ("bipd", "vehi", "weap", "eqip", "garb", "proj", "scen",
             "mach", "ctrl", "lifi", "plac", "ssce", "obje"):
    class_repair_functions[name] = repair_object

# shader subclasses
for name in ("senv", "soso", "sotr", "schi", "scex", "swat", "sgla",
             "smet", "spla", "shdr"):
    class_repair_functions[name] = repair_shader

# make a copy of the class_repair_functions, but have the
# functions indexed by the reversed fcc string as bytes
_class_repair_functions_by_bytes = {
    bytes(k[slice(None, None, -1)], "latin1"): class_repair_functions[k]
    for k in class_repair_functions}
