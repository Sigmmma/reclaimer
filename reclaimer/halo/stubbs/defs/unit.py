from ...hek.defs.unit import *
from ..common_descs import *
from supyr_struct.defs.tag_def import TagDef

unit_attrs = dict(unit_attrs)
unit_attrs[0] = BBool32("flags",
    "circular aiming",
    "destroyed after dying",
    "half-speed interpolation",
    "fires from camera",
    "entrance inside bounding sphere",
    "unused",
    "causes passenger dialogue",
    "resists pings",
    "melee attack is fatal",
    "dont reface during pings",
    "has no aiming",
    "simple creature",
    "impact melee attaches to unit",
    "cannot open doors automatically",
    "melee attackers cannot attach",
    "not instantly killed by melee",
    "shield sapping",
    "runs around flaming",
    "inconsequential",
    "special cinematic unit",
    "ignored by autoaiming",
    "shields fry infection forms",
    "integrated light controls weapon",
    "integrated light lasts forever",
    )
unit_attrs[1] = BSEnum16('default team', *unit_teams)
unit_attrs[48] = BSEnum16('grenade type', *grenade_types)

unit_body = Struct('tagdata',
    unit_attrs,
    SIZE=372
    )

def get():
    return unit_def

unit_def = TagDef("unit",
    blam_header('unit', 2),
    unit_body,

    ext=".unit", endian=">"
    )
