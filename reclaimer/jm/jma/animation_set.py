#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#
import math

from . import animation, limp_node_info
from .. import constants as const
from ..jms import node as jms_node
from reclaimer.util.matrices import Quaternion, Ray
     

class JmaAnimationSet:
    node_list_checksum  = 0
    nodes               = ()
    limp_node_infos     = ()
    animations          = ()
    version             = const.JMA_VER_HALO_1_OLDEST_KNOWN

    def __init__(self, *jma_animations):
        self.nodes = []
        self.animations = {}

        for jma_animation in jma_animations:
            self.merge_jma_animation(jma_animation)

    verify_animations_match = animation.JmaAnimation.verify_animations_match

    @property
    def has_node_names(self):
        return self.version >= const.JMA_VER_HALO_1_NODE_NAMES
    @property
    def has_node_hierarchy(self):
        return self.version >= const.JMA_VER_HALO_1_NODE_HIERARCHY

    def merge_jma_animation(self, other_jma):
        assert isinstance(other_jma, animation.JmaAnimation)

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
                    jms_node.JmsNode(
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
        self.limp_node_infos = [
            limp_node_info.JmaLimpNodeInfo() for n in self.nodes
            ]

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
            return list(map(
                limp_node_info.JmaLimpNodeInfo(mid_vec).angle_to_other, vecs
                ))

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

