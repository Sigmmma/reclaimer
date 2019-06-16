import math
import os
import re
import traceback

from copy import deepcopy
from reclaimer.hek.defs.objs.matrices import quat_to_axis_angle,\
     clip_angle_to_bounds
from reclaimer.util import float_to_str
from reclaimer.common_descs import anim_types, anim_frame_info_types
from reclaimer.model.jms import JmsNode


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


class JmaRootNodeState:
    __slots__ = (
        "dx", "dy", "dz", "dyaw",
        "x", "y", "z", "yaw",
        )
    def __init__(self, dx=0.0, dy=0.0, dz=0.0, dyaw=0.0,
                 x=0.0, y=0.0, z=0.0, yaw=0.0):
        self.dx, self.dy, self.dz, self.dyaw = dx, dy, dz, dyaw
        self.x,  self.y,  self.z,  self.yaw  =  x,  y,  z,  yaw

    def __repr__(self):
        return """JmaRootNodeState(
    dx=%s, dy=%s, dz=%s, dyaw=%s,
    x=%s, y=%s, z=%s, yaw=%s,
)""" % (self.x, self.y, self.z, self.yaw)

    def __eq__(self, other):
        if not isinstance(other, JmaRootNodeState):
            return False
        elif (abs(self.dx - other.dx) > 0.0000000001 or
              abs(self.dy - other.dy) > 0.0000000001 or
              abs(self.dz - other.dz) > 0.0000000001 or
              abs(self.dyaw - other.dyaw) > 0.0000000001):
            return False
        return True

    def __sub__(self, other):
        if not isinstance(other, JmaRootNodeState):
            raise TypeError("Cannot subtract %s from %s" %
                            (type(other), type(self)))
        return JmaRootNodeState(
            self.dx - other.dx, self.dy - other.dy,
            self.dz - other.dz, self.dyaw - other.dyaw,
            other.x, other.y, other.z, other.yaw
            )


