#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

import math
import os
import re
import traceback

from copy import deepcopy
from pathlib import Path
from reclaimer.common_descs import anim_types, anim_frame_info_types
from reclaimer.model.jms import JmsNode, JmsModel
from reclaimer.util import float_to_str, float_to_str_truncate,\
     parse_jm_float, parse_jm_int
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
        return anim_types[2], anim_frame_info_types[0], False
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

    rot_keyframes = ()
    trans_keyframes = ()
    scale_keyframes = ()

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

        self.name = name.strip(" ")
        self.node_list_checksum = node_list_checksum
        self.nodes  = nodes  if nodes  else []
        self.frames = frames if frames else []
        self.world_relative = bool(world_relative)
        self.anim_type = anim_type
        self.frame_info_type = frame_info_type
        self.frame_rate = frame_rate
        self.actors = actors if actors else ["unnamedActor"]

        self.root_node_info = []
        self.setup_keyframes()

    def setup_keyframes(self):
        self.rot_keyframes   = [[] for i in range(self.node_count)]
        self.trans_keyframes = [[] for i in range(self.node_count)]
        self.scale_keyframes = [[] for i in range(self.node_count)]

    @property
    def has_keyframe_data(self):
        if not self.rot_keyframes or len(self.rot_keyframes) != self.node_count:
            return False
        elif not self.trans_keyframes or len(self.trans_keyframes) != self.node_count:
            return False
        elif not self.scale_keyframes or len(self.scale_keyframes) != self.node_count:
            return False
        return True

    @property
    def ext(self):
        return get_anim_ext(self.anim_type, self.frame_info_type,
                            self.world_relative)
    @property
    def has_dxdy(self): return "dx"   in self.frame_info_type
    @property
    def has_dyaw(self): return "dyaw" in self.frame_info_type
    @property
    def has_dz(self):   return "dz"   in self.frame_info_type

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

    def get_node_index(self, node_name):
        node_name = node_name.lower()
        i = 0
        for node in self.nodes:
            if node.name.lower() == node_name:
                return i
            i += 1
        return -1

    def get_root_node_info(self):
        return list(self.root_node_info)

    def get_node(self, node_name_or_index):
        if isinstance(node_name_or_index):
            node_name_or_index = self.get_node_index(node_name_or_index)

        if node_name_or_index in range(self.node_count):
            return self.nodes[node_name_or_index]
    def get_node_frames(self, node_name_or_index):
        if isinstance(node_name_or_index):
            node_name_or_index = self.get_node_index(node_name_or_index)

        if node_name_or_index in range(self.node_count):
            return [frame[node_name_or_index] for frame in self.frames]

    def set_frame(self, frame_index, frame_data=None, frame_info=None):
        assert frame_index in range(-(self.frame_count + 1), self.frame_count + 1)

        if frame_data is not None:
            self.frames[frame_index] = frame_data
        if frame_info is not None:
            self.root_node_info[frame_index] = frame_info
    def set_node_frames(self, node_index, frame_data):
        assert node_index in range(-(self.node_count + 1), self.node_count + 1)
        for f in range(self.frame_count):
            self.frames[f][node_index] = frame_data[f]

    def append_frame(self, frame_data=None, frame_info=None):
        self.insert_frame(self.frame_count, frame_data, frame_info)
    def append_frames(self, frames):
        for frame in frames:
            self.insert_frame(self.frame_count, *frame)

    def append_node(self, node, frame_data=None):
        self.insert_node(self.node_count, node, frame_data)
    def append_nodes(self, nodes_and_frames):
        for node_and_frames in nodes_and_frames:
            assert len(nodes_and_frames) > 0
            self.insert_node(self.node_count, *node_and_frames)

    def insert_frame(self, frame_index, frame_data=None, frame_info=None):
        assert frame_index in range(-(self.frame_count + 1), self.frame_count + 1)

        if frame_data is None:
            frame_data = [JmaNodeState() for i in range(self.node_count)]
        else:
            assert len(frame_data) == self.frame_count
            for node_frame in frame_data:
                assert isinstance(node_frame, JmaNodeState)

        if frame_info is None:
            frame_info = JmaRootNodeState()
        else:
            assert isinstance(frame_info, JmaRootNodeState)

        self.frames.insert(frame_index, frame_data)
        self.root_node_info.insert(frame_index, frame_info)
    def insert_frames(self, frames_by_indices):
        for frame_index in reversed(sorted(frames_by_indices)):
            self.insert_frame(frame_index, *frames_by_indices[frame_index])

    def insert_node(self, node_index, node, frame_data=None):
        assert isinstance(node, JmsNode)
        if frame_data is None:
            frame_data = [JmaNodeState() for i in range(self.frame_count)]
        else:
            assert len(frame_data) == self.frame_count
            for node_frame in frame_data:
                assert isinstance(node_frame, JmaNodeState)

        for f in range(self.frame_count):
            self.frames[f].insert(node_index, frame_data[f])
        self.nodes.insert(node_index, node)
    def insert_nodes(self, nodes_and_frames_by_indices):
        for node_index in reversed(sorted(nodes_and_frames_by_indices)):
            self.insert_node(node_index, *nodes_and_frames_by_indices[node_index])

    def remove_frame(self, frame_index):
        assert frame_index in range(-self.frame_count, self.frame_count)
        if frame_index in range(len(self.root_node_info)):
            return (self.frames.pop(frame_index),
                    self.root_node_info.pop(frame_index))
        return self.frames.pop(frame_index), None
    def remove_frames(self, frame_indices):
        return {int(i): self.remove_frame(i) for i in
                reversed(sorted(frame_indices))}

    def remove_node(self, node_index):
        assert node_index in range(-self.node_count, self.node_count)
        return (self.nodes.pop(node_index),
                [frame.pop(node_index) for frame in self.frames])
    def remove_nodes(self, node_indices):
        return {int(i): self.remove_node(i) for i in
                reversed(sorted(node_indices))}

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

                i, j, k, w = multiply_quaternions(q0, q1)

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

                # remove the rotation of the next node from this one to
                # find the yaw difference between the 2 quaternions
                ex, ey, ez = quaternion_to_euler(
                    *multiply_quaternions(q0, Quaternion(q1).inverse)
                    )
                dyaw = clip_angle_to_bounds(ez)

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
    get_node_depths = JmsModel.get_node_depths

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

        # scale is calculated a bit differently. we ALWAYS store scale
        # frame data for a node if its scale is ever not 1.0, even if
        # it is static for the entire animation length. This seems to
        # be due to how compressed animations handle default scales.
        for node_states in self.frames:
            for n in range(len(node_states)):
                if not are_vectors_equal(
                        (node_states[n].scale, ),
                        (1.0, ), False, tolerance):
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

    def compress_animation(self, **kw):
        raise NotImplementedError("Compression isn't implemented yet.")


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

    if parse_jm_int(data[dat_i]) != 16392:
        print("JMA identifier '16392' not found.")
        return jma_anim

    dat_i += 1

    try:
        frame_count = parse_jm_int(data[dat_i]) & 0xFFffFFff
        dat_i += 1
    except Exception:
        print(traceback.format_exc())
        print("Could not read frame count.")
        return jma_anim

    if frame_count > 2048:
        raise ValueError("Cannot parse jma files with more than 2048 frames.")

    try:
        frame_rate = parse_jm_int(data[dat_i]) & 0xFFffFFff
        dat_i += 1
    except Exception:
        print(traceback.format_exc())
        print("Could not frame rate.")
        return jma_anim

    if stop_at == "actors": return jma_anim

    try:
        jma_anim.actors = [None] * (parse_jm_int(data[dat_i]) & 0xFFffFFff)
        dat_i += 1
    except Exception:
        print(traceback.format_exc())
        print("Failed to read actor count.")
        del jma_anim.actors[:]
        return jma_anim

    if jma_anim.actor_count != 1:
        raise ValueError("Cannot parse jma files with more than one actor.")

    # read the actors
    for actor_i in range(len(jma_anim.actors)):
        # TODO: update getting these if multiple actors are ever supported
        nodes  = jma_anim.nodes
        frames = jma_anim.frames
        try:
            jma_anim.actors[actor_i] = data[dat_i]
            dat_i += 1
        except Exception:
            print(traceback.format_exc())
            print("Failed to read actors.")
            del jma_anim.actors[actor_i: ]
            return jma_anim

        try:
            node_count = parse_jm_int(data[dat_i]) & 0xFFffFFff
            dat_i += 1
        except Exception:
            print(traceback.format_exc())
            print("Could not node count.")
            return jma_anim

        if node_count > 256:
            raise ValueError("Cannot parse jma files with more than 256 nodes.")

        if stop_at == "checksum": continue

        try:
            jma_anim.node_list_checksum = parse_jm_int(data[dat_i])
            dat_i += 1
        except Exception:
            print(traceback.format_exc())
            print("Could not read node list checksum.")
            return jma_anim

        if stop_at == "nodes": continue

        # read the nodes
        try:
            i = 0  # make sure i is defined in case of exception
            nodes[:] = [None] * node_count
            for i in range(node_count):
                nodes[i] = JmsNode(
                    data[dat_i], parse_jm_int(data[dat_i+1]), parse_jm_int(data[dat_i+2])
                    )
                dat_i += 3
            JmsNode.setup_node_hierarchy(nodes)
        except Exception:
            print(traceback.format_exc())
            print("Failed to read nodes.")
            del nodes[i: ]
            return jma_anim


        if stop_at == "frames": continue

        # read the frame data
        try:
            i = 0 # make sure i is defined in case of exception
            for i in range(frame_count):
                frame = [None] * node_count
                for j in range(node_count):
                    frame[j] = JmaNodeState(
                        parse_jm_float(data[dat_i]),   parse_jm_float(data[dat_i+1]),
                        parse_jm_float(data[dat_i+2]), parse_jm_float(data[dat_i+3]),
                        parse_jm_float(data[dat_i+4]), parse_jm_float(data[dat_i+5]),
                        parse_jm_float(data[dat_i+6]), parse_jm_float(data[dat_i+7])
                        )
                    dat_i += 8
                frames.append(frame)
        except Exception:
            print(traceback.format_exc())
            print("Failed to read frames.")
            del frames[i: ]
            return jma_anim

    jma_anim.calculate_root_node_info()
    jma_anim.apply_root_node_info_to_states(True)
    jma_anim.calculate_animation_flags()
    return jma_anim


