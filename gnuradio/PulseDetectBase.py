# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Pulsedetectbase
# GNU Radio version: 3.8.1.0

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from AirspySource import AirspySource  # grc-generated hier_block
from PhaseLockLoop import PhaseLockLoop  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import signal
import cmath
import math




class PulseDetectBase(gr.hier_block2):
    def __init__(self, final_samp_rate=3e6/(16*16*4), gain=21, pulse_duration=0.015, pulse_freq=146000000, samp_rate=3e6, source_index=0):
        gr.hier_block2.__init__(
            self, "Pulsedetectbase",
                gr.io_signature(0, 0, 0),
                gr.io_signaturev(2, 2, [gr.sizeof_float*1, gr.sizeof_gr_complex*1]),
        )

        ##################################################
        # Parameters
        ##################################################
        self.final_samp_rate = final_samp_rate
        self.gain = gain
        self.pulse_duration = pulse_duration
        self.pulse_freq = pulse_freq
        self.samp_rate = samp_rate
        self.source_index = source_index

        ##################################################
        # Blocks
        ##################################################
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,0,0)
        self.blocks_selector_0.set_enabled(True)
        self.PhaseLockLoop_0 = PhaseLockLoop(
            pllFreqMax=100,
            pulse_duration=pulse_duration,
            samp_rate=final_samp_rate,
            wnT=math.pi/4.0*0+0.635,
        )
        self.AirspySource_0 = AirspySource(
            gain=gain,
            pulse_freq=pulse_freq,
            samp_rate=samp_rate,
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.AirspySource_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.PhaseLockLoop_0, 0), (self, 0))
        self.connect((self.blocks_selector_0, 0), (self.PhaseLockLoop_0, 0))
        self.connect((self.blocks_selector_0, 0), (self, 1))

    def get_final_samp_rate(self):
        return self.final_samp_rate

    def set_final_samp_rate(self, final_samp_rate):
        self.final_samp_rate = final_samp_rate
        self.PhaseLockLoop_0.set_samp_rate(self.final_samp_rate)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.AirspySource_0.set_gain(self.gain)

    def get_pulse_duration(self):
        return self.pulse_duration

    def set_pulse_duration(self, pulse_duration):
        self.pulse_duration = pulse_duration
        self.PhaseLockLoop_0.set_pulse_duration(self.pulse_duration)

    def get_pulse_freq(self):
        return self.pulse_freq

    def set_pulse_freq(self, pulse_freq):
        self.pulse_freq = pulse_freq
        self.AirspySource_0.set_pulse_freq(self.pulse_freq)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.AirspySource_0.set_samp_rate(self.samp_rate)

    def get_source_index(self):
        return self.source_index

    def set_source_index(self, source_index):
        self.source_index = source_index