class JmaNodeState:
    __slots__ = (
        "pos_x", "pos_y", "pos_z",
        "rot_i", "rot_j", "rot_k", "rot_w",
        "scale",
        )
    def __init__(self, pos_x=0.0, pos_y=0.0, pos_z=0.0,
                 rot_i=0.0, rot_j=0.0, rot_k=0.0, rot_w=1.0, scale=1.0):
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
    x=%s, y=%s, z=%s,
    i=%s, j=%s, k=%s, w=%s,
    scale=%s
)""" % (self.pos_x, self.pos_y, self.pos_z,
        self.rot_i, self.rot_j, self.rot_k, self.rot_w,
        self.scale)

    def __eq__(self, other):
        if not isinstance(other, JmaNodeState):
            return False
        elif (abs(self.rot_i - other.rot_i) > 0.000001 or
              abs(self.rot_j - other.rot_j) > 0.000001 or
              abs(self.rot_k - other.rot_k) > 0.000001 or
              abs(self.rot_w - other.rot_w) > 0.000001):
            return False
        elif (abs(self.pos_x - other.pos_x) > 0.000001 or
              abs(self.pos_y - other.pos_y) > 0.000001 or
              abs(self.pos_z - other.pos_z) > 0.000001):
            return False
        elif abs(self.scale - other.scale) > 0.000001:
            return False
        return True

    def __sub__(self, other):
        if not isinstance(other, JmaNodeState):
            raise TypeError("Cannot subtract %s from %s" %
                            (type(other), type(self)))
        return JmaNodeState(
            self.pos_x - other.pos_x, self.pos_y - other.pos_y,
            self.pos_z - other.pos_z, self.rot_i - other.rot_i,
            self.rot_j - other.rot_j, self.rot_k - other.rot_k,
            self.rot_w - other.rot_w, self.scale - other.scale,
            )


class JmaAnimation:
    name = ""
    node_list_checksum = 0
    nodes = ()
    frames = ()

    root_node_info = ()

    frame_rate = 30
    actors = ()

    world_relative = False

    rot_flags   = ()
    trans_flags = ()
    scale_flags = ()

    anim_type = anim_types[0]
    frame_info_type = anim_frame_info_types[0]

    def __init__(self, name="", node_list_checksum=0,
                 anim_type="", frame_info_type="", world_relative=False,
                 nodes=None, frames=None, actors=None, frame_rate=30):

        name = name.strip(" ")

        node_list_checksum = node_list_checksum & 0xFFffFFff
        if node_list_checksum >= (1<<31):
            node_list_checksum = node_list_checksum - 0x100000000

        self.name = name
        self.node_list_checksum = node_list_checksum
        self.nodes  = nodes  if nodes  else []
        self.frames = frames if frames else []
        self.world_relative = bool(world_relative)
        self.anim_type = anim_type
        self.frame_info_type = frame_info_type
        self.frame_rate = frame_rate
        self.actors = actors if actors else []

        self.calculate_animation_flags()

    def add_frame(self, new_frame):
        assert len(new_frame) == len(self.nodes)
        for node_frame in new_frame:
            assert isinstance(node_frame, JmaNodeState)

        self.frames.append(new_frame)

    @property
    def last_frame_loops_to_first(self):
        return self.anim_type != "overlay"

    @property
    def rot_flags_int(self):
        return sum((1 << i) * bool(self.rot_flags[i])
                   for i in range(len(self.rot_flags)))

    @property
    def trans_flags_int(self):
        return sum((1 << i) * bool(self.trans_flags[i])
                   for i in range(len(self.trans_flags)))

    @property
    def scale_flags_int(self):
        return sum((1 << i) * bool(self.scale_flags[i])
                   for i in range(len(self.scale_flags)))

    def calculate_animation_flags(self):
        self.rot_flags   = [False] * len(self.nodes)
        self.trans_flags = [False] * len(self.nodes)
        self.scale_flags = [False] * len(self.nodes)
        if len(self.frames) < 2:
            return

        f0 = self.frames[0]

        for node_states in self.frames[1: ]:
            for n in range(len(node_states)):
                diff = node_states[n] - f0[n]
                if (diff.rot_i != 0 or diff.rot_j != 0 or
                    diff.rot_k != 0 or diff.rot_w != 0):
                    self.rot_flags[n] = True

                if diff.pos_x != 0 or diff.pos_y != 0 or diff.pos_z != 0:
                    self.trans_flags[n] = True

                if diff.scale != 0:
                    self.scale_flags[n] = True

    def calculate_root_node_info(self):
        self.root_node_info = [JmaRootNodeState()]

        has_dxdy = "dx" in self.frame_info_type
        has_dz   = "dz" in self.frame_info_type
        has_dyaw = "dyaw" in self.frame_info_type

        dx = dy = dz = dyaw = 0.0
        x = y = z = yaw = 0
        for f in range(anim.frame_count):
            node_state = self.frames[f][0]
            if has_dxdy:
                dx, dy = node_state.pos_x - x,  node_state.pos_y - y
                x, y = node_state.pos_x, node_state.pos_y

            if has_dz:
                dz = node_state.pos_z - z
                z = node_state.pos_z

            if has_dyaw:
                ex, ey, ez, ea = quat_to_axis_angle(
                    node_state.i, node_state.j, node_state.k, node_state.w)
                next_yaw = ex * (-ea)
                dyaw = clip_angle_to_bounds(next_yaw - yaw)
                yaw = next_yaw

            node_info = self.root_node_info[f]
            self.root_node_info.append(
                JmaRootNodeState(
                    dx, dy, dz, dyaw,
                    node_info.dx + dx, node_info.dy + dy,
                    node_info.dz + dz, node_info.dyaw + dyaw
                    )
                )

    def apply_frame_info_to_states(self, undo=False):
        delta = -1 if undo else 1
        for f in range(self.frame_count):
            # apply the total change in the root nodes
            # frame_info for this frame to the frame_data
            node_info = self.root_node_info[f]
            node_state = self.frames[f][0]

            i, j, k, w = multiply_quaternions(
                axis_angle_to_quat(1, 0, 0, delta * (-node_info.yaw)),
                (node_state.rot_i, node_state.rot_j,
                 node_state.rot_k, node_state.rot_w),
                )

            node_state.pos_x += node_info.x * delta
            node_state.pos_y += node_info.y * delta
            node_state.pos_z += node_info.z * delta
            node_state.rot_i = i
            node_state.rot_j = j
            node_state.rot_k = k
            node_state.rot_w = w


class JmaAnimationSet:
    name = ""
    node_list_checksum = 0
    nodes = ()
    animations = ()

    def __init__(self, name="", node_list_checksum=0,
                 nodes=None, animations=None):
        name = name.strip(" ")

        node_list_checksum = node_list_checksum & 0xFFffFFff
        if node_list_checksum >= (1<<31):
            node_list_checksum = node_list_checksum - 0x100000000

        self.name = name
        self.node_list_checksum = node_list_checksum
        self.nodes      = nodes      if nodes      else []
        self.animations = animations if animations else []


def read_jma(jma_string, stop_at="", anim_name=""):
    if anim_name is None:
        anim_name = "__unnamed"

    anim_name, ext = os.path.splitext(anim_name)
    anim_type, frame_info_type, world_relative = get_anim_types(ext)

    jma_data = JmaAnimation(anim_name, 0, anim_type,
                            frame_info_type, world_relative)
    jma_string = jma_string.replace("\n", "\t")

    data = tuple(d for d in jma_string.split("\t") if d)
    dat_i = 0

    if data[dat_i] != "16392":
        print("JMA identifier '16392' not found.")
        return jma_data

    dat_i += 1

    try:
        frame_count = int(data[dat_i]) & 0xFFffFFff
        dat_i += 1
    except Exception:
        print(traceback.format_exc())
        print("Could not read frame count.")
        return jma_data

    try:
        frame_rate = int(data[dat_i]) & 0xFFffFFff
        dat_i += 1
    except Exception:
        print(traceback.format_exc())
        print("Could not frame rate.")
        return jma_data

    if stop_at == "actors": return jma_data

    # read the actors
    try:
        i = 0 # make sure i is defined in case of exception
        jma_data.actors = [None] * (int(data[dat_i]) & 0xFFffFFff)
        dat_i += 1
        for i in range(len(jma_data.actors)):
            jma_data.actors[i] = data[dat_i]
            dat_i += 1
    except Exception:
        print(traceback.format_exc())
        print("Failed to read actors.")
        del jma_data.actors[i: ]
        return jma_data

    try:
        node_count = int(data[dat_i]) & 0xFFffFFff
        dat_i += 1
    except Exception:
        print(traceback.format_exc())
        print("Could not node count.")
        return jma_data

    if stop_at == "checksum": return jma_data

    try:
        node_list_checksum = int(data[dat_i]) & 0xFFffFFff
        if node_list_checksum >= (1<<31):
            node_list_checksum = node_list_checksum - 0x100000000
        jma_data.node_list_checksum = node_list_checksum
        dat_i += 1
    except Exception:
        print(traceback.format_exc())
        print("Could not read node list checksum.")
        return jma_data

    if stop_at == "nodes": return jma_data

    # read the nodes
    try:
        i = 0 # make sure i is defined in case of exception
        jma_data.nodes = [None] * node_count
        for i in range(node_count):
            jma_data.nodes[i] = JmsNode(
                data[dat_i], int(data[dat_i+1]), int(data[dat_i+2])
                )
            dat_i += 3
        JmsNode.setup_node_hierarchy(jma_data.nodes)
    except Exception:
        print(traceback.format_exc())
        print("Failed to read nodes.")
        del jma_data.nodes[i: ]
        return jma_data


    # read the frame data
    try:
        i = 0 # make sure i is defined in case of exception
        for i in range(frame_count):
            frame = [None] * node_count
            for j in range(node_count):
                frame[j] = JmaNodeState(
                    float(data[dat_i]),   float(data[dat_i+1]),
                    float(data[dat_i+2]), float(data[dat_i+3]),
                    float(data[dat_i+4]), float(data[dat_i+5]),
                    float(data[dat_i+6]), float(data[dat_i+7])
                    )
                dat_i += 8
            jma_data.frames.append(frame)
    except Exception:
        print(traceback.format_exc())
        print("Failed to read frames.")
        del jma_data.frames[i: ]
        return jma_data

    return jma_data


def write_jma(filepath, jma_data):
    # If the path doesnt exist, create it
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))

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

#jma_file = open(r'C:\Users\Moses\Desktop\halo\data\characters\cyborg\animations\alert unarmed turn-right.jmt', 'r')
#data = read_jma(jma_file.read(), "", "alert unarmed turn-right.jmt")
