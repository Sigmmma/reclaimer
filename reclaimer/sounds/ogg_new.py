"""
    OGG Encoder:
        Creation: 06/15/2020
        Last Edit: 06/18/2020 (Zatarita)
"""

import struct
from encoder import OGGEncoder
from supyr_struct.defs.audio.wav import wav_def

class OGG():
    file_path = None
    mode = ""

    def __init__(self, filepath, mode):
        self.file_path = filepath
        self.mode = mode

    def __enter__(self):
        if self.mode == "w":
            return Encoder(self.file_path)

    def __exit__(self, type, value, traceback):
        return

class Encoder():
    bits_per_sample = 0
    channels = 0
    sample_rate = 0
    quality = 1
    log = False

    file_stream = None

    data = []

    def __init__(self, file):
        self.file_stream = open(file, "wb")

    #Close the stream
    def close(self):
        if self.file_stream:
            self.file_stream.close()

    #ToDo: Add more formats to load

    #Load wave data using supyr_struct definition
    def load_wave(self, file):
        wave = wav_def.build(filepath=file).data
        self.sample_rate = wave.wav_format.sample_rate
        self.bits_per_sample = wave.wav_format.bits_per_sample
        self.channels = wave.wav_format.channels
        for x in range(len(wave.wav_chunks)):
            if wave.wav_chunks[x][0].enum_name == "data":
                self.data += wave.wav_chunks[x].data

        #When bps are 8, value is unsigned. We're going to sign it
        if self.bits_per_sample == 8:
            for item in self.data:
                item -= 127

        #When bps are less than 32, we need to convert the values to 32 bit floats
        if self.bits_per_sample < 32:
            self.data = self.data_to_float()
            self.data = self.adjust_amplitude()

        #Split the channels into a list of lists. [[Channel #], [Samples]]
        if self.channels > 1:
            self.data = self.deinterlace(self.data, self.channels)
        else:
            self.data = [self.data]

    #convert, write, and close the stream
    def write(self):
        samples  = len(self.data[0])
        print (len(self.data[0]))
        encoding = OGGEncoder(self.data,    self.channels, self.sample_rate,
                              self.quality,  samples,           self.log)
        self.file_stream.write(bytearray(encoding.output))
        self.close()


    #after conversion, float data is between -1 - 1. adjust to percent of bit per sec(signed) max value
    def adjust_amplitude(self):
        return [self.data[x] / 2 ** (self.bits_per_sample - 1) for x in range(len(self.data))]

    #ogg uses float values. Convert from 8-bit PCM, or 16 bit PCM
    def data_to_float(self):
        if self.bits_per_sample == 8: format = "%ib" % float((len(self.data) / (self.bits_per_sample / 8)))
        else: format = "%ih" % float((len(self.data) / (self.bits_per_sample / 8)))
        return list(struct.unpack(format, bytearray(self.data)))

    #Split each channel into its own list
    def deinterlace(self, data, channels):
        if self.log: print("Deinterlacing channels")
        return [data[i::channels] for i in range(channels)]
