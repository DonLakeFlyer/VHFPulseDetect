#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Pulsedetectcmdlineudp
# GNU Radio version: 3.8.1.0

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PulseDetectBase import PulseDetectBase  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import VHFPulseDetect2
import VHFPulseSender2
import cmath
import math

class PulseDetectCmdLineUDP(gr.top_block):

    def __init__(self, channel_index=0, final_decimation=4, gain=21, localhost=0, pulse_duration=0.015, pulse_freq=146000000, samp_rate=3e6):
        gr.top_block.__init__(self, "Pulsedetectcmdlineudp")

        ##################################################
        # Parameters
        ##################################################
        self.channel_index = channel_index
        self.final_decimation = final_decimation
        self.gain = gain
        self.localhost = localhost
        self.pulse_duration = pulse_duration
        self.pulse_freq = pulse_freq
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.total_decimation = total_decimation = 16*16*final_decimation
        self.final_samp_rate = final_samp_rate = samp_rate/total_decimation

        ##################################################
        # Blocks
        ##################################################
        self.blocks_vector_sink_x_1_3 = blocks.vector_sink_f(1, 1024)
        self.blocks_vector_sink_x_1_2 = blocks.vector_sink_f(1, 1024)
        self.blocks_vector_sink_x_1_1_0 = blocks.vector_sink_f(1, 1024)
        self.blocks_vector_sink_x_1_1 = blocks.vector_sink_f(1, 1024)
        self.blocks_vector_sink_x_1 = blocks.vector_sink_f(1, 1024)
        self.blocks_vector_sink_x_0 = blocks.vector_sink_c(1, 1024)
        self.VHFPulseSender_udp_sender_f_0 = VHFPulseSender2.udp_sender_f(channel_index, localhost)
        self.VHFPulseDetect_pulse_detect_ff_0 = VHFPulseDetect2.pulse_detect_ff(2.5, pulse_duration, int(final_samp_rate))
        self.PulseDetectBase = PulseDetectBase(
            final_decimation=final_decimation,
            gain=gain,
            pllFreqMax=100,
            pulse_duration=pulse_duration,
            pulse_freq=pulse_freq,
            samp_rate=samp_rate,
            wnT=math.pi/4.0*0+0.635,
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.PulseDetectBase, 0), (self.VHFPulseDetect_pulse_detect_ff_0, 0))
        self.connect((self.PulseDetectBase, 1), (self.blocks_vector_sink_x_0, 0))
        self.connect((self.VHFPulseDetect_pulse_detect_ff_0, 0), (self.VHFPulseSender_udp_sender_f_0, 0))
        self.connect((self.VHFPulseDetect_pulse_detect_ff_0, 3), (self.blocks_vector_sink_x_1, 0))
        self.connect((self.VHFPulseDetect_pulse_detect_ff_0, 4), (self.blocks_vector_sink_x_1_1, 0))
        self.connect((self.VHFPulseDetect_pulse_detect_ff_0, 1), (self.blocks_vector_sink_x_1_1_0, 0))
        self.connect((self.VHFPulseDetect_pulse_detect_ff_0, 2), (self.blocks_vector_sink_x_1_2, 0))
        self.connect((self.VHFPulseDetect_pulse_detect_ff_0, 5), (self.blocks_vector_sink_x_1_3, 0))
        # The following line is modified from the .grc output. It connects the two objects  
        # such that udp_sender can change parameters in PulseDetectBase.  
        self.VHFPulseSender_udp_sender_f_0.setPulseDetectBase(self.PulseDetectBase)      

    def get_channel_index(self):
        return self.channel_index

    def set_channel_index(self, channel_index):
        self.channel_index = channel_index

    def get_final_decimation(self):
        return self.final_decimation

    def set_final_decimation(self, final_decimation):
        self.final_decimation = final_decimation
        self.set_total_decimation(16*16*self.final_decimation)
        self.PulseDetectBase.set_final_decimation(self.final_decimation)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.PulseDetectBase.set_gain(self.gain)

    def get_localhost(self):
        return self.localhost

    def set_localhost(self, localhost):
        self.localhost = localhost

    def get_pulse_duration(self):
        return self.pulse_duration

    def set_pulse_duration(self, pulse_duration):
        self.pulse_duration = pulse_duration
        self.PulseDetectBase.set_pulse_duration(self.pulse_duration)
        self.VHFPulseDetect_pulse_detect_ff_0.set_pulseDuration(self.pulse_duration)

    def get_pulse_freq(self):
        return self.pulse_freq

    def set_pulse_freq(self, pulse_freq):
        self.pulse_freq = pulse_freq
        self.PulseDetectBase.set_pulse_freq(self.pulse_freq)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_final_samp_rate(self.samp_rate/self.total_decimation)
        self.PulseDetectBase.set_samp_rate(self.samp_rate)

    def get_total_decimation(self):
        return self.total_decimation

    def set_total_decimation(self, total_decimation):
        self.total_decimation = total_decimation
        self.set_final_samp_rate(self.samp_rate/self.total_decimation)

    def get_final_samp_rate(self):
        return self.final_samp_rate

    def set_final_samp_rate(self, final_samp_rate):
        self.final_samp_rate = final_samp_rate
        self.VHFPulseDetect_pulse_detect_ff_0.set_sampleRate(int(self.final_samp_rate))


def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--channel-index", dest="channel_index", type=intx, default=0,
        help="Set channel_index [default=%(default)r]")
    parser.add_argument(
        "--final-decimation", dest="final_decimation", type=intx, default=4,
        help="Set final_decimation [default=%(default)r]")
    parser.add_argument(
        "--gain", dest="gain", type=intx, default=21,
        help="Set gain [default=%(default)r]")
    parser.add_argument(
        "--localhost", dest="localhost", type=intx, default=0,
        help="Set localhost [default=%(default)r]")
    parser.add_argument(
        "--pulse-duration", dest="pulse_duration", type=eng_float, default="15.0m",
        help="Set pulse_duration [default=%(default)r]")
    parser.add_argument(
        "--pulse-freq", dest="pulse_freq", type=intx, default=146000000,
        help="Set pulse_freq [default=%(default)r]")
    parser.add_argument(
        "--samp-rate", dest="samp_rate", type=eng_float, default="3.0M",
        help="Set samp_rate [default=%(default)r]")
    return parser


def main(top_block_cls=PulseDetectCmdLineUDP, options=None):
    if options is None:
        options = argument_parser().parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print("Error: failed to enable real-time scheduling.")
    tb = top_block_cls(channel_index=options.channel_index, final_decimation=options.final_decimation, gain=options.gain, localhost=options.localhost, pulse_duration=options.pulse_duration, pulse_freq=options.pulse_freq, samp_rate=options.samp_rate)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
