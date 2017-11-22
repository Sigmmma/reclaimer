from ..constants import *

# maps tag class four character codes(fccs) in
# their string encoding to their int encoding.
sr_tag_class_fcc_to_be_int = {}
sr_tag_class_fcc_to_le_int = {}
# maps tag class four character codes(fccs) in
# their int encoding to their string encoding.
sr_tag_class_be_int_to_fcc = {}
sr_tag_class_le_int_to_fcc = {}


sr_tag_class_fcc_to_ext = dict(
    srac="shadowrun_actor",
    srud="shadowrun_unit",
    srwd="shadowrun_weapon",
    m1ed="magic_1_effect_data",
    m2ed="magic_2_effect_data",
    m3ed="magic_3_effect_data",
    t1ed="tech_1_effect_data",
    t2ed="tech_2_effect_data",
    t3ed="tech_3_effect_data",
    buym="buy_menu",
    **tag_class_fcc_to_ext
    )

for tag_cls in sr_tag_class_fcc_to_ext:
    sr_tag_class_fcc_to_be_int[tag_cls] = fcc(tag_cls)
    sr_tag_class_be_int_to_fcc[fcc(tag_cls)] = tag_cls
    sr_tag_class_fcc_to_le_int[tag_cls] = fcc(tag_cls)
    sr_tag_class_le_int_to_fcc[fcc(tag_cls)] = tag_cls
