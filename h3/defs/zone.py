from reclaimer.common_descs import *
from supyr_struct.defs.tag_def import TagDef

zone_map_type = (
    "single_player",
    "multiplayer",
    "main_menu",
    )


zone_resource_type = Struct("resource_types",
    BytesRaw("guid", SIZE=16),
    SInt16("unknown"),
    SInt16("unknown_1"),
    SInt16("unknown_2"),
    SInt16("unknown_3"),
    string_id_meta("name"),
    ENDIAN=">", SIZE=28
    )


zone_resource_structure_type = Struct("resource_structure_types",
    BytesRaw("guid", SIZE=16),
    string_id_meta("name"),
    ENDIAN=">", SIZE=20
    )


zone_compression_codec = Struct("compression_codecs",
    BytesRaw("guid", SIZE=16),
    ENDIAN=">", SIZE=16
    )


zone_external_cache_reference = Struct("external_cache_references",
    StrLatin1("map_path", SIZE=256),
    SInt16("unknown"),
    SInt16("unknown_1"),
    Pad(4),
    ENDIAN=">", SIZE=264
    )


zone_raw_page = Struct("raw_pages",
    SInt16("salt"),
    SInt8("flags"),
    SInt8("compression_codec_index"),
    SInt16("shared_cache_index"),
    SInt16("unknown"),
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


zone_size_part = Struct("parts",
    SInt32("unknown"),
    SInt32("size"),
    ENDIAN=">", SIZE=8
    )


zone_size = Struct("sizes",
    SInt32("overall_size"),
    reflexive("parts", zone_size_part),
    ENDIAN=">", SIZE=16
    )


zone_segment = Struct("segments",
    SInt16("primary_page_index"),
    SInt16("secondary_page_index"),
    SInt32("primary_segment_offset"),
    SInt32("secondary_segment_offset"),
    SInt16("primary_size_index"),
    SInt16("secondary_size_index"),
    ENDIAN=">", SIZE=16
    )


zone_tag_resource_resource_fixup = Struct("resource_fixups",
    SInt32("block_offset"),
    Bool8("address_location_high_bits",
        ("fixup", 1 << 5),
        "raw_page",
        ),
    UInt8("address_upper_bits"),
    UInt16("address"),
    ENDIAN=">", SIZE=8
    )


zone_tag_resource_resource_definition_fixup = Struct("resource_definition_fixups",
    Bool8("offset_location_high_bits",
        ("fixup", 1 << 5),
        "raw_page",
        ),
    UInt8("offset_upper_bits"),
    UInt16("offset"),
    SInt32("resource_structure_type_index"),
    ENDIAN=">", SIZE=8
    )


zone_tag_resource = Struct("tag_resources",
    dependency("parent_tag"),
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
    reflexive("resource_fixups", zone_tag_resource_resource_fixup),
    reflexive("resource_definition_fixups", zone_tag_resource_resource_definition_fixup),
    ENDIAN=">", SIZE=64
    )


zone_designer_zoneset_required_raw_pool = Struct("required_raw_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_designer_zoneset_optional_raw_pool = Struct("optional_raw_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_designer_zoneset_optional_raw_pool_2 = Struct("optional_raw_pool_2",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_designer_zoneset_resource_type = Struct("resource_types",
    Pad(20),
    ENDIAN=">", SIZE=20
    )


zone_designer_zoneset_required_tag_pool = Struct("required_tag_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_designer_zoneset_optional_tag_pool = Struct("optional_tag_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_designer_zoneset = Struct("designer_zonesets",
    reflexive("required_raw_pool", zone_designer_zoneset_required_raw_pool),
    Pad(12),
    reflexive("optional_raw_pool", zone_designer_zoneset_optional_raw_pool),
    reflexive("optional_raw_pool_2", zone_designer_zoneset_optional_raw_pool_2),
    Pad(20),
    string_id_meta("set_name"),
    reflexive("resource_types", zone_designer_zoneset_resource_type),
    reflexive("required_tag_pool", zone_designer_zoneset_required_tag_pool),
    reflexive("optional_tag_pool", zone_designer_zoneset_optional_tag_pool),
    Pad(12),
    ENDIAN=">", SIZE=120
    )


zone_global_zoneset_required_raw_pool = Struct("required_raw_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_global_zoneset_optional_raw_pool = Struct("optional_raw_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_global_zoneset_optional_raw_pool_2 = Struct("optional_raw_pool_2",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_global_zoneset_resource_type = Struct("resource_types",
    Pad(20),
    ENDIAN=">", SIZE=20
    )


zone_global_zoneset_required_tag_pool = Struct("required_tag_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_global_zoneset_optional_tag_pool = Struct("optional_tag_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_global_zoneset = Struct("global_zoneset",
    reflexive("required_raw_pool", zone_global_zoneset_required_raw_pool),
    Pad(12),
    reflexive("optional_raw_pool", zone_global_zoneset_optional_raw_pool),
    reflexive("optional_raw_pool_2", zone_global_zoneset_optional_raw_pool_2),
    Pad(20),
    string_id_meta("set_name"),
    reflexive("resource_types", zone_global_zoneset_resource_type),
    reflexive("required_tag_pool", zone_global_zoneset_required_tag_pool),
    reflexive("optional_tag_pool", zone_global_zoneset_optional_tag_pool),
    Pad(12),
    ENDIAN=">", SIZE=120
    )


zone_unattached_zoneset_required_raw_pool = Struct("required_raw_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_unattached_zoneset_optional_raw_pool = Struct("optional_raw_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_unattached_zoneset_optional_raw_pool_2 = Struct("optional_raw_pool_2",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_unattached_zoneset_resource_type = Struct("resource_types",
    Pad(20),
    ENDIAN=">", SIZE=20
    )


zone_unattached_zoneset_required_tag_pool = Struct("required_tag_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_unattached_zoneset_optional_tag_pool = Struct("optional_tag_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_unattached_zoneset = Struct("unattached_zoneset",
    reflexive("required_raw_pool", zone_unattached_zoneset_required_raw_pool),
    Pad(12),
    reflexive("optional_raw_pool", zone_unattached_zoneset_optional_raw_pool),
    reflexive("optional_raw_pool_2", zone_unattached_zoneset_optional_raw_pool_2),
    Pad(20),
    string_id_meta("set_name"),
    reflexive("resource_types", zone_unattached_zoneset_resource_type),
    reflexive("required_tag_pool", zone_unattached_zoneset_required_tag_pool),
    reflexive("optional_tag_pool", zone_unattached_zoneset_optional_tag_pool),
    Pad(12),
    ENDIAN=">", SIZE=120
    )


zone_disc_forbidden_zoneset_required_raw_pool = Struct("required_raw_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_disc_forbidden_zoneset_optional_raw_pool = Struct("optional_raw_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_disc_forbidden_zoneset_optional_raw_pool_2 = Struct("optional_raw_pool_2",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_disc_forbidden_zoneset_resource_type = Struct("resource_types",
    Pad(20),
    ENDIAN=">", SIZE=20
    )


zone_disc_forbidden_zoneset_required_tag_pool = Struct("required_tag_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_disc_forbidden_zoneset_optional_tag_pool = Struct("optional_tag_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_disc_forbidden_zoneset = Struct("disc_forbidden_zoneset",
    reflexive("required_raw_pool", zone_disc_forbidden_zoneset_required_raw_pool),
    Pad(12),
    reflexive("optional_raw_pool", zone_disc_forbidden_zoneset_optional_raw_pool),
    reflexive("optional_raw_pool_2", zone_disc_forbidden_zoneset_optional_raw_pool_2),
    Pad(20),
    string_id_meta("set_name"),
    reflexive("resource_types", zone_disc_forbidden_zoneset_resource_type),
    reflexive("required_tag_pool", zone_disc_forbidden_zoneset_required_tag_pool),
    reflexive("optional_tag_pool", zone_disc_forbidden_zoneset_optional_tag_pool),
    Pad(12),
    ENDIAN=">", SIZE=120
    )


zone_disc_always_streaming_zoneset_required_raw_pool = Struct("required_raw_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_disc_always_streaming_zoneset_optional_raw_pool = Struct("optional_raw_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_disc_always_streaming_zoneset_optional_raw_pool_2 = Struct("optional_raw_pool_2",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_disc_always_streaming_zoneset_resource_type = Struct("resource_types",
    Pad(20),
    ENDIAN=">", SIZE=20
    )


zone_disc_always_streaming_zoneset_required_tag_pool = Struct("required_tag_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_disc_always_streaming_zoneset_optional_tag_pool = Struct("optional_tag_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_disc_always_streaming_zoneset = Struct("disc_always_streaming_zoneset",
    reflexive("required_raw_pool", zone_disc_always_streaming_zoneset_required_raw_pool),
    Pad(12),
    reflexive("optional_raw_pool", zone_disc_always_streaming_zoneset_optional_raw_pool),
    reflexive("optional_raw_pool_2", zone_disc_always_streaming_zoneset_optional_raw_pool_2),
    Pad(20),
    string_id_meta("set_name"),
    reflexive("resource_types", zone_disc_always_streaming_zoneset_resource_type),
    reflexive("required_tag_pool", zone_disc_always_streaming_zoneset_required_tag_pool),
    reflexive("optional_tag_pool", zone_disc_always_streaming_zoneset_optional_tag_pool),
    Pad(12),
    ENDIAN=">", SIZE=120
    )


zone_bsp_zoneset_required_raw_pool = Struct("required_raw_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_bsp_zoneset_optional_raw_pool = Struct("optional_raw_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_bsp_zoneset_optional_raw_pool_2 = Struct("optional_raw_pool_2",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_bsp_zoneset_resource_type = Struct("resource_types",
    Pad(20),
    ENDIAN=">", SIZE=20
    )


zone_bsp_zoneset_required_tag_pool = Struct("required_tag_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_bsp_zoneset_optional_tag_pool = Struct("optional_tag_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_bsp_zoneset = Struct("bsp_zonesets",
    reflexive("required_raw_pool", zone_bsp_zoneset_required_raw_pool),
    Pad(12),
    reflexive("optional_raw_pool", zone_bsp_zoneset_optional_raw_pool),
    reflexive("optional_raw_pool_2", zone_bsp_zoneset_optional_raw_pool_2),
    Pad(20),
    string_id_meta("set_name"),
    reflexive("resource_types", zone_bsp_zoneset_resource_type),
    reflexive("required_tag_pool", zone_bsp_zoneset_required_tag_pool),
    reflexive("optional_tag_pool", zone_bsp_zoneset_optional_tag_pool),
    Pad(12),
    ENDIAN=">", SIZE=120
    )


zone_bsp_zonesets_2_required_raw_pool = Struct("required_raw_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_bsp_zonesets_2_optional_raw_pool = Struct("optional_raw_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_bsp_zonesets_2_optional_raw_pool_2 = Struct("optional_raw_pool_2",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_bsp_zonesets_2_resource_type = Struct("resource_types",
    Pad(20),
    ENDIAN=">", SIZE=20
    )


zone_bsp_zonesets_2_required_tag_pool = Struct("required_tag_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_bsp_zonesets_2_optional_tag_pool = Struct("optional_tag_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_bsp_zonesets_2 = Struct("bsp_zonesets_2",
    reflexive("required_raw_pool", zone_bsp_zonesets_2_required_raw_pool),
    Pad(12),
    reflexive("optional_raw_pool", zone_bsp_zonesets_2_optional_raw_pool),
    reflexive("optional_raw_pool_2", zone_bsp_zonesets_2_optional_raw_pool_2),
    Pad(20),
    string_id_meta("set_name"),
    reflexive("resource_types", zone_bsp_zonesets_2_resource_type),
    reflexive("required_tag_pool", zone_bsp_zonesets_2_required_tag_pool),
    reflexive("optional_tag_pool", zone_bsp_zonesets_2_optional_tag_pool),
    Pad(12),
    ENDIAN=">", SIZE=120
    )


zone_bsp_zonesets_3_required_raw_pool = Struct("required_raw_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_bsp_zonesets_3_optional_raw_pool = Struct("optional_raw_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_bsp_zonesets_3_optional_raw_pool_2 = Struct("optional_raw_pool_2",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_bsp_zonesets_3_resource_type = Struct("resource_types",
    Pad(20),
    ENDIAN=">", SIZE=20
    )


zone_bsp_zonesets_3_required_tag_pool = Struct("required_tag_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_bsp_zonesets_3_optional_tag_pool = Struct("optional_tag_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_bsp_zonesets_3 = Struct("bsp_zonesets_3",
    reflexive("required_raw_pool", zone_bsp_zonesets_3_required_raw_pool),
    Pad(12),
    reflexive("optional_raw_pool", zone_bsp_zonesets_3_optional_raw_pool),
    reflexive("optional_raw_pool_2", zone_bsp_zonesets_3_optional_raw_pool_2),
    Pad(20),
    string_id_meta("set_name"),
    reflexive("resource_types", zone_bsp_zonesets_3_resource_type),
    reflexive("required_tag_pool", zone_bsp_zonesets_3_required_tag_pool),
    reflexive("optional_tag_pool", zone_bsp_zonesets_3_optional_tag_pool),
    Pad(12),
    ENDIAN=">", SIZE=120
    )


zone_cinematic_zoneset_required_raw_pool = Struct("required_raw_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_cinematic_zoneset_optional_raw_pool = Struct("optional_raw_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_cinematic_zoneset_optional_raw_pool_2 = Struct("optional_raw_pool_2",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_cinematic_zoneset_resource_type = Struct("resource_types",
    Pad(20),
    ENDIAN=">", SIZE=20
    )


zone_cinematic_zoneset_required_tag_pool = Struct("required_tag_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_cinematic_zoneset_optional_tag_pool = Struct("optional_tag_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_cinematic_zoneset = Struct("cinematic_zonesets",
    reflexive("required_raw_pool", zone_cinematic_zoneset_required_raw_pool),
    Pad(12),
    reflexive("optional_raw_pool", zone_cinematic_zoneset_optional_raw_pool),
    reflexive("optional_raw_pool_2", zone_cinematic_zoneset_optional_raw_pool_2),
    Pad(20),
    string_id_meta("set_name"),
    reflexive("resource_types", zone_cinematic_zoneset_resource_type),
    reflexive("required_tag_pool", zone_cinematic_zoneset_required_tag_pool),
    reflexive("optional_tag_pool", zone_cinematic_zoneset_optional_tag_pool),
    Pad(12),
    ENDIAN=">", SIZE=120
    )


zone_scenario_zoneset_required_raw_pool = Struct("required_raw_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_scenario_zoneset_optional_raw_pool = Struct("optional_raw_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_scenario_zoneset_optional_raw_pool_2 = Struct("optional_raw_pool_2",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_scenario_zoneset_resource_type = Struct("resource_types",
    Pad(20),
    ENDIAN=">", SIZE=20
    )


zone_scenario_zoneset_required_tag_pool = Struct("required_tag_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_scenario_zoneset_optional_tag_pool = Struct("optional_tag_pool",
    Bool32("active_members",
        ),
    ENDIAN=">", SIZE=4
    )


zone_scenario_zoneset = Struct("scenario_zonesets",
    reflexive("required_raw_pool", zone_scenario_zoneset_required_raw_pool),
    Pad(12),
    reflexive("optional_raw_pool", zone_scenario_zoneset_optional_raw_pool),
    reflexive("optional_raw_pool_2", zone_scenario_zoneset_optional_raw_pool_2),
    Pad(20),
    string_id_meta("set_name"),
    reflexive("resource_types", zone_scenario_zoneset_resource_type),
    reflexive("required_tag_pool", zone_scenario_zoneset_required_tag_pool),
    reflexive("optional_tag_pool", zone_scenario_zoneset_optional_tag_pool),
    Pad(12),
    ENDIAN=">", SIZE=120
    )


zone_scenario_zoneset_group = Struct("scenario_zoneset_groups",
    string_id_meta("name"),
    SInt32("bsp_group_index"),
    Bool32("import_loaded_bsps",
        "bsp_0",
        "bsp_1",
        "bsp_2",
        "bsp_3",
        "bsp_4",
        "bsp_5",
        "bsp_6",
        "bsp_7",
        "bsp_8",
        "bsp_9",
        "bsp_10",
        "bsp_11",
        "bsp_12",
        "bsp_13",
        "bsp_14",
        "bsp_15",
        "bsp_16",
        "bsp_17",
        "bsp_18",
        "bsp_19",
        "bsp_20",
        "bsp_21",
        "bsp_22",
        "bsp_23",
        "bsp_24",
        "bsp_25",
        "bsp_26",
        "bsp_27",
        "bsp_28",
        "bsp_29",
        "bsp_30",
        "bsp_31",
        ),
    Bool32("loaded_bsps",
        "bsp_0",
        "bsp_1",
        "bsp_2",
        "bsp_3",
        "bsp_4",
        "bsp_5",
        "bsp_6",
        "bsp_7",
        "bsp_8",
        "bsp_9",
        "bsp_10",
        "bsp_11",
        "bsp_12",
        "bsp_13",
        "bsp_14",
        "bsp_15",
        "bsp_16",
        "bsp_17",
        "bsp_18",
        "bsp_19",
        "bsp_20",
        "bsp_21",
        "bsp_22",
        "bsp_23",
        "bsp_24",
        "bsp_25",
        "bsp_26",
        "bsp_27",
        "bsp_28",
        "bsp_29",
        "bsp_30",
        "bsp_31",
        ),
    Bool32("loaded_designer_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        "set_16",
        "set_17",
        "set_18",
        "set_19",
        "set_20",
        "set_21",
        "set_22",
        "set_23",
        "set_24",
        "set_25",
        "set_26",
        "set_27",
        "set_28",
        "set_29",
        "set_30",
        "set_31",
        ),
    Bool32("unknown_loaded_designer_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        "set_16",
        "set_17",
        "set_18",
        "set_19",
        "set_20",
        "set_21",
        "set_22",
        "set_23",
        "set_24",
        "set_25",
        "set_26",
        "set_27",
        "set_28",
        "set_29",
        "set_30",
        "set_31",
        ),
    Bool32("unloaded_designer_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        "set_16",
        "set_17",
        "set_18",
        "set_19",
        "set_20",
        "set_21",
        "set_22",
        "set_23",
        "set_24",
        "set_25",
        "set_26",
        "set_27",
        "set_28",
        "set_29",
        "set_30",
        "set_31",
        ),
    Bool32("loaded_cinematic_zonesets",
        "set_0",
        "set_1",
        "set_2",
        "set_3",
        "set_4",
        "set_5",
        "set_6",
        "set_7",
        "set_8",
        "set_9",
        "set_10",
        "set_11",
        "set_12",
        "set_13",
        "set_14",
        "set_15",
        "set_16",
        "set_17",
        "set_18",
        "set_19",
        "set_20",
        "set_21",
        "set_22",
        "set_23",
        "set_24",
        "set_25",
        "set_26",
        "set_27",
        "set_28",
        "set_29",
        "set_30",
        "set_31",
        ),
    SInt32("bsp_atlas_index"),
    ENDIAN=">", SIZE=36
    )


zone_scenario_bsp = Struct("scenario_bsps",
    dependency("bsp"),
    ENDIAN=">", SIZE=16
    )


zone_unknown_4 = Struct("unknown_4",
    Pad(20),
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


zone_prediction_d_tag = Struct("prediction_d_tags",
    SInt16("c_count"),
    SInt16("c_index"),
    SInt16("a_count"),
    SInt16("a_index"),
    ENDIAN=">", SIZE=8
    )


zone_prediction_d2_tag = Struct("prediction_d2_tags",
    UInt32("tag"),
    SInt32("first_value"),
    SInt32("second_value"),
    ENDIAN=">", SIZE=12
    )


zone_meta_def = BlockDef("zone",
    SEnum16("map_type", *zone_map_type),
    SInt16("flags"),
    reflexive("resource_types", zone_resource_type),
    reflexive("resource_structure_types", zone_resource_structure_type),
    reflexive("compression_codecs", zone_compression_codec),
    reflexive("external_cache_references", zone_external_cache_reference),
    reflexive("raw_pages", zone_raw_page),
    reflexive("sizes", zone_size),
    reflexive("segments", zone_segment),
    reflexive("tag_resources", zone_tag_resource),
    reflexive("designer_zonesets", zone_designer_zoneset),
    reflexive("global_zoneset", zone_global_zoneset),
    Pad(12),
    reflexive("unattached_zoneset", zone_unattached_zoneset),
    reflexive("disc_forbidden_zoneset", zone_disc_forbidden_zoneset),
    reflexive("disc_always_streaming_zoneset", zone_disc_always_streaming_zoneset),
    reflexive("bsp_zonesets", zone_bsp_zoneset),
    reflexive("bsp_zonesets_2", zone_bsp_zonesets_2),
    reflexive("bsp_zonesets_3", zone_bsp_zonesets_3),
    reflexive("cinematic_zonesets", zone_cinematic_zoneset),
    reflexive("scenario_zonesets", zone_scenario_zoneset),
    Pad(24),
    reflexive("scenario_zoneset_groups", zone_scenario_zoneset_group),
    reflexive("scenario_bsps", zone_scenario_bsp),
    Pad(36),
    rawdata_ref("fixup_information"),
    Pad(20),
    reflexive("unknown_4", zone_unknown_4),
    Pad(96),
    reflexive("prediction_a", zone_prediction_a),
    reflexive("prediction_b", zone_prediction_b),
    reflexive("prediction_c", zone_prediction_c),
    reflexive("prediction_d_tags", zone_prediction_d_tag),
    reflexive("prediction_d2_tags", zone_prediction_d2_tag),
    SInt32("campaign_id"),
    SInt32("map_id"),
    TYPE=Struct, ENDIAN=">", SIZE=532
    )