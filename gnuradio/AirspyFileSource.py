# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Airspyfilesource
# GNU Radio version: 3.8.1.0

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from DecimateSDR import DecimateSDR  # grc-generated hier_block
from gnuradio import blocks
import pmt
from gnuradio import gr
from gnuradio.filter import firdes
import signal




class AirspyFileSource(gr.hier_block2):
    def __init__(self, samp_rate=3e6):
        gr.hier_block2.__init__(
            self, "Airspyfilesource",
                gr.io_signature(0, 0, 0),
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.samp_rate = samp_rate

        ##################################################
        # Blocks
        ##################################################
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/parallels/vhf.dat', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.DecimateSDR_0 = DecimateSDR(
            samp_rate=3e6,
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.DecimateSDR_0, 0), (self, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.DecimateSDR_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
