#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 gr-VHFPulseSender2 author.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import math
import numpy
import time
from gnuradio import gr
from multiprocessing import Queue
import UDPThread
import TCPThread
import logging

class udp_sender_f(gr.sync_block):
    """
    docstring for block udp_sender_f
    """
    def __init__(self, channel_index, localhost):
        gr.sync_block.__init__(self, name="udp_sender_f", in_sig=[numpy.float32], out_sig=None)

        self.channelIndex = channel_index
        self.localhost = localhost

        self.tcpQueue = Queue()
        self.udpQueue = Queue()

        self.pulseDetectBase = None
        self.lastPulseTime = time.time()

        self.printOnce = True

    def work(self, input_items, output_items):
        for pulseValue in input_items[0]:
            sendPulse = False
            if pulseValue > 0:
                sendPulse = True
            elif time.time() - self.lastPulseTime > 3:
                sendPulse = True

            if sendPulse:
                print("Adding to queue")
                #if self.tcpThread.tcpClient:
                #    self.tcpQueue.put(pulseValue)
                #else:
                #    self.udpQueue.put(pulseValue)
                self.udpQueue.put(pulseValue)
                self.lastPulseTime = time.time()

        return len(input_items[0])


    def setPulseDetectBase(self, pulseDetectBase):
        print("setPulseDetectBase", pulseDetectBase)
        self.pulseDetectBase = pulseDetectBase
        self.udpThread = UDPThread.UDPThread(self.localhost == 1, self.udpQueue, self.channelIndex, pulseDetectBase)
        self.udpThread.start()
        #self.tcpThread = TCPThread.TCPThread(self.tcpQueue, self.channelIndex, pulseDetectBase)
        #self.tcpThread.start()
