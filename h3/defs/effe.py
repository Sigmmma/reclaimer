############# Credits and version info #############
# Definition generated from Assembly XML tag def
#	 Date generated: 2018/12/03  04:56
#
# revision: 1		author: Assembly
# 	Generated plugin from scratch.
# revision: 2		author: -DeToX-
# 	Fixed some Reflexives..
# revision: 3		author: -DeToX-
# 	Named some values..
# revision: 4		author: Lord Zedd
# 	Enums, better names, etc.
# revision: 5		author: Moses_of_Egypt
# 	Cleaned up and converted to SuPyr definition
#
####################################################

from ..common_descs import *
from .objs.tag import *
from supyr_struct.defs.tag_def import TagDef

effe_event_part_camera_mode = (
    "independent_of_camera_mode",
    "first_person_only",
    "third_person_only",
    "both_first_and_third",
    )

effe_event_part_create_in_disposition = (
    "either_mode",
    "violent_mode_only",
    "nonviolent_mode_only",
    )

effe_event_part_create_in_environment = (
    "any_environment",
    "air_only",
    "water_only",
    "space_only",
    )

effe_event_particle_system_coordinate_system = (
    "world",
    "local",
    "ancestor",
    )


effe_location = Struct("location", 
    h3_string_id("marker_name"),
    SInt32("unknown", VISIBLE=False),
    Array("unknown_array", SUB_STRUCT=SInt8("unknown"), SIZE=4, VISIBLE=False),
    ENDIAN=">", SIZE=12
    )


effe_event_part = Struct("part", 
    SEnum16("create_in_environment", *effe_event_part_create_in_environment),
    SEnum16("create_in_disposition", *effe_event_part_create_in_disposition),
    SInt16("location_index"),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("unknown_1", VISIBLE=False),
    SInt8("unknown_2", VISIBLE=False),
    SEnum8("camera_mode", *effe_event_part_camera_mode),
    StrLatin1("anticipated_tag_class", SIZE=4),
    h3_dependency("spawned_tag"),
    QStruct("velocity_bounds", INCLUDE=from_to),
    BytesRaw("unknown_3", SIZE=8, VISIBLE=False),
    float_rad("velocity_cone_angle"),
    from_to_rad("angular_velocity_bounds"),
    QStruct("radius_modifier_bounds", INCLUDE=from_to),
    QStruct("origin_offset", INCLUDE=xyz_float),
    yp_float_rad("origin_rotation"),
    Bool32("a_scales_values", *unknown_flags_32),
    Bool32("b_scales_values", *unknown_flags_32),
    ENDIAN=">", SIZE=96
    )


effe_event_acceleration = Struct("acceleration", 
    SEnum16("create_in_environment", *effe_event_part_create_in_environment),
    SEnum16("create_in_disposition", *effe_event_part_create_in_disposition),
    SInt16("location_index"),
    SInt16("unknown", VISIBLE=False),
    Float("acceleration"),
    Float("inner_cone_angle"),
    Float("outer_cone_angle"),
    ENDIAN=">", SIZE=20
    )


