############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: -DeToX-
# 	Mapped out the Raw Entry Table struct
# revision: 3		author: Lord Zedd
# 	Matching Zonesets
# revision: 4		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from .play import play_body
from supyr_struct.defs.tag_def import TagDef


zone_resource_type = Struct("resource_type", 
    BytesRaw("guid", SIZE=16),
    Array("unknown_array", SUB_STRUCT=SInt16("unknown"), SIZE=4),
    h3_string_id("name"),
    ENDIAN=">", SIZE=28
    )


zone_resource_structure_type = Struct("resource_structure_type", 
    BytesRaw("guid", SIZE=16),
    h3_string_id("name"),
    ENDIAN=">", SIZE=20
    )


zone_tag_resource_resource_fixup = Struct("resource_fixup", 
    SInt32("block_offset"),
    h3_page_offset_info("address_info"),
    ENDIAN=">", SIZE=8,
    COMMENT="""
Block Offset: Offset in tag data sub-buffer.
Address: Fix-up address(either in the data sub-buffer, or a cache-resource offset."""
    )


zone_tag_resource_resource_definition_fixup = Struct("resource_definition_fixup", 
    h3_page_offset_info("offset_info"),
    dyn_senum32("resource_structure_type",
        DYN_NAME_PATH="........resource_structure_types.STEPTREE[DYN_I].name.string",
        WIDGET_WIDTH=32
        ),
    ENDIAN=">", SIZE=8
    )


zone_tag_resource = Struct("tag_resource", 
    h3_dependency("parent_tag"),
    UInt16("salt"),
    dyn_senum8("resource_type",
        DYN_NAME_PATH=".....resource_types.STEPTREE[DYN_I].name.string",
        WIDGET_WIDTH=32
        ),
    UInt8("flags"),
    SInt32("fixup_info_offset"),
    SInt32("fixup_info_size"),
    SInt32("secondary_fixup_info_offset"),
    Bool16("pages_used",
        "primary",
        "secondary",
        ),
    SInt16("segment_index"),
    h3_page_offset_info("root_definition_address_info"),
    h3_reflexive("resource_fixups", zone_tag_resource_resource_fixup),
    h3_reflexive("resource_definition_fixups", zone_tag_resource_resource_definition_fixup),
    ENDIAN=">", SIZE=64,
    )


zone_zoneset_raw_pool = Struct("raw_pool", 
    Bool32("active_members", *("active_member_%s" % i for i in range(32))),
    ENDIAN=">", SIZE=4
    )


zone_zoneset_resource_type = QStruct("resource_type",
    UInt16("unknown0"),
    UInt16("unknown1"),
    UInt16("unknown2"),
    UInt16("unknown3"),
    UInt16("unknown4"),
    UInt16("unknown5"),
    UInt16("unknown6"),
    UInt16("unknown7"),
    UInt16("unknown8"),
    UInt16("unknown9"),
    #BytesRaw("unknown", SIZE=20, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=20
    )


