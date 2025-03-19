#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

__all__ = ( 'JmsTriangle', )


class JmsTriangle:
    __slots__ = (
        "region", "shader",
        "v0", "v1", "v2"
        )
    def __init__(self, region=0, shader=0,
                 v0=0, v1=0, v2=0):
        self.region = region
        self.shader = shader
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2

    def __getitem__(self, index):
        if   index == 0: return self.v0
        elif index == 1: return self.v1
        elif index == 2: return self.v2
        raise IndexError("Triangle indices must be in range(0, 3)")

    def __repr__(self):
        return """JmsTriangle(
    region=%s, shader=%s,
    v0=%s, v1=%s, v2=%s
)""" % (self.region, self.shader,
        self.v0, self.v1, self.v2)

    def __eq__(self, other):
        if (not isinstance(other, JmsTriangle) or
            self.shader != other.shader  or
            self.region != other.region  or
            self.v0     != other.v0      or
            self.v1     != other.v1      or
            self.v2     != other.v2
            ):
            return False
        return True
