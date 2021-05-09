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
import logging

class udp_sender_f(gr.sync_block):
    """
    docstring for block udp_sender_f
    """
    def __init__(self):
        gr.sync_block.__init__(self, name="udp_sender_f", in_sig=[numpy.float32], out_sig=None)
        self.lastPulseTime  = time.time()
        self.udpQueue       = Queue()
        self.udpThread      = UDPThread.UDPThread(self.udpQueue)
        self.udpThread.start()

    def work(self, input_items, output_items):
        for pulseValue in input_items[0]:
            sendPulse = False
            if pulseValue > 0:
                sendPulse = True
            elif time.time() - self.lastPulseTime > 3:
                sendPulse = True

            if sendPulse:
                print("Adding to queue")
                self.udpQueue.put(pulseValue)
                self.lastPulseTime = time.time()

        return len(input_items[0])
