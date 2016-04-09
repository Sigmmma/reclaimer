from ...common_descriptors import *
from supyr_struct.defs.tag_def import TagDef

snde_body = Struct("Data",
    Pad(4),
    BUInt16("priority"),
    Pad(2),
    BFloat("room intensity"),
    BFloat("room intensity hf"),
    BFloat("room rolloff"),
    BFloat("decay time"),
    BFloat("decay hf ratio"),
    BFloat("reflections intensity"),
    BFloat("reflections delay"),
    BFloat("reverb intensity"),
    BFloat("reverb delay"),
    BFloat("diffusion"),
    BFloat("density"),
    BFloat("hf reference"),
    SIZE=72,
    )

def get():
    return snde_def

snde_def = TagDef(
    blam_header('snde'),
    snde_body,
    
    NAME="sound_environment",
    
    ext=".sound_environment", def_id="snde", endian=">"
    )
