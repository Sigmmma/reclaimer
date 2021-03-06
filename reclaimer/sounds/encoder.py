"""
    OGG Encoder:
        Creation: 06/15/2020
        Last Edit: 06/18/2020 (Zatarita)

    KNOWN ISSUES:
        Channels above stereo get mixed. (I don't have a multi-channel speaker setup so I cant fix)

    To Do:
        for the love of all things holy, thread this.
"""

import sys

try:
    from pyogg.vorbis import *
    from pyogg.ogg import ogg_page_eos
except ImportError:
    input("Unable to find pyOGG. \nUse 'pip install pyogg' via cmd on Windows, or 'pip3 install pyogg' via terminal for linux")



#seems to be a bug with pyogg defintion. Redefine to get around.
libvorbis.vorbis_bitrate_flushpacket.argtypes = [vd_p, op_p]

def vorbis_bitrate_flushpacket(vd, op):
        return libvorbis.vorbis_bitrate_flushpacket(vd, op)



class OGGEncoder():
    v_info = vorbis_info()
    v_comment = vorbis_comment()
    v_encoder_state = vorbis_dsp_state()
    v_block = vorbis_block()

    packet = ogg_packet()
    packet_comment = ogg_packet()
    packet_code = ogg_packet()
    page = ogg_page()
    stream_state = ogg_stream_state()

    output = []

    def __init__(self, samples, channelcount, samplerate, quality, samplecount, log = False):
        self.channel_count = channelcount
        self.sample_rate = samplerate
        self.quality = quality
        self.float_samples = samples
        self.sample_count = samplecount
        self.encoder_version = "0.1.0"

        self.log = log

        self.initialize_interpreter()
        self.encode()
        self.release_vorbis()

    #Initialize functions

    def initialize_interpreter(self):
        if self.log: print("Initializing OGG:")
        self.initialize_vorbis_info()
        self.initialize_vorbis_state()
        self.initialize_vorbis_comment()

        #Comments seg fault. I think it might be the similar bug as above.
        #self.add_vorbis_comment("Mozz:", "Encoder: v" + self.encoder_version)

        self.initialize_vorbis_headers()
        self.initialize_vorbis_block()

        self.initialize_ogg_stream()

    def initialize_vorbis_info(self):
        if self.log: print("\tVorbis Info")
        libvorbis.vorbis_info_init(self.v_info)
        if vorbis_encode_init_vbr(self.v_info, self.channel_count, self.sample_rate, self.quality):
            raise EncodingError(" Unable to initialize vorbis info")

    def initialize_vorbis_state(self):
        if self.log: print("\tVorbis State")
        if vorbis_analysis_init(self.v_encoder_state, self.v_info):
            raise EncodingError(" Unable to initialize vorbis state")

    def initialize_vorbis_comment(self):
        if self.log: print("\tVorbis Comment")
        libvorbis.vorbis_comment_init(self.v_comment)
        #No sanity check available. Hope for the best
        return True

    def initialize_vorbis_headers(self):
        if self.log: print("\tVorbis Headers")
        if vorbis_analysis_headerout(self.v_encoder_state, self.v_comment, self.packet,
                                     self.packet_comment,  self.packet_code):
            raise EncodingError(" Unable to initialize vorbis headers")

    def initialize_vorbis_block(self):
        if self.log: print("\tVorbis Block")
        if vorbis_block_init(self.v_encoder_state, self.v_block):
            raise EncodingError(" Unable to initialize vorbis block")

    def initialize_ogg_stream(self):
        if self.log: print("\tOGG Stream")
        if ogg_stream_init(self.stream_state, 0)  != 0:
            raise EncodingError(" Unable to initialize ogg stream")

        if ogg_stream_packetin(self.stream_state, self.packet) !=0:
            raise EncodingError(" Unable to write packet to stream")
        if ogg_stream_packetin(self.stream_state, self.packet_comment) !=0:
            raise EncodingError(" Unable to write comment packet to stream")
        if ogg_stream_packetin(self.stream_state, self.packet_code) !=0:
            raise EncodingError(" Unable to write code packet to stream")

        while True:
            result = ogg_stream_flush(self.stream_state, self.page)
            if result == 0: break
            self.output += self.page.header[0:self.page.header_len]
            self.output += self.page.body[0:self.page.body_len]

    #Incase of exception, close stream. If buffers never cleared it can carry to next encoding
    def __exit__(self, x, y, z):
        self.releasevorbis()

    def release_vorbis(self):
        ogg_stream_clear(self.stream_state)
        vorbis_block_clear(self.v_block)
        vorbis_dsp_clear(self.v_encoder_state)
        vorbis_comment_clear(self.v_comment)
        #vorbis_info_clear(self.v_info)    Bugged? might be an issue actually

    #Encoder

    def encode(self):
        if self.log: print("Encoding Data")
        buffer_size = 1024
        eos = False

        while True:
            if self.log:
                sys.stdout.write("\r\tRemaining Samples:                          ")
                sys.stdout.write("\r\tRemaining Samples: " + str(self.sample_count))

            if self.sample_count == 0:
                vorbis_analysis_wrote(self.v_encoder_state, 0)
                break
            else:
                buffer = vorbis_analysis_buffer(self.v_encoder_state, self.sample_count)

                for c in range(self.channel_count):
                    for i in range(self.sample_count):
                        if i > buffer_size:
                            break
                        buffer[c][i] = self.float_samples[c][i]

                if self.sample_count < buffer_size:
                    vorbis_analysis_wrote(self.v_encoder_state, self.sample_count)
                    self.sample_count = 0
                else:
                    for i in range(self.channel_count):
                        del self.float_samples[i][:buffer_size]
                    self.sample_count -= buffer_size
                    vorbis_analysis_wrote(self.v_encoder_state, buffer_size)

        while vorbis_analysis_blockout(self.v_encoder_state, self.v_block) == 1:
            vorbis_analysis(self.v_block, None)
            vorbis_bitrate_addblock(self.v_block)

            while vorbis_bitrate_flushpacket(self.v_encoder_state, self.packet):
                ogg_stream_packetin(self.stream_state, self.packet)
                while not eos:
                    result = ogg_stream_pageout(self.stream_state, self.page)
                    if result == 0: break
                    self.output += self.page.header[0:self.page.header_len]
                    self.output += self.page.body[0:self.page.body_len]
                    if ogg_page_eos(self.page): eos = True
        if self.log: print("\nFreeing Resources")

    #Quality of life functions:

    def add_vorbis_comment(self, key, value = ""):
        if self.log: print("Adding Vorbis Comment: " + key + " " + value)
        if value == "":
            libvorbis.vorbis_comment_add(self.v_comment, key)
        else:
            libvorbis.vorbis_comment_add_tag(self.v_comment, key, value)

#Exceptions

class EncodingError(Exception):
    def __init__(self, message):
        self.message = message
