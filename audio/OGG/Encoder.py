import ctypes, sys

try:
    from pyogg.vorbis import *
    from pyogg.ogg import ogg_page_eos
except ImportError:
    input("Unable to find pyOGG. \nUse 'pip install pyogg' via cmd on Windows, or 'pip3 install pyogg' via terminal for linux")

#seems to be a bug with pyogg defintion. Redefine to get around.
libvorbis.vorbis_bitrate_flushpacket.argtypes = [vd_p, op_p]
def vorbis_bitrate_flushpacket(vd, op):
        return libvorbis.vorbis_bitrate_flushpacket(vd, op)

"""
    OGG Encoder:
        Creation: 06/15/2020
        Last Edit: 06/18/2020 (Zatarita)

    KNOWN ISSUES:
        Channels above stereo get mixed. (I don't have a multi-channel speaker setup so I cant fix)

    To Do:
        for the love of all things holy, thread this.
"""

class OGGEncoder():
    vorbisinfo = vorbis_info()                                      #Vorbis encoding info
    vorbiscomment = vorbis_comment()                                #Vorbis comment struct
    vorbisencoderstate = vorbis_dsp_state()                         #Encoder state for one instance
    vorbisblock = vorbis_block()                                    #Data for a block of audio

    packet = ogg_packet()                                           #Raw packet of data
    packetcomment = ogg_packet()                                    #Raw packet of data for comments
    packetcode = ogg_packet()                                       #Raw packet of data for code
    page = ogg_page()                                               #Fundamental unit of framing and interleave
    streamstate = ogg_stream_state()                                #Handles current encode/decode state

    Output = []

    def __init__(self, samples, channelcount, samplerate, quality, samplecount, log = False):
        self.channel_count = channelcount                            #Amount of audio channels (mono, l/r, ect)
        self.sample_rate = samplerate                                #How many samples per second
        self.sample_rate = quality                                      #Quality of the OGG compressison
        self.float_samples = samples                                 #16 bit pulse code modulation data (wave)
        self.sample_count = samplecount
        self.encoder_version = "0.1.0"                               #Encoder Version

        self.log = log                                              #For debugging

        self.initializeinterpreter()                                #Initialize the interpreter
        self.encode()                                               #Do the thing
        self.releasevorbis()                                        #Cleanup

    #Initialize functions

    def initializeinterpreter(self):                                #Initialize the OGG interpeter
        if self.log: print("Initializing OGG:")
        if not self.InitializeVorbisInfo(): return                      #Vorbis Info
        if not self.InitializeVorbisState(): return                     #Vorbis State
        if not self.InitializeVorbisComment(): return                   #Vorbis Comment

        #Comments seg fault. I think it might be the similar bug as above.
        #self.AddVorbisComment("Mozz:", "Encoder: v" + self.encoder_version)  #Add Mozz comment and encoder build

        if not self.InitializeVorbisHeaders(): return                   #Vorbis Headers
        if not self.InitializeVorbisBlock(): return                     #Vorbis Block

        if not self.InitializeOggStream(): return                       #OGG stream

    def InitializeVorbisInfo(self):                                 #Vorbis Info initialization
        if self.log: print("\tVorbis Info")
        libvorbis.vorbis_info_init(self.vorbisinfo)                     #Initialize Vorbis Info
        if vorbis_encode_init_vbr(self.vorbisinfo, self.channel_count, self.sample_rate, self.sample_rate):
            self._V_ENCODE_INIT_FAULT()                                 #If failed, handle
            return False
        return True

    def InitializeVorbisState(self):                                #Attempt to initialize analysis state
        if self.log: print("\tVorbis State")
        if vorbis_analysis_init(self.vorbisencoderstate, self.vorbisinfo):
            self._V_ANALYSIS_FAULT()                                    #If failed, handle
            return False
        return True

    def InitializeVorbisComment(self):                              #Initialize Vorbis Comment
        if self.log: print("\tVorbis Comment")
        libvorbis.vorbis_comment_init(self.vorbiscomment)               #No sanity check available.
        return True                                                     #Return true and hope for the best

    def InitializeVorbisHeaders(self):                              #Attempt to create header packets
        if self.log: print("\tVorbis Headers")
        if vorbis_analysis_headerout(self.vorbisencoderstate, self.vorbiscomment, self.packet,
                                                              self.packetcomment, self.packetcode):
            self._OGG_ANALYSIS_HEAD_OUT_FAULT()                         #if failed, handle
            return False
        return True

    def InitializeVorbisBlock(self):                                #Attempt to initialize vorbis block
        if self.log: print("\tVorbis Block")
        if vorbis_block_init(self.vorbisencoderstate, self.vorbisblock):
            self.V_BLOCK_INIT_FAULT()                                   #If failed, handle
            return False
        return True

    def InitializeOggStream(self):                                  #initialize the OGG stream
        if self.log: print("\tOGG Stream")
        if ogg_stream_init(self.streamstate, 0)  != 0:                  #Attempt to initialize ogg stream
            self._OGG_STREAM_FAULT()                                        #if failed, handle

        if ogg_stream_packetin(self.streamstate, self.packet) !=0:      #Attempt to write the packet to stream
            self._OGG_STREAM_FAIL()                                         #if failed, handle
        if ogg_stream_packetin(self.streamstate, self.packetcomment) !=0: #Attempt to write the packet to stream
            self._OGG_STREAM_FAIL()                                         #if failed, handle
        if ogg_stream_packetin(self.streamstate, self.packetcode) !=0:  #Attempt to write the packet to stream
            self._OGG_STREAM_FAIL()                                         #if failed, handle

        while True:
            result = ogg_stream_flush(self.streamstate, self.page)      #Get a page from the stream (regardless of size)
            if result == 0: break                                           #If there are no more pages left, stop
            self.Output += self.page.header[0:self.page.header_len]     #Add the page header to the output
            self.Output += self.page.body[0:self.page.body_len]         #Add the page body to the output

    def releasevorbis(self):                                        #Cleanup Vorbis
        if self.log: print("\nFreeing Resources")
        ogg_stream_clear(self.streamstate)                              #Clear OGG stream
        vorbis_block_clear(self.vorbisblock)                            #Clear Vorbis Block
        vorbis_dsp_clear(self.vorbisencoderstate)                       #Clear Encoder State
        vorbis_comment_clear(self.vorbiscomment)                        #Clear Vorbis Comment
        #vorbis_info_clear(self.vorbisinfo) Bugged?                     #Clear Vorbis Info

    #Encoder

    def encode(self):                                               #Encode the data
        if self.log: print("Encoding Data")
        BufferSize = 1024                                               #Size of the buffer that is requested from encoder
        eos = False                                                     #End of stream flag

        while True:                                                     #While there is audio left to send to buffers
            if self.log:
                sys.stdout.write("\r\tRemaining Samples:                          ")
                sys.stdout.write("\r\tRemaining Samples: " + str(self.sample_count))

            if self.sample_count == 0:                                   #If we reached the end of the input
                vorbis_analysis_wrote(self.vorbisencoderstate, 0)           #Submit an empty buffer to signal end
                break                                                       #Move on
            else:                                                       #If there is more audio
                                                                        #Request a buffer to interface with vorbis
                Buffer = vorbis_analysis_buffer(self.vorbisencoderstate, self.sample_count)

                for c in range(self.channel_count):                      #For each sample in each channel
                    for i in range(self.sample_count):                       #Write the samples to the received buffer
                        if i > BufferSize:                                      #If we've filled the buffer
                            break                                                   #Move on
                        Buffer[c][i] = self.float_samples[c][i]              #Submit the float data to the array

                if self.sample_count < BufferSize:                       #If we didn't write a full buffers worth
                    vorbis_analysis_wrote(self.vorbisencoderstate, self.sample_count)
                    self.sample_count = 0                                    #Tell vorbis how much we did write
                else:                                                   #If we did write a full buffers worth
                    for i in range(self.channel_count):                      #For each channel
                        del self.float_samples[i][:BufferSize]                   #Delete the used samples
                    self.sample_count -= BufferSize                          #Decrement the count
                    vorbis_analysis_wrote(self.vorbisencoderstate, BufferSize)#Tell vorbis we used a full buffer

                                                                        #While there are still blocks to process
        while vorbis_analysis_blockout(self.vorbisencoderstate, self.vorbisblock) == 1:
            vorbis_analysis(self.vorbisblock, None)                     #Analyze the block
            vorbis_bitrate_addblock(self.vorbisblock)                   #Push the block
                                                                        #while there are packets to process
            while vorbis_bitrate_flushpacket(self.vorbisencoderstate, self.packet):
                ogg_stream_packetin(self.streamstate, self.packet)          #Get a packet
                while not eos:                                              #While there is more to stream
                    result = ogg_stream_pageout(self.streamstate, self.page)    #Get a page
                    if result == 0: break                                           #if there are no pages, get next packet
                    self.Output += self.page.header[0:self.page.header_len] #Write output
                    self.Output += self.page.body[0:self.page.body_len]     #Write Output
                    if ogg_page_eos(self.page): eos = True                  #If at end of stream, quit looping

    #Quality of life functions:

    def AddVorbisComment(self, key, value = ""):                    #Add a comment to the stream (Bugged)
        if self.log: print("Adding Vorbis Comment: " + key + " " + value)
        if value == "":                                                 #if there was only one arg
            libvorbis.vorbis_comment_add(self.vorbiscomment, key)           #add the comment
        else:                                                           #If tag and comment ("key", "value")
            libvorbis.vorbis_comment_add_tag(self.vorbiscomment, key, value)#add the comment

    def ToByteArray(self):                                          #Convert to byte array
        return bytearray(self.Output)


    #Error "Handling" functions.
    #ToDo : actually handle the error instead of just print.

    def _GENERIC(self):
        print("An unknown error has occured.")
        self.__exit__()

    def _OGG_STREAM_FAULT(self):
        print("Unable to initialize the ogg stream.")
        self.__exit__()

    def _OGG_ANALYSIS_HEAD_OUT_FAULT(self):
        print("OGG Header packet creation failed.")
        self.__exit__()

    def _OGG_STREAM_FAIL(self):
        print("Unable to write packet to stream.")
        self.__exit__()

    def _V_BLOCK_INIT_FAULT(self):
        print("Unable to initialize the vorbis block.")
        self.__exit__()

    def _V_ANALYSIS_FAULT(self):
        print("Unable to initialize the encoders analysis state.")
        self.__exit__()

    def _V_ENCODE_INIT_FAULT(self):
        print("Internal logic Fault. Likely invalid quality request. (-0.1 - 1.0)")
        self.__exit__()
