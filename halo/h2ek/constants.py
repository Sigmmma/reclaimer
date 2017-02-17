from ..constants import *


# maps tag class four character codes(fccs) in
# their string encoding to their int encoding.
h2tag_class_fcc_to_be_int = {}
h2tag_class_fcc_to_le_int = {}
# maps tag class four character codes(fccs) in
# their int encoding to their string encoding.
h2tag_class_be_int_to_fcc = {}
h2tag_class_le_int_to_fcc = {}

# maps tag class four character codes to the tags file extension
h2tag_class_fcc_to_ext = {
    'ant!': "antenna",
    }

for tag_cls in h2tag_class_fcc_to_ext:
    h2tag_class_fcc_to_be_int[tag_cls] = fcc(tag_cls, 'big')
    h2tag_class_be_int_to_fcc[fcc(tag_cls, 'big')] = tag_cls
    h2tag_class_fcc_to_le_int[tag_cls] = fcc(tag_cls)
    h2tag_class_le_int_to_fcc[fcc(tag_cls)] = tag_cls
