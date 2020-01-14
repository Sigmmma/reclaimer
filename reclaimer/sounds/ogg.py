#
# This file is part of Reclaimer.
#
# For authors and copyright check AUTHORS.TXT
#
# Reclaimer is free software under the GNU General Public License v3.0.
# See LICENSE for more information.
#

class VorbisBitrateInfo:
    '''
    Intermediary class for storing bitrate info to pass to vorbis compression
    functions.

    Combinations of nominal, lower, upper values carry the following
    implications:
      all three set to the same value:
        implies a fixed rate bitstream
      only nominal set:
        implies a VBR stream that nominals the nominal bitrate. No hard
        upper/lower limit
      upper and or lower set:
        implies a VBR bitstream that obeys the bitrate limits. nominal
        may also be set to give a nominal rate.
      none set:
        the coder does not care to speculate.
    '''
    lower = -1
    upper = -1
    nominal = -1

    # compression base quality [-0.1, 1.0]
    quality = None

    use_quality = False

    def __init__(self, nominal=-1, lower=-1, upper=-1, quality=0.5):
        '''
        See class documentation for variable descriptions.
        '''
        if quality is not None:
            self.set_bitrate_quality(quality)
        else:
            self.set_bitrate_variable(nominal, upper, lower)

    def set_bitrate_fixed(self, bitrate):
        '''
        Sets a fixed bitrate to the requested number.
        '''
        self.upper = self.nominal = self.lower = bitrate
        self.use_quality = False

    def set_bitrate_variable(self, nominal, upper=-1, lower=-1):
        '''
        Sets a variable bitrate based on the nominal and
        optionally upper and lower numbers.
        Check class docstring for further detail.
        '''
        self.nominal = nominal
        self.upper = upper
        self.lower = lower
        self.use_quality = False

    def set_bitrate_quality(self, quality):
        '''
        Sets a bitrate using the quality float.
        '''
        self.quality = min(1.0, max(-0.1, float(quality)))
        self.use_quality = True
