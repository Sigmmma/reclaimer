from ...hek.defs.obje import *

def get():
    return obje_def

# replace the model animations dependency with an open sauce one
obje_attrs = dict(obje_attrs)
obje_attrs[8] = dependency('animation graph', valid_model_animations_yelo)

obje_body = Struct('tagdata',
    obje_attrs
    )

obje_def = TagDef("obje",
    blam_header('obje'),
    obje_body,

    ext=".object", endian=">", tag_cls=HekTag
    )
