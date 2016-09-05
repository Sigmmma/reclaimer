from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

def get(): return udlg_def


udlg_body = Struct("tagdata",
    Pad(16),
    Struct("idle",
        dependency("noncombat", valid_sounds),
        dependency("combat", valid_sounds),
        dependency("flee", valid_sounds),
        Pad(48),
        ),
    Struct("involuntary",
        dependency("pain body minor", valid_sounds),
        dependency("pain body maior", valid_sounds),
        dependency("pain shield", valid_sounds),
        dependency("pain falling", valid_sounds),
        dependency("scream fear", valid_sounds),
        dependency("scream pain", valid_sounds),
        dependency("maimed limb", valid_sounds),
        dependency("maimed head", valid_sounds),
        dependency("death quiet", valid_sounds),
        dependency("death violent", valid_sounds),
        dependency("death falling", valid_sounds),
        dependency("death agonizing", valid_sounds),
        dependency("death instant", valid_sounds),
        dependency("death flying", valid_sounds),
        Pad(16),
        ),
    Struct("hurting people",
        dependency("damaged friend", valid_sounds),
        dependency("damaged friend player", valid_sounds),
        dependency("damaged enemy", valid_sounds),
        dependency("damaged enemy cm", valid_sounds),
        Pad(64),
        ),
    Struct("being hurt",
        dependency("hurt friend", valid_sounds),
        dependency("hurt friend re", valid_sounds),
        dependency("hurt friend player", valid_sounds),
        dependency("hurt enemy", valid_sounds),
        dependency("hurt enemy re", valid_sounds),
        dependency("hurt enemy cm", valid_sounds),
        dependency("hurt enemy bullet", valid_sounds),
        dependency("hurt enemy needler", valid_sounds),
        dependency("hurt enemy plasma", valid_sounds),
        dependency("hurt enemy sniper", valid_sounds),
        dependency("hurt enemy grenade", valid_sounds),
        dependency("hurt enemy explosion", valid_sounds),
        dependency("hurt enemy melee", valid_sounds),
        dependency("hurt enemy flame", valid_sounds),
        dependency("hurt enemy shotgun", valid_sounds),
        dependency("hurt enemy vehicle", valid_sounds),
        dependency("hurt enemy mounted weapon", valid_sounds),
        Pad(48),
        ),
    Struct("killing people",
        dependency("killed friend", valid_sounds),
        dependency("killed friend cm", valid_sounds),
        dependency("killed friend player", valid_sounds),
        dependency("killed friend player cm", valid_sounds),
        dependency("killed enemy", valid_sounds),
        dependency("killed enemy cm", valid_sounds),
        dependency("killed enemy player", valid_sounds),
        dependency("killed enemy player cm", valid_sounds),
        dependency("killed enemy covenant", valid_sounds),
        dependency("killed enemy covenant cm", valid_sounds),
        dependency("killed enemy floodcombat", valid_sounds),
        dependency("killed enemy floodcombat cm", valid_sounds),
        dependency("killed enemy floodcarrier", valid_sounds),
        dependency("killed enemy floodcarrier cm", valid_sounds),
        dependency("killed enemy sentinel", valid_sounds),
        dependency("killed enemy sentinel cm", valid_sounds),

        dependency("killed enemy bullet", valid_sounds),
        dependency("killed enemy needler", valid_sounds),
        dependency("killed enemy plasma", valid_sounds),
        dependency("killed enemy sniper", valid_sounds),
        dependency("killed enemy grenade", valid_sounds),
        dependency("killed enemy explosion", valid_sounds),
        dependency("killed enemy melee", valid_sounds),
        dependency("killed enemy flame", valid_sounds),
        dependency("killed enemy shotgun", valid_sounds),
        dependency("killed enemy vehicle", valid_sounds),
        dependency("killed enemy mounted weapon", valid_sounds),
        dependency("killing spree", valid_sounds),
        Pad(48),
        ),
    Struct("player kill responses",
        dependency("player kill cm", valid_sounds),
        dependency("player kill bullet cm", valid_sounds),
        dependency("player kill needler cm", valid_sounds),
        dependency("player kill plasma cm", valid_sounds),
        dependency("player kill sniper cm", valid_sounds),
        dependency("anyone kill grenade cm", valid_sounds),
        dependency("player kill explosion cm", valid_sounds),
        dependency("player kill melee cm", valid_sounds),
        dependency("player kill flame cm", valid_sounds),
        dependency("player kill shotgun cm", valid_sounds),
        dependency("player kill vehicle cm", valid_sounds),
        dependency("player kill mounted weapon cm", valid_sounds),
        dependency("player killing spree cm", valid_sounds),
        Pad(48),
        ),
    Struct("friends dying",
        dependency("friend died", valid_sounds),
        dependency("friend player died", valid_sounds),
        dependency("friend killed by friend", valid_sounds),
        dependency("friend killed by friendly player", valid_sounds),
        dependency("friend enemy", valid_sounds),
        dependency("friend enemy player", valid_sounds),
        dependency("friend covenant", valid_sounds),
        dependency("friend flood", valid_sounds),
        dependency("friend sentinel", valid_sounds),
        dependency("friend betrayed", valid_sounds),
        Pad(32),
        ),
    Struct("shouting",
        dependency("new combat alone", valid_sounds),
        dependency("new enemy recent combat", valid_sounds),
        dependency("old enemy sighted", valid_sounds),
        dependency("unexpected enemy", valid_sounds),
        dependency("dead friend found", valid_sounds),
        dependency("alliance broken", valid_sounds),
        dependency("alliance reformed", valid_sounds),
        dependency("grenade throwing", valid_sounds),
        dependency("grenade sighted", valid_sounds),
        dependency("grenade startle", valid_sounds),
        dependency("grenade danger enemy", valid_sounds),
        dependency("grenade danger self", valid_sounds),
        dependency("grenade danger friend", valid_sounds),
        Pad(32),
        ),
    Struct("group communication",
        dependency("new combat group re", valid_sounds),
        dependency("new combat nearby re", valid_sounds),
        dependency("alert friend", valid_sounds),
        dependency("alert friend re", valid_sounds),
        dependency("alert lost contact", valid_sounds),
        dependency("alert lost contact re", valid_sounds),
        dependency("blocked", valid_sounds),
        dependency("blocked re", valid_sounds),
        dependency("search start", valid_sounds),
        dependency("search query", valid_sounds),
        dependency("search query re", valid_sounds),
        dependency("search report", valid_sounds),
        dependency("search abandon", valid_sounds),
        dependency("search group abandon", valid_sounds),
        dependency("group uncover", valid_sounds),
        dependency("group uncover re", valid_sounds),
        dependency("advance", valid_sounds),
        dependency("advance re", valid_sounds),
        dependency("retreat", valid_sounds),
        dependency("retreat re", valid_sounds),
        dependency("cover", valid_sounds),
        Pad(64),
        ),
    Struct("actions",
        dependency("sighted friend player", valid_sounds),
        dependency("shooting", valid_sounds),
        dependency("shooting vehicle", valid_sounds),
        dependency("shooting berserk", valid_sounds),
        dependency("shooting group", valid_sounds),
        dependency("shooting traitor", valid_sounds),
        dependency("taunt", valid_sounds),
        dependency("taunt re", valid_sounds),
        dependency("flee", valid_sounds),
        dependency("flee re", valid_sounds),
        dependency("free leader died", valid_sounds),
        dependency("attempted flee", valid_sounds),
        dependency("attempted flee re", valid_sounds),
        dependency("lost contact", valid_sounds),
        dependency("hiding finished", valid_sounds),
        dependency("vehicle entry", valid_sounds),
        dependency("vehicle exit", valid_sounds),
        dependency("vehicle woohoo", valid_sounds),
        dependency("vehicle scared", valid_sounds),
        dependency("vehicle collision", valid_sounds),
        dependency("partially sighted", valid_sounds),
        dependency("nothing there", valid_sounds),
        dependency("pleading", valid_sounds),
        Pad(96),
        ),
    Struct("exclamations",
        dependency("surprise", valid_sounds),
        dependency("berserk", valid_sounds),
        dependency("melee attack", valid_sounds),
        dependency("dive", valid_sounds),
        dependency("uncover exclamation", valid_sounds),
        dependency("leap attack", valid_sounds),
        dependency("resurrection", valid_sounds),
        Pad(64),
        ),
    Struct("post-combat actions",
        dependency("celebration", valid_sounds),
        dependency("check body enemy", valid_sounds),
        dependency("check body friend", valid_sounds),
        dependency("shooting dead enemy", valid_sounds),
        dependency("shooting dead enemy player", valid_sounds),
        Pad(64),
        ),
    Struct("post-combat chatter",
        dependency("alone", valid_sounds),
        dependency("unscathed", valid_sounds),
        dependency("seriously wounded", valid_sounds),
        dependency("seriously wounded re", valid_sounds),
        dependency("massacre", valid_sounds),
        dependency("massacre re", valid_sounds),
        dependency("rout", valid_sounds),
        dependency("rout re", valid_sounds),
        ),
    SIZE=4112,
    )

udlg_def = TagDef("udlg",
    blam_header('udlg'),
    udlg_body,

    ext=".dialogue", endian=">"
    )