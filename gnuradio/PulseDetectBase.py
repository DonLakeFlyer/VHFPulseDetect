# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Pulsedetectbase
# Generated: Sat Aug 29 11:04:18 2020
##################################################


from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
import cmath
import math
import osmosdr
import time


class PulseDetectBase(gr.hier_block2):

    def __init__(self, final_decimation=4, gain=21, pllFreqMax=100, pulse_duration=0.015, pulse_freq=146000000, samp_rate=3e6, wnT=math.pi/4.0*0+0.635):
        gr.hier_block2.__init__(
            self, "Pulsedetectbase",
            gr.io_signature(0, 0, 0),
            gr.io_signaturev(2, 2, [gr.sizeof_float*1, gr.sizeof_gr_complex*1]),
        )

        ##################################################
        # Parameters
        ##################################################
        self.final_decimation = final_decimation
        self.gain = gain
        self.pllFreqMax = pllFreqMax
        self.pulse_duration = pulse_duration
        self.pulse_freq = pulse_freq
        self.samp_rate = samp_rate
        self.wnT = wnT

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
        self.decimate_3 = decimate_3 = final_decimation
        self.taps3_len = taps3_len = len(taps3)
        self.taps2_len = taps2_len = len(taps2)
        self.taps1_len = taps1_len = len(taps1)
        self.samp_rate4 = samp_rate4 = samp_rate3/decimate_3
        self.inter_pulse_duration = inter_pulse_duration = 2
        self.fmin = fmin = -pllFreqMax
        self.fmax = fmax = pllFreqMax

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + 'airspy=0,sensitivity' )
        self.osmosdr_source_0.set_clock_source('gpsdo', 0)
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(pulse_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(gain, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)

        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(decimate_1, (taps1), 0, samp_rate)
        self.fir_filter_xxx_0_0_0 = filter.fir_filter_ccf(decimate_3, (taps3))
        self.fir_filter_xxx_0_0_0.declare_sample_delay(0)
        self.fir_filter_xxx_0_0 = filter.fir_filter_ccf(decimate_2, (taps2))
        self.fir_filter_xxx_0_0.declare_sample_delay(0)
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(1)
        self.blocks_moving_average_xx_0_0 = blocks.moving_average_cc(int(samp_rate4*pulse_duration), 1, int(samp_rate4*inter_pulse_duration/10.0))
        self.blocks_complex_to_mag_0_0 = blocks.complex_to_mag(1)
        self.analog_pll_refout_cc_0 = analog.pll_refout_cc(wnT, math.pi/(samp_rate4/2.0)*fmax, math.pi/(samp_rate4/2.0)*fmin)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_pll_refout_cc_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        self.connect((self.blocks_complex_to_mag_0_0, 0), (self, 0))
        self.connect((self.blocks_moving_average_xx_0_0, 0), (self.blocks_complex_to_mag_0_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.blocks_moving_average_xx_0_0, 0))
        self.connect((self.fir_filter_xxx_0_0, 0), (self.fir_filter_xxx_0_0_0, 0))
        self.connect((self.fir_filter_xxx_0_0_0, 0), (self.analog_pll_refout_cc_0, 0))
        self.connect((self.fir_filter_xxx_0_0_0, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        self.connect((self.fir_filter_xxx_0_0_0, 0), (self, 1))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.fir_filter_xxx_0_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))

    def get_final_decimation(self):
        return self.final_decimation

    def set_final_decimation(self, final_decimation):
        self.final_decimation = final_decimation
        self.set_decimate_3(self.final_decimation)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.osmosdr_source_0.set_gain(self.gain, 0)

    def get_pllFreqMax(self):
        return self.pllFreqMax

    def set_pllFreqMax(self, pllFreqMax):
        self.pllFreqMax = pllFreqMax
        self.set_fmin(-self.pllFreqMax)
        self.set_fmax(self.pllFreqMax)

    def get_pulse_duration(self):
        return self.pulse_duration

    def set_pulse_duration(self, pulse_duration):
        self.pulse_duration = pulse_duration
        self.blocks_moving_average_xx_0_0.set_length_and_scale(int(self.samp_rate4*self.pulse_duration), 1)

    def get_pulse_freq(self):
        return self.pulse_freq

    def set_pulse_freq(self, pulse_freq):
        self.pulse_freq = pulse_freq
        self.osmosdr_source_0.set_center_freq(self.pulse_freq, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_taps1(firdes.low_pass_2(1.0, self.samp_rate, 1.5e3, 128e3-1.5e3, 60.0, firdes.WIN_BLACKMAN_HARRIS, 6.76))
        self.set_samp_rate2(self.samp_rate/self.decimate_1)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)

    def get_wnT(self):
        return self.wnT

    def set_wnT(self, wnT):
        self.wnT = wnT
        self.analog_pll_refout_cc_0.set_loop_bandwidth(self.wnT)

    def get_decimate_1(self):
        return self.decimate_1

    def set_decimate_1(self, decimate_1):
        self.decimate_1 = decimate_1
        self.set_samp_rate2(self.samp_rate/self.decimate_1)

    def get_samp_rate2(self):
        return self.samp_rate2

    def set_samp_rate2(self, samp_rate2):
        self.samp_rate2 = samp_rate2
        self.set_taps2(firdes.low_pass_2(1.0, self.samp_rate2, 1.5e3, 16e3-1.5e3, 60.0, firdes.WIN_BLACKMAN_HARRIS, 6.76))
        self.set_samp_rate3(self.samp_rate2/self.decimate_2)

    def get_decimate_2(self):
        return self.decimate_2

    def set_decimate_2(self, decimate_2):
        self.decimate_2 = decimate_2
        self.set_samp_rate3(self.samp_rate2/self.decimate_2)

    def get_samp_rate3(self):
        return self.samp_rate3

    def set_samp_rate3(self, samp_rate3):
        self.samp_rate3 = samp_rate3
        self.set_taps3(firdes.low_pass_2(1.0, self.samp_rate3, 1.5e3, 0.3e3, 30.0, firdes.WIN_KAISER, 6.76/2))
        self.set_samp_rate4(self.samp_rate3/self.decimate_3)

    def get_taps3(self):
        return self.taps3

    def set_taps3(self, taps3):
        self.taps3 = taps3
        self.set_taps3_len(len(self.taps3))
        self.fir_filter_xxx_0_0_0.set_taps((self.taps3))

    def get_taps2(self):
        return self.taps2

    def set_taps2(self, taps2):
        self.taps2 = taps2
        self.set_taps2_len(len(self.taps2))
        self.fir_filter_xxx_0_0.set_taps((self.taps2))

    def get_taps1(self):
        return self.taps1

    def set_taps1(self, taps1):
        self.taps1 = taps1
        self.set_taps1_len(len(self.taps1))
        self.freq_xlating_fir_filter_xxx_0.set_taps((self.taps1))

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
        self.blocks_moving_average_xx_0_0.set_length_and_scale(int(self.samp_rate4*self.pulse_duration), 1)
        self.analog_pll_refout_cc_0.set_max_freq(math.pi/(self.samp_rate4/2.0)*self.fmax)
        self.analog_pll_refout_cc_0.set_min_freq(math.pi/(self.samp_rate4/2.0)*self.fmin)

    def get_inter_pulse_duration(self):
        return self.inter_pulse_duration

    def set_inter_pulse_duration(self, inter_pulse_duration):
        self.inter_pulse_duration = inter_pulse_duration

    def get_fmin(self):
        return self.fmin

    def set_fmin(self, fmin):
        self.fmin = fmin
        self.analog_pll_refout_cc_0.set_min_freq(math.pi/(self.samp_rate4/2.0)*self.fmin)

    def get_fmax(self):
        return self.fmax

    def set_fmax(self, fmax):
        self.fmax = fmax
        self.analog_pll_refout_cc_0.set_max_freq(math.pi/(self.samp_rate4/2.0)*self.fmax)
