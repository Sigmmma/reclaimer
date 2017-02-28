from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef

def get(): return udlg_def

def snd_dependency(name):
    return dependency(name, "snd!")

udlg_body = Struct("tagdata",
    Pad(16),
    Struct("idle",
        snd_dependency("noncombat"),
        snd_dependency("combat"),
        snd_dependency("flee"),
        Pad(48),
        ),

    Struct("involuntary",
        snd_dependency("pain body minor"),
        snd_dependency("pain body maior"),
        snd_dependency("pain shield"),
        snd_dependency("pain falling"),
        snd_dependency("scream fear"),
        snd_dependency("scream pain"),
        snd_dependency("maimed limb"),
        snd_dependency("maimed head"),
        snd_dependency("death quiet"),
        snd_dependency("death violent"),
        snd_dependency("death falling"),
        snd_dependency("death agonizing"),
        snd_dependency("death instant"),
        snd_dependency("death flying"),
        Pad(16),
        ),

    Struct("hurting people",
        snd_dependency("damaged friend"),
        snd_dependency("damaged friend player"),
        snd_dependency("damaged enemy"),
        snd_dependency("damaged enemy cm"),
        Pad(64),
        ),

    Struct("being hurt",
        snd_dependency("hurt friend"),
        snd_dependency("hurt friend re"),
        snd_dependency("hurt friend player"),
        snd_dependency("hurt enemy"),
        snd_dependency("hurt enemy re"),
        snd_dependency("hurt enemy cm"),
        snd_dependency("hurt enemy bullet"),
        snd_dependency("hurt enemy needler"),
        snd_dependency("hurt enemy plasma"),
        snd_dependency("hurt enemy sniper"),
        snd_dependency("hurt enemy grenade"),
        snd_dependency("hurt enemy explosion"),
        snd_dependency("hurt enemy melee"),
        snd_dependency("hurt enemy flame"),
        snd_dependency("hurt enemy shotgun"),
        snd_dependency("hurt enemy vehicle"),
        snd_dependency("hurt enemy mounted weapon"),
        Pad(48),
        ),

    Struct("killing people",
        snd_dependency("killed friend"),
        snd_dependency("killed friend cm"),
        snd_dependency("killed friend player"),
        snd_dependency("killed friend player cm"),
        snd_dependency("killed enemy"),
        snd_dependency("killed enemy cm"),
        snd_dependency("killed enemy player"),
        snd_dependency("killed enemy player cm"),
        snd_dependency("killed enemy covenant"),
        snd_dependency("killed enemy covenant cm"),
        snd_dependency("killed enemy floodcombat"),
        snd_dependency("killed enemy floodcombat cm"),
        snd_dependency("killed enemy floodcarrier"),
        snd_dependency("killed enemy floodcarrier cm"),
        snd_dependency("killed enemy sentinel"),
        snd_dependency("killed enemy sentinel cm"),

        snd_dependency("killed enemy bullet"),
        snd_dependency("killed enemy needler"),
        snd_dependency("killed enemy plasma"),
        snd_dependency("killed enemy sniper"),
        snd_dependency("killed enemy grenade"),
        snd_dependency("killed enemy explosion"),
        snd_dependency("killed enemy melee"),
        snd_dependency("killed enemy flame"),
        snd_dependency("killed enemy shotgun"),
        snd_dependency("killed enemy vehicle"),
        snd_dependency("killed enemy mounted weapon"),
        snd_dependency("killing spree"),
        Pad(48),
        ),

    Struct("player kill responses",
        snd_dependency("player kill cm"),
        snd_dependency("player kill bullet cm"),
        snd_dependency("player kill needler cm"),
        snd_dependency("player kill plasma cm"),
        snd_dependency("player kill sniper cm"),
        snd_dependency("anyone kill grenade cm"),
        snd_dependency("player kill explosion cm"),
        snd_dependency("player kill melee cm"),
        snd_dependency("player kill flame cm"),
        snd_dependency("player kill shotgun cm"),
        snd_dependency("player kill vehicle cm"),
        snd_dependency("player kill mounted weapon cm"),
        snd_dependency("player killing spree cm"),
        Pad(48),
        ),

    Struct("friends dying",
        snd_dependency("friend died"),
        snd_dependency("friend player died"),
        snd_dependency("friend killed by friend"),
        snd_dependency("friend killed by friendly player"),
        snd_dependency("friend enemy"),
        snd_dependency("friend enemy player"),
        snd_dependency("friend covenant"),
        snd_dependency("friend flood"),
        snd_dependency("friend sentinel"),
        snd_dependency("friend betrayed"),
        Pad(32),
        ),

    Struct("shouting",
        snd_dependency("new combat alone"),
        snd_dependency("new enemy recent combat"),
        snd_dependency("old enemy sighted"),
        snd_dependency("unexpected enemy"),
        snd_dependency("dead friend found"),
        snd_dependency("alliance broken"),
        snd_dependency("alliance reformed"),
        snd_dependency("grenade throwing"),
        snd_dependency("grenade sighted"),
        snd_dependency("grenade startle"),
        snd_dependency("grenade danger enemy"),
        snd_dependency("grenade danger self"),
        snd_dependency("grenade danger friend"),
        Pad(32),
        ),

    Struct("group communication",
        snd_dependency("new combat group re"),
        snd_dependency("new combat nearby re"),
        snd_dependency("alert friend"),
        snd_dependency("alert friend re"),
        snd_dependency("alert lost contact"),
        snd_dependency("alert lost contact re"),
        snd_dependency("blocked"),
        snd_dependency("blocked re"),
        snd_dependency("search start"),
        snd_dependency("search query"),
        snd_dependency("search query re"),
        snd_dependency("search report"),
        snd_dependency("search abandon"),
        snd_dependency("search group abandon"),
        snd_dependency("group uncover"),
        snd_dependency("group uncover re"),
        snd_dependency("advance"),
        snd_dependency("advance re"),
        snd_dependency("retreat"),
        snd_dependency("retreat re"),
        snd_dependency("cover"),
        Pad(64),
        ),

    Struct("actions",
        snd_dependency("sighted friend player"),
        snd_dependency("shooting"),
        snd_dependency("shooting vehicle"),
        snd_dependency("shooting berserk"),
        snd_dependency("shooting group"),
        snd_dependency("shooting traitor"),
        snd_dependency("taunt"),
        snd_dependency("taunt re"),
        snd_dependency("flee"),
        snd_dependency("flee re"),
        snd_dependency("free leader died"),
        snd_dependency("attempted flee"),
        snd_dependency("attempted flee re"),
        snd_dependency("lost contact"),
        snd_dependency("hiding finished"),
        snd_dependency("vehicle entry"),
        snd_dependency("vehicle exit"),
        snd_dependency("vehicle woohoo"),
        snd_dependency("vehicle scared"),
        snd_dependency("vehicle collision"),
        snd_dependency("partially sighted"),
        snd_dependency("nothing there"),
        snd_dependency("pleading"),
        Pad(96),
        ),

    Struct("exclamations",
        snd_dependency("surprise"),
        snd_dependency("berserk"),
        snd_dependency("melee attack"),
        snd_dependency("dive"),
        snd_dependency("uncover exclamation"),
        snd_dependency("leap attack"),
        snd_dependency("resurrection"),
        Pad(64),
        ),

    Struct("post-combat actions",
        snd_dependency("celebration"),
        snd_dependency("check body enemy"),
        snd_dependency("check body friend"),
        snd_dependency("shooting dead enemy"),
        snd_dependency("shooting dead enemy player"),
        Pad(64),
        ),

    Struct("post-combat chatter",
        snd_dependency("alone"),
        snd_dependency("unscathed"),
        snd_dependency("seriously wounded"),
        snd_dependency("seriously wounded re"),
        snd_dependency("massacre"),
        snd_dependency("massacre re"),
        snd_dependency("rout"),
        snd_dependency("rout re"),
        ),

    SIZE=4112,
    )

udlg_def = TagDef("udlg",
    blam_header('udlg'),
    udlg_body,

    ext=".dialogue", endian=">"
    )