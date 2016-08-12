from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef
from .objs.schi import SchiTag

schi_body = Struct("tagdata",
    #Radiosity Properties
    radiosity_settings,

    #Shader Type
    material_type,
    FlSEnum16("numeric shader id", DEFAULT=6,
              INCLUDE=shader_id_num),
    Pad(2),

    # Shader Properties
    SInt8("numeric counter limit"),#[0,255]

    Bool8("chicago shader flags",          *trans_shdr_properties),
    BSEnum16("first map type",             *trans_shdr_first_map_type),
    BSEnum16("framebuffer blend function", *framebuffer_blend_modes),
    BSEnum16("framebuffer fade mode",      *trans_shdr_fade_mode),
    BSEnum16("framebuffer fade source",    *function_outputs),

    Pad(2),

    #Lens Flare
    BFloat("lens flare spacing"),#world units
    dependency("lens flare"),
    reflexive("extra layers", extra_layers_block, 4),
    reflexive("maps", chicago_4_stage_maps, 4),
    BBool32("extra flags", *chicago_extra_flags),
    SIZE=108,
    )

    
def get():
    return schi_def

schi_def = TagDef("schi",
    blam_header('schi'),
    schi_body,

    ext=".shader_transparent_chicago",
    endian=">", tag_cls=SchiTag
    )
