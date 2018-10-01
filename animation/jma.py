import math
import re
import traceback

from os import makedirs
from os.path import dirname, exists
from reclaimer.util import float_to_str
from reclaimer.common_descs import anim_types, anim_frame_info_types


def get_anim_ext(anim_type, frame_info_type, world_relative=False):
    anim_type = anim_type.lower()
    frame_info_type = frame_info_type.lower()
    if anim_type == "replacement":
        return ".jmr"
    elif anim_type == "overlay":
        return ".jmo"
    elif "dz" in frame_info_type:
        return ".jmz"
    elif "dyaw" in frame_info_type:
        return ".jmt"
    elif "dx" in frame_info_type and "dy" in frame_info_type:
        return ".jma"
    elif world_relative:
        return ".jmw"
    else:
        return ".jmm"


def get_anim_types(anim_ext):
    anim_ext = anim_ext.lower()
    if "jmr" in anim_ext:
        return anim_types[2], anim_frame_info_types[1], False
    elif "jmo" in anim_ext:
        return anim_types[1], anim_frame_info_types[0], False
    elif "jmz" in anim_ext:
        return anim_types[0], anim_frame_info_types[3], False
    elif "jmt" in anim_ext:
        return anim_types[0], anim_frame_info_types[2], False
    elif "jma" in anim_ext:
        return anim_types[0], anim_frame_info_types[1], False
    else:
        return anim_types[0], anim_frame_info_types[0], "jmw" in anim_ext


class JmaNode:
    __slots__ = ("name", "first_child", "sibling_index", "parent_node")

    def __init__(self, name="", first_child=-1, sibling_index=-1,
                 parent_node=-1):
        self.name = name
        self.sibling_index = sibling_index
        self.first_child = first_child
        self.parent_node = parent_node

    def __repr__(self):
        return """JmaNode(name=%s,
    first_child=%s, sibling_index=%s, parent_node=%s
)""" % (self.name, self.first_child, self.sibling_index, self.parent_node)

    def __eq__(self, other):
        if not isinstance(other, JmaNode):
            return False
        elif self.name != other.name:
            return False
        elif self.first_child != other.first_child:
            return False
        elif self.sibling_index != other.sibling_index:
            return False
        elif self.parent_node != other.parent_node:
            return False
        return True


class JmaNodeState:
    __slots__ = (
        "rot_i", "rot_j", "rot_k", "rot_w",
        "pos_x", "pos_y", "pos_z", "scale",
        )
    def __init__(self, rot_i=0.0, rot_j=0.0, rot_k=0.0, rot_w=1.0,
                 pos_x=0.0, pos_y=0.0, pos_z=0.0, scale=1.0):
        self.rot_i = rot_i
        self.rot_j = rot_j
        self.rot_k = rot_k
        self.rot_w = rot_w
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.scale = scale

    def __repr__(self):
        return """JmaNodeState(
    i=%s, j=%s, k=%s, w=%s,
    x=%s, y=%s, z=%s,
    scale=%s
)""" % (self.rot_i, self.rot_j, self.rot_k, self.rot_w,
        self.pos_x, self.pos_y, self.pos_z, self.scale)

    def __eq__(self, other):
        if (abs(self.rot_i - other.rot_i) > 0.00001 or
              abs(self.rot_j - other.rot_j) > 0.00001 or
              abs(self.rot_k - other.rot_k) > 0.00001 or
              abs(self.rot_w - other.rot_w) > 0.00001):
            return False
        elif (abs(self.pos_x - other.pos_x) > 0.00001 or
              abs(self.pos_y - other.pos_y) > 0.00001 or
              abs(self.pos_z - other.pos_z) > 0.00001):
            return False
        elif abs(self.scale - other.scale) > 0.00001:
            return False
        return True


class JmaAnimation:
    name = ""
    node_list_checksum = 0
    nodes = ()
    frames = ()
    world_relative = False

    anim_type = anim_types[0]
    frame_info_type = anim_frame_info_types[0]

    def __init__(self, name="", node_list_checksum=0,
                 anim_type="", frame_info_type="", world_relative=False,
                 nodes=None, frames=None):

        name = name.strip(" ")

        node_list_checksum = node_list_checksum & 0xFFffFFff
        if node_list_checksum >= (1<<31):
            node_list_checksum = node_list_checksum - 0x100000000

        self.name = name
        self.node_list_checksum = node_list_checksum
        self.nodes  = nodes  if nodes  else []
        self.frames = frames if frames else []
        self.world_relative = world_relative
        self.anim_type = anim_type
        self.frame_info_type = frame_info_type

    def add_frame(self, new_frame):
        assert len(new_frame) == len(self.nodes)
        for node_frame in new_frame:
            assert isinstance(node_frame, JmaNodeState)

        self.frames.append(new_frame)


def write_jma(filepath, jma_data):
    # If the path doesnt exist, create it
    if not exists(dirname(filepath)):
        makedirs(dirname(filepath))

    with open(filepath, "w", encoding='latin1') as f:
        f.write("16392\n")  # unknown constant
        f.write("%s\n" % len(jma_data.frames))
        f.write("30\n")  # I'm guessing this is the frame-rate?
        f.write("1\n")   # And maybe this is the number of "actors"?
        f.write("unnamedActor\n")
        f.write("%s\n" % len(jma_data.nodes))
        f.write("%s\n" % (int(jma_data.node_list_checksum) & 0xFFffFFff))

        for node in jma_data.nodes:
            f.write("%s\n%s\t%s\n" %
                (node.name[: 31], node.first_child, node.sibling_index)
            )

        for frame in jma_data.frames:
            for nf in frame:
                f.write("%s\t%s\t%s\n%s\t%s\t%s\t%s\n%s\n" % (
                    float_to_str(nf.pos_x * 100),
                    float_to_str(nf.pos_y * 100),
                    float_to_str(nf.pos_z * 100),
                    float_to_str(nf.rot_i),
                    float_to_str(nf.rot_j),
                    float_to_str(nf.rot_k),
                    float_to_str(nf.rot_w),
                    float_to_str(nf.scale))
                )
