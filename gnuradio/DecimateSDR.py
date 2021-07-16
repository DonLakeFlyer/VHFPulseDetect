# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Decimatesdr
# GNU Radio version: 3.8.1.0

from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal




class DecimateSDR(gr.hier_block2):
    def __init__(self, samp_rate=3e6):
        gr.hier_block2.__init__(
            self, "Decimatesdr",
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.decimate_1 = decimate_1 = 16
        self.samp_rate2 = samp_rate2 = samp_rate/decimate_1
        self.decimate_2 = decimate_2 = 16
        self.samp_rate3 = samp_rate3 = samp_rate2/decimate_2
        self.taps3 = taps3 = firdes.low_pass_2(1.0, samp_rate3, 1.5e3, 0.3e3, 30.0, firdes.WIN_KAISER, 6.76/2)
        self.taps2 = taps2 = firdes.low_pass_2(1.0, samp_rate2, 1.5e3, 16e3-1.5e3, 60.0, firdes.WIN_BLACKMAN_HARRIS, 6.76)
        self.taps1 = taps1 = firdes.low_pass_2(1.0, samp_rate, 1.5e3, 128e3-1.5e3, 60.0, firdes.WIN_BLACKMAN_HARRIS, 6.76)
        self.decimate_3 = decimate_3 = 4
        self.taps3_len = taps3_len = len(taps3)
        self.taps2_len = taps2_len = len(taps2)
        self.taps1_len = taps1_len = len(taps1)
        self.samp_rate4 = samp_rate4 = samp_rate3/decimate_3

        ##################################################
        # Blocks
        ##################################################
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(decimate_1, taps1, 0, samp_rate)
        self.fir_filter_xxx_0_0_0 = filter.fir_filter_ccf(decimate_3, taps3)
        self.fir_filter_xxx_0_0_0.declare_sample_delay(0)
        self.fir_filter_xxx_0_0 = filter.fir_filter_ccf(decimate_2, taps2)
        self.fir_filter_xxx_0_0.declare_sample_delay(0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.fir_filter_xxx_0_0, 0), (self.fir_filter_xxx_0_0_0, 0))
        self.connect((self.fir_filter_xxx_0_0_0, 0), (self, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.fir_filter_xxx_0_0, 0))
        self.connect((self, 0), (self.freq_xlating_fir_filter_xxx_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samp_rate2(self.samp_rate/self.decimate_1)
        self.set_taps1(firdes.low_pass_2(1.0, self.samp_rate, 1.5e3, 128e3-1.5e3, 60.0, firdes.WIN_BLACKMAN_HARRIS, 6.76))

    def get_decimate_1(self):
        return self.decimate_1

    def set_decimate_1(self, decimate_1):
        self.decimate_1 = decimate_1
        self.set_samp_rate2(self.samp_rate/self.decimate_1)

    def get_samp_rate2(self):
        return self.samp_rate2

    def set_samp_rate2(self, samp_rate2):
        self.samp_rate2 = samp_rate2
        self.set_samp_rate3(self.samp_rate2/self.decimate_2)
        self.set_taps2(firdes.low_pass_2(1.0, self.samp_rate2, 1.5e3, 16e3-1.5e3, 60.0, firdes.WIN_BLACKMAN_HARRIS, 6.76))

    def get_decimate_2(self):
        return self.decimate_2

    def set_decimate_2(self, decimate_2):
        self.decimate_2 = decimate_2
        self.set_samp_rate3(self.samp_rate2/self.decimate_2)

    def get_samp_rate3(self):
        return self.samp_rate3

    def set_samp_rate3(self, samp_rate3):
        self.samp_rate3 = samp_rate3
        self.set_samp_rate4(self.samp_rate3/self.decimate_3)
        self.set_taps3(firdes.low_pass_2(1.0, self.samp_rate3, 1.5e3, 0.3e3, 30.0, firdes.WIN_KAISER, 6.76/2))

    def get_taps3(self):
        return self.taps3

    def set_taps3(self, taps3):
        self.taps3 = taps3
        self.set_taps3_len(len(self.taps3))
        self.fir_filter_xxx_0_0_0.set_taps(self.taps3)

    def get_taps2(self):
        return self.taps2

    def set_taps2(self, taps2):
        self.taps2 = taps2
        self.set_taps2_len(len(self.taps2))
        self.fir_filter_xxx_0_0.set_taps(self.taps2)

    def get_taps1(self):
        return self.taps1

    def set_taps1(self, taps1):
        self.taps1 = taps1
        self.set_taps1_len(len(self.taps1))
        self.freq_xlating_fir_filter_xxx_0.set_taps(self.taps1)

    def get_decimate_3(self):
        return self.decimate_3

    def set_decimate_3(self, decimate_3):
        self.decimate_3 = decimate_3
        self.set_samp_rate4(self.samp_rate3/self.decimate_3)

    def get_taps3_len(self):
        return self.taps3_len

    def set_taps3_len(self, taps3_len):
        self.taps3_len = taps3_len

    def get_taps2_len(self):
        return self.taps2_len

    def set_taps2_len(self, taps2_len):
        self.taps2_len = taps2_len

    def get_taps1_len(self):
        return self.taps1_len

    def set_taps1_len(self, taps1_len):
        self.taps1_len = taps1_len

    def get_samp_rate4(self):
        return self.samp_rate4

    def set_samp_rate4(self, samp_rate4):
        self.samp_rate4 = samp_rate4
