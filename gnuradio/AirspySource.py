# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Airspysource
# GNU Radio version: 3.8.1.0

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from DecimateSDR import DecimateSDR  # grc-generated hier_block
from gnuradio import gr
from gnuradio.filter import firdes
import signal
import osmosdr
import time




class AirspySource(gr.hier_block2):
    def __init__(self, gain=21, pulse_freq=146000000, samp_rate=3e6):
        gr.hier_block2.__init__(
            self, "Airspysource",
                gr.io_signature(0, 0, 0),
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.gain = gain
        self.pulse_freq = pulse_freq
        self.samp_rate = samp_rate

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + 'airspy=0,sensitivity'
        )
        self.osmosdr_source_0.set_clock_source('gpsdo', 0)
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(pulse_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_gain(gain, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        self.DecimateSDR_0 = DecimateSDR(
            samp_rate=3e6,
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.DecimateSDR_0, 0), (self, 0))
        self.connect((self.osmosdr_source_0, 0), (self.DecimateSDR_0, 0))

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.osmosdr_source_0.set_gain(self.gain, 0)

    def get_pulse_freq(self):
        return self.pulse_freq

    def set_pulse_freq(self, pulse_freq):
        self.pulse_freq = pulse_freq
        self.osmosdr_source_0.set_center_freq(self.pulse_freq, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
