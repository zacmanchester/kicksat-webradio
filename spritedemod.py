#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Spritedemod
# Generated: Tue Apr 29 14:45:41 2014
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import sprite

class spritedemod(gr.top_block):

    def __init__(self, input_file_name, output_file, prn0, prn1):
        gr.top_block.__init__(self, "Spritedemod")

        ##################################################
        # Variables
        ##################################################
        self.chip_rate = chip_rate = 64e3

        ##################################################
        # Blocks
        ##################################################
        self.sprite_sprite_decoder_f_0 = sprite.sprite_decoder_f(output_file)
        self.sprite_peak_decimator_ff_0 = sprite.peak_decimator_ff()
        self.sprite_correlator_cf_1 = sprite.correlator_cf(prn0)
        self.sprite_correlator_cf_0 = sprite.correlator_cf(prn1)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, input_file_name, False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_sub_xx_0, 0), (self.sprite_peak_decimator_ff_0, 0))
        self.connect((self.sprite_correlator_cf_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.sprite_correlator_cf_1, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.sprite_peak_decimator_ff_0, 0), (self.sprite_sprite_decoder_f_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.sprite_correlator_cf_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.sprite_correlator_cf_1, 0))


# QT sink close method reimplementation

    def get_chip_rate(self):
        return self.chip_rate

    def set_chip_rate(self, chip_rate):
        self.chip_rate = chip_rate

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()

    if len(args) != 4:
        print "Specify an input .bin file, output .txt file, and two PRN IDs"
        exit()

    output_file = open(args[1], 'w')

    tb = spritedemod(args[0], output_file, int(args[2]), int(args[3]))
    tb.start()
    tb.wait()

    output_file.write('\n')
    output_file.close()
