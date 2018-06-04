from ...hek.defs.soso import *
from .shdr import *
from supyr_struct.defs.tag_def import TagDef

bump_properties = Struct("bump properties",
    Float("bump scale"),
    dependency_stubbs("bump map", "bitm"),
    )

soso_attrs = Struct("soso attrs",
    #Model Shader Properties
    model_shader,
        
    Pad(16),
    #Color-Change
    SEnum16("color change source", *function_names),
        
    Pad(30),
    #Self-Illumination
    self_illumination,
        
    Pad(12),
    #Diffuse, Multipurpose, and Detail Maps
    maps,

    # this padding is the reflexive for the OS shader model extension
    Pad(12),

    #Texture Scrolling Animation
    texture_scrolling,
                   
    Pad(8),
    #Reflection Properties
    reflection,

    Pad(16),
    bump_properties,
    SIZE=440
    )

soso_body = Struct("tagdata",
    shdr_attrs,
    soso_attrs
    )

def get():
    return soso_def

soso_def = TagDef("soso",
    blam_header_stubbs('soso', 3),
    soso_body,

    ext=".shader_model", endian=">"  # increment to differentiate it from halo antr
    )
