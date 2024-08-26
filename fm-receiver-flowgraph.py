#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import osmosdr
import time

class fm_receiver(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "FM Receiver")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2e6
        self.channel_width = channel_width = 200e3
        self.channel_freq = channel_freq = 97.9e6
        self.audio_gain = audio_gain = 1

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + "hackrf"
        )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(channel_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            int(samp_rate / channel_width),
            firdes.low_pass(
                1,
                samp_rate,
                75e3,
                25e3,
                firdes.WIN_HAMMING,
                6.76))
        
        self.fm_demod = analog.wfm_rcv(
            quad_rate=channel_width,
            audio_decimation=1,
        )
        
        self.audio_sink_0 = audio.sink(48000, '', True)
        self.analog_agc_xx_0 = analog.agc_cc(1e-4, 1.0, 1.0)
        self.analog_agc_xx_0.set_max_gain(65536)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.osmosdr_source_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.analog_agc_xx_0, 0), (self.fm_demod, 0))
        self.connect((self.fm_demod, 0), (self.audio_sink_0, 0))

def main(top_block_cls=fm_receiver, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    tb.wait()

if __name__ == '__main__':
    main()
