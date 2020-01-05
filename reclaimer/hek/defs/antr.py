#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

from ...common_descs import *
from .objs.antr import AntrTag
from supyr_struct.defs.tag_def import TagDef

frame_info_dxdy_node = QStruct("frame_info_node",
    Float("dx"),
    Float("dy"), ORIENT='h'
    )

frame_info_dxdydyaw_node = QStruct("frame_info_node",
    Float("dx"),
    Float("dy"),
    Float("dyaw"), ORIENT='h'
    )

frame_info_dxdydzdyaw_node = QStruct("frame_info_node",
    Float("dx"),
    Float("dy"),
    Float("dz"),
    Float("dyaw"), ORIENT='h'
    )

default_node = Struct("default_node",
    # each of these structs exists ONLY if the corrosponding flag
    # for that node it NOT set in the animation it is located in.
    QStruct("rotation",
        SInt16("i", UNIT_SCALE=1/32767),
        SInt16("j", UNIT_SCALE=1/32767),
        SInt16("k", UNIT_SCALE=1/32767),
        SInt16("w", UNIT_SCALE=1/32767),
        ORIENT="h"
        ),
    QStruct("translation", INCLUDE=xyz_float),
    Float("scale"),
    SIZE=24
    )


dyn_anim_path = "tagdata.animations.STEPTREE[DYN_I].name"

object_desc = Struct("object",
    dyn_senum16("animation", DYN_NAME_PATH=dyn_anim_path),
    SEnum16("function",
        "A_out",
        "B_out",
        "C_out",
        "D_out"
        ),
    SEnum16("function_controls",
        "frame",
        "scale",
        ),
    SIZE=20,
    )

anim_enum_desc = QStruct("animation",
    dyn_senum16("animation", DYN_NAME_PATH=dyn_anim_path)
    )

ik_point_desc = Struct("ik_point",
    ascii_str32("marker"),
    ascii_str32("attach_to_marker"),
    SIZE=64,
    )

weapon_types_desc = Struct("weapon_types",
    ascii_str32("label"),
    Pad(16),
    reflexive("animations", anim_enum_desc, 10,
        *unit_weapon_type_animation_names
        ),
    SIZE=60,
    )

unit_weapon_desc = Struct("weapon",
    ascii_str32("name"),
    ascii_str32("grip_marker"),
    ascii_str32("hand_marker"),
    #Aiming screen bounds

    #pitch and yaw are saved in radians.
    float_rad("right_yaw_per_frame"),
    float_rad("left_yaw_per_frame"),
    SInt16("right_frame_count"),
    SInt16("left_frame_count"),

    float_rad("down_pitch_per_frame"),
    float_rad("up_pitch_per_frame"),
    SInt16("down_frame_count"),
    SInt16("up_frame_count"),

    Pad(32),
    reflexive("animations", anim_enum_desc, 55,
        *unit_weapon_animation_names
        ),
    reflexive("ik_points", ik_point_desc, 4, DYN_NAME_PATH=".marker"),
    reflexive("weapon_types", weapon_types_desc, 10, DYN_NAME_PATH=".label"),
    SIZE=188,
    )

unit_desc = Struct("unit",
    ascii_str32("label"),
    #pitch and yaw are saved in radians.

    #Looking screen bounds
    float_rad("right_yaw_per_frame"),
    float_rad("left_yaw_per_frame"),
    SInt16("right_frame_count"),
    SInt16("left_frame_count"),

    float_rad("down_pitch_per_frame"),
    float_rad("up_pitch_per_frame"),
    SInt16("down_frame_count"),
    SInt16("up_frame_count"),

    Pad(8),
    reflexive("animations", anim_enum_desc, 30,
        *unit_animation_names
        ),
    reflexive("ik_points", ik_point_desc, 4, DYN_NAME_PATH=".marker"),
    reflexive("weapons", unit_weapon_desc, 16, DYN_NAME_PATH=".name"),
    SIZE=100,
    )

weapon_desc = Struct("weapon",
    Pad(16),
    reflexive("animations", anim_enum_desc, 11,
        *weapon_animation_names
        ),
    SIZE=28,
    )

suspension_desc = QStruct("suspension_animation",
    SInt16("mass_point_index"),
    dyn_senum16("animation", DYN_NAME_PATH=dyn_anim_path),
    Float("full_extension_ground_depth"),
    Float("full_compression_ground_depth"),
    SIZE=20,
    )

vehicle_desc = Struct("vehicle",
    #pitch and yaw are saved in radians.

    #Steering screen bounds
    float_rad("right_yaw_per_frame"),
    float_rad("left_yaw_per_frame"),
    SInt16("right_frame_count"),
    SInt16("left_frame_count"),

    float_rad("down_pitch_per_frame"),
    float_rad("up_pitch_per_frame"),
    SInt16("down_frame_count"),
    SInt16("up_frame_count"),

    Pad(68),
    reflexive("animations", anim_enum_desc, 8,
        *vehicle_animation_names
        ),
    reflexive("suspension_animations", suspension_desc, 8),
    SIZE=116,
    )

