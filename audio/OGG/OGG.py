import struct
from Encoder import OGGEncoder
from supyr_struct.defs.audio.wav import wav_def

"""
    OGG Encoder:
        Creation: 06/15/2020
        Last Edit: 06/18/2020 (Zatarita)
"""

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

    Data = []

    def __init__(self, file):
        self.filestream = open(file, "wb")

    def __del__(self):
        if self.filestream:
            self.filestream.close()

    def loadwave(self, file):
        wave = wav_def.build(filepath=file).data
        self.samplerate = wave.wav_format.sample_rate
        self.bitspersample = wave.wav_format.bits_per_sample
        self.channelcount = wave.wav_format.channels
        for x in range(len(wave.wav_chunks)):
            if wave.wav_chunks[x][0].enum_name == "data":
                self.Data += wave.wav_chunks[x].data

        if self.bitspersample == 8: #less than 16 bits per sample is unsigned
            for item in self.Data:
                item -= 127

        if self.bitspersample < 32:
            self.Data = self.DataToFloat()
            self.Data = self.AdjustAmplitude()

        if self.channelcount > 1:
            self.Data = self.Deinterlace(self.Data, self.channelcount)
        else:
            self.Data = [self.Data]

    def write(self):
        samples  = len(self.Data[0])if self.bitspersample == 8 else len(self.Data[0])
        output = OGGEncoder(self.Data,    self.channelcount, self.samplerate,
                            self.quality, samples,           self.log)
        self.filestream.write(bytearray(output.Output))

    def AdjustAmplitude(self):
        return [self.Data[x] / 2 ** (self.bitspersample - 1) for x in range(len(self.Data))]

    def DataToFloat(self):
        if self.bitspersample == 8: format = "%ib" % float((len(self.Data) / (self.bitspersample / 8)))
        else: format = "%ih" % float((len(self.Data) / (self.bitspersample / 8)))
        return list(struct.unpack(format, bytearray(self.Data)))

    def Deinterlace(self, data, channelcount):
        if self.log: print("Deinterlacing channels")
        return [data[i::channelcount] for i in range(channelcount)]         #(Python, I love you sometimes.)
