"""
    OGG Encoder:
        Creation: 06/15/2020
        Last Edit: 06/18/2020 (Zatarita)
"""

import struct
from encoder import OGGEncoder
from supyr_struct.defs.audio.wav import wav_def

class OGG():
    filepath = None
    mode = ""

    def __init__(self, filepath, mode):
        self.filepath = filepath
        self.mode = mode

    def __enter__(self):
        if self.mode == "w":
            return Encoder(self.filepath)

    def __exit__(self, type, value, traceback):
        return

class Encoder():
    bitspersample = 0
    channelcount = 0
    samplerate = 0
    quality = 1
    log = False

    filestream = None

    data = []

    def __init__(self, file):
        self.filestream = open(file, "wb")
    
    #Close the stream
    def close(self):
        if self.filestream:
            self.filestream.close()
    
    #ToDo: Add more formats to load
    
    #Load wave data using supyr_struct definition
    def load_wave(self, file):
        wave = wav_def.build(filepath=file).data
        self.samplerate = wave.wav_format.sample_rate
        self.bitspersample = wave.wav_format.bits_per_sample
        self.channelcount = wave.wav_format.channels
        for x in range(len(wave.wav_chunks)):
            if wave.wav_chunks[x][0].enum_name == "data":
                self.data += wave.wav_chunks[x].data

        if self.bitspersample == 8:
            for item in self.data:
                item -= 127

        if self.bitspersample < 32:
            self.data = self.data_to_float()
            self.data = self.adjust_amplitude()

        if self.channelcount > 1:
            self.data = self.deinterlace(self.data, self.channelcount)
        else:
            self.data = [self.data]

    #convert, write, and close the stream
    def write(self):
        samples  = len(self.data[0])if self.bitspersample == 8 else len(self.data[0])
        output = OGGEncoder(self.data,    self.channelcount, self.samplerate,
                            self.quality, samples,           self.log)
        self.filestream.write(bytearray(output.Output))
        self.close()
        
    #after conversion, float data is between -1 - 1. adjust proportionally to bps (signed) max value
    def adjust_amplitude(self):
        return [self.data[x] / 2 ** (self.bitspersample - 1) for x in range(len(self.data))]

    #OGG uses float values. Convert from 8-bit PCM, or 16 bit PCM
    def data_to_float(self):
        if self.bitspersample == 8: format = "%ib" % float((len(self.data) / (self.bitspersample / 8)))
        else: format = "%ih" % float((len(self.data) / (self.bitspersample / 8)))
        return list(struct.unpack(format, bytearray(self.data)))

    #Split each channel into its own list
    def deinterlace(self, data, channelcount):
        if self.log: print("Deinterlacing channels")
        return [data[i::channelcount] for i in range(channelcount)]
