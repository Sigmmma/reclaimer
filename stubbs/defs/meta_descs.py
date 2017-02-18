from ...common_descs import *
from supyr_struct.defs.tag_def import TagDef
from . import *

################################################################
################################################################
'''-----------------------   Notes   ---------------------------
    If a tag is located in one of the shared resource maps, the
    offset in tag_header will the the index in the resource
    map that the tag is located in and indexed will be 1.
    To determine which resource map the tag is in, it must be
    done based on the tag class.
    bitm- > bitmaps.map
    snd! -> sounds.map
    font, hmt , str#, ustr -> loc.map
'''
################################################################
################################################################

meta_cases = {
    'bitm':bitm.bitm_def.descriptor[1],
    'boom':boom.boom_def.descriptor[1],
    'colo':colo.colo_def.descriptor[1],
    'devc':devc.devc_def.descriptor[1],
    'devi':devi.devi_def.descriptor[1],
    'effe':effe.effe_def.descriptor[1],
    'flag':flag.flag_def.descriptor[1],
    'fog ':fog_.fog__def.descriptor[1],
    'foot':foot.foot_def.descriptor[1],
    'hmt ':hmt_.hmt__def.descriptor[1],
    'hud#':hud_.hud__def.descriptor[1],
    'item':item.item_def.descriptor[1],
    'itmc':itmc.itmc_def.descriptor[1],
    'jpt!':jpt_.jpt__def.descriptor[1],
    'metr':metr.metr_def.descriptor[1],
    'mply':mply.mply_def.descriptor[1],
    'ngpr':ngpr.ngpr_def.descriptor[1],
    'pphy':pphy.pphy_def.descriptor[1],
    'scex':scex.scex_def.descriptor[1],
    'schi':schi.schi_def.descriptor[1],
    'senv':senv.senv_def.descriptor[1],
    'sgla':sgla.sgla_def.descriptor[1],
    'shdr':shdr.shdr_def.descriptor[1],
    'smet':smet.smet_def.descriptor[1],
    'snde':snde.snde_def.descriptor[1],
    'snd!':snd_.snd__def.descriptor[1],
    'soso':soso.soso_def.descriptor[1],
    'sotr':sotr.sotr_def.descriptor[1],
    'Soul':Soul.soul_def.descriptor[1],
    'spla':spla.spla_def.descriptor[1],
    'str#':str_.str__def.descriptor[1],
    'swat':swat.swat_def.descriptor[1],
    'tagc':tagc.tagc_def.descriptor[1],
    'trak':trak.trak_def.descriptor[1],
    'ustr':ustr.ustr_def.descriptor[1],
    'wind':wind.wind_def.descriptor[1],
    }
