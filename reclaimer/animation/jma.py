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
     parse_jm_float, parse_jm_int, std_dev
from reclaimer.util.matrices import clip_angle_to_bounds, are_vectors_equal,\
     polar_2d_to_vector_3d, vector_3d_to_polar_2d, cross_product,\
     multiply_quats, quat_to_euler, euler_to_quat, Quaternion, Ray
from reclaimer.animation import constants as const, util


def get_anim_ext(anim_type, frame_info_type, world_relative=False):
    anim_type = anim_type.lower()
    frame_info_type = frame_info_type.lower()
    return "." + (
        "jmr" if anim_type == "replacement" else
        "jmo" if anim_type == "overlay"     else
        "jmz" if "dz"   in frame_info_type  else
        "jmt" if "dyaw" in frame_info_type  else
        "jma" if "dx"   in frame_info_type  else
        "jmw" if world_relative             else
        "jmm"
        )


def get_anim_types(anim_ext):
    anim_ext  = anim_ext.lower().strip(".")
    anim_type = {"jmr": anim_types[2],
                 "jmo": anim_types[1],
                 }.get(anim_ext, anim_types[0])
    info_type = {"jmz": anim_frame_info_types[3],
                 "jmt": anim_frame_info_types[2],
                 "jma": anim_frame_info_types[1],
                 }.get(anim_ext, anim_frame_info_types[0])
    world_rel = anim_ext == "jmw"

    return (anim_type, info_type, world_rel)


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
        if (not isinstance(other, JmaRootNodeState)           or
            abs(self.dx - other.dx)     > const.TRANS_EPSILON or
            abs(self.dy - other.dy)     > const.TRANS_EPSILON or
            abs(self.dz - other.dz)     > const.TRANS_EPSILON or
            abs(self.dyaw - other.dyaw) > const.DYAW_EPSILON
            ):
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

    @property
    def quat(self):
        return Quaternion((self.rot_i, self.rot_j, self.rot_k, self.rot_w))

    def __repr__(self):
        return """JmaNodeState(
    x=%s, y=%s, z=%s,
    i=%s, j=%s, k=%s, w=%s,
    scale=%s
)""" % (self.pos_x, self.pos_y, self.pos_z,
        self.rot_i, self.rot_j, self.rot_k, self.rot_w,
        self.scale)

    def __eq__(self, other):
        if (not isinstance(other, JmaNodeState)                 or
            abs(self.rot_i - other.rot_i) > const.QUAT_EPSILON  or
            abs(self.rot_j - other.rot_j) > const.QUAT_EPSILON  or
            abs(self.rot_k - other.rot_k) > const.QUAT_EPSILON  or
            abs(self.rot_w - other.rot_w) > const.QUAT_EPSILON  or
            abs(self.pos_x - other.pos_x) > const.TRANS_EPSILON or
            abs(self.pos_y - other.pos_y) > const.TRANS_EPSILON or
            abs(self.pos_z - other.pos_z) > const.TRANS_EPSILON or
            abs(self.scale - other.scale) > const.SCALE_EPSILON
            ):
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

