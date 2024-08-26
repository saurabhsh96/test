#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Mon Aug 26 14:07:02 2024
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import iio
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import wx


class top_block(grc_wxgui.top_block_gui):

    def __init__(self, audiodevice="dmix:CARD=monitor,DEV=0", decimation=1, hostname="127.0.0.1"):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Parameters
        ##################################################
        self.audiodevice = audiodevice
        self.decimation = decimation
        self.hostname = hostname

        ##################################################
        # Variables
        ##################################################
        self.sample_rate = sample_rate = 1536000
        self.fm_station = fm_station = 93500000

        ##################################################
        # Blocks
        ##################################################
        self._fm_station_text_box = forms.text_box(
        	parent=self.GetWin(),
        	value=self.fm_station,
        	callback=self.set_fm_station,
        	label="FM station",
        	converter=forms.int_converter(),
        )
        self.Add(self._fm_station_text_box)
        self.low_pass_filter_0 = filter.fir_filter_ccf(sample_rate / (384000 * decimation), firdes.low_pass(
        	1, sample_rate / decimation, 44100, 44100, firdes.WIN_HAMMING, 6.76))
        self.iio_fmcomms2_source_0 = iio.fmcomms2_source(hostname, fm_station, 1536000, decimation - 1, 20000000, True, True, False, False, 0x20000, True, True, True, "slow_attack", 64.0, "slow_attack", 64.0, "A_BALANCED")
        self.blocks_short_to_float_0_0 = blocks.short_to_float(1, 1)
        self.blocks_short_to_float_0 = blocks.short_to_float(1, 1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.audio_sink_0 = audio.sink(48000, audiodevice, True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=384000,
        	audio_decimation=8,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.blocks_float_to_complex_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.blocks_short_to_float_0, 0), (self.blocks_float_to_complex_0, 0))    
        self.connect((self.blocks_short_to_float_0_0, 0), (self.blocks_float_to_complex_0, 1))    
        self.connect((self.iio_fmcomms2_source_0, 0), (self.blocks_short_to_float_0, 0))    
        self.connect((self.iio_fmcomms2_source_0, 1), (self.blocks_short_to_float_0_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv_0, 0))    


    def get_audiodevice(self):
        return self.audiodevice

    def set_audiodevice(self, audiodevice):
        self.audiodevice = audiodevice

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.sample_rate / self.decimation, 44100, 44100, firdes.WIN_HAMMING, 6.76))

    def get_hostname(self):
        return self.hostname

    def set_hostname(self, hostname):
        self.hostname = hostname

    def get_sample_rate(self):
        return self.sample_rate

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.sample_rate / self.decimation, 44100, 44100, firdes.WIN_HAMMING, 6.76))

    def get_fm_station(self):
        return self.fm_station

    def set_fm_station(self, fm_station):
        self.fm_station = fm_station
        self._fm_station_text_box.set_value(self.fm_station)
        self.iio_fmcomms2_source_0.set_params(self.fm_station, 1536000, 20000000, True, True, True, "slow_attack", 64.0, "slow_attack", 64.0, "A_BALANCED")


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("", "--audiodevice", dest="audiodevice", type="string", default="dmix:CARD=monitor,DEV=0",
        help="Set Audio device [default=%default]")
    parser.add_option("", "--decimation", dest="decimation", type="intx", default=1,
        help="Set Decimation [default=%default]")
    parser.add_option("", "--hostname", dest="hostname", type="string", default="127.0.0.1",
        help="Set Hostname [default=%default]")
    (options, args) = parser.parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable realtime scheduling."
    tb = top_block(audiodevice=options.audiodevice, decimation=options.decimation, hostname=options.hostname)
    tb.Start(True)
    tb.Wait()
