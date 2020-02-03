#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

__all__ = ( 'JmsMaterial', )


class JmsMaterial:
    __slots__ = (
        "name", "tiff_path",
        "shader_path", "shader_type",
        "properties"
        )
    def __init__(self, name="__unnamed", tiff_path="<none>",
                 shader_path="", shader_type="", properties=""):
        for c in "!@#$%^&*-.":
            if c in name and c not in properties:
                properties += c
            name = name.replace(c, '')

        self.name = name
        self.tiff_path = tiff_path
        self.shader_path = shader_path if shader_path else name
        self.shader_type = shader_type
        self.properties = properties

    @property
    def ai_defeaning(self): return "&" in self.properties
    @ai_defeaning.setter
    def ai_defeaning(self, new_val):
        self.properties = self.properties.replace("&", "") + ("&" if new_val else "")

    @property
    def allow_transparency(self): return "#" in self.properties
    @allow_transparency.setter
    def allow_transparency(self, new_val):
        self.properties = self.properties.replace("#", "") + ("#" if new_val else "")

    @property
    def breakable(self): return "-" in self.properties
    @breakable.setter
    def breakable(self, new_val):
        self.properties = self.properties.replace("-", "") + ("-" if new_val else "")

    # collision_only means the player collides, but not projectiles
    @property
    def collision_only(self): return "@" in self.properties
    @collision_only.setter
    def collision_only(self, new_val):
        self.properties = self.properties.replace("@", "") + ("@" if new_val else "")

    @property
    def double_sided(self): return "%" in self.properties
    @double_sided.setter
    def double_sided(self, new_val):
        self.properties = self.properties.replace("%", "") + ("%" if new_val else "")

    @property
    def exact_portal(self): return "." in self.properties
    @exact_portal.setter
    def exact_portal(self, new_val):
        self.properties = self.properties.replace(".", "") + ("." if new_val else "")

    @property
    def fog_plane(self): return "$" in self.properties
    @fog_plane.setter
    def fog_plane(self, new_val):
        self.properties = self.properties.replace("$", "") + ("$" if new_val else "")

    @property
    def ladder(self): return "^" in self.properties
    @ladder.setter
    def ladder(self, new_val):
        self.properties = self.properties.replace("^", "") + ("^" if new_val else "")

    # this is what sky and invisible collision get set to
    @property
    def large_collideable(self): return "*" in self.properties
    @large_collideable.setter
    def large_collideable(self, new_val):
        self.properties = self.properties.replace("*", "") + ("*" if new_val else "")

    @property
    def render_only(self): return "!" in self.properties
    @render_only.setter
    def render_only(self, new_val):
        self.properties = self.properties.replace("!", "") + ("!" if new_val else "")

    def __repr__(self):
        return """JmsMaterial(name=%s,
    tiff_path=%s
)""" % (self.name, self.tiff_path)