class JmaLimpNodeInfo:
    __slots__ = (
        "i", "j", "k", "delta", "axes_free",
        "cross_delta"
        )
    def __init__(self, vector=None, delta=0.0,
                 axes_free=None, joint_flags=None, cross_delta=None
                 ):
        assert axes_free   in (0, 1, 2, None)
        assert isinstance(joint_flags, (int, type(None)))
        assert vector is None or len(vector) in (2, 3)

        i, j, k = (
            (1.0, 0.0, 0.0)         if vector is None or len(vector) != 2 else
            Ray(vector).normalized  if vector        and len(vector) == 3 else
            polar_2d_to_vector_3d(*vector)
            )

        self.i, self.j, self.k, self.delta = i, j, k, delta
        if axes_free is None and joint_flags in (1, 2):
            # math just works out like this
            axes_free = 2-joint_flags

        self.axes_free   = axes_free or 0
        self.cross_delta = (cross_delta or 0) if axes_free == 2 else 0

    # NOTE: the only reason we care about polar coordinates for limp nodes
    #       is because the hinge joints are designed to pivot on y and z,
    #       but not x. in polar coordinates we use x as the reference axis

    @property
    def joint_flags(self):  return 1 << (2 - self.axes_free)
    @property
    def vector_ortho(self): return self.i, self.j, self.k
    @property
    def vector_polar(self): return vector_3d_to_polar_2d(*self.vector_ortho)
    @property
    def vector_range(self): return (self.delta if self.axes_free < 2 else
                                    Ray([self.delta, self.cross_delta]).mag)

    def angle_to_other(self, other):
        i0, j0, k0 = self.i, self.j, self.k
        i1, j1, k1 = (
            other if hasattr(other, "__iter__") else
            (other.i, other.j, other.k)
            )
        mag = ((i0**2 + j0**2 + k0**2) *
               (i1**2 + j1**2 + k1**2)) or 1

        cosine = (i0*i1 + j0*j1 + k0*k1)/mag
        return (0       if cosine >=  1 else
                math.pi if cosine <= -1 else
                math.acos(cosine))

    def __repr__(self):
        return """JmaLimpNodeInfo(
    vector_ortho=%s,
    vector_polar=%s,
    delta=%s, cross_delta=%s, axes_free=%s
)""" % (self.vector_ortho, self.vector_polar, self.delta,
        self.cross_delta, self.axes_free)


