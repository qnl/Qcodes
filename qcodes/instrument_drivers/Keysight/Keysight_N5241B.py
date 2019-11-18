from qcodes import VisaInstrument
import numpy as np
from qcodes.utils.validators import Numbers, Strings
import time
"""Driver for the Keysight PNA N5241B"""


# class N5241B(VisaInstrument):
#     """
#     This is the qcodes driver for Keysight/Agilent N5241B PNA-X Network Analyzer.
#     This should be simple to alter to work with other keysight PNAs
#     """
#
#     def __init__(self, name, address, **kwargs):
#         super().__init__(name, address, terminator='\n', **kwargs)
#         # self.write('CALC:PAR:DEF:EXT "MyMeas", S21')
#         self.add_parameter('get_trace',
#                            label='Get Trace',OUTP
#                            get_cmd=self._get_trace,
#                            docstring='Gets the complex trace currently being sampled on the VNA')
#
#         self.add_parameter('phase_offset',
#                            label='Phase Offset',
#                            get_cmd='CALC:OFFS:PHAS?',
#                            set_cmd='CALC:OFFS:PHAS {:.16f}',
#                            docstring='Global complex phase offset',
#                            vals=Numbers(-np.pi, np.pi),
#                            get_parser=float,
#                            unit='rad')
#
#         self.add_parameter('power',
#                            label='Power',
#                            get_cmd='SOUR:POW?',
#                            set_cmd='SOUR:POW {:.16f}',
#                            docstring='Output power of the VNA output port in dBm.',
#                            get_parser=float,
#                            unit='dBm')
#
#         self.add_parameter('rf_output',
#                            label='RF Output',
#                            docstring='RF Output power on or off.',
#                            get_cmd='OUTP?',
#                            set_cmd='OUTP {}',
#                            val_mapping={'on': 1, 'off': 0})
#
#         self.add_parameter('electrical_delay',
#                            label='Electrical Delay',
#                            get_cmd=':CALC1:CORR:EDEL:TIME?',
#                            set_cmd=':CALC1:CORR:EDEL:TIME {:.16f}',
#                            get_parser=float,
#                            unit='s')
#
#         self.add_parameter('bandwidth',
#                            label='Bandwidth',
#                            get_cmd=':SENS:BAND?',
#                            set_cmd=':SENS:BAND {:.16f}',
#                            get_parser=float,
#                            unit='Hz')
#
#         self.add_parameter('center_frequency',
#                            label='Center Frequency',
#                            get_cmd=':SENS:FREQ:CENT?',
#                            set_cmd=':SENS:FREQ:CENT {}',
#                            get_parser=float,
#                            unit='Hz')
#
#         self.add_parameter('start_frequency',
#                            label='Start Frequency',
#                            get_cmd=':SENS:FREQ:STAR?',
#                            set_cmd=':SENS:FREQ:STAR {}',
#                            get_parser=float,
#                            unit='Hz')
#
#         self.add_parameter('stop_frequency',
#                            label='Stop Frequency',
#                            get_cmd=':SENS:FREQ:STOP?',
#                            set_cmd=':SENS:FREQ:STOP {}',
#                            get_parser=float,
#                            unit='Hz')
#
#         self.add_parameter('span',
#                            label='Span',
#                            get_cmd=':SENS:FREQ:SPAN?',
#                            set_cmd=':SENS:FREQ:SPAN {}',
#                            get_parser=float,
#                            unit='Hz')
#
#         self.add_parameter('s_parameter',
#                            label='S parameter',
#                            docstring='Set the measured S parameter, allowed values are "S11", "S12", "S21", and "S22"',
#                            get_cmd=':CALC:PAR:CAT?',
#                            set_cmd=':CALC:PAR:DEL:ALL;CALC:PAR:DEF:EXT "MyMeas"  {}',
#                            get_parser=lambda x: x[1:-1].split(',')[1])
#
#         self.add_parameter('num_points',
#                            label='Number of points',
#                            get_cmd=':SENS:SWE:POIN?',
#                            set_cmd=':SENS:SWE:POIN  {}',
#                            get_parser=int)
#
#         self.add_parameter('num_averages',
#                            label='Number of Averages of a sweep',
#                            get_cmd=':SENS1:AVER:COUN?',
#                            set_cmd=':SENS1:AVER:COUN {}',
#                            get_parser=int)
#
#         self.add_parameter('averaging',
#                            label='Enable Averaging',
#                            get_cmd=':SENS:AVER?',
#                            set_cmd=':SENS:AVER {}',
#                            val_mapping={'on': 1, 'off': 0})
#
#         self.add_parameter('trigger_average_mode',
#                            label='Trigger Average Mode',
#                            get_cmd='SENSE:AVER:MODE?',
#                            set_cmd='SENSE:AVER:MODE {}',
#                            docstring="Sets the trigger averaging mode to point or sweep. One of ['poin', 'point', 'sweep']")
#
#         self.add_parameter('start_sweep',
#                            label='Start Sweep',
#                            get_cmd='*STB?',
#                            set_cmd=(':SENS:SWE:TIME:AUTO ON;'
#                                     ':SENS:AVER:CLE;'
#                                     '*CLS;*ESE 1;'
#                                     ':SENS:SWE:GRO:COUN {};'
#                                     ':SENS:SWE:MODE GRO;'
#                                     '*OPC'),
#                            get_parser=lambda x: int(x) & 32 == 32
#                            )
#
#         self.add_parameter('display_format',
#                            label='Display Format',
#                            get_cmd='CALC:FORM?',
#                            set_cmd='CALC:FORM {}',
#                            docstring="Sets the data format of the active trace. One of ['MLIN', 'MLOG', 'PHAS', 'UPH', 'IMAG', 'REAL', 'POL', 'SMIT', 'SADM', 'SWR', 'GDEL', 'KEL', 'FAHR', 'CEL']")
#
#         self.add_parameter('trigger_source',
#                            label='Trigger Source',
#                            get_cmd=':TRIG:SEQ:SOUR?',
#                            set_cmd='TRIG:SEQ:SOUR {}',
#                            docstring="Sets the trigger source to external, immediate (for continuous triggering) or manual. One of ['ext', 'imm', 'man']")
#
#         self.add_parameter('sweep_time',
#                            label='Sweep Time',
#                            get_cmd='SENS:SWE:TIME?',
#                            docstring='Queries the sweep time of a certain channel.',
#                            get_parser=float)
#
#         self.connect_message()
#
#     def get_idn(self):
#         IDN = self.ask_raw('*IDN?')
#         vendor, model, serial, firmware = map(str.strip, IDN.split(','))
#         IDN = {'vendor': vendor, 'model': model,
#                'serial': serial, 'firmware': firmware}
#         return IDN
#
#     def delete_measurement(self, measurement_name=None):
#         if measurement_name is None:
#             # delete all traces
#             self.write(r'calc:par:del:all')
#         else:
#             self.write("calc:par:del '%s'" % measurement_name)
#
#     def delete_trace(self, trace=None):
#         if trace is None:
#             query = "disp:wind:trac:del"
#         else:
#             query = "disp:wind:trac%d:del" % trace
#         self.write(query)
#
#     def auto_scale(self):
#         query = "DISP:WIND:TRAC:Y:AUTO"
#
#     def _get_trace(self, verbose=False):
#
#         self.start_sweep(self.num_averages())
#         while not self.start_sweep():
#             time.sleep(0.5)
#         data = self._get_trace_nowait()
#         self.write('SENS:SWE:MODE CONT')
#
#         return data
#
#     def _get_trace_nowait(self):
#         """This gets the current trace on the VNA without waiting for a sweep to finish"""
#         # Get the current viewing format
#         current_format = self.ask('CALC:FORM?')
#
#         # Change format to smith, and return the current full trace
#         data = self.visa_handle.query_binary_values('CALC:FORM SMIT;:FORM:DATA REAL,64;:CALC1:DATA? FDATA',
#                                                     container=np.array,
#                                                     datatype='d',
#                                                     is_big_endian=True)
#         # Format it correctly
#         data = data[::2] + 1j * data[1::2]
#
#         # return it to the original format
#         self.write(':CALC:FORM {}'.format(current_format))
#
#         return data
import numpy as np
from .N52xx import PNABase
from time import sleep
from qcodes.utils.validators import Ints, Numbers, Enum, Bool