effe_event_particle_system_emitter_unknown_21_unknown_1 = Struct("unknown_1", 
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    SInt8("input"),
    SInt8("input_range"),
    SEnum8("output_kind", *cntl_contrail_system_output_kind_0),
    SInt8("output"),
    h3_rawdata_ref("unknown_1"),
    BytesRaw("unknown_2", SIZE=8, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=36
    )


effe_event_particle_system_emitter_unknown_21 = Struct("unknown_21", 
    BytesRaw("unknown_0", SIZE=4, VISIBLE=False),
    h3_reflexive("unknown_1", effe_event_particle_system_emitter_unknown_21_unknown_1),
    BytesRaw("unknown_2", SIZE=8, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=24
    )


effe_event_particle_system_emitter_unknown_39 = Struct("unknown_39", 
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=4, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=16
    )


effe_event_particle_system_emitter_compiled_function = Struct("compiled_function", 
    Array("unknown_array", SUB_STRUCT=Float("unknown"), SIZE=16, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=64
    )


effe_event_particle_system_emitter_compiled_color_function = Struct("compiled_color_function", 
    color_rgb_float("color"),
    Float("magnitude"),
    ENDIAN=">", SIZE=16
    )


effe_event_particle_system_emitter = Struct("emitter", 
    h3_string_id("name"),
    Bool16("unknown_0", *unknown_flags_32),
    SInt16("unknown_1", VISIBLE=False),
    BytesRaw("unknown_2", SIZE=16, VISIBLE=False),
    SInt8("input_0"),
    SInt8("input_range_0"),
    SEnum8("output_kind_0", *cntl_contrail_system_output_kind_0),
    SInt8("output_0"),
    h3_rawdata_ref("unknown_3"),
    BytesRaw("unknown_4", SIZE=32, VISIBLE=False),
    SInt8("input_1"),
    SInt8("input_range_1"),
    SEnum8("output_kind_1", *cntl_contrail_system_output_kind_0),
    SInt8("output_1"),
    h3_rawdata_ref("unknown_5"),
    BytesRaw("unknown_6", SIZE=32, VISIBLE=False),
    SInt8("input_2"),
    SInt8("input_range_2"),
    SEnum8("output_kind_2", *cntl_contrail_system_output_kind_0),
    SInt8("output_2"),
    h3_rawdata_ref("unknown_7"),
    BytesRaw("unknown_8", SIZE=8, VISIBLE=False),
    SInt8("input_3"),
    SInt8("input_range_3"),
    SEnum8("output_kind_3", *cntl_contrail_system_output_kind_0),
    SInt8("output_3"),
    h3_rawdata_ref("unknown_9"),
    BytesRaw("unknown_10", SIZE=8, VISIBLE=False),
    SInt8("input_4"),
    SInt8("input_range_4"),
    SEnum8("output_kind_4", *cntl_contrail_system_output_kind_0),
    SInt8("output_4"),
    h3_rawdata_ref("unknown_11"),
    BytesRaw("unknown_12", SIZE=8, VISIBLE=False),
    SInt8("input_5"),
    SInt8("input_range_5"),
    SEnum8("output_kind_5", *cntl_contrail_system_output_kind_0),
    SInt8("output_5"),
    h3_rawdata_ref("unknown_13"),
    BytesRaw("unknown_14", SIZE=8, VISIBLE=False),
    SInt8("input_6"),
    SInt8("input_range_6"),
    SEnum8("output_kind_6", *cntl_contrail_system_output_kind_0),
    SInt8("output_6"),
    h3_rawdata_ref("unknown_15"),
    BytesRaw("unknown_16", SIZE=8, VISIBLE=False),
    SInt8("input_7"),
    SInt8("input_range_7"),
    SEnum8("output_kind_7", *cntl_contrail_system_output_kind_0),
    SInt8("output_7"),
    h3_rawdata_ref("unknown_17"),
    BytesRaw("unknown_18", SIZE=8, VISIBLE=False),
    SInt8("input_8"),
    SInt8("input_range_8"),
    SEnum8("output_kind_8", *cntl_contrail_system_output_kind_0),
    SInt8("output_8"),
    h3_rawdata_ref("unknown_19"),
    BytesRaw("unknown_20", SIZE=8, VISIBLE=False),
    h3_dependency("particle_physics"),
    Array("unknown_array", SUB_STRUCT=SInt8("unknown"), SIZE=4, VISIBLE=False),
    h3_reflexive("unknown_21", effe_event_particle_system_emitter_unknown_21),
    SInt8("input_9"),
    SInt8("input_range_9"),
    SEnum8("output_kind_9", *cntl_contrail_system_output_kind_0),
    SInt8("output_9"),
    h3_rawdata_ref("unknown_22"),
    BytesRaw("unknown_23", SIZE=32, VISIBLE=False),
    SInt8("input_10"),
    SInt8("input_range_10"),
    SEnum8("output_kind_10", *cntl_contrail_system_output_kind_0),
    SInt8("output_10"),
    h3_rawdata_ref("unknown_24"),
    BytesRaw("unknown_25", SIZE=8, VISIBLE=False),
    SInt8("input_11"),
    SInt8("input_range_11"),
    SEnum8("output_kind_11", *cntl_contrail_system_output_kind_0),
    SInt8("output_11"),
    h3_rawdata_ref("unknown_26"),
    BytesRaw("unknown_27", SIZE=8, VISIBLE=False),
    SInt8("input_12"),
    SInt8("input_range_12"),
    SEnum8("output_kind_12", *cntl_contrail_system_output_kind_0),
    SInt8("output_12"),
    h3_rawdata_ref("unknown_28"),
    BytesRaw("unknown_29", SIZE=8, VISIBLE=False),
    SInt8("input_13"),
    SInt8("input_range_13"),
    SEnum8("output_kind_13", *cntl_contrail_system_output_kind_0),
    SInt8("output_13"),
    h3_rawdata_ref("unknown_30"),
    BytesRaw("unknown_31", SIZE=8, VISIBLE=False),
    SInt8("input_14"),
    SInt8("input_range_14"),
    SEnum8("output_kind_14", *cntl_contrail_system_output_kind_0),
    SInt8("output_14"),
    h3_rawdata_ref("particle_scale"),
    BytesRaw("unknown_32", SIZE=8, VISIBLE=False),
    SInt8("input_15"),
    SInt8("input_range_15"),
    SEnum8("output_kind_15", *cntl_contrail_system_output_kind_0),
    SInt8("output_15"),
    h3_rawdata_ref("particle_tint"),
    BytesRaw("unknown_33", SIZE=8, VISIBLE=False),
    SInt8("input_16"),
    SInt8("input_range_16"),
    SEnum8("output_kind_16", *cntl_contrail_system_output_kind_0),
    SInt8("output_16"),
    h3_rawdata_ref("particle_alpha"),
    BytesRaw("unknown_34", SIZE=8, VISIBLE=False),
    SInt8("input_17"),
    SInt8("input_range_17"),
    SEnum8("output_kind_17", *cntl_contrail_system_output_kind_0),
    SInt8("output_17"),
    h3_rawdata_ref("particle_alpha_black_point"),
    BytesRaw("unknown_35", SIZE=8, VISIBLE=False),
    SInt32("unknown_36", VISIBLE=False),
    SInt32("unknown_37", VISIBLE=False),
    SInt32("unknown_38", VISIBLE=False),
    h3_reflexive("unknown_39", effe_event_particle_system_emitter_unknown_39),
    h3_reflexive("compiled_functions", effe_event_particle_system_emitter_compiled_function),
    h3_reflexive("compiled_color_functions", effe_event_particle_system_emitter_compiled_color_function),
    ENDIAN=">", SIZE=752
    )


effe_event_particle_system = Struct("particle_system", 
    Array("unknown_array_0", SUB_STRUCT=SInt8("unknown"), SIZE=4, VISIBLE=False),
    h3_dependency("particle"),
    SInt16("unknown_0", VISIBLE=False),
    SInt16("location_index"),
    SEnum16("coordinate_system", *effe_event_particle_system_coordinate_system),
    SEnum16("environment", *effe_event_part_create_in_environment),
    SEnum16("disposition", *effe_event_part_create_in_disposition),
    SEnum16("camera_mode", *effe_event_part_camera_mode),
    SInt16("sort_bias"),
    Bool16("flags", *unknown_flags_16),
    Array("unknown_array_1", SUB_STRUCT=Float("unknown"), SIZE=4, VISIBLE=False),
    BytesRaw("unknown_1", SIZE=4, VISIBLE=False),
    Float("unknown_2", VISIBLE=False),
    Float("amount_size"),
    Float("unknown_3", VISIBLE=False),
    Float("lod_in_distance"),
    Float("lod_feather_in_delta"),
    h3_reflexive("emitters", effe_event_particle_system_emitter),
    Float("unknown_4", VISIBLE=False),
    ENDIAN=">", SIZE=92
    )


effe_event = Struct("event", 
    h3_string_id("name"),
    SInt32("unknown", VISIBLE=False),
    Array("unknown_array", SUB_STRUCT=SInt8("unknown"), SIZE=4, VISIBLE=False),
    Float("skip_fraction"),
    QStruct("delay_bounds", INCLUDE=from_to),
    QStruct("duration_bounds", INCLUDE=from_to),
    h3_reflexive("parts", effe_event_part),
    h3_reflexive("accelerations", effe_event_acceleration),
    h3_reflexive("particle_systems", effe_event_particle_system),
    ENDIAN=">", SIZE=68
    )


effe_unknown_9 = Struct("unknown_9", 
    BytesRaw("unknown", SIZE=12, VISIBLE=False),
    VISIBLE=False,
    ENDIAN=">", SIZE=12
    )


effe_body = Struct("tagdata", 
    Bool32("flags", 
        ("dark_casings", 1 << 10),
        ),
    SInt32("unknown_0", VISIBLE=False),
    Float("unknown_1", VISIBLE=False),
    BytesRaw("unknown_2", SIZE=4, VISIBLE=False),
    Float("unknown_3", VISIBLE=False),
    Array("unknown_array", SUB_STRUCT=SInt8("unknown"), SIZE=4, VISIBLE=False),
    SInt16("loop_start_event"),
    SInt16("unknown_4", VISIBLE=False),
    BytesRaw("unknown_5", SIZE=4, VISIBLE=False),
    h3_reflexive("locations", effe_location),
    h3_reflexive("events", effe_event),
    h3_dependency("looping_sound"),
    SInt8("location_index"),
    SInt8("event_index"),
    SInt16("unknown_6", VISIBLE=False),
    Float("always_play_distance"),
    Float("never_play_distance"),
    Float("unknown_7", VISIBLE=False),
    Float("unknown_8", VISIBLE=False),
    h3_reflexive("unknown_9", effe_unknown_9),
    ENDIAN=">", SIZE=104
    )


def get():
    return effe_def

effe_def = TagDef("effe",
    h3_blam_header('effe'),
    effe_body,

    ext=".%s" % h3_tag_class_fcc_to_ext["effe"], endian=">", tag_cls=H3Tag
    )