zone_zoneset = Struct("zoneset", 
    h3_reflexive("required_raw_pool", zone_zoneset_raw_pool),
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    h3_reflexive("optional_raw_pool", zone_zoneset_raw_pool),
    h3_reflexive("optional_raw_pool_2", zone_zoneset_raw_pool),
    BytesRaw("unknown_1", SIZE=20, VISIBLE=False),
    h3_string_id("set_name"),
    h3_reflexive("resource_types", zone_zoneset_resource_type),
    h3_reflexive("required_tag_pool", zone_zoneset_raw_pool),
    h3_reflexive("optional_tag_pool", zone_zoneset_raw_pool),
    BytesRaw("unknown_2", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=120
    )


zone_scenario_zoneset_group = Struct("scenario_zoneset_group", 
    h3_string_id("name"),
    SInt32("bsp_group_index"),
    Bool32("import_loaded_bsps", *("bsp_%s" % i for i in range(32))),
    Bool32("loaded_bsps", *("bsp_%s" % i for i in range(32))),
    Bool32("loaded_designer_zonesets", *("set_%s" % i for i in range(32))),
    Bool32("unknown_loaded_designer_zonesets", *("set_%s" % i for i in range(32))),
    Bool32("unloaded_designer_zonesets", *("set_%s" % i for i in range(32))),
    Bool32("loaded_cinematic_zonesets", *("set_%s" % i for i in range(32))),
    SInt32("bsp_atlas_index"),
    ENDIAN=">", SIZE=36
    )


zone_scenario_bsp = Struct("scenario_bsp", 
    h3_dependency("bsp"),
    ENDIAN=">", SIZE=16
    )


zone_unknown_4 = QStruct("unknown_4", 
    UInt32("unknown0"),
    UInt32("unknown1"),
    UInt32("unknown2"),
    UInt32("unknown3"),
    UInt32("unknown4"),
    #BytesRaw("unknown", SIZE=20, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=20
    )


zone_prediction_a = QStruct("prediction_a", 
    UInt32("key"),
    ENDIAN=">", SIZE=4
    )


zone_prediction_b = QStruct("prediction_b", 
    SInt16("overall_index"),
    SInt16("a_count"),
    SInt32("a_index"),
    ENDIAN=">", SIZE=8
    )


zone_prediction_c = QStruct("prediction_c", 
    SInt16("overall_index"),
    SInt16("b_index"),
    ENDIAN=">", SIZE=4
    )


zone_prediction_d_tag = QStruct("prediction_d_tag", 
    SInt16("c_count"),
    SInt16("c_index"),
    SInt16("a_count"),
    SInt16("a_index"),
    ENDIAN=">", SIZE=8
    )


zone_prediction_d2_tag = Struct("prediction_d2_tag", 
    dependency_uint32("tag", VISIBLE=False),
    SInt32("first_value"),
    SInt32("second_value"),
    ENDIAN=">", SIZE=12
    )


zone_body = Struct("tagdata", 
    SEnum16("map_type", *zone_map_type),
    SInt16("flags"),
    h3_reflexive("resource_types", zone_resource_type,
        DYN_NAME_PATH='.name.string'),
    h3_reflexive("resource_structure_types", zone_resource_structure_type,
        DYN_NAME_PATH='.name.string'),
    Struct("play_data", INCLUDE=play_body),
    h3_reflexive("tag_resources", zone_tag_resource),
    Struct("zonesets",
        h3_reflexive("designer", zone_zoneset),
        h3_reflexive("global", zone_zoneset),
        BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
        h3_reflexive("unattached", zone_zoneset),
        h3_reflexive("disc_forbidden", zone_zoneset),
        h3_reflexive("disc_always_streaming", zone_zoneset),
        h3_reflexive("bsp_1", zone_zoneset),
        h3_reflexive("bsp_2", zone_zoneset),
        h3_reflexive("bsp_3", zone_zoneset),
        h3_reflexive("cinematic", zone_zoneset),
        h3_reflexive("scenario", zone_zoneset),
        BytesRaw("unknown_1", SIZE=24, VISIBLE=False),
        ),
    h3_reflexive("scenario_zoneset_groups", zone_scenario_zoneset_group),
    h3_reflexive("scenario_bsps", zone_scenario_bsp),
    BytesRaw("unknown_2", SIZE=36, VISIBLE=False),
    h3_rawdata_ref("fixup_info"),
    BytesRaw("unknown_3", SIZE=20, VISIBLE=False),
    h3_reflexive("unknown_4", zone_unknown_4),
    BytesRaw("unknown_5", SIZE=96, VISIBLE=False),
    h3_reflexive("prediction_a", zone_prediction_a),
    h3_reflexive("prediction_b", zone_prediction_b),
    h3_reflexive("prediction_c", zone_prediction_c),
    h3_reflexive("prediction_d_tags", zone_prediction_d_tag),
    h3_reflexive("prediction_d2_tags", zone_prediction_d2_tag),
    SInt32("campaign_id"),
    SInt32("map_id"),
    ENDIAN=">", SIZE=532
    )


def get():
    return zone_def

zone_def = TagDef("zone",
    h3_blam_header('zone'),
    zone_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["zone"], endian=">", tag_cls=H3Tag
    )
