from ..common_descs import *
from .objs.tag import H2Tag
from supyr_struct.defs.tag_def import TagDef

sound_classes = (
    ("projectile impact", 0),
    ("projectile detonation", 1),
    ("projectile flyby", 2),

    ("weapon fire", 4),
    ("weapon ready", 5),
    ("weapon reload", 6),
    ("weapon empty", 7),
    ("weapon charge", 8),
    ("weapon overheat", 9),
    ("weapon idle", 10),
    ("weapon melee", 11),
    ("weapon animation", 12),
    ("object impacts", 13),
    ("particle impacts", 14),

    ("unit footsteps", 18),
    ("unit dialog", 19),
    ("unit animation", 20),

    ("vehicle collision", 22),
    ("vehicle engine", 23),
    ("vehicle animation", 20),

    ("device door", 26),
    ("device machinery", 28),
    ("device stationary", 29),

    ("music", 32),
    ("ambient nature", 33),
    ("ambient machinery", 34),

    ("huge ass", 36),
    ("object looping", 37),
    ("cinematic music", 38),

    ("cortana mission", 45),
    ("cortana cinematic", 46),
    ("mission dialog", 47),
    ("cinematic dialog", 48),
    ("scripted cinematic foley", 49),
    ("game event", 50),
    ("ui", 51),
    ("test", 52),
    ("multilingual test", 53),
    )

promotion_rule = Struct("promotion rule",
    UEnum16("pitch ranges"),
    UInt16("maximum playing count"),
    float_sec("supression time"),
    )

permutation = Struct("permutation",
    UEnum16("language",
        "english",
        "japanese",
        "german",
        "french",
        "spanish",
        "italian",
        "korean",
        "chinese",
        "portugese",
        ),
    Pad(2),
    ascii_str_varlen("name"),
    Float("skip fraction"),
    Float("gain"),
    h2_rawdata_ref("samples", max_size=0),
    SIZE=32
    )


from_to_cents = QStruct("",
    SInt16("from", GUI_NAME=''),
    SInt16("to"),
    SIDETIP="cents"
    )

pitch_range = Struct("pitch range",
    ascii_str_varlen("name"),
    SInt16("natural pitch", SIDETIP="cents"),
    Pad(2),
    QStruct("bend bounds", INCLUDE=from_to_cents),
    Pad(8),
    h2_reflexive("permutations", permutation),
    SIZE=32
    )

platform_parameter = Struct("platform parameter",
    )

snd__body = Struct("tagdata",
    Bool32("flags",
        "fit to adpcm blocksize",
        "split long sounds into permutations",
        "always spatialize",
        "never obstruct",
        {NAME: "INTERNAL DONT TOUCH", EDITABLE:False},
        "use huge sound transmission"
        "link count to owner unit",
        "pitch range is language",
        "dont use sound class speaker flags",
        "dont use lipsync data",
        ),
    UEnum8("class", *sound_classes),
    UEnum8("sample rate",
        {NAME: "khz_22", GUI_NAME: "22kHz"},
        {NAME: "khz_44", GUI_NAME: "44kHz"},
        {NAME: "khz_32", GUI_NAME: "32kHz"},
        ),
    SEnum16("import type",
        "unknown",
        "single shot",
        "single layer",
        "multi layer",
        ),
    float_wu("minimum distance"),
    float_wu("maximum distance"),
    float_zero_to_one("skip fraction"),
    Float("maximum bend per second", SIDETIP="cents"),

    Struct("randomization",
        Float("gain base"),
        Float("gain variance"),
        QStruct("random pitch bounds", INCLUDE=from_to_cents),
        ),

    Struct("directional sounds",
        float_rad("inner cone angle"),
        float_rad("outer cone angle"),
        Float("outer cone gain", SIDETIP="dB"),
        ),

    Struct("scripted location override",
        Bool32("flags",
            "override azimuth",
            "override 3d gain",
            "override speaker gain",
            ),
        Float("azimuth"),
        Float("positional gain", SIDETIP="dB"),
        Float("first person gain", SIDETIP="dB"),
        ),

    Struct("scale modifiers",
        QStruct("gain", INCLUDE=from_to, SIDETIP="dB"),
        QStruct("pitch", INCLUDE=from_to_cents),
        QStruct("skip fraction", INCLUDE=from_to),
        ),

    Pad(2),
    UEnum8("encoding",
        "mono",
        "stereo",
        ),
    UEnum8("compression",
        "none (big endian)",
        "xbox adpcm",
        "ima adpcm",
        "none (little endian)",
        "wma",
        ),

    h2_reflexive("promotion rules", promotion_rule),
    Pad(12),  # h2_reflexive("unknown0", unknown0_struct),
    Pad(24),
    h2_reflexive("pitch ranges", pitch_range),
    h2_reflexive("platform parameters", platform_parameter),
    Pad(12),  # h2_reflexive("unknown1", unknown1_struct),
    SIZE=172
    )


def get():
    return snd__def

snd__def = TagDef("snd!",
    h2_blam_header('snd!'),
    snd__body,
    ext=".sound", endian="<", tag_cls=H2Tag
    )
