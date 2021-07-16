# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Phaselockloop
# GNU Radio version: 3.8.1.0

from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
import cmath
import math




class PhaseLockLoop(gr.hier_block2):
    def __init__(self, pllFreqMax=100, pulse_duration=0.015, samp_rate=2929, wnT=math.pi/4.0*0+0.635):
        gr.hier_block2.__init__(
            self, "Phaselockloop",
                gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
                gr.io_signature(1, 1, gr.sizeof_float*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.pllFreqMax = pllFreqMax
        self.pulse_duration = pulse_duration
        self.samp_rate = samp_rate
        self.wnT = wnT

        ##################################################
        # Variables
        ##################################################
        self.inter_pulse_duration = inter_pulse_duration = 2
        self.fmin = fmin = -pllFreqMax
        self.fmax = fmax = pllFreqMax

        ##################################################
        # Blocks
        ##################################################
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(1)
        self.blocks_moving_average_xx_0_0 = blocks.moving_average_cc(int(samp_rate*pulse_duration), 1, int(samp_rate*inter_pulse_duration/10.0), 1)
        self.blocks_complex_to_mag_0_0 = blocks.complex_to_mag(1)
        self.analog_pll_refout_cc_0 = analog.pll_refout_cc(wnT, math.pi/(samp_rate/2.0)*fmax, math.pi/(samp_rate/2.0)*fmin)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_pll_refout_cc_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        self.connect((self.blocks_complex_to_mag_0_0, 0), (self, 0))
        self.connect((self.blocks_moving_average_xx_0_0, 0), (self.blocks_complex_to_mag_0_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.blocks_moving_average_xx_0_0, 0))
        self.connect((self, 0), (self.analog_pll_refout_cc_0, 0))
        self.connect((self, 0), (self.blocks_multiply_conjugate_cc_0, 0))

    def get_pllFreqMax(self):
        return self.pllFreqMax

    def set_pllFreqMax(self, pllFreqMax):
        self.pllFreqMax = pllFreqMax
        self.set_fmax(self.pllFreqMax)
        self.set_fmin(-self.pllFreqMax)

    def get_pulse_duration(self):
        return self.pulse_duration

    def set_pulse_duration(self, pulse_duration):
        self.pulse_duration = pulse_duration
        self.blocks_moving_average_xx_0_0.set_length_and_scale(int(self.samp_rate*self.pulse_duration), 1)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_pll_refout_cc_0.set_max_freq(math.pi/(self.samp_rate/2.0)*self.fmax)
        self.analog_pll_refout_cc_0.set_min_freq(math.pi/(self.samp_rate/2.0)*self.fmin)
        self.blocks_moving_average_xx_0_0.set_length_and_scale(int(self.samp_rate*self.pulse_duration), 1)

    def get_wnT(self):
        return self.wnT

    def set_wnT(self, wnT):
        self.wnT = wnT
        self.analog_pll_refout_cc_0.set_loop_bandwidth(self.wnT)

    def get_inter_pulse_duration(self):
        return self.inter_pulse_duration

    def set_inter_pulse_duration(self, inter_pulse_duration):
        self.inter_pulse_duration = inter_pulse_duration

    def get_fmin(self):
        return self.fmin

    def set_fmin(self, fmin):
        self.fmin = fmin
        self.analog_pll_refout_cc_0.set_min_freq(math.pi/(self.samp_rate/2.0)*self.fmin)

    def get_fmax(self):
        return self.fmax

    def set_fmax(self, fmax):
        self.fmax = fmax
        self.analog_pll_refout_cc_0.set_max_freq(math.pi/(self.samp_rate/2.0)*self.fmax)