device_desc = Struct("device",
    Pad(84),
    reflexive("animations", anim_enum_desc, 2,
        *device_animation_names
        ),
    SIZE=96,
    )

fp_animation_desc = Struct("fp_animation",
    Pad(16),
    reflexive("animations", anim_enum_desc, 28,
        *fp_animation_names
        ),
    SIZE=28,
    )

sound_reference_desc = Struct("sound_reference",
    dependency('sound', "snd!"),
    SIZE=20,
    )

nodes_desc = Struct("node",
    ascii_str32("name"),
    dyn_senum16("next_sibling_node_index", DYN_NAME_PATH="..[DYN_I].name"),
    dyn_senum16("first_child_node_index", DYN_NAME_PATH="..[DYN_I].name"),
    dyn_senum16("parent_node_index", DYN_NAME_PATH="..[DYN_I].name"),
    Pad(2),
    Bool32("node_joint_flags",
        "ball_socket",
        "hinge",
        "no_movement",
        ),
    QStruct("base_vector", INCLUDE=ijk_float),
    float_rad("vector_range"),
    Pad(4),
    SIZE=64,
    )

animation_desc = Struct("animation",
    ascii_str32("name"),
    SEnum16("type", *anim_types),
    SInt16("frame_count"),
    SInt16("frame_size"),
    SEnum16("frame_info_type", *anim_frame_info_types),
    SInt32("node_list_checksum"),
    SInt16("node_count"),
    SInt16("loop_frame_index"),

    Float("weight"),
    SInt16("key_frame_index"),
    SInt16("second_key_frame_index"),

    dyn_senum16("next_animation",
        DYN_NAME_PATH="..[DYN_I].name"),
    Bool16("flags",
        "compressed_data",
        "world_relative",
        { NAME:"pal", GUI_NAME:"25Hz(PAL)" },
        ),
    dyn_senum16("sound",
        DYN_NAME_PATH="tagdata.sound_references." +
        "sound_references_array[DYN_I].sound.filepath"),
    SInt16("sound_frame_index"),
    SInt8("left_foot_frame_index"),
    SInt8("right_foot_frame_index"),
    FlSInt16("first_permutation_index", VISIBLE=False,
        TOOLTIP="The index of the first animation in the permutation chain."),
    FlFloat("chance_to_play", VISIBLE=False,
        MIN=0.0, MAX=1.0, SIDETIP="[0,1]",
        TOOLTIP=("Seems to be the chance range to select this permutation.\n"
                 "Random number in the range [0,1] is rolled. The permutation\n"
                 "chain is looped until the number is higher than or equal\n"
                 "to that permutations chance to play. This chance to play\n"
                 "is likely influenced by the animations 'weight' field.\n"
                 "All permutation chains should have the last one end with\n"
                 "a chance to play of 1.0")),

    rawdata_ref("frame_info", max_size=32768),

    # each of the bits in these flags determines whether
    # or not the frame data stores info for each nodes
    # translation, rotation, and scale.
    # This info was discovered by looking at TheGhost's
    # animation importer script, so thank him for that.
    UInt32("trans_flags0", EDITABLE=False),
    UInt32("trans_flags1", EDITABLE=False),
    Pad(8),
    UInt32("rot_flags0", EDITABLE=False),
    UInt32("rot_flags1", EDITABLE=False),
    Pad(8),
    UInt32("scale_flags0", EDITABLE=False),
    UInt32("scale_flags1", EDITABLE=False),
    Pad(4),
    SInt32("offset_to_compressed_data", EDITABLE=False),
    rawdata_ref("default_data", max_size=16384),
    rawdata_ref("frame_data", max_size=1048576),
    SIZE=180,
    )

antr_body = Struct("tagdata",
    reflexive("objects",  object_desc, 4),
    reflexive("units",    unit_desc, 32, DYN_NAME_PATH=".label"),
    reflexive("weapons",  weapon_desc, 1),
    reflexive("vehicles", vehicle_desc, 1),
    reflexive("devices",  device_desc, 1),
    reflexive("unit_damages", anim_enum_desc, 176,
        *unit_damage_animation_names
        ),
    reflexive("fp_animations", fp_animation_desc, 1),
    #i have no idea why they decided to cap it at 257 instead of 256....
    reflexive("sound_references", sound_reference_desc, 257,
        DYN_NAME_PATH=".sound.filepath"),
    Float("limp_body_node_radius"),
    Bool16("flags",
        "compress_all_animations",
        "force_idle_compression",
        ),
    Pad(2),
    reflexive("nodes", nodes_desc, 64, DYN_NAME_PATH=".name"),
    reflexive("animations", animation_desc, 256, DYN_NAME_PATH=".name"),
    SIZE=128,
    )


def get():
    return antr_def

antr_def = TagDef("antr",
    blam_header('antr', 4),
    antr_body,

    ext=".model_animations", endian=">", tag_cls=AntrTag
    )
