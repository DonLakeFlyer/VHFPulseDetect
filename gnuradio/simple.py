#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Pulsedetectcmdlineudp
# GNU Radio version: 3.8.1.0

import os
import logging
import signal
import time

def main():
    def sig_handler(sig=None, frame=None):
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    while True:
        time.sleep(3)
        logging.debug("Loop")

if __name__ == '__main__':
    logging.basicConfig(filename='myapp.log', level=logging.DEBUG)
    main()
