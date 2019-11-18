from qcodes import VisaInstrument
import numpy as np
from qcodes.utils.validators import Numbers
import time
import pyvisa
"""Driver for the Keysight ENA E5063A, adapted from the PNA N5230A"""


class E5063A(VisaInstrument):
    """
    This is the qcodes driver for Keysight/Agilent N5230A PNA-L Network Analyzer.
    This should be simple to alter to work with other keysight PNAs
    """

    def __init__(self, name, address, **kwargs):
        super().__init__(name, address, terminator='\n', **kwargs)

        self.add_parameter('get_trace',
                           label='Get Trace',
                           get_cmd=self._get_trace,
                           docstring='Gets the complex trace currently being sampled on the VNA')

        self.add_parameter('phase_offset',
                           label='Phase Offset',
                           get_cmd='CALC:CORR:OFFS:PHAS?',
                           set_cmd='CALC:CORR:OFFS:PHAS {:.16f}',
                           docstring='Global complex phase offset',
                           vals=Numbers(-180.0,180.0), #vals=Numbers(-np.pi, np.pi),
                           get_parser=float,
                           unit='deg') #unit='rad')

        self.add_parameter('power',
                           label='Power',
                           get_cmd='SOUR:POW?',
                           set_cmd='SOUR:POW {:.16f}',
                           docstring='Output power of the VNA output port in dBm.',
                           get_parser=float,
                           unit='dBm')

        self.add_parameter('rf_output',
                           label='RF Output',
                           docstring='RF Output power on or off.',
                           get_cmd='OUTP?',
                           set_cmd='OUTP {}',
                           val_mapping={'on': 1, 'off': 0})

        self.add_parameter('electrical_delay',
                           label='Electrical Delay',
                           get_cmd=':CALC:CORR:EDEL:TIME?',
                           set_cmd=':CALC:CORR:EDEL:TIME {:.16f}',
                           get_parser=float,
                           unit='s')

        self.add_parameter('bandwidth',
                           label='Bandwidth',
                           get_cmd=':SENS:BAND?',
                           set_cmd=':SENS:BAND {:.16f}',
                           get_parser=float,
                           unit='Hz')

        self.add_parameter('center_frequency',
                           label='Center Frequency',
                           get_cmd=':SENS:FREQ:CENT?',
                           set_cmd=':SENS:FREQ:CENT {}',
                           get_parser=float,
                           unit='Hz')

        self.add_parameter('start_frequency',
                           label='Start Frequency',
                           get_cmd=':SENS:FREQ:STAR?',
                           set_cmd=':SENS:FREQ:STAR {}',
                           get_parser=float,
                           unit='Hz')

        self.add_parameter('stop_frequency',
                           label='Stop Frequency',
                           get_cmd=':SENS:FREQ:STOP?',
                           set_cmd=':SENS:FREQ:STOP {}',
                           get_parser=float,
                           unit='Hz')

        self.add_parameter('span',
                           label='Span',
                           get_cmd=':SENS:FREQ:SPAN?',
                           set_cmd=':SENS:FREQ:SPAN {}',
                           get_parser=float,
                           unit='Hz')

        self.add_parameter('s_parameter',
                           label='S parameter',
                           docstring='Set the measured S parameter, allowed values are "S11", "S12", "S21", and "S22"',
                           get_cmd=':CALC:PAR:DEF?',
                           set_cmd=':CALC:PAR:DEF  {}')
                           #get_parser=lambda x: x[1:-1].split(',')[1])

        self.add_parameter('num_points',
                           label='Number of points',
                           get_cmd=':SENS:SWE:POIN?',
                           set_cmd=':SENS:SWE:POIN  {}',
                           get_parser=int)

        self.add_parameter('num_averages',
                           label='Number of Averages of a sweep',
                           get_cmd=':SENS1:AVER:COUN?',
                           set_cmd=':SENS1:AVER:COUN {}',
                           get_parser=int)

        self.add_parameter('averaging',
                           label='Enable Averaging',
                           get_cmd=':SENS:AVER?',
                           set_cmd=':SENS:AVER {}',
                           val_mapping={'on': 1, 'off': 0})

        self.add_parameter('start_sweep',
                           label='Start Sweep',
                           get_cmd='*OPC?',
                           set_cmd=(':SENS:SWE:TIME:AUTO ON;'
                                    ':SENS:AVER:CLE;'
                                    '*CLS;*ESE 1;'
                                    ':INIT1:CONT ON;'
                                    ':TRIG:AVER ON;'
                                    ':TRIG:SOUR BUS;'
                                    ':TRIG:SING;'))
                           #get_parser=lambda x: int(x) & 4 == 4
                           #)
        self.add_parameter('trigger',
                           label='Trigger',
                           docstring='Set trigger to hold, single, or continuous',
                           get_cmd='INIT:CONT?',
                           set_cmd='INIT:CONT {}',
                           val_mapping={'on': 1, 'off': 0})
        self.connect_message()

    def get_idn(self):
        IDN = self.ask_raw('*IDN?')
        vendor, model, serial, firmware = map(str.strip, IDN.split(','))
        IDN = {'vendor': vendor, 'model': model,
               'serial': serial, 'firmware': firmware}
        return IDN

    def _get_trace(self, verbose=False):

        self.start_sweep(self.num_averages())

        done = 0
        while not done:
            try:
                done = self.start_sweep()
            except pyvisa.VisaIOError:
                print('measuring...')
                time.sleep(0.5)
                # done = 0

        # while not self.start_sweep():
        #     time.sleep(0.5)
        data = self._get_trace_nowait()
        self.write(':INIT1:CONT ON;')

        return data

    def _get_trace_nowait(self):
        """This gets the current trace on the VNA without waiting for a sweep to finish"""
        # Get the current viewing format
        current_format = self.ask('CALC:FORM?')

        # # Change format to smith, and return the current full trace
        # data = self.visa_handle.query_binary_values('CALC:FORM SMIT;:FORM:DATA REAL,64;:CALC1:DATA? FDATA',
        #                                             container=np.array,
        #                                             datatype='d',
        #                                             is_big_endian=True)
        # Format it correctly
        # data = data[::2] + 1j * data[1::2]
        self.write('CALC1:FORM PLOG;')
        data = self.ask('CALC1:DATA:FDAT?;').split(',')
        # return it to the original format
        logmag = [float(d) for d in data[::2]]
        phase = [float(d) * np.pi / 180.0 for d in data[1::2]]
        self.write(':CALC:FORM {}'.format(current_format))

        return logmag, phase
