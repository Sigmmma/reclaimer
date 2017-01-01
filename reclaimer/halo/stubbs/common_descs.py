from ..common_descs import *

# ###########################################################################
# The order of element in all the enumerators is important(DONT SHUFFLE THEM)
# ###########################################################################

#Shared Enumerator options
materials_list = (
    "unknown1",
    "unknown2",
    "unknown3",
    "unknown4",
    "unknown5",
    "unknown6",
    "unknown7",
    "unknown8",
    "unknown9",
    "unknown10",
    "unknown11",
    "unknown12",
    "unknown13",
    "unknown14",
    "unknown15",
    "unknown16",
    "unknown17",
    "unknown18",
    "unknown19",
    "unknown20",
    "unknown21",
    "unknown22",
    "unknown23",
    "unknown24",
    "unknown25",
    "unknown26",
    "unknown27",
    "unknown28",
    "unknown29",
    "unknown30",
    "unknown31",
    "unknown32",
    "unknown33",
    "unknown34",
    "unknown35",
    )
actor_types = (
    "unknown1",
    "unknown2",
    "unknown3",
    "unknown4",
    "unknown5",
    "unknown6",
    "unknown7",
    "unknown8",
    "unknown9",
    "unknown10",
    "unknown11",
    "unknown12",
    "unknown13",
    "unknown14",
    "unknown15",
    "unknown16",
    )
damage_category = (
    "unknown1",
    "unknown2",
    "unknown3",
    "unknown4",
    "unknown5",
    "unknown6",
    "unknown7",
    "unknown8",
    "unknown9",
    "unknown10",
    "unknown11",
    "unknown12",
    "unknown13",
    )
grenade_types = (
    'unknown1',
    'unknown2',
    'unknown3',
    'unknown4',
    )

#Tag class specific enumerators
unit_teams = (
    "none",
    "player",
    "unknown1",
    "unknown2",
    "unknown3",
    "unknown4",
    "unknown5",
    "unknown6",
    "unknown7",
    "unknown8",
    )
vehicle_types = (
    "unknown1",
    "unknown2",
    "unknown3",
    "unknown4",
    "unknown5",
    "unknown6",
    "unknown7",
    )
weapon_types = (
    "unknown1",
    "unknown2",
    "unknown3",
    "unknown4",
    "unknown5",
    )

damage_modifiers = QStruct("damage modifiers",
    *(float_zero_to_inf(material_name) for material_name in materials_list)
    )
