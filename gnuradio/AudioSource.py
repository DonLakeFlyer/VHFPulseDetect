# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Audiosource
# GNU Radio version: 3.8.1.0

from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal




class AudioSource(gr.hier_block2):
    def __init__(self):
        gr.hier_block2.__init__(
            self, "Audiosource",
                gr.io_signature(0, 0, 0),
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=4000,
                decimation=48000,
                taps=None,
                fractional_bw=None)
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_float*1)
        self.blocks_magphase_to_complex_0 = blocks.magphase_to_complex(1)
        self.audio_source_0 = audio.source(48000, 'hw:CARD=Audio,DEV=0', True)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.audio_source_0, 0), (self.blocks_magphase_to_complex_0, 0))
        self.connect((self.blocks_magphase_to_complex_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_null_source_0, 0), (self.blocks_magphase_to_complex_0, 1))
        self.connect((self.rational_resampler_xxx_0, 0), (self, 0))
