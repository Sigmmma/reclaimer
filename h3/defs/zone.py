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
from supyr_struct.defs.tag_def import TagDef

active_members_bits = tuple("active_member_%s" % i for i in range(32))


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


zone_compression_codec = Struct("compression_codec", 
    BytesRaw("guid", SIZE=16),
    ENDIAN=">", SIZE=16
    )


zone_external_cache_reference = Struct("external_cache_reference", 
    StrLatin1("map_path", SIZE=256),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    BytesRaw("unknown_2", SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=264
    )


zone_raw_page = Struct("raw_page", 
    SInt16("salt"),
    SInt8("flags"),
    SInt8("compression_codec_index"),
    SInt16("shared_cache_index"),
    SInt16("unknown_0"),
    SInt32("block_offset"),
    SInt32("compressed_block_size"),
    SInt32("uncompressed_block_size"),
    SInt32("crc_checksum"),
    BytesRaw("entire_buffer_hash", SIZE=20),
    BytesRaw("first_chunk_hash", SIZE=20),
    BytesRaw("last_chunk_hash", SIZE=20),
    SInt16("block_asset_count"),
    SInt16("unknown_1"),
    ENDIAN=">", SIZE=88
    )


zone_size_part = Struct("part", 
    SInt32("unknown"),
    SInt32("size"),
    ENDIAN=">", SIZE=8
    )


zone_size = Struct("size", 
    SInt32("overall_size"),
    h3_reflexive("parts", zone_size_part),
    ENDIAN=">", SIZE=16
    )


zone_segment = Struct("segment", 
    SInt16("primary_page_index"),
    SInt16("secondary_page_index"),
    SInt32("primary_segment_offset"),
    SInt32("secondary_segment_offset"),
    SInt16("primary_size_index"),
    SInt16("secondary_size_index"),
    ENDIAN=">", SIZE=16
    )


zone_tag_resource_resource_fixup = Struct("resource_fixup", 
    SInt32("block_offset"),
    Bool8("address_location_high_bits", 
        ("fixup", 1 << 5),
        "raw_page",
        ),
    UInt8("address_upper_bits"),
    UInt16("address"),
    ENDIAN=">", SIZE=8
    )


zone_tag_resource_resource_definition_fixup = Struct("resource_definition_fixup", 
    Bool8("offset_location_high_bits", 
        ("fixup", 1 << 5),
        "raw_page",
        ),
    UInt8("offset_upper_bits"),
    UInt16("offset"),
    SInt32("resource_structure_type_index"),
    ENDIAN=">", SIZE=8
    )


zone_tag_resource = Struct("tag_resource", 
    h3_dependency("parent_tag"),
    UInt16("salt"),
    UInt8("resource_type_index"),
    UInt8("flags"),
    SInt32("fixup_information_offset"),
    SInt32("fixup_information_length"),
    SInt32("secondary_fixup_information_offset"),
    SInt16("unknown"),
    SInt16("play_segment_index"),
    Bool8("root_definition_address_location_high_bits", 
        ("fixup", 1 << 5),
        "raw_page",
        ),
    UInt8("root_definition_address_upper_bits"),
    UInt16("root_definition_address"),
    h3_reflexive("resource_fixups", zone_tag_resource_resource_fixup),
    h3_reflexive("resource_definition_fixups", zone_tag_resource_resource_definition_fixup),
    ENDIAN=">", SIZE=64
    )


zone_designer_zoneset_required_raw_pool = Struct("required_raw_pool", 
    Bool32("active_members", *active_members_bits),
    ENDIAN=">", SIZE=4
    )


zone_designer_zoneset_optional_raw_pool = Struct("optional_raw_pool", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_designer_zoneset_optional_raw_pool_2 = Struct("optional_raw_pool_2", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_designer_zoneset_resource_type = Struct("resource_type", 
    BytesRaw("unknown", SIZE=20, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=20
    )


zone_designer_zoneset_required_tag_pool = Struct("required_tag_pool", 
    Bool32("active_members", *active_members_bits),
    ENDIAN=">", SIZE=4
    )


zone_designer_zoneset_optional_tag_pool = Struct("optional_tag_pool", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_designer_zoneset = Struct("designer_zoneset", 
    h3_reflexive("required_raw_pool", zone_designer_zoneset_required_raw_pool),
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    h3_reflexive("optional_raw_pool", zone_designer_zoneset_optional_raw_pool),
    h3_reflexive("optional_raw_pool_2", zone_designer_zoneset_optional_raw_pool_2),
    BytesRaw("unknown_1", SIZE=20, VISIBLE=False),
    h3_string_id("set_name"),
    h3_reflexive("resource_types", zone_designer_zoneset_resource_type),
    h3_reflexive("required_tag_pool", zone_designer_zoneset_required_tag_pool),
    h3_reflexive("optional_tag_pool", zone_designer_zoneset_optional_tag_pool),
    BytesRaw("unknown_2", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=120
    )


zone_global_zoneset_required_raw_pool = Struct("required_raw_pool", 
    Bool32("active_members", *active_members_bits),
    ENDIAN=">", SIZE=4
    )


zone_global_zoneset_optional_raw_pool = Struct("optional_raw_pool", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_global_zoneset_optional_raw_pool_2 = Struct("optional_raw_pool_2", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_global_zoneset_resource_type = Struct("resource_type", 
    BytesRaw("unknown", SIZE=20, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=20
    )


zone_global_zoneset_required_tag_pool = Struct("required_tag_pool", 
    Bool32("active_members", *active_members_bits),
    ENDIAN=">", SIZE=4
    )


zone_global_zoneset_optional_tag_pool = Struct("optional_tag_pool", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_global_zoneset = Struct("global_zoneset", 
    h3_reflexive("required_raw_pool", zone_global_zoneset_required_raw_pool),
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    h3_reflexive("optional_raw_pool", zone_global_zoneset_optional_raw_pool),
    h3_reflexive("optional_raw_pool_2", zone_global_zoneset_optional_raw_pool_2),
    BytesRaw("unknown_1", SIZE=20, VISIBLE=False),
    h3_string_id("set_name"),
    h3_reflexive("resource_types", zone_global_zoneset_resource_type),
    h3_reflexive("required_tag_pool", zone_global_zoneset_required_tag_pool),
    h3_reflexive("optional_tag_pool", zone_global_zoneset_optional_tag_pool),
    BytesRaw("unknown_2", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=120
    )


zone_unattached_zoneset_required_raw_pool = Struct("required_raw_pool", 
    Bool32("active_members", *active_members_bits),
    ENDIAN=">", SIZE=4
    )


zone_unattached_zoneset_optional_raw_pool = Struct("optional_raw_pool", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_unattached_zoneset_optional_raw_pool_2 = Struct("optional_raw_pool_2", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_unattached_zoneset_resource_type = Struct("resource_type", 
    BytesRaw("unknown", SIZE=20, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=20
    )


zone_unattached_zoneset_required_tag_pool = Struct("required_tag_pool", 
    Bool32("active_members", *active_members_bits),
    ENDIAN=">", SIZE=4
    )


zone_unattached_zoneset_optional_tag_pool = Struct("optional_tag_pool", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_unattached_zoneset = Struct("unattached_zoneset", 
    h3_reflexive("required_raw_pool", zone_unattached_zoneset_required_raw_pool),
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    h3_reflexive("optional_raw_pool", zone_unattached_zoneset_optional_raw_pool),
    h3_reflexive("optional_raw_pool_2", zone_unattached_zoneset_optional_raw_pool_2),
    BytesRaw("unknown_1", SIZE=20, VISIBLE=False),
    h3_string_id("set_name"),
    h3_reflexive("resource_types", zone_unattached_zoneset_resource_type),
    h3_reflexive("required_tag_pool", zone_unattached_zoneset_required_tag_pool),
    h3_reflexive("optional_tag_pool", zone_unattached_zoneset_optional_tag_pool),
    BytesRaw("unknown_2", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=120
    )


zone_disc_forbidden_zoneset_required_raw_pool = Struct("required_raw_pool", 
    Bool32("active_members", *active_members_bits),
    ENDIAN=">", SIZE=4
    )


zone_disc_forbidden_zoneset_optional_raw_pool = Struct("optional_raw_pool", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_disc_forbidden_zoneset_optional_raw_pool_2 = Struct("optional_raw_pool_2", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_disc_forbidden_zoneset_resource_type = Struct("resource_type", 
    BytesRaw("unknown", SIZE=20, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=20
    )


zone_disc_forbidden_zoneset_required_tag_pool = Struct("required_tag_pool", 
    Bool32("active_members", *active_members_bits),
    ENDIAN=">", SIZE=4
    )


zone_disc_forbidden_zoneset_optional_tag_pool = Struct("optional_tag_pool", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_disc_forbidden_zoneset = Struct("disc_forbidden_zoneset", 
    h3_reflexive("required_raw_pool", zone_disc_forbidden_zoneset_required_raw_pool),
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    h3_reflexive("optional_raw_pool", zone_disc_forbidden_zoneset_optional_raw_pool),
    h3_reflexive("optional_raw_pool_2", zone_disc_forbidden_zoneset_optional_raw_pool_2),
    BytesRaw("unknown_1", SIZE=20, VISIBLE=False),
    h3_string_id("set_name"),
    h3_reflexive("resource_types", zone_disc_forbidden_zoneset_resource_type),
    h3_reflexive("required_tag_pool", zone_disc_forbidden_zoneset_required_tag_pool),
    h3_reflexive("optional_tag_pool", zone_disc_forbidden_zoneset_optional_tag_pool),
    BytesRaw("unknown_2", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=120
    )


zone_disc_always_streaming_zoneset_required_raw_pool = Struct("required_raw_pool", 
    Bool32("active_members", *active_members_bits),
    ENDIAN=">", SIZE=4
    )


zone_disc_always_streaming_zoneset_optional_raw_pool = Struct("optional_raw_pool", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_disc_always_streaming_zoneset_optional_raw_pool_2 = Struct("optional_raw_pool_2", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_disc_always_streaming_zoneset_resource_type = Struct("resource_type", 
    BytesRaw("unknown", SIZE=20, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=20
    )


zone_disc_always_streaming_zoneset_required_tag_pool = Struct("required_tag_pool", 
    Bool32("active_members", *active_members_bits),
    ENDIAN=">", SIZE=4
    )


zone_disc_always_streaming_zoneset_optional_tag_pool = Struct("optional_tag_pool", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_disc_always_streaming_zoneset = Struct("disc_always_streaming_zoneset", 
    h3_reflexive("required_raw_pool", zone_disc_always_streaming_zoneset_required_raw_pool),
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    h3_reflexive("optional_raw_pool", zone_disc_always_streaming_zoneset_optional_raw_pool),
    h3_reflexive("optional_raw_pool_2", zone_disc_always_streaming_zoneset_optional_raw_pool_2),
    BytesRaw("unknown_1", SIZE=20, VISIBLE=False),
    h3_string_id("set_name"),
    h3_reflexive("resource_types", zone_disc_always_streaming_zoneset_resource_type),
    h3_reflexive("required_tag_pool", zone_disc_always_streaming_zoneset_required_tag_pool),
    h3_reflexive("optional_tag_pool", zone_disc_always_streaming_zoneset_optional_tag_pool),
    BytesRaw("unknown_2", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=120
    )


zone_bsp_zoneset_required_raw_pool = Struct("required_raw_pool", 
    Bool32("active_members", *active_members_bits),
    ENDIAN=">", SIZE=4
    )


zone_bsp_zoneset_optional_raw_pool = Struct("optional_raw_pool", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_bsp_zoneset_optional_raw_pool_2 = Struct("optional_raw_pool_2", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_bsp_zoneset_resource_type = Struct("resource_type", 
    BytesRaw("unknown", SIZE=20, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=20
    )


zone_bsp_zoneset_required_tag_pool = Struct("required_tag_pool", 
    Bool32("active_members", *active_members_bits),
    ENDIAN=">", SIZE=4
    )


zone_bsp_zoneset_optional_tag_pool = Struct("optional_tag_pool", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_bsp_zoneset = Struct("bsp_zoneset", 
    h3_reflexive("required_raw_pool", zone_bsp_zoneset_required_raw_pool),
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    h3_reflexive("optional_raw_pool", zone_bsp_zoneset_optional_raw_pool),
    h3_reflexive("optional_raw_pool_2", zone_bsp_zoneset_optional_raw_pool_2),
    BytesRaw("unknown_1", SIZE=20, VISIBLE=False),
    h3_string_id("set_name"),
    h3_reflexive("resource_types", zone_bsp_zoneset_resource_type),
    h3_reflexive("required_tag_pool", zone_bsp_zoneset_required_tag_pool),
    h3_reflexive("optional_tag_pool", zone_bsp_zoneset_optional_tag_pool),
    BytesRaw("unknown_2", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=120
    )


zone_bsp_zonesets_2_required_raw_pool = Struct("required_raw_pool", 
    Bool32("active_members", *active_members_bits),
    ENDIAN=">", SIZE=4
    )


zone_bsp_zonesets_2_optional_raw_pool = Struct("optional_raw_pool", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_bsp_zonesets_2_optional_raw_pool_2 = Struct("optional_raw_pool_2", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_bsp_zonesets_2_resource_type = Struct("resource_type", 
    BytesRaw("unknown", SIZE=20, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=20
    )


zone_bsp_zonesets_2_required_tag_pool = Struct("required_tag_pool", 
    Bool32("active_members", *active_members_bits),
    ENDIAN=">", SIZE=4
    )


zone_bsp_zonesets_2_optional_tag_pool = Struct("optional_tag_pool", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_bsp_zonesets_2 = Struct("bsp_zonesets_2", 
    h3_reflexive("required_raw_pool", zone_bsp_zonesets_2_required_raw_pool),
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    h3_reflexive("optional_raw_pool", zone_bsp_zonesets_2_optional_raw_pool),
    h3_reflexive("optional_raw_pool_2", zone_bsp_zonesets_2_optional_raw_pool_2),
    BytesRaw("unknown_1", SIZE=20, VISIBLE=False),
    h3_string_id("set_name"),
    h3_reflexive("resource_types", zone_bsp_zonesets_2_resource_type),
    h3_reflexive("required_tag_pool", zone_bsp_zonesets_2_required_tag_pool),
    h3_reflexive("optional_tag_pool", zone_bsp_zonesets_2_optional_tag_pool),
    BytesRaw("unknown_2", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=120
    )


zone_bsp_zonesets_3_required_raw_pool = Struct("required_raw_pool", 
    Bool32("active_members", *active_members_bits),
    ENDIAN=">", SIZE=4
    )


zone_bsp_zonesets_3_optional_raw_pool = Struct("optional_raw_pool", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_bsp_zonesets_3_optional_raw_pool_2 = Struct("optional_raw_pool_2", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_bsp_zonesets_3_resource_type = Struct("resource_type", 
    BytesRaw("unknown", SIZE=20, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=20
    )


zone_bsp_zonesets_3_required_tag_pool = Struct("required_tag_pool", 
    Bool32("active_members", *active_members_bits),
    ENDIAN=">", SIZE=4
    )


zone_bsp_zonesets_3_optional_tag_pool = Struct("optional_tag_pool", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_bsp_zonesets_3 = Struct("bsp_zonesets_3", 
    h3_reflexive("required_raw_pool", zone_bsp_zonesets_3_required_raw_pool),
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    h3_reflexive("optional_raw_pool", zone_bsp_zonesets_3_optional_raw_pool),
    h3_reflexive("optional_raw_pool_2", zone_bsp_zonesets_3_optional_raw_pool_2),
    BytesRaw("unknown_1", SIZE=20, VISIBLE=False),
    h3_string_id("set_name"),
    h3_reflexive("resource_types", zone_bsp_zonesets_3_resource_type),
    h3_reflexive("required_tag_pool", zone_bsp_zonesets_3_required_tag_pool),
    h3_reflexive("optional_tag_pool", zone_bsp_zonesets_3_optional_tag_pool),
    BytesRaw("unknown_2", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=120
    )


zone_cinematic_zoneset_required_raw_pool = Struct("required_raw_pool", 
    Bool32("active_members", *active_members_bits),
    ENDIAN=">", SIZE=4
    )


zone_cinematic_zoneset_optional_raw_pool = Struct("optional_raw_pool", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_cinematic_zoneset_optional_raw_pool_2 = Struct("optional_raw_pool_2", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_cinematic_zoneset_resource_type = Struct("resource_type", 
    BytesRaw("unknown", SIZE=20, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=20
    )


zone_cinematic_zoneset_required_tag_pool = Struct("required_tag_pool", 
    Bool32("active_members", *active_members_bits),
    ENDIAN=">", SIZE=4
    )


zone_cinematic_zoneset_optional_tag_pool = Struct("optional_tag_pool", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_cinematic_zoneset = Struct("cinematic_zoneset", 
    h3_reflexive("required_raw_pool", zone_cinematic_zoneset_required_raw_pool),
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    h3_reflexive("optional_raw_pool", zone_cinematic_zoneset_optional_raw_pool),
    h3_reflexive("optional_raw_pool_2", zone_cinematic_zoneset_optional_raw_pool_2),
    BytesRaw("unknown_1", SIZE=20, VISIBLE=False),
    h3_string_id("set_name"),
    h3_reflexive("resource_types", zone_cinematic_zoneset_resource_type),
    h3_reflexive("required_tag_pool", zone_cinematic_zoneset_required_tag_pool),
    h3_reflexive("optional_tag_pool", zone_cinematic_zoneset_optional_tag_pool),
    BytesRaw("unknown_2", SIZE=12, VISIBLE=False),
    ENDIAN=">", SIZE=120
    )


zone_scenario_zoneset_required_raw_pool = Struct("required_raw_pool", 
    Bool32("active_members", *active_members_bits),
    ENDIAN=">", SIZE=4
    )


zone_scenario_zoneset_optional_raw_pool = Struct("optional_raw_pool", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_scenario_zoneset_optional_raw_pool_2 = Struct("optional_raw_pool_2", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_scenario_zoneset_resource_type = Struct("resource_type", 
    BytesRaw("unknown", SIZE=20, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=20
    )


zone_scenario_zoneset_required_tag_pool = Struct("required_tag_pool", 
    Bool32("active_members", *active_members_bits),
    ENDIAN=">", SIZE=4
    )


zone_scenario_zoneset_optional_tag_pool = Struct("optional_tag_pool", 
    Bool32("active_members", *active_members_bits),
    VISIBLE=False,
    ENDIAN=">", SIZE=4
    )


zone_scenario_zoneset = Struct("scenario_zoneset", 
    h3_reflexive("required_raw_pool", zone_scenario_zoneset_required_raw_pool),
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    h3_reflexive("optional_raw_pool", zone_scenario_zoneset_optional_raw_pool),
    h3_reflexive("optional_raw_pool_2", zone_scenario_zoneset_optional_raw_pool_2),
    BytesRaw("unknown_1", SIZE=20, VISIBLE=False),
    h3_string_id("set_name"),
    h3_reflexive("resource_types", zone_scenario_zoneset_resource_type),
    h3_reflexive("required_tag_pool", zone_scenario_zoneset_required_tag_pool),
    h3_reflexive("optional_tag_pool", zone_scenario_zoneset_optional_tag_pool),
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


zone_unknown_4 = Struct("unknown_4", 
    BytesRaw("unknown", SIZE=20, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=20
    )


zone_prediction_a = Struct("prediction_a", 
    UInt32("key"),
    ENDIAN=">", SIZE=4
    )


zone_prediction_b = Struct("prediction_b", 
    SInt16("overall_index"),
    SInt16("a_count"),
    SInt32("a_index"),
    ENDIAN=">", SIZE=8
    )


zone_prediction_c = Struct("prediction_c", 
    SInt16("overall_index"),
    SInt16("b_index"),
    ENDIAN=">", SIZE=4
    )


zone_prediction_d_tag = Struct("prediction_d_tag", 
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
    h3_reflexive("resource_types", zone_resource_type),
    h3_reflexive("resource_structure_types", zone_resource_structure_type),
    h3_reflexive("compression_codecs", zone_compression_codec),
    h3_reflexive("external_cache_references", zone_external_cache_reference),
    h3_reflexive("raw_pages", zone_raw_page),
    h3_reflexive("sizes", zone_size),
    h3_reflexive("segments", zone_segment),
    h3_reflexive("tag_resources", zone_tag_resource),
    h3_reflexive("designer_zonesets", zone_designer_zoneset),
    h3_reflexive("global_zoneset", zone_global_zoneset),
    BytesRaw("unknown_0", SIZE=12, VISIBLE=False),
    h3_reflexive("unattached_zoneset", zone_unattached_zoneset),
    h3_reflexive("disc_forbidden_zoneset", zone_disc_forbidden_zoneset),
    h3_reflexive("disc_always_streaming_zoneset", zone_disc_always_streaming_zoneset),
    h3_reflexive("bsp_zonesets", zone_bsp_zoneset),
    h3_reflexive("bsp_zonesets_2", zone_bsp_zonesets_2),
    h3_reflexive("bsp_zonesets_3", zone_bsp_zonesets_3),
    h3_reflexive("cinematic_zonesets", zone_cinematic_zoneset),
    h3_reflexive("scenario_zonesets", zone_scenario_zoneset),
    BytesRaw("unknown_1", SIZE=24, VISIBLE=False),
    h3_reflexive("scenario_zoneset_groups", zone_scenario_zoneset_group),
    h3_reflexive("scenario_bsps", zone_scenario_bsp),
    BytesRaw("unknown_2", SIZE=36, VISIBLE=False),
    h3_rawdata_ref("fixup_information"),
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