class JmaAnimation:
    name = ""
    node_list_checksum = 0
    nodes = ()
    frames = ()
    version = 0

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

    compress_quality = 1.0

    root_node_info_applied = True
    overlay_base_applied   = True

    anim_type = anim_types[0]
    frame_info_type = anim_frame_info_types[0]

    def __init__(self, name="", node_list_checksum=0,
                 anim_type="", frame_info_type="", world_relative=False,
                 nodes=None, frames=None, actors=None, frame_rate=30,
                 version=const.JMA_VER_HALO_1_RETAIL,
                 ):

        self.name = name.strip(" ")
        self.node_list_checksum = node_list_checksum
        self.nodes  = nodes  if nodes  else []
        self.frames = frames if frames else []
        self.world_relative = bool(world_relative)
        self.anim_type = anim_type
        self.frame_info_type = frame_info_type
        self.frame_rate = frame_rate
        self.actors = actors if actors else ["unnamedActor"]
        self.version = version

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
    def has_frame_info(self):
        return self.has_dxdy or self.has_dz or self.has_dyaw

    @property
    def has_node_names(self):
        return self.version >= const.JMA_VER_HALO_1_NODE_NAMES
    @property
    def has_node_hierarchy(self):
        return self.version >= const.JMA_VER_HALO_1_NODE_HIERARCHY

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
    def is_overlay(self):     return self.anim_type == "overlay"
    @property
    def is_replacement(self): return self.anim_type == "replacement"
    @property
    def is_base(self): return not(self.is_overlay or self.is_replacement)

    @property
    def actor_count(self): return len(self.actors)
    @property
    def frame_count(self): return len(self.frames)
    @property
    def node_count(self): return len(self.nodes)

    @property
    def last_frame_loops_to_first(self):
        return not self.is_overlay

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
        if isinstance(node_name_or_index, int):
            node_name_or_index = self.get_node_index(node_name_or_index)

        if node_name_or_index in range(self.node_count):
            return self.nodes[node_name_or_index]
    def get_node_frames(self, node_name_or_index):
        if isinstance(node_name_or_index, int):
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

    def apply_base_pose_to_states(self, undo=False):
        apply = not undo
        if bool(self.overlay_base_applied) == apply:
            # do nothing if the base is already applied and
            # we are being told to apply it, or its not and
            # we are being told to undo its application.
            return

        # using the base frame, apply each overlay frame onto it
        for n, b_node in enumerate(self.frames[0] if self.is_overlay else []):
            b_s                = b_node.scale
            b_x, b_y, b_z      = b_node.pos_x, b_node.pos_y, b_node.pos_z
            b_i, b_j, b_k, b_w = [b_node.rot_i, b_node.rot_j,
                                  b_node.rot_k, b_node.rot_w]

            if undo:
                b_s           = 1/b_s if b_s else 1
                b_x, b_y, b_z = -b_x, -b_y, -b_z
                b_i, b_j, b_k = -b_i, -b_j, -b_k

            b_quat = Ray([b_i, b_j, b_k, b_w])
            b_quat.normalize()
            for frame in self.frames[1:]:
                o_node = frame[n]
                o_quat = Ray([o_node.rot_i, o_node.rot_j,
                              o_node.rot_k, o_node.rot_w])
                o_quat.normalize()

                q_i, q_j, q_k, q_w = multiply_quats(o_quat, b_quat)
                o_node.pos_x += b_x
                o_node.pos_y += b_y
                o_node.pos_z += b_z
                o_node.scale *= b_s
                o_node.rot_i  = q_i
                o_node.rot_j  = q_j
                o_node.rot_k  = q_k
                o_node.rot_w  = q_w

        self.overlay_base_applied = self.is_overlay and apply

    def apply_root_node_info_to_states(self, undo=False):
        apply = not undo
        if bool(self.root_node_info_applied) == apply:
            # do nothing if the root node info is already applied
            # and we are being told to apply it, or its not applied
            # and we are being told to undo its application.
            return

        if self.has_frame_info:
            delta = 1 if apply else -1
            for f in range(self.frame_count):
                # apply the total change in the root nodes
                # frame_info for this frame to the frame_data
                node_info = self.root_node_info[f]
                node_state = self.frames[f][0]

                q0 = Ray(euler_to_quat(0, 0, -node_info.yaw * delta))
                q1 = Ray((node_state.rot_i, node_state.rot_j,
                          node_state.rot_k, node_state.rot_w))
                q0.normalize()
                q1.normalize()

                i, j, k, w = multiply_quats(q0, q1)

                node_state.pos_x += node_info.x * delta
                node_state.pos_y += node_info.y * delta
                node_state.pos_z += node_info.z * delta
                node_state.rot_i = i
                node_state.rot_j = j
                node_state.rot_k = k
                node_state.rot_w = w

        self.root_node_info_applied = self.has_frame_info and apply

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
                ex, ey, ez = quat_to_euler(
                    *multiply_quats(q0, Quaternion(q1).inverse)
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

    def get_node_depths(self):
        if self.has_node_hierarchy:
            return JmsModel.get_node_depths(self)
        return []

    def verify_nodes_valid(self):
        errors = []
        if self.has_node_hierarchy or len(self.nodes) not in range(1, 64):
            return JmsModel.verify_nodes_valid(self)
        elif self.has_node_names:
            seen_names = set()
            for i in range(len(self.nodes)):
                n = self.nodes[i]
                if len(n.name) >= 32:
                    errors.append("Node name node '%s' is too long." % n.name)
                elif n.name.lower() in seen_names:
                    errors.append("Multiple nodes named '%s'." % n.name)

                seen_names.add(n.name.lower())

        return errors

    def calculate_animation_flags(self, tolerance=1.0):
        # determine which transforms types of each node are animated
        # by seeing how much they change from the starting frame
        r_flags, t_flags, s_flags = util.calculate_anim_flags(
            self.frames, tolerance
            )

        flags = util.pack_anim_flags(r_flags, t_flags, s_flags)
        self.rot_flags_int, self.trans_flags_int, self.scale_flags_int = flags

    def verify_animations_match(self, other_jma):
        errors = list(other_jma.verify_jma())
        if len(other_jma.nodes) != len(self.nodes):
            errors.append("Node counts do not match.")
            return errors

        if self.has_node_names and other_jma.has_node_names:
            for i in range(len(self.nodes)):
                if not self.nodes[i].is_node_hierarchy_equal(
                        other_jma.nodes[i], not (
                            self.has_node_hierarchy and 
                            other_jma.has_node_hierarchy
                            )
                        ):
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

    def calculate_keyframes(self, **kw):
        all_rot_kfs   = []
        all_trans_kfs = []
        all_scale_kfs = []

        for n, xform_flags in enumerate(zip(
                self.rot_flags, self.trans_flags, self.scale_flags
                )):
            has_rot, has_trans, has_scale = xform_flags
            rot_kfs, trans_kfs, scale_kfs = set(), set(), set()

            states  = [ns[n] for ns in self.frames]
            # these hold tuples of transform data
            rot_data, trans_data, scale_data = [], [], []

            # extract the individual transforms for easy manipulation
            has_rot   and rot_data.extend(
                # ensure rotations use the same axis direction
                [( s.rot_i,  s.rot_j,  s.rot_k,  s.rot_w) if s.rot_w > 0 else
                 (-s.rot_i, -s.rot_j, -s.rot_k, -s.rot_w)
                 for s in states]
                )
            has_trans and trans_data.extend(
                [(s.pos_x, s.pos_y, s.pos_z) for s in states]
                )
            has_scale and scale_data.extend([(s.scale, ) for s in states])

            # ensuring the root node's quality doesn't dip too far
            # since errors in it propagate to every other node
            quality = min(const.COMPRESS_QUALITY_MAX, max(
                self.compress_quality,
                const.COMPRESS_QUALITY_MIN if n else
                const.COMPRESS_QUALITY_MIN_NODE_0
                ))

            # squaring the quality achieves a more linear compression ratio
            # curve when going from max quality all the way down to minimum
            q_scale_lo  = (1.0 - quality)**2
            q_scale_hi  =  1.0 - q_scale_lo

            error_range = (
                const.COMPRESS_AREA_ERR_LOWER * q_scale_hi +
                const.COMPRESS_AREA_ERR_UPPER * q_scale_lo
                )
            delta_cutoff = (
                const.COMPRESS_ANGLE_RANGE_LOWER * q_scale_hi +
                const.COMPRESS_ANGLE_RANGE_UPPER * q_scale_lo
                )
            flip_cutoff = (
                const.COMPRESS_ANGLE_FLIP_LOWER * q_scale_hi +
                const.COMPRESS_ANGLE_FLIP_UPPER * q_scale_lo
                )
            diff_cutoff = (
                const.COMPRESS_ANGLE_DIFF_LOWER * q_scale_hi +
                const.COMPRESS_ANGLE_DIFF_UPPER * q_scale_lo
                )

            for kfdata, kfs in ([  rot_data,   rot_kfs],
                                [trans_data, trans_kfs],
                                [scale_data, scale_kfs]):
                count = len(kfdata)
                if not count:
                    continue

                kfs.update(range(1, count-1))

                # calculate acceleration
                acc         = util.get_curve_derivative(kfdata, 2)
                acc_comps   = list(zip(*acc))
                all_angles  = [[0]*len(kfdata) for _ in acc_comps]
                crit_points = set([1, max(kfs)])
                # determine the critical points to the curve's structure by
                # calculating the points the acceleration hits a low and rebounds
                for c, vals in enumerate(acc_comps):
                    for i, v0 in enumerate(vals[:-1]):
                        # figure out the angle of the curve at this point
                        v0  = kfdata[i][c]
                        r0  = Ray([-1, (kfdata[i-1][c]-v0) if i else 0])
                        r1  = Ray([ 1,  kfdata[i+1][c]-v0])
                        r0[0] *= const.COMPRESS_FRAME_WIDTH
                        r1[0] *= const.COMPRESS_FRAME_WIDTH
                        r0.normalize()
                        r1.normalize()

                        # simplified cross-product and dot-products
                        sin = r0[0]*r1[1] - r0[1]*r1[0]
                        cos = r0[0]*r1[0] + r0[1]*r1[1]

                        # avoid math domain errors from rounding errors
                        cos = -1 if cos < -1 else 1 if cos > 1 else cos

                        # we're actually measuring the complementary
                        # angle, and we want it in the [-1, 1] range
                        ang = 1 - math.acos(cos)*const.RAD_TO_UNIT

                        # sign it so we can track inflection changes
                        all_angles[c][i] = -ang if sin < 0 else ang

                    delta, neg = 0, False
                    for i, angle in enumerate(all_angles[c]):
                        abs_angle   = abs(angle)
                        new_delta   = delta + abs_angle
                        abs_delta   = abs(new_delta)
                        new_neg     = angle < 0

                        angle_met = abs_angle > diff_cutoff
                        delta_met = abs_delta > delta_cutoff
                        flipped   = new_neg != neg and abs(angle) > flip_cutoff

                        if (i in crit_points or
                            angle_met or delta_met or flipped):
                            # critical point. either the point was already
                            # recorded, the total diff since the last critical
                            # point passed the threshold, or concavity flipped
                            crit_points.add(i)
                            neg, delta = new_neg, 0
                        else:
                            delta = new_delta


                sorted_crit_points = sorted(crit_points)
                crit_point_pairs = [
                    *((sorted_crit_points[i], x1) for i, x1 in
                      enumerate(sorted_crit_points, -1)
                      ),
                    # as a final pass to get any remaining savings, we'll
                    # have the optimizer cover between the min and max points
                    (1, max(kfs))
                    ]
                zero         = [0.0        for _ in acc[0]]
                area_totals  = [sum(abs(a) for a in areas)
                                for areas in acc_comps]
                # a cross product is the area of a parallelogram, but
                # we want only half that. instead of dividing tri_area
                # by 2, we multiply these by 2 as an optimization.
                error_maxs   = [2*t*error_range for t in area_totals]
                err_totals = [*zero]
                err_segs   = [*zero]
                error_maxs_per_segment = [e/max(1, (count-1))
                                          for e in error_maxs]

                # remove points whose difference in acceleration
                # between frames is below our error tolerances
                while crit_point_pairs:
                    f_min, f_max = crit_point_pairs.pop(0)

                    # number of points to check between min and max bounds
                    if f_max - f_min <= 1:
                        continue

                    # selecting points to drop is being done by starting
                    # at the center of each pair of critical points, as
                    # that's where the least change is likely to occur
                    # and should be the safest to remove without error
                    f0 = f_min
                    for f1 in range(f_min+1, f_max-1):
                        if f1 not in kfs or f1 in crit_points:
                            # point was already removed, so skip
                            f0 = f1
                            continue

                        f2 = f1 + 1

                        # figure out the triangle area with the cross product
                        f01_d, f21_d = f0-f1, f2-f1
                        keep    = False
                        areas   = [abs(f21_d * (A[f0]-A[f1]) -
                                       f01_d * (A[f2]-A[f1]))
                                   for A in acc_comps]

                        for area, err_total, err_seg, err_max, err_seg_max in zip(
                                areas, err_totals, err_segs,
                                error_maxs, error_maxs_per_segment
                                ):
                            # check if triangle is small enough to ignore
                            if (area + err_total > err_max or
                                area + err_seg   > err_seg_max):
                                keep = True
                                break

                        if keep:
                            # split at vert and reprocess halves
                            err_segs[:] = zero
                            crit_point_pairs.insert(0, (f_min, f1))
                            crit_point_pairs.insert(0, (f1, f_max))
                            break

                        # skip the vert and add its area to the error
                        err_segs[:]   = [a+b for a,b in zip(areas, err_segs)]
                        err_totals[:] = [a+b for a,b in zip(areas, err_totals)]
                        kfs.discard(f1)

            all_rot_kfs.append(sorted(rot_kfs))
            all_trans_kfs.append(sorted(trans_kfs))
            all_scale_kfs.append(sorted(scale_kfs))

        self.rot_keyframes   = all_rot_kfs
        self.trans_keyframes = all_trans_kfs
        self.scale_keyframes = all_scale_kfs


class JmaAnimationSet:
    node_list_checksum = 0
    nodes = ()
    limp_node_infos = ()
    animations = ()
    version = const.JMA_VER_HALO_1_OLDEST_KNOWN

    def __init__(self, *jma_animations):
        self.nodes = []
        self.animations = {}

        for jma_animation in jma_animations:
            self.merge_jma_animation(jma_animation)

    verify_animations_match = JmaAnimation.verify_animations_match

    @property
    def has_node_names(self):
        return self.version >= const.JMA_VER_HALO_1_NODE_NAMES
    @property
    def has_node_hierarchy(self):
        return self.version >= const.JMA_VER_HALO_1_NODE_HIERARCHY

    def merge_jma_animation(self, other_jma):
        assert isinstance(other_jma, JmaAnimation)

        if not other_jma:
            return

        if other_jma.version > self.version and self.nodes:
            # if the other jma's version is newer, grab its nodes if they
            # match well enough, since they'll contain more detailed data
            if (self.node_list_checksum == other_jma.node_list_checksum and 
                not self.verify_animations_match(other_jma)):
                self.nodes = []

        if not self.nodes:
            self.node_list_checksum = other_jma.node_list_checksum
            self.version = other_jma.version
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

    def calculate_limp_node_data(self, ignore_overlays=True):
        self.limp_node_infos = [JmaLimpNodeInfo() for n in self.nodes]

        all_node_states = [[] for _ in self.nodes]
        # grab the frame data for EVERY animation and concatenate
        # them together into one large list separated by node
        for anim in self.animations.values():
            if ignore_overlays and anim.is_overlay:
                continue

            frames = anim.frames
            if anim.last_frame_loops_to_first:
                frames = frames[:-1]

            for n, node_states in enumerate(all_node_states):
                node_states.extend(frame[n] for frame in frames)

        if max(*[len(states) for states in all_node_states], 0) < 2:
            # no anims????
            return

        def get_mid_value(vals, offset=0.5):
            return vals[int(min(1.0, max(0.0, offset))*len(vals))]

        def get_deltas(vecs, mid_vec):
            return list(map(JmaLimpNodeInfo(mid_vec).angle_to_other, vecs))

        def get_mid_vector(vecs):
            # calculate the average so we have a starting point to
            # iteratively get closer and closer to the actual median
            mid_vec = Ray([sum(vals) for vals in zip(*vecs)]).normalized
            if not mid_vec.mag:
                # all directions equal, so default to along x-axis
                mid_vec[:] = (1, 0, 0)

            # 3 iterations should be enough to get a decent median
            for i in range(3):
                # quickly calculate the distance from the current mid_vec
                # to each vector to determine how off we really are
                comp_diffs_sq = [list(
                    map((2.0).__rpow__,
                    map(float(v0).__rsub__, comps)))
                    for comps, v0 in zip(zip(*vecs), mid_vec)
                    ]
                diffs = list(
                    map(math.sqrt,
                    map(sum, zip(*comp_diffs_sq)))
                    )
                sorted_diffs = sorted(diffs)
                start = int(len(diffs) * 0.85)
                stop  = int(len(diffs) * 0.95 + 0.5)
                if start == stop:
                    start -= 1
                    if start < 0:
                        start, stop = 0, stop + 1

                mid_diff = sum(sorted_diffs[start: stop])/(stop - start) or 1.0

                weights = [1/(1 + (mid_diff - diff)**2) for diff in diffs]
                weight_total = sum(weights)
                # recalculate the mid_vec using the weights
                mid_vec = [
                    sum(map(float.__rmul__, weights, comps))/weight_total
                    for comps in zip(*vecs)
                    ]
                

            return Ray(mid_vec).normalized

        x_axis = Quaternion([1, 0, 0, 0])
        for node, info, node_states in zip(
                self.nodes, self.limp_node_infos, all_node_states
                ):
            if "spine" in node.name.lower():
                # NOTE: this is a hack. bungie hardcoded a check into tool to skip
                #       calculating limp physics values for a node if the "spine"
                #       is present ANYWHERE in the nodes name. this can be tested
                #       by compiling an animation with tool and renaming the node.
                #       this appears to be because enabling limp physics on torso
                #       nodes results in very ugly inverse-kinematics, regardless
                #       of the base vector or range. we need to emulate this
                continue

            # get the directions the positive x-axis will
            # be pointing after the rotations are applied
            vectors     = [Ray((ns.quat.inverse*x_axis*ns.quat)[:3]).normalized
                           for ns in node_states]

            # calculate the average vector and deltas
            center_vec = get_mid_vector(vectors)
            deltas     = get_deltas(vectors, center_vec)
            avg_delta  = sum(deltas)/len(deltas)
            if avg_delta < const.LIMP_NODE_MIN_RANGE:
                # not enough movement to consider a limp-node joint
                continue

            # set the base vector and calculate delta using the weights
            info.i, info.j, info.k = center_vec
            info.delta, info.axes_free = avg_delta, 1

            # determine if this is a hinge, or ball-socket joint.
            # do this by crossing every vector with center_vec, normalizing
            # and averaging them(using the existing weights), and calculating
            # the cross_deltas. if ANY of the cross_deltas scaled their weight
            # are larger than const.LIMP_NODE_MIN_RANGE radians, then this is
            # a ball-socket joint. if not, its a hinge joint.
            c_vectors   = [center_vec.cross_with(v).normalized for v in vectors]

            # some cross products will point into the opposite hemisphere.
            # account for this by reversing the 90-180 range
            c_deltas = sorted(math.pi/2 - d if d > math.pi/4 else d for d in
                              get_deltas(c_vectors, get_mid_vector(c_vectors)))

            # use a value from the upper90 for the range on the crossed axis
            info.cross_delta = get_mid_value(c_deltas, 0.9)
            # increment the number of axes if there's enough movement
            info.axes_free += info.cross_delta >= const.LIMP_NODE_CROSS_MIN


def read_jma(jma_string, stop_at="", anim_name=""):
    if anim_name is None:
        anim_name = "__unnamed"

    anim_name, ext = os.path.splitext(anim_name)
    anim_type, frame_info_type, world_relative = get_anim_types(ext)

    jma_string = jma_string.replace("\n", "\t")

    data = tuple(d for d in jma_string.split("\t") if d)
    dat_i = 0
    version = parse_jm_int(data[dat_i])

    jma_anim = JmaAnimation(anim_name, 0, anim_type,
                            frame_info_type, world_relative,
                            version=version)

    if version not in const.JMA_VER_ALL:
        print("Unknown JMA version '%s' found." % version)
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

        if jma_anim.node_list_checksum >= 0x80000000:
            # jma gave us an unsigned checksum.... sign it
            jma_anim.node_list_checksum -= 0x100000000

        if stop_at == "nodes": continue

        # read the nodes
        try:
            i = 0  # make sure i is defined in case of exception
            nodes[:] = [None] * node_count
            for i in range(node_count):
                if jma_anim.has_node_hierarchy:
                    node_data = (
                        data[dat_i],
                        parse_jm_int(data[dat_i+1]),
                        parse_jm_int(data[dat_i+2])
                        )
                    dat_i += 3
                elif jma_anim.has_node_names:
                    node_data = (data[dat_i], )
                    dat_i += 1
                else:
                    node_data = ("fake_node_%d" % i, )

                nodes[i] = JmsNode(*node_data)
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

    to_str = (
        float_to_str if not use_blitzkrieg_rounding else
        (lambda f: float_to_str_truncate(f, 6))
        )

    # If the path doesnt exist, create it
    filepath = Path(filepath)
    filepath.parent.mkdir(exist_ok=True, parents=True)

    if not jma_anim.root_node_info_applied:
        jma_anim = deepcopy(jma_anim)
        jma_anim.apply_root_node_info_to_states()

    with filepath.open("w", encoding='latin1', newline="\r\n") as f:
        f.write("%d\n" % jma_anim.version)
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

            if jma_anim.has_node_hierarchy:
                for node in nodes:
                    f.write("%s\n%s\n%s\n" %
                        (node.name[: 31], node.first_child, node.sibling_index)
                    )
            elif jma_anim.has_node_names:
                for node in nodes:
                    f.write("%s\n" % node.name[: 31])

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
