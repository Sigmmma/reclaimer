import traceback

from reclaimer.sounds import util, constants

__all__ = ("compile_sound", "compile_permutation",)


def compile_permutation(pitch_range, jma_anim, ignore_size_limits=False,
                        endian=">"):
    '''
    Compiles the provided BlamSoundPermutation into the
    provided snd! pitch range block.
    '''
    errors = []

    return errors


def compile_sound(snd__tag, blam_sound_bank, ignore_size_limits=False,
                  update_mode=constants.SOUND_COMPILE_MODE_PRESERVE):
    errors = []

    return errors
