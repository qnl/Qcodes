from qcodes import VisaInstrument
import numpy as np
from qcodes.utils.validators import Numbers
import time
"""Driver for the Agilent/Keysight Spectrum Analyzer E9010A"""


class E9010A(VisaInstrument):
    """
    This is the qcodes driver for Keysight/Agilent N5230A PNA-L Network Analyzer.
    This should be simple to alter to work with other keysight PNAs in the N52* family
    """

    def __init__(self, name, address, **kwargs):
        super().__init__(name, address, terminator='\n', **kwargs)

        self.add_parameter('get_trace',
                           label='Get Trace',
                           get_cmd=self._get_trace,
                           docstring='Gets the complex trace currently being sampled on the VNA')

        self.add_parameter('bandwidth',
                           label='Bandwidth',
                           get_cmd=':BAND?',
                           set_cmd=':BAND {:.16f}',
                           get_parser=float,
                           unit='Hz')

        self.add_parameter('video_bandwidth',
                           label='Video Bandwidth',
                           get_cmd=':BAND:VID?',
                           set_cmd=':BAND:VID {:.16f}',
                           get_parser=float,
                           unit='Hz')

        self.add_parameter('center_frequency',
                           label='Center Frequency',
                           get_cmd=self._get_center_freq,
                           set_cmd=self._set_center_freq,
                           get_parser=float,
                           unit='Hz')

        self.add_parameter('start_frequency',
                           label='Start Frequency',
                           get_cmd=':FREQ:STAR?',
                           set_cmd=':FREQ:STAR {}',
                           get_parser=float,
                           unit='Hz',
                           vals=Numbers(min_value=10e3, max_value=26.5e9))

        self.add_parameter('stop_frequency',
                           label='Stop Frequency',
                           get_cmd=':FREQ:STOP?',
                           set_cmd=':FREQ:STOP {}',
                           get_parser=float,
                           unit='Hz',
                           vals=Numbers(min_value=10e3, max_value=26.5e9))

        self.add_parameter('span',
                           label='Span',
                           get_cmd=self._get_span,
                           set_cmd=self._set_span,
                           get_parser=float,
                           unit='Hz')

        self.add_parameter('num_points',
                           label='Number of points',
                           get_cmd=':SWE:POIN?',
                           set_cmd=':SWE:POIN {}',
                           get_parser=int)

        self.add_parameter('num_averages',
                           label='Number of Averages of a sweep',
                           get_cmd=':AVER:COUN?',
                           set_cmd=':AVER:COUN {}',
                           get_parser=int)

        self.add_parameter('averaging',
                           label='Enable Averaging',
                           get_cmd=':AVER?',
                           set_cmd=':AVER {}',
                           val_mapping={'on': 1, 'off': 0})

        self.connect_message()

    def get_idn(self):
        IDN = self.ask_raw('*IDN?')
        vendor, model, serial, firmware = map(str.strip, IDN.split(','))
        IDN = {'vendor': vendor, 'model': model,
               'serial': serial, 'firmware': firmware}
        return IDN

    def _get_trace(self, verbose=False):

        # self.start_sweep(self.num_averages())
        # while not self.start_sweep():
        #     time.sleep(0.5)
        data = self._get_trace_nowait()
        # self.write('SENS:SWE:MODE CONT')

        return data

    def _get_trace_nowait(self):
        """This gets the current trace on the VNA without waiting for a sweep to finish"""

        # Change format to smith, and return the current full trace
        data = self.visa_handle.query_binary_values(':FORM INT,32;:FORM:BORD NORM;:TRAC? TRACE1',
                                                    container=np.array,
                                                    datatype='l',
                                                    is_big_endian=True)
        # Format it correctly, data is returned in milli-dBm
        data = np.array(data, dtype=float)/1000

        return data

    def _get_center_freq(self):
        return (self.start_frequency() + self.stop_frequency()) / 2

    def _set_center_freq(self, center_freq):

        # it's faster to calculate the values from scratch then to call other
        # functions such as get_span, start_frequency etc, as there are more calls
        # to the hardware, better to only have 2 calls to hardware and do more calculation
        # in this function. Even if this calculation is repeating calculations elsewhere
        start_freq = self.start_frequency()
        stop_freq = self.stop_frequency()

        span = stop_freq - start_freq

        self.start_frequency(center_freq - span / 2)
        self.stop_frequency(center_freq + span / 2)

    def _set_span(self, span):
        center_freq = self._get_center_freq()

        self.start_frequency(-span / 2 + center_freq)
        self.stop_frequency(span / 2 + center_freq)

    def _get_span(self):
        return self.stop_frequency() - self.start_frequency()