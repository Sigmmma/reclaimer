import math
import os
import re
import traceback

from copy import deepcopy
from reclaimer.common_descs import anim_types, anim_frame_info_types
from reclaimer.model.jms import JmsNode, JmsModel
from reclaimer.util import float_to_str
from reclaimer.util.matrices import clip_angle_to_bounds, are_vectors_equal,\
     quat_to_matrix, matrix_to_quat, axis_angle_to_quat, quat_to_axis_angle,\
     quaternion_to_euler, euler_to_quaternion, Quaternion, multiply_quaternions


JMA_ANIMATION_EXTENSIONS = (
    ".jma", ".jmm", ".jmo", ".jmr", ".jmt", ".jmw", ".jmz", 
    )


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
)""" % (self.dx, self.dy, self.dz, self.dyaw,
        self.x, self.y, self.z, self.yaw)

    def __eq__(self, other):
        if not isinstance(other, JmaRootNodeState):
            return False
        elif (abs(self.dx - other.dx) > 0.0000000001 or
              abs(self.dy - other.dy) > 0.0000000001 or
              abs(self.dz - other.dz) > 0.0000000001 or
              abs(self.dyaw - other.dyaw) > 0.0000000001):
            return False
        return True


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

    rot_flags_int   = 0
    trans_flags_int = 0
    scale_flags_int = 0

    root_node_info_applied = True

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
        self.actors = actors if actors else ["unnamedActor"]

    def add_frame(self, new_frame):
        assert len(new_frame) == len(self.nodes)
        for node_frame in new_frame:
            assert isinstance(node_frame, JmaNodeState)

        self.frames.append(new_frame)

    @property
    def ext(self):
        return get_anim_ext(self.anim_type, self.frame_info_type,
                            self.world_relative)

    @property
    def has_dxdy(self): return "dx"   in self.frame_info_type
    @property
    def has_dz(self):   return "dz"   in self.frame_info_type
    @property
    def has_dyaw(self): return "dyaw" in self.frame_info_type

    @property
    def actor_count(self): return len(self.actors)
    @property
    def frame_count(self): return len(self.frames)
    @property
    def node_count(self): return len(self.nodes)

    @property
    def last_frame_loops_to_first(self):
        return self.anim_type != "overlay"

    @property
    def trans_flags(self):
        return [bool(self.trans_flags_int & (1 << i))
                for i in range(self.node_count)]

    @property
    def rot_flags(self):
        return [bool(self.rot_flags_int & (1 << i))
                for i in range(self.node_count)]

    @property
    def scale_flags(self):
        return [bool(self.scale_flags_int & (1 << i))
                for i in range(self.node_count)]

    @property
    def root_node_info_frame_size(self):
        if self.has_dz:
            return 16
        elif self.has_dyaw:
            return 12
        elif self.has_dxdy:
            return 8
        return 0

    @property
    def frame_data_frame_size(self):
        return (12 * sum(self.trans_flags) +
                8  * sum(self.rot_flags) +
                4  * sum(self.scale_flags))

    @property
    def default_data_size(self):
        return self.node_count * 24 - self.frame_data_frame_size

    def apply_root_node_info_to_states(self, undo=False):
        if self.root_node_info_applied == (not undo):
            # do nothing if the root node info is already applied
            # and we are being told to apply it, or its not applied
            # and we are being told to undo its application.
            return

        if self.has_dxdy or self.has_dz or self.has_dyaw:
            delta = -1 if undo else 1
            for f in range(self.frame_count):
                # apply the total change in the root nodes
                # frame_info for this frame to the frame_data
                node_info = self.root_node_info[f]
                node_state = self.frames[f][0]

                q0 = Quaternion(euler_to_quaternion(
                    0, 0, -node_info.yaw * delta)).normalized
                q1 = Quaternion((node_state.rot_i, node_state.rot_j,
                                 node_state.rot_k, node_state.rot_w)).normalized

                i, j, k, w = Quaternion(multiply_quaternions(q0, q1)).normalized

                #print([v * 180 / pi for v in quaternion_to_euler(*q0)])
                #print([v * 180 / pi for v in quaternion_to_euler(*q1)])
                #print([v * 180 / pi for v in quaternion_to_euler(i, j, k, w)])
                #print(node_info.yaw)

                node_state.pos_x += node_info.x * delta
                node_state.pos_y += node_info.y * delta
                node_state.pos_z += node_info.z * delta
                node_state.rot_i = i
                node_state.rot_j = j
                node_state.rot_k = k
                node_state.rot_w = w

        self.root_node_info_applied = not undo

    def calculate_root_node_info(self):
        self.root_node_info = []

        has_dxdy, has_dz, has_dyaw = self.has_dxdy, self.has_dz, self.has_dyaw

        dx = dy = dz = dyaw = x = y = z = yaw = 0.0
        frame_count = self.frame_count
        for f in range(frame_count):
            node_state0 = self.frames[f][0]
            node_state1 = self.frames[(f + 1) % frame_count][0]
            if has_dxdy:
                dx = node_state1.pos_x - node_state0.pos_x
                dy = node_state1.pos_y - node_state0.pos_y

            if has_dz:
                dz = node_state1.pos_z - node_state0.pos_z

            if has_dyaw:
                q0 = (node_state0.rot_i, node_state0.rot_j,
                      node_state0.rot_k, node_state0.rot_w)
                q1 = (node_state1.rot_i, node_state1.rot_j,
                      node_state1.rot_k, node_state1.rot_w)
                m0 = quat_to_matrix(*q0)
                m1 = quat_to_matrix(*q1)

                ex, ey, ez = quaternion_to_euler(*matrix_to_quat(m0 / m1))
                #print(round(ex*ea, 5), round(ey*ea, 5), round(ez*ea, 5))
                dyaw = clip_angle_to_bounds(ez)

                # STRIP YAW FROM ROTATION AND FIGURE OUT IF IT NEEDS
                # TO BE APPLIED BEFORE OR AFTER FRAME DATA ROTATION.
                # LOOK AT ANIMATION IMPORTER TO CONFIRM ORDER
                #print(quaternion_to_euler(*matrix_to_quat(m0 / m1)))
                #print(quaternion_to_euler(*matrix_to_quat(m1 / m0)))
                #print(quaternion_to_euler(*matrix_to_quat(m0 * m1)))
                #print(quaternion_to_euler(*matrix_to_quat(m1 * m0)))

            if f + 1 == frame_count:
                dx = dy = dz = dyaw = 0.0

            self.root_node_info.append(
                JmaRootNodeState(dx, dy, dz, dyaw, x, y, z, yaw)
                )
            x += dx
            y += dy
            z += dz
            yaw += dyaw

    verify_nodes_valid = JmsModel.verify_nodes_valid

    def calculate_animation_flags(self, tolerance=None):
        if tolerance is None:
            tolerance = 0

        self.rot_flags_int = 0
        self.trans_flags_int = 0
        self.scale_flags_int = 0
        if len(self.frames) < 2:
            return

        f0 = self.frames[0]

        zero = (0, 0, 0, 0)
        # determine which transforms types of each node are animated
        # by seeing how much they change from the starting frame
        for node_states in self.frames[1: ]:
            for n in range(len(node_states)):
                diff = node_states[n] - f0[n]
                if not are_vectors_equal(
                        (diff.rot_i, diff.rot_j, diff.rot_k, diff.rot_w),
                        zero, False, tolerance):
                    self.rot_flags_int |= (1 << n)

                if not are_vectors_equal(
                        (diff.pos_x, diff.pos_y, diff.pos_z),
                        zero, False, tolerance):
                    self.trans_flags_int |= (1 << n)

                if not are_vectors_equal(
                        (diff.scale, ),
                        zero, False, tolerance):
                    self.scale_flags_int |= (1 << n)

    def verify_animations_match(self, other_jma):
        errors = list(other_jma.verify_jma())
        if len(other_jma.nodes) != len(self.nodes):
            errors.append("Node counts do not match.")
            return errors

        for i in range(len(self.nodes)):
            if not self.nodes[i].is_node_hierarchy_equal(other_jma.nodes[i]):
                errors.append("Nodes '%s' do not match." % i)

        return errors

    def verify_jma(self):
        crc = self.node_list_checksum
        node_error = False
        node_ct = len(self.nodes)

        errors = self.verify_nodes_valid()
        if errors:
            return errors

        for frame in self.frames:
            if len(frame) != node_ct:
                errors.append("Invalid node state count for frame(s).")
                break

        return errors


class JmaAnimationSet:
    node_list_checksum = 0
    nodes = ()
    animations = ()

    def __init__(self, *jma_animations):
        self.nodes = []
        self.animations = {}

        for jma_animation in jma_animations:
            self.merge_jma_animation(jma_animation)

    verify_animations_match = JmaAnimation.verify_animations_match

    def merge_jma_animation(self, other_jma):
        assert isinstance(other_jma, JmaAnimation)

        if not other_jma:
            return

        if not self.nodes:
            self.node_list_checksum = other_jma.node_list_checksum
            self.nodes = []
            for node in other_jma.nodes:
                self.nodes.append(
                    JmsNode(
                        node.name, node.first_child, node.sibling_index,
                        node.rot_i, node.rot_j, node.rot_k, node.rot_w,
                        node.pos_x, node.pos_y, node.pos_z, node.parent_index)
                    )

        errors = self.verify_animations_match(other_jma)
        if errors:
            return errors

        self.animations[other_jma.name] = other_jma

        return errors


def read_jma(jma_string, stop_at="", anim_name=""):
    if anim_name is None:
        anim_name = "__unnamed"

    anim_name, ext = os.path.splitext(anim_name)
    anim_type, frame_info_type, world_relative = get_anim_types(ext)

    jma_anim = JmaAnimation(anim_name, 0, anim_type,
                            frame_info_type, world_relative)
    jma_string = jma_string.replace("\n", "\t")

    data = tuple(d for d in jma_string.split("\t") if d)
    dat_i = 0

    if data[dat_i] != "16392":
        print("JMA identifier '16392' not found.")
        return jma_anim

    dat_i += 1

    try:
        frame_count = int(data[dat_i]) & 0xFFffFFff
        dat_i += 1
    except Exception:
        print(traceback.format_exc())
        print("Could not read frame count.")
        return jma_anim

    try:
        frame_rate = int(data[dat_i]) & 0xFFffFFff
        dat_i += 1
    except Exception:
        print(traceback.format_exc())
        print("Could not frame rate.")
        return jma_anim

    if stop_at == "actors": return jma_anim

    # read the actors
    try:
        i = 0 # make sure i is defined in case of exception
        jma_anim.actors = [None] * (int(data[dat_i]) & 0xFFffFFff)
        dat_i += 1
        for i in range(len(jma_anim.actors)):
            jma_anim.actors[i] = data[dat_i]
            dat_i += 1
    except Exception:
        print(traceback.format_exc())
        print("Failed to read actors.")
        del jma_anim.actors[i: ]
        return jma_anim

    try:
        node_count = int(data[dat_i]) & 0xFFffFFff
        dat_i += 1
    except Exception:
        print(traceback.format_exc())
        print("Could not node count.")
        return jma_anim

    if stop_at == "checksum": return jma_anim

    try:
        node_list_checksum = int(data[dat_i]) & 0xFFffFFff
        if node_list_checksum >= (1<<31):
            node_list_checksum = node_list_checksum - 0x100000000
        jma_anim.node_list_checksum = node_list_checksum
        dat_i += 1
    except Exception:
        print(traceback.format_exc())
        print("Could not read node list checksum.")
        return jma_anim

    if stop_at == "nodes": return jma_anim

    # read the nodes
    try:
        i = 0 # make sure i is defined in case of exception
        jma_anim.nodes = [None] * node_count
        for i in range(node_count):
            jma_anim.nodes[i] = JmsNode(
                data[dat_i], int(data[dat_i+1]), int(data[dat_i+2])
                )
            dat_i += 3
        JmsNode.setup_node_hierarchy(jma_anim.nodes)
    except Exception:
        print(traceback.format_exc())
        print("Failed to read nodes.")
        del jma_anim.nodes[i: ]
        return jma_anim


    if stop_at == "frames": return jma_anim

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
            jma_anim.frames.append(frame)
    except Exception:
        print(traceback.format_exc())
        print("Failed to read frames.")
        del jma_anim.frames[i: ]
        return jma_anim

    jma_anim.calculate_root_node_info()
    jma_anim.apply_root_node_info_to_states(True)
    jma_anim.calculate_animation_flags()
    return jma_anim


def write_jma(filepath, jma_anim):
    # If the path doesnt exist, create it
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))

    if not jma_anim.root_node_info_applied:
        jma_anim = deepcopy(jma_anim)
        jma_anim.apply_root_node_info_to_states()

    with open(filepath, "w", encoding='latin1') as f:
        f.write("16392\n")  # version number
        f.write("%s\n" % jma_anim.frame_count)
        f.write("%s\n" % jma_anim.frame_rate)

        f.write("%s\n" % jma_anim.actor_count)
        for actor_name in jma_anim.actors:
            f.write("%s\n" % actor_name)

        f.write("%s\n" % jma_anim.node_count)
        f.write("%s\n" % (int(jma_anim.node_list_checksum) & 0xFFffFFff))

        for node in jma_anim.nodes:
            f.write("%s\n%s\t%s\n" %
                (node.name[: 31], node.first_child, node.sibling_index)
            )

        for frame in jma_anim.frames:
            for nf in frame:
                f.write("%s\t%s\t%s\n%s\t%s\t%s\t%s\n%s\n" % (
                    float_to_str(nf.pos_x),
                    float_to_str(nf.pos_y),
                    float_to_str(nf.pos_z),
                    float_to_str(nf.rot_i),
                    float_to_str(nf.rot_j),
                    float_to_str(nf.rot_k),
                    float_to_str(nf.rot_w),
                    float_to_str(nf.scale))
                )

#jma_file = open(r'C:\Users\Moses\Desktop\halo\data\characters\cyborg\animations\alert unarmed turn-right.jmt', 'r')
#data = read_jma(jma_file.read(), "", "alert unarmed turn-right.jmt")
