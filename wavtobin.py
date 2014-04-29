#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Wavtobin
# Generated: Tue Apr 29 13:29:12 2014
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.filter import pfb
from optparse import OptionParser

class wavtobin(gr.top_block):

    def __init__(self, inputFile, outputFile, samp_rate):
        gr.top_block.__init__(self, "Wavtobin")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate
        self.chip_rate = chip_rate = 64e3

        ##################################################
        # Blocks
        ##################################################
        self.pfb_arb_resampler_xxx_0 = pfb.arb_resampler_ccf(chip_rate/samp_rate, taps=None, flt_size=32)
        self.blocks_wavfile_source_0 = blocks.wavfile_source(inputFile, False)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, outputFile, False)
        self.blocks_file_sink_0.set_unbuffered(False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_wavfile_source_0, 1), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_float_to_complex_0, 0), (self.pfb_arb_resampler_xxx_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.blocks_file_sink_0, 0))


# QT sink close method reimplementation

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.pfb_arb_resampler_xxx_0.set_rate(self.chip_rate/self.samp_rate)

    def get_chip_rate(self):
        return self.chip_rate

    def set_chip_rate(self, chip_rate):
        self.chip_rate = chip_rate
        self.pfb_arb_resampler_xxx_0.set_rate(self.chip_rate/self.samp_rate)

if __name__ == '__main__':
    import wave
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    
    if len(args) != 2:
        print "Specify an input .wav file and output .bin file"
        exit()

    inputFile = args[0]
    outputFile = args[1]

    wav = wave.open(inputFile)
    inputRate = wav.getframerate()
    wav.close()

    tb = wavtobin(inputFile, outputFile, inputRate)

    tb.start()
    tb.wait()