class N5241B(PNABase):
    """
    This is the qcodes driver for Keysight/Agilent N5241B PNA-X Network Analyzer.
    This should be simple to alter to work with other keysight PNAs
    """

    min_freq = 10e6
    max_freq = 13.5e9
    min_power_port = -95
    min_power_src = -40
    max_power = 30
    power_limits_per_channel = {1: [min_power_port, max_power],
                                2: [min_power_port, max_power],
                                3: [min_power_src, max_power],
                                4: [min_power_src, max_power]}

    nports = 2

    def __init__(self, name, address, **kwargs):

        kwargs['min_freq'] = self.min_freq
        kwargs['max_freq'] = self.max_freq
        kwargs['min_power'] = self.min_power_port
        kwargs['max_power'] = self.max_power
        kwargs['nports'] = self.nports

        super().__init__(name, address, **kwargs)
        # self.add_parameter('power2',
        #                    label='Source 2 Power',
        #                    get_cmd='SOUR:POW3?',
        #                    get_parser=float,
        #                    set_cmd='SOUR:POW3 {:.2f}',
        #                    unit='dBm',
        #                    vals=Numbers(min_value=-30,
        #                                 max_value=30))
        self.add_parameter('power_on',
                           label='Source 2 Power',
                           get_cmd='OUTP?',
                           set_cmd='OUTP {}')
        self.add_parameter('power_coupling',
                           label='Source Power Coupling',
                           get_cmd='SOUR:POW:COUP?',
                           set_cmd='SOUR:POW:COUP  {}')

        for i in range(4):
            self.add_parameter(f'power_mode{i+1}',
                               label=f'Source {i+1} Power mode',
                               get_cmd=f'SOUR:POW{i+1}:MODE?',
                               set_cmd=f'SOUR:POW{i+1}'+':MODE {}',
                               )
        for i in range(4):
            self.add_parameter(f'power_{i+1}',
                               label=f'Source {i+1} Power',
                               get_cmd=f'SOUR:POW{i+1}?',
                               set_cmd=f'SOUR:POW{i+1} {{:.2f}}',
                               unit='dBm',
                               vals=Numbers(min_value=self.power_limits_per_channel[i+1][0],
                                            max_value=self.power_limits_per_channel[i+1][1]))
        self.add_parameter('display_format',
                          label='Display Format',
                          get_cmd='CALC:FORM?',
                          set_cmd='CALC:FORM {}',
                          docstring="Sets the data format of the active trace. One of ['MLIN', 'MLOG', 'PHAS', 'UPH', 'IMAG', 'REAL', 'POL', 'SMIT', 'SADM', 'SWR', 'GDEL', 'KEL', 'FAHR', 'CEL']")

        # self.add_parameter('electrical_delay',
        #                    label='Electrical Delay',
        #                    get_cmd=':CALC1:CORR:EDEL:TIME?',
        #                    set_cmd=':CALC1:CORR:EDEL:TIME {:.16f}',
        #                    get_parser=float,
        #                    unit='s')

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


        self.add_parameter('s_parameter',
                           label='S parameter',
                           docstring='Set the measured S parameter, allowed values are "S11", "S12", "S21", and "S22"',
                           get_cmd=':CALC:PAR:CAT?',
                           set_cmd='CALC:PAR:DEF:EXT "MyMeas"  {}; DISPlay:WINDow:TRACe:FEED "MyMeas"',
                           get_parser=lambda x: x[1:-1].split(',')[1])

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
        self.write('CALC:PAR:SEL 1')
        self.write('DISP:WIND:TRAC1:STAT ON')

        self._two_tone_mode = False
        self.power_coupling(0)
        self.power_mode1('Auto')
        self.power_mode2('Auto')
        self.power_mode3('OFF')
        self.power_mode4('OFF')

        # self.connect_message()


    def delete_measurement(self, measurement_name=None):

        if measurement_name is None:
            # delete all traces
            self.write(r'calc:par:del:all')
        else:
            self.write("calc:par:del '%s'" % measurement_name)

    def delete_trace(self, trace=None):
        if trace is None:
            query = "disp:wind:trac:del"
        else:
            query = "disp:wind:trac%d:del" % trace
        self.write(query)

    def s_parameter(self, s_param=None):
        """

        :param s_param: string, S Parameter to measure. If none, returns the current s-parameter
        :return:
        """
        if s_param is None:
            return self.ask('CALC:PAR:CAT?').split(",")[-1][:-1]  # Get s-parameter
        else:
            self.delete_measurement()
            self.delete_trace()
            self.write(f"CALCulate:PARameter:DEFine:EXT 'MyMeas',{s_param}")  # Define a measurement
            self.write("DISPlay:WINDow:TRACe:FEED 'MyMeas'")  # Create a trace for this measurement
            self.trigger_source('IMM')
            self.write('initiate:continuous 1')  # Set trigger continuous
            self.sweep_mode('CONT')

    def two_tone_mode(self, mode=None, two_tone_port=3, frequency=None):
        """
        Enter two tone mode, where two_tone_port will sweep and source 1 stays on a particular frequency.
        :param two_tone_port:
        :param mode:
        :param frequency:
        :return:
        """
        if mode is None:
            return self._two_tone_mode

        if mode:
            assert frequency is not None, "input a frequency!"
            self.write("SENSE:FOM:RANGE2:COUPLED 0") # First source
            self.write("SENSE:FOM:RANGE3:COUPLED 0") # Receiver
            self.write("SENSE:FOM:RANGE4:COUPLED 1") # Second source
            self.write("SENSE:FOM:RANGE2:FREQUENCY:START %f" % frequency) # Source
            self.write("SENSE:FOM:RANGE2:FREQUENCY:STOP %f" % frequency)
            self.write("SENSE:FOM:RANGE3:FREQUENCY:START %f" % frequency) # Receiver
            self.write("SENSE:FOM:RANGE3:FREQUENCY:STOP %f" % frequency)
            self.write('SENSE:FOM:STATE 1') # Set frequency offset mode to true
            getattr(self, f'power_mode{two_tone_port}')('ON')

        else:
            self.write("SENSE:FOM:RANGE2:COUPLED 1") # First source
            self.write("SENSE:FOM:RANGE3:COUPLED 1") # Receiver
            self.write("SENSE:FOM:RANGE4:COUPLED 0") # Second source
            self.write('SENSE:FOM:STATE 0') # Set frequency offset mode to true
            getattr(self, f'power_mode{two_tone_port}')('OFF')

        self._two_tone_mode = mode

    def get_complex_data(self):
        self.run_sweep()  # If you don't run this, then get_complex_data() will return cached data
        n_tries = 10
        for try_i in range(n_tries):
            try:
                data = self.visa_handle.query_binary_values('CALC:FORM SMIT;:FORM:DATA REAL,64;:CALC1:DATA? FDATA',
                                                   container=np.array,
                                                   datatype='d',
                                                   is_big_endian=True)
                break
            except Exception as e:
                if try_i == n_tries - 1:
                    raise e
                else:
                    print(f"get_complex_data fail count: {try_i+1}")
                    sleep(1)

        return data[::2] + 1j * data[1::2]


    def get_trace(self):
        """ Method to conform to qtrl frequency-domain VNA instrument API"""
        return self.get_complex_data()