def write_jma(filepath, jma_anim, use_blitzkrieg_rounding=False):
    if jma_anim.actor_count != 1:
        raise ValueError("Cannot write jma files with more than one actor.")

    if use_blitzkrieg_rounding:
        to_str = lambda f: float_to_str_truncate(f, 6)
    else:
        to_str = float_to_str

    # If the path doesnt exist, create it
    filepath = Path(filepath)
    filepath.parent.mkdir(exist_ok=True, parents=True)

    if not jma_anim.root_node_info_applied:
        jma_anim = deepcopy(jma_anim)
        jma_anim.apply_root_node_info_to_states()

    with filepath.open("w", encoding='latin1', newline="\r\n") as f:
        f.write("16392\n")  # version number
        f.write("%s\n" % jma_anim.frame_count)
        f.write("%s\n" % jma_anim.frame_rate)

        f.write("%s\n" % jma_anim.actor_count)

        for actor_name in jma_anim.actors:
            # TODO: update getting these if multiple actors are ever supported
            nodes  = jma_anim.nodes
            frames = jma_anim.frames

            f.write("%s\n" % actor_name)
            f.write("%s\n" % len(nodes))
            f.write("%s\n" % int(jma_anim.node_list_checksum))

            for node in nodes:
                f.write("%s\n%s\n%s\n" %
                    (node.name[: 31], node.first_child, node.sibling_index)
                )

            for frame in frames:
                for nf in frame:
                    f.write("%s\t%s\t%s\n%s\t%s\t%s\t%s\n%s\n" % (
                        to_str(nf.pos_x), to_str(nf.pos_y), to_str(nf.pos_z),
                        to_str(nf.rot_i), to_str(nf.rot_j),
                        to_str(nf.rot_k), to_str(nf.rot_w),
                        to_str(nf.scale))
                    )

#jma_file = open(r'C:\Users\Moses\Desktop\halo\data\characters\cyborg\animations\alert unarmed turn-right.jmt', 'r')
#data = read_jma(jma_file.read(), "", "alert unarmed turn-right.jmt")
